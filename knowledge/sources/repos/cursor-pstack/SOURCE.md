# Source — `pstack` (Cursor plugins)

## Fiche

| Champ | Valeur |
|---|---|
| Type | Dépôt de skills (plugin) |
| Titre | pstack |
| Auteur | Lauren Tan (poteto) |
| URL | <https://github.com/cursor/plugins/tree/main/pstack> |
| Révision importée | `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7` |
| Date de révision | 2026-11-14 |
| Importé le | 2026-11-16 |
| Licence | MIT — Copyright (c) 2026 Lauren Tan |
| Snapshot local | [`repo/`](repo) |
| Catalogue | [`catalog.json`](catalog.json) · [`SKILLS-INDEX.md`](SKILLS-INDEX.md) |
| Skills | 61 fichiers `SKILL.md` : 34 skills cœur + 24 principes + 3 skills d'automation |

## Pourquoi cette source

C'est le corpus le plus proche d'un **vrai graphe de skills en production**. pstack ne se contente pas d'empiler des procédures : il définit un routeur (`poteto-mode`), des playbooks, des principes transversaux, des subagents, une politique de modèles, et des skills de méta-amélioration (`reflect`, `correct`, `eval`). C'est l'architecture de référence pour notre phase de construction.

## Ce qui a été importé

Le dossier `pstack/` complet, moins `.git` :

```text
repo/
├── skills/
│   ├── poteto-mode/        # routeur + 23 playbooks + références + scripts
│   ├── principle-*/        # 24 principes, chacun un skill
│   ├── architect/ arena/ swarm/ interrogate/ …
│   ├── create-verification-skill/ maintain-verification-skill/
│   ├── create-formal-verification-skill/ maintain-formal-verification-skill/
│   └── setup-pstack/ poteto-help/ reflect/ correct/ eval…
├── agents/                 # poteto-agent, comment-sicko
├── docs/guide/             # 10 chapitres + index
├── automations/            # 3 skills d'automation (Benny)
├── plugin.json
├── README.md
└── LICENSE
```

## Architecture observée

### 1. Un point d'entrée unique : `poteto-mode`

`poteto-mode` est le seul skill **model-invoked** du cœur (avec `setup-pstack`). C'est un **mode** : l'utilisateur l'invoque explicitement, et il reste épinglé dans le contexte pour les tours suivants. Il contient :

- les **non-negotiables** : triggers qui imposent un comportement ou un skill ;
- un **index de 24 principes** avec la condition d'application de chacun ;
- la politique d'**autonomie** : actions réversibles sans demander, pause sur les écritures irréversibles ;
- la politique de **subagents** : type, modèle, effort, fraîcheur, parallélisme ;
- la politique de **rédaction** des réponses ;
- la politique de **commentaires** ;
- la table de **routage vers 23 playbooks**.

C'est un routeur qui combine un système de règles et une bibliothèque de procédures.

### 2. Les playbooks : des procédures exécutables, pas des descriptions

Chaque playbook est un fichier Markdown avec des étapes numérotées, des critères de sortie et un format de réponse. Au démarrage, `poteto-mode` :

1. copie **verbatim** les étapes du playbook dans la todo list ;
2. exécute les étapes ;
3. appelle les autres skills quand une étape le demande.

Un playbook non choisi reste visible avec `skip: <raison>`. Cette technique rend le routage **auditable** : on voit quel chemin a été sélectionné et ce qui a été écarté.

Les 23 playbooks couvrent : investigation, bug fix, perf, hillclimb, runtime forensics, trace forensics, feature, refactoring, prototype, visual parity, authoring a skill, eval, babysit, shipping, autonomous run, orchestrate, autopilot-full, autopilot-stack, session pickup, pause safely, multi-phase plan, worktree cleanup, opening a PR.

### 3. Les principes : des skills de référence transversaux

24 principes, chacun dans son propre `SKILL.md`, regroupés en cinq familles :

| Famille | Exemples |
|---|---|
| Core | laziness protocol, foundational thinking, attack the premise, subtract before you add, build the lever |
| Architecture | model the domain, boundary discipline, type system discipline, idempotence, migrate callers then delete |
| Verification | prove it works, fix root causes, sequence verifiable units, test behavior not implementation, explain the number |
| Delegation | guard the context window, never block on the human |
| Meta | encode lessons in structure |

`poteto-mode` en embarque un **index inline** et renvoie au fichier complet quand un principe s'applique. C'est de la divulgation progressive appliquée aux règles.

