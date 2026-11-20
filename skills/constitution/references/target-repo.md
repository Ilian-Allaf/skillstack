# The target repo

What the framework keeps in the repo it works on, and who reads each piece. `setup-repo` creates what is missing; other skills keep it up to date.

## Files

| File | Holds | Read by |
|---|---|---|
| `docs/agents/issue-tracker.md` | how to create, read, label, link, block, and close an issue in this repo's tracker, one heading per operation | every skill that touches an issue |
| `AGENTS.md` | a few navigation pointers, nothing more: how to build and test, and where the files below are; every agent pays for each line | every agent |
| `docs/agent-rules.md` | the rule table of `add-guardrail`: each rule and what enforces it; the agent file points to it in one line | `add-guardrail`, `learn-from-mistakes`, the verifier |
| `CODING_STANDARDS.md` | judgment calls only; a mechanical rule becomes a check instead | the verifier, in the `standards` lane, not the builder |
| the repo glossary (`GLOSSARY.md`, or the file `AGENTS.md` names) and `docs/adr/` | domain terms and hard-to-reverse decisions, in the shape of `shape-spec`'s [domain.md](../../shape-spec/references/domain.md) | `shape-spec`, the builder, the verifier |
| `.agents/skills/drive-<app>/` and its feature map | how to launch, drive, and observe the app; every user-facing feature and its entry points | the builder, the verifier |

Standards belong to review because the builder carries the most context and the verifier the least.

## Where skills and instructions live

The repo stays usable by any agent, whatever its provider. Each file has one home, in the cross-agent convention, and harnesses that look elsewhere get a link to it, never a copy: two copies drift.

- **Skills** live in `.agents/skills/<name>/SKILL.md`, the location most agents scan. A harness that reads only its own folder (see the skills row of [harness.md](harness.md)) gets one symlink per skill, for example `.claude/skills/drive-<app>` pointing at `../../.agents/skills/drive-<app>`.
- **Instructions** live in `AGENTS.md`. When the repo also has a `CLAUDE.md`, it keeps its content and gains one line, `@AGENTS.md`, so both files say the same thing.
- **Symlinks on Windows**: git checks a symlink out as a plain text file unless `core.symlinks` is true and the machine allows symlinks. When a link came out as a file, replace it locally with a directory junction and say so in the report; never commit the replacement.

## Rules

- **Create a file only when it has something to hold.** An empty glossary or a standards file with no standard is noise every agent reads.
- **The repo's own files win.** When the repo already has a glossary, a style guide, or a contributing guide, point to it from the agent file instead of creating a second one.
- **Edit the user's files by the smallest diff.** Add the lines the framework needs; never rewrite or reorder what is there.
- **Every change goes through a PR** the user merges, like any other.

## Labels

The skills read and write these labels. `setup-repo` creates the issue labels with the tracker file's "create a label" operation, and the PR labels on the code host (`gh label create <name> --force` on GitHub).

| Label | Set by | Means |
|---|---|---|
| `ready` | `babysit-pr` | on a PR: it needs nothing but the user's merge |
| `needs-human` | `ship`, `babysit-pr`, `ship-queue` | on a PR: the run stopped and needs a decision |
| `escaped` | the user | a bug found after merge |
| `spec` | `shape-spec` | an issue that holds a spec |
| `map` | `shape-spec` | an issue that charts decisions for a large effort |
| `decision:grill`, `decision:prototype`, `decision:research`, `decision:task` | `shape-spec` | the type of a decision issue on a map |
