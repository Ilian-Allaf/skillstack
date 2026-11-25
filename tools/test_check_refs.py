"""Tests for check_refs.py. Run: python -I -m unittest discover -s tools -v"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_refs  # noqa: E402

REPO = Path(__file__).resolve().parent.parent


class CheckRefsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("skills/constitution/README.md", "# Constitution\n\n## Rules\n")
        self.write("skills/constitution/references/principles.md", "| Id | Apply when | Rule |\n|---|---|---|\n| `fix-root-causes` | debugging | Fix the cause. |\n")
        self.write("skills/constitution/references/principles/fix-root-causes.md", "# fix-root-causes\n")
        self.write("skills/constitution/references/glossary.md", "| Term | Meaning | Avoid |\n|---|---|---|\n| `needs-human` | a label; `one-way` door | `escalated` |\n")
        self.write("skills/ship/SKILL.md", "# Ship\n\n## Before build: read `done_when`\n\nRun [the playbook](references/playbooks/bug-fix.md) and `fix-root-causes`.\n")
        self.write("skills/ship/references/playbooks/bug-fix.md", "# Bug fix\n\nSee [ship](../../SKILL.md#before-build-read-done_when) and `ship/SKILL.md`.\n")
        self.write("README.md", "See [ship](skills/ship/SKILL.md) and `tools/check_refs.py`.\n")
        self.write("tools/check_refs.py", "")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding="utf-8")

    def edit(self, rel: str, old: str, new: str) -> None:
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, "test setup: text to replace is missing")
        path.write_text(text.replace(old, new), encoding="utf-8")

    def codes(self) -> list[str]:
        return [f.code for f in check_refs.check(self.root)]

    # A clean tree passes; this guards every other test against false positives.
    def test_clean_tree_has_no_findings(self) -> None:
        self.assertEqual([f.render(self.root) for f in check_refs.check(self.root)], [])

    def test_broken_link_in_a_doc(self) -> None:
        self.edit("README.md", "skills/ship/SKILL.md", "skills/ship/MISSING.md")
        self.assertIn("R001", self.codes())

    def test_broken_anchor(self) -> None:
        self.edit("skills/ship/references/playbooks/bug-fix.md", "#before-build-read-done_when", "#before-build")
        self.assertIn("R002", self.codes())

    def test_anchor_of_a_heading_with_code(self) -> None:
        # The heading "Before build: read `done_when`" has the anchor before-build-read-done_when.
        self.assertNotIn("R002", self.codes())

    def test_missing_backticked_path(self) -> None:
        self.edit("README.md", "`tools/check_refs.py`", "`tools/gone.py`")
        self.assertIn("R003", self.codes())

    def test_path_relative_to_a_skill(self) -> None:
        self.edit("skills/ship/references/playbooks/bug-fix.md", "`ship/SKILL.md`", "`ship/references/missing.md`")
        self.assertIn("R003", self.codes())

    def test_target_repo_paths_are_not_checked(self) -> None:
        self.edit("skills/ship/SKILL.md", "and `fix-root-causes`", "and `docs/agent-rules.md` and `fix-root-causes`")
        self.assertNotIn("R003", self.codes())

    def test_relative_backticked_path_is_not_checked(self) -> None:
        self.edit("README.md", "`tools/check_refs.py`", "`../constitution/`")
        self.assertNotIn("R003", self.codes())

    def test_planned_file_is_allowed(self) -> None:
        self.edit("README.md", "`tools/check_refs.py`", "`tools/graph.py`")
        self.assertNotIn("R003", self.codes())

    def test_unknown_name_in_a_skill(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`fix-the-root`")
        self.assertIn("R004", self.codes())

    def test_names_from_the_glossary_are_known(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`needs-human` or `one-way`")
        self.assertNotIn("R004", self.codes())

    def test_language_rule_ids_are_known(self) -> None:
        table = "| Id | Rule | Check |\n|---|---|---|\n| `no-unknown-returns` | No `unknown` return. | lint |\n"
        self.write("skills/constitution/references/languages/typescript.md", table)
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`no-unknown-returns`")
        self.assertNotIn("R004", self.codes())
        self.edit("skills/ship/SKILL.md", "`no-unknown-returns`", "`no-unknown-return`")
        self.assertIn("R004", self.codes())

    def test_generated_skill_names_are_known(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`drive-<app>`")
        self.assertNotIn("R004", self.codes())

    def test_command_for_a_missing_skill(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`/deploy`")
        self.assertIn("R004", self.codes())

    def test_retired_skill_name(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`", "`probe`")
        self.assertIn("R005", self.codes())

    def test_code_blocks_are_skipped(self) -> None:
        self.edit("skills/ship/SKILL.md", "`fix-root-causes`.\n", "`fix-root-causes`.\n\n```\n[x](missing.md) `probe`\n```\n")
        self.assertEqual(self.codes(), [])

    def test_skill_missing_from_the_map(self) -> None:
        self.write("skills/README.md", "# Skills\n\n```mermaid\nflowchart TB\n  a[other]\n```\n")
        self.assertIn("R006", self.codes())
        self.write("skills/README.md", "# Skills\n\n```mermaid\nflowchart TB\n  s[\"ship\"]\n```\n")
        self.assertNotIn("R006", self.codes())

    def test_plugin_lists_exactly_the_skills(self) -> None:
        self.write(".claude-plugin/plugin.json", '{"name": "x", "skills": ["./skills/ship"]}')
        self.assertNotIn("R007", self.codes())
        self.write(".claude-plugin/plugin.json", '{"name": "x", "skills": []}')
        self.assertIn("R007", self.codes())
        self.write(".claude-plugin/plugin.json", '{"name": "x", "skills": ["./skills/ship", "./skills/gone"]}')
        self.assertIn("R007", self.codes())

    def test_invalid_plugin_json(self) -> None:
        self.write(".claude-plugin/plugin.json", '{"skills": [}')
        self.assertIn("R007", self.codes())

    def test_skill_missing_from_the_readme(self) -> None:
        self.write("skills/verify-pr/SKILL.md", "# Verify\n")
        self.assertIn("R008", self.codes())
        self.edit("README.md", "See [ship]", "See [verify-pr](skills/verify-pr/SKILL.md), [ship]")
        self.assertNotIn("R008", self.codes())

    def test_router_names_every_skill(self) -> None:
        self.write("skills/choose-skill/SKILL.md", "# Choose\n\n| a bug | `/ship <task>` |\n")
        self.assertNotIn("R009", self.codes())
        self.write("skills/choose-skill/SKILL.md", "# Choose\n\n| a bug | `/shipping` |\n")
        self.assertIn("R009", self.codes())

    def test_principle_without_its_full_form(self) -> None:
        (self.root / "skills/constitution/references/principles/fix-root-causes.md").unlink()
        self.assertIn("R010", self.codes())

    def test_full_form_without_its_row(self) -> None:
        self.write("skills/constitution/references/principles/old-name.md", "# old-name\n")
        self.assertIn("R010", self.codes())

    def test_guide_commands_name_skills(self) -> None:
        self.write("docs/guide.md", "# Guide\n\n```text\n/ship the export writes twice\n```\n\nSee `skills/ship/SKILL.md`, and run `/ship`.\n")
        self.assertNotIn("R011", self.codes())
        self.write("docs/guide.md", "# Guide\n\n```text\n/shipping the export writes twice\n```\n")
        self.assertIn("R011", self.codes())

    def test_exit_codes(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(check_refs.main(["--root", str(self.root)]), 0)
            self.edit("README.md", "skills/ship/SKILL.md", "skills/ship/MISSING.md")
            self.assertEqual(check_refs.main(["--root", str(self.root)]), 1)


class RealRepoTest(unittest.TestCase):
    def test_framework_references_resolve(self) -> None:
        findings = [f.render(REPO) for f in check_refs.check(REPO)]
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
