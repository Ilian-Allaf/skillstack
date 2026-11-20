# Audit mode

Measure what the code already enforces, before agents work on it at scale. Change nothing. The output is a report and a list of proposed corrections for the user to pick from.

## Steps

1. **Static checks.** Find the type checker, the linters, and the formatter, and how strict each is. Run them on the base.
   Done when: each tool is listed with its command, its strictness settings, and its error count on the base.

2. **Tests.** Find the test commands and run them. Note what they cover: units, integration, end to end. Note flaky tests.
   Done when: each suite is listed with its command, its duration, and its pass or fail count.

3. **CI.** Read the workflows. Note which checks run on a PR and which are required.
   Done when: the report says which local checks also run in CI and which do not.

4. **Boundaries.** Look for module boundaries the code relies on but nothing enforces: imports across layers, shared mutable state, duplicated sources of truth.
   Done when: each boundary is listed with one `file:line` that crosses it, or "none found".

5. **Mistake classes.** Read recent commits, reverts, and review comments. Group repeated mistakes into classes.
   Done when: each class has two cited examples, or the report says none repeated.

6. **Verification.** Check whether the repo has a `drive-<app>` skill and a feature map.
   Done when: the report says yes with its path, or no.

7. **Report.** Write the findings as a table, then propose the corrections in order of value: the most frequent class at the highest level first.
   Done when: the user has the report and a ranked list of proposed corrections.
