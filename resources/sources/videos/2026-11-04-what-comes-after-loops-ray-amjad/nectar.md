# Nectar — What Comes After Loops

> **Thèse en une phrase** : après la boucle d'un agent unique, le problème est la coordination ; il n'existe pas une bonne topologie multi-agents, seulement une topologie adaptée au **couplage réel** du travail.

**Source** : Ray Amjad, 2026-11-04 · [vidéo](https://www.youtube.com/watch?v=yrRpnx_iugY) · [transcript](transcript.md)

---

## 1. Le déplacement du problème

Résumé du talk OpenAI (00:28) :

- les anciens modèles ne savaient pas s'arrêter ; on les poussait avec `/goal` ou une boucle « Ralph » ;
- ce comportement a été **entraîné dans les modèles** ;
- avec un objectif clair et les bons outils, un agent continue jusqu'à l'atteinte du but ;
- le problème suivant n'est donc plus « faire continuer un agent », mais « **répartir le travail entre plusieurs agents et les garder alignés** ».

C'est le cadre de toute la vidéo : la boucle est le barreau zéro. La valeur se déplace vers l'**orchestration**.

---

## 2. L'échelle à sept barreaux

```text
7. Agent swarms          ← des centaines/milliers, objectif commun
6. Long-lived leads      ← des leads par métier, des semaines/mois, des workers
5. Manager thread        ← un coordinateur qui parle aux autres threads
4. Pairs                 ← builder / reviewer / verifier, boucles bornées
3. Effort scaling        ← modèle fort pour le dur, modèle cheap pour le facile
2. Fan out               ← sous-agents sur du travail réellement indépendant
1. One agent             ← objectif clair + outils + self-check
```

Chaque barreau ajoute de la coordination. Les barreaux bas sont progressivement **absorbés par les modèles** ; les barreaux hauts ne sont pas encore fiables pour tout type de travail.

---

## 3. Barreau 1 — Un agent, un objectif, des outils

Le point le plus important, et le plus souvent raté (01:58) :

- ne pas donner une **liste d'étapes** (« fais X, puis Y, puis Z ») ;
- donner l'**objectif** et laisser l'agent découvrir les étapes ;
- donner accès à **tous les outils** nécessaires ;
- donner un moyen de **vérifier son propre travail**.

Exemple : au lieu de « ajoute un cache à cette requête », dire « amène le P95 de cette page sous 200 ms ». L'agent trouvera peut-être une meilleure solution que le cache.

> « by giving a set of steps that you came up with, you're kind of capping the agent at your own solution » — 01:58

**Pour notre framework** : un skill ne doit pas être un script rigide d'étapes si l'objectif suffit. Les étapes sont utiles quand elles encodent une **méthode** (debug, review, vérification), pas quand elles remplacent le jugement.

---

## 4. Barreau 2 — Fan out, mais seulement sur de l'indépendant

Le fan-out consiste à découper un travail en sous-tâches confiées à des sous-agents (02:51). Le mot clé est **truly independent** :

- comparer 5 bibliothèques d'authentification : chaque agent peut travailler sans connaître les autres ;
- chasser des bugs dans différentes parties du codebase : chaque agent part d'un point différent.

Mais l'usage excessif des sous-agents est courant. Le cas le plus problématique (03:52) : découper un spec en tickets puis lancer des subagents pour implémenter chaque ticket en parallèle. Même quand le travail **semble** indépendant, il peut être **enchevêtré** de façon imprévue.

Anthropic aurait retiré la construction « sprint » : ce qui aidait Opus 4.5 ne serait plus nécessaire avec les modèles suivants. L'argument du « dumb zone » à 150k tokens serait obsolète : avec la compaction, un agent peut monter à 400k, compacter et continuer.

**Pour notre framework** : la décomposition en tickets n'est pas une mauvaise idée en soi ; c'est une mauvaise idée **par défaut**. Elle doit être réservée aux travaux dont les frontières sont prouvées indépendantes. Le graphe doit pouvoir représenter le couplage, pas seulement la séquence.

---

## 5. Barreau 3 — Effort scaling

Tous les travail ne mérite pas le même modèle (05:27). Deux directions :

- **vers le haut** : un exécuteur pas cher qui appelle un advisor plus fort quand il est bloqué ;
- **vers le bas** : un agent fort qui délègue les tâches self-contained à un modèle moins cher (traductions, docs, vérification navigateur).

Exemples cités : Sonnet + Fable en advisor ; Sol Medium + Astra pour une race condition ; Luna High pour les tâches faciles.

**Pour notre framework** : le routage par rôle et par difficulté doit être une **politique configurable**, pas une constante codée dans chaque skill. C'est exactement ce que fait `setup-pstack`.

---

## 6. Barreau 4 — Les paires, et la boucle bornée

Le pattern le plus mature (06:31) : deux agents qui échangent, inspiré des GAN — un générateur et un juge.

Le setup concret de Ray Amjad (07:34) :

```text
spec (avec acceptance criteria)
  → builder
  → reviewer (jusqu'à 3 rounds)
  → verifier (jusqu'à 2 rounds)
  → merge
```

- Le **builder** construit et compacte si nécessaire.
- Le **reviewer** (souvent un autre modèle, ici Codex) renvoie ses findings au builder.
- Le **verifier** utilise Playwright et peut fan-out par flux utilisateur indépendant.
- Les flux qui échouent reviennent au builder.

### Même builder ou nouveau builder ?

Question fréquente en consulting (09:07). L'intuition dit : renvoyer les findings au même builder, qui a déjà le contexte, produit un fix plus rapide et plus architectural. Un test aveugle sur 10 PR rejouées confirme : **même builder, 38 % moins cher**, et de meilleurs résultats. Mais c'est un résultat local à sa factory ; à re-tester dans la nôtre.

**Pour notre framework** : les boucles de correction doivent avoir un **budget de rounds** et un **propriétaire de contexte**. Le builder garde le contexte jusqu'à la fin du cycle, puis on repart frais pour la suite.

---

## 7. Vérifier à la frontière de capacité

Le passage clé (10:14) :

> « the biggest gains in having an evaluator or a verifier agent evaluating at the edges of what the current models are capable of »

Autrement dit :

- vérifier un formulaire de contact que le modèle réussit toujours : gain quasi nul ;
- vérifier une synchronisation offline/online avec fusion de changements : gain réel, car c'est à la frontière.

La citation Anthropic :

> « every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be inaccurate, and both because they can quickly go stale as models improve. » — 11:51

**Conséquence** : un harnais doit être **conçu pour rétrécir**. Quand un nouveau modèle sort, la question n'est pas « comment ajouter un agent ? » mais « quelle étape puis-je supprimer ? ».

**Pour notre framework** : chaque skill doit déclarer l'**hypothèse de capacité** qu'il encode. Un skill de vérification qui existe parce que le modèle ne sait pas faire X doit être réévalué quand X devient fiable. Sans cette discipline, le graphe grossit et se fossilise.

---

## 8. Barreau 5 — Le manager thread

Pattern déjà disponible (13:19) :

- un thread « chief of staff » qui reçoit toutes les instructions et délègue aux autres threads ;
- Codex, Claude Code desktop et Cursor proposent des variantes ;
- Ray utilise une session Claude Code locale connectée à Slack via MCP, qui parle à des sessions distantes sandboxées.

Le coordinateur est le point d'entrée unique ; les workers sont des sessions isolées. L'humain ne change plus de thread, il parle au coordinateur.

**Pour notre framework** : c'est le modèle le plus réaliste pour un **orchestrateur de skills** aujourd'hui. Un routeur central, des workers spécialisés, un état partagé explicite. Pas besoin d'attendre les « long-lived leads ».

---

## 9. Barreaux 6 et 7 — Leads et swarms : prometteurs, pas prêts

### Long-lived leads

L'idée (16:35) : des leads par métier (programming, design, QA) qui vivent des semaines ou des mois, avec des workers, et qui se parlent **comme des pairs**, pas comme des appels d'outils. Ils partagent un **work log** : objectif global, travail en cours, qui fait quoi.

Problème : avec les modèles actuels, ça ne tient pas. Les rôles et personas (tester, builder, verifier, designer, 15–20 rôles) produisent de la **bureaucratie** : les agents passent plus de temps à discuter des règles qu'à travailler. Ça marche quelques heures ou quelques jours, puis ça s'effondre.

### Swarms

L'idée (18:10) : des centaines ou milliers d'agents vers un objectif commun. OpenAI l'a fait pour des preuves mathématiques : plusieurs équipes, chacune avec une approche différente, les leads partagent les découvertes pour éviter la duplication. C'est un trade-off **explore / exploit** : d'abord explorer large, puis converger quand une piste prometteuse apparaît.

Mais le contre-exemple est parlant (19:11) : 50 agents GPT-6.1 dans Minecraft, objectif « bâtir une civilisation prospère ». Résultat : bureaucratie élaborée (permis, registres, rôles), mais les agents n'ont pas su se nourrir ; 22 sont morts la première nuit, puis ils sont restés terrés.

### Ce qui marche : la chasse aux vulnérabilités

(21:19) En fan-out parallèle simple : 21 vulnérabilités pour 6,5 M tokens. En swarm coordonné : 266 vulnérabilités pour 27 M tokens. Soit **4× plus de tokens pour 12× plus de findings**.

Pourquoi ? Parce que la chasse aux vulnérabilités est **indépendante** ; construire une application ou une civilisation est **enchevêtré**.

**Pour notre framework** : ne pas vendre du swarm comme un default. Le graphe doit avoir des **modes de topologie** :

- pipeline séquentiel pour le travail couplé ;
- DAG/frontière pour les tickets indépendants ;
- fan-out pour la couverture ;
- swarm pour la recherche exhaustive ou la chasse de bugs ;
- pairs pour la construction vérifiée.

Le choix de topologie est une **décision de premier ordre**, pas un détail d'implémentation.

---

## 10. Ce que les modèles absorbent

(12:51) Les barreaux bas disparaissent progressivement :

- `/goal` et les boucles Ralph : plus nécessaires ;
- décomposition en sprints/tickets : moins nécessaire ;
- reviewer séparé : peut-être absorbé par une bonne review dans le même contexte ;
- verifier séparé : peut-être absorbé quand le modèle sait vérifier son propre travail.

**Pour notre framework** : construire des skills **supprimables**. Chaque skill doit pouvoir disparaître quand le modèle acquiert la capacité. Un skill qui survit doit apporter soit une **méthode** que le modèle n'a pas, soit une **connexion à un système externe**, soit une **garantie de vérification**.

---

## 11. Implications pour notre framework de skills

### À reprendre

- **La topologie dépend du couplage.** Un graphe unique ne suffit pas ; il faut des modes (pipeline, DAG, fan-out, swarm, pairs).
- **Le builder/reviewer/verifier avec rounds bornés.** C'est le socle fiable aujourd'hui.
- **Le même builder pour corriger.** Préserver le contexte jusqu'à la fin du cycle, puis repartir frais.
- **Le manager thread comme coordinateur.** Un point d'entrée, des workers, un état partagé.
- **La vérification à la frontière de capacité.** Ne pas vérifier ce que le modèle réussit toujours ; vérifier ce qui est risqué.
- **Les hypothèses de harnais comme objets de première classe.** Chaque skill doit pouvoir être remis en cause et supprimé.

### À adapter

- **Les chiffres (38 %, 21 vs 266)** sont des rapports locaux. Les reproduire dans notre contexte avant de les ériger en règles.
- **Le manager thread** est lié à un harnais (Codex, Claude Code, Slack MCP). Notre graphe doit rester agnostique.
- **Le fan-out de vérification par flux utilisateur** est excellent pour l'UI ; moins pertinent pour les invariants globaux.

### À rejeter (pour l'instant)

- **Les rôles et personas en graphe.** La bureaucratie émerge et bloque le travail. Préférer des skills fonctionnels à des personnages.
- **Les swarms pour construire.** Réservés à la recherche, la couverture et la chasse de bugs.
- **Les long-lived leads comme baseline.** À revisiter quand les modèles seront meilleurs en coordination pair-à-pair.

### Question ouverte pour la suite

Comment représenter le **couplage** dans notre graphe de skills ? Un nœud doit pouvoir déclarer : « je peux tourner en parallèle avec X », « je dois voir l'état de Y », « je dois attendre Z ». Sans cette information, l'orchestrateur ne peut pas choisir la bonne topologie.

---

## 12. Citations à garder

> « loops solve the problem of keeping one agent going until your goal is done. But now there's only so much that a single agent can do. So the next problem becomes, how do you split work across many agents and keep them aligned? » — 01:01

> « the key word here is truly independent » — 02:51

> « every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing, both because they may be inaccurate, and both because they can quickly go stale as models improve. » — 11:51

> « the biggest gains in having an evaluator or a verifier agent evaluating at the edges of what the current models are capable of » — 10:51

> « it may be the case that with Opus 6 or Opus 7, it could do a really good code review in the same context window. » — 12:51
