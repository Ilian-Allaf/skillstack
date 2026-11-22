"""Regression checks for the evidence omissions observed in the first real run."""

from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ship/scripts/check_evidence.py"
SPEC = importlib.util.spec_from_file_location("check_evidence", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
PATCH = "a" * 40


class EvidenceTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "run.txt").write_text("command, observed, expected", encoding="utf-8")
        self.record = {
            "cases": [{"id": "1", "level": 4, "evidence": ["run.txt"]}],
            "steps": [{"name": "Frame", "status": "done", "result": "red", "trace": "run.txt"}],
            "required_artifacts": ["run.txt"],
            "verdict": {"patch_id": PATCH},
        }

    def errors(self, record=None, patch=PATCH):
        return MODULE.check(self.record if record is None else record, self.root, patch)

    def test_valid_record_and_pure_rebase(self):
        self.assertEqual([], self.errors())
        self.record["verdict"] = None
        self.assertEqual([], self.errors())

    def test_invalid_levels(self):
        for level in (0, 6, -1, True, 4.0, "5", None):
            with self.subTest(level=level):
                self.record["cases"][0]["level"] = level
                self.assertTrue(self.errors())

    def test_all_valid_levels(self):
        for level in range(1, 6):
            self.record["cases"][0]["level"] = level
            self.assertEqual([], self.errors())

    def test_case_requires_evidence_or_reason(self):
        self.record["cases"][0]["evidence"] = []
        self.assertTrue(self.errors())
        self.record["cases"][0]["not_verified"] = "No live access; grant test access"
        self.assertEqual([], self.errors())

    def test_each_artifact_source_rejects_missing_empty_and_directory(self):
        for value in ("missing.mp4", "empty.txt", ".", "", None):
            (self.root / "empty.txt").touch()
            for target in ("case", "step", "required"):
                with self.subTest(value=value, target=target):
                    record = copy.deepcopy(self.record)
                    if target == "case":
                        record["cases"][0]["evidence"] = [value]
                    elif target == "step":
                        record["steps"][0]["trace"] = value
                    else:
                        record["required_artifacts"] = [value]
                    self.assertTrue(self.errors(record))

    def test_done_needs_result_and_trace(self):
        for key in ("result", "trace"):
            record = copy.deepcopy(self.record)
            del record["steps"][0][key]
            self.assertTrue(self.errors(record))

    def test_skip_and_unverified_need_reason_but_no_trace(self):
        for status in ("skip", "unverified"):
            self.record["steps"][0] = {"name": "Frame", "status": status, "result": "Activity unavailable"}
            self.assertEqual([], self.errors())
            self.record["steps"][0]["result"] = " "
            self.assertTrue(self.errors())
        self.record["steps"][0]["status"] = "pending"
        self.assertTrue(self.errors())

    def test_stale_verdict_and_abbreviated_patch(self):
        self.assertTrue(self.errors(patch="b" * 40))
        self.assertTrue(self.errors(patch="a" * 7))
        self.record["verdict"] = "PASS"
        self.assertTrue(self.errors())

    def test_invalid_lists_rows_and_duplicate_names(self):
        for key in ("cases", "steps"):
            for value in (None, [], "rows", [None], [{}]):
                record = copy.deepcopy(self.record)
                record[key] = value
                self.assertTrue(self.errors(record))
            record = copy.deepcopy(self.record)
            record[key] *= 2
            self.assertTrue(self.errors(record))
        for key in ("evidence",):
            self.record["cases"][0][key] = None
            self.assertTrue(self.errors())

    def test_required_list_is_explicit(self):
        del self.record["required_artifacts"]
        self.assertTrue(self.errors())
        self.record["required_artifacts"] = []
        self.assertEqual([], self.errors())

    def test_top_level_must_be_object(self):
        for value in ([], "PASS", 1):
            self.assertTrue(self.errors(value))

    def test_cli_reports_bad_json_and_bad_evidence(self):
        path = self.root / "record.json"
        for content, expected in (("{", 1), (json.dumps(self.record), 0), ("{}", 1)):
            path.write_text(content, encoding="utf-8")
            result = subprocess.run(
                [sys.executable, "-I", str(SCRIPT), str(path), "--patch-id", PATCH],
                capture_output=True, text=True, cwd=self.root.parent,
            )
            self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        path.unlink()
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), str(path), "--patch-id", PATCH],
            capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("Fix:", result.stdout)


if __name__ == "__main__":
    unittest.main()
