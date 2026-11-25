# Source — `cook`

Research record, imported on 2026-11-25. This source is reference material, not framework instructions.

| Field | Value |
|---|---|
| Type | Skill repository |
| Title | cook |
| Author | Leon Lin (Leonxlnx) |
| URL | <https://github.com/Leonxlnx/cook> |
| Imported revision | `b23cac6fd9439dfddcab61b14808e7bf72549b46` |
| Revision date | 2026-10-31 |
| Imported on | 2026-11-25 |
| License | MIT, Copyright (c) 2026 Leon Lin. See [`repo/LICENSE`](repo/LICENSE). |
| Local snapshot | [`repo/`](repo), full, `.git` excluded |
| Catalog | [`catalog.json`](catalog.json) · [`SKILLS-INDEX.md`](SKILLS-INDEX.md) |
| Skills | 1 |

## Why this source

Cook turns the method in the [Taste Skill video](../../videos/2026-11-20-taste-skill-lessons-eric-tech/SOURCE.md) into one loop: a target, a bar, and time. It is the primary source for lessons 1 to 5, 7 and 8 of that video.

## What to read

| File | What it holds |
|---|---|
| [`SKILL.md`](repo/SKILL.md) | The loop: intake, target, bar, rules, time, rounds, gate, ship, stop check |
| [`references/intake.md`](repo/references/intake.md) | One message with every open question and a default for each; "no idea yet" and "no references yet" paths |
| [`references/target-and-bar.md`](repo/references/target-and-bar.md) | References as the minimum bar, the shot list (for UI, one screen state at a fixed viewport), the rubric, calibration, measured against eyeballed numbers |
| [`references/loop-and-critics.md`](repo/references/loop-and-critics.md) | Choosing the focus, zero-context critics on side-by-side images, median and disagreement, user feedback, pacing |
| [`references/rules.md`](repo/references/rules.md) | The slop ban list, color, detail |
| [`templates/ROUNDS.md`](repo/templates/ROUNDS.md) | The round ledger |
| [`scripts/side-by-side.mjs`](repo/scripts/side-by-side.mjs) | Reference left, render right, one row per shot |

## Caveats

Cook targets 3D worlds, films and launch videos first; UI is one case among them. Several of its choices conflict with our decisions: run state in `cook/` at the project root ([ADR 0016](../../../../docs/adr/0016-the-working-files-live-outside-the-repo.md)), a time floor in hours, no question after intake, and a critic score as the stop condition ([ADR 0004](../../../../docs/adr/0004-a-finding-blocks-only-when-proven.md)). Its separation of measured and eyeballed numbers fits our certainty levels.
