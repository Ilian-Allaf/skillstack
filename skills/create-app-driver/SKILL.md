---
name: create-app-driver
description: "Writes the repo's driver, a skill that launches, drives, and observes the app like a user, with its feature map; keeps it in sync."
disable-model-invocation: true
metadata:
  kind: kit
  produces: "repo:drive-<app> skill and feature map, in one PR; in formal mode, repo:prove-<area>"
  hypothesis: "Without a scripted way to drive the real app, agents prove changes with proxies such as green tests, or improvise a new harness every run."
---

# Create app driver

Read [the constitution](../constitution/README.md) first.

Every agent that proves a change needs the same three things: start the app from nothing, use it the way a user does, and capture what happened. This skill writes them once, as a skill inside the target repo, so `prove` in a builder run and the `live` lane in a verifier run drive the app the same way.

You write for an agent that reads the generated skill cold, mid-task, and has never seen the app.

Three modes:

- **create** (default): the repo has no `drive-<app>` skill. Run the steps below.
- **maintain**: the skill exists and the app has changed. Follow [references/maintain.md](references/maintain.md). Run it when the user asks, and after a `learn-from-mistakes` the user approved that found a gap in the feature map.
- **formal**: the repo has a hard zone where tests rarely reach the breaking case. Follow [references/formal.md](references/formal.md) to write `prove-<area>`.

## Steps

1. **Interview the repo, not the user.** Answer five questions from the code: which surface a user touches, how the app runs locally, how an agent can drive it (the repo's own harness first), what can be observed, and whether two instances can run side by side. Ask the user only what the code cannot show, such as a test account.
   Done when: each answer cites a file or a command you ran, and each unknown is a question sent to the user.

2. **Get the base to start.** Run the app from an empty data directory on the base branch, migrations and seed data included. Usable means a user could act, not that a process answers.
   Done when: you reached a usable state and wrote down the ready signal, or you reported the exact blocker and stopped.

3. **Write the skill.** Create `.agents/skills/drive-<app>/SKILL.md`, with the links target-repo.md asks for, from [references/drive-app-template.md](references/drive-app-template.md). Pick the driver from [references/drivers.md](references/drivers.md) only when the repo has no harness of its own. Use the repo's real commands and stable handles (accessible names, test ids, prompt strings, routes). Scripts the skill ships are executable, and the skill shows how to call them.
   Done when: Launch, Doctor, Drive, Evidence, Demo, and Cleanup hold no placeholder, and every command in them ran once.

4. **Seed the feature map.** Find the top 3 to 5 user-facing features from routes, commands, menus, and docs. Write one file each, in the shape of [references/feature-map.md](references/feature-map.md). List every entry point a user has to each feature.
   Done when: every feature file names its entry points, its drive steps, and the observable end state that proves it works.

5. **Prove the generated skill.** Follow its own instructions end to end: launch, doctor, drive one mapped feature, capture evidence, clean up. Then check that the evidence still exists where the skill says. Fix what fails, and run the cleanup after every failed attempt. When a precondition is missing, the journey fails and the reason goes under Gotchas. Never weaken a journey to make it pass.
   Done when: one full run passed, the evidence survived cleanup, and nothing the run started is still running.

6. **Open the PR.** Use [the PR format](../constitution/references/pr-format.md). Proof holds the end to end run and its evidence. Not verified lists the features the map names but this run did not drive.
   Done when: the PR is open with the run's evidence attached, and the user knows to merge it.

## Reply

The surface and driver chosen, the features mapped, the proof run with its evidence path, and what stays unverified.
