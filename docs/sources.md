# Where the skills come from

Skills name no external source: an agent that read "Matt Pocock `grilling`" in a skill could go find that skill and leave the framework. The linter forbids it (P005, [ADR 0007](adr/0007-no-external-sources-in-skills.md)). Attribution lives here instead: for each file, the attribution text removed from it on 2026-11-19, as it was. The originals are in `knowledge/sources/`.

When a skill changes, update its section here, in the same PR.

## `skills/add-guardrail/SKILL.md`

- Source: pstack `correct`, Lauren Tan's inverted pyramid.
- (Matt Pocock `retro`)

## `skills/add-guardrail/references/levels.md`

- Source: pstack `correct`, Lauren Tan.

## `skills/analyze-impact/SKILL.md`

- Source: pstack `blast-radius`.

## `skills/analyze-impact/references/where-grep-stops.md`

- Source: pstack `blast-radius`.

## `skills/babysit-pr/SKILL.md`

- 2026-11-20: one push per round and the stack rules (the lowest PR first, one babysitter per stack, fixes in the owning PR, the stack's shape kept), from pstack `poteto-mode` babysit playbook. Adapted: rebasing the PRs above after the lowest one is rebased stays the babysitter's job, since our builder owns the stack.
- Source: tstack `babysit-pr`, pstack `shipping`.
- (pstack `babysit`)
- (tstack `full-send`)
- 2026-11-20, from the coherence audit: a verdict requested when none covers the head, and `ready` removed when the patch id moved, from pstack `shipping` ("verify each PR independently before it lands", "Compare git patch-id at the verdict SHA with the current head"). The stack rules moved to `references/stack.md`.
- 2026-11-20, second coherence audit: a FAIL during babysit is fixed or disputed within the PR's 2-FAIL budget; without a PR watcher, a bounded check every 5 to 10 minutes for 2 hours, as pstack's `watch-pr` polls (ours: the bound).

## `skills/babysit-pr/references/stack.md` (2026-11-20)

- Source: pstack `poteto-mode` babysit playbook: the frontier, one babysitter per stack, the owner who babysits its own PR and rebases its own branch ("An Autopilot owner babysitting its own PR is that owner"), and the rebase reported to the owner (Lauren Tan).

## `skills/catch-me-up/SKILL.md` and its references (2026-11-20)

- Source: pstack `ketchup`, and `ketchup-video` for the video mode (Lauren Tan), condensed. Adapted: the window can be a set of PRs or a new session, since our tasks end in PRs; the reply leads with the PRs' demo videos.

## `skills/clean-worktrees/SKILL.md` (2026-11-20)

- Source: pstack `poteto-mode` worktree-cleanup playbook and its `worktree-audit.sh` (Lauren Tan). Adapted: the generic part only, without iOS simulators and editor caches; a worktree touched in the last 24 hours counts as in use, since our harnesses have no list of pinned chats.

## `skills/constitution/README.md`

- (pstack `poteto-mode`)
- 2026-11-20, rules 11 to 13 (ADR 0014): pstack `poteto-mode` Autonomy and Non-negotiables ("don't wait for confirmation", "broken skill mid-task"), and its `autonomous-run` playbook (mid-run discoveries are yours, out-of-band fixes in their own PR, a plateau is not a stop, never relax the predicate). Adapted: a framework skill that is wrong goes to `/learn-from-mistakes`, since a target repo cannot edit the installed plugin.
- 2026-11-20, Reading a principle: pstack `poteto-mode` ("Read the leaf skill in full for any principle you apply", "Cite only principles whose leaf SKILL.md you read this session") and `poteto-agent` ("Navigate to a leaf principle skill whenever you apply that principle"). Ours: never a whole group of the index, and the W002 budget in `tools/lint_skills.py`, since our full forms are longer than pstack's.
- 2026-11-20, from the coherence audit: rule 12 narrowed to what blocks the goal, from pstack `orchestrate` ("Keep only the fixes that block the program, and park the rest as follow-ups"); rule 2 extended to every PR a skill opens, from pstack `shipping`; principles in plain words in the decision log, from pstack `show-me-your-work` (ADR 0015).
- 2026-11-20, third coherence audit: a stop says the call in plain words, a recommended default, and what the user could say instead, keeps working on the rest, and the user's answer in their own words restarts it, from pstack `poteto-mode` ("apply a default, report it with a full explanation, and say in plain words what the operator could tell you to do instead. The operator answers in their own words. Never give a shorthand token to type back") and `babysit` ("Surface the escalation and keep working the rest"). Ours: the `needs-human` label stays as a visible marker.

## `skills/constitution/references/languages/typescript.md` (examples, 2026-11-20)

- The Examples section condenses pstack `typescript-best-practices/references/patterns.md` (Lauren Tan).

## `skills/constitution/references/writing.md` (2026-11-20)

- Source: pstack `technical-writing` (its three top rules, Google developer style, STE, Global English, the Diataxis modes, and its worked example) and `unslop` (the pattern catalog), condensed (Lauren Tan).

## `skills/constitution/references/coverage.md`

- Source: Lauren Tan ("our code review process has now really shrunk into looking at verification artifacts instead. So things like videos, screenshots, diagrams"), pstack `create-verification-skill` (feature map), pstack `statechart`.
- (pstack `ketchup-video`)

## `skills/constitution/references/decision-log.md`

- Source: pstack `show-me-your-work` (Lauren Tan).

## `skills/constitution/references/harness.md`

- 2026-11-20, Model per role: pstack `setup-pstack` and the "Match the model to the job" rules of `poteto-mode` (Lauren Tan). Adapted: roles map to the models of one subscription, Claude or Codex, never across providers; an override is a line in the user's agent file instead of a generated rule file.
- (tstack)
- 2026-11-20, second coherence audit: the verifier's verdict keeps ADR 0003's other family when the harness offers one.

## `skills/constitution/references/languages/typescript.md`

- Source: pstack `typescript-best-practices` (Lauren Tan).

## `skills/constitution/references/parallel.md`

- Source: pstack `arena` and `swarm` (Lauren Tan). Adapted: runners come from the harness's model families (see [harness.md](../skills/constitution/references/harness.md)), not from a model config file.
- 2026-11-20: the arena removed. The user runs on one subscription, not a panel of models, so the builder sketches a design twice itself.

## `skills/constitution/references/pr-format.md`

- 2026-11-20: Why opens with who notices and what the next maintainer inherits, from pstack `poteto-mode` "Frame impact for the consumer and the maintainer".
- (pstack `opening-a-pr`)
- 2026-11-20: the Design section, from pstack `architect`, whose rationale ships beside the sketch.

## `skills/constitution/references/principles.md` and `principles/`

- Most ids come from pstack (Lauren Tan, `cursor-pstack`), where each one is a full skill (`principle-<name>`). Since 2026-11-20, `principles.md` is the one-line index and `principles/<id>.md` holds the full form, condensed from the pstack skill.
- Ours: the uniform shape of every full form (Apply when, Rule, How, Test, Sign it was skipped, Example), so the builder applies a principle and the verifier judges it with the same test; and the ids renamed to say what they do, as skill names do.
- Renamed on 2026-11-20, with the pstack name each came from: `design-the-data-first` (pstack `foundational-thinking`), `validate-at-the-boundary` (pstack `boundary-discipline`), `make-illegal-states-unrepresentable` (pstack `type-system-discipline`), `make-the-smallest-change` (pstack `laziness-protocol`), `design-for-the-consumer` (pstack `experience-first`, added), `build-a-tight-loop` (ours, was `tight-loop`).
- `prove-it-works`: pstack
- `build-a-tight-loop`: Matt Pocock `diagnosing-bugs`
- `test-behavior-not-implementation`: pstack, Matt Pocock `tdd`
- `explain-the-number`: pstack
- `verify-at-the-edge`: Ray Amjad, Anthropic "harness design"
- `fix-root-causes`: pstack
- `attack-the-premise`: pstack
- `encode-lessons-in-structure`: pstack, Lauren Tan
- `build-the-lever`: pstack
- `design-the-data-first`, `redesign-from-first-principles`, `design-for-the-consumer`: pstack, added 2026-11-20
- `model-the-domain`: pstack
- `design-it-twice`: pstack `architect` and `principle-exhaust-the-design-space`
- `migrate-callers-then-delete`: pstack
- `minimize-reader-load`: pstack
- `make-illegal-states-unrepresentable`: pstack, with the examples of its TypeScript skill
- `validate-at-the-boundary`: pstack
- `make-the-smallest-change`: pstack
- `subtract-before-you-add`: pstack
- `sequence-verifiable-units`: pstack
- `scope-stays-put`: tstack `council`, pstack
- `guard-the-context-window`: pstack
- `make-operations-idempotent`: pstack
- `separate-before-serializing-shared-state`: pstack
- `never-block-on-the-human`: pstack
- `keep-the-codebase-clean`: Lauren Tan
- Not taken: pstack `principle-outcome-oriented-execution`, which accepts broken intermediate states; our units each land green, and a wide change uses expand, migrate, contract.
- The opening assumption of the red flags, an agent that sees only the files it opened, comes from pstack `architect` and `correct`.

## `skills/constitution/references/proof.md`

- Sources: tstack `full-send` (proof), pstack `principle-prove-it-works` and `blast-radius` (certainty levels), Matt Pocock `diagnosing-bugs` (red loop), Ray Amjad and Anthropic "harness design" (verify where the model is weakest).
- (pstack: "a small, obvious edit doesn't" need full rigor)
- (Ray Amjad: "you don't really need a verifier to like verify that the contact form submits"; Anthropic "harness design": the evaluator "is worth the cost when the task sits beyond what the current model does reliably solo")
- 2026-11-20, from the coherence audit: a missing driver is not a pass, from pstack "'Inconclusive' or wrong-surface is not a pass" and `autopilot-full` ("The verdict is not clean without the live lane"); a user-facing `low` change is proven on the app, from pstack `poteto-mode` ("Shipping UI: the matching control skill").

## `skills/constitution/references/target-repo.md` (where skills and instructions live, 2026-11-19)

- Agent Skills, "How to add skills support to your agent": "The `.agents/skills/` paths have emerged as a widely-adopted convention for cross-client skill sharing. While the Agent Skills specification does not mandate where skill directories live…" <https://agentskills.io/client-implementation/adding-skills-support>
- Claude Code, Skills: project skills in `.claude/skills/`; "a `<skill-name>` entry in the enterprise, personal, or project location can be a symlink to a directory elsewhere on disk". <https://code.claude.com/docs/en/skills>
- Claude Code, Memory: reads `AGENTS.md` when no `CLAUDE.md` exists (v2.1.277+), and "Not read: … anything under a `.agents/` directory". <https://code.claude.com/docs/en/memory>
- Codex, Build skills: "Codex scans `.agents/skills` in every directory from your current working directory up to the repository root", "supports symlinked skill folders", and `agents/openai.yaml` `policy.allow_implicit_invocation`. <https://learn.chatgpt.com/docs/build-skills>

## `skills/constitution/references/statechart.md`

- Source: pstack `statechart` (Lauren Tan). Adapted: pstack ships a script that runs TLC and draws the chart; here the method is described and the tool is the repo's, or TLC run directly.

## `skills/create-app-driver/SKILL.md`

- 2026-11-20: the control CLI (`references/drivers.md`) and the template's "add a command, not a throwaway script", from pstack guide page "Verify the result and open a PR" (Lauren Tan).
- Source: pstack `create-verification-skill`, `maintain-verification-skill`, and the formal variants.

## `skills/create-app-driver/references/feature-map.md`

- Source: pstack `create-verification-skill`, example `create-note.md`.

## `skills/create-app-driver/references/formal.md`

- Source: pstack `create-formal-verification-skill` and `maintain-formal-verification-skill` (Lauren Tan).

## `skills/create-app-driver/references/maintain.md`

- Source: pstack `maintain-verification-skill`.

## `skills/investigate/SKILL.md`

- Sources: pstack `poteto-mode` investigation, runtime-forensics, trace-forensics, and prototype playbooks, `how`, `why` (Lauren Tan). Grouping them in one skill is ours: they share an answer as output, and none of the steps that lead `ship` to a PR.

## `skills/investigate/references/diagnosis.md`

- Source: pstack `poteto-mode` runtime-forensics and trace-forensics playbooks (Lauren Tan), merged here.

## `skills/investigate/references/prototype.md`

- Source: pstack `poteto-mode` prototype playbook and `principle-exhaust-the-design-space` (Lauren Tan).

## `skills/investigate/references/question.md`

- Source: pstack `poteto-mode` investigation playbook, `how`, and `why` (Lauren Tan).

## `skills/learn-from-mistakes/SKILL.md`

- Sources: pstack `reflect` (three lenses, a synthesizer, approval before any edit), Matt Pocock `retro` (categories of improvement; standards belong to the review agent), Lauren Tan (a correction becomes a check, not a rule).

## `skills/learn-from-mistakes/references/reviewers.md`

- Source: pstack `reflect` reviewer prompts; the tooling lens also takes Matt Pocock `retro` categories.

## `skills/learn-from-mistakes/references/routes.md`

- Source: our verification layers ([design 02](history/02-architecture.md), section 5); Matt Pocock `retro` for the target repo files.
- (Matt Pocock `retro`)

## `skills/learn-from-mistakes/references/synthesis.md`

- Source: pstack `reflect` synthesizer.

## `skills/pause-task/SKILL.md` (2026-11-20)

- Source: pstack `poteto-mode` pause-safely playbook (Lauren Tan). Adapted: the resume note goes in the `wip:` commit body and on the open PR, where a later session finds it, instead of a temporary file; the pause also triggers on a usage limit, since the user runs on a subscription.
- 2026-11-20, from the coherence audit: a task with no branch writes its note to a file outside the repo, as pstack `pause-safely` does ("write it to a file like /tmp/<slug>-resume.md"); the decision log's rows go into the note, since the log lives out of git.

## `skills/recall-context/SKILL.md` (2026-11-20)

- Source: pstack `recall` (Lauren Tan): the two records, the scope fixed first, the fan-out over transcripts, the sweep of the shared record, the brief's contract and its tags. Adapted: transcripts found where the harness keeps them, the bulk-reading model of the Model per role, the repo's issue tracker.

## `skills/resume-task/SKILL.md` (2026-11-20)

- Source: pstack `poteto-mode` session-pickup playbook (Lauren Tan). Adapted: the trail starts from the `wip:` commit and the PR; the task continues without asking (ADR 0014).

## `skills/ship-queue/references/owner-brief.md` (2026-11-20)

- Source: pstack `orchestrate` ("Each kickoff names the evidence that proves the work is done... the paths the worker may and may not write") and `autopilot-full` (push early, push each finished unit), adapted to an owner that runs `ship`.

## `skills/ship-queue/SKILL.md` (2026-11-20)

- Source: pstack `poteto-mode` autopilot-stack and autopilot-full playbooks, and orchestrate for the supervision rules: start with one unit, judge agents by side effects, replace a stuck one with a consolidated brief (Lauren Tan). Adapted: no merge and no merge prep; each owner runs `ship`, whose fresh verifier gives the verdict, instead of a root swarm; at most three owners at once, for a subscription; no cloud agents.
- 2026-11-20, from the coherence audit: two replacements per task, then `needs-human`, from pstack `orchestrate` ("After two retries, drop the unit and replan around it"); each owner babysits its own PR, from pstack `babysit`.

## `skills/say-it-plainly/SKILL.md` (2026-11-20)

- Source: pstack `bro` (Lauren Tan).

## `skills/sharpen-prompt/SKILL.md` (2026-11-20)

- Source: pstack `sharpen` (Lauren Tan), nearly as is.

## `skills/setup-repo/references/trackers/` (an issue tracker of any kind, 2026-11-19)

- Matt Pocock `setup-matt-pocock-skills`: "Those files are the only thing that varies between repos. The skills themselves are identical everywhere. They read `docs/agents/issue-tracker.md` at run time and do what it says." Templates for GitHub, GitLab, and local markdown, and an "Other" option in prose for Jira, Linear, and the rest (`knowledge/sources/repos/mattpocock-skills/repo/docs/engineering/setup-matt-pocock-skills.md`).
- Matt Pocock, ADR 0001: an explicit pointer to the setup only in the skills that truly depend on it (`.agents/adr/0001-explicit-setup-pointer-only-for-hard-dependencies.md`). Adopted for `shape-spec` and `learn-from-mistakes`.
- The `gh` and `glab` commands of the templates are adapted from his `issue-tracker-github.md` and `issue-tracker-gitlab.md`.

## `skills/shape-spec/SKILL.md`

- Source: Ray Amjad (splitting a spec into parallel units gives worse results, the work is tangled in ways nobody expected), Anthropic "harness design" (planner kept, sprints dropped).
- Sources for the modes: Matt Pocock `grilling`, `domain-modeling`, `grill-with-docs`, `to-spec`, `wayfinder`.
- (Anthropic kept its planner for this reason)
- 2026-11-20, from the coherence audit: a question of fact is settled by a run, one of look or feel by the user, from pstack `poteto-mode` ("If the answer is a fact you could observe by running something, it is not the human's to answer").

## `skills/shape-spec/references/domain.md`

- Source: Matt Pocock `domain-modeling`.

## `skills/shape-spec/references/grill.md`

- Source: Matt Pocock `grilling` and `grill-with-docs`.

## `skills/shape-spec/references/map.md`

- Source: Matt Pocock `wayfinder`.
- That keeps the map clear of the problem Ray Amjad describes: implementation split across agents that turn out to be tangled.

## `skills/shape-spec/references/spec.md`

- Source: Matt Pocock `to-spec`; the link between user stories and cases is ours.

## `skills/ship/references/clean.md`

- Source: pstack `no-comments` and its `comment-sicko` agent (Lauren Tan). Adapted: constraint encodings go to `/add-guardrail` instead of an inline approval.

## `skills/ship/references/design.md`

- 2026-11-19, completed from pstack `principle-model-the-domain`: the small module boundary for invariants, structures chosen by access pattern, lifecycle risk, and the phase-named modules sign. The rule that the data shape takes its names from `GLOSSARY.md` is ours: it ties Matt's vocabulary to Lauren's code-as-truth.
- Source: pstack `principle-model-the-domain`, `architect` and its `design-red-flags.md` (Lauren Tan). Adapted: the arena runs as [parallel.md](../skills/constitution/references/parallel.md) describes, with the harness's model families instead of pstack's model config.
- 2026-11-20, architecture method brought closer to pstack (Lauren Tan, `knowledge/sources/repos/cursor-pstack/`): the method gains grounding in the history of the current shape (pstack `architect` Phase A, which runs `why`), the rules of a sketch (`sketch.md`), the design note (`design-note.md`), the design shown to the user for a one-way door or on request (pstack `architect` Phase C, opt-in there), building against the sketch, and the six tells and the procedure for scrapping it (pstack `architect` Phases D and E). The table of how much design a change needs adapts pstack's guide page "Design before you write code", and designs every feature, as pstack's feature playbook runs `architect` on every feature. Ours: the builder writes both sketches itself instead of an arena of models, and a task scraps once, then `needs-human`.

## `skills/ship/references/design-note.md`

- Source: pstack `architect/references/rationale-template.md` (Lauren Tan). Adapted: Synthesis becomes Choice between the builder's two sketches, a Deviations section is filled during the build, and "Next implementation step" is dropped.

## `skills/ship/references/sketch.md`

- Source: pstack `architect/references/runner-prompt.md` (Lauren Tan). Adapted: the builder follows it for both of its sketches, each rule names its principle id, and rule 12 comes from `principle-laziness-protocol`.

## `skills/ship/references/frame.md`

- 2026-11-20: the frame is shown and the build goes on, as pstack `poteto-mode` restates the goal without waiting (ADR 0014).
- Source: pstack `in-your-own-words`, Anthropic "harness design" (agree on what done means before building), Matt Pocock `tdd` (agree the seams first).
- Source: pstack `poteto-mode` playbooks (Lauren Tan).
- 2026-11-20, second coherence audit: a symptom that will not reproduce goes through `investigate`'s diagnosis and the task goes on or stops, as pstack's bug-fix playbook does ("synthesize the trigger, tighten conditions, or instrument until it fires"); several open decisions stop the task and propose `/shape-spec`, since they are the user's (pstack `poteto-mode`: "Reserve the question for a genuine product or preference call").

## `skills/ship/references/playbooks/bespoke.md`

- Source: pstack `figure-it-out` (Lauren Tan); the wide-change sequence comes from Matt Pocock `to-tickets`.
- (Ray Amjad; Anthropic "harness design" dropped sprints once the model could hold the whole build)
- (pstack `opening-a-pr`)

## `skills/ship/references/playbooks/bug-fix.md`

- Source: Matt Pocock `diagnosing-bugs`, pstack `poteto-mode` bug-fix playbook.
- (pstack)

## `skills/ship/references/playbooks/feature.md`

- Source: Matt Pocock `tdd`, pstack `principle-sequence-verifiable-units`.
- 2026-11-20: duty 2 from pstack `principle-redesign-from-first-principles` and `principle-foundational-thinking`.

## `skills/ship/references/playbooks/hillclimb.md` (2026-11-20)

- Source: pstack `poteto-mode` hillclimb playbook (Lauren Tan). Adapted: proof duties in the shape of the other playbooks, and a line for the verifier.

## `skills/ship/references/playbooks/perf.md`

- Source: pstack `poteto-mode` perf-issue playbook and `benchmark-checklist` (Lauren Tan).

## `skills/ship/references/playbooks/refactoring.md`

- Source: pstack `poteto-mode` refactoring playbook, `principle-minimize-reader-load`, `principle-migrate-callers-then-delete-legacy-apis` (Lauren Tan).
- 2026-11-20: the target shape per pstack `principle-redesign-from-first-principles`, as the pstack playbook's step 3 names it.

## `skills/ship/references/playbooks/visual-parity.md`

- Source: pstack `poteto-mode` visual-parity playbook (Lauren Tan).

## `skills/test-skill-change/SKILL.md` (2026-11-20)

- Source: pstack `poteto-mode` eval playbook (Lauren Tan): the blinding rules, the organic prompt, the judge on neutral labels, chain-following graded from what the agent read. Adapted: every run and the judge on the session's model, with no panel of models (ADR 0014 lifts ADR 0002's removal of `eval`).

