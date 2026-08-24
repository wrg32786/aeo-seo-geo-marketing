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
TEST_MODULE = ROOT / "tests" / "test_od.py"
EXPECTED_AUDIT = ROOT / "examples" / "sample-site" / "expected" / "audit.json"
EXPECTED_WORK_ORDERS = ROOT / "examples" / "sample-site" / "expected" / "work-orders.json"
EXPECTED_REPORT = ROOT / "examples" / "sample-site" / "expected" / "report.md"

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
    "scripts/od.py",
    "scripts/od_audit.py",
    "scripts/od_fetch.py",
    "scripts/validate_skill.py",
    "tests/test_od.py",
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
}

REQUIRED_README_TERMS = {
    "SEO",
    "AEO",
    "GEO",
    "Organic Growth Operator",
    "ChatGPT Search",
    "Google AI Overviews",
    "Claude",
    "Perplexity",
    "Bing/Copilot",
    "AI shelf",
    "Current state",
    "Install",
    "Roadmap",
    "Self-audit",
    "python scripts/od.py audit",
    "audit.json",
    "work-orders.json",
    "report.md",
    "does **not yet ship**",
}

REQUIRED_VISION_TERMS = {
    "Current product",
    "North Star",
    "AI shelf",
    "Authority laundering",
    "Truth and recommendation-integrity gate",
    "Public third-party participation",
    "Current capability must be stated honestly",
}

REQUIRED_ROADMAP_TERMS = {
    "Current state — v0.4.0",
    "v0.4 — Deterministic audit foundation",
    "Status: shipped",
    "v0.5 — Business Truth and AI Shelf Mapper",
    "v0.6 — GitHub-backed owned-site operator",
    "v0.7 — Content portfolio and earned-source queue",
    "v0.8 — Measurement adapters and experiment ledger",
    "v0.9 — CMS adapters and bounded autonomy",
    "v1.0 — Continuous Organic Growth Operator",
}

REQUIRED_DOD_TERMS = {
    "Release truth",
    "Demand and AI shelf",
    "Owned-site execution",
    "Earned-source integrity",
    "Outcome measurement",
    "Learning and rollback",
    "v0.4 acceptance",
    "v1.0 acceptance scenario",
}

RELATIVE_REF_RE = re.compile(r"`((?:references|scripts|evals|docs|agents|examples|tests)/[^`]+)`")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
VERSION_RE = re.compile(r'metadata:\s*\n(?:.*\n)*?\s+version:\s*["\']([^"\']+)["\']', re.MULTILINE)


def parse_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, ["SKILL.md frontmatter is not closed"]
    block = text[4:end].splitlines()
    data: dict[str, str] = {}
    current_section = None
    for raw in block:
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


def validate_openai_metadata(errors: list[str]) -> None:
    if not OPENAI_METADATA.is_file():
        return
    text = OPENAI_METADATA.read_text(encoding="utf-8")
    for term in ("display_name:", "short_description:", "default_prompt:", "allow_implicit_invocation:"):
        if term not in text:
            errors.append(f"agents/openai.yaml is missing {term}")
    if "Organic Discovery Operator" not in text:
        errors.append("agents/openai.yaml must use the operator display name")
    if "AI shelf" not in text or "rollback" not in text:
        errors.append("agents/openai.yaml default prompt must include shelf mapping and rollback")


def validate_citation(skill_version: str, errors: list[str]) -> None:
    if not CITATION.is_file():
        return
    text = CITATION.read_text(encoding="utf-8")
    for term in ("cff-version: 1.2.0", "title:", "authors:", "repository-code:", "license: MIT"):
        if term not in text:
            errors.append(f"CITATION.cff is missing {term}")
    if skill_version and f'version: "{skill_version}"' not in text:
        errors.append("CITATION.cff version does not match SKILL.md")
    if "organic growth" not in text.lower() or "AI shelf" not in text:
        errors.append("CITATION.cff does not describe the current operator scope")


