# Base de connaissance — inspirations pour notre graphe de skills

Corpus de référence pour concevoir un ensemble de skills orchestrés en graphe, couvrant le développement logiciel complet. Rien ici n'est encore *notre* framework : ce sont les sources et ce qu'on en retient.

## Par où commencer

1. [`synthesis/00-executive-summary.md`](synthesis/00-executive-summary.md) : les dix idées clés, à lire en 10 min.
2. [`synthesis/04-framework-blueprint.md`](synthesis/04-framework-blueprint.md) : la proposition d'architecture à valider.
3. [`SKILL-CATALOG.md`](SKILL-CATALOG.md) : les 109 skills importés, classés et reliés.

## Organisation

```text
knowledge/
├── README.md                 ← ce fichier
├── SOURCES.md                registre humain : provenance, révisions, licences
├── sources.json              registre machine
├── SKILL-CATALOG.md          index global des skills (généré)
├── skill-catalog.json        catalogue global avec les arêtes du graphe (généré)
├── sources/
│   ├── repos/<repo>/         SOURCE.md · SKILLS-INDEX.md · catalog.json · repo/ (snapshot)
│   ├── videos/<date-slug>/   SOURCE.md · transcript.md · nectar.md · raw/segments.json
│   └── articles/<date-slug>/ SOURCE.md · content.md · nectar.md · assets/
├── synthesis/                analyses transverses (anatomie, orchestration, qualité, blueprint…)
└── tools/                    scripts de collecte et de régénération
```

## Sources

| Type | Source | Accès rapide |
|---|---|---|
| Repo | `mattpocock/skills` (39 skills) | [index](sources/repos/mattpocock-skills/SKILLS-INDEX.md) |
| Repo | `cursor/plugins/pstack` (61 skills) | [index](sources/repos/cursor-pstack/SKILLS-INDEX.md) |
| Repo | `t3dotgg/tstack` (9 skills) | [index](sources/repos/t3dotgg-tstack/SKILLS-INDEX.md) |
| Vidéo | Lauren Tan, *All Code Is Slop* | [nectar](sources/videos/2026-11-14-all-code-is-slop-lauren-tan/nectar.md) · [transcript](sources/videos/2026-11-14-all-code-is-slop-lauren-tan/transcript.md) |
| Vidéo | Ray Amjad, *What Comes After Loops* | [nectar](sources/videos/2026-11-04-what-comes-after-loops-ray-amjad/nectar.md) · [transcript](sources/videos/2026-11-04-what-comes-after-loops-ray-amjad/transcript.md) |
| Article | Anthropic, *Building always-on agents* | [nectar](sources/articles/2026-11-13-building-always-on-agents/nectar.md) · [contenu](sources/articles/2026-11-13-building-always-on-agents/content.md) |
| Article | Anthropic, *Patterns and problems in emerging multiagent systems* | [nectar](sources/articles/2026-08-13-multiagent-systems/nectar.md) · [contenu](sources/articles/2026-08-13-multiagent-systems/content.md) |
| Article | Anthropic, *When to fold subagents into your main agent loop* | [nectar](sources/articles/2026-10-22-fold-subagents-into-main-loop/nectar.md) · [contenu](sources/articles/2026-10-22-fold-subagents-into-main-loop/content.md) |
| Article | Anthropic, *Harness design for long-running application development* | [nectar](sources/articles/2026-03-24-harness-design-long-running-apps/nectar.md) · [contenu](sources/articles/2026-03-24-harness-design-long-running-apps/content.md) |

## Synthèses

| Fichier | Sujet |
|---|---|
| [`00-executive-summary.md`](synthesis/00-executive-summary.md) | Synthèse exécutive |
| [`01-skill-anatomy.md`](synthesis/01-skill-anatomy.md) | Anatomie d'un bon skill |
| [`02-orchestration-patterns.md`](synthesis/02-orchestration-patterns.md) | Patterns d'orchestration |
| [`03-verification-and-quality.md`](synthesis/03-verification-and-quality.md) | Vérification et qualité |
| [`04-framework-blueprint.md`](synthesis/04-framework-blueprint.md) | Blueprint du framework |
| [`05-source-comparison.md`](synthesis/05-source-comparison.md) | Comparaison des sources |
| [`06-glossary.md`](synthesis/06-glossary.md) | Glossaire |

## Maintenance

Voir [`tools/README.md`](tools/README.md) pour rafraîchir un repo, ajouter une vidéo ou régénérer le catalogue.
