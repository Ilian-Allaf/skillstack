# Calibration

Examples of verdicts the user has ruled on. Read them before grading. They show where the line between FAIL and note sits in practice.

**Status: empty.** Real examples come from the testbed repo: verdicts the user agreed or disagreed with, and defects seeded into real PRs. Until then, [verdict.md](verdict.md) defines a FAIL, and these two rulings of the user show where its line falls.

1. **An observed defect stays a FAIL unless `done_when` excludes it.** "It is a small edge case" is not an exclusion.
2. **A finding without a run is a note, however likely it looks.** "This might race" is a note; a script that makes it race is a FAIL.

## Format of an example

```text
### <short title>
PR: <link>   class: <low | medium | high>
finding: <what the verifier saw, with the run>
verifier said: <FAIL | note>
user ruled: <FAIL | note>, because <reason>
lesson: <one sentence the next verifier applies>
```

Add an example each time the user overrules a verdict, each time a seeded defect slips through, and each time `learn-from-mistakes` traces an escaped bug to the verifier. A change made for such an example counts only once a fresh verifier, run on that PR's head, gives the FAIL it missed; the case then joins `evals/verdicts/`. A check never seen failing proves nothing. Keep at most twenty; when a lesson becomes a rule above, delete its examples.
