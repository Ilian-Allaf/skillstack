# design-the-data-first

**Apply when** a change adds logic, a type, or a module, and when you order the work.

**Rule.** Data structures first, scaffold first. Structural decisions keep options open; code-level decisions keep the code simple.

## How

- Define the core types before the logic. List every way the data is read and written: by id, by range, in order, by owner, all at once. Trace each one through the structure. A main path the structure serves badly means the structure is wrong now; "we will add an index later" is that sign.
- Do first what every later step benefits from: the shared types, the test harness, the check that will prove the work. Removing dead code comes before that (`subtract-before-you-add`).
- Factor the structure, not every line. Types and data models converge on one definition. Three similar statements still beat an early abstraction.
- Each increment lands one coherent abstraction, or deepens one that exists. It does not spread a new capability across callers as special-case coordination.

## Test

For each access path, you can point to the field, the index, or the collection that serves it.

## Sign it was skipped

A new capability travels as a flag through several callers. A lookup scans a list that should be a map. A later step recomputes what an earlier type could have held.

## Example

Sessions are read by id on every request, and listed by user on one page.

```ts
// Skipped: the structure was picked before the reads were listed.
const sessions: Session[] = [];
const findSession = (id: SessionId) => sessions.find((s) => s.id === id); // a scan on the hot path

// Applied: each read has the structure that serves it.
type SessionStore = {
  byId: Map<SessionId, Session>;
  idsByUser: Map<UserId, Set<SessionId>>;
};
```
