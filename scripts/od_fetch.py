"""Bounded local/remote loading for Organic Discovery."""
from __future__ import annotations

import hashlib
import http.client
import ipaddress
import socket
import ssl
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DEFAULT_TIMEOUT = 10.0
DEFAULT_MAX_BYTES = 2_000_000
DEFAULT_MAX_REDIRECTS = 5
DEFAULT_USER_AGENT = "OrganicDiscovery/0.4.0 (+https://github.com/wrg32786/aeo-seo-geo-marketing)"
_REDIRECTS = {301, 302, 303, 307, 308}


class AuditError(RuntimeError):
    """Expected input or fetch failure suitable for a concise CLI error."""


@dataclass(frozen=True)
class ResolvedAddress:
    family: int
    sockaddr: tuple[Any, ...]
    ip: str


@dataclass
class TargetDocument:
    requested: str
    display: str
    source_type: str
    final_url: str | None
    local_path: Path | None
    status: int
    headers: dict[str, str]
    redirects: list[dict[str, Any]]
    html_text: str
    content_sha256: str
    robots_text: str | None = None
    robots_source: str | None = None
    sitemap_text: str | None = None
    sitemap_source: str | None = None
    limitations: list[str] = field(default_factory=list)


def _public_ip(value: str) -> bool:
    ip = ipaddress.ip_address(value.split("%", 1)[0])
    return ip.is_global and not any((ip.is_private, ip.is_loopback, ip.is_link_local, ip.is_multicast, ip.is_reserved, ip.is_unspecified))


def resolve_public_host(hostname: str, port: int) -> list[ResolvedAddress]:
    try:
        rows = socket.getaddrinfo(hostname, port, type=socket.SOCK_STREAM)
    except socket.gaierror as exc:
        raise AuditError(f"DNS resolution failed for {hostname}: {exc}") from exc
    addresses: list[ResolvedAddress] = []
    seen: set[tuple[int, str]] = set()
    for family, socktype, _proto, _canon, sockaddr in rows:
        if socktype != socket.SOCK_STREAM or family not in (socket.AF_INET, socket.AF_INET6):
            continue
        ip = sockaddr[0]
        if not _public_ip(ip):
            raise AuditError(f"refusing non-public DNS result for {hostname}: {ip}")
        key = (family, ip)
        if key not in seen:
            seen.add(key)
            addresses.append(ResolvedAddress(family, sockaddr, ip))
    if not addresses:
        raise AuditError(f"no public TCP address found for {hostname}")
    return addresses


def validate_public_url(url: str) -> tuple[urllib.parse.SplitResult, list[ResolvedAddress]]:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        raise AuditError("remote targets must use http or https")
    if parsed.username or parsed.password:
        raise AuditError("URLs with embedded credentials are not allowed")
    if not parsed.hostname:
        raise AuditError("URL has no hostname")
    try:
        port = parsed.port or (443 if parsed.scheme.lower() == "https" else 80)
    except ValueError as exc:
        raise AuditError(f"invalid URL port: {exc}") from exc
    return parsed, resolve_public_host(parsed.hostname, port)