def validate_workflow(errors: list[str]) -> None:
    if not WORKFLOW.is_file():
        return
    text = WORKFLOW.read_text(encoding="utf-8")
    required = (
        "python scripts/validate_skill.py",
        "python -m unittest discover -s tests -v",
        "python scripts/od.py audit examples/sample-site/site/index.html",
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
    if CHANGELOG.is_file() and f"## {skill_version} " not in CHANGELOG.read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG has no release entry for version {skill_version}")
    if README.is_file() and f"version-{skill_version}-" not in README.read_text(encoding="utf-8"):
        errors.append("README version badge does not match SKILL.md")
    if EVALS.is_file():
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
        if payload.get("version") != skill_version:
            errors.append("trigger eval version does not match SKILL.md")


def validate_auditor(skill_version: str, errors: list[str]) -> None:
    if not OD_CLI.is_file():
        return
    auditor_files = [OD_CLI, ROOT / "scripts" / "od_fetch.py", ROOT / "scripts" / "od_audit.py"]
    text = "\n".join(path.read_text(encoding="utf-8") for path in auditor_files if path.is_file())
    for term in (
        "validate_public_url",
        "resolve_public_host",
        "DEFAULT_MAX_BYTES",
        "DEFAULT_MAX_REDIRECTS",
        "opaque_score",
        "work-orders.json",
        "report.md",
    ):
        if term not in text:
            errors.append(f"scripts/od.py is missing auditor contract term: {term}")
    if skill_version and f'VERSION = "{skill_version}"' not in text:
        errors.append("scripts/od.py version does not match SKILL.md")

    try:
        audit = json.loads(EXPECTED_AUDIT.read_text(encoding="utf-8"))
        orders = json.loads(EXPECTED_WORK_ORDERS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid expected auditor output: {exc}")
        return
    if audit.get("schema_version") != skill_version:
        errors.append("expected audit schema version does not match SKILL.md")
    if audit.get("tool", {}).get("version") != skill_version:
        errors.append("expected audit tool version does not match SKILL.md")
    if audit.get("summary", {}).get("opaque_score", "missing") is not None:
        errors.append("expected audit must not contain an opaque score")
    for stage in ("activation", "retrieval", "context_allocation", "source_selection", "absorption", "behavior"):
        if audit.get("stages", {}).get(stage, {}).get("status") != "unknown":
            errors.append(f"expected audit must preserve {stage} as unknown")
    if len(orders) != audit.get("summary", {}).get("finding_count"):
        errors.append("expected work-order count does not match finding count")
    for index, order in enumerate(orders):
        if not order.get("acceptance") or not order.get("rollback"):
            errors.append(f"work order {index} lacks acceptance or rollback")
    if "No opaque readiness score" not in EXPECTED_REPORT.read_text(encoding="utf-8"):
        errors.append("expected report must state the no-score boundary")


def run_smoke_checks(errors: list[str]) -> None:
    commands = (
        [sys.executable, "scripts/od.py", "--version"],
        [sys.executable, "scripts/od.py", "audit", "examples/sample-site/site/index.html", "--output", ".validation-output"],
    )
    for command in commands:
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, check=False)
        if result.returncode:
            errors.append(f"command failed ({' '.join(command)}): {result.stderr.strip() or result.stdout.strip()}")
    output = ROOT / ".validation-output"
    for name in ("audit.json", "work-orders.json", "report.md"):
        if not (output / name).is_file():
            errors.append(f"offline smoke audit did not create {name}")
    if output.exists():
        for path in output.iterdir():
            path.unlink()
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
    require_terms(PRODUCT_VISION, REQUIRED_VISION_TERMS, "docs/PRODUCT-VISION.md", errors)
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
    for json_path in sorted(ROOT.rglob("*.json")):
        try:
            json.loads(json_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON in {json_path.relative_to(ROOT)}: {exc}")

    if README.is_file():
        readme_text = README.read_text(encoding="utf-8")
        for rel in sorted(REQUIRED_FILES):
            if rel.startswith("references/") and rel not in readme_text:
                errors.append(f"README does not list required module: {rel}")
        if "does **not yet ship** an analytics connector" not in readme_text:
            errors.append("README must preserve the post-v0.4 current-versus-planned boundary")

    if EVALS.is_file():
        payload = json.loads(EVALS.read_text(encoding="utf-8"))
        if payload.get("skill") != name:
            errors.append("eval skill name does not match SKILL.md")
        cases = payload.get("cases", [])
        positives = sum(case.get("should_trigger") is True for case in cases)
        negatives = sum(case.get("should_trigger") is False for case in cases)
        if positives < 12 or negatives < 10:
            errors.append(f"trigger evals need at least 12 positive and 10 negative cases; found {positives} and {negatives}")
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
    validate_auditor(skill_version, errors)
    run_smoke_checks(errors)

    if (ROOT / "AGENTS.md").is_file():
        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        for term in (
            "python scripts/validate_skill.py",
            "python -m unittest discover -s tests -v",
            "Public third-party posting is human-approved by default",
            "planned capability",
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
        f"(version {skill_version}, {len(lines)} SKILL.md lines, {len(REQUIRED_FILES)} required files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
