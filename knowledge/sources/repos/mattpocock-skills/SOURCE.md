# Source — Matt Pocock, `mattpocock/skills`

## Fiche

| Champ | Valeur |
|---|---|
| Type | Dépôt de skills |
| Titre | Skills For Real Engineers |
| Auteur | Matt Pocock |
| URL | <https://github.com/mattpocock/skills> |
| Révision importée | `5863806dd4e15c63174bee4e7515a4256792ecfa` |
| Date de révision | 2026-11-12 |
| Importé le | 2026-11-16 |
| Licence | MIT — Copyright (c) 2026 Matt Pocock |
| Snapshot local | [`repo/`](repo) |
| Catalogue | [`catalog.json`](catalog.json) · [`SKILLS-INDEX.md`](SKILLS-INDEX.md) |
| Skills | 39 (20 engineering, 7 productivity, 4 misc, 8 in-progress) |

## Pourquoi cette source

C'est le corpus le plus pédagogique des trois. Matt Pocock documente non seulement les skills, mais aussi les **raisons** derrière leur découpe : contexte, charge cognitive, divulgation progressive, routage, phases, graphe de tâches. Le repo contient une théorie complète de l'écriture de documents pour agents dans `writing-for-agents`, et un routeur explicite `ask-matt` qui décrit le parcours idée → livraison.

## Ce qui a été importé

Le snapshot complet du dépôt, moins `.git` et `node_modules` :

```text
repo/
├── skills/
│   ├── engineering/        # 20 skills : grill, spec, tickets, implement, review, tdd, debug…
│   ├── productivity/       # 7 skills : grilling, handoff, teach, writing-for-agents…
│   ├── misc/               # 4 skills : hooks git, pre-commit, migration shoehorn…
│   └── in-progress/        # 8 skills : software-factory, chief-of-staff, writing…
├── docs/                   # documentation générée par skill
├── .agents/                # règles internes et ADRs du dépôt
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── GLOSSARY.md
├── SCOPE.md
├── LICENSE
└── package.json / scripts
```

Les fichiers `.out-of-scope/*.md` ont aussi été conservés : ils documentent des idées de skills **rejetées** ou repoussées, ce qui est une source précieuse pour éviter de reproduire les mêmes erreurs.

## Architecture observée

### 1. Des skills petits et composables

Le README revendique explicitement le contraire des frameworks qui « possèdent le process » (GSD, BMAD, Spec-Kit) : les skills doivent être **petits, faciles à adapter et composables**. La personnalisation est attendue, pas combattue.

### 2. Un routeur humain : `ask-matt`

`ask-matt` est un skill **user-invoked** (`disable-model-invocation: true`) qui sert de carte du système. Il ne déclenche rien lui-même : il nomme les skills et dit quand les utiliser. C'est un routeur pour l'humain, pas un orchestrateur automatique.

Il distingue quatre objets :

- **main flow** : `grill-with-docs → (prototype) → to-spec → to-tickets → implement / implement-spec → code-review → pr → retro` ;
- **on-ramps** : `triage`, `diagnosing-bugs`, `wayfinder` ;
- **codebase health** : `improve-codebase-architecture` ;
- **vocabulary layers** : `domain-modeling`, `codebase-design` — des skills de référence mobilisés par les autres.

### 3. Le graphe de tâches comme primitive d'orchestration

`to-tickets` transforme un spec en **tickets tracer-bullet**, chacun déclarant ses **blocking edges**. Le résultat n'est pas une liste d'étapes mais un **graphe orienté acyclique** avec une **frontière** de tickets prêts.

`implement-spec` exploite ce graphe :

1. lire le graphe ;
2. lancer un subagent d'exploration ;
3. créer une branche d'intégration ;
4. lancer un implementer par ticket, dans son propre worktree ;
5. merger via un merger subagent ;
6. recalculer la frontière et lancer les tickets suivants ;
7. une seule code review finale sur la branche d'intégration.

