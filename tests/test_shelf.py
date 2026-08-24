from __future__ import annotations

import csv
import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from od_shelf import (  # noqa: E402
    ShelfError,
    build_shelf_map,
    load_observations,
    plan_wedges,
    render_shelf_report,
)
from od_truth import REQUIRED_COLUMNS, validate_fact_registry  # noqa: E402


class OrganicDiscoveryShelfTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_cwd = Path.cwd()
        os.chdir(ROOT)
        self.example = ROOT / "examples" / "sample-shelf"

    def tearDown(self) -> None:
        os.chdir(self.old_cwd)

    def _build(self):
        facts = validate_fact_registry(Path("examples/sample-shelf/fact-registry.csv"))
        records = load_observations(Path("examples/sample-shelf/observations.jsonl"))
        shelf = build_shelf_map(
            records,
            observation_source="examples/sample-shelf/observations.jsonl",
            facts_report=facts,
            facts_source="examples/sample-shelf/fact-registry.csv",
        )
        plan = plan_wedges(
            shelf,
            facts,
            candidates_path=Path("examples/sample-shelf/candidates.json"),
        )
        return facts, records, shelf, plan

    def test_example_matches_committed_outputs(self) -> None:
        facts, records, shelf, plan = self._build()
        generated = {
            "facts.json": json.dumps(facts, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            "normalized-observations.jsonl": "\n".join(
                json.dumps(record, sort_keys=True, ensure_ascii=False) for record in records
            )
            + "\n",
            "shelf-map.json": json.dumps(shelf, indent=2, sort_keys=True, ensure_ascii=False)
            + "\n",
            "shelf-report.md": render_shelf_report(shelf),
            "wedge-plan.json": json.dumps(plan, indent=2, sort_keys=True, ensure_ascii=False)
            + "\n",
        }
        for name, content in generated.items():
            expected = (self.example / "expected" / name).read_text(encoding="utf-8")
            self.assertEqual(content, expected, name)

    def test_fact_registry_preserves_publication_and_source_boundaries(self) -> None:
        facts, _records, _shelf, _plan = self._build()
        self.assertTrue(facts["valid"])
        self.assertIn("kr-independent-review", facts["publishable_fact_ids"])
        self.assertIn("kr-price-draft", facts["blocked_fact_ids"])
        self.assertIn("kr-eczema-safe", facts["blocked_fact_ids"])
        self.assertEqual(facts["summary"]["independent_publishable_count"], 1)
        self.assertGreaterEqual(facts["summary"]["seller_controlled_publishable_count"], 1)
        fact = next(item for item in facts["facts"] if item["claim_id"] == "kr-magnesium")
        self.assertEqual(fact["source_control"], "seller_controlled")

    def test_approved_unavailable_or_unsourced_claim_is_invalid(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, "facts.csv")
            row = {column: "" for column in REQUIRED_COLUMNS}
            row.update(
                {
                    "claim_id": "bad-claim",
                    "entity_id": "bad-product",
                    "entity": "Bad Product",
                    "claim_type": "offer_fit",
                    "canonical_wording": "Bad Product is ideal for the prompt.",
                    "source_type": "none",
                    "verified_at": "2026-08-24",
                    "evidence_grade": "F",
                    "offer_exists": "false",
                    "availability": "unavailable",
                    "publish_status": "approved",
                    "owner": "growth",
                    "refresh_trigger": "change",
                    "prompt_families": "bad-family",
                    "market": "US",
                    "language": "en",
                }
            )
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(REQUIRED_COLUMNS))
                writer.writeheader()
                writer.writerow(row)
            report = validate_fact_registry(path)
            codes = {item["code"] for item in report["errors"]}
            self.assertFalse(report["valid"])
            self.assertIn("approved_claim_missing_source", codes)
            self.assertIn("approved_claim_offer_not_confirmed", codes)
            self.assertIn("approved_claim_unavailable", codes)

    def test_exact_surfaces_are_separate_and_branded_runs_are_excluded(self) -> None:
        _facts, records, shelf, _plan = self._build()
        sensitive = [
            group
            for group in shelf["groups"]
            if group["dimensions"]["prompt_family"] == "sensitive-skin-magnesium"
        ]
        self.assertEqual(len(sensitive), 3)
        states = {
            (group["dimensions"]["surface"], group["dimensions"]["branded"]): group["shelf_state"]
            for group in sensitive
        }
        self.assertEqual(states[("chatgpt-search", False)], "open")
        self.assertEqual(states[("gemini-web", False)], "locked")
        self.assertEqual(states[("chatgpt-search", True)], "unknown")
        branded_count = sum(record["branded"] for record in records)
        self.assertEqual(shelf["branded_exclusion"]["excluded_observation_count"], branded_count)
        for group in sensitive:
            if group["dimensions"]["branded"]:
                self.assertFalse(group["eligible_for_unbranded_recommendation_share"])

    def test_fixture_spans_open_locked_fragmented_and_unsafe_states(self) -> None:
        _facts, _records, shelf, _plan = self._build()
        states = {group["shelf_state"] for group in shelf["groups"]}
        self.assertTrue({"open", "locked", "fragmented", "unsafe", "unknown"}.issubset(states))
        unsafe = next(
            group
            for group in shelf["groups"]
            if group["dimensions"]["prompt_family"] == "eczema-safe-deodorant"
        )
        self.assertIn("unsupported universal safety claim", {
            issue
            for run_id in unsafe["observation_ids"]
            for issue in next(
                record["fidelity_issues"]
                for record in load_observations(Path("examples/sample-shelf/observations.jsonl"))
                if record["run_id"] == run_id
            )
        })
        self.assertLess(unsafe["metrics"]["fidelity"]["rate"], 0.75)

    def test_wedge_planner_hard_rejects_locked_unsafe_and_nonexistent_offers(self) -> None:
        _facts, _records, _shelf, plan = self._build()
        self.assertIsNone(plan["summary"]["opaque_geo_score"])
        accepted = {item["candidate_id"]: item for item in plan["accepted"]}
        rejected = {item["candidate_id"]: item for item in plan["rejected"]}
        self.assertEqual(set(accepted), {"wedge-kindroot-sensitive-skin", "wedge-kindroot-travel"})
        self.assertIn("wedge-kindroot-broad", rejected)
        self.assertIn("wedge-kindroot-eczema", rejected)
        self.assertIn("wedge-ghost-product", rejected)
        self.assertTrue(
            any("locked" in reason for reason in rejected["wedge-kindroot-broad"]["gate_failures"])
        )
        self.assertTrue(
            any("prohibited" in reason for reason in rejected["wedge-kindroot-eczema"]["gate_failures"])
        )
        self.assertTrue(
            any("offer exists" in reason for reason in rejected["wedge-ghost-product"]["gate_failures"])
        )
        sensitive = accepted["wedge-kindroot-sensitive-skin"]
        self.assertEqual(len(sensitive["surface_opportunities"]), 1)
        self.assertEqual(sensitive["surface_opportunities"][0]["shelf_state"], "open")
        self.assertEqual(sensitive["rejected_surfaces"][0]["shelf_state"], "locked")

    def test_missing_observation_data_remains_null_and_out_of_denominator(self) -> None:
        _facts, _records, shelf, _plan = self._build()
        open_group = next(
            group
            for group in shelf["groups"]
            if group["dimensions"]["prompt_family"] == "sensitive-skin-magnesium"
            and group["dimensions"]["surface"] == "chatgpt-search"
            and not group["dimensions"]["branded"]
        )
        retrieval = open_group["metrics"]["target_retrieval"]
        self.assertEqual(retrieval["denominator"], 3)
        self.assertEqual(open_group["runs"], 4)
        self.assertIsNotNone(retrieval["rate"])

    def test_invalid_observation_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir, "bad.jsonl")
            path.write_text('{"run_id":"bad","recommendations":[],"citations":[]}\n', encoding="utf-8")
            with self.assertRaises(ShelfError):
                load_observations(path)


if __name__ == "__main__":
    unittest.main()
