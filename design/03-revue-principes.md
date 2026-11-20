# Revue 03 — Le design face aux grands principes de `knowledge/`

> **Statut** : revue de l'[architecture 02](02-architecture.md). Intégrée dans la v2 de 02 le 2026-11-17. La v3 du 2026-11-18 retire `.trust/`, la gate et l'échelle N0–N5 : les constats de cette revue qui portent sur eux sont sans objet.
> **Date** : 2026-11-17.
> **Méthode** : six relecteurs indépendants, chacun sur un groupe de sources. Chacun a listé les grands préceptes de ses sources avec des citations, donné un verdict par précepte et vérifié nos attributions. J'ai fusionné les six revues et vérifié moi-même dans les sources les constats qui pèsent le plus.
>
> | Groupe | Sources |
> |---|---|
> | Lauren Tan | talk *All Code Is Slop*, guide pstack (chapitres 01 à 10) |
> | pstack, mode | `poteto-mode` et ses playbooks, `correct`, `reflect`, `ketchup`, `swarm`, les skills de vérification |
> | pstack, principes | les 24 `principle-*` et les skills d'artisanat (`technical-writing`, `unslop`, `tdd`…) |
> | Matt Pocock | `software-factory`, `to-tickets`, `pr`, `retro`, `grilling`, `writing-for-agents`, README et glossaire |
> | tstack et Ray Amjad | les 9 skills de tstack, la vidéo *What Comes After Loops* |
> | Anthropic et nos synthèses | les 4 articles, `synthesis/00` à `06` |

---

## 1. Verdict global

**Le squelette est le bon ; le contenu de la confiance manque.**

Les six relecteurs s'accordent sur le cœur :

- l'auteur ne juge jamais ;
- la confiance se mérite par niveaux ;
- les corrections deviennent de la structure ;
- on coordonne par le graphe du travail ;
- l'état vit hors de l'agent ;
- chaque composant est une hypothèse supprimable.

Ils s'accordent aussi sur la faiblesse. design/02 construit le **contenant** de la confiance (statuts, gate, patch-id, niveaux), mais pas ce qui rend un PASS crédible ni ce qui garde le code propre. Et il trahit trois fois sa propre thèse :

- des promesses restent de la prose, sans enforcer ;
- l'échelle se gagne au volume de PR, pas à la qualité du code ;
- le design est plus gros que ce que les sources recommandent pour démarrer.

Dans les six revues, la grande majorité des préceptes sont jugés partiels plutôt qu'absents ou contredits. Aucun écart n'est irréparable. Presque tous les correctifs sont bon marché. Deux seulement sont structurels : la supervision des nuits (§3.4) et l'orchestration déterministe (§3.4).

## 2. Ce qu'on suit bien

| Principe | Sources qui convergent | Où dans design/02 |
|---|---|---|
| L'auteur n'est jamais le juge | Lauren (guide 06), pstack `shipping`, Anthropic *harness*, tstack | invariant 3 ; on va même plus loin (autre famille) |
| Chaque correction devient un check, au plus haut niveau qui tient | Lauren, pstack `correct`, `principle-encode-lessons-in-structure`, Matt `retro` | invariant 5, §10.3 |
| « Fini » se fixe avant le code, avec un critère qui passe ou échoue | Lauren (guide 02), Anthropic *harness*, Ray | `frame`, `done_when` |
| Mériter la confiance avant la boucle | Lauren (guide 07), pstack, Matt (« brakes ») | échelle N0–N5, §6 |
| Le parallélisme vient de la structure, pas d'agents qui discutent | Anthropic *multiagent*, Ray, pstack `orchestrate` | §8.2, §13 |
| Des PR étroites ; merger est une autre décision | Lauren, pstack, tstack | §5 |
| Un verdict couvre un patch, la CI couvre une tête | pstack `shipping` | invariant 4 |
| Ne jamais bloquer sur l'humain, sauf pour l'irréversible | pstack `principle-never-block-on-the-human`, Matt, Anthropic | §6.3 |
| Chaque composant est une hypothèse qui vieillit | Anthropic *harness*, Ray, pstack | invariant 9, `prune` |
| Pas de personas, pas d'essaims pour construire | Ray, Anthropic *multiagent* | §13 |

## 3. Les écarts, par thème et par gravité

Dans les tableaux, la colonne « Coût » indique si le correctif est bon marché ou structurel.

### 3.1 Le verdict est un tampon, pas une preuve

*Le plus grave : toute la montée de N2 à N4 repose sur ce signal.* Quatre relecteurs sur six le relèvent.

