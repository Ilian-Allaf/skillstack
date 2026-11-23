---
name: create-app-driver
description: "Writes the repo's driver, a skill that launches, drives, and observes the app like a user, with its feature map; keeps it in sync."
disable-model-invocation: true
metadata:
  kind: kit
  produces: "repo:drive-<app> skill and feature map, in the project folder or in one PR when shared"
  hypothesis: "Without a scripted way to drive the real app, agents prove changes with proxies such as green tests, or improvise a new harness every run."
---

# Create app driver

Read [the constitution](../constitution/README.md) first.

Every agent that proves a change needs the same three things: start the app from nothing, use it the way a user does, and capture what happened. This skill writes them once, as a skill in the project folder, or in the repo when the user shares it with the team, so `prove` in a builder run and the `live` lane in a verifier run drive the app the same way.

You write for an agent that reads the generated skill cold, mid-task, and has never seen the app.

Two modes:

- **create** (default): the repo has no `drive-<app>` skill. Run the steps below.
- **maintain**: the skill exists and the app has changed. Follow [references/maintain.md](references/maintain.md). Run it when the user asks, and after a `learn-from-mistakes` the user approved that found a gap in the feature map.

## Steps

1. **Interview the repo, not the user.** Answer five questions from the code: which surface a user touches, how the app runs locally, how an agent can drive it (the repo's own harness first), what can be observed, and whether two instances can run side by side. Ask the user only what the code cannot show, such as a test account.
   Done when: each answer cites a file or a command you ran, and each unknown is a question sent to the user.

2. **Get the base to start.** Run the app from an empty data directory on the base branch, migrations and seed data included. Usable means a user could act, not that a process answers.
   Done when: you reached a usable state and wrote down the ready signal, or you reported the exact blocker and stopped.

3. **Write the skill.** Create `~/.agents/projects/<project>/drive-<app>/SKILL.md`, or, when the user shares it, `.agents/skills/drive-<app>/SKILL.md` in the repo with the links and the route [target-repo.md](../constitution/references/target-repo.md) asks for, from [references/drive-app-template.md](references/drive-app-template.md). Pick the driver from [references/drivers.md](references/drivers.md) only when the repo has no harness of its own. Use the repo's real commands and stable handles (accessible names, test ids, prompt strings, routes). Scripts the skill ships are executable, and the skill shows how to call them; when the drive outgrows a few lines, make it a small control CLI, as [references/drivers.md](references/drivers.md#a-control-cli) describes.
   Done when: Launch, Doctor, Drive, Evidence, Demo, and Cleanup hold no placeholder, and every command in them ran once.

4. **Seed the feature map, and its check.** Find the top 3 to 5 user-facing features from routes, commands, menus, and docs, and write one file each in the shape of [references/feature-map.md](references/feature-map.md). Where the code declares entry points, add a check that fails when one has no feature file, and see it fail once by hiding a file. A shared driver runs the check in CI; a private one ships it as a script its Doctor runs.
   Done when: every feature file names where its entry points are declared, the ones no file declares, its drive steps, and the end state that proves it; and the check failed once and passes, or the report says the code declares no entry points.

5. **Prove the generated skill.** Follow its own instructions end to end: launch, doctor, drive one mapped feature, capture evidence, clean up. Then check that the evidence still exists where the skill says. Fix what fails, and run the cleanup after every failed attempt. When a precondition is missing, the journey fails and the reason goes under Gotchas. Never weaken a journey to make it pass.
   Done when: one full run passed, the evidence survived cleanup, and nothing the run started is still running.

6. **Hand it over.** A private driver is done once step 5 passed: report its path. A shared one goes in a PR in [the PR format](../constitution/references/pr-format.md). Proof holds the end to end run and its evidence. Not verified lists the features the map names but this run did not drive.
   Then get a verdict and run `babysit-pr`, as rule 2 of the constitution says.
   Done when: the private driver's run is reported with its evidence; or the PR is open with the run's evidence attached, and carries `ready` or `needs-human`.

## Reply

The surface and driver chosen, the features mapped, the proof run with its evidence path, and what stays unverified.
