# 0019. The spec sets the bar, and a task builds the proof it lacks

- **Status**: proposed, 2026-11-24. Once accepted, it supersedes two clauses of [0017](0017-a-formal-check-guards-every-task-that-touches-its-code.md): "The maintain pass stays outside the task" and "A check stale on the base is not updated by the task". The rest of ADR 0017 stands.
- **Applies to**: `skills/shape-spec/`, `skills/ship/` (frame, verification setup, the units of a task), `skills/verify-pr/` (the brief, `live`, `spec`, coverage), `skills/constitution/references/proof.md` (drivers and formal checks), `skills/constitution/references/coverage.md`, `skills/constitution/references/formal.md` (In a task), `skills/constitution/references/glossary.md`
- **Enforced by**: no tool; two blind `test-skill-change` runs, the first from `shape-spec` to `ship`'s frame, the second on `verify-pr` with a PR whose coverage table misses a story; then review

## Context

The verification of a task is decided by its builder. `shape-spec` writes one global `done_when` and user stories with no observable result. `ship`'s frame turns them into cases, picks the evidence per case with no order of reliability, and the verifier's brief is that frame, not the spec. A formal check is used only when it already exists. A missing driver is found in the frame, yet the task goes on and ends `needs-human` because `live` is INCONCLUSIVE. A check stale on the base leaves its hard zone under Not verified.

On 2026-11-24 the user set the goal: the chain from idea to PR finds by itself the way that gives the most certainty, without stopping on the way.

pstack keeps one falsifiable predicate per task, written by the user or by the agent at framing, has no step that ranks methods, flags a missing means of proof instead of building it, and keeps formal verification as an opt-in layer whose updates ship in a change of their own. Anthropic's verification practice, as Ray Amjad reports it, writes acceptance criteria as user journeys before coding, ranks end-to-end proof on the real surface highest, makes the agent name every fallback to a weaker proof, and has the agent install the tooling it lacks during the task.

## Decision

- **The spec sets the bar.** It keeps one `done_when`. Each user story also states its journey: the surface, the steps, the expected result. The agent drafts them and the user confirms them in the grill. A new section, Promises, holds what must never break: one product sentence each, with the harm when it breaks. Each journey and each promise is a case of the task.
- **`shape-spec` looks up the means of proof** of the area as facts: drivers and formal checks. It writes nothing technical in the spec. When a surface of the spec has no driver, it runs `create-app-driver` while the user is present to give accounts and access.
- **The frame picks the strongest method per case**, in a fixed order by kind of case. For a journey: the running app through its driver, then an end-to-end test on the running app, then a test at the seam, then a unit test. For a property over every order of steps or every input: a formal check, then generated inputs, then example tests. Every fallback to a weaker method is named in the coverage table with its reason. The certainty levels stay 1 to 5: they measure how real an observation is, while a formal check measures its breadth. A promise in a hard zone needs both.
- **A task builds the proof it lacks**, as its first unit, before the change:
  - a missing driver for a touched surface, through `create-app-driver`; the task stops only for what the user alone can give, such as an account or a secret;
  - a missing formal check, through `create-formal-verification`, only for a promise in a hard zone; otherwise the PR recommends one;
  - a formal check stale on the base, through `maintain-formal-verification`. A bug the pass finds becomes an issue, its case stays under Not verified, and the task goes on.
  A shared driver or check lands as its own PR with its own verdict. A private one is updated in place; the verifier's own journeys in `live` and its break in `breakage` keep it honest.
- **The verifier reads the spec.** Its brief carries the spec issue. `live` builds its journeys from the spec's journeys and promises; a journey or a promise missing from the coverage table is a finding; `spec` reads Out of scope to find what nobody asked for.
- **A task launched without a spec** gets its journeys and promises drafted in the frame, shown, and the task goes on, as [ADR 0014](0014-a-launched-task-runs-to-a-ready-pr.md) says.

## Alternatives rejected

- **pstack's way, the predicate alone and the agent writing the cases**: the builder sets the bar of its own judge for every case beyond `done_when`.
- **A fresh verifier reviewing the proof plan before build**: one more agent on every task, and no source does it; the verifier already judges coverage at the end. The review of `done_when` before build, for `high` and hard zones, stays.
- **A sixth certainty level for formal proof**: it mixes how real an observation is with how many cases it covers; a proven model does not show the app.
- **A formal check created for every hard zone a task touches**: too costly for code where tests already reach the cases; kept for the promises the user named.
- **A missing means of proof only flagged, as pstack and ADR 0017 do**: the task then ends `needs-human` or leaves its hard zone unproven, which is the stop the user asked to remove.
- **The plan of proof written in the spec**: the spec names behavior, not files; which driver or tool proves a case goes stale faster than the behavior it proves.

## Consequences

- A spec takes one more grill branch and one more round of confirmation.
- A task on an area without a driver, or with a stale check, is longer: its first unit builds or repairs the means of proof.
- A run on a repo with neither driver nor formal check, such as a new one, creates them as it goes, and the PR says so.
- The coverage table gains the method of each case and the reason for each fallback.
