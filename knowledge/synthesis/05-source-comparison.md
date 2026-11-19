# Comparaison des sources

**But** : confronter les six sources pour identifier les convergences, les contradictions et les angles morts. C'est le document qui évite de recopier une source unique.

---

## 1. Tableau comparatif

| Critère | Matt Pocock | pstack | tstack | Lauren Tan | Ray Amjad | Anthropic |
|---|---|---|---|---|---|---|
| **Question centrale** | Comment écrire des skills composables ? | Comment faire tourner une équipe d'agents en production ? | Comment livrer une PR de bout en bout ? | Comment faire confiance à un agent à haute vélocité ? | Comment coordonner plusieurs agents ? | Comment rendre un agent durable ? |
| **Unité d'orchestration** | Flow / phase / ticket | Mode / playbook | Skill / PR | Boucle interne + outer loop | Barreau de l'échelle | Run / session |
| **Mécanisme de qualité** | Spec, tickets, review à deux axes, TDD | Principes, preuve, eval, vérification | Proof, merge gate, council | Checks déterministes, vérification runtime/formelle | Verifier à la frontière, pairs | Permissions, mémoire, outbox |
| **Autonomie** | Modérée, humaine aux frontières | Réversible auto, irréversible pause | Grant explicite, merge gate | Forte, avec environnement de confiance | Variable selon le barreau | Auto mode + deferred calls |
| **Durabilité** | Faible (session, handoff) | Moyenne (état, reprise) | Faible (watcher) | Faible (session) | Moyenne (manager thread) | Forte (inbox, timers, mémoire) |
| **Invocation** | Mixte, routeur humain | Mode user-invoked + briques | Model-invoked par triggers | N/A | N/A | N/A |
| **Points forts** | Théorie, pédagogie, graphe de tickets | Orchestration, playbooks, méta | Contrat de livraison, preuve | Modèle de qualité, encodage structurel | Topologie, lucidité sur les limites | Durabilité, primitives |
| **Points faibles** | Peu de runtime, skills longs | Monolithe, dense, Cursor-centric | Étroit (PR), pas de design | Peu de coordination | Source secondaire, chiffres locaux | Pas de skills, pas de topologie |

---

## 2. Convergences

Les six sources s'accordent sur sept points.

### 2.1 La qualité est un investissement, pas un coût

Toutes les sources refusent l'idée qu'on peut augmenter la vélocité en baissant les standards. Lauren Tan l'exprime le plus clairement, mais tstack (proof, merge gate), pstack (verify, eval) et Matt (review, TDD) vont dans le même sens.

### 2.2 Le contexte est une ressource rare

Matt formalise `context load` vs `cognitive load`. pstack parle de `guard the context window`. Ray montre les limites du fan-out. Anthropic garde l'overhead lean et utilise la compaction.

**Consensus** : ne pas charger ce qui n'est pas nécessaire ; divulguer progressivement ; communiquer par pointeurs.

### 2.3 Les skills doivent être petits et composables

Matt : « small, easy to adapt, composable ». pstack : des briques, des playbooks, des principes. tstack : 9 skills qui s'appellent. Aucune source ne défend le skill monolithique.

### 2.4 La vérification est le goulot

Lauren : 70 % des tokens. Ray : le verifier est le gain principal. tstack : la preuve est la condition du merge. pstack : `prove-it-works`, `benchmark-checklist`. Anthropic : permissions et gates.

### 2.5 La topologie doit être adaptée

Ray l'explicite, mais les autres l'implémentent : Matt a le DAG de tickets, pstack a `swarm` vs `arena`, tstack a `council` vs `sol-loop`, Anthropic a un run unique vs un swarm.

### 2.6 Le déterminisme bat la prose

Lauren est la plus radicale, mais Matt (`encode lessons in structure`), pstack (`correct`), tstack (merge gate) et Anthropic (permissions, gates) partagent l'idée : une règle qui n'est pas exécutable est fragile.

### 2.7 La méta-amélioration est nécessaire

Matt (`retro`), pstack (`reflect`, `correct`, `eval`), tstack (leçons dans le README), Lauren (chaque correction devient un check), Ray (stress-test du harnais), Anthropic (dreaming). Tous ferment la boucle, à des degrés divers.

---

## 3. Divergences

### 3.1 Planifier ou non

| Source | Position |
|---|---|
| Matt | Spec + tickets + DAG pour le multi-session |
| pstack | « I don't believe in planning. The best spec is code. » |
| Ray | Ne pas décomposer un spec en tickets par défaut |
| Anthropic | La progression doit être persistée, pas nécessairement un plan |

**Analyse** : les positions ne sont pas contradictoires si on distingue :

- **planification de découverte** : clarifier un problème flou (grill, research, prototype) ;
- **planification d'exécution** : découper un travail connu en unités.

