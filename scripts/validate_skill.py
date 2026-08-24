#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
CHANGELOG = ROOT / "CHANGELOG.md"
EVALS = ROOT / "evals" / "trigger-evals.json"
OPENAI_METADATA = ROOT / "agents" / "openai.yaml"
CITATION = ROOT / "CITATION.cff"
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"
PRODUCT_VISION = ROOT / "docs" / "PRODUCT-VISION.md"
ROADMAP = ROOT / "docs" / "ROADMAP.md"
DEFINITION_OF_DONE = ROOT / "docs" / "DEFINITION-OF-DONE.md"
OD_CLI = ROOT / "scripts" / "od.py"

AUDIT_EXPECTED = ROOT / "examples" / "sample-site" / "expected"
SHELF_EXPECTED = ROOT / "examples" / "sample-shelf" / "expected"

PROJECT_VERSION = "0.5.0"
LEGACY_AUDIT_VERSION = "0.4.0"

REQUIRED_FILES = {
    ".github/workflows/validate.yml",
    "AGENTS.md",
    "CITATION.cff",
    "CHANGELOG.md",
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
    "examples/sample-shelf/fact-registry.csv",
    "examples/sample-shelf/observations.jsonl",
    "examples/sample-shelf/candidates.json",
    "examples/sample-shelf/expected/facts.json",
    "examples/sample-shelf/expected/normalized-observations.jsonl",
    "examples/sample-shelf/expected/shelf-map.json",
    "examples/sample-shelf/expected/shelf-report.md",
    "examples/sample-shelf/expected/wedge-plan.json",
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
    "Activation",
    "Eligibility",
    "Retrieval",
    "Source selection",
    "Absorption",
    "Fidelity",
    "Behavior",
    "Business Truth",
    "AI shelf",
    "fact registry",
    "human approval",
    "Reddit",
    "llms.txt",
    "rollback",
    "business result",
    "supervised execute",
    "Repository capability boundary",
    "scripts/od.py",
    "facts validate",
    "shelf map",
    "wedge plan",
}

REQUIRED_README_TERMS = {
    "SEO",
    "AEO",
    "GEO",
    "Organic Growth Operator",
    "AI Shelf Mapper",
    "Business Truth validator",
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
    "Current state — v0.5.0",
    "v0.4 — Deterministic audit foundation",
    "v0.5 — Business Truth and AI Shelf Mapper",
    "**Status: shipped**",
    "v0.6 — GitHub-backed owned-site operator",
    "v0.7 — Content portfolio and earned-source queue",
    "v0.8 — Measurement adapters and experiment ledger",
    "v0.9 — CMS adapters and bounded autonomy",
    "v1.0 — Continuous Organic Growth Operator",
}

REQUIRED_DOD_TERMS = {
    "Release truth",
    "Demand and AI shelf",
    "Truthful wedge gates",
    "Owned-site execution",
    "Earned-source integrity",
    "Outcome measurement",
    "Learning and rollback",
    "v0.4 acceptance",
    "v0.5 acceptance",
    "v1.0 acceptance scenario",
}

RELATIVE_REF_RE = re.compile(r"`((?:references|scripts|evals|docs|agents|examples|tests|schemas)/[^`]+)`")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter is not closed"]
    data: dict[str, str] = {}
    current_section = None
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
    text = path.read_text(encoding="utf-8")
    missing = sorted(term for term in terms if term not in text)
    if missing:
        errors.append(f"{label} is missing required terms: " + ", ".join(missing))


