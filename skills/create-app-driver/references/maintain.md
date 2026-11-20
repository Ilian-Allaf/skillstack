# Maintain mode

A feature map goes stale the moment the app changes. This pass brings `drive-<app>` back in line.

Edit only the `drive-<app>` folder: its SKILL.md, `features/`, and its scripts. Never edit product code here.

## Steps

1. **Index.** Read `features/README.md` and list the feature files. Fix missing, extra, duplicate, or dead entries.
   Done when: the index and the files match one to one.

2. **Source wave.** Spawn one read-only subagent per feature file, all at once. Each explains how the feature works from the source, flags drift from the file with `file:line`, and returns one live recipe. Subagents never drive the app and never edit files.
   Done when: every feature file has a returned summary.

3. **Reconcile.** Merge overlapping recipes into as few app states as practical. Spot-check cited drift. Look at recent merged PRs for user-facing features missing from the map, and name a source path for each one you add.
   Done when: every drift claim is confirmed or dropped, and every new feature has a source path.

4. **Live pass.** Required even when the source looks clean. You alone drive the app, following the skill's own Launch. Drive every feature at least once. Run Doctor before the first drive and after any failed one. Evidence survives every cleanup. Nothing a drive started outlives it.
   Done when: every feature was driven, or marked unreachable with the missing prerequisite and the route tried.

5. **Triage.** A wrong description is drift: fix the file. Working behavior the harness cannot drive is a harness gap: fix the harness and drive it again. Broken app behavior is a product regression: report it to the user and keep it out of this PR.
   Done when: every finding sits in one of the three groups.

6. **Ship or stop.** End on one outcome. `clean`: full coverage, nothing to change, no PR. `changed`: one PR of proven corrections in the PR format. `blocked`: name what blocked the pass.
   Done when: the outcome is reported with the features covered.
