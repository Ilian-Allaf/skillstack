# Playbook: perf

Proof duties for a performance task. Every fix is tied to a measurement; reading the source is not measuring. Each duty is met, or skipped with its reason written in the PR.

`done_when` is a number on a named path: "p50 of export on the 60k-row fixture under 40 ms". It is red on the base. Write the claim you expect to ship before you measure, in the words you would ship it.

1. **A vetted baseline.** Measure the base on the path a user waits on, with realistic data. Before you trust the number, answer the checks below with runs, not with reasoning about the code.
2. **Find the limiter.** Profile in a run you do not report, since profilers slow the work down. Map the hot spot to source. Never claim a ceiling you did not run.
3. **Cheapest fix first.** Try in this order, and stop at the first that meets `done_when`: don't do it; do it once, not again; do it less; do it later; do it when the user is not waiting; do it concurrently; do it cheaper. When the fix crosses a boundary, sketch it first, as [design.md](../design.md) describes.
4. **One attempt at a time.** Measure after each attempt before the next one.
5. **Compare like with like.** Measure the head with the same script, data, machine, and settings as the base. An inconclusive run, or a run on another path, is not a pass.
6. **Cite the measurement.** The PR gives one primary number: base, head, delta, unit, run count, and range. The runs and the profile go in the evidence, with the command that replays them.

## Checks for every number (`explain-the-number`)

| Check | Question |
|---|---|
| limiter | What stops it from going twice as fast? A change that did not move the number is explained by the limiter. |
| tuned | Did both sides run as production runs: release build, production flags, same data and versions? |
| limits | Is the result possible given disk, network, and core counts? Removing 10% of the work saves at most about 11%. |
| errors | Were failures counted, and outputs checked as correct, not just present? Rejections are fast. |
| repeats | At least 5 runs per side, alternated, with median and range. A gap smaller than the spread is no difference. |
| matters | What share of the end-to-end path does the measured piece take? |
| happened | Did the work run inside the timed region: rows written, promises awaited, results used? |

A number that fails `errors` or `happened`, or whose limiter is unknown, is inconclusive. Say so.

The verifier replays the measurement on the head and checks the table above.
