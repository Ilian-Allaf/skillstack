# Target loop

For a task whose spec holds visual targets (`V1`, `V2`): build in rounds until the head holds up next to each target. The `feature` playbook runs it after the layout is built and before motion. The criteria are those of [ui.md](../../constitution/references/ui.md) the spec took.

## Before round 1: the harness

Build it once, so every round costs one command:

1. **One shot per target state**: the screen, its state (empty, filled, error), and its viewport width, as the spec's Visual targets list them, driven with `drive-<app>`.
2. **A capture command** that takes every shot on the head, same framing and size as the target.
3. **A side-by-side image per shot**: target on the left, head on the right.
4. **What a command can measure**: contrast, overflow and tap size at each width, color per region against the target. Record the round 0 numbers.

## Each round

1. **Focus.** The user's open feedback first, in their words. Then the lowest criterion in the lowest shot.
2. **Fix it in depth.** One focus per round; independent shots may go to parallel subagents, each in its own worktree.
3. **Capture and measure** with the harness.
4. **Score with critics.** Spawn at least two fresh subagents, one of another family when available. Give each only the side-by-side images, the criteria, and the bar, with this brief:

   > Each image shows a target on the left and a build on the right, for the first time. Score how close the right is to the left on each criterion, 0 to 10. Then list the three largest gaps per image: where, what is wrong, what to change. End with the weakest area across all images.

   Never tell a critic who built it, how long it took, or your own score. Take the median per criterion; when two critics differ by more than 2 points, add one. With no subagent, a fresh session gets the same inputs; failing that, the round has no score: log it as unscored and let the user's feedback pick the next focus.
5. **Log the round** in the [decision log](../../constitution/references/decision-log.md): the focus and why, what changed, the measured numbers and the critics' medians, each marked measured or judged, and the next focus.
6. **Show the user** the side-by-side images in one line of what changed, and keep going. When the user says the work is lower than the critics do, note the gap and subtract it from every later median.

A round that lowers a median is fixed or reverted before the next one. Commit each kept round.

## Stop

Stop when every shot's median clears the bar on every criterion, after the round floor the spec sets (three rounds when it sets none), and the measured checks pass. Before the floor, a round that scores high means the bar was read too low: look again at full size, at the phone width, and at the weakest shot.

All the rounds count as one build attempt, capped by the round limit the spec sets (ten when it sets none). When the cap is reached below the bar, the PR goes on with each shot's remaining gap under Not verified.

## What the PR carries

The scores steer the build; they prove nothing. The coverage table holds one row per visual target with its final side-by-side images and the measured numbers, at certainty level 5. The medians and the decision log are linked under Proof, as level 1.
