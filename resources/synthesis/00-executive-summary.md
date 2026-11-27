# Synthèse exécutive — ce que le corpus nous apprend

**Date** : 2026-11-16  
**Corpus** : 3 dépôts de skills (109 skills), 2 conférences vidéo, 1 article d'ingénierie.  
**But** : extraire les invariants de conception avant de construire notre propre graphe de skills.

---

## 1. Ce que nous avons collecté

| Source | Nature | Volume | Apport principal |
|---|---|---|---|
| `mattpocock/skills` | 39 skills | 20 engineering, 7 productivity, 4 misc, 8 in-progress | Théorie de l'écriture pour agents, routeur humain, graphe de tickets |
| `cursor/plugins/pstack` | 61 skills | 34 skills cœur, 24 principes, 23 playbooks | Orchestrateur abouti, playbooks, principes, méta-amélioration |
| `t3dotgg/tstack` | 9 skills | Cycle de vie PR | Contrat d'autonomie, preuve, merge gate, council multi-modèles |
| Lauren Tan — *All Code Is Slop* | Conférence 17:31 | Transcript + nectar | Pyramide code → checks → vérification → prose ; confiance |
| Ray Amjad — *What Comes After Loops* | Vidéo 23:11 | Transcript + nectar | Échelle de coordination multi-agents ; topologie selon couplage |
| Anthropic — *Building always-on agents* | Article 14 min | Contenu + 7 diagrammes + nectar | Durabilité : inbox, timers, mémoire, permissions, outbox |

Détail : [`SOURCES.md`](../SOURCES.md) · Catalogue : [`SKILL-CATALOG.md`](../SKILL-CATALOG.md) · Données : [`skill-catalog.json`](../skill-catalog.json)

---

## 2. Les dix idées qui structurent la suite

### 2.1 La confiance est le produit, pas la vitesse

La question n'est pas « combien de PR l'agent peut-il produire ? » mais « puis-je lui confier une PR sans la relire ? ». Lauren Tan construit six mois d'environnement pour obtenir cette confiance. Le volume (11 000 PR/mois, 0,5 % de revert) est une **conséquence**, pas un objectif.

**Conséquence** : notre framework doit être jugé sur sa capacité à produire des changements **dignes de confiance**, pas sur le nombre de skills.

### 2.2 Le déterministe bat la prose

La pyramide inversée est le modèle le plus actionnable du corpus :

```text
code & architecture  >  types / lint / checks  >  vérification  >  prose
```

Chaque correction répétée doit devenir un check, un type, un test ou un changement d'architecture — pas une ligne de plus dans un `AGENTS.md`.

**Conséquence** : un skill qui ne fait qu'ajouter des instructions est faible. Un skill qui déclenche un lint, un test, une preuve runtime ou une modification structurelle est fort.

### 2.3 Un skill est un pointeur, des étapes, un critère de fin

Les meilleurs skills du corpus partagent une anatomie :

- une **description** qui encode les branches de déclenchement ;
- un **corps court** avec des étapes ;
- des **critères de complétion** vérifiables ;
- des **références divulguées** progressivement (`references/`, `playbooks/`, `scripts/`) ;
- une **source de vérité unique** pour chaque règle.

Les skills de 100 à 900 mots dominent. Les seuls fichiers très longs sont des routeurs (`ask-matt` ~1 900 mots, `poteto-mode` ~3 500 mots), et ils sont **user-invoked** pour ne pas coûter du contexte en permanence.

**Conséquence** : notre unité de base doit rester petite. La complexité doit vivre dans les **arêtes** et les **playbooks**, pas dans des monolithes.

### 2.4 L'invocation est une décision de budget

Deux modes, deux coûts :

| Mode | Coût | Quand l'utiliser |
|---|---|---|
| **Model-invoked** | Description chargée à chaque tour | Le skill doit se déclencher seul, ou être appelé par un autre skill |
| **User-invoked** | Zéro contexte, charge cognitive humaine | Le skill est un mode, un routeur, une procédure rare |

