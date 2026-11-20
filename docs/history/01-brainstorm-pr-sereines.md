# Brainstorm 01 — Livrer beaucoup de PR, sereinement

> **Frozen on 2026-11-19.** History only, in French: names, decisions, and paths are those of their time and bind nothing. Decisions in force: [docs/adr/](../adr/). How the framework works today: [skills/README.md](../../skills/README.md).

> **Statut** : brainstorm. Rien n'est décidé, tout est à challenger.
> **Date** : 2026-11-16.
> **Question** : quelle est la meilleure approche pour construire notre framework de skills, afin de livrer beaucoup de PR sereinement, comme poteto (Lauren Tan) ?
> **Entrées** : [`knowledge/`](../../knowledge/README.md), en particulier le [nectar de Lauren Tan](../../knowledge/sources/videos/2026-11-14-all-code-is-slop-lauren-tan/nectar.md), les playbooks `shipping`, `autopilot-full` et `orchestrate` de pstack, `full-send` de tstack et `software-factory` de Matt Pocock.
> **Suite** : l'[architecture 02](02-architecture.md) tranche ces idées. Depuis sa v3 (2026-11-18), l'échelle de confiance (§4) et la forge comme arbitre (§5) sont abandonnées : tu merges toujours toi-même.

---

## 1. Reformuler l'objectif

« Livrer beaucoup de PR sereinement » combine deux variables :

- **le débit** : le nombre de PR mergées par semaine ;
- **la sérénité** : l'attention humaine que coûte chaque PR, et le risque qu'on accepte en ne la relisant pas.

Lauren Tan ne vise pas le débit. Elle vise la confiance, et le débit suit : 3 000 PR en un mois pour elle seule, 11 000 pour l'équipe, environ 0,5 % de revert. Il lui a fallu six mois d'investissement dans l'environnement de ses agents.

La ressource rare n'est donc pas le token, c'est l'**attention humaine**. Lauren Tan dit que la majorité de ses tokens part en vérification : on dépense des tokens pour économiser de l'attention.

**North star proposée** : les minutes d'attention humaine par PR mergée, à taux de revert constant (< 1 %).

## 2. Le constat qui change la question

Le talk de Lauren Tan, son guide pstack et le skill `software-factory` de Matt Pocock disent la même chose :

| Source | Formulation |
|---|---|
| Lauren Tan | Améliorer le codebase, puis la vérification, et seulement ensuite automatiser. « If your inner coding loop produces slop, then automating that loop just produces more slop. » |
| pstack, guide 07 | « Earn the trust before the loop » : quatre conditions à remplir avant de laisser une boucle tourner seule. |
| Matt Pocock, `software-factory` | « Accelerators without brakes make a slop cannon. » On ouvre le débit à mesure que les freins gagnent la confiance. |

**Conséquence** : un framework de skills ne produit pas la sérénité. C'est l'environnement qui la produit. Les skills sont la fine couche de prose au sommet de la pyramide. Un graphe de 50 procédures bien écrites livrerait seulement plus vite du slop.

La question devient : **quel framework de skills construit un environnement de confiance, puis l'exploite ?**

## 3. La thèse

pstack contient les briques du parcours de poteto (`create-verification-skill`, `correct`, `eval`), mais pas le parcours lui-même. Rien n'y dit à quel niveau d'autonomie un repo a droit, ni comment le mériter. C'est le vide qu'on peut combler.

> **Notre framework devrait reproduire le parcours de poteto, pas seulement son style** : faire monter un repo, étape par étape, de « je relis tout » à « je relis les preuves », puis à « je ne relis que les décisions ».

Il s'organise en quatre familles :

```text
  intention
     │
     ▼
  façonnage (si flou) ──► file d'unités vérifiables (graphe du travail)
                                   │
                                   ▼  une colonne par PR, en parallèle si indépendantes
                          ┌──────────────────┐
                          │    colonne       │  reformuler → construire → prouver → PR
                          │   vertébrale     │  → babysit → verdict indépendant → gate
                          └────────┬─────────┘
                                   │ s'appuie sur
                                   ▼
                          ┌──────────────────┐
                          │ kit de confiance │  architecture, types, lint, skill de
                          │    du repo       │  vérification, checks de CI, protection
                          └────────┬─────────┘
                                   │ nourri par
                                   ▼
                          ┌──────────────────┐
                          │   méta-boucle    │  corrections → structure, eval, prune
                          └──────────────────┘
```