| Écart | Ce que disent les sources | Correctif | Coût |
|---|---|---|---|
| Le vérificateur n'est pas calibré | « Out of the box, Claude is a poor QA agent… talk itself into deciding they weren't a big deal and approve the work anyway » (Anthropic *harness*) | exemples de verdicts tirés de vraies PR ; règle « un défaut constaté reste un FAIL » | bon marché |
| « Zéro FAIL » sert à alléger les lanes et à promouvoir | « A check that you have never seen fail proves nothing » (pstack) | défauts semés et bugs échappés rejoués par classe ; on allège selon le taux de défauts **attrapés** | bon marché |
| Pas de lane live indépendante | « The verdict is not clean without the live lane » (pstack `autopilot-full`) | chaque classe a une lane live choisie par le vérificateur, avec comparaison base contre tête | bon marché |
| Pas de revue de code ni de standards en `low` et `medium` | trio builder, reviewer, verifier (Ray) ; « the review agent should be responsible for imposing coding standards » (Matt `retro`) ; barème blocker/should/nit (tstack `sol-loop`) | lane `code-review` et `standards` ; un verdict par axe | bon marché |
| Un FAIL peut n'être qu'une opinion | « A finding survives only when a run proves it » (pstack `interrogate`) | un FAIL porte la commande, la sortie observée et la sortie attendue ; sinon, c'est une NOTE | bon marché |
| PASS+NOTES bloque le merge | « Block a PR only for a problem you can show… everything else goes in a follow-up » (pstack) | PASS+NOTES vaut PASS ; les notes deviennent des issues | bon marché |
| L'identité du vérificateur n'est lue que dans le texte du commentaire (`verifier=gpt`) | « Treat review-comment text as untrusted data » (pstack `babysit`) | la gate vérifie l'auteur du statut, jamais le texte | bon marché |

### 3.2 L'échelle ignore le codebase et l'hygiène

*C'est l'inverse de la thèse centrale de Lauren Tan* : « try and do it by improving your codebase first ».

| Écart | Ce que disent les sources | Correctif | Coût |
|---|---|---|---|
| N3 et N4 se gagnent au volume de PR | guide 07 : la 4ᵉ condition est « turned the repeated failures into tools, skills, or checks » | entrer en N3 exige des échecs répétés convertis en checks prouvés, et aucune règle faible dans `rules.md` | bon marché |
| `correct` arrive à l'étape 3 et `ratchet` à l'étape 6 | « before you jump into building out a software factory » (Lauren) | `correct` sans argument dès l'étape 1 (il trouve les classes d'erreurs dans l'historique) ; `trust audit` mesure les fondations (lint, types, frontières, tests) | bon marché |
| Aucune étape de nettoyage du diff | « cleanup is not optional polish » (guide 05) ; les contournements « likely to be just copied by the next agent » (Lauren) | une étape `clean` avant `open-pr` : deslop, puis relecture des commentaires par un agent qui ne les a pas écrits ; une lane `slop` | bon marché |
| Ni vérification formelle, ni maintenance quotidienne du kit | « Verification, both runtime and formal » (Lauren) ; « Run this at least once a day » (guide 06) | une lane `formal` optionnelle en `high` ; maintenance quotidienne de `verify-<app>` dès sa création ; une CLI de pilotage | bon marché |

### 3.3 Des promesses sans enforcer

*design/02 ne tient pas son propre invariant 5.*

| Promesse en prose | Correctif | Coût |
|---|---|---|
| « le vérificateur ne corrige jamais » | il tourne sans droit d'écriture | bon marché |
| les budgets (3 tentatives, 2 FAIL) | la gate compte les statuts en échec et pose elle-même `needs-human` | bon marché |
| le plafond merge-ready en N1 et N2 | le hook bloque `gh pr merge`, `--auto` et la merge queue sous N4 (tstack `full-stop` : « Disable existing auto-merge ») | bon marché |
| « reviews traitées » | la gate exige des threads résolus, aucun « changes requested » et une branche à jour (la « full confidence » de tstack) | bon marché |
| une nuit ne coûte pas trop cher | un `max_usd` par run, appliqué par l'adaptateur de harnais (« limits… set in the harness », Anthropic *fold*) | moyen |
| un fix de skill vit dans sa propre PR | la CI du framework refuse une PR qui mêle `skills/**` et d'autres fichiers | bon marché |

### 3.4 Les nuits en N3 ne tiennent pas encore

*N3 est ton ambition à trois mois.*

