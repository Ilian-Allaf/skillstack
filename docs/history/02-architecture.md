# Architecture 02 — Le framework de skills (v3)

> **Frozen on 2026-11-19.** History only, in French: names, decisions, and paths are those of their time and bind nothing. Decisions in force: [docs/adr/](../adr/). How the framework works today: [skills/README.md](../../skills/README.md).

> **Statut** : v3, du 2026-11-18. Construits en v0, non prouvés : `constitution` (dossier partagé), `choose-skill`, `setup-repo`, `create-app-driver` (avec le mode `formal`), `add-guardrail`, `shape-spec`, `investigate`, `learn-from-mistakes`, `ship` (6 playbooks), `analyze-impact`, `verify-pr`, `babysit-pr`, et `tools/lint_skills.py`. Ajouts du 2026-11-19, repris de pstack et de Matt Pocock : `shape-spec` (grill, domain, spec, map), `learn-from-mistakes`, les références `parallel`, `decision-log`, `statechart` et `languages/typescript`, le playbook `bespoke`. `to-tickets` n'est pas repris : Ray Amjad et Anthropic montrent qu'un spec découpé en tickets confiés à des agents parallèles donne de moins bons résultats.
> **Ce qui change depuis la v2** ([archivée](02-architecture-v2.md)) : ta décision du 2026-11-18.
>
> - **Tu merges toujours toi-même, sans exception.** L'agent rend une PR prête à merger, et s'arrête là.
> - Disparaissent donc : le dossier `.trust/`, la gate de CI, l'échelle N0–N5, `/ship send`, le merge sans toi, le skill `trust` et le merge par `land`.
> - **Le centre du document devient la vérification** : comment l'agent prouve que son code marche et trouve ce qui casse (section 5).
>
> **Entrées** : le [brainstorm 01](01-brainstorm-pr-sereines.md), la [revue 03](03-revue-principes.md) et la base [`knowledge/`](../../knowledge/README.md).
> **Reste ouvert** : le repo cobaye (section 13).

---

## 1. En une phrase

> **Tu donnes une tâche. L'agent rend une PR prête à merger : il a prouvé sur l'app réelle qu'elle fait ce qui était demandé, il a cherché ce qu'elle casse ailleurs, et un vérificateur indépendant a essayé de la prendre en défaut. Tu lis, tu merges.**

Cinq choix structurent le reste :

1. **Le codebase d'abord, puis la vérification, puis l'automatisation** (Lauren Tan). « if your inner coding loop produces slop, then automating that loop just produces more slop ». On n'automatise rien tant que l'agent ne sait pas prouver une PR.
2. **Deux questions, pas une.** « Est-ce que ça fait ce qui était demandé ? » ne suffit pas. Il faut aussi « qu'est-ce que ça casse ailleurs ? » (pstack `blast-radius`).
3. **L'auteur n'est jamais le juge.** Un modèle vérifie ce qu'il a voulu construire, pas ce qu'il a construit. « Tuning a standalone evaluator to be skeptical turns out to be far more tractable than making a generator critical of its own work » (Anthropic, *harness design*).
4. **Seul ce qui a tourné compte.** Une affirmation sans exécution ne vaut rien, qu'elle vienne du builder ou du vérificateur (pstack `prove-it-works`, `interrogate`).
5. **Commencer petit.** Le catalogue est un plafond. Un skill n'entre que quand le même échec est vu deux fois (pstack, « Start smaller than you think »).

## 2. Vue d'ensemble

```text
                 TOI : /ship <tâche>, puis tu lis la PR et tu merges
                  │                                        ▲
┌─────────────────▼────────────────────────────────────────┴───────────┐
│ ENTRÉES       ship · shape-spec · investigate (lancées par toi)       │
│ FAÇONNAGE     shape-spec : grill, spec, map (si la tâche est floue)  │
│ COLONNE       ship (frame, build, clean, prove, open-pr)              │
│               → analyze-impact → verify-pr → babysit-pr → PR prête    │
│ KIT           setup-repo · create-app-driver · add-guardrail · ratchet│
│ MÉTA          learn-from-mistakes · lint des skills (script)          │
│ CONSTITUTION  principes, standard de preuve, glossaire, harnais       │
└──────────────────┬───────────────────────────────────────────────────┘
                   │ écrit et lit
                   ▼
     REPO CIBLE : drive-<app> et sa feature map, lints, types, tests,
                  CODING_STANDARDS.md ; GitHub : PR, issues, labels
```

- **La colonne** est le chemin de chaque tâche, jusqu'à une PR prête.
- **Le kit** écrit dans ton repo ce qui rend la vérification possible : un pilote de l'app, des checks qui empêchent les erreurs connues.
- **Le méta** transforme chaque problème raté en check, après ton accord.

## 3. Les invariants

1. **L'agent ne merge jamais.** Il s'arrête à « prête à merger ». Un hook du harnais bloque `gh pr merge`, `--auto` et la merge queue, pour que la règle ne dépende pas d'une phrase dans un skill.
2. **L'auteur n'est jamais le juge.** Le vérificateur est un agent frais, sans droit d'écriture, d'une autre famille de modèle quand elle est disponible.
3. **Une affirmation porte son niveau de certitude** (section 5.2). « J'ai vérifié » sans exécution est une affirmation de niveau 1.
4. **Un problème bloque seulement s'il est prouvé** : une exécution qui échoue sur la tête de la PR. Sinon c'est une note, qui devient une issue (règle de blocage de pstack).
5. **Un verdict couvre un patch.** Du nouveau code exige un nouveau verdict ; un rebase pur le conserve (`patch-id`, pstack).
6. **Chaque boucle a un budget.** À épuisement, le run teste sa prémisse, replanifie une fois, puis s'arrête sur un résumé et une recommandation.
7. **Chaque problème raté devient un check.** Un bug que tu trouves après coup donne un lint, un type ou un test (`add-guardrail`), et un défaut semé pour le vérificateur.
8. **L'état vit dans GitHub** : PR, issues, labels, commentaires. Jamais dans la seule mémoire d'un agent.
9. **Chaque étape est idempotente.** Elle lit l'état existant et n'applique que la différence.
10. **Chaque skill déclare son hypothèse** et peut être supprimé.

