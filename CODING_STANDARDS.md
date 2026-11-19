# Coding standards

Judgment calls only: what `tools/check.py` already enforces is not repeated here. The verifier reads this file in its `standards` lane; a breach quoted with its rule and hunk is a should.

## Writing a skill

- **A step is one action and its completion criterion.** Detail that only some runs need goes to a reference, behind a pointer that says when to read it. Example: `skills/ship/SKILL.md:28` frames in one sentence and sends the detail to `references/frame.md`. Does not apply to a step whose detail every run needs.
- **A skill the user launches has a one-line description, written for the user.** It says what the skill produces; trigger lists belong to skills an agent picks on its own. Example: `skills/ship/SKILL.md:3`.
- **State the behavior you want.** A prohibition earns its place only as a hard guardrail, next to its positive. Example: `skills/verify-pr/SKILL.md:22`, "You read, run, and comment", instead of a list of what the verifier must not do.
- **One meaning, one home.** Link to the rule instead of restating it; a playbook names a principle by its id. Example: `skills/ship/references/playbooks/bug-fix.md:10` cites `fix-root-causes` instead of copying its rule.
- **A repeated idea becomes a glossary term** the model already knows, used as a single word. Example: `run`, in `skills/constitution/references/glossary.md:18`, replaced "the command, the observed output, and the expected output" in four files.
- **A skill reads the code before it asks the user.** Questions are for decisions and for facts no file or command can give. Example: `skills/setup-repo/SKILL.md:23`.

## Writing a tool

- **Every rule of a tool has a test that makes it fail.** A check never seen red proves nothing. Example: `tools/test_lint_skills.py:227` writes an external attribution into a skill and expects P005.
- **A tool's message says how to fix what it found**, so an agent reading only the message can act on it. Example: the `Fix:` part of every finding in `tools/check_refs.py`.

## Writing docs and ADRs

- **Every idea in a doc or an ADR names its source**, or says it is ours. In the skills, sources never appear; they live in `docs/sources.md`.
- **A doc is executed or dated.** A new doc either has a check that fails when it disagrees with the code, or is a dated record nobody rewrites. Example: `docs/adr/0013-a-doc-stays-fresh-by-running-or-by-date.md`.
- **An ADR records one decision that is hard to reverse, surprising without context, and a real trade-off.** It carries Status, Applies to, and Enforced by, and names the alternatives it rejected. Example: `docs/adr/0001-the-user-always-merges.md`.
