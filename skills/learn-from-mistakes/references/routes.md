# Routes

Where a lesson goes, by the layer that should have caught the mistake.

## By layer

| The mistake got through because | The layer | Route |
|---|---|---|
| the code allowed it | the code itself | `/add-guardrail`: architecture, a type, a lint whose message names the fix, a test |
| `done_when` did not describe what the user wanted | the contract | `ship`'s [frame.md](../../ship/references/frame.md), or `shape-spec` if the task needed decisions first |
| no case covered that path | coverage | the feature map, through `create-app-driver` in maintain mode, and the case list rules in [coverage.md](../../constitution/references/coverage.md) |
| the proof drove the app the wrong way | proof on the app | the target repo's `drive-<app>` skill |
| the change broke something outside its diff | breakage | the `analyze-impact` skill |
| a formal check covered the code and passed, or its property missed the case | formal check | `/maintain-formal-verification` when the check was stale or its model wrong; `/create-formal-verification` for a property no check holds |
| the verifier saw it and passed it, or never tried it | the verifier | an example in [calibration.md](../../verify-pr/references/calibration.md), and the lane that should have tried it; replayed until a fresh verifier gives the missed FAIL |
| a skill guided the agent badly, or did not fire | the framework | a PR on that skill, in its own PR, never inside a task |
| the repo has no hook or CI running its checks | guardrails | a `/add-guardrail` PR that wires them |

## Files in the target repo

Which file a lesson lands in, and who reads it, is in [target-repo.md](../../constitution/references/target-repo.md). A mechanical rule becomes a check through `add-guardrail`; only a judgment call goes in `coding-standards.md` of the project folder.