Les trois corpus illustrent les trois stratégies :

- **Matt** : 15 model-invoked / 24 user-invoked, avec un routeur humain `ask-matt` ;
- **pstack** : 1 model-invoked (`setup-pstack`) / 60 user-invoked, avec un mode `poteto-mode` comme porte d'entrée ;
- **tstack** : 9 model-invoked / 0, avec des triggers en langage naturel.

**Conséquence** : il n'y a pas de bonne réponse universelle, mais une règle : **payer le contexte seulement quand le déclenchement autonome vaut son prix**.

### 2.5 La topologie doit épouser le couplage

C'est l'apport central de Ray Amjad :

- travail **indépendant** → fan-out, swarm, parallélisme ;
- travail **enchevêtré** → agent unique, paires, pipeline séquentiel ;
- travail **exploratoire** → arena, swarm de recherche ;
- travail **répétitif et vérifiable** → DAG de tickets avec frontière.

Les échecs viennent presque toujours d'une **topologie inadaptée** : découper un spec couplé en tickets parallèles, ou lancer des personas qui passent leur temps à négocier des règles.

**Conséquence** : notre graphe doit supporter **plusieurs modes de topologie** et choisir en fonction d'une propriété déclarée par le travail, pas d'une mode du moment.

### 2.6 Le graphe de tâches avec frontière est la primitive la plus solide

`to-tickets` + `implement-spec` de Matt Pocock donnent un modèle complet :

- chaque ticket est une **tranche verticale** demoable ;
- chaque ticket déclare ses **blocking edges** ;
- l'ensemble forme un **DAG** ;
- l'exécution suit la **frontière** des tickets prêts ;
- chaque implémenteur travaille dans son **worktree** ;
- un merger subagent intègre ;
- une **code review unique** passe sur la branche d'intégration.

C'est plus robuste qu'une liste d'étapes ou qu'un swarm non structuré. C'est aussi compatible avec la compaction et les modèles actuels.

### 2.7 Le trio builder / reviewer / verifier est le socle fiable

Le pattern le plus mature aujourd'hui :

```text
spec → builder → reviewer (≤3 rounds) → verifier (≤2 rounds) → merge
```

Deux nuances importantes :

1. **Le même builder corrige.** Un test aveugle sur 10 PR montre 38 % de coût en moins et de meilleurs résultats, parce que le builder conserve le contexte architectural.
2. **Le verifier intervient à la frontière de capacité du modèle.** Vérifier ce que le modèle réussit toujours est du gaspillage ; vérifier ce qui est risqué est rentable.

**Conséquence** : notre graphe de base doit avoir des **cycles bornés** avec un propriétaire de contexte, et des **gates de vérification** placées là où le risque est réel.

### 2.8 Les hypothèses du harnais expirent

Citation clé d'Anthropic :

> « every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be inaccurate, and both because they can quickly go stale as models improve. »

Chaque skill de vérification, chaque reviewer, chaque étape de décomposition encode une hypothèse sur les limites du modèle. Quand le modèle progresse, l'étape devient un coût inutile.

**Conséquence** : notre framework doit être **conçu pour rétrécir**. Chaque skill doit déclarer son hypothèse et pouvoir être supprimé. Un graphe qui ne fait que grossir est un graphe qui se fossilise.

### 2.9 Un skill n'est pas un runtime

L'article always-on sépare clairement :

- le **runtime** : inbox, timers, mémoire, permissions, outbox ;
- le **skill** : la procédure de jugement exécutée dans un run.

Si on met la durabilité dans les skills, chaque skill réinvente une mauvaise state machine. Le graphe a besoin d'un **état externe** : événements, échéances, progression, approbations, messages.

**Conséquence** : avant d'écrire des skills, il faut définir le **contrat d'état** et le **contrat d'événement**. C'est la décision la plus structurante de la phase suivante.

### 2.10 La méta-amélioration est ce qui empêche la dérive

