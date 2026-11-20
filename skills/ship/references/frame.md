# Frame

Framing costs a message; a misread task costs hours.

## Before you frame

- **Resume what exists.** When a branch or PR for this task already exists, read its state and resume at the first step of `ship` whose Done when fails.
- **Reproduce a bug first.** Drive the symptom the user reported, as the first duty of the [bug-fix playbook](playbooks/bug-fix.md) says, before you write `done_when`.
- **Collect the cases** as [coverage.md](../../constitution/references/coverage.md) describes, and the risk class and hard zones as proof.md does.

## What to send the user

```text
Goal: <what the user wants, in their terms>
Problem: <what is wrong or missing today>
Smallest change: <the least that meets the goal>
Done when: <observable condition>. Ran it on the base: <command> -> <red output>.
Cases: <numbered list: the main case, each entry point, the edge cases of the hard zones>
Evidence: <demo video, state chart, screenshots, or command output, and why>
Out of scope: <what this PR will not do>
Risk: <low | medium | high>, because <path or reason>. Hard zones: <list, or none>.
Playbook: <one from the list below>. Seams under test: <public interfaces>.
Go?
```

## `done_when`

The rules live in [proof.md](../../constitution/references/proof.md): observable, red on the base, from the user, narrow, confirmed. A playbook can give `done_when` two parts; [refactoring](playbooks/refactoring.md), [visual-parity](playbooks/visual-parity.md), and [perf](playbooks/perf.md) say how.

## Before the go

Ask through the harness's question tool. For a `high` task, or one that touches a hard zone, spawn a fresh verifier to read `done_when` first, as [verify-pr](../../verify-pr/SKILL.md#before-build-read-done_when) describes, and show the user its flags with the message.

## When the task is unclear

Ask one question at a time, each with your recommended answer. Stop asking once you can write an observable `done_when`. When the task needs one design decision first, say so and settle it with the smallest prototype, in the prototype mode of [investigate](../../investigate/SKILL.md). When it needs several decisions, or is too big to frame, propose running [shape-spec](../../shape-spec/SKILL.md) first.

## Playbooks

Pick one playbook per task, from the first column. A playbook names principles by their id; the rules are in [principles.md](../../constitution/references/principles.md).

| Task | Playbook | Ends with |
|---|---|---|
| a behavior is wrong | [bug-fix](playbooks/bug-fix.md) | a PR |
| a behavior is missing | [feature](playbooks/feature.md) | a PR |
| the structure changes, the behavior does not | [refactoring](playbooks/refactoring.md) | a PR |
| a path is too slow or uses too much | [perf](playbooks/perf.md) | a PR |
| the UI must look exactly the same after a migration | [visual-parity](playbooks/visual-parity.md) | a PR per component or batch |
| none of the above: a wide migration, a change in several parts, a long unattended run | [bespoke](playbooks/bespoke.md) | an ordered series of PRs and a decision log |

A task that matches two rows is two tasks; propose the split. Every playbook ends in a PR. A question, a diagnosis, or a prototype is not a playbook: it is `investigate`.
