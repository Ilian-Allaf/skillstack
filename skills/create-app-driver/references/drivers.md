# Drivers

Fallback recipes, for when the repo has no harness of its own, then how to grow the driver into a small CLI. Prefer what the repo already uses. Copy the recipe into the generated skill and adapt it; the target repo never calls this file.

## Web app or Electron: a browser driver

- Playwright, driven by a small script the skill ships, for example `scripts/drive.mjs <action> [args]`.
- Select by role and accessible name (`getByRole('button', { name: 'Save note' })`) or test id. Never by CSS position.
- Evidence: a screenshot and an accessibility snapshot after each step; network responses for the calls that matter; the database row or API state after the action.
- Before and after: run the same journey on the base checkout and the head checkout, on two ports.
- Video: open the browser context with `recordVideo: { dir, size }`; Playwright writes one video per page when the context closes. Record each case in its own context, so each case is its own clip.

## CLI or TUI: a terminal session

- One fresh PTY or tmux session per drive, so a hung prompt never leaks into the next one.
- Send keys, wait for a prompt string, then capture the pane.
- Evidence: the full transcript, the exit code, and any file the command wrote.
- Pin what makes output vary: time zone, locale, terminal width, color.
- Video: record the session with a terminal recorder (asciinema, or a scripted one such as vhs), one recording per case.

## HTTP service or API

- `curl` or a small script, against a local instance on a port the run owns.
- Evidence: the request, the status, the response body, and the stored state read back.
- External systems stay behind the boundary the code already has. Mock only there.

## Library

- A script that imports the package the way a user does, from its public entry point, and calls the changed function.
- Evidence: the script, its output, and the version or commit it ran against.

## A control CLI

When the drive takes more than a few lines of script, or agents keep writing throwaway scripts to click through the app, grow the script the skill ships into a small control CLI (`build-the-lever`). Every run then drives the app the same way, for fewer tokens, and the evidence replays. A CLI agents use well has:

- a few composable commands that each do real work, such as `launch`, `drive <feature>`, `capture`, `reset`, rather than many thin ones;
- `--dry-run` on anything that deletes or writes outside the run's own directory;
- `--help` on every command, with an example;
- machine-readable output, such as JSON, beside the human one;
- errors that say what to do next: "port 3000 is taken; pass --port or run `reset`";
- one command that brings the environment up the same way every time: dependencies, migrations, seed data, test users.


A helper `record-demo` turns the per-case clips into one video, as [coverage.md](../../constitution/references/coverage.md) describes:

- concatenate the clips in the coverage table's order, base before head for a bug;
- burn a caption strip under each clip with its case number, the case, and the expected result, readable at chat size;
- speed up idle waits, and print each chapter's start time so the PR can list them;
- write the video and a chapter list next to the other evidence.

`ffmpeg` does all four. The helper takes the case list as input and fails when a case has no clip.

## Mobile

- Simulator or emulator driven by the platform's UI test tool.
- Video: the simulator's own screen recording, one clip per case.
- This is the hardest surface. When the repo has no harness, report that and agree a scope with the user before writing one.
