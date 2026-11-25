# Proof

What counts as evidence, how sure a claim is, and how deep to verify for a given risk.

## Evidence

Evidence is something observed in this session:

- command output, with the command;
- a test or script that fails without the change and passes with it;
- a screenshot, recording, or accessibility snapshot of the running app, before and after;
- a stored value read back: a database row, a written file, a response body;
- a profile or a log line.

Each of these is a claim, not evidence:

- "the build passes" or "it compiles";
- "the tests are green" when no test covers the changed behavior;
- a mocked test standing in for a UI or an external system;
- "I checked" with no artifact;
- a screenshot with no steps to reproduce it.

Evidence is replayable. The PR gives the command or the steps that produced it.

## Certainty levels

Every claim that matters carries the level it reached.

| Level | What was done | Example |
|---|---|---|
| 1, said | the agent states it | "this does not touch export" |
| 2, pointed | a real `file:line` is cited | "`export.ts:42` never reads this field" |
| 3, reasoned | the failure case was walked step by step and does not happen | "the only caller always passes a saved note" |
| 4, ran | a script or test calls the real code and would fail if the claim were false | `npm test -- export.double-save` |
| 5, reproduced | observed in the running app | before and after captures from `drive-<app>` |

Required levels:

- **`done_when`** reaches level 5 when the app has a user-facing surface, and level 4 for a library or a stateless CLI.
- **The safety fact** of a change, the one fact the change is safe because of, reaches level 4. Otherwise mark it `unproven` in the PR.
- **A verifier FAIL** comes with its run, at level 4.

## Drivers and formal checks

Level 5 needs the running app, driven the way a user does. The repo's drivers live in `~/.agents/projects/<project>/drive-*/SKILL.md`, one per surface: a repo with a web app and a CLI has two; a driver the team shares is a route to the repo. Look there, not only in the harness's skill list, which a subagent may not have.

- Use the driver whose surface the change touches. A change across surfaces is proven on each surface, with its driver.
- When no driver exists for a touched surface, build it before the change, as [frame.md](../../ship/references/frame.md) says, through [create-app-driver](../../create-app-driver/SKILL.md), with the access `shape-spec` wrote to `access/<app>.md`. Stop only for access no earlier step collected (rule 11). When the app does not start, that is a dead end: prove what you can at level 4, write the gap under Not verified, and end `needs-human` with the blocker and its remedy. A missing driver is never a pass: for a `medium` or `high` task without one, the `live` lane is INCONCLUSIVE.

The repo's formal checks live in `~/.agents/projects/<project>/prove-*/SKILL.md`, one per guarded area; a check the team shares is a route to the repo. Look there too, not in the harness's skill list. A check covers a touched file when its Covered code section lists that file: read that section of each check against the diff. [formal.md](formal.md#in-a-task) says what a task does with each check it touches.

Where the project folder is absent, as in a cloud session or CI, read the shared drivers and checks at the repo paths [target-repo.md](target-repo.md) gives.

## The target of a case

Each case aims at the highest proof its kind allows, and says why when it falls short.

- **A journey** reaches the highest certainty level its surface allows: level 5 through the driver where the surface has one. A case below the level this file requires names why.
- **A property**, a claim about every order of steps or every input, follows a breadth order: a formal check, then generated inputs, then example tests. A property below a formal check names why.
- **A promise in a hard zone** needs both: its journey at its level, and its property at its breadth.
- **A visual target** reaches level 5: the head captured through the driver at the target's states and widths, side by side with the target, with the measured numbers of the [target loop](../../ship/references/visual-loop.md). A critic's score is level 1 and never reaches the target.

The levels measure how real an observation is; the breadth order measures how many cases it covers. Neither replaces the other.

## `done_when`

`done_when` is the finish condition of a task. It is:

- **observable**: a command, a test, or an app journey that answers yes or no. "Works correctly" is not observable; "the e2e double-click test passes and the notes table holds one row" is;
- **red on the base**: run it before any code changes, and confirm it fails. A `done_when` that is already green proves nothing: the task is misread or already done, so ask. A refactoring adds a behavior pin that is green on both the base and the head;
- **from the user**: taken from the request or the issue. The builder never sets the bar for its own judge. When it has to sharpen the wording, it shows the sharpened version and the user corrects it;
- **narrow**: one task, one condition. Several conditions mean several units of the task: one PR each, stacked, as `frame` describes. The exception is the two parts a playbook defines, such as a refactoring's target and its pin;
- **shown**: it is in the frame, where the user can correct it at any time. For `high`, or a task that touches a hard zone, the verifier reads it before `build` and flags it if it cannot be checked.

## Risk classes

The builder announces the class in `frame`. The user can correct it in one word.

| Class | When |
|---|---|
| `high` | the change touches auth, payments, migrations, data deletion, CI, or secrets; or it changes more than 400 lines |
| `low` | every changed file is docs or tests, and none is in a hard zone; or a change of about 30 lines inside one function, with no hard zone and no public interface changed |
| `medium` | everything else |

The class sets how deep verification goes:

| Step | `low` | `medium` | `high` |
|---|---|---|---|
| `frame` | short | full; `done_when` read by the verifier when a hard zone is touched | full, `done_when` read by the verifier |
| red to green loop | when code changes | yes | yes, plus the hard zones `frame` marked |
| proof on the app | before and after when `done_when` is user-facing; otherwise the docs render | before and after | before and after, every touched path |
| `analyze-impact` | no | yes, without widening | yes, widened to several subagents |
| `verify-pr` lanes | `replay`, `spec`, `standards` | adds `live`; `breakage` when a hard zone is touched | adds `breakage` and `adversarial` |

Hard zones are where models fail most, and this is their one list: concurrency and locking, sync, retries, payments, data loss, security, migrations, and protocols, connection lifecycles included; and every file a formal check covers, as its `prove-<area>` lists them. `frame` names the ones a change touches, and verification goes deeper there. Below that edge a verifier mostly confirms what the builder already got right.

A lane gets lighter only when the seeded defects in calibration show it no longer catches anything the other lanes miss.
