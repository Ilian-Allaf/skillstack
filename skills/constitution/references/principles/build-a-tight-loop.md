# build-a-tight-loop

**Apply when** you start a bug fix or a feature, before you change product code.

**Rule.** First build one command that goes red on this exact problem, then make it fast and deterministic. Every later attempt is judged by it.

## How

- Pick the narrowest command that reaches the problem: a failing test at the seam, a curl script, a CLI call with a fixture, a browser script, a replayed trace.
- Make it fast and deterministic: pin time, seed randomness, isolate files and ports.
- For a flaky problem, loop the trigger until the failure rate is high enough to debug.
- Watch it fail for the intended reason before you change code. A command that fails for another reason is fixed first.
- With no loop, stop and ask for access or an artifact instead of guessing.

## Test

One command, run on the base, shows the problem; the same command on the head shows it gone.

## Sign it was skipped

A fix verified only by reading the code. A test written after the fix that nobody saw fail.
