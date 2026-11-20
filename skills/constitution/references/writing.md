# Writing

How to write what a person reads: a PR body, a commit message, an issue, a reply, a doc, a skill. The target is a tired engineer who understands on the first read. `tools/lint_skills.py` already rejects some of the patterns below in the skills (P001 to P004); this file covers the judgment the linter cannot hold.

## Three rules above the rest

- **Cut every word that does no work.** If the sentence survives without the word, the word goes. "In order to" is "to"; "it is important to note that" is nothing.
- **Use the short, everyday word.** "Use", not `utilize`; "help", not `facilitate`; "many", not "numerous"; "if", not "in the event that".
- **When a rule makes a sentence worse, fix the sentence another way.** A sentence that follows every rule and reads like a machine wrote it has failed.

The codebase is the word list: write the real symbol, file, flag, or command, not a synonym or a description of it.

## Sentences

- One thought per sentence. Split a sentence a reader has to parse twice; keep a long one that carries a single fact with its condition.
- Say who does what: "the compiler checks the types", not "the types are checked". Passive only when the actor is unknown or does not matter.
- Present tense, to "you". Instructions as commands: "Run the script." Never "should be run".
- The condition before the instruction: "To reset the cache, delete `.cache/`."
- The common case first, the exceptions after.
- Keep "the" and "a", and the verbs: "The parser rejects a bad date, exits with code 2, and writes nothing", not "parser rejects bad date → exit 2, no write". Spell out arrows and abbreviations.
- Every "it", "this", and "they" points at one obvious thing; repeat the noun when in doubt.
- Keep "only" and "not" next to the word they change.
- Break long noun strings: "the script that checks the import budget", not "the import budget check script".
- Periods, not semicolons in a run of clauses; no dashes as punctuation; no slashes for "or".
- One name per thing, everywhere, and one word per action. The glossary holds the names.
- Mix lengths: a short sentence lands a point, a longer one carries a fact with its consequence.

## Patterns to cut

| Pattern | Instead |
|---|---|
| words that sound important: `crucial`, `pivotal`, `delve`, `enhance`, `robust`, `seamless`, `leverage`, `landscape` | the plain word, or the fact |
| "serves as", "stands as", "boasts" | "is", "has" |
| "not just X, but Y"; ideas forced into threes; synonyms cycled for variety | the point, the natural number of items, one name |
| "-ing" tails: "ensuring safety", "highlighting the risk" | a sentence that says what does it |
| a vague origin: "experts say", "it is known" | name who said it, or cut |
| hedges: "could potentially", "it might be argued" | "may", or the fact |
| metaphor nouns: north star, flywheel, substrate, wedge, surface, paradigm | the concrete word |
| feelings instead of mechanisms: "SQL you can read" | what it does: "`.toSQL()` returns the exact query" |
| adverbs propping a weak verb: "significantly improves" | the measured delta |
| bold labels that restate the line; title case headings; emojis in headings | prose; sentence case; none |
| chatbot phrases: "Great question!", "I hope this helps", "Let me know if" | nothing |
| generic endings: "the future looks bright" | the next step, or nothing |

A sentence that could appear unchanged in another project's docs says nothing about this one: cut it.

## A doc has one mode

Pick it first, and do not mix: a **tutorial** teaches by doing, with a visible result at each step; a **how-to** solves one problem for someone competent, action only; a **reference** describes, dry and complete; an **explanation** gives the why, the history, and the trade-offs, and is the only place for opinion. Split and link instead of mixing.

## PRs, commits, and replies

- A PR body is a briefing a reviewer reads in under a minute, in the shape of [pr-format.md](pr-format.md). Logs, SHA lists, and tables of runs go in a linked artifact or the folded part.
- A commit subject says why, in the imperative; the body does not repeat it.
- A reply to the user leads with what changed for them and what waits on them.

## Example

Before:

> Configuration of the import budget script parameters is performed via budget.json. Note that it's important to remember that running with --write, which updates the committed budget to reflect the current count, should only be done when lowering it. If exceeded, CI fails.

After:

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.
