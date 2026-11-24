# 0019. The spec sets the bar, and a task builds the proof it lacks

- **Status**: proposed, 2026-11-24. Once accepted, it supersedes two clauses of [0017](0017-a-formal-check-guards-every-task-that-touches-its-code.md), "The maintain pass stays outside the task" and "A check stale on the base is not updated by the task", and adds one stop to the list in [0014](0014-a-launched-task-runs-to-a-ready-pr.md) and rule 11 of the constitution: access only the user can give. The rest of both ADRs stands.
- **Applies to**: `skills/shape-spec/`, `skills/ship/` (frame, verification setup, the units of a task, `scripts/check_evidence.py`), `skills/verify-pr/` (the brief, `live`, `breakage`, `spec`), `skills/create-app-driver/`, `skills/constitution/README.md` (rule 11), `skills/constitution/references/proof.md`, `coverage.md`, `formal.md` (In a task), `glossary.md`
- **Enforced by**: `check_evidence.py` fails when a story or a promise of the spec has no case in the evidence record, with a test in `tools/test_check_evidence.py`. The rest by three blind `test-skill-change` runs and by review.

## Context

The verification of a task is decided by its builder. `shape-spec` writes one global `done_when` and user stories with no observable result. `ship`'s frame turns them into cases and picks the evidence per case, and the verifier's brief is that frame, not the spec. A formal check is used only when it already exists. A missing driver is found in the frame, yet the task goes on and ends `needs-human` because `live` is INCONCLUSIVE, while `ship`'s verification setup already says to prepare the driver first. A check stale on the base leaves its hard zone under Not verified.

On 2026-11-24 the user set the goal: the chain from idea to PR finds by itself the way that gives the most certainty, as simply as it can, without stopping on the way.

What the sources say, and where they are silent:

- pstack keeps one falsifiable predicate per task, written by the user or by the agent at framing. It has no step that ranks proof methods. It flags a missing means of proof rather than building it, and ships an update to a formal check in a change of its own.
- Ray Amjad's account of Anthropic's practice:
  - Acceptance criteria are written as user journeys, before coding, and each journey is verified separately.
  - End-to-end proof on the real surface is "the most reliable form of testing", and without it the agent "results to a cheaper test… which can ultimately give you less confidence".
  - The agent installs what it lacks during the task, and reports what it could not prove.
  - A separate checker makes sure the driver did not cheat.
- No source ranks proof methods in a fixed order, and none says what a task does with a missing formal check. Those parts of this decision are ours.

An independent review of the first draft, against these sources and for the experience of the developer and the agent, kept its direction and asked for less weight. One ladder instead of two, the driver built in one place, drafted promises that start no costly work, builder-made instruments checked independently, and a test that measures certainty and interview length rather than format.

## Decision

- **The spec sets the bar.** It keeps one `done_when`. Each user story also states its journey: the surface, the steps, the expected result. One journey per story is the minimum and usually enough; hard zones add their edge cases. The agent drafts the journeys and the user confirms them with a yes in the grill. A section, Promises, holds what must never break: one product sentence each, with the harm when it breaks. A promise about every order of steps or every input, such as a race, a retry, or an invariant, is a property; any other promise is a journey. Each journey and each promise is a case. For a spec with a user-facing surface, the journeys' surfaces are its seams; the Seams section names only seams beyond them, such as a library's API.
- **`shape-spec` looks up the means of proof** of the area as facts: drivers and formal checks, stale or not. It writes nothing technical in the spec. For a surface with no driver, it collects from the user what only the user can give, the account, the access, and where the secret lives, and records it in the project folder, never in the spec and never the secret itself.
- **The frame aims each case at the highest proof its kind allows.**
  - A journey reaches the highest certainty level its surface allows: level 5 through the driver where there is one. A case below the level `proof.md` requires names why.
  - A property follows a breadth order: a formal check, then generated inputs, then example tests. A property below a formal check names why.
  - A promise in a hard zone needs both a level and a breadth. No new column: the coverage table shows the reason only for a case below its target.
- **A task builds the proof it lacks**, as its first unit, before the change:
  - a missing driver for a touched surface, through `create-app-driver`, with the access `shape-spec` collected;
  - a missing formal check, through `create-formal-verification`, only for a promise the user stated in a hard zone; otherwise the PR recommends one;
  - a formal check stale on the base, through `maintain-formal-verification`.

  A bug either pass finds on the base becomes an issue. Its case stays under Not verified, and the task goes on. When the app does not start, the task proves what it can at level 4, and ends `needs-human` with the blocker and its remedy.
- **An instrument the builder made is checked by someone else.**
  - A driver built in the task is followed cold by a fresh subagent before the change uses it.
  - A shared driver or check lands as its own PR, with its own verdict.
  - For a private check repaired or created in the task, the builder saves the check as it stood on the base in the work directory. The verifier's `breakage` lane compares the two and breaks the guarded code once.
- **The verifier reads the spec.** Its brief carries the spec issue, and `live` drives the spec's journeys and promises. A story or a promise missing from the coverage table is graded as `verify-pr` grades any missing case: a FAIL when it misbehaves, a coverage gap the builder adds before `ready` when it works. `spec` reads Out of scope to find what nobody asked for.
- **A task without a spec**, when `medium` or `high`, gets its journeys and promises drafted in the frame, shown, and the task goes on, as ADR 0014 says. A `low` task keeps its light path. A promise the builder drafted never starts `create-formal-verification`; it yields a recommendation.
- **One more stop.** A task stops for access only the user can give, such as an account or a secret, when no earlier step collected it.
- **A check holds the bar.** The evidence record lists the spec's story and promise ids, and `check_evidence.py` fails when one has no case.

## Alternatives rejected

- **pstack's way, the predicate alone and the agent writing the cases**: the builder sets the bar of its own judge for every case beyond `done_when`.
- **A fixed method order for journeys**: it repeats the certainty levels, where level 5 already means driven through the driver, and adds a column the user must read. The draft had it.
- **Building the driver during `shape-spec`**: six steps of setup inside an interview, for no more certainty than building it as the task's first unit. Collecting the access while the user is present keeps the task from stopping. The draft had it.
- **A fresh verifier reviewing the proof plan before build**: one more agent on every task, and no source does it. The verifier already judges coverage at the end. The review of `done_when` before build, for `high` and hard zones, stays.
- **A sixth certainty level for formal proof**: it mixes how real an observation is with how many cases it covers. A proven model does not show the app.
- **A formal check created for every hard zone a task touches, or for a promise the builder drafted**: too costly for code where tests already reach the cases, and the builder would set the bar that starts the costliest work.
- **A missing means of proof only flagged, as pstack and ADR 0017 do**: the task then ends `needs-human` or leaves its hard zone unproven, which is the stop the user asked to remove.
- **The plan of proof written in the spec**: the spec names behavior, not files. Which driver or tool proves a case goes stale faster than the behavior it proves.

## Consequences

- A spec takes one more grill branch and one more round of confirmation. The test of this decision caps how much longer the interview may get.
- A task on an area without a driver, or with a stale check, is longer: its first unit builds or repairs the means of proof, and a fresh subagent or the verifier checks what it built.
- A run on a repo with neither driver nor formal check, such as a new one, creates the driver as it goes, and formal checks only for the promises the user stated.
- The coverage table changes only by the reasons of cases below their target.
