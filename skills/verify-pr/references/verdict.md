# Verdict

The one place that defines a FAIL. Every other file points here.

## What makes a FAIL

A finding is a FAIL when all three hold:

1. **It is proven.** It comes with its run on the head of the PR, and you reran that command yourself and saw the same output. A breach of a documented repo standard (`coding-standards.md` in the project folder, the agent file, the repo's glossary, or an accepted ADR whose Applies to covers the hunk) is proven instead by quoting the file, the rule, and the hunk. A PR that changes such a decision on purpose carries the ADR that supersedes it.
2. **It is in the task's scope**: it breaks the task or `done_when`, or the diff itself breaks a documented standard. A finding outside the task's scope is a note, however real.
3. **Its grade is blocker or should**, in the table below.

A defect you observed stays a FAIL unless `done_when` excludes it: keep it, whatever reason to wave it off comes to mind. Anything not proven is a note, however likely it looks.

## Grades

| Grade | Meaning | Effect |
|---|---|---|
| blocker | breaks `done_when`, loses or corrupts data, opens a security hole, or breaks a feature that worked on the base | FAIL |
| should | a real bug in the task's own scope that a user will hit; a row of the coverage table whose evidence is missing or does not show its case; a breach of a documented repo standard | FAIL |
| nit | a real but minor issue, or a judgment call | note |
| coverage gap | a case missing from the coverage table that behaves correctly when driven | the builder adds it with the verifier's evidence before `ready`; not a FAIL |

## Outcomes per axis

- **PASS**: every lane of the axis ran and none produced a FAIL. Notes are allowed; PASS with notes is a PASS.
- **FAIL**: at least one FAIL.
- **INCONCLUSIVE**: a lane could not run, for a reason outside the PR: no driver for a touched surface, the app would not start on the base, a missing credential. Say what would make it runnable.

The PR is verified when both axes are PASS.

## The patch id

A verdict covers one patch id: `git diff <base>...<head> | git patch-id --stable`. A new push with the same patch id, such as a pure rebase, keeps the verdict. A different patch id needs a new one.

## Comment format

Post exactly this shape, so the builder and the user can read it at a glance and a script can parse its first lines.

```text
verdict: PASS | FAIL | INCONCLUSIVE   sha=<head sha, 7 chars>   patch-id=<7 chars>
behavior: <outcome> (<lanes run>)   code: <outcome> (<lanes run>)
verifier: <model family>, fresh context: yes | no (<what leaked>)

FAIL 1 (blocker | should): <title>
  run:      <command>
  observed: <output, trimmed to the lines that show the failure>
  expected: <what the task or done_when requires>

coverage gap: <case> (<evidence>)
note: <title> (<where, and why it does not block>)
skipped: <lane> (<reason>)
```
