from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_front_page  # noqa: E402

GOOD = """# Widget: a CLI for checking widgets

[![CI](https://example.com/badge.svg)](https://example.com/ci)

Widget is a command-line tool for developers that checks widget files before release.

[Install](#install) · [FAQ](#faq)

## Install

```bash
pip install widget
```

## Evidence and limits

- Tested on 12 sample files.

## What this changes on your machine

Nothing outside the output folder.

## FAQ

### Does it need a network connection?

No.

### Is it free?

Yes, MIT.

### Does it work on Windows?

Not tested yet.

## Alternatives

- Other tools exist.
"""

BAD = """# Widget

The ultimate widget toolkit \u2014 revolutionary and seamless.

## Usage

Run it.
"""


class FrontPageCheckTests(unittest.TestCase):
    def test_good_page_passes(self) -> None:
        result = check_front_page.check(GOOD)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["warnings"], [])

    def test_bad_page_fails_required_checks(self) -> None:
        result = check_front_page.check(BAD)
        self.assertFalse(result["ok"])
        for check_id in ("faq", "evidence_and_limits", "no_em_or_en_dashes"):
            self.assertIn(check_id, result["failed"])
        self.assertIn("no_superlatives", result["warnings"])

    def test_dashes_inside_code_are_ignored(self) -> None:
        text = GOOD + "\n```text\na \u2014 b\n```\n\nUse `x \u2013 y` here.\n"
        result = check_front_page.check(text)
        self.assertTrue(result["ok"], result)

    def test_question_mentioning_faq_is_not_the_faq_section(self) -> None:
        text = GOOD.replace("## FAQ", "## Questions").replace(
            "### Is it free?", "### Is FAQ schema still worth adding?"
        )
        result = check_front_page.check(text)
        self.assertIn("faq", result["failed"])

    def test_repository_readme_practices_the_playbook(self) -> None:
        result = check_front_page.check((ROOT / "README.md").read_text(encoding="utf-8"))
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["warnings"], [], result)


if __name__ == "__main__":
    unittest.main()
