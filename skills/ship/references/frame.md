# Frame

Framing costs a message; a misread task costs hours.

## Before you frame

- **Resume what exists.** When a branch or PR for this task already exists, read its state and resume at the first step of `ship` whose Done when fails.
- **Reproduce a bug first.** Drive the symptom the user reported, as the first duty of the [bug-fix playbook](playbooks/bug-fix.md) says, before you write `done_when`.
- **Read the accepted ADRs** whose Applies to covers the code you will touch. A task that goes against one says so in the message, with a superseding ADR for the user to decide: it is a one-way door.
- **Collect the cases** as [coverage.md](../../constitution/references/coverage.md) describes, and the risk class and hard zones as proof.md does.
- **Try the verification setup** as [verification.md](verification.md) describes, before implementation. A failed startup is an environment limit, not the red behavior that proves `done_when`.
- **Build the proof the task lacks, first.** A missing driver for a touched surface, a missing formal check for a promise the user stated in a hard zone, and a formal check stale on the base are built or repaired before the change, by [create-app-driver](../../create-app-driver/SKILL.md), [create-formal-verification](../../create-formal-verification/SKILL.md), and [maintain-formal-verification](../../maintain-formal-verification/SKILL.md), as [proof.md](../../constitution/references/proof.md#drivers-and-formal-checks) and [formal.md](../../constitution/references/formal.md#in-a-task) say. What the team shares lands as the task's first unit, its own PR, stacked under the change as the [bespoke](playbooks/bespoke.md) flow of units does; what stays private is written in place.

## What to send the user

```text
Goal: <what the user wants, in their terms>
Problem: <what is wrong or missing today>
Smallest change: <the least that meets the goal>
Done when: <observable condition>. Ran it on the base: <command> -> <red output>.
Cases: <numbered list: the spec's journeys, promises, and visual targets by their ids (S1, P1, V1), the main case, each entry point, the edge cases of the hard zones; each with its target, a level or a breadth>
Evidence: <demo video, state chart, screenshots, or command output, and why>
Verification setup: <startup runs for builder and verifier, capture command, the driver or formal check built or repaired first, access limits and remedy>
Out of scope: <what this PR will not do>
Risk: <low | medium | high>, because <path or reason>. Hard zones: <list, or none>.
Playbook: <one from the list below>. Seams under test: <public interfaces>.
Design: <none | two sketches | two sketches, shown to you before code>, because <the row of design.md's table>.
Going on now. Stop me, or say "show me the design", at any time.
```

## `done_when`

The rules live in [proof.md](../../constitution/references/proof.md): observable, red on the base, from the user, narrow, shown. A playbook can give `done_when` two parts; [refactoring](playbooks/refactoring.md), [visual-parity](playbooks/visual-parity.md), [perf](playbooks/perf.md), and [hillclimb](playbooks/hillclimb.md) say how.

## Before you build

For a `high` task, or one that touches a hard zone, spawn a fresh verifier to read `done_when` first, as [verify-pr](../../verify-pr/SKILL.md#before-build-read-done_when) describes. Fix what it flags, and show its flags in the frame.

## When the task is unclear

Read the code, the issue, and the history first: most questions answer themselves there. Ask only what is the user's to decide, through the harness's question tool, one question at a time with your recommended answer, and stop asking once you can write an observable `done_when`. When the task needs one design decision first, say so and settle it with the smallest prototype, in the prototype mode of [investigate](../../investigate/SKILL.md). When it needs several decisions, is too big to frame, or is a heavy visual change with no visual target, stop and propose `/shape-spec`: those decisions are the user's.

## Playbooks

Pick one playbook per task, from the first column. A playbook names principles by their id; the rules are in [principles.md](../../constitution/references/principles.md), and you read the full form of one when you apply it.

| Task | Playbook | Ends with |
|---|---|---|
| a behavior is wrong | [bug-fix](playbooks/bug-fix.md) | a PR |
| a behavior is missing, or a screen to build or redesign | [feature](playbooks/feature.md) | a PR |
| the structure changes, the behavior does not | [refactoring](playbooks/refactoring.md) | a PR |
| a path is too slow or uses too much | [perf](playbooks/perf.md) | a PR |
| one metric must reach a target over many attempts | [hillclimb](playbooks/hillclimb.md) | a PR, one commit per kept change |
| the UI must look exactly the same after a migration | [visual-parity](playbooks/visual-parity.md) | a PR per component or batch |
| none of the above: a wide migration, a change in several parts, a long unattended run | [bespoke](playbooks/bespoke.md) | an ordered series of PRs and a decision log |

A task that matches two rows is two units of this task: one PR each, the second stacked on the first, each through steps 2 to 7 of `ship`, then `babysit-pr` once over the stack, as the `bespoke` playbook does. Every playbook ends in a PR. A question, a diagnosis, or a prototype is not a playbook: it is `investigate`.
