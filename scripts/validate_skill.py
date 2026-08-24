#!/usr/bin/env python3
from __future__ import annotations

import json
import re
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
    "scripts/validate_skill.py",
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
    "open",
    "fact registry",
    "human approval",
    "Reddit",
    "llms.txt",
    "rollback",
    "business result",
    "supervised execute",
    "Repository capability boundary",
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
    "does **not yet ship**",
    "Install",
    "Roadmap",
    "Self-audit",
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
    "Current state — v0.3.1",
    "does **not yet ship**",
    "v0.4 — Deterministic audit foundation",
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
    "v1.0 acceptance scenario",
}

RELATIVE_REF_RE = re.compile(r"`((?:references|scripts|evals|docs|agents)/[^`]+)`")
LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


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


def require_terms(path: Path, terms: set[str], label: str, errors: list[str]) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    missing = sorted(term for term in terms if term not in text)
    if missing:
        errors.append(f"{label} is missing required terms: " + ", ".join(missing))


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
    if "python scripts/validate_skill.py" not in text:
        errors.append("validation workflow does not run scripts/validate_skill.py")
    if "pull_request:" not in text:
        errors.append("validation workflow must run on pull requests")


def validate_current_vs_planned(errors: list[str]) -> None:
    if not README.is_file() or not ROADMAP.is_file():
        return
    readme = README.read_text(encoding="utf-8")
    roadmap = ROADMAP.read_text(encoding="utf-8")

    if not OD_CLI.exists():
        if "does **not yet ship**" not in readme or "`scripts/od.py`" not in readme:
            errors.append("README must explicitly disclose that scripts/od.py is not shipped")
        bash_blocks = re.findall(r"```(?:bash|shell)\n(.*?)```", readme, flags=re.DOTALL)
        if any("scripts/od.py" in block for block in bash_blocks):
            errors.append("README exposes a runnable scripts/od.py example before the file exists")
        if "does **not yet ship**" not in roadmap:
            errors.append("ROADMAP must disclose missing executable capabilities")
    else:
        if "v0.4 — Deterministic audit foundation" not in roadmap:
            errors.append("scripts/od.py exists but the v0.4 roadmap contract is missing")

    forbidden_current_claims = (
        "currently ships a dashboard",
        "currently ships an autonomous publisher",
        "currently ships a scheduler",
        "v0.4 is live",
    )
    lowered = readme.lower()
    for claim in forbidden_current_claims:
        if claim in lowered:
            errors.append(f"README contains unsupported current capability claim: {claim}")


def validate_versions(skill_version: str, errors: list[str]) -> None:
    if not skill_version:
        return
    if CHANGELOG.is_file() and f"## {skill_version} " not in CHANGELOG.read_text(encoding="utf-8"):
        errors.append(f"CHANGELOG has no release entry for version {skill_version}")
    if README.is_file() and f"version-{skill_version}-" not in README.read_text(encoding="utf-8"):
        errors.append("README version badge does not match SKILL.md")


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
    if len(name) > 64:
        errors.append("skill name exceeds 64 characters")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        errors.append("skill name must be lowercase alphanumeric with single hyphens")
    if not description:
        errors.append("description is required")
    elif len(description) > 1024:
        errors.append(f"description exceeds 1024 characters ({len(description)})")
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
        for rel in ("docs/PRODUCT-VISION.md", "docs/ROADMAP.md", "docs/DEFINITION-OF-DONE.md"):
            if rel not in readme_text:
                errors.append(f"README does not link product document: {rel}")

    if EVALS.is_file():
        try:
            payload = json.loads(EVALS.read_text(encoding="utf-8"))
            if payload.get("skill") != name:
                errors.append("eval skill name does not match SKILL.md")
            if skill_version and payload.get("version") != skill_version:
                errors.append(
                    f"eval version {payload.get('version')!r} does not match skill version {skill_version!r}"
                )
            cases = payload.get("cases", [])
            positives = sum(case.get("should_trigger") is True for case in cases)
            negatives = sum(case.get("should_trigger") is False for case in cases)
            if positives < 12 or negatives < 10:
                errors.append(
                    f"trigger evals need at least 12 positive and 10 negative cases; found {positives} and {negatives}"
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
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"invalid eval JSON: {exc}")

    validate_openai_metadata(errors)
    validate_citation(skill_version, errors)
    validate_workflow(errors)
    validate_current_vs_planned(errors)
    validate_versions(skill_version, errors)

    if (ROOT / "AGENTS.md").is_file():
        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        if "python scripts/validate_skill.py" not in agents_text:
            errors.append("AGENTS.md must declare the required validation command")
        if "Public third-party posting is human-approved by default" not in agents_text:
            errors.append("AGENTS.md must preserve the third-party approval gate")
        if "planned capability" not in agents_text:
            errors.append("AGENTS.md must preserve current-versus-planned release truth")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(
        "OK: organic-discovery skill validated "
        f"(version {skill_version}, {len(lines)} SKILL.md lines, {len(REQUIRED_FILES)} required files)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
