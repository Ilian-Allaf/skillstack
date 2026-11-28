---
name: maintain-app-driver
description: "Brings the repo's driver and its feature map back in line with the app, drives every mapped feature live, and maps a few more features each pass."
disable-model-invocation: true
argument-hint: "<a drive-<app> skill, an approved learn-from-mistakes row, or nothing for every driver>"
metadata:
  kind: kit
  reads: "create-app-driver"
  consumes: "the repo's drive-<app> skills, their feature maps, and the commits since each feature was last driven"
  produces: "one outcome per driver (clean, changed, blocked); proven corrections and up to five new feature files, in place or in one PR when shared; each product regression reported"
  hypothesis: "A feature map goes stale the moment the app changes, and a map nobody completes leaves most entry points unproven, while agents trust it as if it were whole."
---

# Maintain app driver

Read [the constitution](../constitution/README.md) first.

A driver starts with a few features. This pass keeps what its feature map says true, and grows the map a few features at a time, so that writing the driver never means mapping the whole app at once. Launch it whenever the app has changed, and after a `learn-from-mistakes` the user approved that found a gap in the map; that row is its argument.

Edit only the `drive-<app>` folder: its SKILL.md, `features/`, and its `scripts/`, the seed included. Never edit product code here, nor a test harness or a seed outside that folder: a gap there is reported like a product regression.

## Outcomes

| Outcome | Means |
|---|---|
| `clean` | every mapped feature was driven, or marked unreachable with a prerequisite its file already names; nothing needed a change; no user-facing feature is missing from the map |
| `changed` | proven corrections, new feature files, or both; the reply lists the features still missing |
| `blocked` | the pass could not finish; say what blocked it |

## Steps

1. **Find the drivers.** Read each `~/.agents/projects/<project>/drive-*/SKILL.md`, following routes into the repo, or the one the user named. With none, stop and point at `/create-app-driver`.
   Done when: you hold the drivers to maintain, or you stopped.

2. **Index.** Read `features/README.md` and list the feature files. Fix missing, extra, duplicate, or dead entries.
   Done when: the index and the files match one to one.

3. **Source wave.** Spawn one read-only subagent per feature file, all at once. Each explains how the feature works from the source, flags drift from the file with `file:line`, lists the entry points the code has and the file lacks, and returns one live recipe. Subagents never drive the app and never edit files.
   Done when: every feature file has a returned summary.

4. **Reconcile.** Merge overlapping recipes into as few app states as practical. Spot-check cited drift. An entry point a mapped feature lacks goes into its file, the one the argument's row named first.
   Done when: every drift claim is confirmed or dropped, and every missing entry point is in its file.

5. **Find what the map lacks, and map a few.** Read where the code declares what a user can reach, such as the router, the command registry, and the menus, and the PRs merged since the oldest `Last driven`. List each user-facing feature with no file, with its source path. Map at most five this pass, in the shape of [feature-map.md](../create-app-driver/references/feature-map.md): first the one the argument's row named, then those the most recent commits touched, then the rest.
   Done when: every missing feature has a source path, and is mapped in this pass or listed in the reply as not mapped yet.

6. **Live pass.** Required even when the source looks clean. You alone drive the app, following the driver's own Launch. Drive every feature at least once, the new ones included. Move a file's `Last driven` to the commit you drove only when you drove every entry point it lists. Run Doctor before the first drive and after any failed drive. Where Doctor cannot see a failure, such as a stuck screen on a healthy process, reset or relaunch. Evidence survives every cleanup, checked where Evidence says. Nothing a drive started outlives it.
   Done when: every feature was driven, or marked unreachable with the missing prerequisite and the route tried; a prerequisite its file did not name is drift, and goes into it.

7. **Triage.** A wrong description is drift: fix the file. Working behavior the driver cannot drive is a harness gap: fix the driver's folder and drive it again; a gap outside that folder is reported, as above. Broken app behavior is a product regression: report it to the user and keep it out of this pass.
   Done when: every finding sits in one of the three groups, and every fix to the driver was driven again.

8. **Ship or stop.** End on one outcome. A private driver takes its changes in place. A shared one takes them in one PR in [the PR format](../constitution/references/pr-format.md), through a verdict and `babysit-pr`, as rule 2 of the constitution says.
   Done when: the outcome is reported with the features covered; or the PR is open in state `ready` or `needs-human`.

## Reply

For each driver: the outcome; the features driven, with the evidence path; the drift and harness gaps fixed; each product regression, with its evidence; the features mapped in this pass; and the features still missing from the map, with their source paths, for the next pass.
