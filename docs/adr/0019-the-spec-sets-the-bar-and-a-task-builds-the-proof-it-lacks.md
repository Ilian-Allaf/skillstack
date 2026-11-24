# 0019. The spec sets the bar, and a task builds the proof it lacks

- **Status**: accepted, 2026-11-24; proposed 2026-11-24.
- **Supersedes**:
  - in [0017](0017-a-formal-check-guards-every-task-that-touches-its-code.md), three clauses: "its case goes under Not verified, and the builder opens an issue for `/maintain-formal-verification`"; "The maintain pass stays outside the task"; and "A check stale on the base is not updated by the task".
- **Extends**:
  - in 0017, the verifier's judgment of a check, now also for a check created or repaired in the task, not only one in sync on the base;
  - in [0014](0014-a-launched-task-runs-to-a-ready-pr.md) and rule 11 of the constitution, the list of stops, with one more: access only the user can give;
  - in [0016](0016-the-working-files-live-outside-the-repo.md), "chosen entry by entry when `setup-repo` runs": one entry is never shared and is written by `shape-spec`, `access/<app>.md`, since it says where a secret lives.

  The rest of these ADRs stands.
- **Applies to**: `skills/shape-spec/`, `skills/ship/` (frame, verification setup, the units of a task, `scripts/check_evidence.py`), `skills/verify-pr/` (the brief, `live`, `breakage`, `spec`), `skills/create-app-driver/`, `skills/constitution/README.md` (rule 11), `skills/constitution/references/proof.md`, `coverage.md`, `formal.md` (In a task), `glossary.md`, `target-repo.md`
- **Enforced by**: `check_evidence.py` fails when a story or a promise of the spec has no case in the evidence record, with a test in `tools/test_check_evidence.py`. The rest by three blind `test-skill-change` runs and by review.

## Context

Today the builder decides how a task is verified:
- `shape-spec` writes one global `done_when` and user stories with no observable result.
- `ship`'s frame turns them into cases and picks the evidence per case. The verifier's brief is that frame, not the spec.
- A formal check is used only when it already exists.
- A missing driver is found in the frame, yet the task goes on and ends `needs-human` because `live` is INCONCLUSIVE. This happens although `ship`'s verification setup already says to prepare the driver first.
- A check stale on the base leaves its hard zone under Not verified.

On 2026-11-24 the user set the goal: the chain from idea to PR finds by itself the way that gives the most certainty. It does so as simply as it can, and without stopping on the way.

**pstack** (`knowledge/sources/repos/cursor-pstack/repo/`):
- It keeps one done check per task that "must be able to pass or fail" (`docs/guide/02-poteto-mode.md:45`).
- On a task, "'Inconclusive' or wrong-surface is not a pass. Flag it" (`skills/poteto-mode/playbooks/feature.md:13`).
- Its setup offers once to generate a driver and a formal check (`docs/guide/01-setup.md:35-41`), but a task does not build them.
- It puts "the verification updates in a change of their own" (`skills/maintain-formal-verification-skill/SKILL.md:58`).

**Ray Amjad's account of Anthropic's practice** (`knowledge/sources/videos/2026-11-23-how-anthropic-verifies-code-ray-amjad/transcript.md`):
- Success is set by "acceptance criteria with 10 different flows" in the spec (07:14, 18:31), each flow verified separately, in parallel (06:16).
- End-to-end testing is "the most reliable form of testing" (04:21).
- An agent that cannot verify to the end "usually results to a cheaper test", with less confidence (08:45).
- Asked to "install into the sandbox" what it lacks (03:22), the agent installs it during the task, then proposes to make it permanent (05:44).

**Where the sources are silent**: no source sets the proof target by kind of case, or says what a task does with a missing formal check. Those parts of this decision are ours.

An independent review of the first draft checked it against these sources and for the experience of the developer and of the agent. It kept the direction and asked for less weight:
- one ladder instead of two;
- the driver built in one place;
- drafted promises that start no costly work;
- builder-made instruments checked independently;
- a test that measures certainty and interview length, not format.

## Decision

### The spec sets the bar
- **One `done_when`, plus one journey per story.** Each journey states the surface, the steps, and the expected result. One journey per story is the minimum and usually enough; hard zones add their edge cases.
- **The grill drafts and you confirm.** The agent drafts the journeys, the promises, and what cannot be verified. The user confirms with a yes in the grill. Step 3 of `shape-spec` is done only when the spec holds them.
- **Promises.** A section, Promises, holds what must never break: one product sentence each, with the harm when it breaks.
  - A promise about every order of steps or every input, such as a race, a retry, or an invariant, is a property.
  - Any other promise is a journey.
