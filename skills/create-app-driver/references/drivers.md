# Drivers

Fallback recipes, for when the repo has no harness of its own, then how to grow the driver into a small CLI. Prefer what the repo already uses. Copy the recipe into the generated skill and adapt it; the target repo never calls this file. A tool a recipe needs installs as the template's [rules](drive-app-template.md#rules-for-the-generated-skill) say.

## Web app or Electron: a browser driver

- First a ready-made browser control CLI, installed globally, such as Playwright's command line for agents (the `@playwright/cli` package): the skill calls it, with no code to write.
- A small Playwright script the skill ships, for example `scripts/drive.mjs <action> [args]`, only when that CLI cannot do a step, such as recording one clip per case.
- Select by role and accessible name (`getByRole('button', { name: 'Save note' })`) or test id. Never by CSS position, and never by the element refs a snapshot hands out: they change from one run to the next, so a step written with one never replays.
- Evidence: a screenshot and an accessibility snapshot after each step; network responses for the calls that matter; the database row or API state after the action.
- Before and after: run the same journey on the base checkout and the head checkout, on two ports. The driver says from the code whether that works; the first task that needs it proves it.
- Some dev servers lock their checkout, such as Next.js with `.next/dev`: two instances side by side then need a worktree each.
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

It starts with `launch`, `doctor`, `drive`, and `stop`, and gains a command each time a run needs a step it lacks.


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

## Windows hosts

Copy this into the generated skill's Gotchas when the machine runs Windows. Each command was run in Git Bash on Windows 11, with Windows PowerShell 5.1 and PowerShell 7.

- **A detached launch.** `nohup cmd &` gives an MSYS pid that `taskkill` does not know, and can die with the shell when the harness ends its process tree; `cmd //c start //b` is mangled by MSYS. Start the app through PowerShell, with Windows paths, and every handle of the PowerShell call redirected to a file: a child inherits the caller's stdout, so `| tr` or the harness's own pipe never closes and the call hangs.

  ```bash
  RUN="$(cygpath -w "$RUN_DIR")"
  powershell -NoProfile -Command "Start-Process -FilePath '$(cygpath -w "$(command -v node)")' -ArgumentList 'server.js','4791' -WorkingDirectory '$(cygpath -w "$PWD")' -RedirectStandardOutput '$RUN\app.out' -RedirectStandardError '$RUN\app.err' -WindowStyle Hidden -PassThru | ForEach-Object Id" > "$RUN_DIR/app.pid" 2> "$RUN_DIR/launch.err" < /dev/null
  ```

  The process survives the shell. Stop it by the PID in the run directory, tree included: `taskkill //F //T //PID "$(tr -d '\r' < "$RUN_DIR/app.pid")"`. Never by process name.
- **Paths.** A native Windows program (node, python, PowerShell, docker) reads `/c/...` as a missing path: pass `"$(cygpath -w "$path")"`. MSYS also rewrites an argument that looks like a path, such as `/FI`, or the container side of `-v C:\x:/w`: double the slash (`tasklist //FI "PID eq 4"`), or set `MSYS2_ARG_CONV_EXCL='*'` or `MSYS_NO_PATHCONV=1` for that command.
- **PowerShell automatic variables.** Never name a variable `$pid`, `$host`, or `$error`: they are read-only, and the script fails. `$args` and `$input` are reset inside every function and script block. Use `$procId`.
- **Processes and ports.** `ps` lists only MSYS processes; `ps -W`, `tasklist //FI "PID eq <pid>"`, or `Get-Process -Id <pid>` list native ones. For the owner of a port: `netstat -ano | grep ":<port> .*LISTENING"`, or `Get-NetTCPConnection -LocalPort <port> -State Listen | Select-Object -ExpandProperty OwningProcess`.
- **Python.** `python3` can be the Microsoft Store alias, which opens the Store instead of running. Write the driver's small scripts for node, which the app already needs, and give them Windows paths too.
- **Every wait has a timeout.** A ready or doctor loop stops at a deadline and prints the cause, such as the end of the app's log:

  ```bash
  deadline=$((SECONDS+60)); until curl -fsS "http://127.0.0.1:$PORT/" >/dev/null 2>&1; do [ $SECONDS -ge $deadline ] && { echo "not ready after 60s:"; tail -5 "$RUN_DIR/app.err"; exit 1; }; sleep 1; done
  ```