pstack est le seul corpus qui ferme la boucle :

- `reflect` capture la recette d'une tâche longue ;
- `correct` encode les corrections répétées dans la structure ;
- `eval` compare des variantes avec un protocole aveugle ;
- `retro` (Matt) transforme les erreurs en checks.

Sans ces skills, un graphe accumule des règles, des exceptions et des couches mortes. Avec eux, il peut **se simplifier** à mesure que les modèles progressent.

**Conséquence** : la méta-amélioration n'est pas un nice-to-have. C'est un **organe vital** du framework.

---

## 3. Les trois tensions à résoudre

### 3.1 Planifier ou ne pas planifier ?

| Source | Position |
|---|---|
| Matt Pocock | Spec + tickets + graphe de dépendances pour le multi-session |
| pstack | « I don't believe in planning. The best spec is code. » |
| Ray Amjad | Ne pas décomposer un spec en tickets par défaut ; les modèles récents gèrent la compaction |
| Anthropic | La mémoire de progression est indispensable ; le plan peut vivre dans l'état |

**Synthèse proposée** : distinguer **planification de découverte** et **planification d'exécution**.

- Pour un travail flou, une phase de découverte (grill, research, prototype) est rentable.
- Pour un travail clair et couplé, un agent unique avec compaction est souvent meilleur qu'un découpage.
- Pour un travail large et **prouvé indépendant**, le graphe de tickets est rentable.
- Dans tous les cas, l'**état de progression** doit être persisté, même sans plan formel.

### 3.2 Décomposer ou garder le contexte ?

La décomposition aide la parallélisation mais casse le contexte. La compaction préserve le contexte mais perd du détail.

**Synthèse proposée** : décomposer seulement quand les frontières sont **vérifiables** (interfaces, contrats, tests). Sinon, garder un agent unique et persister les décisions dans la mémoire. La question n'est pas « combien d'agents ? » mais « quelles frontières puis-je prouver ? ».

### 3.3 Autonomie ou gates ?

| Source | Position |
|---|---|
| pstack | Réversible → agir ; irréversible → pause |
| tstack | Grant explicite (`full send`), merge gate, escalade |
| Anthropic | Auto mode + deferred tool calls + proxy de credentials |

**Synthèse proposée** : une **politique d'autonomie graduée** :

- **Niveau 0** : lecture seule.
- **Niveau 1** : écriture locale réversible (fichiers, branche).
- **Niveau 2** : actions externes réversibles (PR, commentaire, ticket).
- **Niveau 3** : merge, deploy, suppression, message à un client — gate humaine ou merge gate explicite.

Chaque skill déclare le niveau maximal qu'il peut atteindre et les gates associées.

---

## 4. Ce que nous ne faisons pas encore

Conformément à la demande : **on ne construit pas les skills maintenant**. Cette base de connaissance sert à :

1. choisir les invariants du framework ;
2. définir le contrat d'un nœud et d'une arête ;
3. décider du runtime et du schéma d'état ;
4. sélectionner les patterns à implémenter en premier ;
5. seulement ensuite, écrire les skills.

Le document [`04-framework-blueprint.md`](04-framework-blueprint.md) propose une architecture cible et un ordre de construction. Il est explicitement une **hypothèse à valider**, pas un plan figé.

---

## 5. Prochaine étape recommandée

Une session de conception en cinq décisions :

1. **Runtime** : où vivent l'inbox, les timers, la mémoire, les permissions et l'outbox ?
2. **Contrat de nœud** : quels champs chaque skill doit-il déclarer ?
3. **Topologies** : quels modes supporte-t-on (pipeline, DAG, fan-out, swarm, pairs) ?
4. **Gates** : quelles actions sont automatiques, humaines, ou mixtes ?
5. **Preuve** : quel est le standard de preuve minimal pour qu'un run soit « done » ?

Une fois ces cinq décisions prises, le graphe peut être dessiné, puis les skills écrits et évalués.
