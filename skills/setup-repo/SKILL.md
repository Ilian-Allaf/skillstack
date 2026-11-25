---
name: setup-repo
description: "Prepares a repo the first time you work in it: issue tracker, merge guard, labels, glossary, coding standards, language rules, app driver. Keeps each private or shares it with the team, as asked."
disable-model-invocation: true
argument-hint: "<nothing, or the parts to run again>"
metadata:
  kind: kit
  calls: "create-app-driver, add-guardrail"
  reads: "shape-spec"
  consumes: "a repo the framework has not worked in, or one to bring up to date"
  produces: "a readiness report, the project folder, a docs PR for what the user shares, and the PRs of the skills it runs"
  hypothesis: "An agent dropped in a new repo guesses its commands, its words, and its rules, and the first tasks pay for every guess."
---

# Setup repo

Read [the constitution](../constitution/README.md) and [target-repo.md](../constitution/references/target-repo.md) first.

You prepare this repo so every later task starts from facts, not guesses, and impose no file on its team. A rerun finds what already exists and does only what is missing.

## Steps

1. **Read the repo.** From the code, not from the user: the languages and the stack, how to install, build, run, and test (run each command once), the linters and the type checker, the CI workflows, the default branch, where the team tracks issues, and the files the repo already has for agents and contributors (`AGENTS.md`, `CLAUDE.md`, `docs/agents/`, `CONTRIBUTING.md`, a style guide, a glossary, ADRs, skills under `.agents/skills/` or a harness folder).
   Done when: each fact cites a file or a command you ran, and each command's result is noted.

2. **Check what the agent can do here.** The code host's CLI is authenticated and the repo has a remote. Then each capability in [harness.md](../constitution/references/harness.md): spawn a subagent, spawn one of another family, wake on a PR change, ask the user a question, block the merge. Try each one; a capability you could not try is "not confirmed", never "works".
   Done when: every capability is listed as works, missing, or not confirmed, with what you tried.

3. **Offer the plan.** Through the harness's question tool, show the user what the repo already has, what is missing, and the parts below, each with what it will write and what it costs. The first part is the issue tracker: recommend the one that matches the remote, and offer the others of [references/trackers/README.md](references/trackers/README.md). Each file part is private or shared, as target-repo.md says. Language rules: [references/language-rules.md](references/language-rules.md). The user picks. Parts the project folder already has are skipped, unless the user asked to run them again.
   Done when: the user said which parts to run.

4. **Record the issue tracker and install the merge guard.** Write `~/.agents/projects/<project>/issue-tracker.md` from the chosen template, or a route, and prove it with a read-only operation; then create the labels the user agreed to, issue labels through that file and PR labels on the code host. Install the hook that blocks merge commands, as [harness.md](../constitution/references/harness.md) describes for this harness, and prove it: a merge on a PR number that does not exist is refused.
   Done when: the tracker file answers every operation and its read ran, every label the user agreed to exists, and the hook refused a merge in a run you show, or its absence is in the report.

5. **Draft the glossary.** Follow [references/first-glossary.md](references/first-glossary.md): terms from the code's own names, each checked against how the code uses it. Ask the user only about the terms whose meaning the code leaves open.
   Done when: the draft holds only terms the code uses, and the user settled every open one; or it routes to the repo's own glossary.

6. **Draft the coding standards.** Follow [references/standards.md](references/standards.md): sort what the repo already does into checks and judgment calls. Mechanical rules go to the report as candidates for `add-guardrail`; only judgment calls go in the coding standards. Name each language of the repo that the constitution has no rules file for yet.
   Done when: every standard is a candidate check or a judgment call with its example, and the user confirmed the judgment calls.

7. **Write the files, and open the docs PR for what is shared.** Write each part where target-repo.md puts it; for shared parts, `AGENTS.md` gains the commands from step 1. Open one PR in [the PR format](../constitution/references/pr-format.md) with the shared files and the merge guard's settings if in the repo.
   Then rule 2: a verdict and `babysit-pr`.
   Done when: every part chosen is written, and every route resolves; and the docs PR carries `ready` or `needs-human`, or nothing was shared.

8. **Build the app driver, if the user chose it.** Run [create-app-driver](../create-app-driver/SKILL.md). It asks for what it needs, such as a test account.
   Done when: it reported its driver or its PR, or its blocker is in the report, or the user declined it.

9. **Audit the checks, if the user chose it.** Run [add-guardrail](../add-guardrail/SKILL.md) in audit mode. It changes nothing; its proposed corrections join the report, with the candidates from step 6.
   Done when: the audit report is attached, or the user declined it.

10. **Give the readiness report.** What works, what is missing, and what is not confirmed; the PRs to merge, in order; the corrections proposed; the hard zones you saw, with `/create-formal-verification` as an option for each; and one first task to try. Start nothing.
    Done when: the report covers every capability of step 2, every part of step 3, and every PR this run opened.

## Reply

The readiness report, the project folder with each entry private or routed, the PR links, and the questions still open.