## `skills/verify-pr/SKILL.md`

- Anthropic found that an untuned evaluator finds real issues, then talks itself into approving the work anyway ("harness design").

## `skills/verify-pr/references/calibration.md`

- (pstack `create-formal-verification-skill`)

## `skills/verify-pr/references/lanes.md`

- Source: tstack `full-send`.
- Source: Anthropic "harness design" (the evaluator drives the live app), pstack `create-verification-skill`.
- Source: pstack `blast-radius`.
- Source: pstack `interrogate`.
- Source: Matt Pocock `code-review` (Spec axis), `tdd`, pstack refactoring playbook.
- Source: Matt Pocock `code-review` (Standards axis, Fowler smells).
- 2026-11-20: the standards lane checks the shape against the red flags, the architecture principles, and the PR's design note, as pstack `architect` holds an implementation to its sketch.

## `skills/verify-pr/references/verdict.md`

- Source: tstack severity scale, pstack blocking rule.
- Source: Matt Pocock `code-review` ("documented-standard breaches can be hard"), pstack ("a doc line the PR made wrong").

## `docs/guide.md` (2026-11-20)

- Source: pstack `poteto-help` references `prompting.md` and `recipes.md`, and the guide pages "Route work through /poteto-mode" and "Recipes and pitfalls" (Lauren Tan), rewritten for these skills. Checked by R011, as ADR 0013 asks of a doc.

