#!/usr/bin/env python3
"""Organic Discovery deterministic audit CLI."""
from __future__ import annotations

import argparse
import socket  # re-exported for focused tests
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from od_audit import (  # noqa: E402
    SCHEMA_VERSION,
    VERSION,
    audit_document,
    important_schema_values,
    json_ld_types,
    parse_json_ld,
    write_outputs,
)
from od_fetch import (  # noqa: E402
    DEFAULT_MAX_BYTES,
    DEFAULT_MAX_REDIRECTS,
    DEFAULT_TIMEOUT,
    DEFAULT_USER_AGENT,
    AuditError,
    load_target,
    validate_public_url,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="od.py", description="Organic Discovery deterministic webpage auditor")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit", help="audit one remote URL or local HTML file")
    audit.add_argument("target", help="http(s) URL or local HTML path")
    audit.add_argument("--output", default="output", help="directory for audit.json, work-orders.json, and report.md")
    audit.add_argument("--query", action="append", default=[], help="optional target query; repeatable")
    audit.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="per-request timeout in seconds")
    audit.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="maximum bytes per fetched resource")
    audit.add_argument("--max-redirects", type=int, default=DEFAULT_MAX_REDIRECTS, help="maximum redirects per resource")
    audit.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent for remote fetches")
    return parser


def run_audit(args: argparse.Namespace) -> int:
    if args.timeout <= 0:
        raise AuditError("--timeout must be greater than zero")
    if args.max_bytes < 1024:
        raise AuditError("--max-bytes must be at least 1024")
    if not 0 <= args.max_redirects <= 20:
        raise AuditError("--max-redirects must be between 0 and 20")
    document = load_target(args.target, timeout=args.timeout, max_bytes=args.max_bytes, max_redirects=args.max_redirects, user_agent=args.user_agent)
    audit, orders, report = audit_document(document, queries=args.query)
    output = Path(args.output).expanduser()
    write_outputs(output, audit, orders, report)
    print(f"Wrote {output / 'audit.json'}, {output / 'work-orders.json'}, and {output / 'report.md'} ({len(audit['findings'])} findings; no opaque score).")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return run_audit(args) if args.command == "audit" else 2
    except AuditError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
