# 0020. A heavy visual change is specified by a target

- **Status**: proposed, 2026-11-25.
- **Extends**: [0019](0019-the-spec-sets-the-bar-and-a-task-builds-the-proof-it-lacks.md), "the spec sets the bar": for a story that changes a visual surface heavily, the bar is also a visual target, and each target is a case. The rest of 0019 stands.
- **Applies to**: `skills/shape-spec/` (SKILL.md, the grill's visual branch, the spec's Visual targets), `skills/investigate/references/prototype.md`, `skills/ship/` (`playbooks/feature.md`, `references/visual-loop.md`, `scripts/check_evidence.py`), `skills/verify-pr/references/lanes.md` (`live`, `standards`), `skills/choose-skill/SKILL.md`, `skills/constitution/` (`README.md`, and in `references/`: `ui.md`, `proof.md`, `coverage.md`, `glossary.md`, `harness.md`)
- **Enforced by**: `check_evidence.py` fails when a visual target of the spec (`V1`) has no case, with a test in `tools/test_check_evidence.py`. The rest by two blind `test-skill-change` runs on one UI task, with and without this change, and by review.

## Context

On 2026-11-25 the user asked for a framework that is good at UI and UX. With the decision as it was:
- `shape-spec` sends a question of look or feel to a prototype the user picks from. The pick ends as a line of prose under Decisions.
- `ship` builds a feature from journeys that say what works, not how it looks.
- `verify-pr` judges whether the journeys work (`live`) and whether the code is sound (`standards`). Only `visual-parity` compares images, and only for exact sameness.

So the chain carries no target for how a page looks, and nobody but the builder judges it.

**Anthropic, harness design** (`knowledge/sources/articles/2026-03-24-harness-design-long-running-apps/content.md`):
- Unprompted, the model "gravitates toward safe, predictable layouts that are technically functional but visually unremarkable" (35).
- "Is this design beautiful?" is hard to answer consistently, but "does this follow our principles for good design?" gives something concrete to grade against (37).
- Four criteria (design quality, originality, craft, functionality) penalize "AI slop" patterns (39-46).
- The evaluator is separate from the generator, calibrated with few-shot examples, and drives the live page before scoring (48, 50).
- The criteria's wording steers the output, and the last iteration is not always the best (54, 56).

**Cook, by Leon Lin** (`knowledge/sources/repos/leonxlnx-cook/repo/`):
- "References are the minimum bar, not inspiration" (`SKILL.md:45`). For UI, "a shot is one screen state at a fixed viewport size" (`references/target-and-bar.md:29`).
- Critics are fresh subagents that get only side-by-side images and the rubric. There are at least two, and the median is taken; when they disagree, another one is added (`references/loop-and-critics.md:34-37`).
- "Your own score is logged, never decisive" (`SKILL.md:85`). It keeps measured numbers apart from eyeballed ones (`references/target-and-bar.md:72`).
- User feedback beats critic priorities. When the user cannot name a problem, the agent describes how it built that part (`SKILL.md:95`, `references/loop-and-critics.md:71`).
- Motion references are analyzed frame by frame, and no element is copied one to one (`references/target-and-bar.md:33-41`).
- One intake asks every question with a default (`references/intake.md`).

**Taste Skill, by Leon Lin** (`knowledge/sources/repos/leonxlnx-taste-skill/repo/skills/taste-skill/SKILL.md`):
- Every checklist line names the browser checks that hold it, and the last line is "for your eyes" (298-363).
- One system: one button pair, one card style, one radius scale (342).
- Every width from 1440 down to 320, with tap targets of 44px (355-361).

**Eric Tech's summary** (`knowledge/sources/videos/2026-11-20-taste-skill-lessons-eric-tech/notes.md`) adds three things: lay out before you animate (07:43), check three mockups at phone width (03:06), and give the agent an MCP server of captured sites, with their colors and fonts, and a browser tool to use a site like a visitor (01:16).

**Ours**, settled with the user on 2026-11-25:
- the trigger and the visual branch inside `shape-spec`;
- the three design modes;
- the rule that the repo's design system is read from the code and never written down;
- the target as a case, and its place in `verify-pr`;
- the inspiration library as a harness capability, with the web and a browser as fallbacks.

