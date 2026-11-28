# Template for `drive-<app>`

Copy this into `~/.agents/projects/<project>/drive-<app>/SKILL.md`, or, when the user shares it, into the repo at `.agents/skills/drive-<app>/SKILL.md`, linked and routed as [target-repo.md](../../constitution/references/target-repo.md) describes. Replace every `<...>`. The generated skill keeps no `<...>` once written.

```markdown
---
name: drive-<app>
description: "Launch, drive, and observe <app> (<surface>) the way a user does, and capture evidence. Use to prove a change, reproduce a bug, or check a feature by hand."
---

# Verify <app>

Drives the real <app> through <driver>. Every proof uses the user's path, never internal setters or test-only endpoints.

## Preflight

<one read-only command, a few seconds, that checks what the rules below list and stops at the first failure with its fix>

## Launch

Run Preflight first.
<exact command, from an empty data directory, migrations and seed included>
Ready when: <a log line, a prompt, a page that accepts input>.
Isolation: <ports, data dir, profile> that would let two instances run side by side, or "single instance only" and why. Answered from the code; the first task that needs two instances proves it.

## Doctor

<one read-only command>: process up, right build, port owned by this run, auth valid.
Run it before the first drive, after any failed drive, and whenever something looks off.

## Drive

<the harness commands, with this repo's real handles>
Prefer accessible names, test ids, prompt strings, and routes. Never coordinates or tab order.

## Evidence

Capture the action and the state it produced, not only the final screen.
Check side effects too: <rows written, files created, messages sent>.
Save evidence to <path>. Name files <feature>-<entry point>-<step>-<base|head>.<ext>.
Profile, only when the repo has a cheap profiling command: <command that captures a CPU profile, a heap snapshot, or a trace of the running app, and where it writes them>. Otherwise omit this line; the first task that needs a profile adds it.
A dry run proves only what it observably skipped.
Mock only at a boundary the code already has around an outside system, never the app's own database or routes.

## Gotchas

<what this host and this app make go wrong, with the right way; on a Windows host, the Windows hosts section of the drivers reference, adapted; "None known yet." when there is nothing>

## Cleanup

<command> stops what this run started. Never kill by process name.
Evidence stays where Evidence put it.

## Features

The [feature map](features/README.md) lists the user-facing features mapped so far, each with its entry points and the end state that proves it. It grows a few features per maintenance pass, and a task that touches a feature with no file writes it, as the coverage rules say.
A proof that drives one convenient entry point is incomplete when the map lists others.
```

## Rules for the generated skill

- **Preflight fails fast.** Before any install, read-only, in a few seconds, it checks the runtime version the repo pins (such as `engines`, `.nvmrc`, `.node-version`, `.tool-versions`, `volta`, `packageManager`, `.python-version`, `rust-toolchain.toml`) against the one the PATH actually calls, the package manager the lockfile names, that the container daemon answers when Launch needs one, that Launch's ports are free, and that the driver's tools are installed. It stops at the first failure with the cause and the command that fixes it. It never changes the machine: a runtime version the PATH lacks runs through a per-run selector, such as `nvm exec`, `volta run`, or `mise exec`, never by changing the default; with no selector installed, that is a dead end, reported with the command that fixes it. On a Windows host, read [Windows hosts](drivers.md#windows-hosts) first.
- **Start from the repo's own run.** A package script, a Makefile target, the README quickstart, a compose file, or an end-to-end script comes before a launch of your own.
- **Ready means usable.** A database health check can pass while its init scripts still run.
- **A short-lived CLI has no server.** Launch builds the binary once; each drive starts its own isolated session.
- **No demo at creation.** The first task whose coverage requires a demo adds a Demo section that calls the `record-demo` helper, from [drivers.md](drivers.md#a-control-cli).
- **Add a command, not a throwaway script.** When a drive needs a step the CLI lacks, add it as a command with `--help` and JSON output, so the next run reuses it.
- **Scaffolding is marked.** When an unrelated missing asset blocks startup, the skill may create it, labeled as verification scaffolding, and Cleanup removes it.
- **A seed lives with the driver.** A state no user path reaches gets a seed in the driver's `scripts/`: in the project folder for a private driver, in the repo only when the driver already lives there. Never ask where. Launch runs it, and the features that need it say so under Preconditions.
- **The driver's tools live with the driver.** They install in its folder or globally, never in the repo's manifest or lockfile, unless the repo already uses them.
