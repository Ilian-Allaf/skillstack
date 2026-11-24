---
name: shape-spec
description: "Turns a loose idea into a spec issue through an interview, or into a map of decisions when the work is too big for one session."
disable-model-invocation: true
argument-hint: "<idea, issue number, or map issue>"
metadata:
  kind: shaping
  calls: "investigate"
  role: builder
  consumes: "a loose idea, a conversation, or a map issue"
  produces: "a spec issue labeled spec, or a map issue labeled map with its decision issues"
  hypothesis: "Without a spec, the builder under-scopes the work; without an interview, the spec carries the agent's guesses instead of the user's decisions."
---

# Shape spec

Read [the constitution](../constitution/README.md) first, and `~/.agents/projects/<project>/issue-tracker.md`: this skill publishes to the tracker, so without that file it stops and asks the user to run `/setup-repo`.

You turn what the user wants into decisions, then into a spec. You do not write product code. The spec is product-level: a technical error in a spec cascades through the whole build, so the spec names behavior and decisions, not files.

You do not cut the spec into implementation slices for parallel agents. One builder carries the spec; when it is large, the builder lands it as an ordered series of PRs with the `bespoke` playbook. Work that looks independent turns out tangled, and only a builder holding the whole spec sees how.

## Steps

1. **Pick the mode.** From what the user brings:
   - a loose idea, or a plan with open decisions: **grill**, then **spec**;
   - a conversation that already settled the decisions: **spec** directly;
   - work too big for one session, where the way to the goal is not visible yet: **map**;
   - a map issue: **map**, working its next decision.

   A question of fact a run can answer, such as a timing or whether an approach works, is not the user's to decide: run [investigate](../investigate/SKILL.md) in prototype mode, and the observation decides. A question of look or feel gets a prototype too, but the user picks from its variants.
   Done when: the mode is named to the user with the reason.

2. **Grill.** Interview the user in rounds, as [references/grill.md](references/grill.md) describes, and keep the repo's domain model up to date as [references/domain.md](references/domain.md) describes. Facts are your job; decisions are the user's.
   Done when: no open decision is left, every story has a journey and every promise its harm, confirmed by the user, the drivers and formal checks of the area are looked up, the access for any surface without a driver is written down, every resolved term is in the repo glossary, and the user confirmed you share the same understanding.

3. **Write the spec.** Follow [references/spec.md](references/spec.md): problem, solution, `done_when` agreed with the user, user stories with their journeys, promises, what is not verifiable, the seams to test at, decisions, testing decisions, out of scope. Check the seams with the user, then publish it as an issue labeled `spec`.
   The docs PR goes through a verdict and `babysit-pr`, as rule 2 of the constitution says.
   Done when: the issue exists and links the docs PR that holds the glossary terms and ADRs, the user approved the seams, and every numbered journey and promise can become a case in `frame`.

4. **Map.** For work too big for one session, chart or work the map as [references/map.md](references/map.md) describes. Resolve at most one decision per session, except research.
   Done when: charting: the map issue and its first decision issues exist, wired by blocking links. Working: one decision is resolved, recorded on the map, and the fog it cleared is turned into new decision issues.

5. **Hand over.** When the spec is ready, give the user the issue link and the next command: `/ship <issue>`. A spec too large for one PR names the `bespoke` playbook. A finished map hands over its destination: usually a spec, sometimes a decision.
   Done when: the user has the link and the next command.

## Reply

The mode, the decisions made and who made them, the terms added to the glossary, the ADRs written, the drivers and formal checks found (stale ones named) and the access collected, the spec or map link, and what is still open.
