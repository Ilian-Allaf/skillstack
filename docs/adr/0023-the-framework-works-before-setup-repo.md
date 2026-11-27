# 0023. The framework works before setup-repo

- **Status**: accepted, 2026-11-27
- **Applies to**: `skills/constitution/README.md` (rule 8 and the tracker file), `skills/constitution/references/target-repo.md`, `skills/constitution/references/pr-format.md`, `skills/setup-repo/`, every skill that reads or writes an issue or a PR's state
- **Enforced by**: review

## Context

The skills assumed `setup-repo` had run. Most first runs start with `/ship`, and on a repo nobody prepared two things broke:

- **No tracker file.** `shape-spec` and `learn-from-mistakes` stopped. The other skills listed the issues they would have opened in a reply that dies with the session, and the steps whose Done when needs an issue (a `MUST KILL`, a confirmed risk) could never pass.
- **No PR labels.** A PR's state lived only in the labels `ready` and `needs-human`, which do not exist on a fresh code host. Adding one fails, and creating one puts a label the team did not choose on its repo, which [ADR 0016](0016-the-working-files-live-outside-the-repo.md) rules out.

## Decision

- **A default tracker.** When `issue-tracker.md` is missing from the project folder, the first skill that needs an issue writes it from the markdown template, private: issues live in `~/.agents/projects/<project>/issues/`, one file each, numbered across the repo like a hosted tracker's. The file's first line marks it as written without `setup-repo`, and the skill says so in its reply. `setup-repo` treats a marked file as a tracker nobody chose: it proposes the one that matches the remote, and moves the open issues when the user picks another.
- **The PR's state is a line of its body.** The Risk section of the PR format gains `State: ready` or `State: needs-human, <what it waits on>`, beside the Verdict line. Skills read and write that line. The labels `ready` and `needs-human` mirror it when they exist on the code host, so the team can filter PRs by state; a skill never creates them.
- **The merge guard has no default.** It is a harness setting the user installs. `ship`'s frame says when it is missing, and the run goes on.

## Alternatives rejected

- **The default tracker in the repo, under `.scratch/`**: it imposes files on the team, against ADR 0016. It stays the shared variant of the same template.
- **GitHub Issues as the default**: it needs an authenticated `gh` and issues enabled, and the team sees every issue.
- **Creating the labels on first use**: labels are created only with the user's consent (ADR 0016).
- **The draft status as the state**: many review bots and some CI skip drafts, so `babysit-pr` would wait on reviews that never come, and a draft cannot tell a run in progress from one that waits on the user.
- **Stopping and asking for `/setup-repo`**: a launched task runs to a PR (rule 11 of the constitution), and setup is a choice, not a toll.

## Consequences

- [ADR 0009](0009-the-issue-tracker-is-agnostic.md) still holds: the tracker file is the contract. `setup-repo` is no longer its only writer.
- Private issues are invisible to the team, to a cloud session, and to CI, like every private entry. A PR names no private issue, since its readers cannot open it.
- Filtering the PR list by state needs the labels, which `setup-repo` creates when the user agrees.
- A PR opened before this ADR has no State line; its label is its state until a skill writes the line.
