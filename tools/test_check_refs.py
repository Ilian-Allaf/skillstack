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

    def graph(self, *rows: str) -> None:
        table = "| Skill | What it does | Runs | Run by |\n|---|---|---|---|\n" + "".join(r + "\n" for r in rows)
        self.write("skills/GRAPH.md", "# The skill graph\n\n## Every skill, with its edges\n\n" + table)

    def test_skill_missing_from_the_graph(self) -> None:
        self.graph()
        self.assertIn("R006", self.codes())
        self.graph("| [ship](ship/SKILL.md) | One task to a PR | | |")
        self.assertNotIn("R006", self.codes())

    def test_graph_edges_match_the_frontmatter(self) -> None:
        self.write("skills/verify-pr/SKILL.md", '---\nname: verify-pr\nmetadata:\n  calls: "repo:drive-<app>"\n---\n\n# Verify\n')
        self.edit("skills/ship/SKILL.md", "# Ship\n", '---\nname: ship\nmetadata:\n  calls: "verify-pr, repo:drive-<app>"\n---\n\n# Ship\n')
        self.edit("README.md", "See [ship]", "See [verify-pr](skills/verify-pr/SKILL.md), [ship]")
        self.graph("| [ship](ship/SKILL.md) | One task | verify-pr, drive-\\<app\\> | |",
                   "| [verify-pr](verify-pr/SKILL.md) | A verdict | drive-\\<app\\> | ship |")
        self.assertEqual(self.codes(), [])
        self.graph("| [ship](ship/SKILL.md) | One task | drive-\\<app\\> | |",
                   "| [verify-pr](verify-pr/SKILL.md) | A verdict | | ship |")
        self.assertEqual(self.codes(), ["R012"])
        self.graph("| [ship](ship/SKILL.md) | One task | verify-pr | |",
                   "| [verify-pr](verify-pr/SKILL.md) | A verdict | | |")
        self.assertEqual(self.codes(), ["R012"])

    def test_removed_file_is_allowed_only_in_dated_docs(self) -> None:
        self.write("CHANGELOG.md", "- The map moved out of `skills/README.md`.\n")
        self.write("docs/adr/0001-x.md", "# 0001\n\nThe map lives in `skills/README.md`.\n")
        self.assertEqual(self.codes(), [])
        self.edit("README.md", "`tools/check_refs.py`", "`skills/README.md`")
        self.assertEqual(self.codes(), ["R003"])

    def test_link_from_the_top_of_skills_is_checked(self) -> None:
        self.write("skills/GRAPH.md", "# Graph\n\nRead [the map](README.md).\n\n| [ship](ship/SKILL.md) | x | | |\n")
        self.assertIn("R001", self.codes())

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
