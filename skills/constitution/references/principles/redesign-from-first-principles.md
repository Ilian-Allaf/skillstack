# redesign-from-first-principles

**Apply when** a new requirement lands in an existing design, and when a sketch is scrapped.

**Rule.** Build as if the requirement had been an assumption from day one, instead of bolting it on.

## How

1. Read every affected file, and write how the current design works.
2. Answer in writing: "If we wrote this from scratch with this requirement, what would we build?"
3. Set that answer beside the bolt-on. Take the redesign when the bolt-on adds a branch, a flag, or a special case that the redesign does not need.
4. Carry the change through every reference: types, tests, docs, examples, config.
5. Think the whole redesign first, then ship it in units that each land green (`sequence-verifiable-units`).

Distinct from `attack-the-premise`, which questions a fact the current design assumes. This one rebuilds the design around a new requirement.

## Test

A reader who never saw the old design could not tell that this requirement came late.

## Sign it was skipped

The new requirement lives in an `if` at each place it touches. A parameter is threaded through layers that never read it.

## Example

The requirement: a document can now have several owners.

```ts
// Skipped: bolted on. Every check now asks two questions.
type Doc = { ownerId: UserId; extraOwnerIds?: UserId[] };
const canEdit = (d: Doc, u: UserId) => d.ownerId === u || (d.extraOwnerIds ?? []).includes(u);

// Applied: as if several owners had always existed.
type Doc = { ownerIds: NonEmpty<UserId> };
const canEdit = (d: Doc, u: UserId) => d.ownerIds.includes(u);
```

The redesign also migrates the stored rows and deletes `ownerId` (`migrate-callers-then-delete`).
