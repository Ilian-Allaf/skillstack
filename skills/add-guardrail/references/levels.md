# Levels

From the strongest to the weakest.

| Level | How it stops the mistake | Examples |
|---|---|---|
| 1. Architecture | the wrong way no longer exists | one owner per piece of state; internals hidden so the wrong import fails; one source of truth instead of hand-synced lists; the old API deleted |
| 2. Type | the bad state cannot be written | a branded id type; a union that makes the illegal state unrepresentable; a required field instead of an optional one |
| 3. Lint or CI check | the bad code is written, then fails loudly | a custom lint rule; a script in CI that greps for the pattern; a dependency boundary check |
| 4. Test | the bad behavior fails a test | a test at a public seam that fails when the behavior breaks |
| 5. Docs or agent rule | nothing fails; an agent may skip it | `coding-standards.md` in the project folder, for judgment calls only |

## Rules

- **A lint message names the fix.** "Use `useNoteStore()` from `src/notes/store.ts`; components never read `store.state` directly." An agent reading only the message can correct the code.
- **Delete what would be copied.** Dead code and old patterns are examples the next agent will follow.
- **Tests that lie get fixed or deleted.** A test that still passes when its behavior breaks, or fails when only internals change, misleads more than it protects.
- **Exceptions carry a reason and an owner.** An allowed occurrence goes in the check's own list of exceptions, with the reason and the user's approval. Never in a code comment: the comment hunter in `ship` deletes those.
