---
name: analyze-impact
description: "Finds what a change breaks outside its diff, and proves by a run the one fact it is safe because of."
disable-model-invocation: true
metadata:
  kind: spine
  calls: "repo:drive-<app>, repo:prove-<area>"
  consumes: "a diff or a PR, and the task it serves"
  produces: "safety fact with its certainty level, confirmed risks, cleared risks, the cheapest catching test"
  hypothesis: "A model checks the lines it changed and misses what they break elsewhere; a plausible writeup reads the same whether it is true or not."
---

# Analyze impact

Read [the constitution](../constitution/README.md) and [proof.md](../constitution/references/proof.md) first.

Find what a change breaks somewhere else, before the user merges it. Listing the callers is not the job: grep does that in a second. The job is the breakage grep does not show.

Two callers use this skill. The builder runs it in `ship` for `medium` and `high` tasks. The verifier runs it in its `breakage` lane, without seeing the builder's report. Both follow the same steps.

## Steps

1. **Read the change.** Read the diff, the symbols it adds, changes, and deletes, and what now behaves differently, including what the diff does not spell out: a default that changed, an order of calls, a value that is now shared.
   Done when: you can state in two sentences what changed, including one behavior change that is not visible in the diff, or "none".

2. **Find the safety fact.** Most changes that look risky are safe because of one fact, such as "this call only drops cache entries that are already dead". Find it. If it holds, most risks clear at once.
   Done when: the safety fact is one sentence, or you wrote that the change rests on more than one and listed them.

3. **Look where grep stops.** See [references/where-grep-stops.md](references/where-grep-stops.md): library source at its pinned version, execution order, data formats on the wire and on disk, other languages reading the same bytes, feature flags, and code a few calls away.
   Done when: every place on that list that applies to this change was checked and noted, and every list item that does not apply is named as skipped.

4. **Rate each risk.** For each risk give how it breaks, the `file:line`, a real likelihood, and a real cost. Keep confirmed risks apart from cleared ones, and give the reason for each cleared one. A search that finds nothing is an answer; an invented caller or API is not.
   Done when: every risk sits in confirmed or cleared, each with a real `file:line`.

5. **Prove the safety fact.** Write a small script or test that calls the real code and fails if the fact is false. Run it and keep the output. Push it to level 5 when the fact is about user-visible behavior and `drive-<app>` exists. When a `prove-<area>` skill covers the code the fact is about, its check run is the proof.
   Done when: the fact reached level 4 or 5 with its command and output, or it is marked `unproven` with the reason.

6. **Widen for a `high` change.** When the task is `high`, spawn two or more subagents, from different model families when available, with the same question and the same diff. Merge their risks; different models catch different real bugs.
   Done when: the task is not `high` and you skipped this step, or every subagent's risks were merged into step 4's lists.

## Output

- **What it does**: the change, including the part that is not obvious.
- **Safety fact**: the sentence, its certainty level, and the command and output that proved it, or `unproven`.
- **Confirmed risks**: how each breaks, `file:line`, likelihood, cost, evidence.
- **Cleared**: what you checked and why it is fine.
- **Catching test**: the cheapest test that would catch the real bug, with its code. The builder adds it to the PR.

Strip secrets and private data before the output goes anywhere public.

## Reply

The output above.
