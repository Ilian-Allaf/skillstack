# Registre des sources

Toutes les sources importées dans cette base de connaissance, avec leur provenance, leur révision et leur licence.

**Date d'import** : 2026-11-16  
**Registre machine** : [`sources.json`](sources.json)

**Additional import, 2026-11-23**: sources 7 and 8 below. Earlier source records are unchanged.

---

## Vue d'ensemble

| # | Source | Type | Auteur | Date | Licence | Fichiers locaux |
|---|---|---|---|---|---|---|
| 1 | [Skills For Real Engineers](https://github.com/mattpocock/skills) | Dépôt de skills | Matt Pocock | 2026-11-12 | MIT | [`SOURCE.md`](sources/repos/mattpocock-skills/SOURCE.md) · [`index`](sources/repos/mattpocock-skills/SKILLS-INDEX.md) · [`snapshot`](sources/repos/mattpocock-skills/repo) |
| 2 | [pstack](https://github.com/cursor/plugins/tree/main/pstack) | Dépôt de skills | Lauren Tan (poteto) | 2026-11-14 | MIT | [`SOURCE.md`](sources/repos/cursor-pstack/SOURCE.md) · [`index`](sources/repos/cursor-pstack/SKILLS-INDEX.md) · [`snapshot`](sources/repos/cursor-pstack/repo) |
| 3 | [tstack](https://github.com/t3dotgg/tstack) | Dépôt de skills | Theo Browne | 2026-11-11 | MIT | [`SOURCE.md`](sources/repos/t3dotgg-tstack/SOURCE.md) · [`index`](sources/repos/t3dotgg-tstack/SKILLS-INDEX.md) · [`snapshot`](sources/repos/t3dotgg-tstack/repo) |
| 4 | [All Code Is Slop (Except Mine)](https://www.youtube.com/watch?v=O_zcc6Xl12g) | Vidéo | Lauren Tan (AI Engineer) | 2026-11-14 | YouTube standard | [`SOURCE.md`](sources/videos/2026-11-14-all-code-is-slop-lauren-tan/SOURCE.md) · [`transcript`](sources/videos/2026-11-14-all-code-is-slop-lauren-tan/transcript.md) · [`nectar`](sources/videos/2026-11-14-all-code-is-slop-lauren-tan/nectar.md) |
| 5 | [OpenAI and Anthropic Agree on What Comes After Loops](https://www.youtube.com/watch?v=yrRpnx_iugY) | Vidéo | Ray Amjad | 2026-11-04 | YouTube standard | [`SOURCE.md`](sources/videos/2026-11-04-what-comes-after-loops-ray-amjad/SOURCE.md) · [`transcript`](sources/videos/2026-11-04-what-comes-after-loops-ray-amjad/transcript.md) · [`nectar`](sources/videos/2026-11-04-what-comes-after-loops-ray-amjad/nectar.md) |
| 6 | [Building always-on agents](https://claude.com/fr/resources/articles/building-always-on-agents) | Article | William Hu (Anthropic) | 2026-11-13 | © Anthropic, usage documentaire | [`SOURCE.md`](sources/articles/2026-11-13-building-always-on-agents/SOURCE.md) · [`content`](sources/articles/2026-11-13-building-always-on-agents/content.md) · [`nectar`](sources/articles/2026-11-13-building-always-on-agents/nectar.md) |
| 7 | [How the Claude Code team thinks about verification](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/) | Article | Addy Osmani (Anthropic) | 2026-11-16 | © Anthropic; no redistribution license identified | [`SOURCE.md`](sources/articles/2026-11-16-claude-code-verification/SOURCE.md) · [reading notes](sources/articles/2026-11-16-claude-code-verification/content.md) · [nectar](sources/articles/2026-11-16-claude-code-verification/nectar.md) |
| 8 | [How Anthropic Verifies Code Written by Claude](https://www.youtube.com/watch?v=DNwMbJf5SAI) | Video | Ray Amjad | 2026-11-23 | No redistribution license verified | [`SOURCE.md`](sources/videos/2026-11-23-how-anthropic-verifies-code-ray-amjad/SOURCE.md) · [transcript](sources/videos/2026-11-23-how-anthropic-verifies-code-ray-amjad/transcript.md) · [timestamped notes](sources/videos/2026-11-23-how-anthropic-verifies-code-ray-amjad/notes.md) · [nectar](sources/videos/2026-11-23-how-anthropic-verifies-code-ray-amjad/nectar.md) |

---

## Provenance détaillée

### 1. `mattpocock/skills`

- **URL** : <https://github.com/mattpocock/skills>
- **Révision** : `5863806dd4e15c63174bee4e7515a4256792ecfa`
- **Date de révision** : 2026-11-12
- **Import** : snapshot complet, `.git` et `node_modules` exclus.
- **Contenu** : 39 skills, docs, ADRs, fichiers de scope, licence.
- **Licence** : MIT — Copyright (c) 2026 Matt Pocock. Voir [`repo/LICENSE`](sources/repos/mattpocock-skills/repo/LICENSE).

### 2. `cursor/plugins` → `pstack`

- **URL** : <https://github.com/cursor/plugins/tree/main/pstack>
- **Révision** : `bf0c7cd80abdbf7fe47b634978a7d1b4071f71a7`
- **Date de révision** : 2026-11-14
- **Import** : dossier `pstack/` complet, `.git` exclu.
- **Contenu** : 61 `SKILL.md`, 2 agents, 23 playbooks, 24 principes, docs, automatisations, licence.
- **Licence** : MIT — Copyright (c) 2026 Lauren Tan. Voir [`repo/LICENSE`](sources/repos/cursor-pstack/repo/LICENSE).

### 3. `t3dotgg/tstack`

- **URL** : <https://github.com/t3dotgg/tstack>
- **Révision** : `11e37a74d0a6868c121cd0910ab2b3bd9873b92a`
- **Date de révision** : 2026-11-11
- **Import** : snapshot complet, `.git` exclu.
- **Contenu** : 9 skills, README, licence.
- **Licence** : MIT — Copyright (c) 2026 Theo Browne. Voir [`repo/LICENSE`](sources/repos/t3dotgg-tstack/repo/LICENSE).

### 4. Vidéo — All Code Is Slop (Except Mine)

- **URL** : <https://www.youtube.com/watch?v=O_zcc6Xl12g>
- **Vidéo ID** : `O_zcc6Xl12g`
- **Publiée le** : 2026-11-14
- **Durée** : 17:31
- **Transcript** : sous-titres automatiques anglais, récupérés via `youtube-transcript-api`, nettoyés et regroupés en paragraphes.
- **Données brutes** : 470 segments horodatés dans `raw/segments.json`.
- **Fiabilité** : noms propres potentiellement mal transcrits ; vérifier avant citation publiée.

### 5. Vidéo — What Comes After Loops

- **URL** : <https://www.youtube.com/watch?v=yrRpnx_iugY>
- **Vidéo ID** : `yrRpnx_iugY`
- **Publiée le** : 2026-11-04
- **Durée** : 23:11
- **Transcript** : sous-titres automatiques anglais, récupérés via `youtube-transcript-api`, nettoyés et regroupés en paragraphes.
- **Données brutes** : 303 segments horodatés dans `raw/segments.json`.
- **Fiabilité** : source secondaire ; les chiffres sont des rapports, pas des mesures indépendantes.

### 6. Article — Building always-on agents

- **URL** : <https://claude.com/fr/resources/articles/building-always-on-agents>
- **Auteur** : William Hu (Anthropic)
- **Publié le** : 2026-11-13
- **Contenu** : version hors-ligne nettoyée, navigation et articles associés retirés. Les diagrammes d'origine sont conservés dans `assets/`.
- **Droits** : contenu © Anthropic, conservé à des fins de recherche documentaire. Ne pas republier comme contenu original.

---

## Additional provenance, collected 2026-11-23

### 7. Article — How the Claude Code team thinks about verification

- **URL**: <https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/>
- **Author**: Addy Osmani (Anthropic).
- **Published**: 2026-11-16; retrieved 2026-11-23.
- **Import**: paraphrased reading notes and dated analysis, not a full article copy. No illustrations imported.
- **Reliability**: a primary account of the team's process. Internal results were not independently reproduced.

### 8. Video — How Anthropic Verifies Code Written by Claude

- **URL**: <https://www.youtube.com/watch?v=DNwMbJf5SAI>
- **Author**: Ray Amjad.
- **Published**: 2026-11-23; retrieved 2026-11-23; duration 25:24.
- **Collection**: title and channel checked through YouTube oEmbed; publication date, duration and chapters through `yt-dlp`; automatic English captions retrieved with `youtube-transcript-api`. This import retains 822 timed segments in `raw/segments.json`, a readable timestamped transcript in `transcript.md`, selected metadata, reading notes and analysis. The transcript uses the same collection format as source 4 (Lauren Tan).
- **Dependency**: the video explicitly discusses source 7 and adds the presenter's demonstrations. Do not count both as independent evidence of the article's claims.
- **Framework status**: reference material only. The analyses distinguish proposals from adopted decisions and flag practices that conflict with accepted ADRs.

---

## Méthode de collecte

### Repos

```bash
git clone --depth 1 <url>
# copie du snapshot sans .git
```

Les révisions sont enregistrées dans `sources.json` et dans chaque `SOURCE.md`. Pour rafraîchir un repo, voir [`tools/README.md`](tools/README.md).

### Vidéos

Les transcripts ont été récupérés avec `youtube-transcript-api` après un échec 429 de `yt-dlp` sur les sous-titres. Le script [`tools/fetch_youtube_transcript.py`](tools/fetch_youtube_transcript.py) reproduit l'opération.

Chaque transcript contient :

- le texte nettoyé avec timestamps ;
- les segments bruts en JSON ;
- un fichier `nectar.md` qui distille les idées, les citations et les implications.

### Article

Le contenu a été récupéré depuis la page publique, puis nettoyé manuellement : navigation, menus, articles associés et pied de page retirés. Les images ont été téléchargées pour un usage hors-ligne.

---

## Attribution et licences

- Les trois dépôts sont sous licence MIT. Leurs textes et licences sont conservés dans les snapshots. Toute réutilisation doit conserver l'attribution aux auteurs.
- Les vidéos sont la propriété de leurs auteurs et chaînes. Les transcripts sont des notes de recherche, pas des publications.
- L'article est © Anthropic. Il est conservé comme source documentaire, avec attribution.
- Les documents de synthèse de ce dépôt sont des analyses originales. Ils citent les sources et ne prétendent pas remplacer leur lecture.

---

## Comment citer une source

Format recommandé :

```text
<Auteur> — <Titre>, <type>, <date>. <URL> (consulté le 2026-11-16).
```

Exemple :

```text
Lauren Tan — All Code Is Slop (Except Mine), conférence, 2026-11-14.
https://www.youtube.com/watch?v=O_zcc6Xl12g (consulté le 2026-11-16).
```
