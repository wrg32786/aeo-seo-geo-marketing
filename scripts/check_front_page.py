#!/usr/bin/env python3
"""Check a Markdown front page (README or docs landing page) against the playbook.

Checks for a direct-answer opener, a FAQ, an evidence and limits section,
install, machine-changes and alternatives sections, em and en dashes, and
superlatives. Standard library only. Exit code 1 when a required check fails.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

DASHES = {"\u2014": "em dash", "\u2013": "en dash"}
SUPERLATIVES = (
    "best",
    "ultimate",
    "leading",
    "revolutionary",
    "world-class",
    "cutting-edge",
    "game-changing",
    "unparalleled",
    "seamless",
    "seamlessly",
    "blazing",
    "definitive",
    "premier",
    "most powerful",
    "state-of-the-art",
)
SUPERLATIVE_RE = re.compile(
    r"(?<![\w-])(" + "|".join(re.escape(word) for word in SUPERLATIVES) + r")(?![\w-])",
    re.IGNORECASE,
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
MAX_OPENER_WORDS = 40


def _strip_inline_code(line: str) -> str:
    return re.sub(r"`[^`]*`", "", line)


def _prose_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line_number, text) for lines outside fenced code blocks."""
    result: list[tuple[int, str]] = []
    in_fence = False
    for number, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            result.append((number, line))
    return result


def _headings(prose: list[tuple[int, str]]) -> list[tuple[int, int, str]]:
    found = []
    for number, line in prose:
        match = HEADING_RE.match(line)
        if match:
            found.append((number, len(match.group(1)), match.group(2)))
    return found


