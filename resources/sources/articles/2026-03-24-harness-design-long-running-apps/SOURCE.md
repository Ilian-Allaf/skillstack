# Source — Harness design for long-running application development

## Fiche

| Champ | Valeur |
|---|---|
| Type | Article d'ingénierie (retour d'expérience) |
| Titre | Harness design for long-running application development |
| Auteur | Prithvi Rajasekaran (Anthropic Labs) |
| URL | <https://www.anthropic.com/research/harness-design-long-running-apps> |
| Publié le | 2026-03-24 (modifié le 2026-10-18) |
| Temps de lecture | non indiqué (~5 300 mots, ~22 min) |
| Catégorie | Engineering — Agents, Coding, Context engineering |
| Contenu hors-ligne | [`content.md`](content.md) — version nettoyée, anglais original |
| Diagrammes | [`assets/`](assets) — 8 PNG (captures d'écran ; pas de schéma d'architecture dans l'article) |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

Comment un harnais multi-agents fait produire à Claude des applications complètes en plusieurs heures, sans humain. L'auteur part d'une boucle **générateur / évaluateur** inspirée des GAN (d'abord sur le design frontend, avec des critères notables), puis passe à une architecture **planner / generator / evaluator** avec des **contrats de sprint** négociés et un QA qui clique dans l'app via Playwright. Il chiffre le coût (solo 20 min / 9 $ contre harnais 6 h / 200 $), puis **simplifie** le harnais quand Opus 4.6 arrive, composant par composant.

## Pourquoi cette source

C'est la source la plus directe sur trois questions ouvertes de `design/02` : la **séparation auteur / juge** (invariant 3), la **gestion du contexte** sur des runs longs (reset vs compaction, même builder de bout en bout), et le **coût réel** d'un évaluateur. Elle apporte aussi une règle de maintenance : chaque composant d'un harnais encode une hypothèse sur ce que le modèle ne sait pas faire, et doit être re-testé à chaque nouveau modèle — exactement le champ `hypothesis` et le mode `prune` d'`eval`.

## Fiabilité de la source

Article officiel Anthropic, écrit par un ingénieur de Labs, à partir de ses propres expériences. Résultats **qualitatifs et anecdotiques** : deux applications principales (game maker, DAW), pas de benchmark, pas de répétitions statistiques. Les chiffres de coût et de durée sont des runs uniques. Les modèles cités (Sonnet 4.5, Opus 4.5, Opus 4.6) datent du premier semestre 2026 ; les conclusions sur le « context anxiety » sont explicitement liées à un modèle.

## Structure de l'article

1. Introduction : deux problèmes (design frontend, apps complètes sans humain).
2. Pourquoi les implémentations naïves échouent : perte de cohérence / context anxiety, auto-évaluation complaisante.
3. Frontend design : rendre la qualité subjective notable (4 critères, évaluateur calibré, Playwright).
4. Passage au full-stack :
   - l'architecture planner / generator / evaluator, contrats de sprint ;
   - exécution du harnais (game maker, solo vs harnais) ;
   - itération sur le harnais (simplifier composant par composant) ;
   - suppression des sprints ;
   - résultats du harnais V2 (DAW, 3 h 50, 124,70 $).
5. Ce qui vient ensuite.
6. Annexe : extrait de spec générée par le planner.

## Fichiers

- [`content.md`](content.md) — article complet, navigation retirée.
- [`assets/01-solo-start-screen.png`](assets/01-solo-start-screen.png) — app solo, écran initial.
- [`assets/02-solo-sprite-editor.png`](assets/02-solo-sprite-editor.png) — app solo, éditeur de sprites.
- [`assets/03-solo-play-broken.png`](assets/03-solo-play-broken.png) — app solo, mode jeu cassé.
- [`assets/04-harness-new-game.png`](assets/04-harness-new-game.png) — app harnais, création de jeu.
- [`assets/05-harness-sprite-editor.png`](assets/05-harness-sprite-editor.png) — app harnais, éditeur de sprites.
- [`assets/06-harness-ai-level-1.png`](assets/06-harness-ai-level-1.png) — génération de niveau par l'IA intégrée (1).
- [`assets/07-harness-ai-level-2.png`](assets/07-harness-ai-level-2.png) — génération de niveau par l'IA intégrée (2).
- [`assets/08-harness-play.png`](assets/08-harness-play.png) — app harnais, jeu jouable.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
