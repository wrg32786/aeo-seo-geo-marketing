from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("od", ROOT / "scripts" / "od.py")
assert SPEC and SPEC.loader
od = importlib.util.module_from_spec(SPEC)
sys.modules["od"] = od
SPEC.loader.exec_module(od)


class OrganicDiscoveryAuditorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.old_cwd = Path.cwd()
        os.chdir(ROOT)

    def tearDown(self) -> None:
        os.chdir(self.old_cwd)

    def test_offline_fixture_matches_committed_outputs(self) -> None:
        target = "examples/sample-site/site/index.html"
        with tempfile.TemporaryDirectory() as temp_dir:
            exit_code = od.main(["audit", target, "--output", temp_dir])
            self.assertEqual(exit_code, 0)
            for name in ("audit.json", "work-orders.json", "report.md"):
                generated = Path(temp_dir, name).read_text(encoding="utf-8")
                expected = (ROOT / "examples" / "sample-site" / "expected" / name).read_text(encoding="utf-8")
                self.assertEqual(generated, expected, name)

    def test_fixture_exposes_required_failure_classes_without_score(self) -> None:
        document = od.load_target(
            "examples/sample-site/site/index.html",
            timeout=1,
            max_bytes=od.DEFAULT_MAX_BYTES,
            max_redirects=od.DEFAULT_MAX_REDIRECTS,
            user_agent=od.DEFAULT_USER_AGENT,
        )
        audit, work_orders, _report = od.audit_document(document)
        codes = {finding["code"] for finding in audit["findings"]}
        required = {
            "canonical.local_fixture_mismatch",
            "robots.ai_search_blocked",
            "rendering.javascript_only_risk",
            "schema.visible_mismatch",
            "claims.provenance_gap",
            "manipulation.hidden_instruction",
            "sitemap.target_missing",
        }
        self.assertTrue(required.issubset(codes), required - codes)
        self.assertIsNone(audit["summary"]["opaque_score"])
        for stage in ("activation", "retrieval", "context_allocation", "source_selection", "absorption", "behavior"):
            self.assertEqual(audit["stages"][stage]["status"], "unknown")
        self.assertTrue(work_orders)
        for order in work_orders:
            self.assertTrue(order["acceptance"])
            self.assertTrue(order["rollback"])

    def test_private_and_non_http_targets_are_rejected(self) -> None:
        for url in ("http://127.0.0.1/", "http://[::1]/", "file:///etc/passwd", "ftp://example.com/file"):
            with self.subTest(url=url), self.assertRaises(od.AuditError):
                od.validate_public_url(url)

    def test_dns_result_with_any_non_public_address_is_rejected(self) -> None:
        public = (od.socket.AF_INET, od.socket.SOCK_STREAM, 6, "", ("93.184.216.34", 443))
        private = (od.socket.AF_INET, od.socket.SOCK_STREAM, 6, "", ("10.0.0.8", 443))
        with mock.patch.object(od.socket, "getaddrinfo", return_value=[public, private]):
            with self.assertRaises(od.AuditError):
                od.validate_public_url("https://example.com/")
        with mock.patch.object(od.socket, "getaddrinfo", return_value=[public]):
            parsed, addresses = od.validate_public_url("https://example.com/")
            self.assertEqual(parsed.hostname, "example.com")
            self.assertEqual(addresses[0].ip, "93.184.216.34")

    def test_jsonld_graph_and_invalid_blocks_are_handled(self) -> None:
        documents, errors = od.parse_json_ld(
            [
                '{"@context":"https://schema.org","@graph":[{"@type":"Product","name":"Example"}]}',
                "{not-json}",
            ]
        )
        self.assertEqual(od.json_ld_types(documents), ["Product"])
        self.assertEqual(len(errors), 1)
        values = od.important_schema_values(documents)
        self.assertIn({"field": "name", "value": "Example"}, values)

    def test_expected_json_contract_is_valid(self) -> None:
        audit = json.loads((ROOT / "examples/sample-site/expected/audit.json").read_text(encoding="utf-8"))
        orders = json.loads((ROOT / "examples/sample-site/expected/work-orders.json").read_text(encoding="utf-8"))
        self.assertEqual(audit["schema_version"], od.SCHEMA_VERSION)
        self.assertEqual(audit["tool"]["version"], od.VERSION)
        self.assertEqual(len(orders), audit["summary"]["finding_count"])


if __name__ == "__main__":
    unittest.main()
