# Source — Building always-on agents

## Fiche

| Champ | Valeur |
|---|---|
| Type | Article d'ingénierie |
| Titre | Building always-on agents |
| Auteur | William Hu (Anthropic) |
| URL | <https://claude.com/fr/resources/articles/building-always-on-agents> |
| Publié le | 2026-11-13 |
| Temps de lecture | 14 min |
| Catégorie | Best practices, Claude Platform |
| Contenu hors-ligne | [`content.md`](content.md) — version nettoyée, anglais original |
| Diagrammes | [`assets/`](assets) — 4 PNG, 3 GIF |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

L'architecture autour de la boucle d'un agent « always-on » : un agent qui dort la plupart du temps, se réveille sur événement, travaille dans une session, persiste ce qu'il a appris, puis se rendort. L'article définit cinq primitives — event inbox, timers, memory, permissions, outbox — et montre comment elles forment un cycle.

## Pourquoi cette source

Les trois autres sources parlent de **qualité** et de **coordination**. Celle-ci parle de **durabilité** : comment un système d'agents survit aux crashes, aux sessions, aux approbations humaines et au temps. C'est la couche qui manque à la plupart des frameworks de skills, qui supposent implicitement une session unique et un humain présent.

## Fiabilité de la source

Article officiel Anthropic, écrit par un ingénieur produit. Les primitives sont présentées comme des recommandations d'architecture, pas comme des spécifications exhaustives. Les noms de modèles et les chiffres de coût sont datés de novembre 2026.

## Structure de l'article

1. Le cycle derrière l'agent always-on.
2. Les cinq primitives :
   - event inbox ;
   - timers ;
   - memory (avec la gestion du contexte) ;
   - permissions ;
   - outbox.
3. Comment tout s'assemble.
4. Remerciements.

## Fichiers

- [`content.md`](content.md) — article complet, navigation retirée.
- [`assets/01-run-cycle.gif`](assets/01-run-cycle.gif) — timeline d'un run.
- [`assets/02-event-inbox.png`](assets/02-event-inbox.png) — inbox.
- [`assets/03-timers.png`](assets/03-timers.png) — timers et scheduler.
- [`assets/04-memory-layout.png`](assets/04-memory-layout.png) — arborescence mémoire.
- [`assets/05-context-window.gif`](assets/05-context-window.gif) — contexte et compaction.
- [`assets/06-outbox.png`](assets/06-outbox.png) — outbox.
- [`assets/07-primitives-cycle.gif`](assets/07-primitives-cycle.gif) — cycle complet.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
