# Nectar — Harness design for long-running application development

> **Thèse en une phrase** : pour qu'un agent construise seul, pendant des heures, quelque chose qui marche vraiment, il faut **séparer celui qui fait de celui qui juge**, rendre le jugement **notable par des critères et des seuils**, négocier « fini » **avant** d'écrire le code, et **retirer chaque pièce du harnais** dès que le modèle n'en a plus besoin.

**Source** : Prithvi Rajasekaran, Anthropic Labs, 2026-03-24 · [article](https://www.anthropic.com/research/harness-design-long-running-apps) · [contenu hors-ligne](content.md)

---

## 1. Deux modes d'échec des runs longs

| Mode d'échec | Symptôme | Remède proposé |
|---|---|---|
| **Perte de cohérence** | le modèle dérive quand le contexte se remplit ; certains modèles ont une « context anxiety » et bâclent la fin | **context reset** + artefact de passation structuré (état, prochaines étapes) |
| **Auto-évaluation complaisante** | l'agent juge son propre travail excellent, même médiocre | un **évaluateur séparé**, réglé pour être sceptique |

Reset contre compaction :

- **compaction** : on résume l'historique sur place, le même agent continue. Continuité, mais pas d'ardoise propre : l'anxiété persiste.
- **reset** : un agent neuf repart d'un artefact de passation. Ardoise propre, mais l'artefact doit tout porter, et l'orchestration coûte en tokens et en latence.

Point daté : avec Sonnet 4.5, le reset était indispensable ; avec **Opus 4.5, l'auteur a supprimé les resets** et fait tourner tout le build en **une seule session** avec compaction automatique (Agent SDK). Le choix dépend du modèle, pas d'un principe.

**Pour notre framework** : **confirme** le choix de `design/02` §5 : « le même builder porte la PR de `frame` à `land` ». Sur des modèles récents, une session continue avec compaction tient plus de deux heures de build. Mais la conclusion est **liée au modèle** : l'adaptateur de harnais doit savoir faire un reset avec passation si un modèle builder montre de l'anxiété. Notre passation existe déjà : l'issue (contrat `done_when`), la PR (`Why/Proof/Risk/Decisions`) et `decisions.tsv`. Elle doit suffire à reprendre une PR **sans** le transcript.

---

## 2. Séparer le juge de l'auteur

Constats clés :

- un agent qui évalue son propre travail **le loue**, surtout sur des tâches subjectives ;
- un évaluateur séparé reste **un LLM indulgent envers un LLM** : la séparation ne suffit pas seule ;
- mais **rendre sceptique un évaluateur autonome est bien plus facile** que rendre critique un générateur envers lui-même ;
- une fois le retour externe en place, le générateur a quelque chose de **concret** contre quoi itérer.

« Out of the box, Claude is a poor QA agent » : il trouve de vrais bugs, puis **se convainc qu'ils ne sont pas graves** et approuve ; il teste en surface. Le réglage s'est fait par une boucle : **lire les logs de l'évaluateur, trouver où son jugement diverge du mien, corriger le prompt**, plusieurs rounds.

**Pour notre framework** : **confirme fortement** l'invariant 3 (« l'auteur n'est jamais le juge ») et la règle « le vérificateur ne corrige jamais ». **Complète** `design/02` sur deux points :

1. La séparation ne garantit pas la sévérité. `verify` a besoin de **calibrage** : des exemples few-shot de verdicts (PASS, PASS+NOTES, FAIL) tirés de vraies PR, et une règle explicite contre la rationalisation (« un défaut constaté reste un FAIL tant que le `done_when` ne le justifie pas »).
2. La boucle de réglage de l'auteur, c'est notre `reflect` → `eval` appliqué au skill `verify` : lire les verdicts, comparer à ton jugement, PR de skill, A/B. Il faut prévoir **des cas d'eval de verdicts**, pas seulement de builds.

L'article n'utilise **pas** une autre famille de modèles : son évaluateur est un Claude. Notre exigence « autre famille » va plus loin ; l'article ne la confirme ni ne l'infirme.

---

## 3. Rendre le jugement notable

Sur le design frontend, quatre critères donnés **au générateur et à l'évaluateur** :

| Critère | Ce qu'il mesure | Poids |
|---|---|---|
| Design quality | cohérence d'ensemble, identité | fort |
| Originality | choix délibérés, pas de « AI slop » | fort |
| Craft | typo, espacements, contrastes | faible (déjà bon par défaut) |
| Functionality | utilisabilité | faible (déjà bon par défaut) |

Leçons :

- **pondérer là où le modèle est faible**, pas là où il est déjà bon ;
- **calibrer** l'évaluateur avec des exemples few-shot détaillés : moins de dérive des notes ;
- la **formulation des critères oriente la sortie** (« museum quality » fait converger les designs) ;
- les scores montent puis plafonnent, **pas toujours linéairement** : l'auteur préfère parfois une itération intermédiaire ;
- l'évaluateur **interagit avec l'app vivante** (Playwright), il ne note pas une capture.

En full-stack : critères produit, fonctionnalité, design, qualité du code, **chacun avec un seuil dur** ; un seul critère sous le seuil = sprint en échec, avec retour détaillé.

**Pour notre framework** : **confirme** que `prove` et `verify` doivent **exercer l'application réelle** via `verify-<app>` (navigateur, API, base), pas relire le diff. **Confirme** le verdict à seuils : un FAIL sur n'importe quel critère du `done_when`. Les constats de l'évaluateur de l'article (fichier, ligne, condition fautive, correction) donnent le **niveau de précision** attendu d'un commentaire de verdict : actionnable sans enquête.

---

## 4. Le contrat de sprint : « fini » avant le code

Avant chaque sprint, générateur et évaluateur **négocient un contrat** : ce qui sera construit et **comment le succès sera vérifié**. Ils itèrent jusqu'à accord. Le sprint 3 avait **27 critères**. La communication passe **par des fichiers** : l'un écrit, l'autre lit et répond.

Pourquoi : la spec du planner est volontairement haut niveau (produit, pas implémentation), car une erreur technique dans la spec **cascade** dans tout le build. Le contrat fait le pont entre user stories et comportements testables.

**Pour notre framework** : **confirme** `frame` (« fini quand » vérifiable avant de construire) et le contrat d'unité en tête d'issue (§8.2). **Suggère** un ajout : faire **relire le `done_when` par le rôle vérificateur avant `build`** quand la classe de risque est `medium` ou `high`. Un `done_when` que le juge trouve invérifiable coûte alors un message, pas un FAIL après deux heures. Et **confirme** la communication par artefacts (fichiers, issues, PR) plutôt que par messages entre agents : c'est notre invariant 8.

Le planner, lui, **reste utile** même avec Opus 4.6 : sans lui, le générateur **sous-dimensionne** le travail. C'est un argument pour `shape` et `frame`.

---

## 5. Chaque composant est une hypothèse périmable

> « Every component in a harness encodes an assumption about what the model can't do on its own. »

Méthode de simplification :

1. couper radicalement **ne marche pas** : on ne sait plus ce qui portait la charge ;
2. retirer **un composant à la fois** et mesurer l'effet ;
3. refaire l'exercice **à chaque nouveau modèle**.

Résultat avec Opus 4.6 : **sprints supprimés**, planner gardé, évaluateur déplacé en **une passe finale** au lieu d'une par sprint (3 rounds build/QA sur le DAW).

**Pour notre framework** : **confirme exactement** l'invariant 9 (« chaque skill déclare son hypothèse et peut être supprimé »), le champ `metadata.hypothesis` et le mode `prune` d'`eval`. La méthode « un composant à la fois » doit être la règle de `prune`. Ajouter un déclencheur : **une nouvelle version du modèle builder lance une campagne `prune`** sur les skills de la colonne.

---

## 6. L'évaluateur n'est pas un oui/non

> « The evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo. »

Sur Opus 4.5, les builds étaient à la limite du modèle : l'évaluateur trouvait des problèmes partout. Sur 4.6, la frontière a reculé : pour les tâches **en deçà**, l'évaluateur devient du **coût pur** ; pour celles **au-delà**, il apporte encore un vrai gain (fonctionnalités « stub », détails manqués).

**Pour notre framework** : c'est **le point qui challenge le plus `design/02`**. Notre gate exige un verdict d'une autre famille **à partir de N2, pour toute PR**, quelle que soit sa difficulté. L'article suggère que la valeur du vérificateur **dépend de la distance entre la tâche et la capacité du builder**. Pistes compatibles avec nos invariants :

- garder le verdict **obligatoire** pour merger sans toi (la gate est une garantie, pas une optimisation) ;
- mais **proportionner la profondeur** du `verify` à la classe de risque, comme `prove` se proportionne déjà au risque ;
- mesurer, par classe, le **taux de FAIL utiles** : une classe où `verify` ne trouve jamais rien est candidate à un `verify` léger, pas à sa suppression.

---

## 7. Coût et durée : l'ordre de grandeur

| Run | Durée | Coût |
|---|---|---|
| Solo, game maker | 20 min | 9 $ |
| Harnais V1, game maker | 6 h | 200 $ |
| Harnais V2, DAW | 3 h 50 | 124,70 $ |
| dont QA (3 rounds) | ~25 min | ~10 $ |

Le harnais coûte **plus de 20×** le solo, mais le solo **ne marche pas** (le jeu ne répond pas aux entrées). Dans le V2, le **QA pèse moins de 10 %** du coût ; l'essentiel va au build.

**Pour notre framework** : **confirme** que le vérificateur est bon marché par rapport au builder : l'argument « trop cher » contre `verify` ne tient pas. **Confirme** l'invariant 7 (budgets) : sans budget, un harnais long dépense des centaines de dollars. Nos budgets comptent des **tentatives** (3 builds, 5 rounds, 2 FAIL) ; il manque peut-être un **budget en tokens ou en dollars par run d'`autopilot`**, déclaré dans `policy.yml`, pour les nuits non surveillées.

---

## 8. Implications pour notre framework de skills

### 8.1 Ce que l'article confirme dans `design/02`

- **Invariant 3** : auteur ≠ juge ; le juge ne corrige pas, il renvoie des constats.
- **§5, même builder de bout en bout** : une session continue avec compaction tient des heures sur un modèle récent.
- **Contrat avant code** : `frame`, `done_when`, contrat d'unité en tête d'issue.
- **Preuve sur l'app vivante** : `verify-<app>` qui clique, appelle l'API, lit la base.
- **Invariant 8** : communication par artefacts (fichiers, issues, PR), pas par mémoire d'agent.
- **Invariant 9 et `prune`** : chaque composant est une hypothèse à re-tester.
- **Budgets** : sans eux, un run long coûte cher.

### 8.2 Ce que l'article challenge ou complète

1. **La valeur du vérificateur varie** avec la difficulté de la tâche. À traiter par la profondeur du `verify`, pas par sa suppression.
2. **La séparation ne suffit pas** : `verify` doit être **calibré** (few-shot, règle anti-rationalisation) et **évalué** sur des cas de verdicts.
3. **Reset ou compaction dépend du modèle** : l'adaptateur de harnais doit pouvoir faire un reset avec passation ; nos artefacts (issue, PR, `decisions.tsv`) doivent suffire à reprendre sans transcript.
4. **Le `done_when` gagne à être relu par le juge avant le build**, pour les classes à risque.
5. **Budget en tokens ou en dollars** pour `autopilot`, en plus des budgets en tentatives.
6. **Nouveau modèle = campagne `prune`** sur la colonne.

### 8.3 Ce que l'article ne couvre pas

- Pas de PR, pas de CI, pas de merge : l'app est construite **dans un seul repo vierge**, sans revue humaine ni gate. Notre colonne (`open-pr`, `babysit`, `land`) n'a pas d'équivalent.
- Pas de parallélisme : un seul générateur. Rien sur `orchestrate`.
- Pas d'autre famille de modèles pour le juge.
- Pas de mesure statistique : deux apps, des runs uniques. À traiter comme des **hypothèses** à vérifier par nos propres `eval`.

---

## 9. Citations à garder

> « Separating the agent doing the work from the agent judging it proves to be a strong lever to address this issue. »

> « Tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work. »

> « Out of the box, Claude is a poor QA agent. In early runs, I watched it identify legitimate issues, then talk itself into deciding they weren't a big deal and approve the work anyway. »

> « Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing. »

> « The evaluator is not a fixed yes-or-no decision. It is worth the cost when the task sits beyond what the current model does reliably solo. »

> « The space of interesting harness combinations doesn't shrink as models improve. Instead, it moves. »
