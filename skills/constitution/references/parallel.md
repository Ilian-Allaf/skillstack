# Parallel subagents

Two shapes for running several subagents on one job. Skills name the shape; this file owns how it runs.

| Shape | Use when | Returns |
|---|---|---|
| **arena** | one artifact, several valid shapes: a design sketch, a hard function, a prompt | one synthesized artifact |
| **swarm** | many slices of one job, or a race on one brief: drive every feature, try every attack, measure every commit | one consolidated report |

## Rules for both

- **The brief is the contract.** Each brief stands alone: the goal, the scope or slice, how to verify, and what to report. File paths, not pasted context.
- **One writable place per subagent.** Its own worktree, branch, or output file. Never two writers on one file.
- **Families mixed when available.** Runners from different model families catch different things. When only one family runs, say so in the result.
- **A dropout is a gap, not a pass.** Proceed without it, respawn it once, and report it.
- **Read the artifacts, not the summaries.** A subagent's report is a claim until you open what it produced.

## Arena

1. **Frame.** Name the artifact. Write 3 to 6 criteria that grade it on this task; runners never see them.
2. **Fan out.** Spawn 2 or 3 runners on the same brief, from different families when the harness offers them.
3. **Cross-judge.** When a family other than yours is available, spawn one judge from it with the criteria and the candidates, labeled by path only. It scores each criterion and recommends a base.
4. **Pick a base.** Read every candidate end to end and score it criterion by criterion. Agreement with the judge confirms the pick; disagreement means a bias or a vague criterion, so read both reasons. When tied, take the smaller interface.
5. **Graft.** Walk each losing candidate once for one or two parts worth porting, and fold them in by hand so the result keeps one design. Candidates that converge need no graft. Candidates that diverge wildly mean the frame was vague: reframe and rerun, never average.
6. **Verify.** Check the synthesized artifact like any other output.

Output: the artifact and a short note naming the base and why, the judge's verdict, each graft and its source, and what was rejected.

## Swarm

1. **Frame.** State the done condition and the report shape. Choose the shape: slices (each worker gets one part), a race (N workers on one brief), or both. For a race, declare the rule before spawning: first pass, rank all, or best of.
2. **Fan out.** Spawn every worker in one message. A brief that verifies or measures commits names the exact SHAs and the method.
3. **Aggregate.** Each worker reports `PASS`, `ISSUES`, or `BLOCKED` with evidence, and lists every issue it can prove, not only the first. Drop a result that skips the SHAs or the method its brief named, and respawn once. Every slice needs a result.
4. **Report.** One table of results, one line per issue, and the gaps.
