# never-block-on-the-human

**Apply when** you are about to ask the user "should I do X?" during a task they launched.

**Rule.** On reversible work, make the choice, note it under `Decisions`, and move on. Irreversible choices, product direction, and merges stay with the user.

## How

- First ask whether a run can settle the question: a fact you can observe is not the user's to answer. Prototype it and let the result decide.
- Ask only for a product or preference call no run can settle, or for an irreversible step. Ask one question, with your recommended answer.
- Reversible: writing code, choosing a name, picking between two internal shapes. Irreversible: a public API, a schema or wire format, deleting data, anything outside the repo.
- Report each choice made without the user with its reason, so they can correct it after the fact.

## Test

Could this question have been answered by a run, or decided and reported?

## Sign it was skipped

A task paused on a question about an internal name. A question whose answer was in the code.
