# Source — Building agents: When to fold subagents into your main agent loop

## Fiche

| Champ | Valeur |
|---|---|
| Type | Article de bonnes pratiques (Applied AI) |
| Titre | Building agents: When to fold subagents into your main agent loop |
| Auteur | Diane Sarkis (Anthropic) |
| URL | <https://claude.com/fr/resources/articles/building-agents-when-to-fold-subagents-into-your-main-agent-loop> |
| Publié le | 2026-10-22 |
| Temps de lecture | 18 min |
| Catégorie | Best practices, Perspectives, Claude Platform |
| Contenu hors-ligne | [`content.md`](content.md) — version nettoyée, anglais original |
| Diagrammes | [`assets/`](assets) — 1 PNG, 2 GIF |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

Quand replier des sous-agents (routeurs, planificateurs, spécialistes de domaine) dans la boucle principale d'un agent unique, qui charge skills et outils par divulgation progressive. L'article donne les trois cas où un sous-agent reste justifié, le design cible d'une boucle unique, et une méthode de migration pas à pas pilotée par des evals.

## Pourquoi cette source

Notre architecture (design/02) repose sur un builder unique qui porte une PR, un vérificateur séparé et un orchestrateur d'une dizaine de workers. Cet article est l'argument le plus direct d'Anthropic sur **où couper** entre agents : il valide le découpage par contexte (vérification boîte noire, travail parallèle indépendant) et attaque le découpage par type de problème. C'est un test de nos frontières.

## Fiabilité de la source

Article officiel Anthropic, issu de l'équipe Applied AI, fondé sur des déploiements en entreprise. Les chiffres (latence ~2x, 30-50 outils, prompt Claude Code réduit de plus de 80 %) sont des retours de terrain non détaillés. Le contexte est surtout celui d'agents conversationnels face au client, pas d'agents de code autonomes. Il promeut aussi des outils maison (migration kit, `/claude-api`, `/skill-doctor`).

## Structure de l'article

1. Introduction : quand garder des sous-agents (trois conditions), loi de Conway.
2. Les modes d'échec des grandes organisations.
3. La boucle unique avec divulgation progressive (trois raisons).
4. Comment replier les sous-agents :
   - evals de complétion de tâche ;
   - réduction progressive ;
   - fusion d'agents de domaine ;
   - sous-agents appelés comme outils ;
   - repli via skills et outils.
5. Plusieurs équipes, un seul agent : outils MCP, skills, bases de connaissance.
6. Outils pour accélérer le travail.

## Fichiers

- [`content.md`](content.md) — article complet, navigation retirée.
- [`assets/01-subagent-design.gif`](assets/01-subagent-design.gif) — design à sous-agents.
- [`assets/02-subagents-split-by-problem.png`](assets/02-subagents-split-by-problem.png) — découpage par problème vs par contexte.
- [`assets/03-folding-in-subagents.gif`](assets/03-folding-in-subagents.gif) — repli des sous-agents dans la boucle.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
