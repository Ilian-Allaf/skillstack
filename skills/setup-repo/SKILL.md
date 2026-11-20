---
name: setup-repo
description: "Prepares a repo the first time you work in it: issue tracker, merge guard, labels, glossary, coding standards, agent file, app driver. Asks before each part."
disable-model-invocation: true
argument-hint: "<nothing, or the parts to run again>"
metadata:
  kind: kit
  calls: "create-app-driver, add-guardrail"
  reads: "shape-spec"
  consumes: "a repo the framework has not worked in, or one to bring up to date"
  produces: "a readiness report, one docs PR, and the PRs of the skills it runs"
  hypothesis: "An agent dropped in a new repo guesses its commands, its words, and its rules, and the first tasks pay for every guess."
---

# Setup repo

Read [the constitution](../constitution/README.md) and [target-repo.md](../constitution/references/target-repo.md) first.

You prepare this repo so every later task starts from facts, not guesses. Each part is offered to the user, never forced. A rerun finds what already exists and does only what is missing.

## Steps

1. **Read the repo.** From the code, not from the user: the languages and the stack, how to install, build, run, and test (run each command once), the linters and the type checker, the CI workflows, the default branch, where the team tracks issues, and the files the repo already has for agents and contributors (`AGENTS.md`, `CLAUDE.md`, `docs/agents/`, `CONTRIBUTING.md`, a style guide, a glossary, ADRs, skills under `.agents/skills/` or a harness folder).
   Done when: each fact cites a file or a command you ran, and each command's result is noted.

2. **Check what the agent can do here.** The code host's CLI is authenticated and the repo has a remote. Then each capability in [harness.md](../constitution/references/harness.md): spawn a subagent, spawn one of another family, wake on a PR change, ask the user a question, block the merge. Try each one; a capability you could not try is "not confirmed", never "works".
   Done when: every capability is listed as works, missing, or not confirmed, with what you tried.

3. **Offer the plan.** Through the harness's question tool, show the user what the repo already has, what is missing, and the parts below, each with what it will write and what it costs. The first part is the issue tracker: recommend the one that matches the remote, and offer the others of [references/trackers/README.md](references/trackers/README.md). The user picks the parts. Parts the repo already has are skipped, unless the user asked to run them again.
   Done when: the user said which parts to run.

4. **Record the issue tracker and install the merge guard.** Write `docs/agents/issue-tracker.md` from the chosen template and prove it with a read-only operation; then create the labels target-repo.md lists, issue labels through that file and PR labels on the code host. Install the hook that blocks merge commands, as [harness.md](../constitution/references/harness.md) describes for this harness, and prove it: a merge on a PR number that does not exist is refused. When the harness cannot block the merge, the report says so.
   Done when: the tracker file answers every operation and its read ran, every label exists, and the hook refused a merge in a run you show, or its absence is in the report.

5. **Draft the glossary.** Follow [references/first-glossary.md](references/first-glossary.md): terms from the code's own names, each checked against how the code uses it. Ask the user only about the terms whose meaning the code leaves open.
   Done when: the draft holds only terms the code uses, and the user settled every open one; or the repo's own glossary was kept and the agent file points to it.

6. **Draft the coding standards.** Follow [references/standards.md](references/standards.md): sort what the repo already does into checks and judgment calls. Mechanical rules go to the report as candidates for `add-guardrail`; only judgment calls go in `CODING_STANDARDS.md`. Name each language of the repo that the constitution has no rules file for yet.
   Done when: every standard is a candidate check or a judgment call with its example, and the user confirmed the judgment calls.

7. **Write the agent file and open the docs PR.** Give `AGENTS.md` the commands from step 1 and the paths of the files above, as target-repo.md describes, and move skills kept in a harness folder if the user chose it. Open one PR in [the PR format](../constitution/references/pr-format.md) with these files and the merge guard's settings if in the repo.
   Then rule 2: a verdict and `babysit-pr`.
   Done when: the docs PR carries `ready` or `needs-human`, or the user chose none of steps 4 to 7.

8. **Build the app driver, if the user chose it.** Run [create-app-driver](../create-app-driver/SKILL.md). It asks for what it needs, such as a test account.
   Done when: its PR is open, or its blocker is in the report, or the user declined it.

9. **Audit the checks, if the user chose it.** Run [add-guardrail](../add-guardrail/SKILL.md) in audit mode. It changes nothing; its proposed corrections join the report, with the candidates from step 6. Launch none of them.
   Done when: the audit report is attached, or the user declined it.

10. **Give the readiness report.** What works, what is missing, and what is not confirmed; the PRs to merge, in order; the corrections proposed; the hard zones you saw, with the formal mode of `create-app-driver` as an option for each; and one first task to try. Start nothing.
    Done when: the report covers every capability of step 2, every part of step 3, and every PR this run opened.

## Reply

The readiness report, the PR links, and the questions still open.