pstack rejette la seconde comme défaut, pas la première. Ray rejette la décomposition **non prouvée**. Matt l'utilise quand le travail dépasse une session.

**Synthèse** : planifier quand l'incertitude ou la taille le justifie ; sinon, laisser l'agent choisir ses étapes. Dans tous les cas, persister l'état.

### 3.2 Décomposer ou compacter

| Source | Position |
|---|---|
| Matt | Tickets pour les gros travaux, un par contexte |
| Ray | La compaction rend la décomposition moins nécessaire |
| Anthropic | La compaction perd du détail ; persister ce qui compte |

**Analyse** : la décomposition et la compaction sont deux réponses à des problèmes différents.

- Décomposition : permettre le **parallélisme** et l'**isolation**.
- Compaction : permettre la **continuité** dans un contexte long.

**Synthèse** : décomposer seulement quand les frontières sont **vérifiables** ; sinon, compacter et persister les décisions.

### 3.3 Rôles et personas

| Source | Position |
|---|---|
| Ray | Les rôles/personas produisent de la bureaucratie et stagnent |
| pstack | Des skills fonctionnels, pas des personnages |
| tstack | Des skills nommés par action (`file-pr`, `babysit-pr`) |
| Matt | Des skills nommés par méthode (`tdd`, `code-review`) |

**Consensus** : nommer par **fonction**, pas par **personnage**. Un skill « architecte senior » est moins utile qu'un skill « architect » qui décrit une méthode.

### 3.4 Invocation

| Source | Stratégie |
|---|---|
| Matt | 15 model-invoked / 24 user-invoked, routeur humain |
| pstack | 1 model-invoked / 60 user-invoked, mode comme porte d'entrée |
| tstack | 9 model-invoked, triggers verbaux |

**Analyse** : plus le système est large, plus il faut un routeur et une discipline d'invocation. tstack peut se permettre 9 model-invoked parce que le domaine est étroit.

**Synthèse** : un routeur user-invoked pour l'humain ; des skills de phase model-invoked quand ils doivent se déclencher seuls ; des skills de référence user-invoked ou pointés.

### 3.5 Vérification

| Source | Accent |
|---|---|
| Lauren | Runtime, formel, property-based, feature map |
| Ray | À la frontière de capacité, pas partout |
| tstack | Proof + merge gate |
| pstack | `prove-it-works`, benchmark, eval |
| Matt | Review à deux axes, TDD |
| Anthropic | Permissions, gates, outbox |

**Synthèse** : empiler les niveaux, choisir le moins cher qui prouve, et placer le verifier là où le risque est réel.

### 3.6 Autonomie

| Source | Modèle |
|---|---|
| pstack | Réversible auto, irréversible pause |
| tstack | Grant explicite, merge gate, escalade |
| Anthropic | Auto mode + deferred calls + proxy credentials |
| Matt | Humain aux frontières de phase |
| Lauren | Confiance acquise par l'environnement |
| Ray | Dépend du barreau |

**Synthèse** : une politique graduée (0–3), avec des gates explicites et des grants bornés.

---

## 4. Couverture par phase du cycle de vie

| Phase | Matt | pstack | tstack | Lauren | Ray | Anthropic |
|---|---|---|---|---|---|---|
| **Découverte du besoin** | `grill-with-docs`, `research` | `sharpen`, `in-your-own-words` | — | — | — | — |
| **Spécification** | `to-spec`, `to-tickets` | — (anti-planning) | — | — | — | — |
| **Design** | `prototype`, `codebase-design` | `architect`, `arena` | — | — | — | — |
| **Implémentation** | `implement`, `tdd` | playbooks feature/bug/refactor | `full-send` | boucle interne | builder | — |
| **Vérification** | `code-review`, `diagnosing-bugs` | verify, formal, benchmark | `sol-loop`, proof | runtime/formel | verifier | permissions |
| **Livraison** | `pr` | `babysit`, `shipping` | `file-pr`, `babysit-pr`, merge | outer loop | — | outbox |
| **Opération** | — | `worktree-cleanup`, `reflect` | `modernize`, `takeover` | monitoring implicite | — | inbox/timers |
| **Méta** | `retro` | `correct`, `reflect`, `eval` | README | chaque correction → check | stress-test harnais | dreaming |

**Lecture** : aucun corpus ne couvre tout. Matt et pstack couvrent le début et le milieu ; tstack couvre la fin ; Anthropic couvre l'opération durable. C'est précisément l'espace de notre framework.

---

## 5. Ce que chaque source fait le mieux

