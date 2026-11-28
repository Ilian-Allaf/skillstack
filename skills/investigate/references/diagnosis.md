# Mode: diagnosis

For a runtime symptom whose cause is unknown: a spinning process, a leak, a hang, a visual glitch, a slow path. The deliverable is a cited diagnosis, not a fix.

Instrument the running process or read the capture; never theorize from source alone.

## Duties

1. **Get the artifact.** If the user gave a capture (a CPU profile, a trace, a heap snapshot, a spindump), it is a fixed dataset: read it, do not rerun it. Otherwise capture the live signal on the running app with the repo's `drive-<app>`, adding its Profile line first when it has none: a CPU profile for a spinning process, a heap snapshot for a leak, a browser trace for a glitch.
2. **Make it queryable.** Load the artifact with the right parser and dump it into a form you can query, such as one SQLite row per sample, frame, or node. Parse large artifacts in a subagent and keep only the reduced finding.
3. **Narrow to the cause.** The frames that hold the most time and their call tree; for a leak, the retainer chain from the leaked object to a root; for a hang, the stuck thread and its wait reason.
4. **Prove the mechanism.** On a live process, confirm the hypothesis cheaply: inject a log or a counter, or patch the running code in a scratch checkout. On a capture alone, diff it with a paired before-and-after capture. Without either, call the finding the strongest hypothesis the artifact supports, not a cause.
5. **Map it to source.** File, symbol, and the line that allocates, schedules, or blocks. A frame with no source mapping is not yet a diagnosis.

## Shape of the answer

The artifact and its path, the reduced finding, how the mechanism was proven and at which certainty level, and the source location. The proposed task names the `bug-fix` or `perf` playbook of `ship`.
