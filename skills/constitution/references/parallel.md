# Parallel subagents

How to run several subagents on one job: a swarm, for many slices of one job or a race on one brief, such as driving every feature, trying every attack, or measuring every commit. It returns one consolidated report. One artifact with several valid shapes, such as a design, is not a swarm: the builder sketches it twice itself, as `constitution/references/architecture.md` describes.

## Rules

- **The brief is the contract.** Each brief stands alone: the goal, the scope or slice, how to verify, and what to report. File paths, not pasted context.
- **One writable place per subagent.** Its own worktree, branch, or output file. Never two writers on one file.
- **Families mixed when available.** Runners from different model families catch different things. When only one family runs, say so in the result.
- **A dropout is a gap, not a pass.** Proceed without it, respawn it once, and report it.
- **Read the artifacts, not the summaries.** A subagent's report is a claim until you open what it produced.

## Swarm

1. **Frame.** State the done condition and the report shape. Choose the shape: slices (each worker gets one part), a race (N workers on one brief), or both. For a race, declare the rule before spawning: first pass, rank all, or best of.
2. **Fan out.** Spawn every worker in one message. A brief that verifies or measures commits names the exact SHAs and the method.
3. **Aggregate.** Each worker reports `PASS`, `ISSUES`, or `BLOCKED` with evidence, and lists every issue it can prove, not only the first. Drop a result that skips the SHAs or the method its brief named, and respawn once. Every slice needs a result.
4. **Report.** One table of results, one line per issue, and the gaps.