C'est le modèle le plus directement réutilisable pour un orchestrateur de skills : **les nœuds sont des tickets, les arêtes sont des blocages, l'exécution suit la frontière**.

### 4. La séparation par invocation

`writing-for-agents/SKILL-MECHANICS.md` formalise deux mécanismes :

- **model-invoked** : le skill garde une `description`, peut être déclenché par l'agent ou par un autre skill, mais coûte du contexte à chaque tour ;
- **user-invoked** : `disable-model-invocation: true`, zéro charge de contexte, mais l'humain doit savoir qu'il existe.

Un **router skill** est la réponse à la charge cognitive quand les skills user-invoked se multiplient : un seul skill à mémoriser, qui pointe vers les autres.

### 5. La théorie de l'écriture pour agents

`writing-for-agents` est peut-être le document le plus important du corpus pour notre projet. Il définit :

- **context pointer** : une référence hors contexte qui encode la condition pour y accéder ;
- **context load** vs **cognitive load** ;
- **hiérarchie de l'information** : étape dans le fichier, référence dans le fichier, référence divulguée ;
- **progressive disclosure** et **co-location** ;
- **completion criteria** : clarté et exigence, pour éviter la complétion prématurée ;
- **leading words** : un token pré-entraîné qui ancre un comportement (_tracer bullet_, _fog of war_) ;
- **negation** : dire le positif plutôt que l'interdit ;
- **pruning** : single source of truth, relevance, no-ops, sédiment.

## Skills notables

| Skill | Rôle | Pourquoi le lire |
|---|---|---|
| `ask-matt` | Routeur | Carte complète du flux idée → ship, avec on-ramps et frontières de phase |
| `writing-for-agents` | Référence | Théorie de rédaction des documents consommés par les agents |
| `to-tickets` | Planification | Tickets verticaux + blocking edges + exception wide refactor |
| `implement-spec` | Orchestration | Exécution parallèle par frontière de graphe, worktrees, merger subagents |
| `code-review` | Vérification | Revue à deux axes : Standards et Spec, en subagents parallèles |
| `diagnosing-bugs` | Debug | Boucle de diagnostic qui exige une boucle de feedback rouge avant toute théorie |
| `research` | Connaissance | Recherche en sources primaires, sauvegardée en Markdown dans le repo |
| `retro` | Méta | Transforme les erreurs mécaniques en checks déterministes |
| `software-factory` | Vocabulaire | Langage partagé : task, trigger, run, runner, orchestrator, services |
| `wayfinder` | Planification | Carte de décisions pour les efforts trop gros pour une session |

## Conventions à retenir

- Frontmatter minimal : `name`, `description`, `disable-model-invocation` quand pertinent.
- Descriptions qui portent les **branches de déclenchement**, pas une identité.
- Un skill de setup par repo (`setup-matt-pocock-skills`) pour configurer tracker, labels, docs.
- Des skills de vocabulaire partagé, sans workflow, réutilisés par les autres.
- Des docs générées par skill dans `docs/`, synchronisées avec les sources.
- Un `GLOSSARY.md` et des ADRs comme mémoire durable du domaine.
- La règle « make the change easy, then make the easy change » dans `to-tickets`.
- L'exception **wide refactor** : expand → migrate par lots → contract, avec intégration finale.

## Limites et angles morts

- Peu de skills de vérification runtime : la couche « preuve d'exécution » est moins développée que dans pstack.
- Pas de playbooks séparés : les procédures longues vivent dans le `SKILL.md`, ce qui peut créer des skills très longs.
- Le routeur est purement humain : aucune politique de sélection automatique par l'agent.
- Les skills `in-progress` ne sont pas stables ; les traiter comme des hypothèses, pas comme des standards.

## Licence et attribution

MIT. Le texte original et la licence sont conservés dans [`repo/LICENSE`](repo/LICENSE). Toute réutilisation doit conserver l'attribution à Matt Pocock.
