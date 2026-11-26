# 0020. A heavy visual change is specified by a target

- **Status**: proposed, 2026-11-25; revised 2026-11-26.
- **Extends**: [0019](0019-the-spec-sets-the-bar-and-a-task-builds-the-proof-it-lacks.md), "the spec sets the bar": for a story that changes a visual surface heavily, the bar also holds visual targets, still or in motion, and each target is a case. The rest of 0019 stands.
- **Applies to**: `skills/shape-spec/` (SKILL.md, `references/grill.md`, `references/spec.md`), `skills/investigate/references/prototype.md`, `skills/ship/` (`SKILL.md`, `references/design.md`, `references/frame.md`, `references/verification.md`, `references/visual-loop.md`, `playbooks/feature.md`, `scripts/check_evidence.py`), `skills/verify-pr/references/lanes.md` (`live`, `standards`), `skills/choose-skill/SKILL.md`, `skills/README.md`, `skills/constitution/` (`README.md`, and in `references/`: `ui.md`, `proof.md`, `coverage.md`, `glossary.md`, `harness.md`, `decision-log.md`)
- **Enforced by**: `check_evidence.py` fails when a visual target of the spec (`V1`) has no case, with a test in `tools/test_check_evidence.py`. The rest by two blind `test-skill-change` runs on one UI task, with and without this change, and by review against the map below.

## Context

On 2026-11-25 the user asked for a framework that is good at UI and UX, motion included. With the decision as it was:
- `shape-spec` sends a question of look or feel to a prototype the user picks from. The pick ends as a line of prose under Decisions.
- `ship` builds a feature from journeys that say what works, not how it looks or moves.
- `verify-pr` judges whether the journeys work (`live`) and whether the code is sound (`standards`). Only `visual-parity` compares images, and only for exact sameness.

So the chain carries no target for how a page looks or moves, and nobody but the builder judges it.

A first draft copied the source flow into every layer: a six-step branch in the grill, a score bar in the spec, a loop with its own budget, critics with their own model rule. An audit of that draft found each copy restating, or contradicting, a concept the framework already had: prototype mode, grounding, rule 7, the race, the decision log, the proof levels, and the line "nothing technical goes in the spec". This decision therefore starts from the framework's concepts: each idea of the sources lands in the home that already holds its kind, as a change to that home, and a new home exists only where none did.

**Anthropic, harness design** (`knowledge/sources/articles/2026-03-24-harness-design-long-running-apps/content.md`):
- Unprompted, the model "gravitates toward safe, predictable layouts that are technically functional but visually unremarkable" (35).
- "Is this design beautiful?" is hard to answer consistently, but "does this follow our principles for good design?" gives something concrete to grade against (37).
- Four criteria (design quality, originality, craft, functionality) penalize "AI slop" patterns (39-46).
- The evaluator is separate from the generator, calibrated with few-shot examples, and drives the live page before scoring (48, 50).
- The criteria's wording steers the output, and the last iteration is not always the best (54, 56).

**Cook, by Leon Lin** (`knowledge/sources/repos/leonxlnx-cook/repo/`):
- "References are the minimum bar, not inspiration" (`SKILL.md:45`). For UI, "a shot is one screen state at a fixed viewport size" (`references/target-and-bar.md:29`).
- Motion references are cut into frames and contact sheets, and written as one line per effect: what moves, its easing, duration, and direction. The build takes from many references and copies no element one to one (`references/target-and-bar.md:31-41`).
- Critics are fresh subagents that get only side-by-side images and the rubric. There are at least two, and the median is taken; when they differ by more than 1.0 on 10, another one is added (`references/loop-and-critics.md:34-37`).
- "Your own score is logged, never decisive" (`SKILL.md:85`). It keeps measured numbers apart from eyeballed ones (`references/target-and-bar.md:72`).
- User feedback beats critic priorities. When the user cannot name a problem, the agent describes how it built that part (`SKILL.md:95`, `references/loop-and-critics.md:71`).

