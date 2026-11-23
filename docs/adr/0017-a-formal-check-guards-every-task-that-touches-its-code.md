# 0017. A formal check guards every task that touches its code

- **Status**: accepted, 2026-11-23
- **Applies to**: `skills/constitution/references/formal.md` (In a task, Stale), `skills/constitution/references/proof.md` (hard zones), `skills/constitution/references/coverage.md`, `skills/ship/SKILL.md` (build), `skills/verify-pr/references/lanes.md` (breakage), `skills/analyze-impact/references/where-grep-stops.md`, `skills/create-formal-verification/`
- **Enforced by**: no tool; the verifier's `breakage` lane, which fails a PR whose formal check misses a break or went stale at the head

## Context

A formal check (`prove-<area>`) is only worth something while its model describes the code. Before this decision, it ran only when `analyze-impact` ran, so never for a `low` task; only `analyze-impact` noticed a stale check; and a builder had no rule for a change that alters covered code, so either every such PR left the check stale, or the builder updated the model and judged its own update.

pstack, where the formal skills come from, leaves all of this to the agent: the generated skill is picked by its description, an update is made under the agent's own discipline, and staleness is noticed when someone asks.

## Decision

- Every file a formal check covers is a hard zone. A task that touches one is never `low`, its property is a case of the coverage table, and the verifier runs its `breakage` lane.
- `frame` checks each such check for staleness on the base. A stale check proves nothing: its case goes under Not verified, and the builder opens an issue for `/maintain-formal-verification`. The maintain pass stays outside the task.
- A builder whose change alters covered code of an in-sync check updates the check in its build, by the rules of `formal.md`, and lists the update in the PR's Proof. A check stale on the base is not updated by the task.
- For each check in sync on the base, the verifier judges the check as it stands at the head: it breaks the guarded code once, and a break the check misses, or a check the change left stale, is a FAIL graded should. A model does not read the code, so the break is described in the model before the model checker runs.
- Staleness compares each covered file with the content id the check records, `git rev-parse <commit>:<file>`, not history, so a squash, a rebase, or a fresh clone that lacks the updating commit leaves the check in sync.
- A shared check also runs in the repo's CI, wired by the PR that shares it.

## Alternatives rejected

- **pstack's way, the agent's judgment**: the check runs when an agent thinks of it, and a stale pass looks like a proof.
- **Every update through the maintain pass**: every PR that touches covered code would end with an issue, and the check would stay stale until the user ran the pass.
- **The builder updates and judges its own update**: the author is never the judge ([ADR 0003](0003-the-author-is-never-the-judge.md)); a model loosened until it passes reads the same as a correct one.
- **Staleness by history** (`git log <sync commit>..HEAD`): a squash merge rewrites the commit the builder recorded, so every updated check would read stale after its merge.
- **Staleness by a diff against the sync commit** (`git diff <sync commit> <commit>`): after a squash merge and a deleted branch, a fresh clone lacks that commit, and the diff errors instead of comparing.

## Consequences

- Tasks that touch covered code cost more: a full frame, the verifier reading `done_when` before build, and the `breakage` lane.
- A private check is updated in place while its PR is open, so another task on the base sees it stale until the merge, which is true: the model describes the branch.
- The CI run of a shared check is the team's check, not a gate of the framework's own, which [ADR 0001](0001-the-user-always-merges.md) rules out. For a model, CI proves the model and, through the staleness test, that the covered files still match it; a code change made without updating the model fails the staleness test, not the model checker.
