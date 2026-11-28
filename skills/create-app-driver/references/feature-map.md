# Feature map

`features/README.md` indexes one file per user-facing feature mapped so far; the map grows by maintenance. It opens with the rules every recipe shares:

```markdown
# <app> feature map

## Baseline

- <the state every recipe starts from: URL or command, data directory, seed data, tools on PATH>
- Never drive an instance this run did not start.
- Restore the seed data after a recipe changes it.

## Proof

- A screen: an accessibility snapshot and a screenshot that shows it is the right app.
- A command: the command, stdout, stderr, and the exit code.
- A skipped entry point is never reported verified because another path worked.

## Features

- [<Feature>](<feature>.md): <what it covers>
```

Each feature file is written from the user's point of view, with four sections.

```markdown
# <Feature>

<One sentence: what the user can do.>

Last driven: <commit SHA of the last run that drove every entry point below>

## Sub-features

- `<id>` <what it does>

## How to get to it (user POV)

- <every entry point: button, shortcut, command, link, route, import, API call>

## Driving it with drive-<app>

Preconditions: <instance healthy, fixture state, account>.

- **<Step>.** <what the user does>. Run `<command>`. <observable result>.
- **Proof.** <the end state that proves it works, read back from a second view or the stored state>.

## Gotchas

- <what an agent got wrong here, and the right way>
```

## Rules

- **Every entry point counts.** A bug in an entry point the map omits passes every proof. When `learn-from-mistakes` finds such a gap, the missing entry point goes here.
- **The map grows by maintenance.** It starts with a few features. Each maintenance pass checks every file against the source, drives every feature, and maps a few more, so a missing feature is found at the next pass, not by a check.
- **Prove from a second view.** A "saved" toast proves nothing; reopen the item from the list.
- **Record the last drive.** Each run that drives every entry point of a file moves its `Last driven` commit forward. `frame` compares it with the commits that touched the feature's code.
- **Gotchas grow from failures.** Each time an agent fails a journey for a reason the map did not warn about, add it.
- **Features, not pages.** One file per thing a user can do, even when it spans several screens.