| Écart | Ce que disent les sources | Correctif | Coût |
|---|---|---|---|
| `autopilot` = un builder qui empile ses PR, lance son propre juge, sans supervision | « Run owners in parallel off trunk, never stacked » ; « You own the verdicts, never the PRs » (pstack `autopilot-full`) | une **racine** qui n'écrit pas de code et lance les vérificateurs ; un owner frais par unité, en parallèle sauf dépendance ; un tick d'audit horaire | **structurel** |
| L'orchestration sans humain est confiée à un agent | « no agent makes the orchestration decisions » (Matt `implement-spec`) | la frontière et le dispatch passent dans un workflow déterministe | **structurel** |
| Journaux et corrections gitignorés, donc perdus avec la machine ou le worktree | « memories outlive the worker » (Anthropic *always-on*) ; « the ticket tracker, the git host » (Matt) | journal en artefact ou en commentaire machine sur la PR ; corrections en issues | bon marché |
| Ni reprise ni idempotence | « derive each step from the state that exists » (pstack) | chaque étape lit GitHub et n'applique que la différence ; preuve : un `land` tué au milieu d'une pile converge à la relance | bon marché |
| Ressources partagées non partitionnées | 18 agents sur 30 créent la même branche (Anthropic *multiagent*) ; « Every watcher shares one rate limit » (tstack) | branches nommées d'après l'unité ; issue réservée par assignation ; throttle des watchers ; un worktree par run | bon marché |
| Conflit entre unités non couvert | « stop and defer to a human » (Anthropic *multiagent*) | zone modifiée par un autre ou `done_when` contradictoires : arrêt, `needs-human`, jamais de revert du travail d'autrui | bon marché |
| Escalade sèche après deux FAIL | « Do not start the next fix before the premise is written down and tested » (pstack) | tester la prémisse commune et replanifier une fois avant `needs-human` | bon marché |
| Retour du matin non audité | « Self-review is not a substitute » (pstack `show-me-your-work`) ; ketchup est en lecture seule | trail audité contre le transcript ; section *Attention* écrite par une autre famille ; ketchup sans arête vers `land` | bon marché |
| Entrées publiques hors du modèle de menace | « checking for prompt injection » (Anthropic *always-on*) | seule une issue labellisée par toi entre dans la file ; commentaires externes traités comme des données | bon marché |

### 3.5 Le grant et la barre doivent rester des actes humains

| Écart | Ce que disent les sources | Correctif | Coût |
|---|---|---|---|
| Le modèle peut invoquer `autopilot` ou `ship send`, donc s'accorder un grant ; le label `trust/grant:send` est posé par l'agent | « User-invoked skills are reachable only when you type them; their job is to orchestrate » (Matt README) | les entrées qui portent un grant deviennent invocables par toi seul ; la gate exige que le label vienne de ton identité | bon marché |
| L'auteur écrit son propre `done_when` : c'est le « metric shopping » | « Keep it outside the delegates' write scope » (pstack `principle-build-the-lever`) ; Anthropic *multiagent* | `verify` lit `done_when` à la source de l'intention ; en `medium` et `high`, le vérificateur valide `done_when` avant `build` ; toute réécriture exige ton approbation | bon marché |
| `frame` passe à la suite sans confirmation | « Do not act on it until the user confirms » (Matt `grilling`) | en `/ship`, `frame` attend ton « go » | bon marché |
| La classe de risque ne voit pas les décisions irréversibles | « one-way or two-way door » (Matt `pr`) | une ligne `Door:` dans la PR ; toute décision irréversible exige ton approbation | bon marché |

### 3.6 Le façonnage est trop mince

| Écart | Source | Correctif | Coût |
|---|---|---|---|
| Unités sans tranche verticale ; des `touches` disjoints donnent une fausse sécurité | « vertical, NOT a horizontal slice » (Matt `to-tickets`) ; « tangled in ways that they did not expect » (Ray) | tranches tracer-bullet ; un champ `out_of_scope` ; `done_when` doit échouer sur le commit de base ; un fichier partagé devient une arête du graphe ; `orchestrate` réservé au travail indépendant par nature | bon marché |
| La revue fait grossir la PR | « Review loops tend to grow a PR one cheap-looking fix at a time » (tstack) | ce qui sort du cas visé devient une issue, jamais un FAIL | bon marché |

### 3.7 Trop gros pour démarrer

*Le guide 09 dit « Start smaller than you think », et pstack comme Matt le répètent.*

