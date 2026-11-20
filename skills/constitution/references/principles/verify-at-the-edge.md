# verify-at-the-edge

**Apply when** you size verification: how many lanes, how deep, how many cases.

**Rule.** Spend verification where the model is weakest: the hard zones and the high-risk changes. Below that edge, a verifier mostly confirms and costs.

## How

- The risk class and the hard zones in [proof.md](../proof.md) set the depth. A `low` change gets a short proof; a hard zone gets every case and, when it can, a formal check.
- Put the extra effort on the cases a model tends to miss: concurrency, sync, data loss, security, migrations, every entry point of a feature.
- Do not grow verification on a change that is simple and reversible; grow it on one that is not.

## Test

Is the deepest check on the riskiest part of the change?

## Sign it was skipped

Ten screenshots of a label change, and no run on the migration in the same PR.