1. **La colonne vertébrale** : le chemin unique de chaque changement, de l'intention à la PR mergée, avec une preuve à chaque étape.
2. **Le kit de confiance** : des skills qui écrivent l'environnement dans le repo cible (lint, types, frontières, skill de vérification, feature map, checks de CI).
3. **Le façonnage** : en amont, transformer une intention floue en une file d'unités vérifiables. Seulement quand c'est flou.
4. **La méta-boucle** : transformer chaque correction en structure, et tester chaque changement de skill.

Les sections suivantes détaillent sept idées.

## 4. Idée 1 — L'échelle de confiance

L'autonomie n'est pas un réglage global. Elle se **gagne**, niveau par niveau, **par repo et par classe de risque**, sur des critères mesurables.

| Niveau | L'agent | L'humain | Pour y entrer |
|---|---|---|---|
| **N0 · Assisté** | propose et code à la demande | fait tout le reste | rien |
| **N1 · PR prouvée** | livre une PR petite, avec une preuve observée | relit la preuve et le diff, merge | CI qui build et teste ; template de PR avec preuve |
| **N2 · PR vérifiée** | + un vérificateur indépendant rend un verdict sur la SHA | lit le verdict, survole le diff, merge | skill de vérification du repo (feature map + pilote) ; statut de verdict |
| **N3 · Autopilot-stack** | mène une file de PR en parallèle jusqu'à merge-ready, verdict compris | merge par lots, le matin | N2 tenu sur ~20 PR sans bug échappé ; journal de décisions ; rapport de rattrapage |
| **N4 · Autopilot-full par classe** | merge seul les classes à faible risque | ne voit que le risque élevé et les décisions | protection de branche qui exige le verdict ; classement automatique du risque ; revert < 1 % sur ~50 PR de la classe |
| **N5 · Boucle externe** | déclencheurs automatiques : fuzz à chaque release, triage, ratchet, retro | arbitre les décisions produit | budgets, throttles, kill switch ; N4 stable |

Les seuils (20, 50, 1 %) sont des valeurs de départ, à calibrer sur nos données.

**Le niveau dépend de la classe de risque.** Les PR de docs et de tests peuvent être en N4 pendant que l'authentification reste en N2. C'est l'application directe de « vérifier à la frontière de capacité » (Ray Amjad).

Un skill `trust-audit` mesure où en est un repo sur cette échelle et dit ce qui manque pour monter. C'est le point d'entrée du parcours.

## 5. Idée 2 — La forge fait respecter le contrat, pas la prose

Le nectar de Lauren Tan se terminait sur une question ouverte : quel est l'équivalent, pour un skill, d'un lint rule ? Proposition de réponse :

> **Chaque promesse d'un skill a un check qui la fait respecter.** Le skill dit quoi faire. La forge garantit que c'est fait.

| Promesse | Enforcement déterministe |
|---|---|
| Chaque PR porte sa preuve | check de CI `evidence` : la description contient *Pourquoi*, *Preuve* et *Risque*, avec au moins un artefact |
| L'auteur n'est jamais le juge | le vérificateur pose un statut de commit `trust/verdict` sur la SHA ; un nouveau push ne l'a pas |
| Rien ne merge sans verdict | protection de branche qui exige `trust/verdict` et la CI |
| Le risque décide du niveau | action `risk-label` qui calcule `risk:low/med/high` depuis les chemins touchés et la taille du diff, configurée dans `.trust/risk.yml` |
| Le risque élevé passe par un humain | CODEOWNERS sur les chemins sensibles |
| Personne ne contourne | pas de `--admin`, pas de bypass |

Même si un agent ignore son skill, la garantie tient. C'est la pyramide de Lauren appliquée au pipeline de PR lui-même.

**Point dur** : si l'auteur et le vérificateur partagent le même token GitHub, l'auteur peut poser le statut lui-même. Il faut une identité dédiée au vérificateur (une GitHub App, par exemple), et exiger que le statut vienne d'elle.

On reprend aussi la table de `correct` (pstack) : chaque règle du repo est associée à ce qui l'applique. Une règle sans enforcement est signalée comme faible.

## 6. Idée 3 — Une colonne vertébrale unique

Chaque changement suit le même chemin :