def _bounded_read(response: http.client.HTTPResponse, max_bytes: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = response.read(min(65_536, max_bytes + 1 - total))
        if not chunk:
            break
        chunks.append(chunk)
        total += len(chunk)
        if total > max_bytes:
            raise AuditError(f"response exceeds --max-bytes ({max_bytes})")
    return b"".join(chunks)


def _request(url: str, *, timeout: float, max_bytes: int, user_agent: str) -> tuple[int, str, dict[str, str], bytes]:
    parsed, addresses = validate_public_url(url)
    host = parsed.hostname or ""
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    target = urllib.parse.urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
    host_header = host if port in {80, 443} else f"{host}:{port}"
    last_error: OSError | ssl.SSLError | None = None
    for address in addresses:
        sock: socket.socket | ssl.SSLSocket | None = None
        try:
            sock = socket.socket(address.family, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect(address.sockaddr)
            if parsed.scheme == "https":
                sock = ssl.create_default_context().wrap_socket(sock, server_hostname=host)
            request = (
                f"GET {target} HTTP/1.1\r\nHost: {host_header}\r\nUser-Agent: {user_agent}\r\n"
                "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.1\r\n"
                "Accept-Encoding: identity\r\nConnection: close\r\n\r\n"
            ).encode("ascii", "strict")
            sock.sendall(request)
            response = http.client.HTTPResponse(sock)
            response.begin()
            headers = {key.lower(): value.strip() for key, value in response.getheaders()}
            body = _bounded_read(response, max_bytes)
            return response.status, response.reason, headers, body
        except (OSError, ssl.SSLError, http.client.HTTPException) as exc:
            last_error = exc
        finally:
            if sock is not None:
                try:
                    sock.close()
                except OSError:
                    pass
    raise AuditError(f"fetch failed for {url}: {last_error}")


def fetch_remote(url: str, *, timeout: float, max_bytes: int, max_redirects: int, user_agent: str) -> tuple[str, int, dict[str, str], bytes, list[dict[str, Any]]]:
    current = urllib.parse.urldefrag(url)[0]
    redirects: list[dict[str, Any]] = []
    seen: set[str] = set()
    for _ in range(max_redirects + 1):
        if current in seen:
            raise AuditError("redirect loop detected")
        seen.add(current)
        status, reason, headers, body = _request(current, timeout=timeout, max_bytes=max_bytes, user_agent=user_agent)
        if status not in _REDIRECTS:
            return current, status, headers, body, redirects
        location = headers.get("location")
        if not location:
            raise AuditError(f"HTTP {status} redirect has no Location header")
        if len(redirects) >= max_redirects:
            raise AuditError(f"redirect limit exceeded ({max_redirects})")
        next_url = urllib.parse.urljoin(current, location)
        validate_public_url(next_url)
        redirects.append({"from": current, "to": next_url, "status": status, "reason": reason})
        current = next_url
    raise AuditError("redirect limit exceeded")


def _decode(body: bytes, headers: dict[str, str]) -> str:
    content_type = headers.get("content-type", "")
    charset = "utf-8"
    for item in content_type.split(";")[1:]:
        key, sep, value = item.strip().partition("=")
        if sep and key.lower() == "charset" and value.strip():
            charset = value.strip().strip('"\'')
    try:
        return body.decode(charset, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


def _read_file(path: Path, max_bytes: int) -> bytes:
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise AuditError(f"cannot read {path}: {exc}") from exc
    if size > max_bytes:
        raise AuditError(f"file exceeds --max-bytes ({max_bytes})")
    try:
        return path.read_bytes()
    except OSError as exc:
        raise AuditError(f"cannot read {path}: {exc}") from exc


def _robots_sitemaps(text: str | None) -> list[str]:
    if not text:
        return []
    return [line.split(":", 1)[1].strip() for line in text.splitlines() if line.lower().startswith("sitemap:") and ":" in line]


def load_target(target: str, *, timeout: float = DEFAULT_TIMEOUT, max_bytes: int = DEFAULT_MAX_BYTES, max_redirects: int = DEFAULT_MAX_REDIRECTS, user_agent: str = DEFAULT_USER_AGENT) -> TargetDocument:
    if urllib.parse.urlsplit(target).scheme:
        final_url, status, headers, body, redirects = fetch_remote(target, timeout=timeout, max_bytes=max_bytes, max_redirects=max_redirects, user_agent=user_agent)
        parsed = urllib.parse.urlsplit(final_url)
        origin = f"{parsed.scheme}://{parsed.netloc}"
        limitations: list[str] = []
        robots_text = sitemap_text = robots_source = sitemap_source = None
        try:
            robots_source, _s, _h, robots_body, _r = fetch_remote(origin + "/robots.txt", timeout=timeout, max_bytes=max_bytes, max_redirects=max_redirects, user_agent=user_agent)
            robots_text = robots_body.decode("utf-8", errors="replace")
        except AuditError as exc:
            limitations.append(f"robots.txt unavailable: {exc}")
        sitemap_candidates = _robots_sitemaps(robots_text) or [origin + "/sitemap.xml"]
        try:
            sitemap_source, _s, _h, sitemap_body, _r = fetch_remote(sitemap_candidates[0], timeout=timeout, max_bytes=max_bytes, max_redirects=max_redirects, user_agent=user_agent)
            sitemap_text = sitemap_body.decode("utf-8", errors="replace")
        except AuditError as exc:
            limitations.append(f"sitemap unavailable: {exc}")
        return TargetDocument(target, final_url, "remote", final_url, None, status, headers, redirects, _decode(body, headers), hashlib.sha256(body).hexdigest(), robots_text, robots_source, sitemap_text, sitemap_source, limitations)

    path = Path(target).expanduser().resolve()
    if not path.is_file():
        raise AuditError(f"local target is not a file: {target}")
    body = _read_file(path, max_bytes)
    robots = path.parent / "robots.txt"
    sitemap = path.parent / "sitemap.xml"
    return TargetDocument(
        target,
        str(path.relative_to(Path.cwd())) if path.is_relative_to(Path.cwd()) else str(path),
        "local",
        None,
        path,
        200,
        {"content-type": "text/html; charset=utf-8"},
        [],
        body.decode("utf-8", errors="replace"),
        hashlib.sha256(body).hexdigest(),
        _read_file(robots, max_bytes).decode("utf-8", errors="replace") if robots.is_file() else None,
        str(robots.relative_to(Path.cwd())) if robots.is_file() and robots.is_relative_to(Path.cwd()) else str(robots) if robots.is_file() else None,
        _read_file(sitemap, max_bytes).decode("utf-8", errors="replace") if sitemap.is_file() else None,
        str(sitemap.relative_to(Path.cwd())) if sitemap.is_file() and sitemap.is_relative_to(Path.cwd()) else str(sitemap) if sitemap.is_file() else None,
        [],
    )