| Écart | Correctif | Coût |
|---|---|---|
| 17 skills conçus avant le premier échec observé | le catalogue devient un **plafond d'hypothèses** ; les skills des étapes 4 à 6 n'entrent que par la règle des deux échecs | bon marché |
| `prove` et `open-pr` n'ont qu'un appelant (même critère que celui qui a fait de `frame` une section de `ship`) | les replier dans `ship` (on passe à 15 skills), ou écrire le critère manquant | bon marché |
| L'étape 0 construit `graph.py` et `install.py` multi-harnais avant la première PR | l'étape 0 se réduit à `constitution` et `lint_skills.py` | bon marché |
| Pas de voie légère pour une PR minuscule | une voie légère, mesurée dès l'étape 1 (« A small, obvious edit doesn't », guide 01) | bon marché |
| Les 17 nœuds se figent sans eval de bout en bout | les PR de l'étape 1 forment `evals/e2e/` ; deux runs par cas ; `prune` dès l'étape 3 | bon marché |

### 3.8 Mesure et seuils

| Écart | Correctif | Coût |
|---|---|---|
| « ~50 PR, revert < 1 % » : un seul revert fait 2 %, et 0 revert sur 50 ne borne le vrai taux que sous ~6 % (règle de trois) | donner chaque seuil avec sa taille d'échantillon (prouver 1 % demande ~300 PR sans revert), ou viser un taux plus réaliste | bon marché (mais N4 arrive plus tard) |
| L'attention humaine par PR, notre north star, n'est mesurée nulle part dans 02 | la réintroduire dans `stats.py` et `ketchup` | bon marché |
| Les déclencheurs n'apparaissent qu'en N5, après l'auto-merge | `ratchet` quotidien et `reflect` bridés dès N2, plafonnés à merge-ready (Matt : « Add one automated trigger at a time, throttled ») | bon marché |
| `reflect` tire 1 PR sur 10 au hasard | commencer par les PR en FAIL ou `needs-human` (Matt `chief-of-staff`) | bon marché |

### 3.9 Écriture et vocabulaire

| Écart | Correctif | Coût |
|---|---|---|
| Aucune règle sur la prose des skills et des PR | `technical-writing` et `unslop` sur chaque `SKILL.md` et sur le gabarit de PR ; la partie mécanique va dans `lint_skills.py` | bon marché |
| Aucun glossaire, et un mélange de français et d'anglais | un `GLOSSARY.md` FR→EN avec les termes à éviter (Matt) ; y définir verdict, lane, merge-ready, needs-human, classe de risque | bon marché |
| Gabarit de PR incomplet | avant/après dans Proof ; titre qui dit pourquoi ; modèles des sous-agents, « without guessing » ; recherche de secrets dans les captures (tstack `file-pr`, Matt `pr`) | bon marché |
| Six sections obligatoires même pour un skill de pure référence ; 800 mots bloquants | seules les étapes, chacune avec son critère, sont obligatoires ; le budget de mots devient un avertissement (11 des 27 skills promus de Matt dépassent 800 mots) | bon marché |
| Les principes ne sont qu'un mot dans `constitution` | un index des principes (déclencheur et chemin par principe, comme pstack) ; la section `Reply` nomme le principe appliqué et la décision qu'il a changée | bon marché |

## 4. Contradictions internes de design/02

1. **Famille du vérificateur.** §7.3 exige une autre famille dès N2. §9.1 et §14 acceptent une autre gamme de Claude jusqu'à N3. Il faut une seule règle dans `policy.yml` : la famille n'est vérifiée que pour un merge sans toi.
2. **`prove` dépend de `verify-<app>`**, créé seulement à l'étape 2. Soit `create-verify-app` entre dans `trust setup` à l'étape 1, soit l'étape 1 prouve en direct (lancer l'app, faire une capture).
3. **Le plafond merge-ready ne tient que par la prose en N2** : un PASS rend la gate verte sans ton approbation (voir §3.3).
4. **design/01 §14 dit « je garde les dix invariants » du blueprint**, mais design/02 en publie dix autres. Trois disparaissent sans le dire : « un point d'entrée unique », « un nœud = une responsabilité vérifiable » et « une arête = une condition ». Les deux derniers méritent de revenir dans le lint.
5. **§1 dit « le modèle ne peut pas se tromper de skill ».** C'est trop fort : un nœud lu par chemin peut être lu de travers ou pas lu du tout. Il faut une vérification par transcript (synthèse 03 §6.3).
6. **`reflect` dans 02 correspond à la « Retro » de notre glossaire**, pas à son « Reflect ». « Niveau d'autonomie » vaut 0–3 dans le glossaire et N0–N5 dans 02.

## 5. Tensions entre les sources

Ces points ne sont pas des erreurs : les sources se contredisent, et on doit trancher en connaissance de cause.

