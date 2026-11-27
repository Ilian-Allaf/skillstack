# Source — All Code Is Slop (Except Mine)

## Fiche

| Champ | Valeur |
|---|---|
| Type | Conférence vidéo |
| Titre | All Code Is Slop (Except Mine) — Lauren Tan, SpaceXSI |
| Autrice | Lauren Tan (poteto) |
| Chaîne | AI Engineer |
| URL | <https://www.youtube.com/watch?v=O_zcc6Xl12g> |
| Publiée le | 2026-11-14 |
| Durée | 17:31 |
| Langue | Anglais |
| Transcript | [`transcript.md`](transcript.md) — sous-titres automatiques nettoyés |
| Données brutes | [`raw/segments.json`](raw/segments.json) — 470 segments horodatés |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

Comment passer d'un agent de faible confiance à un agent de haute confiance, et augmenter massivement la production de code sans dégrader la qualité. Lauren Tan décrit l'environnement qu'elle a construit pour son équipe : contraintes déterministes dans le code, vérification runtime et formelle, puis une petite couche de prose.

## Fiabilité du transcript

Le transcript provient des sous-titres automatiques YouTube, nettoyés et regroupés en paragraphes. Les noms propres et acronymes sont susceptibles d'être mal transcrits (`Grokbot`, `Dune`, `SpaceXSI`, `Grabot`). Les citations du nectar sont fidèles au transcript, mais l'orthographe des noms doit être vérifiée contre la vidéo avant publication.

## Chapitres

| Temps | Sujet |
|---|---|
| 00:01 | 3 000 PR en un mois ; le slop des autres |
| 01:25 | Le vrai sujet : la confiance, pas la vitesse |
| 01:59 | La pyramide inversée de l'environnement agent |
| 02:44 | Le codebase est le plus gros input |
| 03:27 | Le codebase comme jardin |
| 04:53 | Dune : contraindre plutôt que corriger |
| 06:12 | La structure de répertoires comme contexte |
| 06:53 | Les agents utilisent le Markdown pour justifier leurs contournements |
| 08:14 | Bannir les commentaires ; des lint rules qui expliquent la cause racine |
| 09:32 | La revue devient une revue d'artefacts de vérification |
| 10:52 | Vérification formelle : TLA+, Lean |
| 11:33 | Property-based testing ; 70 % des tokens en vérification |
| 12:52 | L'âge d'or du test ; statechart |
| 13:29 | Résultats : 11 000 PR, 227 contributeurs, 0,5 % de revert |
| 14:49 | Commencer par le codebase et la vérification, pas par l'automatisation |
| 16:11 | La boucle externe : routines, fuzzing, PR de fix, auto-merge |

## Fichiers

- [`transcript.md`](transcript.md) — transcript lisible avec timestamps.
- [`raw/segments.json`](raw/segments.json) — segments source, pour retrouver une citation exacte.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
