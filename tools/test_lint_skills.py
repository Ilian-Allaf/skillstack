"""Tests for lint_skills.py. Run: python -I -m unittest discover -s tools -v"""

from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lint_skills  # noqa: E402

REPO = Path(__file__).resolve().parent.parent

GLOSSARY = """\
# Glossary

| Term | Meaning | Avoid |
|---|---|---|
| verifier | the fresh agent | `QA agent` |
| ready | needs only the merge | `merge-ready` |
"""

GOOD_ENTRY = """\
---
name: ship
description: "Turns a task into a ready PR."
disable-model-invocation: true
metadata:
  kind: entry
  calls: "probe, repo:verify-<app>"
  hypothesis: "Without a fixed path, the model skips proof."
---

# Ship

## Steps

1. Frame the task. Done when: the user said go.
2. Build it, then run [probe](../probe/SKILL.md).
   Done when: `done_when` is green.
"""

CODEX_POLICY = """interface:
  display_name: "{name}"
  short_description: "A skill."
policy:
  allow_implicit_invocation: false
"""

GOOD_PROBE = """\
---
name: probe
description: "Finds what a change breaks elsewhere."
disable-model-invocation: true
metadata:
  kind: spine
  hypothesis: "The builder checks the diff, not its callers."
---

## Steps

1. Find the safety fact. Done when: it ran at level 4.
"""


class LintTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("skills/constitution/README.md", "# Constitution\n\nRead [the glossary](references/glossary.md).\n")
        self.write("skills/constitution/references/glossary.md", GLOSSARY)
        self.write("skills/ship/SKILL.md", GOOD_ENTRY)
        self.write("skills/probe/SKILL.md", GOOD_PROBE)
        for name in ("ship", "probe"):
            self.write(f"skills/{name}/agents/openai.yaml", CODEX_POLICY.format(name=name))

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> Path:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(textwrap.dedent(text), encoding="utf-8")
        return path

    def codes(self, level: str = "error") -> list[str]:
        return [f.code for f in lint_skills.lint(self.root) if f.level == level]

    def edit(self, rel: str, old: str, new: str) -> None:
        path = self.root / rel
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text, "test setup: text to replace is missing")
        path.write_text(text.replace(old, new), encoding="utf-8")

    # A clean tree passes; this guards every other test against false positives.
    def test_clean_tree_has_no_findings(self) -> None:
        self.assertEqual(lint_skills.lint(self.root), [])

    def test_missing_frontmatter(self) -> None:
        self.write("skills/probe/SKILL.md", "# Probe\n")
        self.assertIn("F001", self.codes())

    def test_unclosed_frontmatter(self) -> None:
        self.write("skills/probe/SKILL.md", "---\nname: probe\n")
        self.assertIn("F001", self.codes())

    def test_unknown_top_level_key(self) -> None:
        self.edit("skills/probe/SKILL.md", "name: probe", "name: probe\nkind: spine")
        self.assertIn("F003", self.codes())

    def test_name_must_match_folder(self) -> None:
        self.edit("skills/probe/SKILL.md", "name: probe", "name: prober")
        self.assertIn("F005", self.codes())

    def test_description_required(self) -> None:
        self.edit("skills/probe/SKILL.md", 'description: "Finds what a change breaks elsewhere."\n', "")
        self.assertIn("F007", self.codes())

    def test_description_length(self) -> None:
        self.edit("skills/probe/SKILL.md", "Finds what a change breaks elsewhere.", "x" * 1100)
        self.assertIn("F008", self.codes())

    def test_description_names_other_skill(self) -> None:
        self.edit("skills/probe/SKILL.md", "Finds what a change breaks elsewhere.", "Called by ship to find breakage.")
        self.assertIn("F009", self.codes())

    def test_description_word_inside_other_word_is_fine(self) -> None:
        self.edit("skills/probe/SKILL.md", "Finds what a change breaks elsewhere.", "Finds breakage in shipping code.")
        self.assertNotIn("F009", self.codes())

    def test_invocation_flag_required(self) -> None:
        self.edit("skills/probe/SKILL.md", "disable-model-invocation: true\n", "")
        self.assertIn("F010", self.codes())

    def test_model_invocation_must_be_disabled(self) -> None:
        self.edit("skills/probe/SKILL.md", "disable-model-invocation: true", "disable-model-invocation: false")
        self.assertIn("F017", self.codes())

    def test_codex_policy_file_required(self) -> None:
        (self.root / "skills/probe/agents/openai.yaml").unlink()
        self.assertIn("F018", self.codes())

    def test_codex_policy_must_keep_the_skill_for_the_user(self) -> None:
        self.edit("skills/probe/agents/openai.yaml", "allow_implicit_invocation: false", "allow_implicit_invocation: true")
        self.assertIn("F018", self.codes())

    def test_codex_picker_fields_required(self) -> None:
        self.edit("skills/probe/agents/openai.yaml", '  short_description: "A skill."\n', "")
        self.assertIn("F018", self.codes())

    def test_unknown_kind(self) -> None:
        self.edit("skills/probe/SKILL.md", "kind: spine", "kind: helper")
        self.assertIn("F011", self.codes())

    def test_hypothesis_required(self) -> None:
        self.edit("skills/probe/SKILL.md", '  hypothesis: "The builder checks the diff, not its callers."\n', "")
        self.assertIn("F012", self.codes())

    def test_calls_must_exist(self) -> None:
        self.edit("skills/ship/SKILL.md", "probe, repo:verify-<app>", "probe, verify")
        self.assertIn("F013", self.codes())

    def test_call_must_be_linked_by_path(self) -> None:
        self.edit("skills/ship/SKILL.md", "[probe](../probe/SKILL.md)", "the `probe` skill")
        self.assertIn("F015", self.codes())

    def test_link_to_a_skill_needs_a_call(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Hand back to [ship](../ship/SKILL.md).")
        self.assertIn("F014", self.codes())

    def test_link_to_skill_files_needs_reads(self) -> None:
        self.write("skills/ship/references/frame.md", "# Frame\n")
        self.edit("skills/ship/SKILL.md", "Frame the task.", "Frame the task per [frame](references/frame.md).")
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Read [frame](../ship/references/frame.md).")
        self.assertIn("F014", self.codes())
        self.edit("skills/probe/SKILL.md", "kind: spine", 'kind: spine\n  reads: "ship"')
        self.assertNotIn("F014", self.codes())

    def test_reads_must_exist(self) -> None:
        self.edit("skills/probe/SKILL.md", "kind: spine", 'kind: spine\n  reads: "nowhere"')
        self.assertIn("F013", self.codes())

    def test_repo_call_accepts_placeholders(self) -> None:
        self.edit("skills/ship/SKILL.md", "probe, repo:verify-<app>", "probe, repo:verify-<app>, repo:verify-<area>-formal")
        self.assertNotIn("F013", self.codes())
        self.edit("skills/ship/SKILL.md", "repo:verify-<area>-formal", "repo:Verify_Formal")
        self.assertIn("F013", self.codes())

    def test_steps_section_required_for_non_reference(self) -> None:
        self.edit("skills/probe/SKILL.md", "## Steps", "## Method")
        self.assertIn("S001", self.codes())

    def test_step_without_completion_criterion(self) -> None:
        self.edit("skills/ship/SKILL.md", "Frame the task. Done when: the user said go.", "Frame the task.")
        self.assertIn("S003", self.codes())

    def test_criterion_on_continuation_line_counts(self) -> None:
        # Step 2 of GOOD_ENTRY puts "Done when" on its second line.
        self.assertNotIn("S003", self.codes())

    def test_reference_skill_needs_no_steps(self) -> None:
        self.write("skills/rules/SKILL.md", '---\nname: rules\ndescription: "Rules."\ndisable-model-invocation: true\nmetadata:\n  kind: reference\n  hypothesis: "Shared."\n---\n\n# Rules\n')
        self.assertNotIn("S001", self.codes())

    def test_shared_folder_needs_no_frontmatter(self) -> None:
        self.assertNotIn("F000", self.codes())

    def test_shared_folder_with_frontmatter_is_flagged(self) -> None:
        self.write("skills/constitution/README.md", "---\nname: constitution\n---\n\nRead [the glossary](references/glossary.md).\n")
        self.assertIn("F016", self.codes())

    def test_shared_folder_is_not_callable(self) -> None:
        self.edit("skills/ship/SKILL.md", "probe, repo:verify-<app>", "probe, constitution, repo:verify-<app>")
        self.assertIn("F013", self.codes())

    def test_broken_link(self) -> None:
        self.edit("skills/constitution/README.md", "references/glossary.md", "references/missing.md")
        self.assertIn("L001", self.codes())

    def test_orphan_reference(self) -> None:
        self.write("skills/constitution/references/unused.md", "# Unused\n")
        self.assertIn("L002", self.codes())

    def test_banned_word(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Leverage the safety fact.")
        self.assertIn("P001", self.codes())

    def test_avoid_term_from_glossary(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Ask the QA agent.")
        self.assertIn("P002", self.codes())

    def test_avoid_term_allowed_in_glossary_itself(self) -> None:
        self.assertNotIn("P002", self.codes())

    def test_code_is_skipped_for_words(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Run `leverage --merge-ready`.\n\n```\nQA agent\n```\n")
        self.assertNotIn("P001", self.codes())
        self.assertNotIn("P002", self.codes())

    def test_em_dash(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Find the fact — then prove it.")
        self.assertIn("P003", self.codes())

    def test_curly_quote(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Find the “safety” fact.")
        self.assertIn("P004", self.codes())

    def test_external_attribution(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Find the safety fact. Source: pstack `blast-radius`.")
        self.assertIn("P005", self.codes())

    def test_external_skill_name_in_code_is_caught(self) -> None:
        self.edit("skills/probe/SKILL.md", "Find the safety fact.", "Run it like Matt Pocock `grilling` does.")
        self.assertIn("P005", self.codes())

    def test_principle_budget_is_a_warning(self) -> None:
        self.write("skills/constitution/references/principles/probe-rule.md", "# probe-rule\n\n" + "word " * 400)
        self.edit("skills/constitution/README.md", "Read [the glossary]", "See [probe-rule](references/principles/probe-rule.md). Read [the glossary]")
        self.assertNotIn("W002", self.codes("warning"))
        self.write("skills/constitution/references/principles/probe-rule.md", "# probe-rule\n\n" + "word " * 600)
        self.assertIn("W002", self.codes("warning"))
        self.assertEqual(self.codes(), [])

    def test_word_budget_is_a_warning(self) -> None:
        self.edit("skills/probe/SKILL.md", "## Steps", "word " * 900 + "\n\n## Steps")
        self.assertIn("W001", self.codes("warning"))
        self.assertEqual(self.codes(), [])

    def test_exit_codes(self) -> None:
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(lint_skills.main(["--root", str(self.root)]), 0)
            self.write("skills/broken/SKILL.md", "# no frontmatter\n")
            self.assertEqual(lint_skills.main(["--root", str(self.root)]), 1)


class RealRepoTest(unittest.TestCase):
    def test_framework_skills_pass(self) -> None:
        errors = [f.render(REPO) for f in lint_skills.lint(REPO) if f.level == "error"]
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
