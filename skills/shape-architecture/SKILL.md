---
name: shape-architecture
description: "Puts the architecture choices of a spec to you, two real shapes at a time, and records the ones you make before the build."
disable-model-invocation: true
argument-hint: "<spec issue>"
metadata:
  kind: shaping
  calls: "investigate"
  reads: "shape-spec"
  role: builder
  consumes: "a spec issue"
  produces: "the spec's Technical decisions; the sketches in sketches/<spec>/ of the project folder; ADRs and glossary terms, in place or in a docs PR"
  hypothesis: "Left alone, the builder settles the shape of the code without the user, and a choice the user would have made otherwise shows only in the PR, once it is built."
---

# Shape architecture

Read [the constitution](../constitution/README.md) first, then [architecture.md](../constitution/references/architecture.md), and `~/.agents/projects/<project>/issue-tracker.md`: this skill edits the spec issue. Without that file, read the argument first: a spec in a hosted tracker is read and edited with `setup-repo`'s template for that tracker; otherwise the constitution's row for the tracker file applies.

The spec says what the user wants; you settle how, where the user wants a say. You sketch, the user decides, and `ship` builds within what they decided. What the user leaves open stays the builder's, as it is when this skill never runs. You do not write product code.

## When it is worth it

A run pays when the code the spec touches shows one of these signals. `shape-spec` looks for them before its hand over.

- **A one-way door**, as the glossary defines it.
- **Two viable whole shapes**, with a real trade-off between them.
- **A piece of state that changes owner**, or a new boundary between modules.
- **An accepted ADR** the spec comes close to, or goes against.

Without one, the builder's own design is enough.

## Steps

1. **Read the spec.** The argument names an issue labeled `spec` in the tracker. Without one, such as a file, an idea, or no argument, write nothing: say that no spec exists, give `/shape-spec <idea>` as the next command, and stop. You never write a spec's stories, promises, or `done_when`: only the user's interview in `shape-spec` settles them. Read the spec issue, the repo glossary, and the accepted ADRs whose Applies to covers the code it touches. A spec that a `ship` task is building, with its branch or an open PR, is not reshaped: say so and stop. An open decision of product goes back to `/shape-spec`: you settle how, never what. Take the signals `shape-spec` found in this session; otherwise spawn a fresh subagent to look for them. Go on either way: launching was the go. With none, say so, and that `/ship <issue>` would do.
   Done when: the signals, or their absence, are named to the user, or the user has `/shape-spec` as the next command because no spec issue exists.

2. **Ground and sketch.** Follow steps 1 to 4 of architecture.md, with a fresh subagent to ground, briefed with the notes of the signal scan. Sketch in code: a sketch in prose hides what makes a shape fail. A technical decision the spec already holds is kept by both sketches. A choice a run can settle goes to [investigate](../investigate/SKILL.md) in prototype mode. Save the sketches to `~/.agents/projects/<project>/sketches/<spec>/`, with the full SHA of the base and the modules they touch.
   Done when: two screened sketches are saved with their commit, or the one viable shape is saved with the reason no other is.

3. **Grill the shape.** Put the decisions the sketches carry to the user in rounds, as [references/questions.md](references/questions.md) describes. Keep the repo glossary as shape-spec's [domain.md](../shape-spec/references/domain.md) says.
   Done when: every decision that carries the shape is made by the user, left to the builder, or waits on a product decision sent back to `shape-spec`, and the user confirmed the whole.

4. **Record it.** Check again that no `ship` task is building the spec, then write its Technical decisions as [references/decisions.md](references/decisions.md) shapes them, with the tracker's Edit an issue. ADRs and glossary terms land as domain.md says; a docs PR, when there is one, goes through a verdict and `babysit-pr`, as rule 2 of the constitution says.
   Done when: the issue holds the section, each decision can be checked against a diff, and the issue links the docs PR when there is one.

5. **Hand over.** Give the user the issue link and the next command: `/ship <issue>`, or `/shape-spec <issue>` when step 3 sent a product decision back, with that decision named.
   Done when: the user has the link and the command.

## Reply

The signals found, the decisions made, what is left to the builder, where the sketches are saved, the ADRs and glossary terms written, and what is still open.
