# Source — `tstack`

## Fiche

| Champ | Valeur |
|---|---|
| Type | Dépôt de skills |
| Titre | tstack |
| Auteur | Theo Browne (t3dotgg) |
| URL | <https://github.com/t3dotgg/tstack> |
| Révision importée | `11e37a74d0a6868c121cd0910ab2b3bd9873b92a` |
| Date de révision | 2026-11-11 |
| Importé le | 2026-11-16 |
| Licence | MIT — Copyright (c) 2026 Theo Browne |
| Snapshot local | [`repo/`](repo) |
| Catalogue | [`catalog.json`](catalog.json) · [`SKILLS-INDEX.md`](SKILLS-INDEX.md) |
| Skills | 9 |

## Pourquoi cette source

tstack est le plus petit des trois corpus, et le plus **vertical** : il couvre un seul cycle de vie, celui de la pull request, de la modification au merge. Il est intéressant pour trois raisons :

1. ses **dépendances entre skills sont explicites** dans le README ;
2. il définit un **contrat d'autonomie** précis (`full-send`) ;
3. il traite la **preuve** et la **merge gate** comme des objets de premier ordre.

C'est un bon contrepoint aux corpus plus larges : au lieu d'un graphe de 60 skills, un graphe de 9 skills très liés.

## Ce qui a été importé

Le snapshot complet du dépôt, moins `.git` :

```text
repo/
├── skills/
│   ├── full-send/
│   ├── full-stop/
│   ├── council/
│   ├── sol-loop/
│   ├── file-pr/
│   ├── takeover/
│   ├── babysit-pr/
│   ├── modernize/
│   └── leaving-pr-comments/
├── README.md
└── LICENSE
```

## Architecture observée

### 1. Un graphe de dépendances déclaré

Le README documente les appels entre skills :

```text
full-send    → sol-loop, file-pr, babysit-pr
full-stop    → full-send
takeover     → modernize, file-pr, babysit-pr, leaving-pr-comments
file-pr      → leaving-pr-comments
babysit-pr   → leaving-pr-comments
modernize    → leaving-pr-comments
```

C'est une **hiérarchie d'orchestration** : un skill de haut niveau (`full-send`) compose des skills de plus bas niveau. Les feuilles (`leaving-pr-comments`) sont des formatteurs réutilisables.

### 2. Un contrat d'autonomie explicite

`full-send` est un **grant** : l'utilisateur dit « full send », et le skill énumère ce que cela autorise :

- merger une PR quand la merge gate passe ;
- force-push la branche de la PR avec `--force-with-lease` après rebase ;
- utiliser les méthodes de test nécessaires sans demander.

Le grant est **borné** : il ne couvre pas les changements en production, la suppression de données, le force-push d'autres branches, ni les approbations du harnais. C'est un modèle de délégation réversible vs irréversible.

### 3. La preuve comme condition de sortie

`full-send` définit « Proof » comme une évidence observée dans la session :

- reproduire l'échec, appliquer le fix, revoir la reproduction passer ;
- exécuter les checks de la CI ;
- ajouter un test ciblé qui échoue sans le fix ;
- pour l'UI, lancer l'app et regarder le changement.

« When you cannot find a way to prove a change, you do not have full confidence. Ask the user. » La preuve n'est pas un rapport, c'est une observation.

### 4. La merge gate

La gate énumère les conditions exactes :

- la preuve couvre chaque changement du diff ;
- les checks requis sont verts ;
- les review bots ont fini, chaque finding est corrigé ou rejeté avec une raison écrite ;
- aucune review humaine ne demande encore un changement ;
- la branche est à jour et mergeable.

C'est une **condition d'arrêt vérifiable**, pas une sensation de fin.

### 5. Le conseil multi-fournisseurs

`council` fait reviewer par trois modèles forts de trois fournisseurs différents, en parallèle, avec un score sur 10 et des rounds jusqu'à accord. Le skill insiste sur le fait de **ne pas attendre passivement** : dès qu'un résultat arrive, vérifier les findings contre le code et commencer à corriger pendant que les autres tournent.

### 6. Le watcher comme primitive d'autonomie

`full-send` exige de rester actif jusqu'au merge. Si des checks ou des bots sont en attente, il faut un watcher (`watch_pull_request` dans T3 Code) pour être réveillé. Sinon le travail s'arrête silencieusement. C'est un détail d'implémentation qui a des conséquences directes pour un orchestrateur durable.

## Skills notables

| Skill | Rôle | Pourquoi le lire |
|---|---|---|
| `full-send` | Autonomie | Contrat complet : grant, proof, merge gate, escalation |
| `full-stop` | Autonomie | Variante qui s'arrête avant le merge — bonne illustration des niveaux d'autonomie |
| `council` | Review | Panel multi-fournisseurs, score, rounds, gestion de l'asynchrone |
| `sol-loop` | Review | Boucle builder/reviewer jusqu'à accord |
| `file-pr` | Livraison | PR courte qui commence par le problème, pas par l'inventaire des changements |
| `takeover` | Reprise | Reprend une PR, une branche ou un thread d'agent en conservant le crédit |
| `babysit-pr` | Livraison | Surveille CI et bots, corrige les vrais findings |
| `modernize` | Maintenance | Rebase une vieille PR et décide si elle doit encore exister |
| `leaving-pr-comments` | Format | Formate les commentaires postés au nom de l'utilisateur |

## Conventions à retenir

- Dépendances inter-skills déclarées dans le README, pas seulement implicites.
- Un skill de haut niveau peut être un **contrat d'autonomie** complet.
- La preuve et la merge gate sont des sections nommées, pas des intentions.
- Les skills de livraison sont séparés : file, babysit, modernize, comment.
- Un formatteur de commentaires réutilisable comme feuille du graphe.
- Les triggers sont des expressions naturelles (« full send », « council »).
- Tous les skills sont model-invoked : les descriptions portent les phrases de déclenchement.

## Limites et angles morts

- Pas de couche de planification ou de spécification.
- Pas de skills de design, de refactoring ou de debug profond.
- Très dépendant de GitHub CLI, de Python et d'un harnais capable de faire tourner des modèles de plusieurs fournisseurs.
- Le corpus suppose un contexte de PR et de CI ; il ne couvre pas la découverte du besoin.
- Peu de méta-amélioration : pas d'équivalent à `reflect`, `correct` ou `eval`.

## Licence et attribution

MIT. Le texte original et la licence sont conservés dans [`repo/LICENSE`](repo/LICENSE). Toute réutilisation doit conserver l'attribution à Theo Browne.