```text
intention
  → reformuler     objectif, problème, plus petit changement (une erreur de lecture coûte un message)
  → construire     playbook selon l'intention : bug, feature, refactor, perf
  → prouver        sur l'artefact réel, via le skill de vérification du repo
  → ouvrir la PR   petite ; pourquoi, preuve, risque, modèle utilisé
  → babysit        conflits, puis reviews, puis CI ; triage sceptique ; fixes groupés
  → vérifier       agent frais, autre famille de modèle, verdict PASS / PASS+NOTES / FAIL sur la SHA
  → gate           selon niveau × risque : merge, ou humain
  → journal        une ligne par décision
```

Règles reprises du corpus :

- **L'humain déclare le grant, le routeur choisit le playbook.** Les points d'entrée se nomment par autonomie, pas par phase : `full send` / `full stop` chez tstack, `autopilot-full` / `autopilot-stack` chez pstack.
- **Un propriétaire par PR, un juge différent par verdict.** Seul le propriétaire pousse sur sa branche (pstack `orchestrate`).
- **Vert n'est pas sûr.** La CI est une entrée du verdict, pas le verdict.
- **Un verdict couvre un patch** (`git patch-id`), pas une branche. Un rebase qui change le patch demande un nouveau verdict.
- **Une question à l'humain est une vraie décision.** Si la réponse est observable, on prototype au lieu de demander. Sinon, la question arrive avec son contexte, des options et une recommandation.
- **Cinq PR étroites valent mieux qu'une grosse.** On empile une PR seulement sur une PR dont elle dépend ; sinon, en parallèle depuis trunk.
- **Une unité de bout en bout avant d'éventer** : un défaut dans le brief coûte alors un agent au lieu de cinquante.

## 7. Idée 4 — Le kit de confiance : des skills qui écrivent l'environnement

C'est la famille qui distingue un framework d'un recueil de procédures. Son produit n'est pas du texte, c'est du code dans le repo cible.

| Skill (nom provisoire) | Ce qu'il produit dans le repo |
|---|---|
| `trust-audit` | un rapport : le niveau atteint par classe de risque, et ce qui manque |
| `trust-setup` | template de PR, check `evidence`, action `risk-label`, statut de verdict, réglages de protection de branche recommandés |
| `create-verify-app` | un skill de vérification du projet (lancer, diagnostiquer, piloter, capturer, nettoyer), une feature map et une CLI de pilotage |
| `maintain-verify-app` | les corrections de dérive de la feature map, en tâche planifiée |
| `correct` | un lint, un type, un test ou un changement d'architecture, prouvé sur une erreur passée |
| `ratchet` | une PR par jour qui retire un fichier de la liste d'exceptions d'un check plus strict |

Ordre de préférence, repris de `correct` et de Lauren Tan : architecture, puis types, puis un lint dont le message nomme le fix, puis un test, et la doc en dernier.

## 8. Idée 5 — Deux graphes, pas un

On parle de « graphe de skills », mais il y en a deux. Les confondre mène à la sur-ingénierie.

| | Graphe des skills | Graphe du travail |
|---|---|---|
| Nœuds | les skills | les unités de travail (PR, tickets) |
| Arêtes | appelle, produit pour, vérifie, répare | dépend de, bloque |
| Où il vit | le frontmatter, généré et linté par script | GitHub (PR, labels, statuts) et un fichier de suivi |
| Rythme | change rarement, par PR et eval | change à chaque tâche |
| Forme | presque une ligne (la colonne), avec des branches par playbook | un DAG ; la frontière des unités prêtes donne le parallélisme |

Le parallélisme vit dans le graphe du travail. La topologie (agent unique, DAG, fan-out, swarm de vérification) se choisit selon le couplage des unités (Ray Amjad), pas selon le nombre de skills.