**Taste Skill, by Leon Lin** (`knowledge/sources/repos/leonxlnx-taste-skill/repo/skills/taste-skill/SKILL.md`):
- Every checklist line names the browser checks that hold it, and the last line is "for your eyes" (298-363).
- One system: one button pair, one card style, one radius scale (342).
- Every width from 1440 down to 320, with tap targets of 44px (355-361).
- Every control visibly answers the pointer; under reduced motion everything rests and nothing stays hidden (328-334).

**Eric Tech's summary** (`knowledge/sources/videos/2026-11-20-taste-skill-lessons-eric-tech/notes.md`) adds three things: lay out before you animate (07:43), check three prototypes at phone width (03:06), and give the agent an MCP server of captured sites, with their colors and fonts, and a browser tool to use a site like a visitor (01:16).

**Ours**, settled with the user on 2026-11-25 and 2026-11-26:
- the trigger inside `shape-spec`, and the three design modes;
- the rule that the repo's design system is read from the code and never written down;
- the target as a case, still or in motion, and its place in `verify-pr`;
- the critic score kept out of the spec;
- motion in scope from the start;
- the inspiration library as a harness capability, with the web and a browser as fallbacks.

## Decision

### The map: each idea in the home of its kind

| Idea | Home | Change to that home |
|---|---|---|
| A heavy visual change is spotted early | `shape-spec` step 1, which already sends a look question to a prototype | One sentence: a story that adds a screen, redesigns one, or builds a page whose look is the point, is a heavy visual change; say so and propose prototypes before any other question. A small change follows the design system as it is. |
| References first, prototypes, feedback made specific | `investigate`'s prototype mode, `prototype.md` | Its duties gain: the user's references first (screens, sites, videos for motion), else five to eight proposed with one line each on what to take; three variants from the real components; each shown at a desktop and a phone width, and in motion as a recording when motion is part of the change; when the user cannot name a problem, describe how that part was built. The grill holds no copy of these steps. |
| The design system is a fact | `ui.md`, read by the grounding of `design.md` and by "Facts are yours" in the grill | `ui.md` says where to look and that nothing is written down. Every other file links to it. |
| Design mode: follow, extend, break away | a decision of the grill's design tree | Recommended from the grounding, confirmed by the user, written in the spec's Visual targets. Defined once, in `ui.md`. |
| The pick becomes a target | the spec's cases, beside stories (`S1`) and promises (`P1`), and the project folder (ADR 0016) for its files | The spec gains Visual targets, `V1`, whose files live in `targets/` of the project folder: a still (a capture at a state and a width) or a motion (a recording, with its effect list: trigger, what moves, duration, easing, direction). Each is a case; `check_evidence.py` fails on one without a case. |
| Motion references read frame by frame | `prototype.md`, where references are read | A reference video becomes an effect list; the build takes from several and copies none one to one. The list the user confirms goes in the motion target. |
| Criteria and generic defaults to drop | `ui.md`, new: shipped generic rules, beside the language rules | Criteria for stills and for motion, the widths, the defaults to drop. The spec names the bans and measured checks it takes; only those can block. Read by `standards` as a source of notes, never of a should. |
| The score bar | `visual-loop.md`, as the loop's stop score | Out of the spec: a score is judged and a build choice. Its default lives in `visual-loop.md` alone. |
| Measured or judged | `proof.md`, the certainty levels | A visual target reaches level 5 on a capture or recording, side by side with the target, with its measured numbers. A critic's score is level 1. Stated there only. |
| Build layout, then motion | the `feature` playbook's duties | One duty: build the stills, run the target loop on them, then build motion as its own slice and run the loop on the motion targets. Stated there only. |
| Rounds until the head holds up | rule 7 (every loop has a budget, a plateau changes the approach) and `hillclimb`'s keep-or-revert past the noise | `visual-loop.md` holds what is visual (the captures, the frame strips, the critics' brief) and the loop's own numbers: the stop score and a budget of passes per kind of target. It links rule 7 and `hillclimb` for the rest. At the budget, a measured check still failing means `needs-human`; medians short of the stop score only stop the loop, since a score is level 1. |
| Critics | the race of `parallel.md`, the model table of `harness.md` | Critics run as a race on one brief. `harness.md` gains a critic row: a mid-size model, another family when available, as for the verifier's lanes. With no subagent, a pass goes unscored, never self-scored (ADR 0003). |
| A trail of passes | `decision-log.md` | Its "When" gains the target loop, one row per pass. |
| The verifier's look | `live` and `verdict.md` | `live` captures and records the head at each target, side by side with it, before reading the builder's images. Blocks only: a measured check the spec took that fails, an effect of a motion target missing or out of its tolerance, a ban the spec took that a command detects. `spec` treats a component the design mode does not allow as a part nobody asked for. Graded by `verdict.md`. Any other taste judgment is a note. |
| Routing | `frame.md`'s playbook table, `ship`'s stop for open decisions, `choose-skill` | `feature` covers a screen to build or redesign. A heavy visual task that reaches `ship` with no spec is proposed `/shape-spec`, like several open decisions. |
| Inspiration library | `harness.md`'s capabilities | A row: search a library of real UI references; else the web, or a real site in a browser. Also a row: record a page and cut a video into frames, whose fallback leaves the motion target's case under Not verified. The agent never installs a tool on its own. |
| Words | the glossary | Heavy visual change, visual target (still or motion), effect list, design mode, critic, and target loop, made of passes. "Round" stays `babysit-pr`'s; "shot" is a capture; "bar" stays 0019's. |

