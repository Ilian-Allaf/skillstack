# Verdict

The one place that defines a FAIL. Every other file points here.

## What makes a FAIL

A finding is a FAIL when all three hold:

1. **It is proven.** It comes with its run on the head of the PR, and you reran that command yourself and saw the same output. A breach of a documented repo standard (`coding-standards.md` in the project folder, the agent file, the repo's glossary, or an accepted ADR whose Applies to covers the hunk) is proven instead by quoting the file, the rule, and the hunk. A PR that changes such an ADR on purpose carries the ADR that supersedes it. A breach of a technical decision the spec holds is proven the same way, by quoting the decision and the hunk, whether or not Deviations names it: a replaced decision has left the spec.
2. **It is in the task's scope**: it breaks the task or `done_when`, or the diff itself breaks a documented standard or a technical decision of the spec. A finding outside the task's scope is a note, however real.
3. **Its grade is blocker or should**, in the table below.

A defect you observed stays a FAIL unless `done_when` excludes it: keep it, whatever reason to wave it off comes to mind. Anything not proven is a note, however likely it looks.

## Grades

| Grade | Meaning | Effect |
|---|---|---|
| blocker | breaks `done_when`, loses or corrupts data, opens a security hole, or breaks a feature that worked on the base | FAIL |
| should | a real bug in the task's own scope that a user will hit; a row of the coverage table whose evidence is missing or does not show its case; a breach of a documented repo standard, or of a technical decision the spec holds | FAIL |
| nit | a real but minor issue, or a judgment call | note |
| coverage gap | a case missing from the coverage table that behaves correctly when driven | the builder adds it with the verifier's evidence before `ready`; not a FAIL |

## Outcomes per axis

- **PASS**: every lane of the axis ran and none produced a FAIL. Notes are allowed; PASS with notes is a PASS.
- **FAIL**: at least one FAIL.
- **INCONCLUSIVE**: a lane could not run, for a reason outside the PR: no driver for a touched surface, the app would not start on the base, a missing credential. Say what would make it runnable.

The PR is verified when both axes are PASS.

## Verdict validity

A verdict covers the exact base and head commits checked. Record their full SHAs from the code host: the base-sha field is the current tip of the PR's target branch, not the merge base; the sha field is the PR head checked out for the runs. Compute the patch id with `git diff <base-sha>...<head-sha> | git patch-id --stable`. The patch id describes the diff, not the code it runs with.

Reuse a linked verdict only while both SHAs still match the PR. A changed base or head needs a new verdict, including a conflict-free rebase, a commit with the same tree, or a target-branch update with no push to the PR. A missing SHA makes an older verdict historical too. Remove `ready`, refresh the proof on the current head against the current base, and run the selected lanes again before linking the new verdict. Keep the old comment as evidence of the old version. An unchanged pair allows reuse only while the recorded rules and environment still apply.

Record the rule files and revisions used, and the runtime, dependency setup, driver, and service configuration needed to replay the runs. For private files outside git, record a content hash and a safe location. Keep credentials out of the comment. This records what the verifier used; review of proposed rule changes is still the `standards` lane's job.

Before posting, fetch the PR's base and head again. If either moved during verification, keep the result historical and verify the new pair. The verdict comment and existing CI artifacts hold this record; no database or committed per-run file is required.

## Comment format

Post exactly this shape, so the builder and the user can read it at a glance and a script can parse its first lines.

```text
verdict: PASS | FAIL | INCONCLUSIVE   sha=<full head SHA>   base-sha=<full base SHA>   patch-id=<full stable patch id>
behavior: <outcome> (<lanes run>)   code: <outcome> (<lanes run>)
verifier: <model family>, fresh context: yes | no (<what leaked>)
rules: <paths and revisions, or content hashes for private files>
environment: <runtime, dependency setup, driver, services, and replay instructions or artifact link>

FAIL 1 (blocker | should): <title>
  run:      <command>
  observed: <output, trimmed to the lines that show the failure>
  expected: <what the task or done_when requires>

coverage gap: <case> (<evidence>)
note: <title> (<where, and why it does not block>)
skipped: <lane> (<reason>)
```
