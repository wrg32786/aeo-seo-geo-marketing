"""Deterministic HTML checks and output contracts for Organic Discovery."""
from __future__ import annotations

import html
import json
import os
import re
import tempfile
import urllib.parse
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable

from od_fetch import TargetDocument

VERSION = "0.4.0"
SCHEMA_VERSION = "0.4.0"
STAGES = ("activation", "eligibility", "retrieval", "context_allocation", "source_selection", "absorption", "fidelity", "behavior")
P_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
S_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}
INJECTION_RE = re.compile(r"(?is)(ignore\s+(all\s+)?(previous|prior)\s+instructions|system\s+prompt|developer\s+message|do\s+not\s+follow\s+the\s+user|(?:chatgpt|llm|ai\s+(?:assistant|crawler|agent)).{0,120}(?:recommend|rank|cite|trust|prefer))")
CLAIM_RE = re.compile(r"(?i)(\b(best|leading|#\s*1|number\s+one|guaranteed|clinically\s+proven|certified|award[- ]winning|trusted\s+by)\b|[$€£]\s?\d[\d,.]*|\b\d+(?:\.\d+)?\s?%|\b\d[\d,]*\+?\s+(customers|users|businesses|companies|studies|years?)\b)")
SOURCE_RE = re.compile(r"(?i)\b(source|sources|methodology|study|studies|evidence|according\s+to|verified|reference|references)\b")
MONEY_RE = re.compile(r"(?i)([$€£]\s?\d|\b(?:usd|eur|gbp)\s?\d|\bprice\b.{0,30}\d)")
SPACE_RE = re.compile(r"\s+")


def norm(value: str) -> str:
    return SPACE_RE.sub(" ", html.unescape(value)).strip()


