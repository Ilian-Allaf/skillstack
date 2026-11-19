# Verdict cases

Cases the verifier must catch: bugs it once passed, and defects seeded into real PRs. Each one proves that the verifier can fail, which nothing else in the framework shows. The user replays the list when they choose, for example after a change to `verify-pr`; nothing runs it on a schedule.

One file per case, `<slug>.md`:

```text
# <short title>
repo: <owner/name>   PR: <link>   head: <sha>
bug: <what goes wrong, from the user's side>
run: <the command or journey that shows it>
expected verdict: FAIL on <axis>, lane <lane>
origin: escaped (issue <link>) | seeded
added after: <the change to verify that made it catch the bug, with its PR>
```

A replay spawns a fresh verifier on each case's head with the normal brief from `skills/verify-pr/SKILL.md` step 1, and counts the cases where it gave the expected FAIL.
