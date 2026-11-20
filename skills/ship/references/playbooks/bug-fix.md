# Playbook: bug fix

Proof duties for a bug. Each duty is met, or skipped with its reason written in the PR.

Every shipped line traces to runtime evidence. A guard that "might help" is a hypothesis, not a fix: it does not ship.

0. **Reproduce the reported symptom, before the go.** Drive the symptom the user reported on the base with `drive-<app>`, or synthesize its trigger until it fires. Then find the cause by elimination: list the candidate mechanisms, and rule them out with runtime evidence, each pass taking the split that removes the most. Confirm the surviving mechanism before you frame. `done_when` states the symptom as the user reported it; the mechanism you found is one case of the list, not the bar. A symptom you cannot reproduce goes to `investigate` in diagnosis mode.
1. **A tight loop that goes red** (`build-a-tight-loop`). Build one command that fails on this exact bug: a failing test at the seam that reaches it, a curl script, a CLI call with a fixture, a browser script, a replayed trace. Make it fast and deterministic: pin time, seed randomness, isolate files. For a flaky bug, loop the trigger until the failure rate is high enough to debug. With no loop, stop and list what you tried.
2. **The repro lands first.** Commit the failing test or script before the fix, so the history shows it red.
3. **Fix the root cause** (`fix-root-causes`).
4. **Green on the head, red on the base.** The PR shows both runs of the same command.
5. **Look for siblings.** Search for the same pattern elsewhere. Fix siblings in the task's scope; open issues for the others and link them.
6. **Prove on the app.** When the bug was user-visible, reproduce it on the base and show it gone on the head with `drive-<app>`.

The verifier checks that the repro commit comes before the fix in the history, runs it red on the base and green on the head, and searches for siblings the PR missed.
