# Blueprint du framework — proposition à valider

> **Statut** : hypothèse de conception. Aucun skill n'est encore construit.  
> **But** : donner une architecture cible, des contrats et un ordre de construction pour la phase suivante.

---

## 1. Les invariants

Dix règles non négociables, dérivées du corpus. Elles doivent tenir même si les skills changent.

1. **Un point d'entrée unique.** L'humain parle à un routeur, pas à une collection de skills.
2. **Un nœud = une responsabilité vérifiable.** Pas de skill fourre-tout.
3. **Une arête = une condition.** Pas de transition implicite.
4. **Une preuve par nœud.** Chaque nœud produit un artefact observable.
5. **Une gate par action irréversible.** Le réversible avance ; l'irréversible attend.
6. **Un budget par boucle.** Review, verify, retry : bornés.
7. **Un état externe.** Le graphe survit aux sessions et aux crashes.
8. **Une topologie par couplage.** Pipeline, DAG, fan-out, swarm, pairs.
9. **Une hypothèse de suppression.** Chaque nœud peut disparaître quand le modèle progresse.
10. **Une méta-boucle.** Le système corrige ses skills, pas seulement son code.

---

## 2. L'architecture en couches

```text
┌─────────────────────────────────────────────────────────────┐
│ 6. Méta                                                     │
│    retro · correct · reflect · eval · prune                 │
├─────────────────────────────────────────────────────────────┤
│ 5. Vérification                                             │
│    checks déterministes · runtime · formel · eval           │
├─────────────────────────────────────────────────────────────┤
│ 4. Playbooks                                                │
│    bug fix · feature · migration · incident · release …     │
├─────────────────────────────────────────────────────────────┤
│ 3. Phases                                                   │
│    discover · specify · design · build · verify · ship      │
├─────────────────────────────────────────────────────────────┤
│ 2. Router                                                   │
│    intention · topologie · plan · dispatch                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Constitution                                             │
│    principes · vocabulaire · autonomie · preuve · modèles   │
├─────────────────────────────────────────────────────────────┤
│ 0. Runtime & état                                           │
│    inbox · timers · mémoire · permissions · outbox          │
└─────────────────────────────────────────────────────────────┘
```

### Couche 0 — Runtime & état

Ce n'est pas un skill. C'est le socle qui rend le graphe durable :

- **inbox** : événements prêts à traiter ;
- **timers** : follow-ups et schedules ;
- **mémoire** : instructions, notes, progression, messages déjà envoyés ;
- **permissions** : credentials, auto mode, approbations différées ;
- **outbox** : messages et artefacts à délivrer.

**Décision à prendre** : harness natif, service externe, ou hybride.

### Couche 1 — Constitution

Les règles qui s'appliquent à tous les skills :

- principes d'ingénierie (modèle du domaine, frontières, idempotence, preuve) ;
- vocabulaire partagé (skill, run, gate, preuve, frontière) ;
- politique d'autonomie (niveaux 0–3) ;
- standard de preuve ;
- politique de modèles (rôles, fallbacks) ;
- politique de rédaction.

**Format** : des skills de référence model-invoked, ou des fichiers externes pointés. Pas un `AGENTS.md` monolithique.

### Couche 2 — Router

Le routeur reçoit l'intention et produit :

1. une **classification** (bug, feature, review, migration, incident, question) ;
2. une **topologie** (pipeline, DAG, fan-out, swarm, pairs) ;
3. un **plan** de nœuds et d'arêtes ;
4. un **budget** ;
5. des **gates**.

Il ne fait pas le travail. Il route et supervise.

### Couche 3 — Phases

Sept phases, chacune avec entrée/sortie :

| Phase | Entrée | Sortie | Gate de sortie |
|---|---|---|---|
| **Discover** | idée floue, problème | compréhension partagée | objectif et contraintes explicites |
| **Specify** | compréhension | spec / décisions | critères d'acceptation vérifiables |
| **Design** | spec | design / prototypes | décision prise, preuve que ça tient |
| **Build** | spec + design | code / artefacts | tests locaux, diff cohérent |
| **Verify** | build | preuve | gate de vérification |
| **Ship** | preuve | PR / deploy | merge gate |
| **Operate** | production | observation | incident ou prochaine itération |

**Règle** : une phase peut être sautée si l'évidence le justifie, mais la décision doit être tracée.

### Couche 4 — Playbooks

Les procédures situationnelles, séparées des phases :

