# attack-the-premise

**Apply when** two or more fixes that share one premise have failed the same check.

**Rule.** Suspect the premise, not the fixes. Each failed fix is evidence against the belief it assumed.

## How

1. **Write the premise down**: the one sentence every failed fix assumed.
2. **Test it before the next fix.** Find an observation that would come out differently if the premise were false, and make it. Look at how the failures are distributed, not only at how large they are. Make the check rerunnable (`build-the-lever`).
3. **Follow the evidence.** If it contradicts the premise, the cause is elsewhere: look for what the failures share that the premise did not predict. If it confirms the premise, ask the next "why" (`fix-root-causes`); the earlier fixes may have treated a consequence.
4. **Remove the condition instead of compensating for it.** A mechanism that cleans up after the cause leaves the cause in place and adds work on every run.

Do not start the next fix before the premise is written down and tested. Distinct from `redesign-from-first-principles`, which rebuilds a design around a new requirement; this one questions a fact the current design assumes.

## Test

The premise is written, and a run either confirmed or refuted it.

## Sign it was skipped

A third fix in the same place. "This time it should work."
