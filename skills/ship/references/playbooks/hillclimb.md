# Playbook: hillclimb

Proof duties for a sustained improvement of one metric against a target: one change, one measurement, keep or revert, again and again. A one-off slowness is the `perf` playbook. Each duty is met, or skipped with its reason written in the PR.

`done_when` pairs a target with a floor on attempts, so a lucky early win cannot end the run: "p50 of export on the 60k-row fixture at least 40% under the base, after at least 10 attempts". It is red on the base.

1. **Reproduce the complaint before choosing the metric.** Trace the target, and name the dimensions of a realistic workload that move the result: data size, history, state, concurrency. Pick a case that shows what the user reported. If no case shows it, fix the repro first.
2. **Build the harness, prove it, then freeze it** (`build-the-lever`, `explain-the-number`). Run contrasting workloads: the target case shows the symptom, easier cases separate as expected. The harness prints its error count and a count of the work done, and one command emits the metric as a median over enough runs to clear the noise. Record the base metric and a green run of the regression gate, the tests that must keep passing, before any change. Once frozen, the harness does not change.
3. **Keep the decision log** (see [decision-log.md](../../../constitution/references/decision-log.md)): one row per attempt with the hypothesis, the change, before, after, the gate, and kept or reverted. Read it before each attempt.
4. **Ground each hypothesis in a mechanism**: "defer X off the startup path because it blocks the first paint", not "try caching something". For speed, order hypotheses as the cheapest-fix list of the `perf` playbook does.
5. **One attempt at a time.** Make the change, measure with the frozen harness, run the gate. Keep it only when the metric moves past the noise and the gate stays green; otherwise revert it in full. One commit per kept change, staging only the files it touched. Never stack untested changes, and never claim a win from reading the code. Independent hypotheses may run in parallel, each in its own worktree.
6. **Push past the first plateau.** After several reverts in a row, change the category of hypothesis, combine near misses, reread the source, or try something more radical. Correctness and simplicity outrank the number: revert a win that breaks behavior, and keep a simplification that holds the number (`make-the-smallest-change`).
7. **Stop at the target, or when what is left is marginal.** Never relax `done_when` to meet it, and do not stop while cheap untried hypotheses remain.

The PR stacks the kept commits in the order they landed, and gives one primary number: base, head, delta, unit, run count, and range, with the log path and the best next idea.

The verifier replays the frozen harness on the base and the head, and checks that each kept commit moved the metric past the noise in the log.