### 4. Les subagents

Deux agents :

- `poteto-agent` : wrapper de tous les délégués lancés dans un playbook. Il lit `poteto-mode` en entier avant d'agir, pour éviter la dérive.
- `comment-sicko` : reviewer de commentaires en lecture seule, invoqué via `/no-comments`.

Le skill parent possède le travail : il review le diff et écrit son propre résumé, il ne relaie pas le rapport du subagent.

### 5. Le routage par modèle

`setup-pstack` détecte les modèles disponibles et écrit une règle de configuration qui mappe des **rôles** à des modèles :

- code, prose, judgment ;
- hardest tasks ;
- swarm workers ;
- panels de review et de design.

Les skills lisent cette règle et retombent sur des défauts. C'est une **configuration externe au skill**, ce qui permet de changer de modèle sans réécrire les skills.

### 6. La vérification comme couche de première classe

pstack contient des skills dédiés à la création et à la maintenance de la vérification :

- `create-verification-skill` : génère un skill de vérification projet avec une **feature map** ;
- `maintain-verification-skill` : détecte la dérive entre la feature map et l'app ;
- `create-formal-verification-skill` : modélise une propriété (TLA+, Lean, etc.) et génère un skill de recheck ;
- `benchmark-checklist` : vette un chiffre avant de le publier ;
- `prove-it-works` : vérifier l'artefact réel, pas un proxy.

### 7. La méta-amélioration

- `reflect` : capture la recette d'une tâche longue sous forme d'édition de skill ;
- `correct` : mine l'historique des corrections répétées et corrige à la **plus haute couche** qui marche (architecture, types, lint, CI, tests, docs en dernier) ;
- `eval` : compare des variantes de skills avec **blinding** strict et un juge d'une autre famille de modèles.

C'est le mécanisme qui permet à un graphe de skills de s'améliorer sans dérive.

## Skills notables

| Skill | Rôle | Pourquoi le lire |
|---|---|---|
| `poteto-mode` | Routeur | Le meilleur exemple de mode orchestrateur avec playbooks et principes |
| `authoring-a-skill` (playbook) | Méta | Règles de rédaction : « when in doubt, delete », déléguer par chemin, ne pas répéter |
| `eval` (playbook) | Méta | Protocole de test aveugle d'un skill |
| `architect` | Design | Design parallèle avant d'écrire du code qui traverse une frontière |
| `arena` | Design | N tentatives, sélection d'une base, greffe des meilleures parties |
| `swarm` | Exécution | N workers sur des tranches indépendantes, un rapport agrégé |
| `interrogate` | Review | Review multi-modèles adversarial, ne garde que les findings prouvés |
| `create-verification-skill` | Vérification | Génère la preuve runtime projet, avec feature map |
| `statechart` | Vérification | Vérifie un modèle TLA+ et dessine l'état vu par l'utilisateur |
| `correct` | Méta | Encode les corrections en structure plutôt qu'en prose |
| `reflect` | Méta | Transforme une tâche longue en amélioration de skill |

## Conventions à retenir

- Un mode/user-invoked comme point d'entrée unique ; les autres skills sont des briques.
- Des playbooks séparés pour les procédures longues, avec étapes copiées dans la todo.
- Des principes séparés, indexés inline, cités par nom.
- Un agent wrapper qui lit le mode avant d'agir.
- Une configuration de modèles par rôle, hors des skills.
- Une politique d'autonomie explicite : réversible vs irréversible.
- Une politique de subagents : frais par défaut, périmètre consolidé, parallélisme.
- Un format de réponse normé : objectif, preuve, décisions, liens.
- Des skills de méta-amélioration : `correct`, `reflect`, `eval`.

## Limites et angles morts

- Le corpus est très orienté Cursor et son écosystème (modèles, custom modes, `/loop`). Certaines mécaniques ne se transposent pas telles quelles.
- La prose est dense, parfois télégraphique ; la charge de lecture est élevée.
- Le routeur est un gros fichier de règles ; sans discipline, il peut devenir un monolithe.
- pstack revendique « pas de planning » et « le meilleur spec est le code ». C'est une position forte, à confronter aux sources qui défendent spec/tickets.
- Les 3 skills d'automation sont hors du cœur ; ne pas les compter comme des skills de développement généraux.

## Licence et attribution

MIT. Le texte original et la licence sont conservés dans [`repo/LICENSE`](repo/LICENSE). Toute réutilisation doit conserver l'attribution à Lauren Tan.
