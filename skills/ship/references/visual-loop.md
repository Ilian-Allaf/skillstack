# Target loop

For a spec with visual targets (`V1`, `V2`): passes that close the gap between the head and each target. The `feature` playbook runs it once per kind of target, as its duty 8 says. It is a loop, so rule 7 of the constitution holds.

## Before the first pass: the harness

Build it once, so a pass costs one command, with `drive-<app>`:

1. **A capture per still target**: the screen at its state and width, same framing and size as the target's capture.
2. **A recording per motion target**, at its width, and a frame strip cut from it at the same moments as the target's strip. Each effect's duration is measured on the frames: from the first frame that changes to the first that rests.
3. **A side-by-side image per target**: the target on the left, the head on the right; strips one above the other.
4. **The measured checks** the spec's Visual targets take, from [ui.md](../../constitution/references/ui.md#measured-checks), as commands, and a command for each ban a command can detect. Record their pass 0 numbers.

The targets' files are in the project folder, as the spec names them. Without the recording capability of [harness.md](../../constitution/references/harness.md), a motion target is built from its effect list alone, and its case goes under Not verified with that reason.

## Each pass

1. **Focus.** The user's feedback first, in their words, whether it came in the session or on the PR. Then a failing measured check. Then the lowest criterion of the lowest target.
2. **Fix it in depth.** One focus per pass; independent targets may go to parallel subagents, each in its own worktree.
3. **Capture and measure** with the harness, and look for the spec's bans on each capture.
4. **Score with critics**, a race of at least two on one brief, ranked all, as [parallel.md](../../constitution/references/parallel.md) describes, on the model [harness.md](../../constitution/references/harness.md#model-per-role) gives critics. Each gets only the side-by-side images, the criteria table of ui.md, and, for a motion target, its effect list:

   > Each image shows a target on the left, or on top, and a build beside it, for the first time. Score how close the build is to the target on each criterion, 0 to 10. Then list the three largest gaps per image: where, what is wrong, what to change. End with the weakest area across all images.

   Never tell a critic who built it, how long it took, or your own score. Take the median per criterion; when two critics differ by more than 2 points, add one. With no subagent, the pass goes unscored: the measured checks and the user's feedback alone steer it.
5. **Keep or revert** as [hillclimb](playbooks/hillclimb.md) duty 5 says, with the measured checks as the gate and the critics' spread as the noise.
6. **Log the pass** in the [decision log](../../constitution/references/decision-log.md): the focus, the change, the measured numbers and the medians, kept or reverted.
7. **Show the user** the side-by-side images and one line of what changed, and keep going.

## Stop

The loop ends when the measured checks pass and, after at least three passes, every median clears 8 on each criterion; an unscored loop ends when the measured checks pass and the user's feedback is met. Before the third pass, a high score means the criteria were read too loosely: look again at full size, at the phone width, and at the weakest target.

The target-loop budget is ten passes per kind of target, with rule 7's plateau and premise. When it runs out:
- a measured check still fails: its case fails, and the PR opens `needs-human`, as `ship` says for a spent budget;
- only the medians fall short: the loop stops, and the PR goes on with each target's medians and remaining gaps under Proof, for the user to judge.

## What the PR carries

One row per visual target in the coverage table, with its final side-by-side images and measured numbers, at the level [proof.md](../../constitution/references/proof.md#the-target-of-a-case) gives it. The medians and the decision log are linked under Proof.
