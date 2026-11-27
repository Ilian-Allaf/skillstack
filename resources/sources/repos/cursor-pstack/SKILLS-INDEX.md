# Index des skills — pstack (plugin Cursor)

- **Repo** : [https://github.com/cursor/plugins/tree/main/pstack](https://github.com/cursor/plugins/tree/main/pstack)
- **Auteur** : Lauren Tan (poteto)
- **Révision** : `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7` (2026-11-14)
- **Importé le** : 2026-11-16
- **Licence** : MIT
- **Skills** : 61
- **Invocation** : 1 modèle, 60 utilisateur
- **Avec scripts** : 3 · **avec références** : 10 · **avec playbooks** : 1

> Catalogue complet : [`catalog.json`](catalog.json). Les descriptions sont celles du frontmatter, tronquées ici.

## automations/benny/skills (3)

| Skill | Invocation | Description | Mots | Support |
|---|---|---|---:|---|
| [`reproduce-and-fix-issues`](repo/automations/benny/skills/reproduce-and-fix-issues/SKILL.md) | user | Reproduce triaged Slack bugs through a configured app-control adapter, verify existing fixes, and open a bounded draft pull request only after before-and-after proof. Use only from the configured Benny repro automation. | 2179 | references |
| [`setup-benny`](repo/automations/benny/skills/setup-benny/SKILL.md) | user | Configure Benny and prepare its triage and repro automations. Use when installing Benny or changing its Slack, tracker, repository, routing, control, model, or budget settings. | 1975 | — |
| [`triage-issue-reports`](repo/automations/benny/skills/triage-issue-reports/SKILL.md) | user | Triage Slack issue reports with one thread-only verdict, evidence review, cause-aware routing, tracker dedupe, and fail-closed ticket creation. Use only from the configured Benny triage automation. | 1612 | references |

## skills (58)

| Skill | Invocation | Description | Mots | Support |
|---|---|---|---:|---|
| [`architect`](repo/skills/architect/SKILL.md) | user | Sketch types, signatures, and module structure before code, then stay in the loop while implementation fills in. Use for /architect, 'architect this', 'design this', or non-trivial work where jumping to code would lock… | 764 | references |
| [`arena`](repo/skills/arena/SKILL.md) | user | Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would… | 909 | — |
| [`automate-me`](repo/skills/automate-me/SKILL.md) | user | Use for \"automate me\", \"create/update/refresh my -mode skill\", \"turn/capture my preferences or working style into a skill\", or wanting agents to follow how the user works. Drafts or revises a personal -mode skill… | 1023 | — |
| [`benchmark-checklist`](repo/skills/benchmark-checklist/SKILL.md) | user | Vet a perf measurement (limiter, tuning, limits, errors, repeatability, relevance, and whether the work happened) before you report or act on it. Use when you run a benchmark or report a speedup or regression you… | 837 | — |
| [`blast-radius`](repo/skills/blast-radius/SKILL.md) | user | Find what a change could break somewhere else before it ships, beyond the diff, and prove the one fact it's safe because of by running real code instead of writing it up. Use for 'blast radius of X', 'what could this… | 641 | — |
| [`bro`](repo/skills/bro/SKILL.md) | user | Restate the last message in plain human language, with no jargon. | 22 | — |
| [`correct`](repo/skills/correct/SKILL.md) | user | Find the mistakes agents keep repeating in this repo and make each one impossible. Try architecture first, then types, then a lint whose error names the fix, then a test, and write docs last. Prove each check fails on… | 374 | — |
| [`create-formal-verification-skill`](repo/skills/create-formal-verification-skill/SKILL.md) | user | Generate a project-local skill that formally verifies the code where a bug costs the most and tests reach the least, in any language, with whichever verification tool fits. Use for /create-formal-verification-skill,… | 927 | — |
| [`create-verification-skill`](repo/skills/create-verification-skill/SKILL.md) | user | Generate a project-local verification skill that drives your app the way a user does — any language, framework, or platform. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project… | 1010 | references |
| [`figure-it-out`](repo/skills/figure-it-out/SKILL.md) | user | Design an auditable playbook when no narrower one fits: a large migration, an ambitious multi-part change, or work a human reviews after stepping away. Scales rigor to the task, runs a hypothesis loop, and logs… | 603 | — |
| [`how`](repo/skills/how/SKILL.md) | user | Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains… | 133 | — |
| [`in-your-own-words`](repo/skills/in-your-own-words/SKILL.md) | user | Restate in your own words what you think the user's goals are and what problem they're trying to solve. Use for /in-your-own-words. | 19 | — |
| [`interrogate`](repo/skills/interrogate/SKILL.md) | user | Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and… | 341 | — |
| [`ketchup`](repo/skills/ketchup/SKILL.md) | user | Catch the user up on what changed in this chat since their last message, in plain words and small visuals. List every item waiting on them with what they need to decide it from the reply alone. Use for /ketchup. | 1150 | — |
| [`ketchup-video`](repo/skills/ketchup-video/SKILL.md) | user | Catch the user up like /ketchup, with a short subtitled video of slides for what happened and the waiting calls as text under it. Use for /ketchup-video. | 673 | — |
| [`maintain-formal-verification-skill`](repo/skills/maintain-formal-verification-skill/SKILL.md) | user | Bring a project's formal verification back in line with the code after the code changes: find the commits that touched verified code, update the model, harness, or properties to describe the code as it is now, rerun,… | 1156 | — |
| [`maintain-verification-skill`](repo/skills/maintain-verification-skill/SKILL.md) | user | Periodic pass that keeps a project's verification skill and feature map honest: parallel source readers per feature, one live session driving every feature, at most one PR of proven corrections. Use for… | 720 | — |
| [`make-bot-ui`](repo/skills/make-bot-ui/SKILL.md) | user | Use when building a custom UI (page, dashboard, buttons) that should wake a Grok Bot over a webhook, when the user must provide a webhook sender key, or when exposing that UI on Tailscale. | 744 | — |
| [`no-comments`](repo/skills/no-comments/SKILL.md) | user | Spawn Comment Sicko, fix accepted findings, and offer encodings for claimed constraints. | 383 | — |
| [`poteto-help`](repo/skills/poteto-help/SKILL.md) | user | Guides users through pstack setup, /poteto-mode, and picking the skill, playbook, or principle for a task. Type /poteto-help with a question. | 2410 | references |
| [`poteto-mode`](repo/skills/poteto-mode/SKILL.md) | user | poteto's agent style for concise, detailed responses, deliberate subagents, unslopped prose, simple code, and verified work. Use for poteto, /poteto-mode, or requests to work in this style. | 3450 | playbooks, references, scripts |
| [`principle-attack-the-premise`](repo/skills/principle-attack-the-premise/SKILL.md) | user | Apply when two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it. | 257 | — |
| [`principle-boundary-discipline`](repo/skills/principle-boundary-discipline/SKILL.md) | user | Apply when wiring validation, error handling, or framework adapters. Concentrate guards at system boundaries (CLI, config, network, external APIs); trust internal types and keep business logic in pure functions. | 238 | — |
| [`principle-build-the-lever`](repo/skills/principle-build-the-lever/SKILL.md) | user | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. Build the tool that does it or proves it (codemod, script, generator, or a skill your subagents follow) instead of working by… | 334 | — |
| [`principle-encode-lessons-in-structure`](repo/skills/principle-encode-lessons-in-structure/SKILL.md) | user | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime check, or script instead of more text. | 43 | — |
| [`principle-exhaust-the-design-space`](repo/skills/principle-exhaust-the-design-space/SKILL.md) | user | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. Build 2-3 competing prototypes and compare side by side before committing. | 20 | — |
| [`principle-experience-first`](repo/skills/principle-experience-first/SKILL.md) | user | Apply when product, UX, or feature-scope tradeoffs come up. Choose user delight over implementation convenience; ship fewer polished features over more rough ones. | 148 | — |
| [`principle-explain-the-number`](repo/skills/principle-explain-the-number/SKILL.md) | user | Apply before you measure, and before you trust, report, or act on a number you measured: a speedup, a regression, a throughput, a latency, or an eval result. Find what limits it, and rule out that it measured something… | 279 | — |
| [`principle-fix-root-causes`](repo/skills/principle-fix-root-causes/SKILL.md) | user | Apply when debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate. | 285 | — |
| [`principle-foundational-thinking`](repo/skills/principle-foundational-thinking/SKILL.md) | user | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. Get the data structures right so downstream code becomes obvious. | 172 | — |
| [`principle-guard-the-context-window`](repo/skills/principle-guard-the-context-window/SKILL.md) | user | Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads. | 35 | — |
| [`principle-laziness-protocol`](repo/skills/principle-laziness-protocol/SKILL.md) | user | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. Bias toward deletion and the smallest change that solves the problem. | 47 | — |
| [`principle-make-operations-idempotent`](repo/skills/principle-make-operations-idempotent/SKILL.md) | user | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. Converge to the same end state regardless of partial prior runs. | 259 | — |
| [`principle-migrate-callers-then-delete-legacy-apis`](repo/skills/principle-migrate-callers-then-delete-legacy-apis/SKILL.md) | user | Apply when introducing a new internal API while old callers still exist. Migrate callers and delete the old API in the same wave instead of preserving compatibility layers. | 55 | — |
| [`principle-minimize-reader-load`](repo/skills/principle-minimize-reader-load/SKILL.md) | user | Apply when reviewing or shaping code that's hard to trace. Count layers between question and answer, and hidden state in the reader's head; collapse one-caller wrappers and shrink mutable scope. | 269 | — |
| [`principle-model-the-domain`](repo/skills/principle-model-the-domain/SKILL.md) | user | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. | 271 | — |
| [`principle-never-block-on-the-human`](repo/skills/principle-never-block-on-the-human/SKILL.md) | user | Apply when tempted to ask 'should I do X?' on reversible work. | 117 | — |
| [`principle-outcome-oriented-execution`](repo/skills/principle-outcome-oriented-execution/SKILL.md) | user | Apply during planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture; don't preserve smooth intermediate states with throwaway compatibility code. | 105 | — |
| [`principle-prove-it-works`](repo/skills/principle-prove-it-works/SKILL.md) | user | Apply after completing a task, before declaring done. Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or 'it compiles.' | 172 | — |
| [`principle-redesign-from-first-principles`](repo/skills/principle-redesign-from-first-principles/SKILL.md) | user | Apply when integrating a new requirement into an existing design. | 93 | — |
| [`principle-separate-before-serializing-shared-state`](repo/skills/principle-separate-before-serializing-shared-state/SKILL.md) | user | Apply when concurrent actors might write to the same file, branch, key, or state object. Eliminate the sharing first; serialize structurally only when one shared writer is a real invariant. | 182 | — |
| [`principle-sequence-verifiable-units`](repo/skills/principle-sequence-verifiable-units/SKILL.md) | user | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. Break work into small units that each end in a verifiable state, check each before the next, and order delivery… | 227 | — |
| [`principle-subtract-before-you-add`](repo/skills/principle-subtract-before-you-add/SKILL.md) | user | Apply when sequencing an addition, refactor, or rewrite. Remove dead code, redundant validators, and stub references first, then build on the simpler base. | 102 | — |
| [`principle-test-behavior-not-implementation`](repo/skills/principle-test-behavior-not-implementation/SKILL.md) | user | Apply when you write, change, or keep a test. Assert what the code's users can observe, so that the test fails when that behavior breaks and keeps passing when only the internals change. | 411 | — |
| [`principle-type-system-discipline`](repo/skills/principle-type-system-discipline/SKILL.md) | user | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. Make illegal states unrepresentable, brand semantic primitives, parse external data at boundaries, exhaust… | 168 | — |
| [`recall`](repo/skills/recall/SKILL.md) | user | Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X',… | 801 | — |
| [`reflect`](repo/skills/reflect/SKILL.md) | user | Spawn three parallel review subagents over the active transcript, surface learnings, and route each to a concrete edit on an existing skill. Use when the user says reflect. | 680 | references |
| [`setup-pstack`](repo/skills/setup-pstack/SKILL.md) | model | Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack… | 1170 | — |
| [`sharpen`](repo/skills/sharpen/SKILL.md) | user | Make a task deeper, not bigger, then rewrite the prompt. Use for /sharpen. | 124 | — |
| [`show-me-your-work`](repo/skills/show-me-your-work/SKILL.md) | user | Keep a reviewable decision trail for long-running or unattended work: a TSV log with one row per decision (what, why, evidence, result). Local by default; commit it when a reviewer needs the trail to trust the result.… | 1038 | references, scripts |
| [`statechart`](repo/skills/statechart/SKILL.md) | user | Check a TLA+ model of a system that moves between states, such as a product flow, a protocol, or a service, and draw it as a Mermaid statechart. The report gives the shortest path to each state that breaks a rule. Use… | 1646 | references, scripts |
| [`swarm`](repo/skills/swarm/SKILL.md) | user | Fan out N parallel workers, drain them, and return one report. Use for /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration. | 428 | — |
| [`tdd`](repo/skills/tdd/SKILL.md) | user | Use only when the user explicitly asks for TDD, a failing test, or a regression test, OR when the bug has an obvious cheap local test target. Skip when the test path is unclear, expensive, integration-heavy, or not… | 443 | — |
| [`teach`](repo/skills/teach/SKILL.md) | user | Explain a body of work plainly so a person actually understands it. Runs the `how` and `why` skills and weaves what they find into one clear explanation. Use for 'teach me this', 'help me really understand X', 'explain… | 920 | — |
| [`technical-writing`](repo/skills/technical-writing/SKILL.md) | user | Layered technical-writing standard: Diátaxis structure, Google developer style sentences, STE instruction rules, Global English syntax. Use for /technical-writing or when writing or reviewing docs, RFCs, readmes, PR… | 1479 | — |
| [`typescript-best-practices`](repo/skills/typescript-best-practices/SKILL.md) | user | TypeScript best practices. Use when reading or editing any .ts or .tsx file. | 414 | references |
| [`unslop`](repo/skills/unslop/SKILL.md) | user | Cut AI tells from any writing. | 878 | — |
| [`why`](repo/skills/why/SKILL.md) | user | Use for 'why does X work this way', 'why we picked Y', design rationale, regressions, postmortems, or data-backed thresholds. Returns a cited read on decisions and tradeoffs. Use how for runtime behavior. | 50 | — |

## Références explicites entre skills

| Depuis | Vers | Mentions |
|---|---|---:|
| `poteto-help` | `poteto-mode` | 32 |
| `poteto-help` | `setup-pstack` | 13 |
| `teach` | `why` | 7 |
| `poteto-help` | `automate-me` | 6 |
| `poteto-help` | `reflect` | 6 |
| `teach` | `how` | 6 |
| `create-formal-verification-skill` | `statechart` | 5 |
| `ketchup-video` | `ketchup` | 5 |
| `poteto-help` | `architect` | 5 |
| `poteto-help` | `how` | 5 |
| `poteto-help` | `ketchup` | 5 |
| `poteto-help` | `teach` | 5 |
| `poteto-help` | `arena` | 4 |
| `poteto-help` | `blast-radius` | 4 |
| `poteto-help` | `create-formal-verification-skill` | 4 |
| `poteto-help` | `create-verification-skill` | 4 |
| `poteto-help` | `figure-it-out` | 4 |
| `poteto-help` | `interrogate` | 4 |
| `poteto-help` | `maintain-formal-verification-skill` | 4 |
| `poteto-help` | `recall` | 4 |
| `poteto-help` | `swarm` | 4 |
| `poteto-help` | `why` | 4 |
| `poteto-mode` | `setup-pstack` | 4 |
| `ketchup` | `bro` | 3 |
| `poteto-help` | `benchmark-checklist` | 3 |
| `poteto-help` | `bro` | 3 |
| `poteto-help` | `correct` | 3 |
| `poteto-help` | `in-your-own-words` | 3 |
| `poteto-help` | `ketchup-video` | 3 |
| `poteto-help` | `maintain-verification-skill` | 3 |
| `poteto-help` | `make-bot-ui` | 3 |
| `poteto-help` | `no-comments` | 3 |
| `poteto-help` | `sharpen` | 3 |
| `poteto-help` | `show-me-your-work` | 3 |
| `poteto-help` | `statechart` | 3 |
| `poteto-help` | `tdd` | 3 |
| `poteto-help` | `technical-writing` | 3 |
| `poteto-help` | `typescript-best-practices` | 3 |
| `poteto-help` | `unslop` | 3 |
| `blast-radius` | `how` | 2 |

93 arêtes explicites au total. Elles surestiment les dépendances réelles : un skill peut citer un autre skill sans en dépendre.
