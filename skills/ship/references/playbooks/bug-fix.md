# Playbook: bug fix

Proof duties for a bug. Each duty is met, or skipped with its reason written in the PR.

Every shipped line traces to runtime evidence. A guard that "might help" is a hypothesis, not a fix: it does not ship.

0. **Reproduce the reported symptom, before you frame.** Drive the symptom the user reported on the base with `drive-<app>`, or synthesize its trigger until it fires. Reading and driving only: no edit before the frame. `done_when` states the symptom as the user reported it. A symptom you cannot reproduce: run `investigate` in diagnosis mode, then go on when it finds a trigger that fires, or stop as `ship` says.
1. **A tight loop that goes red** (`build-a-tight-loop`). Build one command that fails on this exact bug: a failing test at the seam that reaches it, a curl script, a CLI call with a fixture, a browser script, a replayed trace. Make it fast and deterministic: pin time, seed randomness, isolate files. For a flaky bug, loop the trigger until the failure rate is high enough to debug. With no loop, stop as `ship` does for a symptom that does not reproduce, and list what you tried.
2. **Find the cause by elimination.** List the candidate mechanisms, and rule them out with runtime evidence, each pass taking the split that removes the most. Confirm the surviving mechanism before you fix it; it becomes one case of the list, not the bar.
3. **The repro lands first.** Commit the failing test or script before the fix, so the history shows it red.
4. **Fix the root cause** (`fix-root-causes`).
5. **Green on the head, red on the base.** The PR shows both runs of the same command.
6. **Look for siblings.** Search for the same pattern elsewhere. Fix siblings in the task's scope; open issues for the others and link them.
7. **Prove on the app.** When the bug was user-visible, reproduce it on the base and show it gone on the head with `drive-<app>`.

The verifier checks that the repro commit comes before the fix in the history, runs it red on the base and green on the head, and searches for siblings the PR missed.