- bug fix ;
- feature ;
- refactoring ;
- migration ;
- perf ;
- incident ;
- review ;
- release ;
- onboarding ;
- audit de sécurité.

Un playbook copie ses étapes dans la todo et appelle les skills de phase/vérification.

### Couche 5 — Vérification

- checks déterministes (types, lint, tests) ;
- runtime (app, browser, CDP, captures) ;
- formel (TLA+, Lean) quand justifié ;
- eval des skills.

**Règle** : chaque phase a une gate de vérification, mais le **niveau** dépend du risque.

### Couche 6 — Méta

- `retro` : erreurs → checks ;
- `correct` : corrections répétées → structure ;
- `reflect` : tâche longue → édition de skill ;
- `eval` : variantes → test aveugle ;
- `prune` : skills obsolètes → suppression.

---

## 3. Le contrat d'un nœud

Chaque skill doit déclarer :

```yaml
id: kebab-case
version: 0.1.0
kind: router | phase | playbook | principle | verification | meta | tool
title: ...
description: ...
invocation: model | user | both

triggers:
  - intent: ...
  - event: ...
  - schedule: ...

inputs:
  - name: ...
    type: artifact | text | state | event
    required: true
    source: ...

outputs:
  - name: ...
    type: artifact | state | message
    evidence: ...

preconditions:
  - ...

postconditions:
  - ...

gate:
  type: none | auto | human | mixed
  criteria:
    - ...
  on_fail: repair | escalate | abort

budget:
  max_rounds: ...
  max_tokens: ...
  max_minutes: ...

autonomy: 0 | 1 | 2 | 3

model_role: code | judgment | hardest | worker | panel

state:
  reads:
    - memory/...
  writes:
    - memory/...

parallel:
  safe_with:
    - ...
  shared_artifacts:
    - ...

hypothesis: "Ce skill existe parce que le modèle ne sait pas encore ..."

references:
  - path: ...
    when: ...
```

**Règle** : un champ absent est un choix explicite, pas un oubli. Les champs vides doivent être supprimés.

---

## 4. Le contrat d'une arête

```yaml
from: skill_id
to: skill_id
type: triggers | blocks | requires | reviews | verifies | repairs | informs | escalates | resumes | produces
condition: "..."
payload:
  - artifact_ref
on_fail: retry | repair | escalate | abort
```

**Règle** : une arête sans condition n'est pas une transition. C'est une intention.

---

## 5. Le schéma d'état

```yaml
project:
  id: ...
  repo: ...
  default_branch: ...
  constraints: [...]

task:
  id: ...
  goal: ...
  phase: discover | specify | design | build | verify | ship | operate
  status: queued | running | waiting_human | blocked | done | failed | cancelled
  priority: ...
  spec_ref: ...
  design_ref: ...
  tickets: [...]
  artifacts: [...]
  evidence: [...]
  decisions: [...]
  approvals: [...]
  budget: {...}

graph:
  nodes: [...]
  edges: [...]

runs:
  - id: ...
    skill: ...
    status: ...
    started_at: ...
    ended_at: ...
    evidence: [...]
    next: [...]

memory:
  instructions: ...
  notes: [...]
  progress: [...]
  reported: [...]

outbox:
  - id: ...
    type: message | artifact
    status: pending | sent | failed
```

**Règle** : l'état est la source de vérité. Le contexte du modèle est un cache.

---

## 6. Choisir la topologie

Le routeur classe le travail selon cinq axes :

| Axe | Question | Impact |
|---|---|---|
| **Indépendance** | Les morceaux peuvent-ils avancer sans se voir ? | DAG / fan-out / swarm |
| **Couplage** | Partagent-ils des artefacts ? | Pipeline / agent unique |
| **Exploration** | La solution est-elle inconnue ? | Arena / prototype |
| **Risque** | L'action est-elle irréversible ? | Gates humaines |
| **Taille** | Dépasse-t-elle une session ? | DAG / manager thread / always-on |

### Arbre de décision

```text
1. L'action est-elle irréversible ?
   OUI → gate humaine obligatoire, quelle que soit la topologie.

2. Le travail est-il indépendant et vérifiable par morceaux ?
   OUI → les morceaux sont-ils homogènes ?
         OUI → swarm / fan-out
         NON → DAG / frontier
   NON → le travail est-il exploratoire ?
         OUI → arena / prototype
         NON → le travail est-il couplé ?
               OUI → agent unique + compaction, ou pairs
               NON → pipeline séquentiel

3. Doute sur l'indépendance ?
   → agent unique + compaction par défaut.
   → décomposer seulement quand une frontière est prouvée.
```

