#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
EVALS = ROOT / "evals" / "trigger-evals.json"
OPENAI_METADATA = ROOT / "agents" / "openai.yaml"
CITATION = ROOT / "CITATION.cff"
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
ROADMAP = ROOT / "docs" / "ROADMAP.md"
DEFINITION_OF_DONE = ROOT / "docs" / "DEFINITION-OF-DONE.md"
OD_CLI = ROOT / "scripts" / "od.py"
OD_AUDIT = ROOT / "scripts" / "od_audit.py"

AUDIT_EXPECTED = ROOT / "examples" / "sample-site" / "expected"
SHELF_EXPECTED = ROOT / "examples" / "sample-shelf" / "expected"

PROJECT_VERSION = "0.5.0"
AUDIT_ARTIFACT_VERSION = "0.4.0"
FACT_SCHEMA_VERSION = "organic-discovery/facts/1.0"
OBSERVATION_SCHEMA_VERSION = "organic-discovery/observations/1.0"
SHELF_SCHEMA_VERSION = "organic-discovery/shelf-map/1.0"
WEDGE_SCHEMA_VERSION = "organic-discovery/wedge-plan/1.0"

REQUIRED_FILES = {
    ".github/workflows/validate.yml",
    ".release/v0.4.0.md",
    ".release/v0.5.0.md",
    "AGENTS.md",
    "CHANGELOG.md",
    "CITATION.cff",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SECURITY.md",
    "SKILL.md",
    "agents/openai.yaml",
    "docs/DEFINITION-OF-DONE.md",
    "docs/PRODUCT-VISION.md",
    "docs/ROADMAP.md",
    "docs/SELF-AUDIT.md",
    "evals/trigger-evals.json",
    "examples/sample-site/README.md",
    "examples/sample-site/expected/audit.json",
    "examples/sample-site/expected/report.md",
    "examples/sample-site/expected/work-orders.json",
    "examples/sample-site/site/app.js",
    "examples/sample-site/site/index.html",
    "examples/sample-site/site/robots.txt",
    "examples/sample-site/site/sitemap.xml",
    "examples/sample-shelf/README.md",
    "examples/sample-shelf/candidates.json",
    "examples/sample-shelf/expected/facts.json",
    "examples/sample-shelf/expected/normalized-observations.jsonl",
    "examples/sample-shelf/expected/shelf-map.json",
    "examples/sample-shelf/expected/shelf-report.md",
    "examples/sample-shelf/expected/wedge-plan.json",
    "examples/sample-shelf/fact-registry.csv",
    "examples/sample-shelf/observations.jsonl",
    "references/ai-shelf-and-growth-loop.md",
    "references/evidence-and-tactics.md",
    "references/execution-and-evidence.md",
    "references/measurement-protocol.md",
    "references/output-contracts.md",
    "references/platform-adapters.md",
    "references/regional-and-surface-adapters.md",
    "references/source-earning.md",
    "references/source-register.md",
    "references/tracking-and-opportunity-recon.md",
    "references/vertical-adapters.md",
    "schemas/fact-record.schema.json",
    "schemas/observation.schema.json",
    "schemas/shelf-map.schema.json",
    "schemas/wedge-plan.schema.json",
    "scripts/od.py",
    "scripts/od_audit.py",
    "scripts/od_fetch.py",
    "scripts/od_shelf.py",
    "scripts/od_truth.py",
    "scripts/validate_skill.py",
    "tests/test_od.py",
    "tests/test_shelf.py",
}

REQUIRED_SKILL_TERMS = {
    "activation",
    "eligibility",
    "retrieval",
    "source selection",
    "absorption",
    "fidelity",
    "behavior",
    "business truth",
    "ai shelf",
    "approval",
    "reddit",
    "llms.txt",
    "rollback",
    "supervised execute",
    "python scripts/od.py audit",
    "python scripts/od.py facts validate",
    "python scripts/od.py shelf map",
    "python scripts/od.py wedge plan",
}

