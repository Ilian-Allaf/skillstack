# A first glossary

The first `GLOSSARY.md` of a repo, drafted from the code. Its shape and its rules are those of `shape-spec`'s [domain.md](../../shape-spec/references/domain.md): terms only, each with its meaning and the words to avoid.

## Where the terms are

- **Domain types**: models, entities, schemas, database tables, the enums and unions that name states.
- **What the user sees**: route names, menu items, buttons, command names, error messages.
- **What people write**: the README, docs, issue titles, and review comments, which show the words the team actually says.

Keep a term when the domain owns it: "note", "draft", "sync". Leave out what any codebase has: "user", "service", "helper", unless this repo gives it a meaning of its own.

## Check each term against the code

- **One word, two meanings.** `account` is the billing customer in one module and the login in another. Say so; the user picks the meaning, and the other one gets its own term.
- **Two words, one meaning.** `remove` in the UI, `delete` in the API, `purge` in the job. Pick the word the code uses most, list the others under Avoid, and ask when the choice is not clear.
- **A state the code allows that the word hides.** `saved` while a sync is still pending. Note it: it is a case for later proof.

## Ask the user only what the code leaves open

Ask in one round, each question with your recommended answer, through the harness's question tool. Everything the code settles, you settle. Keep the draft short: twenty well-checked terms beat a hundred guessed ones.