Le graphe des skills ne se dessine pas à la main. Il est **généré** depuis le frontmatter (`build_skill_catalog.py` en est l'embryon) et **linté** : pas d'orphelin, pas de cycle sans budget, une condition sur chaque arête.

## 9. Idée 6 — Pas de runtime maison au départ

Le blueprint `04` prévoyait un runtime (inbox, timers, mémoire, outbox). Je recommande de ne pas le construire au départ, car nos outils fournissent déjà ces primitives :

| Primitive (Anthropic) | Ce qu'on utilise |
|---|---|
| Inbox | les événements GitHub (PR, CI, reviews), les issues, le watcher de PR du harnais |
| Timers | les tâches planifiées du harnais, le cron de la CI |
| Mémoire | le repo (journal de décisions, fichier de suivi) et la mémoire du harnais |
| Permissions | le grant explicite, la protection de branche, les checks requis |
| Outbox | la description et les commentaires de PR, le rapport de rattrapage |

Matt Pocock le résume ainsi : « Buy the services and build the tasks. » Et : « A run never waits for a human: it ends, and the human's later change […] triggers a new run. »

On construira un runtime le jour où un besoin mesuré l'exige, par exemple router des événements entre plusieurs repos.

## 10. Idée 7 — Le framework s'applique sa propre pyramide

Notre repo de skills est un produit. Il suit les mêmes règles que les repos qu'il outille :

- **Un lint des skills** : frontmatter valide, sections obligatoires (*Objectif*, *Fini quand*, *Preuve*, *Escalade*), budget de mots, liens valides, graphe cohérent.
- **Des scripts plutôt que de la prose** : toute étape mécanique devient un script testé. pstack livre `watch-pr` et `check-plan.mjs` avec leurs tests ; tstack livre `pr-wait`.
- **Un eval avant promotion** : un changement de comportement passe un test aveugle A/B (playbook `eval` de pstack).
- **Une hypothèse déclarée** : chaque skill dit quelle limite du modèle il compense. À chaque nouveau modèle, on essaie de le supprimer.
- **Un skill cassé se répare dans sa propre PR**, jamais au milieu d'une tâche.
- **Les changements du framework passent toujours par une revue humaine**, même en N5. Matt Pocock applique la même règle à sa factory : ses fixes ne s'enchaînent jamais.

## 11. Le tableau de bord de sérénité

À mesurer dès la première PR. Sinon, on ne saura pas si on monte l'échelle.

| Métrique | Pourquoi | Tendance visée |
|---|---|---|
| Attention humaine par PR (minutes ou interventions) | la north star | ↓ |
| Taux de revert | le garde-fou du débit | < 1 % |
| PR mergées par semaine | le débit | ↑ |
| Part des PR avec preuve complète | le respect du contrat | 100 %, imposé par la CI |
| Taux de FAIL du vérificateur | l'utilité du vérificateur | proche de 0 longtemps sur une classe : alléger ; élevé : améliorer la boucle interne |
| Bugs échappés (trouvés après merge) | la vraie qualité | ↓ |
| Corrections converties en structure | la santé de la méta-boucle | ↑ |
| Coût en tokens par PR mergée | la soutenabilité | ↓ à qualité égale |

## 12. Ordre de construction proposé

Chaque étape se termine sur une preuve, pas sur une date.

1. **Choisir un repo cobaye réel** et faire un premier `trust-audit` à la main. Sans vrai repo, les skills restent abstraits (risque relevé dans le blueprint).
2. **Colonne en N1, humain présent** : `ship` (reformuler, construire, prouver, PR, babysit, arrêt à merge-ready). Dix vraies PR. Chaque intervention humaine est notée dans un registre.
3. **Passage en N2** : `create-verify-app` sur le cobaye, vérificateur indépendant, statut de verdict. Vingt PR.
4. **Méta** : `correct` sur le registre d'interventions, lint de nos skills, premier eval.
5. **Passage en N3** : autopilot-stack, journal de décisions, rapport de rattrapage. Premières nuits.
6. **Passage en N4** : `risk-label` et auto-merge de la classe à faible risque.
7. **Passage en N5** : boucle externe (ratchet quotidien, fuzz à chaque release, retro sur une PR mergée sur dix).

Le façonnage amont (grill, prototype, architect, découpage en unités) arrive quand le cobaye en a besoin, pas avant.

**Règle de croissance** (pstack, guide 09) : on ajoute un skill ou un check quand le même échec apparaît deux fois.

**MVP probable** : six skills (`ship`, `prove`, `verify`, `babysit`, `trust-setup`, `correct`) et le lint de nos skills. Le reste se mérite.

## 13. Ce qu'on emprunte, et à qui

| Source | On reprend | Pour quelle famille |
|---|---|---|
| tstack | le grant `full send` / `full stop`, le standard de preuve, la merge gate, la portabilité Claude Code / Codex / T3 Code | colonne |
| pstack | le verdict sur la SHA, `patch-id`, auteur ≠ juge, le run contigu, la feature map, `correct`, `eval`, le journal de décisions, `ketchup` | colonne, kit, méta |
| Matt Pocock | le vocabulaire `software-factory` (task, trigger, run, runner), les freins et le throttle, la tâche `ratchet`, la retro sur une PR sur dix, `to-tickets` pour le graphe du travail, `writing-for-agents` | kit, façonnage, méta |
| Lauren Tan | la pyramide comme critère de qualité, bannir ce qui demande de la nuance, remplacer les commentaires par des lints, la preuve par artefacts | kit |
| Ray Amjad | la topologie selon le couplage, la vérification à la frontière de capacité, pas de personas | colonne, graphe du travail |
| Anthropic | run, session et mémoire ; la gate humaine comme événement ; commencer silencieux | colonne, rattrapage |

pstack est très lié à Cursor (agents cloud, Origin, `cursor-team-kit`, slugs de modèles). tstack est portable, mais ne couvre que la PR. D'où la proposition : écrire notre propre colonne en reprenant les meilleurs passages, sous licence MIT et avec attribution.

## 14. Ce que je révise dans le blueprint `04`

- **Je garde** les dix invariants, la politique d'autonomie 0–3, la politique de modèles par rôle et le principe d'hypothèse supprimable.
- **Je remplace** l'ordre de construction en sept phases par l'échelle de confiance : on construit dans l'ordre où un repo gagne la confiance.
- **Je diffère** le runtime maison et le contrat YAML complet. Au début, un frontmatter léger suffit : `id`, `kind`, `grant` maximal, entrées et sorties, `proof`, `enforced_by`, `hypothesis`. Le lint le vérifie.
- **Je réduis** les sept couches à quatre familles (colonne, kit, façonnage, méta) et quelques points d'entrée (`ship`, `autopilot`, `orchestrate`, rattrapage).

Mon blueprint risquait de construire la plateforme au lieu de livrer des PR.

## 15. Tensions que nos données trancheront

| Tension | Position A | Position B | Proposition |
|---|---|---|---|
| Qui corrige après une review ? | le même agent, qui garde le contexte (Ray Amjad : 38 % moins cher sur 10 PR) | un agent frais à chaque round, avec un périmètre consolidé (pstack) | eval A/B sur le cobaye |
| Un mode ou des entrées ? | un mode épinglé de ~3 500 mots (`poteto-mode`) | des entrées courtes nommées par grant (tstack) | entrées courtes, principes chargés à la demande |
| Vérifier tout, ou à la frontière ? | vérificateur systématique | vérificateur seulement là où le modèle échoue | systématique en N2, puis allégé par classe quand le taux de FAIL reste nul |

## 16. Pièges à éviter

- Automatiser avant que la boucle interne soit fiable.
- Mesurer le débit sans le taux de revert.
- Des personas (testeur, designer, PM) : la bureaucratie est garantie (Ray Amjad).
- Découper par défaut un spec couplé en tickets parallèles.
- Une boucle sans prédicat de fin (« travaille 4 h dessus »).
- Plusieurs agents dans le même worktree.
- Une règle dans `AGENTS.md` là où un check est possible.
- Éditer un skill au milieu d'une tâche.
- Construire la plateforme au lieu de livrer des PR.

## 17. Questions ouvertes

1. **Le repo cobaye** : sur quel projet réel construit-on et mesure-t-on, et avec quelle stack ? Ce repo-ci peut servir pour la méta (lint et eval des skills), mais la colonne a besoin d'une vraie application pour que la preuve runtime ait un sens.
2. **Les modèles** : a-t-on accès à une autre famille que Claude (GPT via Codex, Gemini) ? Le vérificateur doit venir d'une autre famille que l'auteur.
3. **L'ambition à trois mois** : N3 (tu merges chaque matin) ou N4 (auto-merge du faible risque) ?
4. **Le harnais** : Claude Code seul, ou aussi Codex et Cursor ? Cela fixe le niveau de portabilité à viser.
5. **La forge** : GitHub, repo public ou privé, quel plan ? Sur un repo privé, la protection de branche demande en principe un plan payant (GitHub Pro ou Team), et toute l'idée 2 en dépend.