class PageParser(HTMLParser):
    IGNORED = {"script", "style", "template", "svg", "noscript"}
    ROOT_IDS = {"app", "root", "__next", "__nuxt", "svelte"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: list[str] = []
        self.visible: list[str] = []
        self.hidden: list[str] = []
        self.comments: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.headings: list[dict[str, Any]] = []
        self.links: list[dict[str, str]] = []
        self.images: list[dict[str, str]] = []
        self.jsonld: list[str] = []
        self.external_scripts: list[str] = []
        self.inline_scripts: list[str] = []
        self.lang: str | None = None
        self.framework_roots: dict[str, list[str]] = {}
        self.has_article = False
        self.times: list[str] = []
        self._stack: list[tuple[str, bool, str | None]] = []
        self._heading: tuple[int, list[str]] | None = None
        self._anchor: dict[str, Any] | None = None
        self._in_title = False
        self._script_type: str | None = None
        self._script: list[str] = []

    @staticmethod
    def attrs(rows: list[tuple[str, str | None]]) -> dict[str, str]:
        return {key.lower(): (value or "") for key, value in rows}

    @staticmethod
    def hidden_attr(attrs: dict[str, str]) -> bool:
        style = attrs.get("style", "").replace(" ", "").lower()
        return "hidden" in attrs or attrs.get("aria-hidden", "").lower() == "true" or any(token in style for token in ("display:none", "visibility:hidden", "opacity:0"))

    def handle_starttag(self, tag: str, rows: list[tuple[str, str | None]]) -> None:
        tag = tag.lower(); attrs = self.attrs(rows)
        parent_hidden = self._stack[-1][1] if self._stack else False
        hidden = parent_hidden or self.hidden_attr(attrs)
        parent_root = self._stack[-1][2] if self._stack else None
        root = attrs.get("id", "").lower() if attrs.get("id", "").lower() in self.ROOT_IDS else parent_root
        if root: self.framework_roots.setdefault(root, [])
        self._stack.append((tag, hidden, root))
        if tag == "html" and attrs.get("lang"): self.lang = attrs["lang"].strip()
        elif tag == "title": self._in_title = True
        elif tag == "meta": self.meta.append(attrs)
        elif tag == "link" and "canonical" in attrs.get("rel", "").lower().split() and attrs.get("href"): self.canonicals.append(attrs["href"].strip())
        elif re.fullmatch(r"h[1-6]", tag): self._heading = (int(tag[1]), [])
        elif tag == "a": self._anchor = {"href": attrs.get("href", "").strip(), "aria_label": attrs.get("aria-label", "").strip(), "parts": []}
        elif tag == "img": self.images.append({"src": attrs.get("src", "").strip(), "alt": attrs.get("alt", "").strip()})
        elif tag == "script": self._script_type = attrs.get("type", "").lower(); self._script = []; self.external_scripts += [attrs["src"].strip()] if attrs.get("src") else []
        elif tag == "article": self.has_article = True
        elif tag == "time": self.times.append(attrs.get("datetime", "").strip())

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title": self._in_title = False
        elif re.fullmatch(r"h[1-6]", tag) and self._heading:
            level, parts = self._heading; self.headings.append({"level": level, "text": norm(" ".join(parts))}); self._heading = None
        elif tag == "a" and self._anchor:
            self.links.append({"href": self._anchor["href"], "text": norm(" ".join(self._anchor["parts"])), "aria_label": self._anchor["aria_label"]}); self._anchor = None
        elif tag == "script":
            raw = "".join(self._script).strip()
            if self._script_type == "application/ld+json" and raw: self.jsonld.append(raw)
            elif raw: self.inline_scripts.append(raw)
            self._script_type = None; self._script = []
        if self._stack:
            for index in range(len(self._stack) - 1, -1, -1):
                if self._stack[index][0] == tag:
                    del self._stack[index:]; break

    def handle_data(self, data: str) -> None:
        if self._script_type is not None: self._script.append(data); return
        text = norm(data)
        if not text: return
        if self._in_title: self.title.append(text)
        if self._heading: self._heading[1].append(text)
        if self._anchor: self._anchor["parts"].append(text)
        tag, hidden, root = self._stack[-1] if self._stack else ("", False, None)
        if tag in self.IGNORED: return
        (self.hidden if hidden else self.visible).append(text)
        if root: self.framework_roots[root].append(text)

    def handle_comment(self, data: str) -> None:
        text = norm(data)
        if text: self.comments.append(text)


def meta_values(parser: PageParser, key: str) -> list[str]:
    key = key.lower(); values = []
    for item in parser.meta:
        name = (item.get("name") or item.get("property") or item.get("http-equiv") or "").lower()
        if name == key and item.get("content"): values.append(item["content"].strip())
    return values


def parse_json_ld(blocks: Iterable[str]) -> tuple[list[Any], list[dict[str, str]]]:
    docs: list[Any] = []; errors: list[dict[str, str]] = []
    for index, raw in enumerate(blocks, 1):
        try: docs.append(json.loads(raw))
        except json.JSONDecodeError as exc: errors.append({"block": str(index), "error": f"line {exc.lineno}, column {exc.colno}: {exc.msg}"})
    return docs, errors


def iter_json_nodes(value: Any) -> Iterable[dict[str, Any]]:
    if isinstance(value, dict):
        yield value
        for child in value.values(): yield from iter_json_nodes(child)
    elif isinstance(value, list):
        for child in value: yield from iter_json_nodes(child)


def json_ld_types(docs: Iterable[Any]) -> list[str]:
    found: set[str] = set()
    for node in iter_json_nodes(list(docs)):
        values = node.get("@type", [])
        if isinstance(values, str): values = [values]
        if isinstance(values, list): found.update(str(value) for value in values if value)
    return sorted(found)


def important_schema_values(docs: Iterable[Any]) -> list[dict[str, str]]:
    fields = ("name", "headline", "description", "price", "priceCurrency", "ratingValue", "reviewCount", "datePublished", "dateModified", "author")
    out: list[dict[str, str]] = []
    for node in iter_json_nodes(list(docs)):
        for field in fields:
            value = node.get(field)
            if isinstance(value, (str, int, float)) and str(value).strip(): out.append({"field": field, "value": str(value).strip()})
            elif field == "author" and isinstance(value, dict) and value.get("name"): out.append({"field": field, "value": str(value["name"]).strip()})
    return out


def parse_sitemap(text: str | None) -> dict[str, Any]:
    if not text: return {"present": False, "valid": None, "urls": [], "error": None}
    try:
        root = ET.fromstring(text)
        urls = [norm(node.text or "") for node in root.iter() if node.tag.rsplit("}", 1)[-1] == "loc" and norm(node.text or "")]
        return {"present": True, "valid": True, "urls": urls, "error": None}
    except ET.ParseError as exc:
        return {"present": True, "valid": False, "urls": [], "error": str(exc)}


def robots_controls(document: TargetDocument) -> list[dict[str, Any]]:
    controls = []
    for crawler, purpose in (("Googlebot", "search"), ("bingbot", "search"), ("OAI-SearchBot", "search_answer"), ("Claude-SearchBot", "search_answer"), ("PerplexityBot", "search_answer"), ("GPTBot", "training"), ("ClaudeBot", "training"), ("Google-Extended", "model_use")):
        allowed: bool | None = None
        if document.robots_text:
            parser = urllib.robotparser.RobotFileParser(); parser.parse(document.robots_text.splitlines())
            path = urllib.parse.urlsplit(document.final_url or "/").path or "/"
            allowed = parser.can_fetch(crawler, path)
        controls.append({"crawler": crawler, "purpose": purpose, "allowed": allowed})
    return controls


def _finding(code: str, priority: str, severity: str, stage: str, title: str, detail: str, evidence: dict[str, Any], owner: str, risk: str, change: list[str], acceptance: list[str], rollback: list[str]) -> dict[str, Any]:
    return {"code": code, "priority": priority, "severity": severity, "stage": stage, "title": title, "detail": detail, "evidence": evidence, "owner": owner, "risk": risk, "change": change, "acceptance": acceptance, "rollback": rollback}


def _add(findings: list[dict[str, Any]], *args: Any) -> None:
    findings.append(_finding(*args))


def _same_url(left: str, right: str) -> bool:
    def clean(value: str) -> str:
        parsed = urllib.parse.urlsplit(value)
        port = parsed.port
        netloc = (parsed.hostname or "").lower()
        if port and port not in {80, 443}: netloc += f":{port}"
        path = parsed.path or "/"
        if path != "/": path = path.rstrip("/")
        return urllib.parse.urlunsplit((parsed.scheme.lower(), netloc, path, parsed.query, ""))
    return clean(left) == clean(right)


def audit_document(document: TargetDocument, queries: list[str] | None = None) -> tuple[dict[str, Any], list[dict[str, Any]], str]:
    parser = PageParser(); parser.feed(document.html_text); parser.close()
    visible = norm(" ".join(parser.visible)); hidden = norm(" ".join(parser.hidden)); title = norm(" ".join(parser.title))
    visible_lower = visible.casefold(); findings: list[dict[str, Any]] = []
    robots = robots_controls(document); sitemap = parse_sitemap(document.sitemap_text)
    docs, json_errors = parse_json_ld(parser.jsonld); schema_types = json_ld_types(docs); schema_values = important_schema_values(docs)

    if document.status >= 400:
        _add(findings, "http.error_status", "P0", "critical", "eligibility", "Page is not successfully reachable", f"The target returned HTTP {document.status}.", {"status": document.status}, "engineering", "high", ["restore a stable successful response for the canonical asset"], ["target returns a successful HTML response"], ["revert the routing/deployment change if availability worsens"])
    content_type = document.headers.get("content-type", "")
    if document.source_type == "remote" and "html" not in content_type.lower():
        _add(findings, "http.non_html", "P1", "high", "eligibility", "Response is not identified as HTML", f"Content-Type is {content_type or 'missing'}.", {"content_type": content_type}, "engineering", "low", ["serve the canonical page with the correct HTML content type"], ["Content-Type identifies HTML and extraction still matches the visible page"], ["restore the previous response headers"])

    blocked_search = [row["crawler"] for row in robots if row["purpose"] == "search" and row["allowed"] is False]
    blocked_ai = [row["crawler"] for row in robots if row["purpose"] == "search_answer" and row["allowed"] is False]
    if blocked_search:
        _add(findings, "robots.search_blocked", "P0", "critical", "eligibility", "Conventional search crawlers are blocked", ", ".join(blocked_search) + " cannot fetch the target path.", {"crawlers": blocked_search, "robots_source": document.robots_source}, "engineering", "high", ["change robots rules only if the page is intended for public search"], ["the intended search crawlers can fetch the target path"], ["restore the prior robots policy if exposure was intentional"])
    if blocked_ai:
        _add(findings, "robots.ai_search_blocked", "P1", "high", "eligibility", "AI search crawlers are blocked", ", ".join(blocked_ai) + " cannot fetch the target path.", {"crawlers": blocked_ai, "robots_source": document.robots_source}, "engineering", "medium", ["allow only the search-answer crawlers the owner intentionally supports"], ["approved AI search crawlers can fetch the path while training policy remains unchanged"], ["restore the prior per-crawler rules"])

    directives = " ".join(meta_values(parser, "robots") + meta_values(parser, "googlebot") + [document.headers.get("x-robots-tag", "")]).lower()
    if "noindex" in directives:
        _add(findings, "index.noindex", "P0", "critical", "eligibility", "Indexing is explicitly disabled", "A meta or header directive contains noindex.", {"directives": directives}, "engineering", "high", ["remove noindex only if this is the canonical public asset"], ["noindex is absent from the final response and intended crawler view"], ["restore noindex if publication was not approved"])

    canonicals = [urllib.parse.urljoin(document.final_url or "file:///", value) for value in parser.canonicals]
    if not canonicals:
        _add(findings, "canonical.missing", "P2", "medium", "eligibility", "Canonical URL is missing", "No canonical link was found in initial HTML.", {}, "engineering", "low", ["add one self-referential canonical when the page has a stable public URL"], ["exactly one intended canonical is present"], ["remove the canonical if the URL strategy is not approved"])
    elif len(canonicals) > 1:
        _add(findings, "canonical.multiple", "P1", "high", "eligibility", "Multiple canonical URLs conflict", f"Found {len(canonicals)} canonical links.", {"canonicals": canonicals}, "engineering", "medium", ["emit one canonical URL from the shared template"], ["exactly one canonical remains"], ["restore the prior template while routing is reviewed"])
    elif document.source_type == "local":
        path = urllib.parse.urlsplit(canonicals[0]).path.rstrip("/")
        if path and not (path.endswith("/index.html") or path.endswith("/")):
            _add(findings, "canonical.local_fixture_mismatch", "P0", "high", "eligibility", "Canonical conflicts with the audited local asset", f"The local index fixture declares {canonicals[0]}.", {"canonical": canonicals[0]}, "engineering", "medium", ["set the canonical to the deployed URL represented by this file"], ["the canonical resolves to the intended deployed page"], ["restore the previous canonical if the deployment mapping differs"])
    elif document.final_url and not _same_url(canonicals[0], document.final_url):
        _add(findings, "canonical.mismatch", "P1", "high", "eligibility", "Canonical points away from the fetched page", f"Fetched {document.final_url}, canonical {canonicals[0]}.", {"canonical": canonicals[0], "final_url": document.final_url}, "engineering", "medium", ["choose the intended canonical and align redirects, links, and sitemap"], ["final URL and canonical agree"], ["restore prior routing if consolidation is not intended"])

    words = visible.split()
    if len(words) < 60 and (parser.external_scripts or any(not norm(" ".join(parts)) for parts in parser.framework_roots.values())):
        _add(findings, "rendering.javascript_only_risk", "P1", "high", "eligibility", "Core answer may require JavaScript", f"Only {len(words)} visible words were present in initial HTML while client scripts/framework roots were detected.", {"visible_words": len(words), "external_scripts": parser.external_scripts, "framework_roots": sorted(parser.framework_roots)}, "engineering", "medium", ["render the primary answer, offer facts, and links in initial HTML"], ["initial HTML contains the same core facts available after rendering"], ["revert to the prior rendering path if hydration or functionality regresses"])

    if not title:
        _add(findings, "metadata.title_missing", "P1", "high", "eligibility", "Document title is missing", "Initial HTML has no non-empty title.", {}, "content", "low", ["add a concise intent-aligned title"], ["one non-empty title is present"], ["restore the previous title"])
    if not meta_values(parser, "description"):
        _add(findings, "metadata.description_missing", "P2", "medium", "eligibility", "Meta description is missing", "No meta description was found.", {}, "content", "low", ["add a truthful summary for search snippets"], ["one visible-content-aligned description is present"], ["remove it if the template duplicates or misstates the page"])
    if not parser.lang:
        _add(findings, "metadata.lang_missing", "P2", "medium", "eligibility", "Document language is missing", "The html element has no lang value.", {}, "engineering", "low", ["set the correct BCP 47 language tag"], ["the html element declares the page language"], ["restore the prior language routing if locale detection regresses"])
    if not meta_values(parser, "viewport"):
        _add(findings, "accessibility.viewport_missing", "P3", "low", "eligibility", "Viewport metadata is missing", "No viewport meta element was found.", {}, "engineering", "low", ["add a standard responsive viewport declaration"], ["mobile layout remains usable and viewport metadata is present"], ["remove the change if it breaks intentional embedded behavior"])

    h1s = [item for item in parser.headings if item["level"] == 1 and item["text"]]
    if not h1s:
        _add(findings, "headings.h1_missing", "P2", "medium", "eligibility", "Primary heading is missing", "No non-empty H1 was found.", {}, "content", "low", ["add one descriptive primary heading"], ["one useful H1 is present"], ["restore the prior heading if layout or semantics regress"])
    elif len(h1s) > 1:
        _add(findings, "headings.multiple_h1", "P2", "medium", "eligibility", "Multiple primary headings dilute page purpose", f"Found {len(h1s)} H1 elements.", {"headings": [row["text"] for row in h1s]}, "content", "low", ["retain one page-level H1 and demote subordinate headings"], ["one descriptive H1 remains"], ["restore previous heading levels if accessibility testing finds a regression"])
    levels = [row["level"] for row in parser.headings if row["text"]]
    if any(current > previous + 1 for previous, current in zip(levels, levels[1:])):
        _add(findings, "headings.level_skip", "P3", "low", "eligibility", "Heading levels skip hierarchy", "The heading outline jumps by more than one level.", {"levels": levels}, "content", "low", ["make heading levels reflect document hierarchy"], ["the heading outline has no unexplained jumps"], ["restore previous levels if component semantics require another hierarchy"])

    empty_links = [row for row in parser.links if row["href"] and not (row["text"] or row["aria_label"])]
    if empty_links:
        _add(findings, "links.empty_anchor", "P2", "medium", "eligibility", "Links lack accessible descriptive text", f"Found {len(empty_links)} non-empty links with no text or aria-label.", {"examples": empty_links[:5]}, "engineering", "low", ["add descriptive link text or an accessible name"], ["every actionable link has an accessible name"], ["restore the prior component if navigation behavior regresses"])
    missing_alt = [row for row in parser.images if row["src"] and not row["alt"]]
    if missing_alt:
        _add(findings, "images.alt_missing", "P2", "medium", "eligibility", "Images are missing alternative text", f"Found {len(missing_alt)} images without alt text.", {"examples": missing_alt[:5]}, "content", "low", ["add useful alt text or an explicit empty alt for decorative images"], ["each image has an intentional alt value"], ["restore prior markup if assistive-technology testing regresses"])

    if sitemap["present"] and sitemap["valid"] is False:
        _add(findings, "sitemap.invalid", "P1", "high", "eligibility", "Sitemap XML is invalid", sitemap["error"] or "XML parsing failed.", {"sitemap_source": document.sitemap_source}, "engineering", "low", ["repair the sitemap XML"], ["the sitemap parses and lists canonical public URLs"], ["restore the last valid sitemap"])
    elif sitemap["valid"] and document.source_type == "local" and not any(url.rstrip("/").endswith(("/", "/index.html")) for url in sitemap["urls"]):
        _add(findings, "sitemap.target_missing", "P2", "medium", "eligibility", "Audited page is absent from the sitemap fixture", "The sibling sitemap does not contain the represented index URL.", {"sitemap_urls": sitemap["urls"]}, "engineering", "low", ["add the canonical deployed URL to the sitemap"], ["the canonical target appears exactly once"], ["remove the entry if the page should not be indexed"])
    elif sitemap["valid"] and document.final_url and not any(_same_url(url, document.final_url) for url in sitemap["urls"]):
        _add(findings, "sitemap.target_missing", "P2", "medium", "eligibility", "Fetched page is absent from the sitemap", "The final URL is not listed in the sampled sitemap.", {"final_url": document.final_url, "sitemap_source": document.sitemap_source}, "engineering", "low", ["add the intended canonical URL when sitemap inclusion is appropriate"], ["the final canonical URL is listed once"], ["remove the entry if publication is reversed"])

    if json_errors:
        _add(findings, "schema.invalid_jsonld", "P1", "high", "fidelity", "JSON-LD cannot be parsed", f"Found {len(json_errors)} invalid JSON-LD block(s).", {"errors": json_errors}, "engineering", "low", ["repair or remove invalid JSON-LD"], ["all JSON-LD blocks parse successfully"], ["restore the last valid structured-data block"])
    mismatches = [row for row in schema_values if row["field"] in {"name", "price", "priceCurrency", "ratingValue", "reviewCount"} and norm(row["value"]).casefold() not in visible_lower]
    if mismatches:
        _add(findings, "schema.visible_mismatch", "P1", "high", "fidelity", "Structured data contains unsupported visible facts", "Important schema values are absent from visible initial content.", {"mismatches": mismatches[:10], "types": schema_types}, "content", "high", ["remove unsupported values or render the verified facts visibly"], ["visible copy and structured data agree for every material value"], ["remove the changed markup if facts cannot be maintained"])

    injection_sources = [value for value in (hidden, *parser.comments, *parser.inline_scripts) if INJECTION_RE.search(value)]
    if injection_sources:
        _add(findings, "manipulation.hidden_instruction", "P0", "critical", "fidelity", "Hidden machine-targeted instructions were detected", "Hidden/comment/script content appears to instruct an AI or crawler how to rank, cite, or respond.", {"examples": injection_sources[:3]}, "security", "high", ["remove the hidden instruction and review its origin"], ["the pattern is absent from source and rendered output"], ["restore a clean known-good revision"])
    if len(hidden.split()) >= 40:
        _add(findings, "manipulation.substantial_hidden_text", "P1", "high", "fidelity", "Substantial hidden text may create content disparity", f"Found {len(hidden.split())} hidden words.", {"hidden_words": len(hidden.split())}, "security", "medium", ["remove hidden substantive content or make legitimate content visible"], ["hidden content is limited to functional/accessibility needs"], ["restore prior markup if an accessibility feature was misclassified"])

    external_links = [row for row in parser.links if urllib.parse.urlsplit(row["href"]).scheme in {"http", "https"}]
    claim_sentences = [sentence for sentence in re.split(r"(?<=[.!?])\s+", visible) if CLAIM_RE.search(sentence)]
    if claim_sentences and not SOURCE_RE.search(visible) and not external_links:
        _add(findings, "claims.provenance_gap", "P1", "high", "fidelity", "Material claims lack visible provenance", "Numeric, superlative, certification, or performance claims appear without visible sourcing.", {"examples": claim_sentences[:5]}, "content", "high", ["verify each material claim and add visible source/method/limitations or remove it"], ["every material claim has an approved source and visible qualification"], ["remove the unsupported claim if verification fails"])
    if re.search(r"(?i)\b(buy|order|pricing|product|service|plan)\b", visible) and not MONEY_RE.search(visible):
        _add(findings, "offer.material_fact_gap", "P2", "medium", "fidelity", "Commercial offer omits a material price or availability fact", "The page presents an offer but no visible price or explicit availability path was detected.", {}, "content", "medium", ["show current price/availability or clearly explain how to obtain it"], ["the offer exposes accurate current commercial terms"], ["restore the prior copy if terms cannot be maintained"])
    author_values = meta_values(parser, "author") + [row["value"] for row in schema_values if row["field"] == "author"]
    date_values = parser.times + [row["value"] for row in schema_values if row["field"] in {"datePublished", "dateModified"}]
    if parser.has_article and not author_values:
        _add(findings, "article.author_missing", "P2", "medium", "fidelity", "Article authorship is unclear", "Article content has no visible/meta/schema author signal.", {}, "content", "low", ["identify the accountable author or organization when truthful"], ["authorship is visible and machine-readable consistently"], ["remove attribution if permission cannot be verified"])
    if parser.has_article and not any(date_values):
        _add(findings, "article.date_missing", "P2", "medium", "fidelity", "Article date is unclear", "Article content has no publication or modified date signal.", {}, "content", "low", ["add a truthful publication or update date"], ["visible and structured dates agree"], ["remove the date if it cannot be verified"])

    for query in queries or []:
        terms = {term for term in re.findall(r"[a-z0-9]+", query.casefold()) if len(term) > 2}
        covered = sorted(term for term in terms if term in visible_lower)
        if terms and len(covered) / len(terms) < 0.35:
            _add(findings, "content.query_gap", "P2", "medium", "fidelity", "Target query is weakly represented in initial content", f"The page visibly covers {len(covered)} of {len(terms)} meaningful query terms.", {"query": query, "covered_terms": covered, "missing_terms": sorted(terms - set(covered))}, "content", "low", ["answer the underlying user job with verified content rather than keyword stuffing"], ["a reviewer can locate a direct useful answer for the query"], ["revert the section if it harms intent clarity or duplicates another page"])

    findings.sort(key=lambda row: (P_ORDER[row["priority"]], S_ORDER[row["severity"]], row["stage"], row["code"], row["title"]))
    for index, row in enumerate(findings, 1): row["id"] = f"F-{index:03d}"
    stages = build_stages(findings)
    counts = Counter(row["priority"] for row in findings)
    earliest = next((stage for stage in STAGES if stages[stage]["status"] in {"blocked", "weak"}), None)
    audit = {
        "schema_version": SCHEMA_VERSION,
        "tool": {"name": "organic-discovery", "version": VERSION},
        "target": {"requested": document.requested, "display": document.display, "source_type": document.source_type, "final_url": document.final_url, "http_status": document.status, "content_type": document.headers.get("content-type"), "content_sha256": document.content_sha256, "redirects": document.redirects},
        "queries": queries or [],
        "summary": {"earliest_failing_stage": earliest, "finding_count": len(findings), "finding_counts_by_priority": {key: counts.get(key, 0) for key in ("P0", "P1", "P2", "P3")}, "opaque_score": None},
        "stages": stages,
        "extraction": {"title": title or None, "description": (meta_values(parser, "description") or [None])[0], "language": parser.lang, "canonical_urls": canonicals, "visible_word_count": len(words), "heading_count": len(parser.headings), "link_count": len(parser.links), "image_count": len(parser.images), "jsonld_types": schema_types, "robots_controls": robots, "sitemap": sitemap},
        "findings": findings,
        "limitations": document.limitations + ["Initial HTML parser; no browser rendering or index/citation observation.", "Heuristic claim and hidden-instruction checks require human review."],
    }
    orders = build_work_orders(findings, document.display)
    return audit, orders, render_report(audit, orders)


def build_stages(findings: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for stage in STAGES:
        related = [row for row in findings if row["stage"] == stage]
        if stage not in {"eligibility", "fidelity"}:
            out[stage] = {"status": "unknown", "evidence": "not observable from a deterministic page fetch", "confidence": "low", "finding_ids": []}
        else:
            blocked = any(row["priority"] == "P0" for row in related)
            out[stage] = {"status": "blocked" if blocked else "weak" if related else "healthy", "evidence": "deterministic initial-page audit", "confidence": "medium", "finding_ids": [row["id"] for row in related]}
    return out


def build_work_orders(findings: list[dict[str, Any]], asset: str) -> list[dict[str, Any]]:
    orders = []
    for index, row in enumerate(findings, 1):
        orders.append({"id": f"OD-{index:03d}", "priority": row["priority"], "stage": row["stage"], "root_cause": row["detail"], "recommendation_evidence": "deterministic", "observation_grade": "local_or_live_fetch", "risk": row["risk"], "assets": [asset], "owner": row["owner"], "change": row["change"], "acceptance": row["acceptance"], "observation": {"metric": "technical_acceptance" if row["stage"] == "eligibility" else "fidelity_and_delayed_discovery", "window": "immediate technical check; 28d delayed outcome where applicable"}, "rollback": row["rollback"], "status": "planned", "source_finding_ids": [row["id"]]})
    return orders


def render_report(audit: dict[str, Any], orders: list[dict[str, Any]]) -> str:
    summary = audit["summary"]; target = audit["target"]["display"]
    earliest = summary["earliest_failing_stage"] or "none detected in observable stages"
    lines = [f"# Organic Discovery Audit — {target}", "", "## Executive diagnosis", "", f"Earliest observable failing stage: **{earliest}**. The audit found **{summary['finding_counts_by_priority']['P0']} P0** and **{summary['finding_counts_by_priority']['P1']} P1** findings. Technical eligibility is not proof of indexing, retrieval, citation, recommendation, traffic, or conversion. No opaque readiness score is calculated.", "", "## Stage diagnosis", "", "| Stage | Status | Confidence | Evidence |", "|---|---|---|---|"]
    for stage in STAGES:
        item = audit["stages"][stage]; lines.append(f"| {stage.replace('_', ' ').title()} | {item['status']} | {item['confidence']} | {item['evidence']} |")
    lines += ["", "## Findings", "", "| ID | Priority | Stage | Finding |", "|---|---|---|---|"]
    for row in audit["findings"]: lines.append(f"| {row['id']} | {row['priority']} | {row['stage']} | **{row['title']}** — {row['detail'].replace('|', '\\|')} |")
    if not audit["findings"]: lines.append("| — | — | — | No deterministic findings. Delayed outcomes remain unknown. |")
    lines += ["", "## Work orders", ""]
    for order in orders:
        lines += [f"### {order['id']} — {order['priority']} / {order['stage']}", "", f"- **Root cause:** {order['root_cause']}", f"- **Owner:** {order['owner']}", f"- **Risk:** {order['risk']}", "- **Change:**", *[f"  - {item}" for item in order["change"]], "- **Acceptance:**", *[f"  - {item}" for item in order["acceptance"]], f"- **Delayed observation:** {order['observation']['metric']} / {order['observation']['window']}", "- **Rollback:**", *[f"  - {item}" for item in order["rollback"]], ""]
    lines += ["## Limitations", "", *[f"- {item}" for item in audit["limitations"]], "", "## Deliberately not done", "", "- No opaque readiness score.", "- No claim that crawler access equals indexing, retrieval, citation, or recommendation.", "- No automatic content generation, community posting, outreach, or publishing.", "- No recommendation to create `llms.txt` without a named consumer.", ""]
    return "\n".join(lines)


def _atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as handle:
        handle.write(content); name = handle.name
    os.replace(name, path)


def write_outputs(output: Path, audit: dict[str, Any], orders: list[dict[str, Any]], report: str) -> None:
    output.mkdir(parents=True, exist_ok=True)
    _atomic(output / "audit.json", json.dumps(audit, indent=2, ensure_ascii=False) + "\n")
    _atomic(output / "work-orders.json", json.dumps(orders, indent=2, ensure_ascii=False) + "\n")
    _atomic(output / "report.md", report)
