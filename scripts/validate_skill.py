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
    "docs/SELF-AUDIT.md",
    "evals/trigger-evals.json",
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
    "fact registry",
    "Reddit",
    "llms.txt",
    "rollback",
}

REQUIRED_README_TERMS = {
    "SEO",
    "AEO",
    "GEO",
    "Agent Skill",
    "ChatGPT Search",
    "Google AI Overviews",
    "Claude",
    "Perplexity",
    "Bing/Copilot",
    "Install",
    "Self-audit",
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
    if "Organic Discovery" not in text:
        errors.append("agents/openai.yaml must use the canonical display name")


def validate_citation(skill_version: str, errors: list[str]) -> None:
    if not CITATION.is_file():
        return
    text = CITATION.read_text(encoding="utf-8")
    for term in ("cff-version: 1.2.0", "title:", "authors:", "repository-code:", "license: MIT"):
        if term not in text:
            errors.append(f"CITATION.cff is missing {term}")
    if skill_version and f'version: "{skill_version}"' not in text:
        errors.append("CITATION.cff version does not match SKILL.md")


def validate_workflow(errors: list[str]) -> None:
    if not WORKFLOW.is_file():
        return
    text = WORKFLOW.read_text(encoding="utf-8")
    if "python scripts/validate_skill.py" not in text:
        errors.append("validation workflow does not run scripts/validate_skill.py")
    if "pull_request:" not in text:
        errors.append("validation workflow must run on pull requests")


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

    if CHANGELOG.is_file() and skill_version:
        if f"## {skill_version} " not in CHANGELOG.read_text(encoding="utf-8"):
            errors.append(f"CHANGELOG has no release entry for version {skill_version}")

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
            if positives < 8 or negatives < 8:
                errors.append(
                    f"trigger evals need at least 8 positive and 8 negative cases; found {positives} and {negatives}"
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

    if (ROOT / "AGENTS.md").is_file():
        agents_text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        if "python scripts/validate_skill.py" not in agents_text:
            errors.append("AGENTS.md must declare the required validation command")

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