REQUIRED_README_TERMS = {
    "seo",
    "aeo",
    "geo",
    "business truth validator",
    "ai shelf mapper",
    "truthful wedge planner",
    "python scripts/od.py audit",
    "python scripts/od.py facts validate",
    "python scripts/od.py shelf map",
    "python scripts/od.py wedge plan",
    "normalized-observations.jsonl",
    "shelf-map.json",
    "wedge-plan.json",
    "does **not yet ship**",
}

REQUIRED_ROADMAP_TERMS = {
    "current state — v0.5.0",
    "v0.4 — deterministic audit foundation",
    "v0.5 — business truth and ai shelf mapper",
    "status: shipped",
    "v0.6 — github-backed owned-site operator",
    "v0.7 — content portfolio and earned-source queue",
    "v0.8 — measurement adapters and experiment ledger",
    "v0.9 — cms adapters and bounded autonomy",
    "v1.0 — continuous organic growth operator",
}

REQUIRED_DOD_TERMS = {
    "release truth",
    "demand and ai shelf",
    "truthful wedge gates",
    "owned-site execution",
    "earned-source integrity",
    "outcome measurement",
    "learning and rollback",
    "v0.4 acceptance",
    "v0.5 acceptance",
    "v1.0 acceptance scenario",
}

RELATIVE_REF_RE = re.compile(
    r"`((?:references|scripts|evals|docs|agents|examples|tests|schemas)/[^`]+)`"
)
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter is not closed"]

    data: dict[str, str] = {}
    current_section: str | None = None
    for raw in text[4:end].splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  "):
            if current_section == "metadata" and ":" in raw:
                key, value = raw.strip().split(":", 1)
                data[f"metadata.{key.strip()}"] = value.strip().strip("\"'")
            continue
        if ":" not in raw:
            errors.append(f"invalid frontmatter line: {raw}")
            continue
        key, value = raw.split(":", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        data[key] = value
        current_section = key if not value else None
    return data, errors


def require_terms(path: Path, terms: set[str], label: str, errors: list[str]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8").casefold()
    missing = sorted(term for term in terms if term.casefold() not in text)
    if missing:
        errors.append(f"{label} is missing required terms: " + ", ".join(missing))


def validate_local_links(errors: list[str]) -> None:
    root = ROOT.resolve()
    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            candidate = (markdown.parent / path).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(
                    f"local link escapes repository: {markdown.relative_to(ROOT)} -> {target}"
                )
                continue
            if not candidate.exists():
                errors.append(
                    f"broken local link: {markdown.relative_to(ROOT)} -> {target}"
                )


def validate_serialized_files(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")

    for path in sorted(ROOT.rglob("*.jsonl")):
        for line_number, raw in enumerate(
            path.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if not raw.strip():
                continue
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(
                    f"invalid JSONL in {path.relative_to(ROOT)}:{line_number}: {exc}"
                )


def validate_versions(skill_version: str, errors: list[str]) -> None:
    if skill_version != PROJECT_VERSION:
        errors.append(
            f"SKILL.md version must be {PROJECT_VERSION}, found {skill_version or 'missing'}"
        )

    if f"## {PROJECT_VERSION} " not in CHANGELOG.read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG has no {PROJECT_VERSION} release entry")
    if f"version-{PROJECT_VERSION}-" not in README.read_text(encoding="utf-8"):
        errors.append("README version badge does not match the project version")

    evals = json.loads(EVALS.read_text(encoding="utf-8"))
    if evals.get("version") != PROJECT_VERSION:
        errors.append("trigger eval version does not match the project version")

    citation = CITATION.read_text(encoding="utf-8")
    if f'version: "{PROJECT_VERSION}"' not in citation:
        errors.append("CITATION.cff version does not match the project version")

    cli = OD_CLI.read_text(encoding="utf-8")
    if f'VERSION = "{PROJECT_VERSION}"' not in cli:
        errors.append("scripts/od.py project version does not match")

    auditor = OD_AUDIT.read_text(encoding="utf-8")
    if f'VERSION = "{AUDIT_ARTIFACT_VERSION}"' not in auditor:
        errors.append("scripts/od_audit.py no longer preserves the v0.4 artifact version")
    if f'SCHEMA_VERSION = "{AUDIT_ARTIFACT_VERSION}"' not in auditor:
        errors.append("scripts/od_audit.py no longer preserves the v0.4 schema version")


def validate_evals(errors: list[str]) -> None:
    payload = json.loads(EVALS.read_text(encoding="utf-8"))
    if payload.get("skill") != "organic-discovery":
        errors.append("eval skill name does not match SKILL.md")

    cases = payload.get("cases", [])
    positives = sum(case.get("should_trigger") is True for case in cases)
    negatives = sum(case.get("should_trigger") is False for case in cases)
    if positives < 12 or negatives < 10:
        errors.append(
            "trigger evals need at least 12 positive and 10 negative cases; "
            f"found {positives} and {negatives}"
        )

    prompts: set[str] = set()
    for index, case in enumerate(cases):
        prompt = case.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"eval case {index} has no prompt")
        elif prompt.casefold() in prompts:
            errors.append(f"eval case {index} duplicates an earlier prompt")
        else:
            prompts.add(prompt.casefold())
        if case.get("should_trigger") not in (True, False):
            errors.append(f"eval case {index} has invalid should_trigger")
        if not isinstance(case.get("reason"), str) or not case["reason"].strip():
            errors.append(f"eval case {index} has no reason")


def validate_workflow(errors: list[str]) -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        "python scripts/validate_skill.py",
        "python -m unittest discover -s tests -v",
        "python scripts/od.py audit examples/sample-site/site/index.html",
        "python scripts/od.py facts validate examples/sample-shelf/fact-registry.csv",
        "python scripts/od.py shelf map examples/sample-shelf/observations.jsonl",
        "python scripts/od.py wedge plan /tmp/organic-discovery-shelf/shelf-map.json",
        "cmp /tmp/organic-discovery-shelf/wedge-plan.json",
        "pull_request:",
        '"3.11"',
        '"3.13"',
    )
    for term in required:
        if term not in text:
            errors.append(f"validation workflow is missing: {term}")


def validate_metadata(errors: list[str]) -> None:
    text = OPENAI_METADATA.read_text(encoding="utf-8").casefold()
    for term in (
        "display_name:",
        "short_description:",
        "default_prompt:",
        "allow_implicit_invocation:",
        "organic discovery operator",
        "business truth",
        "ai shelf",
        "rollback",
    ):
        if term.casefold() not in text:
            errors.append(f"agents/openai.yaml is missing: {term}")

    citation = CITATION.read_text(encoding="utf-8").casefold()
    for term in (
        "cff-version: 1.2.0",
        "repository-code:",
        "license: mit",
        "organic growth",
        "ai shelf",
        "business truth",
    ):
        if term.casefold() not in citation:
            errors.append(f"CITATION.cff is missing: {term}")


def load_json(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid {label}: {exc}")
        return None
    if not isinstance(value, dict):
        errors.append(f"{label} must be a JSON object")
        return None
    return value


def validate_audit_fixture(errors: list[str]) -> None:
    audit = load_json(AUDIT_EXPECTED / "audit.json", "expected audit", errors)
    orders = load_json(
        AUDIT_EXPECTED / "work-orders.json", "expected work orders", errors
    )
    if audit is None or orders is None:
        return

    if audit.get("schema_version") != AUDIT_ARTIFACT_VERSION:
        errors.append("expected audit schema version drifted")
    if audit.get("tool", {}).get("version") != AUDIT_ARTIFACT_VERSION:
        errors.append("expected audit tool version drifted")
    if audit.get("summary", {}).get("opaque_score", "missing") is not None:
        errors.append("expected audit must not contain an opaque score")

    for stage in (
        "activation",
        "retrieval",
        "context_allocation",
        "source_selection",
        "absorption",
        "behavior",
    ):
        if audit.get("stages", {}).get(stage, {}).get("status") != "unknown":
            errors.append(f"expected audit must preserve {stage} as unknown")

    if not isinstance(orders, list):
        errors.append("expected work orders must be a JSON array")
        return
    if len(orders) != audit.get("summary", {}).get("finding_count"):
        errors.append("expected work-order count does not match finding count")
    for index, order in enumerate(orders):
        if not order.get("acceptance") or not order.get("rollback"):
            errors.append(f"audit work order {index} lacks acceptance or rollback")

    report = (AUDIT_EXPECTED / "report.md").read_text(encoding="utf-8")
    if "No opaque readiness score" not in report:
        errors.append("expected audit report must state the no-score boundary")


def validate_fact_fixture(errors: list[str]) -> None:
    facts = load_json(SHELF_EXPECTED / "facts.json", "expected facts", errors)
    if facts is None:
        return

    if facts.get("schema_version") != FACT_SCHEMA_VERSION:
        errors.append("expected facts schema version drifted")
    if facts.get("record_schema") != "schemas/fact-record.schema.json":
        errors.append("expected facts record schema path drifted")
    if facts.get("valid") is not True:
        errors.append("sample fact registry must remain structurally valid")

    summary = facts.get("summary", {})
    expected_counts = {
        "fact_count": 10,
        "publishable_count": 7,
        "blocked_count": 3,
        "error_count": 0,
        "independent_publishable_count": 1,
        "seller_controlled_publishable_count": 6,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            errors.append(
                f"expected fact fixture {key} must be {expected}, found {summary.get(key)}"
            )

    blocked = set(facts.get("blocked_fact_ids", []))
    if not {"ghost-exists", "kr-eczema-safe", "kr-price-draft"}.issubset(blocked):
        errors.append("expected fact fixture lost required blocked claims")

    records = facts.get("facts", [])
    if len(records) != 10:
        errors.append("expected fact fixture must contain ten normalized records")
    for record in records:
        if not record.get("claim_id") or not record.get("entity_id"):
            errors.append("normalized fact lacks a stable claim or entity ID")
        if record.get("source_control") not in {
            "seller_controlled",
            "independent",
            "community",
            "unknown",
        }:
            errors.append(
                f"normalized fact {record.get('claim_id')} has invalid source_control"
            )


def _validate_rate_objects(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, dict):
        if "rate" in value:
            if "numerator" not in value or "denominator" not in value:
                errors.append(f"rate object lacks numerator or denominator: {path}")
            denominator = value.get("denominator")
            numerator = value.get("numerator")
            if isinstance(denominator, int) and isinstance(numerator, int):
                if denominator < 0 or numerator < 0 or numerator > denominator:
                    errors.append(f"invalid rate counts at {path}")
            if denominator == 0 and value.get("rate") is not None:
                errors.append(f"zero-denominator rate must be null at {path}")
        for key, child in value.items():
            _validate_rate_objects(child, f"{path}.{key}", errors)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _validate_rate_objects(child, f"{path}[{index}]", errors)


def validate_shelf_fixture(errors: list[str]) -> None:
    shelf = load_json(SHELF_EXPECTED / "shelf-map.json", "expected shelf map", errors)
    wedges = load_json(
        SHELF_EXPECTED / "wedge-plan.json", "expected wedge plan", errors
    )
    if shelf is None or wedges is None:
        return

    if shelf.get("schema_version") != SHELF_SCHEMA_VERSION:
        errors.append("expected shelf schema version drifted")
    if shelf.get("record_schema") != "schemas/observation.schema.json":
        errors.append("expected shelf observation schema path drifted")
    if shelf.get("shelf_map_schema") != "schemas/shelf-map.schema.json":
        errors.append("expected shelf-map schema path drifted")

    groups = shelf.get("groups", [])
    if len(groups) != 6:
        errors.append(f"expected shelf fixture must contain six groups, found {len(groups)}")
    if shelf.get("source", {}).get("observation_count") != 22:
        errors.append("expected shelf fixture must preserve 22 observations")
    if shelf.get("branded_exclusion", {}).get("excluded_observation_count") != 2:
        errors.append("expected shelf fixture must preserve two branded observations")

    required_dimensions = {
        "platform",
        "surface",
        "mode",
        "model",
        "market",
        "language",
        "device",
        "account_state",
        "session_state",
        "prompt_family",
        "target_entity_id",
        "branded",
    }
    states = {group.get("shelf_state") for group in groups}
    if not {"open", "locked", "fragmented", "unsafe", "unknown"}.issubset(states):
        errors.append("expected shelf fixture lost one or more required states")

    branded_groups = 0
    for group in groups:
        dimensions = group.get("dimensions", {})
        if not required_dimensions.issubset(dimensions):
            errors.append(f"shelf group {group.get('group_id')} lacks exact dimensions")
        if not group.get("classification_reasons"):
            errors.append(f"shelf group {group.get('group_id')} lacks classification reasons")
        if dimensions.get("branded"):
            branded_groups += 1
            if group.get("eligible_for_unbranded_recommendation_share") is not False:
                errors.append("branded group is eligible for unbranded recommendation share")
            if group.get("shelf_state") != "unknown":
                errors.append("branded group must remain unknown for opportunity planning")
        _validate_rate_objects(group.get("metrics", {}), group.get("group_id", "group"), errors)

    if branded_groups != 1:
        errors.append(f"expected shelf fixture must contain one branded group, found {branded_groups}")

    normalized_path = SHELF_EXPECTED / "normalized-observations.jsonl"
    normalized = [
        json.loads(raw)
        for raw in normalized_path.read_text(encoding="utf-8").splitlines()
        if raw.strip()
    ]
    if len(normalized) != 22:
        errors.append(
            f"expected normalized observation fixture must contain 22 records, found {len(normalized)}"
        )
    for index, record in enumerate(normalized, start=1):
        missing = required_dimensions - set(record)
        if missing:
            errors.append(
                f"normalized observation {index} lacks dimensions: {', '.join(sorted(missing))}"
            )

    if wedges.get("schema_version") != WEDGE_SCHEMA_VERSION:
        errors.append("expected wedge schema version drifted")
    if wedges.get("wedge_plan_schema") != "schemas/wedge-plan.schema.json":
        errors.append("expected wedge-plan schema path drifted")

    summary = wedges.get("summary", {})
    if summary.get("accepted_count") != 2 or summary.get("rejected_count") != 3:
        errors.append("expected wedge fixture must contain two accepted and three rejected cases")
    if summary.get("opaque_geo_score", "missing") is not None:
        errors.append("wedge plan must not contain an opaque GEO score")

    for item in wedges.get("accepted", []):
        if item.get("status") != "approved_for_planning":
            errors.append(f"accepted wedge {item.get('candidate_id')} has invalid status")
        if item.get("gate_failures"):
            errors.append(f"accepted wedge {item.get('candidate_id')} has gate failures")
        if not item.get("surface_opportunities"):
            errors.append(f"accepted wedge {item.get('candidate_id')} has no surface opportunity")

    for item in wedges.get("rejected", []):
        if not item.get("candidate_id"):
            errors.append("rejected wedge lacks candidate_id")
        if item.get("status") != "rejected":
            errors.append(f"rejected wedge {item.get('candidate_id')} has invalid status")
        if not item.get("gate_failures"):
            errors.append(f"rejected wedge {item.get('candidate_id')} lacks gate failures")

    report = (SHELF_EXPECTED / "shelf-report.md").read_text(encoding="utf-8")
    for term in (
        "Branded validation is excluded",
        "No opaque GEO score",
        "fixed time-to-shelf promise",
        "Seller-controlled evidence is counted separately",
    ):
        if term not in report:
            errors.append(f"shelf report is missing boundary: {term}")


def compare_files(actual: Path, expected: Path, label: str, errors: list[str]) -> None:
    if not actual.is_file():
        errors.append(f"smoke command did not create {label}")
        return
    if actual.read_bytes() != expected.read_bytes():
        errors.append(f"smoke output differs from committed artifact: {label}")


def run_smoke_checks(errors: list[str]) -> None:
    output = ROOT / ".validation-output"
    shutil.rmtree(output, ignore_errors=True)
    output.mkdir()

    commands = (
        [sys.executable, "scripts/od.py", "--version"],
        [
            sys.executable,
            "scripts/od.py",
            "audit",
            "examples/sample-site/site/index.html",
            "--output",
            str(output / "audit"),
        ],
        [
            sys.executable,
            "scripts/od.py",
            "facts",
            "validate",
            "examples/sample-shelf/fact-registry.csv",
            "--output",
            str(output / "facts.json"),
        ],
        [
            sys.executable,
            "scripts/od.py",
            "shelf",
            "map",
            "examples/sample-shelf/observations.jsonl",
            "--facts",
            "examples/sample-shelf/fact-registry.csv",
            "--output",
            str(output / "shelf"),
        ],
        [
            sys.executable,
            "scripts/od.py",
            "wedge",
            "plan",
            str(output / "shelf" / "shelf-map.json"),
            "--facts",
            "examples/sample-shelf/fact-registry.csv",
            "--candidates",
            "examples/sample-shelf/candidates.json",
            "--output",
            str(output / "wedge-plan.json"),
        ],
    )

    for command in commands:
        result = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode:
            errors.append(
                f"command failed ({' '.join(command)}): "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

    for name in ("audit.json", "work-orders.json", "report.md"):
        compare_files(
            output / "audit" / name,
            AUDIT_EXPECTED / name,
            f"audit/{name}",
            errors,
        )
    compare_files(output / "facts.json", SHELF_EXPECTED / "facts.json", "facts.json", errors)
    for name in (
        "normalized-observations.jsonl",
        "shelf-map.json",
        "shelf-report.md",
    ):
        compare_files(
            output / "shelf" / name,
            SHELF_EXPECTED / name,
            f"shelf/{name}",
            errors,
        )
    compare_files(
        output / "wedge-plan.json",
        SHELF_EXPECTED / "wedge-plan.json",
        "wedge-plan.json",
        errors,
    )

    shutil.rmtree(output, ignore_errors=True)


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    if not SKILL.is_file():
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    skill_text = SKILL.read_text(encoding="utf-8")
    metadata, frontmatter_errors = parse_frontmatter(skill_text)
    errors.extend(frontmatter_errors)
    skill_version = metadata.get("metadata.version", "")

    if metadata.get("name") != "organic-discovery":
        errors.append("skill name must be organic-discovery")
    description = metadata.get("description", "")
    if not description or len(description) > 1024:
        errors.append("skill description is required and must not exceed 1024 characters")
    if len(skill_text.splitlines()) > 500:
        errors.append("SKILL.md exceeds 500 lines")

    require_terms(SKILL, REQUIRED_SKILL_TERMS, "SKILL.md", errors)
    require_terms(README, REQUIRED_README_TERMS, "README.md", errors)
    require_terms(ROADMAP, REQUIRED_ROADMAP_TERMS, "docs/ROADMAP.md", errors)
    require_terms(
        DEFINITION_OF_DONE,
        REQUIRED_DOD_TERMS,
        "docs/DEFINITION-OF-DONE.md",
        errors,
    )

    for relative in sorted(set(RELATIVE_REF_RE.findall(skill_text))):
        if not (ROOT / relative).is_file():
            errors.append(f"broken referenced path in SKILL.md: {relative}")

    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        if text.count("```") % 2:
            errors.append(f"unbalanced fenced code block: {markdown.relative_to(ROOT)}")
        if re.search(r"\b(?:TODO|FIXME|TBD)\b", text):
            warnings.append(f"placeholder marker found: {markdown.relative_to(ROOT)}")

    validate_local_links(errors)
    validate_serialized_files(errors)
    validate_versions(skill_version, errors)
    validate_evals(errors)
    validate_workflow(errors)
    validate_metadata(errors)
    validate_audit_fixture(errors)
    validate_fact_fixture(errors)
    validate_shelf_fixture(errors)
    run_smoke_checks(errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "OK: organic-discovery validated "
        f"(project {PROJECT_VERSION}, audit artifact {AUDIT_ARTIFACT_VERSION}, "
        f"{len(skill_text.splitlines())} SKILL.md lines, "
        f"{len(REQUIRED_FILES)} required files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
