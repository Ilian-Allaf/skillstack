# Glossaire

Vocabulaire partagé du corpus et du blueprint. Les termes anglais sont conservés quand ils sont utilisés tels quels dans les skills.

---

## Skills et documents

| Terme | Définition | Source |
|---|---|---|
| **Skill** | Document exécutable par un agent, chargé à la demande, qui encode un déclencheur, des étapes ou une référence, et un critère de complétion. | Corpus |
| **Skill graph** | Ensemble de skills reliés par des arêtes typées (blocage, vérification, réparation, escalade). | Blueprint |
| **Router** | Skill ou composant qui reçoit l'intention et sélectionne le skill, le playbook ou la topologie appropriée. | Matt, pstack |
| **Playbook** | Procédure situationnelle longue, séparée du routeur, dont les étapes sont copiées dans la todo. | pstack |
| **Principle** | Skill de référence court qui encode une règle d'ingénierie transversale. | pstack |
| **Template** | Squelette de sortie (PR, ticket, spec, preuve), pas un skill. | Blueprint |
| **Context pointer** | Référence hors contexte qui encode la condition pour atteindre le matériel. | Matt |
| **Progressive disclosure** | Fait de pousser une référence hors du fichier principal, derrière un pointeur, pour garder le corps lisible. | Matt |
| **Leading word** | Token pré-entraîné qui ancre un comportement (_tracer bullet_, _frontier_, _red_). | Matt |
| **Completion criterion** | Condition vérifiable qui dit qu'une étape est finie. | Matt |
| **No-op** | Instruction que le modèle suit déjà par défaut ; elle coûte du contexte sans changer le comportement. | Matt |
| **Model-invoked** | Skill dont la description est chargée en permanence et qui peut être déclenché par l'agent. | Matt |
| **User-invoked** | Skill sans description chargée, invocable uniquement par l'humain (`disable-model-invocation: true`). | Matt |
| **Context load** | Coût en contexte d'un matériel toujours chargé. | Matt |
| **Cognitive load** | Coût humain de savoir quels documents existent et quand les utiliser. | Matt |

---

## Travail et planification

| Terme | Définition | Source |
|---|---|---|
| **Task** | Unité de travail durable, indépendante d'un run. | Anthropic, blueprint |
| **Run** | Une exécution d'un skill ou d'une tâche, d'un événement à sa fin. | Anthropic |
| **Session** | Transcript des messages et appels d'outils ; peut couvrir plusieurs runs. | Anthropic |
| **Trigger** | Événement qui démarre un run : message, webhook, timer, changement de tracker. | Anthropic, Matt |
| **Ticket** | Unité de travail publiée dans un tracker, avec un comportement attendu et des critères d'acceptation. | Matt |
| **Tracer bullet** | Tranche verticale complète qui traverse toutes les couches et est demoable seule. | Matt |
| **Frontier** | Ensemble des tickets dont tous les bloqueurs sont terminés et qui peuvent démarrer. | Matt |
| **Blocking edge** | Dépendance d'un ticket vers un autre : le second doit finir avant le premier. | Matt |
| **DAG** | Graphe orienté acyclique de tickets ou de skills. | Matt, blueprint |
| **Wide refactor** | Changement mécanique dont la blast radius traverse tout le codebase ; séquencé en expand → migrate → contract. | Matt |
| **Spec** | Description du comportement attendu et des critères d'acceptation. | Matt |
| **Handoff** | Artefact portable qui permet à un autre agent de reprendre le travail. | Matt, pstack |
| **Session pickup** | Reprise d'un travail en cours à partir d'un transcript, d'une branche ou d'une URL. | pstack |
| **Worktree** | Checkout git isolé, utilisé pour qu'un agent travaille sans marcher sur un autre. | pstack, Matt |
| **Integration branch** | Branche qui agrège les travaux de plusieurs tickets avant la revue finale. | Matt |

---

## Topologies

| Terme | Définition | Source |
|---|---|---|
| **Pipeline** | Séquence de phases avec des artefacts intermédiaires. | Matt |
| **Fan-out** | Distribution de sous-tâches indépendantes à N workers, puis agrégation. | Ray |
| **Swarm** | N workers qui couvrent des tranches ou des races, avec un objectif de couverture. | pstack, Ray |
| **Arena** | N tentatives sur le même brief, puis sélection d'une base et greffe des meilleures parties. | pstack |
| **Pair** | Deux agents qui échangent, souvent générateur et juge. | Ray, tstack |
| **Council** | Panel de trois modèles de fournisseurs différents, avec scores et rounds. | tstack |
| **Manager thread** | Thread coordinateur qui délègue à des sessions isolées. | Ray |
| **Long-lived lead** | Agent responsable d'un domaine pendant des semaines/mois, avec des workers. | Ray |
| **Coupling** | Degré auquel deux unités de travail partagent des artefacts ou de l'état. | Ray, blueprint |
| **Independence** | Propriété d'unités qui peuvent avancer sans se connaître. | Ray |