| Tension | Positions | Proposition |
|---|---|---|
| Même builder ou agent frais pour les fixes | Ray : même builder, 38 % moins cher et meilleur, sur ~10 PR. Matt et pstack : agent frais à chaque round. Anthropic *fold* : une boucle unique par défaut | garder l'écart assumé, et faire de la tension 1 le premier eval de l'étape 3 |
| Vérificateur d'une autre famille | Aucune source ne l'exige partout : pstack ne l'exige que dans `orchestrate`, Anthropic utilise un Claude. Anthropic *multiagent* montre que des agents identiques se trompent ensemble | garder l'exigence pour le merge sans toi, et la mesurer |
| Auto-merge en N4 et N5 | Matt garde toujours une revue humaine. L'automation de pstack (`benny`) n'ouvre que des PR en brouillon. Lauren auto-merge, mais après six mois d'environnement | l'affirmer comme écart assumé dans 02, conditionné à §3.1 et §3.8 |
| Identité séparée dès N3 | Lauren et pstack : en autopilot-stack, « you review and land them yourself ». Le hook suffit tant que tu merges | à trancher : identité dès N3 (plus sûr) ou seulement en N4 (moins de mise en place) |

## 6. Citations à corriger

| Où | Erreur | Correction |
|---|---|---|
| 02 §16 | pstack « route par description », « impossible d'évaluer une étape seule », « tout le savoir au même endroit » | 57 des 58 skills de pstack ont `disable-model-invocation: true` ; ses playbooks s'ouvrent par chemin, son SKILL.md est un index, et le guide 09 teste un changement de skill à l'aveugle. Notre routage par chemin **vient** de pstack |
| 02 §16 | `disable-model-invocation` « propre à Claude Code » | pstack l'utilise sous Cursor ; pour Codex, `install.py` écrit `allow_implicit_invocation: false` |
| 02 §16 | Matt n'aurait « ni colonne ni contrat » | il a un flux principal et des contrats ; ne pas posséder le processus est un choix de sa part |
| 02 §8.2 | « un agent, pas dix », règles « reprises d'`orchestrate` » | l'original dit « fifty » et « Call no scripts » ; le script sur `touches` est notre ajout |
| 02 §5 | Ray, « 38 % moins cher » | Ray dit aussi « better » ; c'est sur ~10 PR, dans un contexte promotionnel, et pour les fixes de review uniquement |
| 01 §4 | « vérifier à la frontière de capacité » = vérifier le risque | la frontière désigne la difficulté de la tâche pour le modèle (Anthropic *harness*, relu par Ray) |
| 01 §13, 02 §13 | « pas de personas : la bureaucratie est garantie » | Ray dit que ça ne marche pas « right now » |
| 01 §10, 02 §10.3 | Matt, « fixes never chain » | la règle veut dire « un échec dans un run de fix ne déclenche rien » ; « jamais au milieu d'une tâche » vient du guide 09 de pstack |
| 02 §4.2 | `ratchet` « durcit un check » | le check ne change pas : un fichier sort de la liste d'exceptions et est corrigé |
| 01 §3 | « Rien n'y dit comment le mériter » | le guide 07 pose quatre conditions ; ce qui manque, c'est un niveau mesuré par repo et par classe |
| 01 §6 | Permissions = protection de branche | chez Anthropic, c'est une décision par appel d'outil ; l'équivalent est le hook |
| 02 §6.3 | le repli de l'outil de question | tstack passe par l'outil parce qu'un message normal « goes unseen » quand tu es absent ; le chemin sûr est « leave the PR open and unmerged » |
| 02 §10.3 | règle de croissance | la phrase commence par « Start smaller than you think » |

## 7. Plan de révision proposé pour design/02

Dans cet ordre, du plus structurant au plus cosmétique :

1. **Le verdict** (§3.1) : calibration, règle de blocage, lane live, revue de code et standards, FAIL prouvé, défauts semés, identité vérifiée.
2. **Le codebase d'abord** (§3.2) : `correct` et `trust audit` dès l'étape 1, étape `clean`, condition de qualité pour entrer en N3.
3. **Les enforcers** (§3.3) et **les actes humains** (§3.5).
4. **Les nuits** (§3.4) : racine et owners en parallèle, workflow déterministe, journaux durables, idempotence.
5. **Réduire** (§3.7) : 15 skills, étape 0 minimale, voie légère, eval de bout en bout.
6. **Mesure, écriture, citations** (§3.8, §3.9, §6) et les contradictions de §4.

Deux décisions te reviennent avant cette révision : l'identité séparée dès N3 ou seulement en N4, et l'auto-merge en N4–N5 comme écart assumé.
