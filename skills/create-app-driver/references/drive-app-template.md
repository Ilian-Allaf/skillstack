# Template for `drive-<app>`

Copy this into the target repo at `.agents/skills/drive-<app>/SKILL.md`, link it for the harnesses that need it as [target-repo.md](../../constitution/references/target-repo.md) describes, and replace every `<...>`. The generated skill keeps no `<...>` once written.

```markdown
---
name: drive-<app>
description: "Launch, drive, and observe <app> (<surface>) the way a user does, and capture evidence. Use to prove a change, reproduce a bug, or check a feature by hand."
---

# Verify <app>

Drives the real <app> through <driver>. Every proof uses the user's path, never internal setters or test-only endpoints.

## Launch

<exact command, from an empty data directory, migrations and seed included>
Ready when: <a log line, a prompt, a page that accepts input>.
Isolation: <ports, data dir, profile> so two instances can run side by side, or "single instance only" and why.

## Doctor

<one read-only command>: process up, right build, port owned by this run, auth valid.
Run it before the first drive, after any failed drive, and whenever something looks off.

## Drive

<the harness commands, with this repo's real handles>
Prefer accessible names, test ids, prompt strings, and routes. Never coordinates or tab order.

## Evidence

Capture the action and the state it produced, not only the final screen.
Check side effects too: <rows written, files created, messages sent>.
Save evidence to <path>. Name files <feature>-<step>-<base|head>.<ext>.
Profile: <command that captures a CPU profile, a heap snapshot, or a trace of the running app, and where it writes them>.
A dry run proves only what it observably skipped.

## Demo

`<record-demo command> <cases file>` records each case as its own clip, then assembles the demo video with a caption per case and prints the chapter list.
It fails when a case in the file has no clip.

## Cleanup

<command> stops what this run started. Never kill by process name.
Evidence stays where Evidence put it.

## Features

The [feature map](features/README.md) lists every user-facing feature, its entry points, and the end state that proves it.
A proof that drives one convenient entry point is incomplete when the map lists others.
```

## Rules for the generated skill

- **Ready means usable.** A database health check can pass while its init scripts still run.
- **A short-lived CLI has no server.** Launch builds the binary once; each drive starts its own isolated session.
- **Scaffolding is marked.** When an unrelated missing asset blocks startup, the skill may create it, labeled as verification scaffolding, and Cleanup removes it.
