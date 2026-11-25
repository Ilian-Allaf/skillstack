"""Checks of the lint pass runner: the user's decisions, the diff, and what blocks. No Node needed;
the rules themselves are tested by the pack's own suite, which tools/check.py runs."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/constitution/lint/lint_diff.py"
SPEC = importlib.util.spec_from_file_location("lint_diff", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE  # dataclasses look their module up there
SPEC.loader.exec_module(MODULE)
PACK = MODULE.load_packs()["typescript"]
ENTRY = """# TypeScript rules

Pass: private

## Rules

| Rule | Decision | Reason |
|---|---|---|
| `no-unknown-returns` | on | |
| no-module-mocking | off | the payment SDK cannot run locally |

## Exceptions

| Rule | File | Reason |
|---|---|---|
| no-unknown-returns | src/legacy/*.ts | parsed by the caller, approved 2026-11-25 |
"""


def entry(text: str | None):
    return MODULE.parse_entry(Path("lint/typescript.md"), text)


class ProjectNameTest(unittest.TestCase):
    def test_remote_forms(self) -> None:
        for remote in ["https://github.com/Photo-Platform/photo-platform.git", "git@github.com:Photo-Platform/photo-platform.git", "ssh://git@github.com/Photo-Platform/photo-platform"]:
            self.assertEqual(MODULE.project_name(remote, ""), "photo-platform__photo-platform", remote)

    def test_no_remote_uses_the_main_checkout(self) -> None:
        self.assertEqual(MODULE.project_name("", "/home/me/Notes-App/.git"), "notes-app")


class EntryTest(unittest.TestCase):
    def test_private_entry(self) -> None:
        read = entry(ENTRY)
        self.assertEqual(read.kind, "private")
        self.assertEqual(read.decisions, {"no-unknown-returns": "on", "no-module-mocking": "off"})
        self.assertEqual(read.exceptions, [("no-unknown-returns", "src/legacy/*.ts")])

    def test_route_missing_and_off(self) -> None:
        self.assertEqual(entry("This lives in the repo at eslint.config.js. Read it there instead.\n").route, "eslint.config.js")
        self.assertEqual(entry(None).kind, "missing")
        self.assertEqual(entry("# TypeScript rules\n\nPass: off\n").kind, "off")

    def test_a_bad_decision_stops_with_a_fix(self) -> None:
        with self.assertRaisesRegex(MODULE.PassError, "Fix: write on or off"):
            entry(ENTRY.replace("| on |", "| yes |"))

    def test_no_pass_line_stops_with_a_fix(self) -> None:
        with self.assertRaisesRegex(MODULE.PassError, "Pass: private"):
            entry(ENTRY.replace("Pass: private", ""))


class DiffTest(unittest.TestCase):
    def test_added_and_edited_lines(self) -> None:
        diff = "\n".join([
            "diff --git a/src/a.ts b/src/a.ts", "--- a/src/a.ts", "+++ b/src/a.ts",
            "@@ -2 +2,2 @@", "-old", "+edited", "+added",
            "@@ -9,0 +11 @@", "+late",
            "diff --git a/gone.ts b/gone.ts", "--- a/gone.ts", "+++ /dev/null", "@@ -1 +0,0 @@", "-x",
        ])
        self.assertEqual(MODULE.parse_diff(diff), {"src/a.ts": {2: "edited", 3: "added", 11: "late"}})

    def test_changed_lines_in_a_real_repo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            def git(*args: str) -> None:
                subprocess.run(["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=repo, check=True, capture_output=True)
            git("init", "-q", "-b", "main")
            (repo / "a.ts").write_text("one\ntwo\n", encoding="utf-8")
            git("add", ".")
            git("commit", "-qm", "base")
            git("checkout", "-qb", "task")
            (repo / "a.ts").write_text("one\nTWO\nthree\n", encoding="utf-8")
            (repo / "new.ts").write_text("x\n", encoding="utf-8")
            changed = MODULE.changed_lines(repo, "main")
            self.assertEqual(changed["a.ts"], {2: "TWO", 3: "three"})
            self.assertIsNone(changed["new.ts"])


class LevelsTest(unittest.TestCase):
    def test_on_blocks_off_skips_and_new_rules_warn(self) -> None:
        check_levels, undecided = MODULE.levels(PACK, entry(ENTRY), everything=False)
        self.assertEqual(check_levels["typescript-rules/no-unknown-returns"], "error")
        self.assertNotIn("typescript-rules/no-module-mocking", check_levels)
        self.assertEqual(check_levels["typescript-rules/no-runtime-typeof"], "warn")
        self.assertIn("no-runtime-typeof", undecided)

    def test_everything_turns_every_check_on(self) -> None:
        check_levels, undecided = MODULE.levels(PACK, entry(None), everything=True)
        self.assertEqual(set(check_levels.values()), {"error"})
        self.assertEqual(undecided, set())

    def test_options_reach_the_config(self) -> None:
        config = MODULE.build_config(PACK, {"typescript-rules/no-runtime-typeof": "error"}, Path("/cache/dist/plugin.mjs"))
        self.assertEqual(config["rules"]["typescript-rules/no-runtime-typeof"], ["error", {"allowInTypeGuards": True}])
        self.assertEqual(set(config["categories"].values()), {"off"})


class FindingsTest(unittest.TestCase):
    def finding(self, file: str, line: int, rule: str = "no-unknown-returns"):
        return MODULE.Finding(file, line, rule, "message", True)

    def test_only_changed_lines_and_new_files_count(self) -> None:
        changed = {"src/a.ts": {3: "x"}, "src/new.ts": None}
        kept = MODULE.keep([self.finding("src/a.ts", 3), self.finding("src/a.ts", 4), self.finding("src/new.ts", 9), self.finding("src/b.ts", 1)], changed, [])
        self.assertEqual([(f.file, f.line) for f in kept], [("src/a.ts", 3), ("src/new.ts", 9)])

    def test_an_exception_drops_its_rule_in_its_files(self) -> None:
        changed = {"src/legacy/x.ts": None}
        kept = MODULE.keep([self.finding("src/legacy/x.ts", 1), self.finding("src/legacy/x.ts", 2, "no-reflect-get")], changed, entry(ENTRY).exceptions)
        self.assertEqual([f.rule for f in kept], ["no-reflect-get"])

    def test_diagnostics_map_to_rule_ids(self) -> None:
        diagnostics = [
            {"code": "typescript-rules(no-unknown-returns)", "severity": "error", "filename": "src\\a.ts", "message": "m", "labels": [{"span": {"line": 4}}]},
            {"code": "oxc(no-accumulating-spread)", "severity": "warning", "filename": "src/b.ts", "message": "m", "labels": [{"span": {"line": 2}}]},
        ]
        found = MODULE.to_findings(diagnostics, PACK)
        self.assertEqual([(f.file, f.line, f.rule, f.blocking) for f in found], [("src/a.ts", 4, "no-unknown-returns", True), ("src/b.ts", 2, "no-reduce-accumulator-copy", False)])

    def test_a_disable_comment_for_a_framework_rule_blocks(self) -> None:
        changed = {"src/a.ts": {1: "// eslint-disable-next-line typescript-rules/no-unknown-returns", 2: "// eslint-disable-next-line no-console"}}
        found = MODULE.suppressions(PACK, changed, Path("."))
        self.assertEqual([(f.line, f.rule, f.blocking) for f in found], [(1, "no-unknown-returns", True)])


class NodeTest(unittest.TestCase):
    def test_versions(self) -> None:
        floors = ["20.19", "22.12"]
        for version, ok in [("v20.10.0", False), ("v20.19.1", True), ("v21.7.0", False), ("v22.11.0", False), ("v22.12.0", True), ("v24.1.0", True)]:
            self.assertEqual(MODULE.node_supported(version, floors), ok, version)


class PackTest(unittest.TestCase):
    """The rule ids agree across the language file, the pack, and the plugin."""

    def test_every_pack_rule_is_a_row_of_the_language_file(self) -> None:
        text = (ROOT / "skills/constitution/references/languages/typescript.md").read_text(encoding="utf-8")
        ids = set(re.findall(r"^\| `([a-z0-9-]+)` \|", text, re.MULTILINE))
        missing = set(PACK["rules"]) - ids
        self.assertEqual(missing, set(), "pack rules with no row in languages/typescript.md")

    def test_every_plugin_check_is_registered_and_has_a_test(self) -> None:
        index = (PACK["dir"] / "plugin/index.ts").read_text(encoding="utf-8")
        registered = {f"typescript-rules/{name}" for name in re.findall(r'^\t\t"([a-z-]+)":', index, re.MULTILINE)}
        in_pack = {check for checks in PACK["rules"].values() for check in checks if check.startswith("typescript-rules/")}
        self.assertEqual(registered, in_pack)
        for check in in_pack:
            name = check.split("/", 1)[1]
            self.assertTrue((PACK["dir"] / f"plugin/rules/{name}.test.ts").is_file(), name)

    def test_the_manifest_pins_exact_versions(self) -> None:
        manifest = json.loads((PACK["dir"] / "package.json").read_text(encoding="utf-8"))
        for name, version in {**manifest["dependencies"], **manifest["devDependencies"]}.items():
            self.assertRegex(version, r"^\d+\.\d+\.\d+$", name)
        self.assertEqual(manifest["dependencies"]["oxlint"], manifest["dependencies"]["@oxlint/plugins"])


if __name__ == "__main__":
    unittest.main()
