#!/usr/bin/env python3
"""Organic Discovery command-line interface."""
from __future__ import annotations

import argparse
import json
import socket  # re-exported for focused auditor tests
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from od_audit import (  # noqa: E402
    SCHEMA_VERSION as AUDIT_SCHEMA_VERSION,
    VERSION as AUDITOR_VERSION,
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
from od_shelf import (  # noqa: E402
    ShelfError,
    build_shelf_map,
    load_observations,
    plan_wedges,
    write_shelf_outputs,
    write_wedge_plan,
)
from od_truth import (  # noqa: E402
    TruthError,
    validate_fact_registry,
    write_fact_report,
)

VERSION = "0.5.0"
SCHEMA_VERSION = AUDIT_SCHEMA_VERSION  # Backward-compatible auditor test/export alias.


def _date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--as-of must use YYYY-MM-DD") from exc


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="od.py",
        description="Organic Discovery deterministic audit, Business Truth, and AI Shelf tools",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    commands = parser.add_subparsers(dest="command", required=True)

    audit = commands.add_parser("audit", help="audit one remote URL or local HTML file")
    audit.add_argument("target", help="http(s) URL or local HTML path")
    audit.add_argument(
        "--output",
        default="output",
        help="directory for audit.json, work-orders.json, and report.md",
    )
    audit.add_argument("--query", action="append", default=[], help="optional target query; repeatable")
    audit.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT, help="per-request timeout in seconds")
    audit.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="maximum bytes per fetched resource")
    audit.add_argument(
        "--max-redirects",
        type=int,
        default=DEFAULT_MAX_REDIRECTS,
        help="maximum redirects per resource",
    )
    audit.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent for remote fetches")

    facts = commands.add_parser("facts", help="validate canonical Business Truth")
    facts_commands = facts.add_subparsers(dest="facts_command", required=True)
    facts_validate = facts_commands.add_parser("validate", help="validate a fact-registry CSV")
    facts_validate.add_argument("registry", help="fact-registry CSV path")
    facts_validate.add_argument(
        "--output",
        default="output/facts.json",
        help="facts validation JSON path",
    )
    facts_validate.add_argument(
        "--as-of",
        type=_date,
        default=None,
        help="optional expiry-evaluation date in YYYY-MM-DD",
    )

    shelf = commands.add_parser("shelf", help="validate observations and map exact AI shelves")
    shelf_commands = shelf.add_subparsers(dest="shelf_command", required=True)
    shelf_map = shelf_commands.add_parser("map", help="map exact-surface shelves from JSONL observations")
    shelf_map.add_argument("observations", help="raw observation JSONL path")
    shelf_map.add_argument("--facts", default=None, help="optional fact-registry CSV for integrity checks")
    shelf_map.add_argument(
        "--output",
        default="output",
        help="directory for normalized-observations.jsonl, shelf-map.json, and shelf-report.md",
    )
    shelf_map.add_argument(
        "--as-of",
        type=_date,
        default=None,
        help="optional fact-expiry evaluation date in YYYY-MM-DD",
    )

    wedge = commands.add_parser("wedge", help="plan truthful exact-surface growth wedges")
    wedge_commands = wedge.add_subparsers(dest="wedge_command", required=True)
    wedge_plan = wedge_commands.add_parser("plan", help="apply Business Truth and shelf hard gates")
    wedge_plan.add_argument("shelf_map", help="shelf-map JSON path")
    wedge_plan.add_argument("--facts", required=True, help="fact-registry CSV path")
    wedge_plan.add_argument("--candidates", default=None, help="optional candidate JSON path")
    wedge_plan.add_argument(
        "--output",
        default="output/wedge-plan.json",
        help="wedge-plan JSON path",
    )
    wedge_plan.add_argument(
        "--as-of",
        type=_date,
        default=None,
        help="optional fact-expiry evaluation date in YYYY-MM-DD",
    )
    return parser


def run_audit(args: argparse.Namespace) -> int:
    if args.timeout <= 0:
        raise AuditError("--timeout must be greater than zero")
    if args.max_bytes < 1024:
        raise AuditError("--max-bytes must be at least 1024")
    if not 0 <= args.max_redirects <= 20:
        raise AuditError("--max-redirects must be between 0 and 20")
    document = load_target(
        args.target,
        timeout=args.timeout,
        max_bytes=args.max_bytes,
        max_redirects=args.max_redirects,
        user_agent=args.user_agent,
    )
    audit, orders, report = audit_document(document, queries=args.query)
    output = Path(args.output).expanduser()
    write_outputs(output, audit, orders, report)
    print(
        f"Wrote {output / 'audit.json'}, {output / 'work-orders.json'}, and "
        f"{output / 'report.md'} ({len(audit['findings'])} findings; no opaque score)."
    )
    return 0


def run_facts_validate(args: argparse.Namespace) -> int:
    registry = Path(args.registry).expanduser()
    report = validate_fact_registry(registry, as_of=args.as_of)
    output = Path(args.output).expanduser()
    write_fact_report(output, report)
    print(
        f"Wrote {output} ({report['summary']['publishable_count']} publishable, "
        f"{report['summary']['blocked_count']} blocked, {report['summary']['error_count']} errors)."
    )
    return 0 if report["valid"] else 1


def run_shelf_map(args: argparse.Namespace) -> int:
    observations = Path(args.observations).expanduser()
    facts_report = None
    facts_source = None
    if args.facts:
        facts_path = Path(args.facts).expanduser()
        facts_report = validate_fact_registry(facts_path, as_of=args.as_of)
        if not facts_report["valid"]:
            raise TruthError("fact registry is invalid; run `od.py facts validate` for details")
        facts_source = str(facts_path)
    records = load_observations(observations)
    shelf_map = build_shelf_map(
        records,
        observation_source=str(observations),
        facts_report=facts_report,
        facts_source=facts_source,
    )
    output = Path(args.output).expanduser()
    write_shelf_outputs(output, records, shelf_map)
    print(
        f"Wrote {output / 'normalized-observations.jsonl'}, {output / 'shelf-map.json'}, "
        f"and {output / 'shelf-report.md'} ({len(shelf_map['groups'])} exact-surface groups; "
        "branded validation excluded from unbranded share)."
    )
    return 0


def run_wedge_plan(args: argparse.Namespace) -> int:
    shelf_path = Path(args.shelf_map).expanduser()
    try:
        shelf_map = json.loads(shelf_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ShelfError(f"cannot read shelf map {shelf_path}: {exc}") from exc
    facts_path = Path(args.facts).expanduser()
    facts_report = validate_fact_registry(facts_path, as_of=args.as_of)
    candidates = Path(args.candidates).expanduser() if args.candidates else None
    plan = plan_wedges(shelf_map, facts_report, candidates_path=candidates)
    output = Path(args.output).expanduser()
    write_wedge_plan(output, plan)
    print(
        f"Wrote {output} ({plan['summary']['accepted_count']} accepted, "
        f"{plan['summary']['rejected_count']} rejected; unsafe and unsupported wedges hard-blocked)."
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "audit":
            return run_audit(args)
        if args.command == "facts" and args.facts_command == "validate":
            return run_facts_validate(args)
        if args.command == "shelf" and args.shelf_command == "map":
            return run_shelf_map(args)
        if args.command == "wedge" and args.wedge_command == "plan":
            return run_wedge_plan(args)
        return 2
    except (AuditError, TruthError, ShelfError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
