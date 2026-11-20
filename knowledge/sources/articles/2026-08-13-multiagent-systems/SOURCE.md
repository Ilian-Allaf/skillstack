# Source — Patterns and problems in emerging multiagent systems

## Fiche

| Champ | Valeur |
|---|---|
| Type | Article de recherche |
| Titre | Patterns and problems in emerging multiagent systems |
| Auteur | Frontier Red Team, Anthropic (auteure correspondante : Carolyn Zou) |
| URL | <https://www.anthropic.com/research/multiagent-systems> |
| Publié le | 2026-08-13 |
| Temps de lecture | ~18 min (estimé, non indiqué par la page) |
| Catégorie | Research — Agents, Alignment, Cybersecurity, Coding, Measurement and mitigation |
| Contenu hors-ligne | [`content.md`](content.md) — version nettoyée, anglais original |
| Diagrammes | [`assets/`](assets) — 7 PNG (graphiques de résultats) |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

Une série d'expériences sur des essaims d'agents (Claude de Sonnet 4.6 à Mythos 5) qui coopèrent ou s'affrontent : chasse aux vulnérabilités, construction d'un jeu à plusieurs dizaines d'agents avec PR et merges, jeux économiques, détection de mensonges, « hidden profile », et une « guerre de territoire » entre trois agents aux objectifs incompatibles. L'article en tire quatre familles de défaillances : coordination, conformité, épistémique, buts incompatibles.

## Pourquoi cette source

Les autres sources décrivent comment **construire** un système d'agents. Celle-ci mesure comment il **échoue** quand plusieurs agents partagent un repo. Elle donne des chiffres directement liés à notre objectif : fraction de PR mergées, partage de code, conflits abandonnés, sabotage entre agents. C'est la meilleure preuve externe pour décider entre « essaim qui discute » et « graphe de travail partitionné » (design/02, section 8.2 et hors périmètre).

## Fiabilité de la source

Recherche officielle Anthropic (Frontier Red Team), avec protocoles et tailles d'échantillon (n=120 ou n=400 épisodes selon l'expérience). Ce sont des environnements expérimentaux, souvent avec des agents tous issus du même modèle et sans supervision ; les auteurs notent eux-mêmes que des agents hétérogènes en conditions réelles varieraient davantage. Les noms de modèles et les résultats sont datés d'août 2026.

## Structure de l'article

1. Introduction : pourquoi les interactions agent-agent vont exploser.
2. Measuring coordination : essaim vs agents parallèles (vulnérabilités) ; essaims qui construisent un jeu (PR mergées, partage de code).
3. Failures from conformity : agents à faible variance, ressources inondées, collusion.
4. Epistemic failures : détection de mensonges, tâches « hidden profile ».
5. Incompatible goals : la guerre de territoire de la migration de backend.
6. Conclusion.

## Fichiers

- [`content.md`](content.md) — article complet, navigation retirée.
- [`assets/01-vuln-swarm-vs-parallel.png`](assets/01-vuln-swarm-vs-parallel.png) — vulnérabilités trouvées, essaim vs parallèle.
- [`assets/02-merge-fraction-code-sharing.png`](assets/02-merge-fraction-code-sharing.png) — fraction de PR mergées et partage de code selon la taille de l'essaim.
- [`assets/03-pr-progress.png`](assets/03-pr-progress.png) — PR ouvertes vs mergées sur 12 h, par modèle.
- [`assets/04-lie-detection.png`](assets/04-lie-detection.png) — précision face à une source menteuse.
- [`assets/05-hidden-profile.png`](assets/05-hidden-profile.png) — précision de groupe sur les tâches « hidden profile ».
- [`assets/06-turf-war-outcomes.png`](assets/06-turf-war-outcomes.png) — issue des guerres de territoire (force, passivité, trêve).
- [`assets/07-turf-war-resolution-time.png`](assets/07-turf-war-resolution-time.png) — temps et mode de résolution.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
