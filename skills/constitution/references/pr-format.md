# PR format

The user reads the PR body to decide the merge without running anything. It is a one-minute briefing, not a lab notebook: what is visible says why, what is covered, what is not, the risk, and the verdict. Proof, breakage, and decisions are folded below, there to dig into. See [coverage.md](coverage.md), and write it as [writing.md](writing.md) says.

```markdown
<title that says why, not what>

## Why
Who notices the change and what changes for them, then the problem, in one or two sentences. Then one line on what the next engineer who owns this code inherits. If you cannot say what either would notice, the change or the explanation is off.

## Done when
The `done_when`, and the run that showed it red on the base.

## Coverage
| # | Case | Evidence | Level |
One row per case of the case list. A case without evidence points to Not verified.

## Demo
The video, when coverage.md requires one, with its chapters listed by case number.
The state chart, when the journey moves between states, each arrow marked with its case number.

## Not verified
What no run could prove. Write "nothing" when everything was proven.

## Risk
Class: low | medium | high. Door: two-way | one-way, and the irreversible choice when one-way.
Verdict: behavior <outcome>, code <outcome>, patch-id <7 chars>, <link to the verifier's comment>

<details><summary>Proof, breakage, decisions</summary>

## Proof
The commands and scripts that replay the evidence, the demo included.

## Breakage
The safety fact and its certainty level, or `unproven`.
Confirmed risks with their evidence. Cleared risks with the reason.
(`medium` and `high` only.)

## Design
The design note, when the change crossed a boundary and was sketched, as `ship`'s [design-note.md](../../ship/references/design-note.md) shapes it. Omit the section otherwise.

## Decisions
Choices made without the user, if any, each with the id of the principle that drove it when one did.

</details>

Created with <model> in <harness> (+ subagent models, never guessed)
```

## Rules

- **Title**: the reason for the change, in the imperative. "Prevent duplicate notes on double click", not "Update save handler".
- **Every claim in Coverage, Proof, and Breakage carries its certainty level** (see [proof.md](proof.md)).
- **No case is dropped from Coverage.** A case the agent could not prove stays in the table and points to Not verified.
- **A `one-way` door** names the irreversible choice on the Risk line, outside the folded part, so the user sees it before merging.
- **Captures and videos** go through a secret scan before upload, frames included. They are attached to the PR so they play in the page when the harness can upload; otherwise they live in CI artifacts and the body links them.
- **Out of scope findings** become issues, linked from the PR. They never grow the PR.
- **Model names** come from the session, never from a guess.
