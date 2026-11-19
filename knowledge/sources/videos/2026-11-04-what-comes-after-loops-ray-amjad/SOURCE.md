# Source — OpenAI and Anthropic Agree on What Comes After Loops

## Fiche

| Champ | Valeur |
|---|---|
| Type | Vidéo d'analyse |
| Titre | OpenAI and Anthropic Agree on What Comes After Loops |
| Auteur | Ray Amjad |
| URL | <https://www.youtube.com/watch?v=yrRpnx_iugY> |
| Publiée le | 2026-11-04 |
| Durée | 23:11 |
| Langue | Anglais |
| Transcript | [`transcript.md`](transcript.md) — sous-titres automatiques nettoyés |
| Données brutes | [`raw/segments.json`](raw/segments.json) — 303 segments horodatés |
| Nectar | [`nectar.md`](nectar.md) |

## Sujet

Synthèse de la conférence OpenAI DevDay Tokyo « What Comes After Loops » et du research post Anthropic « Patterns and Problems in Emerging Multi-Agent Systems ». Le fil conducteur : les boucles d'un agent unique sont résolues ; le problème suivant est la **coordination de plusieurs agents**. La vidéo propose une échelle à sept barreaux, du single agent au swarm, et discute ce qui marche aujourd'hui, ce qui ne marche pas encore, et pourquoi.

## Fiabilité de la source

C'est une source **secondaire** : Ray Amjad rapporte et interprète les propos d'OpenAI et d'Anthropic, avec ses propres expériences et celles de ses étudiants. Les chiffres et les affirmations sur les modèles doivent être traités comme des rapports, pas comme des mesures indépendantes. Le transcript est automatique ; certains noms de modèles et de produits peuvent être mal transcrits.

## Chapitres

| Temps | Sujet |
|---|---|
| 00:00 | Contexte : DevDay Tokyo, « What Comes After Loops » |
| 00:28 | Les boucles sont résolues ; le problème devient la coordination |
| 01:32 | L'échelle à sept barreaux |
| 01:58 | Barreau 1 : un agent, un objectif clair, des outils, un self-check |
| 02:51 | Barreau 2 : fan-out sur du travail réellement indépendant |
| 03:52 | Pourquoi la décomposition spec → tickets → subagents échoue souvent |
| 05:27 | Barreau 3 : effort scaling et advisor |
| 06:31 | Barreau 4 : les paires builder / reviewer / verifier |
| 09:07 | Même builder ou nouveau builder ? Les 38 % |
| 10:14 | Vérifier à la frontière de capacité du modèle |
| 11:51 | Les hypothèses du harnais deviennent obsolètes |
| 12:51 | Ce que les modèles absorbent |
| 13:19 | Barreau 5 : le manager thread |
| 15:27 | Barreaux 6 et 7 : long-lived leads et swarms |
| 17:09 | Pourquoi les rôles et personas échouent |
| 18:10 | Les swarms OpenAI et l'explore-exploit |
| 19:11 | Minecraft : 50 agents, bureaucratie, famine |
| 20:17 | L'expérience personnelle : stagnation par les rôles |
| 21:19 | Le swarm qui marche : la chasse aux vulnérabilités |
| 22:26 | Le futur : des agents sur le système de production |

## Fichiers

- [`transcript.md`](transcript.md) — transcript lisible avec timestamps.
- [`raw/segments.json`](raw/segments.json) — segments source.
- [`nectar.md`](nectar.md) — distillation en français, avec implications pour notre framework.
