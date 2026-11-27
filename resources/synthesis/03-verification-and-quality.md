# Vérification et qualité

**But de ce document** : définir ce qui compte comme « fini », comment prouver qu'un changement est bon, et comment vérifier les skills eux-mêmes.

Sources principales : Lauren Tan (pyramide, feature map, vérification formelle), Ray Amjad (vérification à la frontière de capacité), tstack (proof, merge gate), pstack (`prove-it-works`, `benchmark-checklist`, `eval`).

---

## 1. La vérification est le vrai goulot

Le corpus converge sur un point : produire du code est devenu facile ; **savoir qu'il est bon** est devenu le coût dominant.

- Lauren Tan : ~70 % des tokens vont en vérification.
- Ray Amjad : les meilleurs gains viennent du verifier, mais seulement à la frontière de capacité.
- tstack : une PR n'est pas finie tant que la preuve ne couvre pas chaque changement et que la merge gate ne passe pas.

**Conséquence** : un framework de skills qui n'a pas de couche de vérification est un framework de génération de slop.

---

## 2. La pile de vérification

Toutes les vérifications ne se valent pas. Il faut les empiler, du moins cher au plus cher.

| Niveau | Coût | Confiance | Exemples | Quand l'utiliser |
|---|---:|---|---|---|
| **Statique** | Très bas | Moyenne | Types, lint, compilation, dependency graph | Toujours |
| **Tests unitaires** | Bas | Moyenne | Comportement d'une fonction | À chaque changement logique |
| **Tests d'intégration** | Moyen | Haute | API + DB, contrats | À chaque changement de frontière |
| **Runtime** | Moyen | Haute | Lancer l'app, CDP, Playwright, captures | UI, flux utilisateur, bugs |
| **Property-based** | Moyen | Haute | Bombadil, génération d'interactions | UI, invariants |
| **Formel** | Élevé | Très haute | TLA+, Lean | Concurrence, protocoles, algorithmes |
| **Revue humaine** | Élevé | Variable | Artefacts, diff, décisions | Actions irréversibles, design |

**Règle** : utiliser le niveau **le plus bas** qui prouve le changement. Ne pas sauter directement au formel parce que c'est impressionnant.

---

## 3. Le standard de preuve

### 3.1 Proof (tstack)

Une preuve est une **évidence observée dans la session** :

- sortie de commande ;
- reproduction qui échoue puis passe ;
- capture d'écran ou vidéo ;
- test qui échoue sans le fix ;
- valeur stockée, profil, log.

Ce n'est **pas** :

- « le build passe » ;
- « l'agent dit que c'est fait » ;
- « les tests mockés sont verts » ;
- « le code semble correct ».

> « When you cannot find a way to prove a change, you do not have full confidence. Ask the user. » — `full-send`

### 3.2 Merge gate (tstack)

Une gate n'est pas une sensation. C'est une liste de conditions observables :

- la preuve couvre chaque changement du diff ;
- les checks requis sont verts ;
- les review bots ont fini ;
- chaque finding est corrigé ou rejeté avec une raison écrite ;
- aucune review humaine ne demande encore un changement ;
- la branche est à jour et mergeable.

**Pour notre framework** : chaque skill de livraison doit déclarer sa **gate**, et chaque gate doit être une liste de conditions vérifiables.

### 3.3 Prove it works (pstack)

Le principe est plus large que la PR :

> Verify against the real artifact (run the feature, read the actual value, inspect the diff), not a proxy, self-report, or "it compiles".

**Test** : si l'agent peut te montrer la preuve sans que tu exécutes rien, c'est une bonne preuve. S'il te dit « fais-moi confiance », ce n'est pas une preuve.

---

## 4. Vérifier à la frontière de capacité

C'est l'idée la plus contre-intuitive du corpus.

> « the biggest gains in having an evaluator or a verifier agent evaluating at the edges of what the current models are capable of » — Ray Amjad, 10:51

### 4.1 Le principe

- Si le modèle réussit toujours la tâche, le verifier ne fait que confirmer. C'est du coût sans information.
- Si la tâche est à la frontière, le verifier attrape des erreurs réelles. C'est du gain.
- Si la tâche est au-delà de la frontière, le verifier échoue aussi. Il faut un humain ou un autre outil.

### 4.2 Exemples

