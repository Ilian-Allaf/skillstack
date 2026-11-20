# fix-root-causes

**Apply when** you debug.

**Rule.** Fix the fault, not the place where it surfaced. The symptom is where a wrong state became visible; the root cause is the first place the system did something it should not do, or failed to handle a state it should handle.

## How

- Reproduce first (`build-a-tight-loop`).
- Ask "why" at each step until the answer is a wrong decision in the code, not a consequence of an earlier one.
- When stuck, instrument. Read the actual error and the actual state. Do not guess.
- Ask whether the state that triggered the symptom is legitimate. If the system may be in that state, the code that broke on it is the root cause, and handling the state there is the fix. If the state should never exist, a check where it broke hides the bug: find what produced the state. Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide a bug.
- When something fails only after a restart, suspect persisted state first: config files, caches, lock files, serialized state.
- Fix the pattern, not just the instance: find every place with the same fault.
- A workaround that needs a paragraph of comment to justify it means the code is wrong. Fix the code.
- When the deciding fact took a deep dig to find, propose the cheap, always-on signal that would have shown it at first look: a log line, an assertion, a metric.

## Test

Can you name the first wrong decision in the code, and show with a run that the fix removes it rather than its consequence?

## Sign it was skipped

A null check added where the crash happened. A retry around a call that fails for a reason. A `catch` that logs and continues.

## Example

```ts
// Skipped: the crash is silenced where it surfaced.
const name = user?.profile?.name ?? "Unknown";

// Applied: the profile is created with the user, so a user without one cannot exist.
async function createUser(input: NewUser): Promise<User> {
  return db.transaction(async (tx) => {
    const user = await tx.users.insert(input);
    await tx.profiles.insert({ userId: user.id, name: input.name });
    return user;
  });
}
```