## The layout of this repo (2026-11-19)

- Source: Matt Pocock's `mattpocock/skills` repo (`knowledge/sources/repos/mattpocock-skills/repo/`): a README that says why and lists every skill linked to its `SKILL.md`; `SCOPE.md` (its bar of an observed failure was dropped on 2026-11-20: a change needs only to fit the ADRs); a bug issue template with the skill, version, and harness; `CHANGELOG.md`; decisions as ADRs; the `AGENTS.md` rule that a skill added or renamed updates every list of skills in the same PR.
- Install: the plugin manifests (`.claude-plugin/plugin.json` listing each skill, `marketplace.json` with the repo as its own source), `agents/openai.yaml` beside each `SKILL.md` with `policy.allow_implicit_invocation: false` (his `.agents/invocation.md`), and `tools/link_skills.py`, adapted from his `scripts/link-skills.sh` (same destinations, same guard against a destination linked into the repo). Ours: shared folders linked beside the skills, a real folder never deleted, the Windows junction fallback, `--dry-run` and `--unlink`.
- Ours: the rule that a doc is either executed or dated ([ADR 0013](adr/0013-a-doc-stays-fresh-by-running-or-by-date.md)), and the ADRs in `docs/adr/`, the folder the framework gives target repos, instead of `.agents/adr/`.