## Decision

### `shape-spec` runs a visual branch for a heavy visual change
- **Trigger.** A story that adds a screen, redesigns one, or builds a page whose look is the point opens the branch. The agent names the reason. A small change on an existing screen does not open it, and follows the design system as it is.
- **The design system is a fact.** A subagent finds in the code where the tokens, components, and patterns of the area live. Nothing is written down: the code says it, and the builder reads it again in `ship`.
- **Design mode.** The agent recommends one, and the user confirms:
  - **follow**: only existing components;
  - **extend**: new components in the same idiom;
  - **break away**: a look of its own, when the task calls for it, such as a marketing page or a new product.
- **References.** The agent asks for the user's references. With none, it proposes some from a library of real product screens when the harness has one, else from the web.
- **Prototypes.** Three variants are built through `investigate`'s prototype mode, with the repo's real components under follow and extend. Each is shown at a desktop and a phone width. Feedback is made specific: when the user cannot name a problem, the agent describes what it built.
- **The spec holds Visual targets** (`V1`, `V2`): the picked screens, as captures attached to the issue, at their widths and states. It also holds the design mode, and the criteria and bans of `ui.md` that apply, confirmed by the user. No file paths.

### Generic criteria ship with the skills
`constitution/references/ui.md` holds the criteria (coherence, originality, craft, usability) and the list of generic defaults to avoid. The builder, the loop's critics, and the verifier read it, as they read the language rules. Only what the spec took from it can block.

### `ship` closes the gap in rounds
When the spec has a visual target, `feature` builds the layout before the motion. It then runs the target loop of `visual-loop.md`:
- capture each target state at its widths;
- put the target and the head side by side;
- measure what a command can measure;
- have at least two critics score it, each a fresh subagent (from another family when available) that sees only the images and the criteria; with none, the round goes unscored rather than self-scored (ADR 0003);
- fix the weakest gap;
- log the round in the decision log, outside the repo.

The loop stops when every critic median clears the bar after the round floor, or at the round limit. The user's feedback ranks before the critics'.

### Critic scores steer, the verdict proves
A score is level 1: it chooses the next round and never decides a verdict. `live` captures the head at each target's states and widths, side by side with the target. A gap the spec's Visual targets or criteria name, shown on that capture, is a finding. Any other taste judgment is a note.

### Inspiration is a capability, not a dependency
"Search a library of real UI references" is a harness capability. Without it, the agent searches the web or drives a real site in a browser. The agent never installs one on its own.

## Alternatives rejected

- **A designer skill or persona**: `SCOPE.md` excludes personas. The gap is a kind of evidence and a review question, not a role.
- **A critic score as the blocking bar**, as Cook's stop check uses it: under [ADR 0004](0004-a-finding-blocks-only-when-proven.md), a score is a claim, not a run.
- **The design system described in `coding-standards.md`**: the code already says it, and a prose copy goes stale with the next component. A mechanical rule, such as no raw color outside the tokens, becomes a check through `add-guardrail`.
- **The criteria and bans in the project folder, seeded by `setup-repo`**: only `skills/` is installed, and `setup-repo` derives standards from the repo, never from a generic list.
- **A playbook of its own**: two playbooks split a task into two PRs, which would cut a UI feature in two. The loop is a duty of `feature`.
- **A time floor in hours**, as Cook sets: it spends usage without proof that it helps. A round floor is measurable, as `hillclimb` already does.
- **Run state in a folder of the repo**, as Cook keeps it: [ADR 0016](0016-the-working-files-live-outside-the-repo.md) keeps working files outside.
- **No question after intake**, as Cook runs: `shape-spec` already settles every decision before the build, and `ship` stops only on the stops of the constitution.

## Consequences

- A heavy visual spec takes one more branch in the grill and a round of prototypes. Small UI changes take none.
- A UI feature with a target costs more to build: at least two critics a round, for several rounds. The round limit caps it, and all its rounds count as one build attempt.
- The verifier's `live` lane captures more states, at more widths.
- The criteria in `ui.md` steer every design the agent makes. Their wording is tested by the blind runs, since the harness design article reports that wording alone moved the output.