- **Every journey and every promise is a case.**
- **Seams.** For a spec with a user-facing surface, the journeys' surfaces are its seams. The Seams section names only seams beyond them, such as a library's API.

### `shape-spec` looks up the means of proof
It looks up the drivers and formal checks of the area as facts, stale or not, and writes nothing technical in the spec. For a surface with no driver, it asks the user for what only the user can give: the account, the access, and where the secret lives. It records them in the project folder, in `access/<app>.md`, apart from `drive-<app>/` so a shared driver's folder stays a route; never in the spec, and never the secret itself.

### The frame aims each case at the highest proof its kind allows
- **A journey** reaches the highest certainty level its surface allows. A case below the level `proof.md` requires names why.
- **A property** follows a breadth order: a formal check, then generated inputs, then example tests. A property below a formal check names why.
- **A promise in a hard zone** needs both.
- **The coverage table** shows a reason only for a case below its target.

### A task builds the proof it lacks
This is the task's first unit, before the change.
- **A missing driver** for a touched surface: through `create-app-driver`, with the access `shape-spec` collected.
- **A missing formal check**: through `create-formal-verification`, only for a promise the user stated in a hard zone. Otherwise, the PR recommends one.
- **A formal check stale on the base**: through `maintain-formal-verification`.

When either formal pass finds a bug on the base, the bug becomes an issue. Its case stays under Not verified, and the task goes on.

When the app does not start, that is a dead end in the sense of ADR 0014. The task proves what it can at level 4, and ends `needs-human` with the blocker and its remedy.

### What the builder built is checked by someone else
- **A driver built in the task** is followed cold by a fresh subagent before the change uses it.
- **A shared driver or check** lands as its own PR, with its own verdict.
- **A private check repaired in the task**: the builder saves the check as it stood on the base in the work directory.
- **The verifier's `breakage` lane** judges every check created or repaired in the task. It compares a repaired check with its base version, then breaks the guarded code once.

### The verifier reads the spec
- Its brief carries the spec issue, and `live` drives the spec's journeys and promises.
- A story or a promise missing from the coverage table is graded as `verify-pr` grades any missing case: a FAIL when it misbehaves, a coverage gap the builder adds before `ready` when it works.
- `spec` reads Out of scope.

### A task without a spec
- **A `medium` or `high` task**: the frame drafts the journeys and promises, shows them, and the task goes on, as ADR 0014 says.
- **A `low` task** keeps its light path.
- **A promise the builder drafted** never starts `create-formal-verification`. It yields a recommendation.

### One more stop
A task stops for access only the user can give, such as an account or a secret, when no earlier step collected it.

### A check holds the bar
The evidence record lists the spec's story and promise ids. `check_evidence.py` fails when one has no case.

## Alternatives rejected

- **pstack's way, the done check alone and the agent writing the cases**: the builder sets the bar of its own judge for every case beyond `done_when`.
- **A fixed method order for journeys**, as the first draft had: it repeats the certainty levels, and adds a column the user must read.
- **Building the driver during `shape-spec`**, as the first draft had: six steps of setup inside an interview, for no more certainty than building it as the task's first unit. Collecting the access while the user is present is enough to keep the task from stopping.
- **A fresh verifier reviewing the proof plan before build**: one more agent on every task, and no source does it. The verifier already judges coverage at the end, and the review of `done_when` before build stays for `high` and hard zones.
- **A sixth certainty level for formal proof**: it mixes how real an observation is with how many cases it covers. A proven model does not show the app.
- **A formal check for every hard zone a task touches, or for a promise the builder drafted**: too costly where tests already reach the cases. It would also let the builder set the bar that starts the costliest work.
- **A missing means of proof only flagged, as a pstack task and ADR 0017 do**: the task then ends `needs-human`, or leaves its hard zone unproven. This is the stop the user asked to remove.
- **The plan of proof written in the spec**: the spec names behavior, not files. Which driver or tool proves a case goes stale faster than the behavior it proves.

## Consequences

- A spec takes one more grill branch and one more round of confirmation. The test of this decision caps how much longer the interview may get.
- A task on an area without a driver, or with a stale check, takes longer. Its first unit builds or repairs the means of proof, and a fresh subagent or the verifier checks what it built.
- A run on a repo with neither driver nor formal check creates the driver as it goes. It creates formal checks only for the promises the user stated.
- The coverage table changes only by the reasons of cases below their target.
