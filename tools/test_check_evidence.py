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
BASE = "b" * 40
HEAD = "c" * 40


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
            "verdict": {"patch_id": PATCH, "base_sha": BASE, "head_sha": HEAD},
        }

    def errors(self, record=None, patch=PATCH, base=BASE, head=HEAD):
        return MODULE.check(self.record if record is None else record, self.root, patch, base, head)

    def test_valid_record_and_no_verdict_yet(self):
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

    def test_changed_base_or_head_invalidates_same_patch(self):
        self.assertTrue(self.errors(base="d" * 40))
        self.assertTrue(self.errors(head="d" * 40))
        self.record["verdict"] = {"patch_id": PATCH}
        self.assertTrue(self.errors())

    def test_commit_ids_must_be_full_and_explicit(self):
        for field in ("base_sha", "head_sha"):
            for value in (None, "c" * 7, "z" * 40, "", 42):
                with self.subTest(field=field, value=value):
                    record = copy.deepcopy(self.record)
                    record["verdict"][field] = value
                    args = {"base": value} if field == "base_sha" else {"head": value}
                    self.assertTrue(self.errors(record, **args))
            record = copy.deepcopy(self.record)
            del record["verdict"][field]
            self.assertTrue(self.errors(record))

    def test_sha256_ids(self):
        self.record["verdict"] = {"patch_id": "a" * 64, "base_sha": "b" * 64, "head_sha": "c" * 64}
        self.assertEqual([], self.errors(patch="a" * 64, base="b" * 64, head="c" * 64))

    def test_conflict_free_rebase_keeps_patch_but_breaks_behavior(self):
        repo = self.root / "repo"
        repo.mkdir()

        def git(*args, data=None):
            return subprocess.run(
                ["git", "-C", str(repo), *args], input=data,
                capture_output=True, text=True, check=True,
            ).stdout.strip()

        def run_app():
            return subprocess.run(
                [sys.executable, "-I", str(repo / "app.py")],
                capture_output=True, text=True, check=True,
            ).stdout.strip()

        def patch(base, head):
            return git("patch-id", "--stable", data=git("diff", f"{base}...{head}")).split()[0]

        git("init", "-b", "main")
        git("config", "user.name", "Regression test")
        git("config", "user.email", "regression@example.invalid")
        git("config", "commit.gpgsign", "false")
        (repo / "config.json").write_text('{"factor": 1}\n', encoding="utf-8")
        (repo / "app.py").write_text(
            'import json\nfrom pathlib import Path\nfactor = json.loads(Path(__file__).with_name("config.json").read_text())["factor"]\nprint(10 * factor)\n',
            encoding="utf-8",
        )
        git("add", ".")
        git("commit", "-m", "Base")
        base = git("rev-parse", "HEAD")
        git("switch", "-c", "feature")
        app = repo / "app.py"
        app.write_text(app.read_text(encoding="utf-8").replace("print(10 * factor)", "print(20 * factor)"), encoding="utf-8")
        git("add", ".")
        git("commit", "-m", "Produce twenty")
        head = git("rev-parse", "HEAD")
        patch_id = patch(base, head)
        self.assertEqual("20", run_app())
        self.record["verdict"] = {"patch_id": patch_id, "base_sha": base, "head_sha": head}
        self.assertEqual([], self.errors(patch=patch_id, base=base, head=head))

        git("switch", "main")
        (repo / "config.json").write_text('{"factor": 2}\n', encoding="utf-8")
        git("add", ".")
        git("commit", "-m", "Change dependency behavior")
        new_base = git("rev-parse", "HEAD")
        git("switch", "feature")
        git("rebase", "main")
        new_head = git("rev-parse", "HEAD")
        self.assertEqual(patch_id, patch(new_base, new_head))
        self.assertNotEqual(head, new_head)
        self.assertEqual("40", run_app())
        self.assertTrue(self.errors(patch=patch_id, base=new_base, head=new_head))
        self.record["verdict"] = {"patch_id": patch_id, "base_sha": new_base, "head_sha": new_head}
        self.assertEqual([], self.errors(patch=patch_id, base=new_base, head=new_head))

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
                [sys.executable, "-I", str(SCRIPT), str(path), "--patch-id", PATCH, "--base-sha", BASE, "--head-sha", HEAD],
                capture_output=True, text=True, cwd=self.root.parent,
            )
            self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stderr)
        path.unlink()
        result = subprocess.run(
            [sys.executable, "-I", str(SCRIPT), str(path), "--patch-id", PATCH, "--base-sha", BASE, "--head-sha", HEAD],
            capture_output=True, text=True,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("Fix:", result.stdout)


if __name__ == "__main__":
    unittest.main()