| Tâche | Frontière ? | Verifier utile ? |
|---|---|---|
| Formulaire de contact simple | Non, bien en deçà | Non |
| Sync offline/online avec merge | Oui | Oui |
| Race condition subtile | Oui | Oui, plus formel |
| Migration de données irréversible | Oui + risque | Oui + humain |
| Traduction de docs | Non | Non, sauf review de qualité |

### 4.3 L'effet de cliquet

Quand le modèle progresse, la frontière se déplace. Ce qui était à la frontière devient trivial ; le verifier devient inutile. Il faut **réévaluer** régulièrement.

**Règle** : chaque skill de vérification doit déclarer :

- quelle **propriété** il vérifie ;
- sur quel **type de tâche** ;
- quelle **hypothèse de capacité** il encode ;
- quand il faut le **supprimer**.

---

## 5. Les artefacts de vérification

La revue humaine se déplace du code vers les **artefacts** :

- vidéos et captures ;
- diagrammes de state machine ;
- feature maps ;
- profils de performance ;
- sorties de tests ;
- preuves formelles.

### 5.1 Feature map

Une carte des fonctionnalités du point de vue utilisateur. Elle donne :

- un **vocabulaire partagé** (« le panneau de notifications » au lieu de « le truc à gauche ») ;
- une **couverture** explicite ;
- un support pour le fan-out de vérification par flux.

**Pour notre framework** : un skill de vérification projet devrait générer et maintenir une feature map. C'est un artefact durable, pas un prompt.

### 5.2 CLIs de pilotage

Des pilotes réutilisables pour l'agent :

- lancer l'app ;
- naviguer ;
- capturer ;
- lire l'état ;
- injecter un scénario.

Avantages : moins de tokens, comportement testable, cohérence entre runs.

**Pour notre framework** : les skills de vérification runtime doivent s'appuyer sur des **outils**, pas sur des instructions en prose.

---

## 6. Vérifier un skill

Un skill est un artefact logiciel. Il doit être vérifié comme tel.

### 6.1 Validation structurelle

- frontmatter valide ;
- pointeurs existants ;
- liens croisés résolus ;
- pas de duplication ;
- pas de dossier orphelin ;
- taille raisonnable ;
- critères de complétion présents.

**Automatisable** : un script de lint de skills.

### 6.2 Évaluation comportementale

Le protocole de pstack (`eval`) est le plus abouti :

1. **Frame** : quelle variante, quel comportement de succès, rubrique de 3–6 critères.
2. **Environnements sanitisés** : un répertoire par candidat, avec le variant en place.
3. **Prompt organique** : ce qu'un utilisateur taperait, sans méta.
4. **N candidats parallèles** : mêmes conditions, modèles différents.
5. **Juge aveugle** : un modèle d'une autre famille, qui voit les sorties par label sanitisé.
6. **Vérification de la chaîne** : lire les transcripts pour voir quels fichiers l'agent a réellement ouverts, pas ce qu'il prétend.
7. **Synthèse** : lire chaque sortie, comparer au jugement, recommandation.

**Règles de blinding** :

- aucun mot `eval`, `test`, `judge`, `rubric`, `score` dans les répertoires ou prompts candidats ;
- le prompt candidat ressemble à une requête utilisateur ;
- pas d'indices de chaîne ;
- les noms de répertoires sont neutres ;
- le juge ne voit pas les noms de modèles.

**Pour notre framework** : ne pas promouvoir un skill sans un eval aveugle, même léger. Sinon on accumule des croyances.

### 6.3 Vérification par transcript

Le self-report est une mauvaise source. Ce qui compte :

- quels fichiers l'agent a lus ;
- quels outils il a appelés ;
- quel ordre il a suivi ;
- où il a divergé.

**Règle** : évaluer la **chaîne d'exécution**, pas la narration.

---

## 7. Les métriques

### 7.1 Métriques de qualité

| Métrique | Ce qu'elle mesure | Cible |
|---|---|---|
| **Taux de revert** | Qualité perçue en production | Bas et stable |
| **Defects échappés** | Bugs trouvés après merge | En baisse |
| **Coverage des preuves** | % de changements avec preuve | 100 % pour les changements risqués |
| **Taux de passage des gates** | Gates qui passent du premier coup | En hausse |
| **Faux positifs de review** | Findings rejetés / total | En baisse |
| **Temps jusqu'à preuve** | Durée entre changement et évidence | En baisse |
| **Coût par changement vérifié** | Tokens + temps | En baisse |