### Motion has the same chain as stills

A motion target is proven like a still one: the head is recorded at the target's width and state, and frames are cut at the same moments as the target's. Measured: each effect of the list happens, its duration within the tolerance `ui.md` sets unless the spec sets one, and under reduced motion nothing moves and nothing stays hidden. Judged, so level 1: the feel of the easing and the choreography.

## Alternatives rejected

- **A visual branch of its own in the grill**, as the first draft had: it restated prototype mode and the grounding. The grill keeps only the decisions: the design mode and the pick.
- **A critic score as the spec's bar**: a score is a claim, not a run ([ADR 0004](0004-a-finding-blocks-only-when-proven.md)), and a build choice, not the user's. It stays the loop's stop score.
- **The round floor and limit in the spec**: technical. The loop's budget lives in `visual-loop.md`.
- **Motion left for later**: the user wants it from the start, and a page whose look is the point often moves.
- **A separate id for motion (`M1`)**: one id family keeps `check_evidence.py` and the coverage table as they are. The target says whether it is a still or a motion.
- **A designer skill or persona**: `SCOPE.md` excludes personas. The gap is a kind of evidence and a review question, not a role.
- **The design system described in `coding-standards.md`**: the code already says it, and a prose copy goes stale with the next component. A mechanical rule, such as no raw color outside the tokens, becomes a check through `add-guardrail`.
- **The criteria in the project folder, seeded by `setup-repo`**: only `skills/` is installed, and `setup-repo` derives standards from the repo, never from a generic list.
- **A playbook of its own**: two playbooks split a task into two PRs, which would cut a UI feature in two. The loop is a duty of `feature`.
- **A time floor in hours**, as Cook sets: it spends usage without proof that it helps.
- **Run state in a folder of the repo**, as Cook keeps it: [ADR 0016](0016-the-working-files-live-outside-the-repo.md) keeps working files outside.
- **No question after intake**, as Cook runs: `shape-spec` already settles every decision before the build, and `ship` stops only on the stops of the constitution.

## Consequences

- A heavy visual spec takes a round of prototypes, recorded when motion is part of it. Small UI changes take none.
- A UI feature with a target costs more to build: at least two critics a pass, for several passes, on stills then on motion. The loop's budget caps it, and a spent budget goes to the user.
- The verifier's `live` lane captures and records more states, at more widths.
- The criteria in `ui.md` steer every design the agent makes. Their wording is tested by the blind runs, since the harness design article reports that wording alone moved the output.
- Future imports of a third-party flow start with such a map, before any skill changes: `CODING_STANDARDS.md` gains that rule.
