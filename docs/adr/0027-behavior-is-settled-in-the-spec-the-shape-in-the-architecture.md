# 0027. Behavior is settled in the spec, the shape in the architecture

- **Status**: accepted, 2026-11-28. Amends [0024](0024-the-architecture-is-shaped-apart-from-the-intent.md): `shape-architecture` no longer asks a product question.
- **Applies to**: `skills/shape-architecture/` (SKILL.md, `references/questions.md`), `skills/shape-spec/` (SKILL.md, `references/grill.md`)
- **Enforced by**: review

## Context

On 2026-11-28, the user ran `shape-spec` then `shape-architecture` on a real codebase, a shared-expenses app, for a feature that lets a participant leave a group. `shape-architecture` asked six questions. Three were about behavior, not about the shape of the code: whether a participant added by mistake is deleted, whether a recurring expense keeps charging someone who left, and whether former participants stay in the stats. The user expected every question about how the app behaves in `shape-spec`, and only architecture in `shape-architecture`.

Two things let this happen:

- `shape-architecture`'s `questions.md`, under ADR 0024, says: "When a shape has a consequence for the product the spec does not settle, such as working offline, ask it as a product question and record the answer under the spec's Decisions." This puts behavior questions in the architecture interview, which goes against the skill's own rule, "you settle how, never what".
- `shape-spec`'s grill asks about what the user brought, not about what the code already does. The three questions came from reading the code: the cascade delete, the recurring expense that copies its split, the stats built from every participant. They were facts the grill should have found and turned into questions first.

## Decision

### `shape-spec` asks what the code reveals
The grill gains a branch: a fresh subagent reads the code the feature touches and lists the behaviors already there that the feature collides with, such as data a delete removes, a copy that carries a value forward, a default, or a total. Each collision that changes what a user sees or loses becomes a product question on the frontier. The subagent starts with the interview; only the questions that hang off its findings wait for it.

### `shape-architecture` asks only about the shape
A consequence for the product that the spec does not settle is not asked. `shape-architecture` names it to the user, leaves the shape decisions that hang off it open, and hands over `/shape-spec <issue>` before `/ship`. `shape-spec`, given a spec issue with an open decision, grills it and edits the spec in place.

The rest of ADR 0024 stands, including asking each shape trade-off with its consequence for the product: the user picks between shapes knowing what each one costs, but the behavior itself is decided in `shape-spec`.

## Alternatives rejected

- **Keep the product question in `shape-architecture`**: one session fewer, but behavior gets decided by whichever skill happens to find it, and the spec's Decisions get written by a skill that should only add Technical decisions.
- **Stop `shape-architecture` at the first product gap**: the shape questions that do not depend on it would wait for nothing. Naming the gap and leaving only what hangs off it open costs less.

## Consequences

- A spec takes more questions in `shape-spec` and fewer surprises in `shape-architecture`.
- A product gap found late costs one more `shape-spec` session on the same issue, then the architecture decisions that waited for it.
- These ideas are ours, from the session of 2026-11-28.