## 4. Les skills

### 4.1 La règle de découpage

Une étape devient un skill si elle remplit au moins une condition :

- **on l'appelle seule** : « vérifie la PR 42 », « qu'est-ce que ça casse ? » ;
- **plusieurs appelants la réutilisent** ;
- **un autre rôle l'exécute** : le vérificateur.

Sinon, c'est une section d'un skill existant. `frame`, `build`, `clean`, `prove` et `open-pr` sont donc des sections de `ship`.

### 4.2 Le catalogue : 13 skills au plus

C'est un **plafond**, pas un plan. Les skills des dernières étapes n'entrent que si la règle des deux échecs les déclenche.

| Famille | Skill | Ce qu'il fait | Étape |
|---|---|---|---|
| Référence | `constitution` | **pas un skill** (depuis le 2026-11-19) : un dossier partagé (`README.md`, sans frontmatter) que chaque skill lit par chemin ; aucun harnais ne le liste. Principes, standard de preuve et échelle de certitude, glossaire, rôles, adaptateurs de harnais, format de PR, repo cible | 0 |
| Entrée | `choose-skill` | le routeur : tu décris ta situation, il te donne le skill à lancer et la commande ; ne lance rien. Le seul skill à retenir | 2 (v0 écrit) |
| Kit | `setup-repo` | la première fois dans un repo : vérifie ce que l'agent peut faire, installe le hook anti-merge et les labels, rédige glossaire, standards et fichier agent depuis le code, propose `create-app-driver` et l'audit ; demande avant chaque partie, finit par un bilan | 2 (v0 écrit) |
| Kit | `create-app-driver` | crée le skill `drive-<app>` du repo (lancer, piloter, observer l'app) et sa feature map ; le prouve de bout en bout ; le maintient | 1 |
| Kit | `add-guardrail` | `audit` mesure les fondations du code ; une correction devient un check, prouvé sur l'erreur réelle | 1 |
| Entrée | `ship` | une tâche → une PR prête. Sections `frame`, `build` (playbooks), `clean`, `prove`, `open-pr` | 2 |
| Colonne | `analyze-impact` | cherche ce qu'un changement casse ailleurs, et prouve le fait dont dépend sa sûreté ; lance le check formel du repo quand le diff touche un fichier qu'il couvre | 2 |
| Colonne | `babysit-pr` | conflits, reviews, CI ; triage sceptique, fixes reprouvés ; restack après ton merge | 2 |
| Colonne | `verify-pr` | rôle vérificateur : essaie de prendre la PR en défaut et rend un verdict par axe | 3 |
| Méta | `learn-from-mistakes` | retro sur une session, une PR en échec, ou un bug trouvé après coup ; trois relecteurs, une synthèse, rien d'appliqué sans ton accord | 4 (v0 écrit) |
| Kit | `ratchet` | à ta demande : une PR qui durcit une règle sur un fichier de plus | 4 |
| Entrée | `investigate` | répond sans changer le produit : `question` (how, why, quel choix), `diagnosis` (cause d'un symptôme à l'exécution), `prototype` (une décision par l'expérience) ; propose la tâche `/ship` sans la lancer | 2 (v0 écrit) |
| Façonnage | `shape-spec` | `grill` (+ glossaire et ADR), `spec`, `map` : d'une intention floue à une spec ; pas de découpage en tickets | 2 (v0 écrit) |

Plus un script dès l'étape 0 : `tools/lint_skills.py`.

### 4.3 Le graphe

Le graphe fait foi dans [`skills/README.md`](../../skills/README.md) : la carte des skills et le parcours d'une tâche, en Mermaid. `tools/check_refs.py` échoue (règle R006) si un skill y manque, pour qu'il ne se périme pas.

Chaque flèche pleine est un `calls` du frontmatter : le skill appelant lit le `SKILL.md` appelé par son chemin (routage pstack). Les lectures d'un fichier d'un autre skill sont des `reads`. La lint vérifie que le texte et le frontmatter disent la même chose (règles F014 et F015).

## 5. Le cœur : comment l'agent vérifie et trouve les problèmes

Cette section explique le pourquoi. Les règles qui font foi sont dans les skills (`constitution`, `ship`, `verify-pr`, `analyze-impact`) ; quand les deux divergent, ce sont les skills qui ont raison, et cette section doit être corrigée.

C'est la section qui compte. Tout le reste sert à la faire tenir.

### 5.1 Le principe : chaque couche attrape ce que la précédente laisse passer

Le corpus converge : produire du code est devenu facile, **savoir qu'il est bon** est le coût dominant. Lauren Tan y consacre environ 70 % de ses tokens. On empile donc les vérifications, de la moins chère à la plus chère, et chaque couche a un rôle que les autres ne jouent pas.

| # | Couche | Où | Question | Attrape | Source |
|---|---|---|---|---|---|
| 0 | Le code lui-même | `add-guardrail`, `ratchet` | l'erreur peut-elle seulement s'écrire ? | les erreurs connues, avant qu'elles existent | Lauren Tan, pstack `correct` |
| 1 | Le contrat | `ship › frame` | sait-on ce que « fini » veut dire, et peut-on l'observer ? | la mauvaise tâche, bien faite | harness design, Matt |
| 2 | La boucle rouge → vert | `ship › build` | ai-je un signal qui échoue sur ce problème précis ? | le fix qui ne fixe rien | Matt `diagnosing-bugs`, `tdd` |
| 3 | Les checks du repo | `ship › clean` | lint, types et tests sont-ils verts ? | les régressions déjà couvertes | — |
| 4 | La preuve sur l'app réelle | `ship › prove` + `drive-<app>` | le comportement change-t-il vraiment pour l'utilisateur ? | « les tests passent, l'app est cassée » | pstack `create-verification-skill`, tstack |
| 5 | L'onde de choc | `analyze-impact` | qu'est-ce que ça casse ailleurs ? | les régressions hors du diff | pstack `blast-radius` |
| 6 | Le juge indépendant | `verify-pr` | un autre modèle, sceptique, arrive-t-il à la casser ? | ce que l'auteur ne voit pas | harness design, pstack `interrogate`, Matt `code-review` |
| 7 | Le retour d'expérience | `learn-from-mistakes`, `add-guardrail` | pourquoi ce bug est-il passé ? | les trous du système lui-même | Lauren Tan, Matt `retro` |

Les sections suivantes détaillent chaque couche.

### 5.2 L'échelle de certitude

Reprise de pstack `blast-radius`, et appliquée à **toute** affirmation de l'agent, dans la PR comme dans le verdict :

| Niveau | Ce qui a été fait | Exemple |
|---|---|---|
| 1 · dit | l'agent l'affirme | « ça ne touche pas l'export » |
| 2 · pointé | une ligne réelle est citée, `fichier:ligne` | « `export.ts:42` ne lit pas ce champ » |
| 3 · raisonné | le cas d'échec a été déroulé pas à pas, et il n'arrive pas | « le seul appelant passe toujours une note sauvegardée » |
| 4 · exécuté | un script ou un test appelle le vrai code, et échouerait si c'était faux | `npm test -- export.double-save` |
| 5 · reproduit | observé dans l'app qui tourne | capture avant/après via `drive-notes` |

Règles :

- **Le fait dont dépend la sûreté du changement doit atteindre le niveau 4.** Sinon, il est marqué `unproven` dans la PR, en clair.
- **Le comportement demandé (`done_when`) doit atteindre le niveau 5** quand l'app a une surface utilisateur, et le niveau 4 pour une lib ou une CLI sans état.
- La PR dit, pour chaque affirmation importante, le niveau atteint. Tu sais ainsi ce qui a été vu et ce qui est seulement cru.

### 5.3 Couche 1 — Le contrat, avant d'écrire du code

`frame` reformule la tâche (pstack `in-your-own-words`) : objectif, problème, plus petit changement, hors périmètre, classe de risque. Puis il fixe `done_when` :

- **observable** : une commande, un test ou un parcours dans l'app qui dit oui ou non ;
- **rouge sur la base** : on l'exécute avant de coder, et il doit échouer. Un `done_when` déjà vert ne prouve rien ;
- **tiré de ta demande**, pas inventé par l'agent. L'auteur ne fixe pas la barre de son propre juge ;
- **validé par toi** (ton « go ») et, en `high` ou en zone difficile, relu par le vérificateur avant `build`. Un `done_when` invérifiable coûte alors un message, pas un FAIL après deux heures (harness design).

`frame` marque aussi les **zones difficiles** pour le modèle : concurrence, synchronisation, perte de données, sécurité, migrations. C'est là que la vérification s'approfondit (Ray Amjad : le vérificateur rapporte surtout « at the edges of what the current models are capable of »).

La classe de risque n'a plus de fichier de config. `frame` l'annonce d'après une règle simple de la constitution :
- **high** : auth, migrations, paiement, suppression de données, CI, ou plus de 400 lignes ;
- **low** : uniquement docs ou tests ;
- **medium** : le reste.

Tu peux la corriger d'un mot. Elle ne sert qu'à **proportionner la vérification** (section 5.8).

### 5.4 Couche 2 — La boucle rouge → vert, pendant le code

Repris de Matt Pocock. « If you have a tight pass/fail signal for the bug, you will find the cause » (`diagnosing-bugs`).

- **Bug** : d'abord un signal qui échoue sur *ce* bug : test, script curl, CLI avec fixture, script de navigateur, rejeu d'une trace. Il va dans un commit séparé, avant le fix. Sans signal, l'agent ne fait pas d'hypothèse : il dit ce qu'il a essayé et te demande un accès ou un artefact.
- **Feature** : des tests aux interfaces publiques (« seams »), une tranche verticale à la fois (`tdd`). Les seams sont annoncés dans `frame`.
- **Interdits** : le test tautologique, qui recalcule l'attendu comme le code ; le test couplé à l'implémentation ; le mock d'un collaborateur interne. Une valeur attendue vient d'une source indépendante : un littéral connu, un exemple, la spec.
- **Budget** : 3 tentatives de `build`. Ensuite, le run teste sa prémisse, replanifie une fois, puis s'arrête avec `needs-human`.

### 5.5 Couche 4 — La preuve sur l'app réelle

C'est la couche la plus importante, et celle qui manque le plus souvent. Les tests verts disent que le code fait ce que les tests demandent, pas que l'app marche.

Le repo a un skill `drive-<app>`, écrit par `create-app-driver` d'après pstack `create-verification-skill`. Il contient :

- **Launch** : la commande qui démarre l'app depuis un état vide, et comment savoir qu'elle est utilisable ;
- **Doctor** : un check en lecture seule, « cette instance vaut-elle la peine d'être pilotée ? » ;
- **Drive** : la recette pour piloter l'app comme un utilisateur (Playwright pour le web, PTY pour une CLI, HTTP pour un service), avec les vrais sélecteurs du repo ;
- **Evidence** : quoi capturer : l'action et l'état qui en résulte, et les effets de bord (ligne en base, fichier écrit) ;
- **Cleanup** : arrêter ce que le run a lancé, sans effacer les preuves ;
- **la feature map** : une fiche par fonctionnalité, du point de vue de l'utilisateur. Comment y arriver, comment la piloter, quel état final prouve qu'elle marche (Lauren Tan, pstack).

`prove` s'en sert ainsi :

1. **Avant / après** : le même parcours sur la base et sur la tête. La différence est la preuve.
2. **Le vrai chemin utilisateur** : jamais un setter interne ni un endpoint de test.
3. **Toutes les entrées de la feature map** qui mènent à la fonctionnalité touchée, pas seulement la plus pratique.
4. **Rejouable** : la PR donne la commande, et tu peux la relancer.
5. **Sans proxy** : un test mocké ne prouve pas une UI ; « le build passe » ne prouve rien.

Quand l'agent ne trouve aucun moyen de prouver un changement, il le dit dans `Not verified` et te le signale. Il ne déclare pas « fini » (tstack `full-send` : « When you cannot find a way to prove a change, you do not have full confidence »).

### 5.5 bis La couverture : exhaustive, parce que tu ne relis que la preuve

Décidé le 2026-11-18. Tu relis la preuve, pas le code : ce qu'elle ne montre pas, tu ne le vois pas. Lauren Tan le dit : « our code review process has now really shrunk into looking at verification artifacts instead. So things like videos, screenshots, diagrams ». Détail dans `constitution/references/coverage.md`.

- **La liste des cas est fixée dans `frame`**, avant ton « go » : le cas principal, chaque point d'entrée de la feature map, les cas limites des zones difficiles.
- **L'agent choisit la meilleure preuve par cas** : un chapitre de vidéo pour un parcours, une capture pour un état, une sortie de commande pour le reste.
- **La PR s'ouvre sur une table de couverture** (cas → preuve → niveau). Aucun cas n'en sort : un cas sans preuve renvoie à `Not verified`.
- **La vidéo de démo** est exigée quand un parcours utilisateur change sur une surface visuelle. Elle est scriptée et rejouable, avec un chapitre et un sous-titre par cas.
- **Un diagramme d'états** accompagne les parcours à états. Chaque flèche porte le numéro du cas qui la couvre (pstack `statechart`).
- **Le vérificateur contrôle la couverture** : il rejoue les scripts de la démo et pilote les cas qu'il attendait. Un cas manquant qui se comporte mal est un FAIL ; un cas manquant correct est un trou de couverture, que le builder ajoute avant `ready`.
- **À confirmer sur le cobaye** : téléverser une vidéo pour qu'elle se lise dans la PR. `gh` n'a pas de commande pour ça ; le repli est un lien vers un artefact.

### 5.6 Couche 5 — L'onde de choc : `analyze-impact`

La preuve dit que le changement fait ce qui était demandé. Elle ne dit rien de ce qu'il casse ailleurs. `analyze-impact` reprend pstack `blast-radius` :

> « Listing the callers is not the job. The agent can grep those in a second. The job is the breakage grep won't show you. »

1. **Lire le changement**, y compris ce que le diff ne dit pas : un comportement qui change sans qu'une ligne le montre.
2. **Trouver le fait dont dépend la sûreté.** La plupart des changements qui ont l'air risqués sont sûrs grâce à un seul fait, par exemple « cet appel ne supprime que des entrées de cache déjà mortes ». S'il tient, la plupart des risques tombent d'un coup.
3. **Chercher là où grep s'arrête** :
   - le code source de la librairie appelée, dans sa version épinglée ;
   - l'ordre d'exécution (asynchrone, démontage, teardown) ;
   - le JSON renvoyé par une API, une colonne en base, un format sur le fil ;
   - un autre langage qui lit les mêmes octets ;
   - un feature flag, du code trois appels plus loin.
4. **Noter chaque risque honnêtement** : probabilité, coût, `fichier:ligne`. Les risques écartés sont listés à part, avec la raison.
5. **Prouver le fait au niveau 4** : un petit script ou un test qui appelle le vrai code. Sinon, il est marqué `unproven`.

`analyze-impact` sort trois listes : les risques confirmés, avec leur preuve ; les risques écartés ; et le test le moins cher qui attraperait le vrai bug. Ce test va dans la PR.

`ship` l'appelle en `medium` et `high`. `verify-pr` l'appelle aussi, sans voir le rapport du builder (section 5.7).

### 5.7 Couche 6 — Le juge indépendant : `verify-pr`

Anthropic le dit sans détour : « Out of the box, Claude is a poor QA agent ». Un vérificateur qu'on ne règle pas trouve les défauts, puis valide quand même. `verify-pr` est donc construit contre ce défaut.

**Qui il est** :
- un agent **frais**, qui ne voit ni le raisonnement ni le rapport de `analyze-impact` du builder. Il voit la tâche, `done_when`, le diff et la PR ;
- **sans droit d'écriture** : il ne corrige jamais, il constate ;
- **d'une autre famille de modèle** quand elle est disponible (GPT via Codex), parce que des agents d'une même famille se trompent ensemble (Anthropic, *multiagent*).

**Ce qu'il fait** : des **lanes**, chacune avec sa question.

| Lane | Question | Comment | Source |
|---|---|---|---|
| `replay` | la preuve du builder tient-elle ? | rejoue les commandes de la PR et compare les sorties | tstack |
| `live` | l'app fait-elle ce que dit `done_when` ? | pilote l'app réelle via `drive-<app>`, sur la base puis sur la tête, sans suivre le parcours du builder | harness design (l'évaluateur « interagit avec l'app vivante ») |
| `spec` | le code fait-il ce qui était demandé, tout ce qui était demandé, et rien de plus ? | compare le diff à la tâche et à `done_when` | Matt `code-review`, axe *Spec* |
| `standards` | le code respecte-t-il les standards du repo ? | `CODING_STANDARDS.md`, puis la base d'odeurs de code de Fowler | Matt `code-review`, axe *Standards* |
| `breakage` | qu'est-ce que ça casse ailleurs ? | lance `analyze-impact`, de son côté | pstack `blast-radius` |
| `adversarial` | des adversaires arrivent-ils à la casser ? | plusieurs agents reçoivent « Break this change », et seul ce qu'un run prouve survit | pstack `interrogate` |

**Ce qu'il rend** :
- un verdict **par axe** : *comportement* (`replay`, `live`, `breakage`, `adversarial`) et *code* (`spec`, `standards`). Un bon axe ne masque pas l'autre ;
- **FAIL** seulement avec une preuve : la commande, la sortie observée et la sortie attendue. Sans exécution, c'est une **NOTE** ;
- barème repris de tstack : un *blocker* ou un *should* donne FAIL ; un *nit* donne NOTE ;
- **PASS+NOTES vaut PASS**. Les notes restent dans le commentaire du verdict ; tu transformes en issue celles que tu veux (décision du 2026-11-19, pour ne pas inonder le tracker). La review ne fait pas grossir la PR ;
- le builder peut contester un FAIL avec des preuves. Si le désaccord persiste, la PR passe en `needs-human` avec les deux positions ;
- 2 FAIL au plus. Ensuite, `needs-human`.

Le verdict est un commentaire au format fixe sur la PR :

```text
verdict: PASS   sha=3f2a9c1 patch-id=8be04d7
behaviour: PASS (replay, live, breakage)   code: PASS (spec, standards)
- note : le même motif de double envoi existe dans « Dupliquer » → issue #57
```

**Comment on sait qu'il marche** : on mesure qu'il sait **échouer**.
- `evals/verdicts/` contient des **défauts semés** dans de vraies PR du cobaye, par type (logique, régression hors diff, spec incomplète, test tautologique, sécurité), et chaque **bug échappé** rejoué.
- Il est **calibré par des exemples** : des verdicts sur lesquels tu as tranché. Règle : un défaut constaté reste un FAIL, sauf si `done_when` l'exclut.
- Le chiffre suivi est le **taux de défauts attrapés**, jamais le taux de PASS. Un vérificateur qui ne dit jamais FAIL est un vérificateur cassé.

### 5.8 Proportionner au risque

Vérifier tout, tout le temps, coûte cher sans rien apprendre. Sous la frontière de ce que le modèle réussit seul, un vérificateur ne fait que confirmer (Ray Amjad ; Anthropic « harness design »). La classe de risque règle donc la profondeur. La table qui fait foi est dans `skills/constitution/references/proof.md`, section Risk classes. En bref :

- `low` (docs et tests, ou une trentaine de lignes dans une fonction, sans zone difficile) : cadrage court, pas de `analyze-impact`, lanes `replay`, `spec` et `standards` ;
- `medium` : la colonne complète, sans relecture de `done_when` avant le build ni lane `breakage`, sauf quand une zone difficile est touchée ;
- `high` : tout, y compris la relecture avant le build, un `analyze-impact` élargi à plusieurs sous-agents et la lane `adversarial`.

On n'allège une lane qu'à une condition : les défauts semés de `evals/verdicts/` montrent qu'elle n'attrape plus rien que les autres n'attrapent déjà.

### 5.9 Couche 7 — Chaque bug raté rend le système plus fort

Quand tu trouves un problème après coup, en review ou après le merge, tu le dis (ou tu poses le label `escaped` sur l'issue). Alors :

1. **`learn-from-mistakes`** trouve la couche qui aurait dû l'attraper, et pourquoi elle ne l'a pas fait :
   - le code permettait l'erreur → `add-guardrail` ;
   - la preuve ne couvrait pas ce chemin → la feature map de `drive-<app>` ;
   - le vérificateur l'a vu passer → un défaut semé de plus dans `evals/verdicts/` ;
   - un skill a mal guidé → une PR sur le skill, que tu approuves.
2. **`add-guardrail`** préfère, dans l'ordre : l'architecture, les types, un lint dont le message nomme le fix, un test, et la doc en dernier (Lauren Tan, pstack). Chaque nouveau check est prouvé sur l'erreur réelle qui l'a motivé.
3. **Règle de croissance** : un skill ou un check naît quand le même échec apparaît deux fois.

C'est la phrase de Lauren Tan, appliquée : « whenever you're correcting your agent, think about how you can make that a deterministic check instead of adding another line to your rules ».

## 6. La colonne

```text
frame ─► build ─► clean ─► prove ─► analyze-impact ─► open-pr ─► verify-pr ─► babysit-pr ─► PR prête ─► toi
  │        ▲                                              │          │
  │        └─────────── FAIL prouvé (≤ 2) ────────────────┘          └─ conflits, reviews, CI (≤ 5 rounds)
  └─► shape-spec, si « fini quand » n'est pas observable
```

| Étape | Passe à la suite quand | Budget | Sinon |
|---|---|---|---|
| `frame` | `done_when` est observable, rouge sur la base, et validé par ton « go » | — | `shape-spec`, ou une question |
| `build` | `done_when` est vert ; chaque obligation du playbook est tenue | 3 tentatives | `needs-human` |
| `clean` | deslop fait ; commentaires relus par un agent qui ne les a pas écrits ; lint, types et tests verts | — | retour à `build` |
| `prove` | `done_when` est au niveau 5 (ou 4 sans surface utilisateur), rejouable | compte dans `build` | retour à `build` |
| `analyze-impact` | le fait de sûreté est au niveau 4, ou marqué `unproven` | — | — |
| `open-pr` | la PR suit le format (section 6.2) | — | — |
| `verify-pr` | un verdict est posé sur le patch de tête | 2 FAIL | `needs-human` |
| `babysit-pr` | aucun conflit, threads résolus, CI verte, chaque fix reprouvé ; un nouveau patch repasse par `verify-pr` | 5 rounds | `needs-human` |

Une PR est **prête** quand il ne lui manque que ta décision. Elle porte alors le label `ready`. `needs-human` est un label, avec un résumé de ce qui bloque.

### 6.1 Règles

- **`build` choisit un playbook** selon la tâche : six playbooks repris de pstack (table dans `ship/references/frame.md`), tous finissent par une PR : `bug-fix`, `feature`, `refactoring`, `perf`, `visual-parity` et `bespoke` (dont expand → migrate → contract pour une migration large). Les trois playbooks pstack qui finissent par une réponse sont devenus les modes de `investigate` (décision du 2026-11-19 : ils ne partageaient aucune étape de `ship` au-delà du cadrage). Un playbook énonce des **obligations de preuve**, pas une recette, et cite les principes par leur id au lieu de les recopier.
- **`clean` garde le jardin propre.** Le prochain agent copiera ce qu'on laisse (Lauren Tan) : on retire le slop, et ce qui se répète part dans `add-guardrail`.
- **Le même builder porte la PR de `frame` à « prête »**, fixes de review compris, car il garde le contexte. C'est un écart assumé : Ray Amjad le mesure meilleur et 38 % moins cher sur ~10 PR, alors que Matt et pstack prennent un agent frais à chaque round. On tranche en comparant sur les PR du cobaye.
- **Une tâche, une PR étroite.** On empile une PR seulement sur une PR dont elle dépend. Après ton merge, tu lances `babysit-pr` sur la suivante pour la restacker.
- **La voie légère** : une PR `low` garde une preuve courte et saute `analyze-impact`.
- **Hors colonne** : les questions, diagnostics et prototypes (`investigate`), et le déploiement.

### 6.2 Le format de PR

Le corps est un briefing d'une minute, pas un cahier de labo (pstack `opening-a-pr`). En clair : Why, Done when, Coverage, Demo, Not verified, puis une ligne Risk avec la porte et une ligne Verdict. Proof, Breakage et Decisions sont repliés en dessous. Le format qui fait foi est `skills/constitution/references/pr-format.md`.

## 7. Tu lances chaque tâche

**Décision du 2026-11-19** : tu restes maître des tâches lancées. Rien ne démarre sans toi : pas de run de nuit, pas de file traitée seule, pas de PR planifiée.

- **Retirés du catalogue** : `autopilot` (une file d'issues traitée la nuit), `ketchup` (le compte rendu du matin) et `eval` (l'A/B des skills).
- **Devenus à la demande** : le mode `maintain` de `create-app-driver` et `ratchet`, qui tournaient planifiés.
- **Ce qui reste automatique** se passe à l'intérieur d'une tâche que tu as lancée : sous-agents, vérificateur, `babysit-pr` jusqu'à « prête ».
- **Une grosse spec** passe par le playbook `bespoke` : un seul builder, une série de PR ordonnées, chacune lancée dans la tâche que tu as donnée.

## 8. Modèles et harnais

| Rôle | Ce qu'il fait | Famille par défaut |
|---|---|---|
| builder (owner) | porte une PR de `frame` à « prête » | Claude, gamme haute |
| verifier | essaie de casser la PR, sans droit d'écriture | GPT, via Codex |

Sans autre famille disponible, le vérificateur reste un agent frais de la même famille. C'est moins fort ; les défauts semés de la calibration diront de combien.

Les skills nomment des **capacités**, jamais des outils. `constitution/references/harness.md` les traduit :

| Capacité | T3 Code | Claude Code seul | Codex |
|---|---|---|---|
| lancer un sous-agent d'une autre famille | `delegate_task` | à préciser | à préciser |
| garantir un contexte frais | sous-agent neuf | sous-agent neuf | à préciser |
| isoler un run | worktree | worktree | worktree |
| être réveillé par une PR | `watch_pull_request` | repli REST | idem |
| poser une question | `AskUserQuestion` | `AskUserQuestion` | `request_user_input` |
| bloquer le merge | hook du harnais | hook | à préciser |

## 9. Le format des skills et la méta-couche

### 9.1 Un nœud

Le frontmatter suit la spec Agent Skills. Les arêtes du graphe vivent dans `metadata`. Exemple pour `verify-pr` :

```yaml
---
name: verify-pr
description: "Tries to break a pull request's head patch and gives a verdict per axis, without editing code."
disable-model-invocation: true
metadata:
  kind: spine
  role: verifier
  calls: "repo:drive-<app>, analyze-impact"   # repo: = un skill du repo cible
  consumes: "pr, head-sha, done-when"
  produces: "verdict comment"
  budget: "2 FAIL"
  hypothesis: "An author model checks what it meant to build, not what it built."
---
```

Règles d'écriture :

- **Les descriptions ne nomment aucun autre skill.** Le graphe vit dans `metadata`.
- **Les skills ne nomment aucune source externe** (pstack, Matt, tstack, Anthropic…). Un agent pourrait aller lancer le skill d'origine et sortir du framework. La traçabilité vit dans `design/sources.md`, et la lint l'impose (règle P005).
- **Le routage se fait par chemin** (pstack) : un nœud interne n'est jamais choisi par le modèle sur sa description. `learn-from-mistakes` vérifie dans les transcripts que les nœuds attendus ont bien été lus.
- **Chaque étape a un critère de fin observable.**
- **Un `SKILL.md` vise moins de 800 mots.** Le détail va dans `references/`, le mécanique dans `scripts/`.
- **La prose suit `technical-writing` et `unslop` (pstack)** ; leur partie mécanique est dans le lint.
- **Les skills sont en anglais** ; la constitution impose de te répondre dans ta langue.
- **Écrits selon `writing-for-agents` (Matt)**, revus le 2026-11-19 : une étape tient en une action et son critère de fin, le détail va dans une référence pointée ; une description de skill lancé par toi est un résumé d'une ligne ; une idée répétée devient un mot-clé du glossaire (`run`, `red`) ; on énonce le comportement voulu, et l'interdiction seulement comme garde-fou dur.
- **Indépendants du fournisseur d'IA** (décidé le 2026-11-19). Le format suit la spécification Agent Skills (agentskills.io). Dans un repo cible, chaque skill vit dans `.agents/skills/`, et un harnais qui ne lit que son propre dossier reçoit un lien symbolique, jamais une copie. Les instructions vivent dans `AGENTS.md`. Les règles sont dans `skills/constitution/references/target-repo.md`. Les sources de ce framework restent dans `skills/` : c'est le dossier de distribution, pas un repo où l'on travaille.

### 9.2 Les scripts du framework

| Script | Étape | Échoue si |
|---|---|---|
| `tools/lint_skills.py` | 0 | champ manquant, étape sans critère, lien cassé, terme du glossaire à éviter, appel déclaré sans lien par chemin, lien vers un autre skill sans arête déclarée, source externe nommée dans un skill |
| `tools/check_refs.py` | 0 | lien ou ancre cassé, chemin entre backticks introuvable, nom de skill, de principe ou de playbook inconnu, ancien nom de skill |
| `tools/check.py` | 0 | lance les tests, `lint_skills.py` et `check_refs.py` : la commande unique, en local comme en CI |
| `tools/graph.py` | 4 | nœud orphelin, arête non déclarée, cycle sans budget |
| `tools/install.py` | 2 | copie chaque skill de `skills/` dans `~/.agents/skills/<nom>/`, et `constitution/` à côté, sans `SKILL.md`, pour que les liens `../constitution/` marchent sans qu'elle apparaisse dans les menus (la convention commune, lue par Codex, Cursor, Gemini CLI, Copilot) ; crée un lien par skill dans `~/.claude/skills/` pour Claude Code, qui ne lit pas `.agents/` ; écrit `agents/openai.yaml` avec `allow_implicit_invocation: false` pour Codex, l'équivalent de `disable-model-invocation` ; installe le hook anti-merge |

### 9.3 La méta-boucle

- **`learn-from-mistakes`** propose les changements de skill ; tu les approuves ligne par ligne. Pas d'`eval` A/B (retiré le 2026-11-19) : un changement de skill se juge sur les PR suivantes du cobaye.
- **Un skill cassé se répare dans sa propre PR**, jamais au milieu d'une tâche (pstack, guide 09).
- **Le glossaire** (`constitution/references/glossary.md`) est une table FR→EN avec les termes à éviter (Matt). Il définit : `done_when`, preuve, niveau de certitude, verdict, lane, prête, `needs-human`, classe de risque, porte (door), unité.

## 10. L'arborescence du framework

```text
software-ai-skills-framework/
├── knowledge/               base de connaissance
├── design/                  brainstorm, architecture, revue, archive/, puis decisions/ (ADR)
├── skills/
│   ├── constitution/        README.md (dossier partagé, pas un skill) et references/ : principles, proof, coverage, glossary, harness, pr-format, target-repo, parallel (arena, swarm), decision-log, statechart, languages/
│   ├── setup-repo/          SKILL.md, references/ : first-glossary, standards
│   ├── create-app-driver/   SKILL.md, references/ (template, drivers, feature map, maintain, formal)
│   ├── shape-spec/          SKILL.md, references/ : grill, domain, spec, map
│   ├── investigate/         SKILL.md, references/ : question, diagnosis, prototype
│   ├── add-guardrail/
│   ├── learn-from-mistakes/ SKILL.md, references/ : reviewers, synthesis, routes
│   ├── ship/                SKILL.md (frame, build, clean, prove, analyze-impact, open-pr, verdict, babysit-pr) ; references/design.md, clean.md et playbooks/ : bug-fix, feature, refactoring, perf, visual-parity, bespoke
│   ├── analyze-impact/  verify-pr/  babysit-pr/
│   └── …                    les autres, quand la règle de croissance les déclenche
├── tools/                   lint_skills.py et ses tests ; graph.py et install.py plus tard
├── evals/                   verdicts/ : défauts semés et bugs échappés, pour calibrer le vérificateur
└── .github/workflows/       CI du framework : lint et tests des scripts
```

## 11. Un exemple de bout en bout

`/ship le bouton Enregistrer crée parfois deux notes`

1. **frame** : l'agent reproduit d'abord le symptôme sur la base avec `drive-notes`, puis élimine les causes candidates. Seule survit celle-ci : un double clic envoie deux requêtes avant que le bouton se désactive. Il écrit : « Bug : Enregistrer crée parfois deux notes. Fini quand : quelle que soit la façon d'enregistrer, une seule note existe en base. Cas : double clic, Ctrl+S pendant l'enregistrement, enregistrement hors ligne, import. Je l'ai lancé sur la base : le double clic crée deux notes. Hors périmètre : Dupliquer. Classe : `medium`. Go ? » Tu réponds « go ».
2. **build** (playbook `bug-fix`) : le test rouge dans un premier commit, puis le fix. Le test passe.
3. **clean** : deslop ; un commentaire qui justifiait un contournement est retiré. Lint, types et tests verts.
4. **prove** : `drive-notes` lance l'app, double-clique sur la base puis sur la tête, et capture l'écran et la table `notes`. Niveau 5.
5. **analyze-impact** : le fix désactive le bouton pendant l'enregistrement. Le fait de sûreté : « le bouton est réactivé même quand l'enregistrement échoue ». Un script coupe le réseau, enregistre, et vérifie que le bouton revient. Niveau 4. Risque écarté : le raccourci Ctrl+S passe par le même handler (`editor.ts:88`).
6. **open-pr** : « Empêcher le double enregistrement d'une note », au format de la section 6.2.
7. **verify-pr** : un agent GPT frais, sans droit d'écriture.
   - `replay` : la preuve tient.
   - `live` : il pilote l'app lui-même et tente un triple clic et Ctrl+S pendant l'enregistrement.
   - `breakage` : il retrouve le même fait de sûreté, et le cas Ctrl+S.
   - Verdict : comportement PASS, code PASS. Une note : le même motif existe dans « Dupliquer ». Elle reste dans le commentaire du verdict, et tu en fais une issue si tu veux.
8. **babysit-pr** : un bot signale un cas limite hors périmètre ; il devient l'issue #58. CI verte. Label `ready`.

**Ton temps** : dire « go », puis lire Why, Coverage, la démo, Not verified et la ligne Verdict, et merger. Environ deux minutes.

**Une semaine plus tard**, tu trouves que l'import d'une note crée aussi un doublon. Tu poses `escaped` sur l'issue. `learn-from-mistakes` conclut que la feature map ne listait pas l'import comme entrée de création de note : la fiche est complétée, et un défaut semé « doublon par l'import » rejoint `evals/verdicts/`.

## 12. Hors périmètre

- **Le merge par l'agent**, sous toutes ses formes : décidé le 2026-11-18.
- **Une gate de CI propre au framework**, et le dossier `.trust/` : la CI existante du repo et ta lecture de la PR suffisent.
- **Serveur, base de données, file de messages** : GitHub et le harnais suffisent.
- **Personas** (testeur, PM, designer) : ils ne marchent pas « right now » (Ray Amjad).
- **Des essaims qui discutent** : la coordination vient du graphe du travail (Anthropic, *multiagent*).
- **Le déploiement** : le framework s'arrête à la PR prête.
- **Les tâches lancées sans toi** : `autopilot`, `ketchup`, les runs planifiés ; et `eval` : décidé le 2026-11-19.

## 13. Décisions prises et hypothèses restantes

| Question | Statut | Choix |
|---|---|---|
| Qui merge | **décidé** (2026-11-18) | toi, toujours, sans exception |
| `.trust/`, gate, échelle N0–N5 | **retirés** (2026-11-18) | remplacés par la vérification de la section 5 et par le hook qui bloque le merge |
| Compte GitHub séparé pour l'agent | **sans objet** | il servait à l'approbation en N3 ; l'agent travaille sous ton nom, et le hook l'empêche de merger |
| Repo cobaye | **ouvert, bloquant** | sans lui, ni `drive-<app>`, ni preuve, ni défaut semé. Une lib ou une CLI se prouve par des commandes plutôt que par des captures |
| Autre famille de modèle | hypothèse | GPT via T3 Code. Sans elle, vérificateur de la même famille, mesuré |
| Harnais | hypothèse | T3 Code, avec Claude Code |
| Le « go » avant le code | **décidé** (2026-11-19) | à chaque tâche, quel que soit le risque : rien ne démarre sans toi (Matt ; pstack dit le contraire) |
| Les principes dans la réponse | **décidé** (2026-11-19) | plus dans la réponse ; l'id du principe va avec le choix qu'il a changé, dans Decisions ou le journal |
| Le suivi des issues | **décidé** (2026-11-19) | indépendant de l'outil, comme chez Matt : les skills nomment une opération (« publier dans le tracker », « poser le label `escaped` »), et `docs/agents/issue-tracker.md`, écrit par `setup-repo` depuis un modèle (GitHub, GitLab, markdown local, ou un autre outil comme Linear ou Jira décrit par toi), dit comment la faire. Les PR et la CI restent sur GitHub pour l'instant |
| Les tâches planifiées | **décidé** (2026-11-19) | aucune : aucun skill ne tourne par cron ; la fraîcheur de la feature map est signalée par `frame` (commit « Last driven ») |
| Les notes du vérificateur | **décidé** (2026-11-19) | listées dans le commentaire du verdict ; une issue seulement si tu la demandes |

## 14. La feuille de route

L'ordre suit Lauren Tan : le code, puis la vérification, puis l'automatisation. Chaque étape se termine sur une preuve, pas sur une date.

| Étape | On construit | Preuve de sortie |
|---|---|---|
| 0 · Fondations | `constitution` (standard de preuve, échelle de certitude, glossaire), `lint_skills.py` | lint vert en CI sur `constitution` |
| 1 · Le repo sait se vérifier | `create-app-driver`, `add-guardrail` (`audit`, puis une correction) | `drive-<app>` lance, pilote et prouve chaque fonctionnalité de la feature map, de bout en bout ; fondations du cobaye mesurées ; au moins une classe d'erreurs de l'historique convertie en check prouvé |
| 2 · Une PR prouvée | `ship` (`bug-fix`, `feature`), `analyze-impact`, `babysit-pr`, le hook anti-merge, `install.py` pour Claude Code | 10 vraies PR sur le cobaye, que tu as mergées ; preuves rejouées par toi ; `done_when` rouge sur la base dans 10 cas sur 10 ; tes corrections notées. Ces PR forment `evals/e2e/` |
| 3 · Un juge qui sait dire non | `verify-pr` (lanes, calibrage), `evals/verdicts/` | des défauts semés de chaque type ; le vérificateur en attrape au moins 80 % (seuil de départ) ; aucun FAIL sans exécution |
| 4 · Le système apprend | `learn-from-mistakes` (v0 écrit), `ratchet` à la demande, `graph.py` | chaque bug échappé a produit un check ou un défaut semé, après ton accord |

**Premier jalon utile** : l'étape 2. **L'étape 1 vient avant `ship`**, parce qu'un agent qui ne peut pas piloter l'app ne peut rien prouver.

## 15. Pourquoi cette architecture

| Alternative | Ce qu'elle fait bien | Ce qu'on en garde |
|---|---|---|
| pstack (`poteto-mode`) | `create-verification-skill`, `blast-radius`, `interrogate`, la règle de blocage, le patch-id, `learn-from-mistakes` | presque toute notre couche de vérification ; pas son lien à Cursor |
| Matt Pocock | la boucle de feedback d'abord, le TDD par seams, la review sur deux axes, les petits skills, l'humain qui merge | la couche 2, les lanes `spec` et `standards`, le glossaire, le dispatch par script |
| tstack | le standard de preuve, le barème, « pas de preuve, pas de confiance » | le format de PR et le barème du verdict |
| Lauren Tan | la pyramide inversée, la feature map, l'ordre code → vérification → automatisation | l'ordre de la feuille de route, `add-guardrail`, `ratchet` |
| Anthropic | l'évaluateur séparé et réglé pour être sceptique, qui pilote l'app vivante | le vérificateur, la lane `live`, le calibrage |

**Notre apport** : assembler ces couches en une colonne unique, où chaque affirmation porte son niveau de certitude, et où chaque bug raté devient un check ou un défaut semé.

**Les risques** :

- **La vérification coûte des tokens.** On la proportionne au risque, et on n'allège une lane que sur preuve qu'elle n'attrape plus rien d'unique.
- **`drive-<app>` peut être difficile à écrire** selon la stack du cobaye (app mobile, service avec dépendances externes). C'est pour ça qu'il passe en premier.
- **Les seuils sont des valeurs de départ** (80 % de défauts attrapés, 10 PR). On les recalibre sur nos données.

## 16. Ce qu'il faut pour avancer

1. **Le repo cobaye** : quel projet réel, et quelle stack ? Il décide de la forme de `drive-<app>`.
2. Ensuite, l'étape 0 : `constitution` et `lint_skills.py`.