| Source | Meilleur pour | À lire en premier |
|---|---|---|
| **Matt Pocock** | Comprendre la **théorie** des skills et le flux idée → ship | `writing-for-agents`, `ask-matt` |
| **pstack** | Voir un **système complet** en production | `poteto-mode`, playbooks `authoring-a-skill` et `eval` |
| **tstack** | Définir un **contrat de livraison** fiable | `full-send`, `council` |
| **Lauren Tan** | Comprendre pourquoi le **codebase et la vérification** priment | nectar + transcript |
| **Ray Amjad** | Choisir la **topologie** selon le couplage | nectar + transcript |
| **Anthropic** | Concevoir la **durabilité** | article + nectar |

---

## 6. Les angles morts du corpus

Le corpus est riche en **ingénierie de code**, pauvre en d'autres domaines. Voici ce qu'il ne couvre pas, et qu'il faudra chercher ailleurs ou construire.

### 6.1 Découverte produit

Aucun skill ne traite vraiment :

- la recherche utilisateur ;
- la validation d'un problème ;
- la priorisation ;
- les métriques produit ;
- l'alignement avec le business.

`grill-with-docs` et `research` aident, mais ce sont des skills d'ingénierie, pas de product management.

### 6.2 Design UX / UI

`prototype`, `visual-parity`, `experience-first` effleurent le design, mais il n'y a pas de méthode de design system, d'accessibilité, de recherche UX, ou de test utilisateur.

### 6.3 Sécurité

`git-guardrails`, `permissions`, `interrogate` couvrent des morceaux, mais pas :

- threat modeling ;
- sécurité des dépendances ;
- secrets management ;
- audit ;
- réponse à incident.

### 6.4 Données et migrations

`to-tickets` mentionne les wide refactors, mais il n'y a pas de skill dédié aux migrations de données, aux rollbacks, aux schémas versionnés, ou aux données personnelles.

### 6.5 Opérations / SRE

Pas de skill pour :

- observabilité ;
- runbooks ;
- gestion d'incident ;
- post-mortem ;
- capacity planning ;
- coûts cloud.

### 6.6 Coordination d'équipe

Les skills sont个体-centric. Il n'y a pas de pattern pour :

- plusieurs humains sur le même repo ;
- revue de code humaine à grande échelle ;
- transfert de connaissance ;
- onboarding ;
- gouvernance des skills.

### 6.7 Évaluation

pstack a un protocole d'eval, mais le corpus manque de :

- jeux de données de référence ;
- métriques standardisées ;
- benchmarks reproductibles ;
- comparaison entre frameworks.

### 6.8 Multi-repo / monorepo

Peu de contenu sur :

- les dépendances entre repos ;
- les changements atomiques multi-repo ;
- les versions ;
- les contrats d'API.

### 6.9 Artefacts non-code

Les skills sont très orientés code. Peu de choses sur :

- la documentation produit ;
- les specs fonctionnelles ;
- les contrats ;
- les présentations ;
- la communication client.

### 6.10 Coût et économie

Le corpus parle de tokens, mais peu de :

- budget par tâche ;
- coût par feature ;
- arbitrage modèle/cost ;
- mesure du ROI.

---

## 7. Ordre de lecture recommandé

Pour quelqu'un qui découvre le corpus :

1. **`synthesis/00-executive-summary.md`** — la vue d'ensemble.
2. **`synthesis/01-skill-anatomy.md`** — la grammaire.
3. **`synthesis/02-orchestration-patterns.md`** — les topologies.
4. **`synthesis/03-verification-and-quality.md`** — la preuve.
5. **`synthesis/04-framework-blueprint.md`** — la cible.
6. Puis les sources :
   - `mattpocock-skills/repo/skills/productivity/writing-for-agents/SKILL.md` ;
   - `cursor-pstack/repo/skills/poteto-mode/SKILL.md` ;
   - `cursor-pstack/repo/skills/poteto-mode/playbooks/eval.md` ;
   - `t3dotgg-tstack/repo/skills/full-send/SKILL.md` ;
   - les nectars des vidéos et de l'article.

---

## 8. Recommandation de synthèse

Notre framework devrait être une **synthèse sélective**, pas une copie :

- **de Matt** : la théorie de l'écriture, le graphe de tickets, la discipline d'invocation ;
- **de pstack** : les playbooks, les principes, la méta-amélioration, le routage par modèle ;
- **de tstack** : le standard de preuve, la merge gate, le grant d'autonomie ;
- **de Lauren** : la pyramide déterministe, la feature map, l'idée que chaque correction devient structure ;
- **de Ray** : la topologie selon le couplage, le trio builder/reviewer/verifier, la vérification à la frontière ;
- **d'Anthropic** : les primitives de durabilité, les gates différées, la mémoire indexée.

Et il devrait **ajouter** ce que le corpus ne couvre pas : produit, sécurité, données, opérations, évaluation standardisée.

C'est un programme de plusieurs mois, pas un sprint. La base de connaissance est la fondation ; le blueprint est la carte ; les skills seront les briques.