### 7.2 Métriques d'orchestration

| Métrique | Ce qu'elle mesure |
|---|---|
| **Taux de runs réussis** | Fiabilité du graphe |
| **Taux d'escalade** | Fréquence des blocages humains |
| **Rounds moyens de review** | Efficacité du builder |
| **Taux de reprise après crash** | Robustesse de l'état |
| **Latence d'approbation** | Fluidité des gates |
| **Bruit de l'outbox** | Charge de notification |

### 7.3 Métriques de skill

| Métrique | Ce qu'elle mesure |
|---|---|
| **Taux de déclenchement correct** | Le skill fire quand il faut |
| **Taux de complétion** | Le skill va au bout |
| **Coût en tokens** | Charge du skill |
| **Taux de correction humaine** | Qualité de la sortie |
| **Taux de suppression** | Le skill devient-il obsolète ? |

**Règle** : mesurer le **coût total** (tokens + temps + humain), pas seulement le nombre de PR.

---

## 8. Les anti-patterns

| Anti-pattern | Symptôme | Correctif |
|---|---|---|
| **Green build = done** | Le build passe, le bug reste | Preuve runtime, test qui échoue sans le fix |
| **Self-report** | « J'ai vérifié » sans artefact | Exiger la sortie, la capture, le test |
| **Vérifier tout** | Chaque tâche a un verifier | Vérifier à la frontière |
| **Vérifier rien** | Pas de gate | Gate minimale + preuve |
| **Benchmark non vetté** | « 40 % plus rapide » sans contrôle | `benchmark-checklist` |
| **Review infinie** | Rounds sans budget | Budget + escalade |
| **Scope creep** | Les reviews ajoutent des features | « Fight to keep scope limited » |
| **Faux positifs acceptés** | Chaque commentaire de bot est corrigé | Trier : fix / dismiss / ask |
| **Preuve proxy** | Tests mockés pour une UI | Lancer l'app |
| **Preuve non reproductible** | Capture sans étapes | Commande, fixture, scénario |

---

## 9. Checklist pour nos futurs skills

### Pour chaque skill

- [ ] Le skill déclare son **artefact de sortie**.
- [ ] Le skill déclare sa **preuve**.
- [ ] Le skill déclare ses **conditions d'échec**.
- [ ] Le skill déclare ses **gates** (si action irréversible).
- [ ] Le skill déclare son **budget** (si boucle).
- [ ] Le skill déclare son **hypothèse de capacité** (si vérification).

### Pour chaque gates

- [ ] La gate est binaire (pass/fail/wait).
- [ ] La gate est observable sans jugement subjectif.
- [ ] La gate a un propriétaire (agent, humain, outil).
- [ ] La gate a une action de remédiation.
- [ ] La gate a un délai ou un budget.

### Pour chaque eval

- [ ] Le prompt est organique.
- [ ] Le candidat ne sait pas qu'il est évalué.
- [ ] Le juge est d'une autre famille de modèles.
- [ ] Le juge voit des labels sanitisés.
- [ ] Les transcripts sont inspectés.
- [ ] La décision de promotion est écrite.

---

## 10. Ce que cela implique pour notre framework

1. **La vérification est un nœud, pas une étape.** Elle a ses propres skills, ses outils, ses budgets.
2. **Le standard de preuve est global.** Tous les skills de livraison partagent la même définition de « done ».
3. **Les gates sont déclaratives.** Un skill ne « décide » pas qu'il a fini ; il passe une gate.
4. **Les evals sont obligatoires.** Un skill non évalué est une hypothèse, pas un composant.
5. **Les métriques sont instrumentées.** Sans traces, pas d'amélioration.
6. **Les hypothèses sont datées.** Chaque vérification encode une limite de modèle ; elle doit être réévaluée.

---

## 11. Questions ouvertes

- **Quel est le coût acceptable d'un eval ?** Combien de runs, de tokens, de temps ?
- **Comment évaluer un skill d'orchestration ?** Pas seulement la sortie, mais la topologie choisie.
- **Comment mesurer le couplage ?** Nombre d'artefacts partagés, fréquence de conflits, temps de merge ?
- **Comment gérer les preuves non déterministes ?** UI, performances, données réelles.
- **Quand supprimer un verifier ?** Quel signal indique que la frontière a bougé ?
- **Comment éviter les evals qui mesurent la chance ?** Taille d'échantillon, variance, répétitions.
