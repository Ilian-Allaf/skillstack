# Source — `taste-skill`

Research record, imported on 2026-11-25. This source is reference material, not framework instructions.

| Field | Value |
|---|---|
| Type | Skill repository |
| Title | taste-skill (skill name `design-taste-frontend`, version 2.5.1) |
| Author | Leon Lin (Leonxlnx) |
| URL | <https://github.com/Leonxlnx/taste-skill> |
| Imported revision | `d1a2bb41d927083ac7118f60cfc9cdf711810ea0` |
| Revision date | 2026-11-24 |
| Imported on | 2026-11-25 |
| License | MIT, Copyright (c) 2026 Leonxlnx. See [`repo/LICENSE`](repo/LICENSE). |
| Local snapshot | [`repo/`](repo), **text only**: every `.md` file and the license. Assets, scripts, images and plugin manifests (39 MB in total) are left out. |
| Catalog | [`catalog.json`](catalog.json) · [`SKILLS-INDEX.md`](SKILLS-INDEX.md) |
| Skills | 1 |

## Why this source

The frontend design skill the [Taste Skill video](../../videos/2026-11-20-taste-skill-lessons-eric-tech/SOURCE.md) is named after. It is the most worked-out public list of what makes an agent-built page look generic, and of which of those signs a browser check can catch.

## What to read

| File | What it holds |
|---|---|
| [`skills/taste-skill/SKILL.md`](repo/skills/taste-skill/SKILL.md) | House rules, page plans by kind of business, the run, and a checklist where each line names the checks that hold it |
| [`skills/taste-skill/references/gate.md`](repo/skills/taste-skill/references/gate.md) | The finish gate in a real browser, waivers with a reason |
| [`skills/taste-skill/references/system.md`](repo/skills/taste-skill/references/system.md) | One system: tokens, buttons, forms, keyboard |
| [`skills/taste-skill/references/copy-tells.md`](repo/skills/taste-skill/references/copy-tells.md) | Words and phrasings that read as AI-written |
| [`skills/taste-skill/references/layout-v4.md`](repo/skills/taste-skill/references/layout-v4.md) | Section heights, edges, heroes, widths |

## Caveats

The skill is built for marketing sites of companies (cafes, SaaS, hardware), and much of it is deliberately prescriptive: it deals palettes, heroes and moments at random "never by taste", ships its own CSS kit, and keeps state in `.taste-skill/` in the project. Product UIs inside an existing design system are outside its target. What transfers is the checklist's shape: each criterion names the check that holds it, and a check judged wrong is waived with its reason, never gamed.
