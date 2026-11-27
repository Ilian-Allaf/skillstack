# The target repo

What the framework keeps for the repo it works on, where each piece lives, and who reads it. `setup-repo` creates what is missing; other skills keep it up to date.

The framework works on any repo without imposing a file on the people who share it. Each piece lives in the project folder, on the user's machine, unless the user chose to share it with the team in the repo.

## The project folder

`~/.agents/projects/<project>/`, outside every repo, so every worktree of the repo finds the same files and the team never sees them.

`<project>` comes from `git remote get-url origin`: the path after the host, without `.git`, in lowercase, each `/` replaced by `__`. `https://github.com/Photo-Platform/photo-platform.git` gives `photo-platform__photo-platform`. Without an `origin`, `<project>` is the name of the folder that holds the main checkout, the parent of `git rev-parse --path-format=absolute --git-common-dir`, in lowercase.

## Files

| In the project folder | Shared in the repo at | Holds | Read by |
|---|---|---|---|
| `issue-tracker.md` | `docs/agents/issue-tracker.md` | how to create, read, label, link, block, and close an issue in this repo's tracker, one heading per operation | every skill that touches an issue |
| `issues/` | `.scratch/issues/` | the issues of the markdown tracker, one file each, the default tracker's included | every skill that touches an issue, through the tracker file |
| `glossary.md` and `adr/` | `GLOSSARY.md` and `docs/adr/` | domain terms and hard-to-reverse decisions, in the shape of `shape-spec`'s [domain.md](../../shape-spec/references/domain.md) | `shape-spec`, the builder, the verifier |
| `coding-standards.md` | `CODING_STANDARDS.md` | judgment calls only; a mechanical rule becomes a check instead | the verifier, in the `standards` lane, not the builder |
| `agent-rules.md` | `docs/agent-rules.md` | the rule table of `add-guardrail`: each rule and what enforces it | `add-guardrail`, `learn-from-mistakes`, the verifier |
| `drive-<app>/` and `prove-<area>/` | `.agents/skills/drive-<app>/` and `.agents/skills/prove-<area>/` | the driver and its feature map: how to launch, drive, and observe the app; the formal checks | the builder, the verifier |
| `targets/<spec>/` | never shared | the captures and recordings of a spec's visual targets, saved by `shape-spec` | `ship`, the verifier |
| `access/<app>.md` | never shared | the account, the access, and where the secret lives for a surface, written by `shape-spec` before the driver exists; never the secret itself | `create-app-driver` |

Standards belong to review because the builder carries the most context and the verifier the least.

Only `issue-tracker.md` is required, and it has a default: the first skill that needs an issue and finds none writes it from the private markdown template, [local.md](../../setup-repo/references/trackers/local.md), as the constitution says. Every other entry is created when it has something to hold; a missing one means the project has none yet.

## Routes

An entry the team shares stays in the project folder as a route: a file whose whole content is one line.

```text
This lives in the repo at docs/agents/issue-tracker.md. Read it there instead.
```

A folder entry (`adr/`, `drive-<app>/`) is a route when its only file is such a line, `README.md` for `adr/` and `SKILL.md` for a skill. The path is relative to the repo root, so every worktree resolves it.

- **One hop.** A route points at the repo, never at another route.
- **One home.** An entry is either in the project folder or in the repo, never both: two copies drift. A term the team's glossary lacks goes into the team's file, by PR, or the whole glossary stays private.
- **A broken route stops.** When the path a route names does not exist, say so and ask the user; never fall back to another file.

## Private or shared

`setup-repo` asks, entry by entry, except for `access/<app>.md`, which is never shared since it says where a secret lives. Private is the default: the entry lives in the project folder, is written there directly, and is listed in the reply. Shared: the entry lives in the repo, reaches it through a PR the team reviews, and the project folder holds a route to it.

- **The repo's own files win.** When the repo already has a tracker file, a glossary, standards, ADRs, or a driver, even in another place or another shape, the project folder routes to it instead of creating a second one.
- **The agent file is the team's.** `AGENTS.md` (and `CLAUDE.md`, which imports it with `@AGENTS.md`) is edited only when the user shares an entry and the file needs a pointer to it, by the smallest diff.
- **The merge guard** goes in the user's harness settings when nothing is shared, in the repo's when the user shares it.
- **Labels** live on the code host, so the team sees them. `setup-repo` names them in its plan and creates them only when the user says so. No skill needs them: a PR's state is the State line of its body, and the labels only mirror it.

## Where shared skills and instructions live

A shared entry stays usable by any agent, whatever its provider. Each file has one home, in the cross-agent convention, and harnesses that look elsewhere get a link to it, never a copy.

- **Skills** live in `.agents/skills/<name>/SKILL.md`, the location most agents scan. A harness that reads only its own folder (see the skills row of [harness.md](harness.md)) gets one symlink per skill, for example `.claude/skills/drive-<app>` pointing at `../../.agents/skills/drive-<app>`.
- **Instructions** live in `AGENTS.md`. When the repo also has a `CLAUDE.md`, it keeps its content and gains one line, `@AGENTS.md`, so both files say the same thing.
- **Symlinks on Windows**: git checks a symlink out as a plain text file unless `core.symlinks` is true and the machine allows symlinks. When a link came out as a file, replace it locally with a directory junction and say so in the report; never commit the replacement.

## Rules

- **Create a file only when it has something to hold.** An empty glossary or a standards file with no standard is noise every agent reads.
- **Edit the user's files by the smallest diff.** Add the lines the framework needs; never rewrite or reorder what is there.
- **Every change to the repo goes through a PR** the user merges, like any other. The project folder is the user's own and takes direct writes.

## Labels

The skills read and write these labels where they exist. A PR's `ready` and `needs-human` are first the State line of its body, as [pr-format.md](pr-format.md) says; the PR labels mirror that line, so the team can filter PRs by state, and a skill that finds no such label on the code host writes the line alone. In the markdown tracker, an issue label exists once an issue uses it. `setup-repo` creates the issue labels with the tracker file's "create a label" operation, and the PR labels on the code host (`gh label create <name> --force` on GitHub), once the user agreed.

| Label | Set by | Means |
|---|---|---|
| `ready` | `babysit-pr` | on a PR: it needs nothing but the user's merge |
| `needs-human` | `ship`, `babysit-pr`, `ship-queue` | on a PR: the run stopped and needs a decision |
| `escaped` | the user | a bug found after merge |
| `spec` | `shape-spec` | an issue that holds a spec |
| `map` | `shape-spec` | an issue that charts decisions for a large effort |
| `decision:grill`, `decision:prototype`, `decision:research`, `decision:task` | `shape-spec` | the type of a decision issue on a map |