def _is_decoration(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return True
    if stripped.startswith(("[![", "![", "<", "---", "|", ">")):
        return True
    # Navigation rows such as "[Install](#install) · [FAQ](#faq)".
    without_links = re.sub(r"\[[^\]]*\]\([^)]*\)", "", stripped)
    if stripped.startswith("[") and not re.search(r"[A-Za-z]{3,}", without_links.replace("·", "")):
        return True
    return False


def _opener(prose: list[tuple[int, str]]) -> tuple[int, str] | None:
    seen_h1 = False
    paragraph: list[str] = []
    start = 0
    for number, line in prose:
        heading = HEADING_RE.match(line)
        if heading:
            if seen_h1 and paragraph:
                break
            if heading.group(1) == "#":
                seen_h1 = True
                continue
            if seen_h1:
                break
            continue
        if not seen_h1:
            continue
        if _is_decoration(line):
            if paragraph:
                break
            continue
        if not paragraph:
            start = number
        paragraph.append(line.strip())
    if not paragraph:
        return None
    return start, " ".join(paragraph)


def _first_sentence(text: str) -> str:
    plain = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    plain = plain.replace("**", "").replace("__", "")
    match = re.match(r"(.+?[.!?])(\s|$)", plain)
    return (match.group(1) if match else plain).strip()


def _section_lines(prose, headings, pattern: re.Pattern[str]) -> tuple[int, list[tuple[int, str]]] | None:
    for index, (number, level, title) in enumerate(headings):
        # A question heading that mentions the pattern ("Is FAQ schema worth it?")
        # is content, not the section heading itself.
        if pattern.search(title) and not title.rstrip().endswith("?"):
            end = None
            for next_number, next_level, _ in headings[index + 1 :]:
                if next_level <= level:
                    end = next_number
                    break
            body = [(n, t) for n, t in prose if n > number and (end is None or n < end)]
            return number, body
    return None


def check(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    prose = _prose_lines(lines)
    headings = _headings(prose)
    checks: list[dict[str, Any]] = []

    def add(check_id: str, status: str, detail: str, lines_: list[int] | None = None) -> None:
        item: dict[str, Any] = {"id": check_id, "status": status, "detail": detail}
        if lines_:
            item["lines"] = lines_
        checks.append(item)

    opener = _opener(prose)
    if opener is None:
        add("direct_answer_opener", "fail", "No prose paragraph found under the H1.")
    else:
        line_number, paragraph = opener
        sentence = _first_sentence(paragraph)
        words = len(sentence.split())
        defines = re.search(r"\b(is|are)\b", sentence, re.IGNORECASE) is not None
        if defines and words <= MAX_OPENER_WORDS:
            add("direct_answer_opener", "pass", f"Opener defines the subject in {words} words.", [line_number])
        elif defines:
            add(
                "direct_answer_opener",
                "warn",
                f"Opener defines the subject but runs {words} words; aim for {MAX_OPENER_WORDS} or fewer.",
                [line_number],
            )
        else:
            add(
                "direct_answer_opener",
                "fail",
                "First sentence under the H1 does not say what this is (no 'is' or 'are').",
                [line_number],
            )

    faq = _section_lines(prose, headings, re.compile(r"\b(faq|frequently asked)\b", re.IGNORECASE))
    if faq is None:
        add("faq", "fail", "No FAQ heading found.")
    else:
        number, _body = faq
        questions = [n for n, level, title in headings if n > number and title.rstrip().endswith("?")]
        if len(questions) >= 3:
            add("faq", "pass", f"FAQ found with {len(questions)} question headings.", [number])
        else:
            add("faq", "warn", "FAQ found but fewer than three question headings ending in '?'.", [number])

    def heading_check(check_id: str, pattern: str, missing_status: str, label: str) -> None:
        found = [n for n, _level, title in headings if re.search(pattern, title, re.IGNORECASE)]
        if found:
            add(check_id, "pass", f"{label} section found.", found[:1])
        else:
            add(check_id, missing_status, f"No {label} section found.")

    heading_check("evidence_and_limits", r"\b(evidence|limits|limitations)\b", "fail", "evidence and limits")
    heading_check("install", r"\binstall", "warn", "install")
    heading_check("machine_changes", r"what (this|it) changes", "warn", "'what this changes on your machine'")
    heading_check("alternatives", r"\balternatives\b", "warn", "alternatives")

    dash_lines: list[int] = []
    super_lines: list[int] = []
    super_words: set[str] = set()
    for number, line in prose:
        visible = _strip_inline_code(line)
        if any(dash in visible for dash in DASHES):
            dash_lines.append(number)
        visible_no_urls = re.sub(r"\]\([^)]*\)", "]", visible)
        for match in SUPERLATIVE_RE.finditer(visible_no_urls):
            super_lines.append(number)
            super_words.add(match.group(1).lower())
    if dash_lines:
        add("no_em_or_en_dashes", "fail", f"Found em or en dashes on {len(dash_lines)} line(s).", dash_lines)
    else:
        add("no_em_or_en_dashes", "pass", "No em or en dashes outside code.")
    if super_lines:
        add(
            "no_superlatives",
            "warn",
            "Possible superlatives: " + ", ".join(sorted(super_words)) + ". Replace with a checkable fact or quote the user's words.",
            sorted(set(super_lines)),
        )
    else:
        add("no_superlatives", "pass", "No listed superlatives outside code.")

    failed = [item["id"] for item in checks if item["status"] == "fail"]
    return {
        "ok": not failed,
        "failed": failed,
        "warnings": [item["id"] for item in checks if item["status"] == "warn"],
        "checks": checks,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("path", help="Markdown file to check, for example README.md")
    parser.add_argument("--json", action="store_true", help="Print the full result as JSON")
    args = parser.parse_args(argv)

    path = Path(args.path)
    if not path.is_file():
        print(f"ERROR: not a file: {path}", file=sys.stderr)
        return 2
    result = check(path.read_text(encoding="utf-8"))
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for item in result["checks"]:
            where = f" (line {', '.join(map(str, item['lines'][:8]))})" if item.get("lines") else ""
            print(f"{item['status'].upper():4} {item['id']}: {item['detail']}{where}")
        print("OK" if result["ok"] else "FAILED: " + ", ".join(result["failed"]))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
