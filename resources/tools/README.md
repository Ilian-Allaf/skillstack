# Outils de la base de connaissance

Scripts à lancer depuis `resources/`. Python 3.10+.

| Script | Rôle | Dépendances |
|---|---|---|
| [`build_skill_catalog.py`](build_skill_catalog.py) | Scanne chaque `SKILL.md` des snapshots de repos et régénère `catalog.json`, `SKILLS-INDEX.md` par repo, puis `SKILL-CATALOG.md` et `skill-catalog.json` à la racine. | aucune |
| [`fetch_youtube_transcript.py`](fetch_youtube_transcript.py) | Télécharge les sous-titres d'une vidéo YouTube et écrit `raw/segments.json` et `transcript.md`. | `youtube-transcript-api` |

## Rafraîchir un repo de skills

```bash
# 1. Cloner la dernière révision dans un dossier temporaire vide
git clone --depth 1 https://github.com/mattpocock/skills /tmp/mattpocock-skills
git -C /tmp/mattpocock-skills rev-parse HEAD        # noter la révision

# 2. Remplacer le snapshot (sans .git ni node_modules)
rm -rf sources/repos/mattpocock-skills/repo
mkdir -p sources/repos/mattpocock-skills/repo
cp -r /tmp/mattpocock-skills/. sources/repos/mattpocock-skills/repo/
rm -rf sources/repos/mattpocock-skills/repo/.git sources/repos/mattpocock-skills/repo/node_modules

# 3. Mettre à jour la révision dans sources.json et SOURCE.md, puis régénérer le catalogue
python -I tools/build_skill_catalog.py
```

Pour `cursor-pstack`, ne copier que le sous-dossier `pstack/` du repo `cursor/plugins`.

## Ajouter une vidéo

```bash
python -I tools/fetch_youtube_transcript.py <video_id> sources/videos/<AAAA-MM-JJ>-<slug> --title <slug>
```

Ensuite, écrire à la main `SOURCE.md` (fiche) et `nectar.md` (distillation), puis ajouter l'entrée dans `sources.json` et `SOURCES.md`.