def validate_local_links(errors: list[str]) -> None:
    for md in sorted(ROOT.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            path = target.split("#", 1)[0]
            if not path:
                continue
            candidate = (md.parent / path).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                errors.append(f"local link escapes repository: {md.relative_to(ROOT)} -> {target}")
                continue
            if not candidate.exists():
                errors.append(f"broken local link: {md.relative_to(ROOT)} -> {target}")


def validate_json_and_jsonl(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
    for path in sorted(ROOT.rglob("*.jsonl")):
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            try:
                json.loads(raw)
            except json.JSONDecodeError as exc:
                errors.append(f"invalid JSONL in {path.relative_to(ROOT)}:{line_number}: {exc}")


def validate_openai_metadata(errors: list[str]) -> None:
    if not OPENAI_METADATA.is_file():
        return
    text = OPENAI_METADATA.read_text(encoding="utf-8")
    for term in ("display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"):
        if term not in text:
            errors.append(f"agents/openai.yaml is missing {term}")
    for term in ("Organic Discovery Operator", "Business Truth", "AI shelf", "rollback"):
        if term not in text:
            errors.append(f"agents/openai.yaml is missing current scope term: {term}")


def validate_citation(skill_version: str, errors: list[str]) -> None:
    if not CITATION.is_file():
        return
    text = CITATION.read_text(encoding="utf-8")
    for term in ("cff-version: 1.2.0", "title:", "authors:", "repository-code:", "license: MIT"):
        if term not in text:
            errors.append(f"CITATION.cff is missing {term}")
    if skill_version and f'version: "{skill_version}"' not in text:
        errors.append("CITATION.cff version does not match SKILL.md")
    for term in ("organic growth", "AI shelf", "Business Truth"):
        if term.lower() not in text.lower():
            errors.append(f"CITATION.cff is missing current scope term: {term}")


def validate_workflow(errors: list[str]) -> None:
    if not WORKFLOW.is_file():
        return
    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        "python scripts/validate_skill.py",
        "python -m unittest discover -s tests -v",
        "python scripts/od.py audit examples/sample-site/site/index.html",
        "python scripts/od.py facts validate examples/sample-shelf/fact-registry.csv",
        "python scripts/od.py shelf map examples/sample-shelf/observations.jsonl",
        "python scripts/od.py wedge plan .ci-shelf/shelf-map.json",
        "pull_request:",
        '"3.11"',
        '"3.13"',
    )
    for term in required:
        if term not in text:
            errors.append(f"validation workflow is missing: {term}")


def validate_versions(skill_version: str, errors: list[str]) -> None:
    if not skill_version:
        return
    if skill_version != PROJECT_VERSION:
        errors.append(f"SKILL.md version must be {PROJECT_VERSION}, found {skill_version}")
    if CHANGELOG.is_file() and f"## {skill_version} " not in CHANGELOG.read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG has no release entry for version {skill_version}")
    if README.is_file() and f"version-{skill_version}-" not in README.read_text(encoding="utf-8"):
        errors.append("README version badge does not match SKILL.md")
    if EVALS.is_file():
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
        if payload.get("version") != skill_version:
            errors.append("trigger eval version does not match SKILL.md")
    cli_text = OD_CLI.read_text(encoding="utf-8") if OD_CLI.is_file() else ""
    if f'VERSION = "{skill_version}"' not in cli_text:
        errors.append("CLI project version does not match SKILL.md")
    if f'AUDITOR_VERSION = "{LEGACY_AUDIT_VERSION}"' not in cli_text:
        errors.append("CLI must preserve the legacy v0.4 audit artifact version")


def validate_audit_fixture(errors: list[str]) -> None:
    try:
        audit = json.loads((AUDIT_EXPECTED / "audit.json").read_text(encoding="utf-8"))
        orders = json.loads((AUDIT_EXPECTED / "work-orders.json").read_text(encoding="utf-8"))
        report = (AUDIT_EXPECTED / "report.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid expected audit output: {exc}")
        return
    if audit.get("schema_version") != LEGACY_AUDIT_VERSION:
        errors.append("legacy expected audit schema changed without an explicit contract migration")
    if audit.get("tool", {}).get("version") != LEGACY_AUDIT_VERSION:
        errors.append("legacy expected audit tool version changed")
    if audit.get("summary", {}).get("opaque_score", "missing") is not None:
        errors.append("expected audit must not contain an opaque score")
    for stage in ("activation", "retrieval", "context_allocation", "source_selection", "absorption", "behavior"):
        if audit.get("stages", {}).get(stage, {}).get("status") != "unknown":
            errors.append(f"expected audit must preserve {stage} as unknown")
    if len(orders) != audit.get("summary", {}).get("finding_count"):
        errors.append("expected work-order count does not match finding count")
    for index, order in enumerate(orders):
        if not order.get("acceptance") or not order.get("rollback"):
            errors.append(f"audit work order {index} lacks acceptance or rollback")
    if "No opaque readiness score" not in report:
        errors.append("expected audit report must state the no-score boundary")


def validate_shelf_fixture(errors: list[str]) -> None:
    try:
        facts = json.loads((SHELF_EXPECTED / "facts.json").read_text(encoding="utf-8"))
        shelf = json.loads((SHELF_EXPECTED / "shelf-map.json").read_text(encoding="utf-8"))
        wedges = json.loads((SHELF_EXPECTED / "wedge-plan.json").read_text(encoding="utf-8"))
        normalized = [json.loads(line) for line in (SHELF_EXPECTED / "normalized-observations.jsonl").read_text(encoding="utf-8").splitlines() if line]
        report = (SHELF_EXPECTED / "shelf-report.md").read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid expected v0.5 output: {exc}")
        return

    if facts.get("schema_version") != "organic-discovery/facts/1.0":
        errors.append("expected facts schema version is wrong")
    if facts.get("tool", {}).get("version") != PROJECT_VERSION:
        errors.append("expected facts tool version is wrong")
    summary = facts.get("summary", {})
    if summary.get("publishable_count") != 7 or summary.get("blocked_count") != 3 or summary.get("error_count") != 0:
        errors.append("expected fact fixture summary drifted")

    if shelf.get("schema_version") != "organic-discovery/shelf-map/1.0":
        errors.append("expected shelf schema version is wrong")
    if shelf.get("summary", {}).get("group_count") != 6:
        errors.append("expected shelf fixture must contain six exact-surface groups")
    if shelf.get("summary", {}).get("branded_group_count") != 1:
        errors.append("expected shelf fixture must contain one branded group")
    states = {group.get("shelf_state") for group in shelf.get("groups", [])}
    for state in ("open", "locked", "fragmented", "unsafe", "unknown"):
        if state not in states:
            errors.append(f"expected shelf fixture is missing state: {state}")
    for group in shelf.get("groups", []):
        if group.get("dimensions", {}).get("branded"):
            if group.get("eligible_unbranded_runs") != 0 or group.get("shelf_state") != "unknown":
                errors.append("branded group is contaminating unbranded shelf metrics")
        for name, metric in group.get("metrics", {}).items():
            if isinstance(metric, dict) and "rate" in metric:
                if "numerator" not in metric or "denominator" not in metric:
                    errors.append(f"shelf metric {name} lacks numerator or denominator")

    if len(normalized) != shelf.get("summary", {}).get("observation_count"):
        errors.append("normalized observation count does not match shelf summary")

    if wedges.get("schema_version") != "organic-discovery/wedge-plan/1.0":
        errors.append("expected wedge schema version is wrong")
    wedge_summary = wedges.get("summary", {})
    if wedge_summary.get("accepted_count") != 2 or wedge_summary.get("rejected_count") != 3:
        errors.append("expected wedge fixture must contain two accepted and three rejected cases")
    for item in wedges.get("rejected", []):
        if not item.get("hard_gates"):
            errors.append(f"rejected wedge {item.get('wedge_id')} lacks hard-gate reasons")
    if "not an engine score" not in report or "No fixed time-to-shelf" not in report:
        errors.append("shelf report is missing evidence boundaries")


def compare_files(actual: Path, expected: Path, label: str, errors: list[str]) -> None:
    if not actual.is_file():
        errors.append(f"smoke command did not create {label}")
        return
    if actual.read_bytes() != expected.read_bytes():
        errors.append(f"smoke output differs from committed expected artifact: {label}")


def run_smoke_checks(errors: list[str]) -> None:
    output = ROOT / ".validation-output"
    if output.exists():
        for child in sorted(output.rglob("*"), reverse=True):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                child.rmdir()
    output.mkdir(exist_ok=True)

    commands = (
        [sys.executable, "scripts/od.py", "--version"],
        [sys.executable, "scripts/od.py", "audit", "examples/sample-site/site/index.html", "--output", str(output / "audit")],
        [sys.executable, "scripts/od.py", "facts", "validate", "examples/sample-shelf/fact-registry.csv", "--output", str(output / "facts.json")],
        [sys.executable, "scripts/od.py", "shelf", "map", "examples/sample-shelf/observations.jsonl", "--facts", "examples/sample-shelf/fact-registry.csv", "--output", str(output / "shelf")],
        [sys.executable, "scripts/od.py", "wedge", "plan", str(output / "shelf" / "shelf-map.json"), "--facts", "examples/sample-shelf/fact-registry.csv", "--candidates", "examples/sample-shelf/candidates.json", "--output", str(output / "wedge-plan.json")],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode:
            errors.append(f"command failed ({' '.join(command)}): {result.stderr.strip() or result.stdout.strip()}")

    for name in ("audit.json", "work-orders.json", "report.md"):
        compare_files(output / "audit" / name, AUDIT_EXPECTED / name, f"audit/{name}", errors)
    compare_files(output / "facts.json", SHELF_EXPECTED / "facts.json", "facts.json", errors)
    for name in ("normalized-observations.jsonl", "shelf-map.json", "shelf-report.md"):
        compare_files(output / "shelf" / name, SHELF_EXPECTED / name, f"shelf/{name}", errors)
    compare_files(output / "wedge-plan.json", SHELF_EXPECTED / "wedge-plan.json", "wedge-plan.json", errors)

    for child in sorted(output.rglob("*"), reverse=True):
        if child.is_file():
            child.unlink()
        elif child.is_dir():
            child.rmdir()
    output.rmdir()


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    for rel in sorted(REQUIRED_FILES):
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if not SKILL.is_file():
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    skill_text = SKILL.read_text(encoding="utf-8")
    lines = skill_text.splitlines()
    meta, frontmatter_errors = parse_frontmatter(skill_text)
    errors.extend(frontmatter_errors)
    name = meta.get("name", "")
    description = meta.get("description", "")
    skill_version = meta.get("metadata.version", "")

    if name != "organic-discovery":
        errors.append(f"skill name must be 'organic-discovery', found {name!r}")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("skill name must be lowercase alphanumeric with single hyphens")
    if not description or len(description) > 1024:
        errors.append("description is required and must not exceed 1024 characters")
    if not skill_version:
        errors.append("metadata.version is required")
    if len(lines) > 500:
        errors.append(f"SKILL.md exceeds 500 lines ({len(lines)})")

    require_terms(SKILL, REQUIRED_SKILL_TERMS, "SKILL.md", errors)
    require_terms(README, REQUIRED_README_TERMS, "README.md", errors)
    require_terms(ROADMAP, REQUIRED_ROADMAP_TERMS, "docs/ROADMAP.md", errors)
    require_terms(DEFINITION_OF_DONE, REQUIRED_DOD_TERMS, "docs/DEFINITION-OF-DONE.md", errors)

    for rel in sorted(set(RELATIVE_REF_RE.findall(skill_text))):
        if not (ROOT / rel).is_file():
            errors.append(f"broken referenced path in SKILL.md: {rel}")

    for markdown in sorted(ROOT.rglob("*.md")):
        text = markdown.read_text(encoding="utf-8")
        if text.count("```") % 2:
            errors.append(f"unbalanced fenced code block: {markdown.relative_to(ROOT)}")
        if re.search(r"\b(?:TODO|FIXME|TBD)\b", text):
            warnings.append(f"placeholder marker found: {markdown.relative_to(ROOT)}")

    validate_local_links(errors)
    validate_json_and_jsonl(errors)

    if EVALS.is_file():
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
        if payload.get("skill") != name:
            errors.append("eval skill name does not match SKILL.md")
        cases = payload.get("cases", [])
        positives = sum(case.get("should_trigger") is True for case in cases)
        negatives = sum(case.get("should_trigger") is False for case in cases)
        if positives < 15 or negatives < 10:
            errors.append(f"trigger evals need at least 15 positive and 10 negative cases; found {positives} and {negatives}")
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

    validate_openai_metadata(errors)
    validate_citation(skill_version, errors)
    validate_workflow(errors)
    validate_versions(skill_version, errors)
    validate_audit_fixture(errors)
    validate_shelf_fixture(errors)
    run_smoke_checks(errors)

    if (ROOT / "AGENTS.md").is_file():
        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for term in (
            "python scripts/validate_skill.py",
            "python -m unittest discover -s tests -v",
            "Public third-party posting is human-approved by default",
            "planned capability",
            "Branded validation",
            "hard gate",
        ):
            if term not in agents_text:
                errors.append(f"AGENTS.md is missing: {term}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "OK: organic-discovery validated "
        f"(project {skill_version}, legacy audit {LEGACY_AUDIT_VERSION}, "
        f"{len(lines)} SKILL.md lines, {len(REQUIRED_FILES)} required files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