**Règle** : le défaut est **un agent unique avec un bon contexte**, pas un swarm. La parallélisation est une optimisation, pas une valeur.

---

## 7. La politique d'autonomie

| Niveau | Autonomie | Exemples | Gate |
|---|---|---|---|
| **0** | Lecture seule | analyse, review, recherche | aucune |
| **1** | Écriture locale réversible | fichiers, branche, tests | aucune |
| **2** | Action externe réversible | PR, commentaire, ticket | auto ou légère |
| **3** | Action irréversible | merge, deploy, suppression, message client | humaine ou merge gate |

**Règles** :

- un skill déclare le niveau maximal qu'il peut atteindre ;
- le routeur peut **réduire** le niveau, jamais l'augmenter sans grant explicite ;
- une gate humaine est un **événement**, pas un blocage ;
- un grant (`full send`) doit énumérer ce qu'il autorise et ce qu'il n'autorise pas.

---

## 8. La politique de modèles

```yaml
roles:
  code:
    default: <modèle fort rapide>
    fallback: <modèle équivalent>
  judgment:
    default: <modèle fort>
  hardest:
    default: <modèle le plus fort>
  worker:
    default: <modèle rapide/cheap>
  panel:
    - <modèle famille A>
    - <modèle famille B>
    - <modèle famille C>
```

**Règles** :

- la config est **externe** aux skills ;
- un skill lit le rôle, pas le nom du modèle ;
- le panel reste **diversifié** ;
- un modèle rejeté n'est pas retenté à l'aveugle ;
- le choix est **rapporté** dans la sortie.

---

## 9. La structure de répertoires cible

```text
framework/
├── constitution/
│   ├── principles/
│   ├── vocabulary.md
│   ├── autonomy.md
│   ├── proof.md
│   └── models.md
├── router/
│   ├── SKILL.md
│   ├── topology.md
│   └── intent.md
├── phases/
│   ├── discover/
│   ├── specify/
│   ├── design/
│   ├── build/
│   ├── verify/
│   ├── ship/
│   └── operate/
├── playbooks/
│   ├── bug-fix/
│   ├── feature/
│   ├── refactoring/
│   ├── migration/
│   ├── perf/
│   ├── incident/
│   ├── review/
│   └── release/
├── verification/
│   ├── static/
│   ├── runtime/
│   ├── formal/
│   └── eval/
├── meta/
│   ├── retro/
│   ├── correct/
│   ├── reflect/
│   └── prune/
├── runtime/
│   ├── state-schema.md
│   ├── events.md
│   ├── memory.md
│   ├── permissions.md
│   └── outbox.md
├── templates/
│   ├── skill/
│   ├── ticket/
│   ├── spec/
│   └── evidence/
└── tools/
    ├── lint_skills.py
    ├── eval_skill.py
    └── build_catalog.py
```

**Note** : c'est une cible. Ne pas créer cette arborescence avant d'avoir validé les contrats.

---

## 10. L'ordre de construction

### Phase 0 — Base de connaissance (fait)

- importer les sources ;
- extraire les transcripts ;
- distiller les nectars ;
- produire la synthèse.

### Phase 1 — Invariants et contrats (1 session)

- valider les 10 invariants ;
- écrire le contrat de nœud et d'arête ;
- décider du schéma d'état ;
- décider de la politique d'autonomie ;
- décider du standard de preuve.

**Livrable** : `constitution/` + `runtime/state-schema.md`.

### Phase 2 — Runtime minimal

- choisir le store (fichiers, SQLite, Postgres) ;
- implémenter inbox, timers, mémoire, outbox ;
- définir les événements et les transitions ;
- instrumenter les runs.

**Livrable** : un runtime capable de lancer un skill, de persister l'état et de reprendre.

### Phase 3 — Squelette du graphe

- router ;
- 2 phases : build + verify ;
- 2 playbooks : bug fix + feature ;
- 1 gate : merge gate ;
- 1 skill de preuve runtime.

**Livrable** : une tranche verticale complète, testée sur un vrai repo.

### Phase 4 — Vérification et eval

- lint de skills ;
- eval aveugle ;
- benchmark checklist ;
- métriques de base.

**Livrable** : un skill ne peut être promu sans eval.

