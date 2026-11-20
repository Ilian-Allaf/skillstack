# explain-the-number

**Apply when** you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a latency, a throughput, an eval result.

**Rule.** Say what produced the number, what limits it, and what would make it wrong, before anyone uses it.

## How

- Before the run, write the result that would change a decision, and the noise floor. Stop when the run-to-run spread is larger than the effect.
- Ask "why not twice as good?" Name the resource or code path that bounds the result: a core, a lock, the disk, the network, the load generator. Get it from a profile or system counters taken during a run, then map it to source. A guess from reading the code is not a limiter.
- List what else the number could be measuring, and rule out each one with evidence: errors, skipped or cached work, code that never ran, an untuned side, noise, a piece too small to matter end to end.
- Keep the run count, the spread, and the limiter with the number.

For a performance number, the full checks are in the `perf` playbook.

## Test

You can say why the number is not twice as good, and the evidence holds a run count and a spread.

## Sign it was skipped

A single run. A time saved larger than the time the changed piece took. A speedup on a path that returned errors.