---

## Qualité et vérification

| Terme | Définition | Source |
|---|---|---|
| **Deterministic check** | Vérification reproductible : type, lint, test, compilation, analyse de dépendances. | Lauren |
| **Proof** | Évidence observée dans la session : sortie, reproduction, capture, test. | tstack |
| **Evidence** | Artefact qui atteste qu'un critère est rempli. | Blueprint |
| **Gate** | Condition binaire qui autorise ou bloque une transition. | Blueprint |
| **Merge gate** | Liste de conditions observables avant un merge. | tstack |
| **Verification at the capability edge** | Vérifier là où le modèle est à la limite de ses capacités, pas ce qu'il réussit toujours. | Ray |
| **Feature map** | Carte des fonctionnalités du point de vue utilisateur, utilisée pour la vérification runtime. | Lauren |
| **Formal verification** | Preuve mathématique d'une propriété (TLA+, Lean). | Lauren |
| **Property-based testing** | Génération d'entrées/interactions pour vérifier une propriété. | Lauren |
| **Benchmark checklist** | Vetting d'un chiffre avant de le publier : limite, tuning, erreurs, répétitions. | pstack |
| **Eval** | Test comportemental d'un skill ou d'un prompt, avec un protocole et un juge. | pstack |
| **Blinding** | Fait de cacher au candidat et/ou au juge l'identité des variantes. | pstack |
| **False positive** | Finding de review qui n'est pas un vrai problème. | tstack, pstack |
| **Escaped defect** | Bug trouvé après le merge. | Blueprint |

---

## Autonomie et runtime

| Terme | Définition | Source |
|---|---|---|
| **Autonomy grant** | Autorisation explicite et bornée donnée par l'utilisateur pour une tâche (`full send`). | tstack |
| **Autonomy level** | Niveau 0–3 : lecture, écriture locale, action externe, action irréversible. | Blueprint |
| **Harness** | Environnement qui exécute les skills : modèle, outils, permissions, sessions. | Ray, pstack |
| **Event inbox** | Store durable des événements prêts à être traités par un worker. | Anthropic |
| **Timer** | Échéance (follow-up) ou récurrence (schedule) qui produit un événement. | Anthropic |
| **Memory** | Store durable des instructions, notes, messages et progressions. | Anthropic |
| **Deferred tool call** | Appel d'outil suspendu qui attend une entrée humaine et reprend via un événement. | Anthropic |
| **Outbox** | Store des messages/artefacts sortants, avec un dispatcher. | Anthropic |
| **Always-on agent** | Agent stateful et proactif qui se réveille sur événement, travaille, persiste, puis se rendort. | Anthropic |
| **Compaction** | Compression du transcript ancien en résumé pour libérer du contexte. | Anthropic, Ray |
| **Idempotent** | Opération qui converge vers le même état, même relancée ou partiellement exécutée. | pstack |
| **Dreaming** | Passe qui relit les sessions passées pour curer la mémoire. | Anthropic |
| **Credential proxy** | Proxy hors de l'environnement de l'agent qui injecte les credentials dans les requêtes. | Anthropic |
| **Auto mode** | Mode où des classificateurs bloquent les actions à risque et laissent passer les autres. | Anthropic |

---

## Méta

| Terme | Définition | Source |
|---|---|---|
| **Retro** | Rétrospective qui transforme les erreurs d'une session en améliorations d'environnement. | Matt |
| **Correct** | Skill qui mine les corrections répétées et les encode à la plus haute couche qui marche. | pstack |
| **Reflect** | Skill qui capture la recette d'une tâche longue sous forme d'édition de skill. | pstack |
| **Prune** | Suppression des skills, règles ou étapes devenues obsolètes. | Blueprint |
| **Hypothesis of capability** | Limite de modèle qu'un skill encode ; elle doit être datée et réévaluée. | Ray, blueprint |
| **Meta-improvement** | Boucle qui améliore les skills eux-mêmes, pas seulement le code. | pstack, Matt |

---

## Notes de traduction

- **Skill** n'est pas traduit : « compétence » est trop large et ne correspond pas à l'objet technique.
- **Run** n'est pas traduit : « exécution » est utilisé quand le contexte est clair.
- **Gate** est parfois traduit par « porte » ou « seuil », mais le terme anglais reste dominant dans le corpus.
- **Proof** est traduit par « preuve » ; **evidence** par « évidence » ou « artefact de preuve ».
- **Harness** est parfois traduit par « harnais » ; le terme anglais est conservé dans les documents techniques.