### Phase 5 — Extension du cycle de vie

- discover, specify, design, ship, operate ;
- playbooks migration, incident, release ;
- topologies DAG, fan-out, pairs.

**Livrable** : cycle complet idée → production.

### Phase 6 — Méta-amélioration

- retro, correct, reflect, prune ;
- revue périodique des hypothèses ;
- suppression des skills obsolètes.

**Livrable** : le graphe peut se simplifier.

### Phase 7 — Durcissement

- projets réels ;
- incidents ;
- sécurité ;
- coûts ;
- portabilité.

**Livrable** : un framework utilisé sur des projets réels, avec des métriques.

---

## 11. Ce qu'on reprend, adapte, rejette

| Source | Reprendre | Adapter | Rejeter / différer |
|---|---|---|---|
| **Matt Pocock** | `writing-for-agents`, task graph, routeur, discipline d'invocation | spec/tickets selon le couplage | pipeline rigide pour tout |
| **pstack** | playbooks, principes, méta-amélioration, routage par modèle | `poteto-mode` comme mode, pas comme monolithe | « pas de planning » comme dogme, personas |
| **tstack** | proof, merge gate, autonomy grant, council | scope PR → cycle complet | dépendance à GitHub uniquement |
| **Lauren Tan** | pyramide, encodage déterministe, feature map | bannissement avec exceptions | formel partout, métriques de volume |
| **Ray Amjad** | topologie/couplage, builder/reviewer/verifier, vérification à la frontière | manager thread selon harnais | leads/swarms comme baseline |
| **Anthropic** | inbox/timers/mémoire/permissions/outbox | runtime selon besoin réel | always-on avant d'en avoir besoin |

---

## 12. Les risques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Sur-ingénierie du runtime | Haute | Haut | Commencer par fichiers + un seul process |
| Graphe trop gros | Haute | Haut | Limite de nœuds, prune, routeur |
| Skills trop abstraits | Moyenne | Haut | Tranche verticale concrète d'abord |
| Modèles qui changent | Haute | Moyen | Hypothèses datées, eval, suppression |
| Coût des evals | Moyenne | Moyen | Evals légers, échantillonnage |
| Portabilité harnais | Moyenne | Moyen | Contrats agnostiques, adapters |
| Charge cognitive | Haute | Moyen | Un routeur, docs courtes, glossaire |
| Sécurité des permissions | Basse | Très haut | Proxy credentials, gates, moindre privilège |
| Dérive de scope | Haute | Moyen | Budgets, gates, « fight scope creep » |

---

## 13. Les décisions à prendre

Avant d'écrire le premier skill :

1. **Runtime** : harness natif, service externe, ou hybride ?
2. **Store** : fichiers, SQLite, Postgres ?
3. **Triggers** : user, CLI, git, issue tracker, timer ?
4. **Invocation** : quels skills sont model-invoked vs user-invoked ?
5. **Gates** : quelles actions sont auto, humaines, mixtes ?
6. **Topologie** : qui choisit — le routeur, l'humain, une heuristique ?
7. **Preuve** : quel standard minimal ?
8. **Eval** : quel budget, quelle fréquence ?
9. **Langue** : docs en français, skills en anglais ? (Recommandation : docs de conception en français, descriptions et corps de skills en anglais pour la performance modèle, avec un glossaire bilingue.)
10. **Distribution** : repo, plugin, marketplace ?

---

## 14. Les critères de succès

Le framework sera considéré comme réussi si :

- un nouvel ingénieur comprend le graphe en moins de 30 minutes ;
- chaque skill a un contrat complet ;
- chaque run produit une preuve ;
- chaque gate est observable ;
- un skill peut être supprimé sans casser le graphe ;
- un eval peut comparer deux variantes ;
- le taux de revert reste bas à mesure que le volume augmente ;
- le coût par changement vérifié baisse ;
- le système est utilisé sur un vrai projet, pas seulement en démo.

---

## 15. Ce qui reste ouvert

- La forme exacte du routeur (skill, service, CLI, UI).
- Le format des skills (Markdown + frontmatter, YAML, autre).
- La manière de représenter le couplage.
- La politique de mémoire à long terme.
- La stratégie de versioning des skills.
- La gouvernance des changements (qui peut modifier un skill ?).
- La relation entre skills et code exécutable (scripts, tools).
- La place de l'humain dans la boucle.

Ces questions doivent être tranchées en Phase 1, pas pendant l'écriture des skills.
