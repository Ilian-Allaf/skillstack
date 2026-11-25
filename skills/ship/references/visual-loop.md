# Target loop

For a spec with visual targets (`V1`, `V2`): passes that close the gap between the head and each target. The `feature` playbook runs it on the still targets once the stills are built, then on the motion targets once motion is built. It is a loop, so rule 7 of the constitution holds: a budget, and a plateau changes the approach.

## Before the first pass: the harness

Build it once, so a pass costs one command, with `drive-<app>`:

1. **A capture per still target**: the screen at its state and width, same framing and size as the target's capture.
2. **A recording per motion target**, at its width, and a frame strip cut from it at the same moments as the target's strip.
3. **A side-by-side image per target**: the target on the left, the head on the right; strips one above the other.
4. **The measured checks** the spec's Visual targets take, from [ui.md](../../constitution/references/ui.md#measured-checks), as commands. Record their pass 0 numbers.

## Each pass

1. **Focus.** The user's open feedback first, in their words. Then the lowest criterion of the lowest target.
2. **Fix it in depth.** One focus per pass; independent targets may go to parallel subagents, each in its own worktree.
3. **Capture and measure** with the harness.
4. **Score with critics**, a race of at least two on one brief, ranked all, as [parallel.md](../../constitution/references/parallel.md) describes, on the model [harness.md](../../constitution/references/harness.md#model-per-role) gives critics. Each gets only the side-by-side images, the criteria table of ui.md, and, for a motion target, its effect list:

   > Each image shows a target on the left, or on top, and a build beside it, for the first time. Score how close the build is to the target on each criterion, 0 to 10. Then list the three largest gaps per image: where, what is wrong, what to change. End with the weakest area across all images.

   Never tell a critic who built it, how long it took, or your own score. Take the median per criterion; when two critics differ by more than 2 points, add one. With no subagent, the pass goes unscored: the user's feedback picks the next focus.
5. **Keep or revert.** Keep the pass when no median falls by more than the critics' spread and the measured checks hold; otherwise revert it in full. Commit each kept pass.
6. **Log the pass** in the [decision log](../../constitution/references/decision-log.md), one row: the focus, the change, the measured numbers and the medians, kept or reverted.
7. **Show the user** the side-by-side images and one line of what changed, and keep going. When the user rates the work lower than the critics, log the gap, and lower every later median by it.

## Stop

Stop when the measured checks pass and every median clears the stop score, 8 on each criterion, after at least three passes. Before the third, a pass that scores high means the criteria were read too loosely: look again at full size, at the phone width, and at the weakest target.

The budget is ten passes for the stills and ten for motion. Two passes in a row with no median moving past the spread are a plateau: change the approach, such as another reference, another layout, or another effect. When the budget runs out below the stop score, the build budget is spent: the PR opens `needs-human`, as `ship` says, with each target's remaining gap.

## What the PR carries

One row per visual target in the coverage table, with its final side-by-side images and measured numbers, at the level [proof.md](../../constitution/references/proof.md#the-target-of-a-case) gives it. The medians and the decision log are linked under Proof.
