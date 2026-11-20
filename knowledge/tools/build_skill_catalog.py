"""Build the skill catalog and human-readable indexes from imported repo snapshots.

Reads knowledge/sources.json for repo metadata, scans every SKILL.md under each
repo's local_path, and writes:
  - <repo>/catalog.json          full machine-readable catalog
  - <repo>/SKILLS-INDEX.md       per-repo index grouped by category
  - SKILL-CATALOG.md             global index across repos
  - skill-catalog.json           global machine-readable catalog

No third-party dependencies. Frontmatter support is limited to the keys these
repos use (name, description, disable-model-invocation, plus scalar extras and
folded descriptions).
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources.json"
FRONTMATTER = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.S)


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    match = FRONTMATTER.match(text)
    if not match:
        return {}, text
    raw = match.group(1)
    body = text[match.end():]
    data: dict[str, object] = {}
    lines = raw.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value in {">", ">-", "|", "|-"}:
            chunk = []
            i += 1
            while i < len(lines) and (lines[i].startswith(" ") or not lines[i].strip()):
                chunk.append(lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in chunk if part).strip()
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
        i += 1
    return data, body


def clean_description(value: object) -> str:
    text = str(value or "").strip()
    return re.sub(r"\s+", " ", text)


def category_for(repo_dir: Path, skill_file: Path) -> str:
    rel = skill_file.parent.relative_to(repo_dir)
    parts = rel.parts
    if parts and parts[0] == "skills" and len(parts) > 1:
        return parts[1] if len(parts) > 2 else "skills"
    if parts and parts[0] == "skills":
        return "skills"
    return "root" if len(parts) == 1 else "/".join(parts[:-1])


def support_files(skill_dir: Path) -> dict[str, object]:
    files = [p for p in skill_dir.rglob("*") if p.is_file() and p.name != "SKILL.md"]
    dirs = {p.name for p in skill_dir.rglob("*") if p.is_dir()}
    return {
        "file_count": len(files),
        "has_playbooks": "playbooks" in dirs,
        "has_references": "references" in dirs,
        "has_scripts": "scripts" in dirs,
        "has_assets": "assets" in dirs,
        "files": [str(p.relative_to(skill_dir)).replace("\\", "/") for p in files],
    }


def explicit_references(body: str, names: list[str], self_name: str) -> list[dict[str, object]]:
    refs: list[dict[str, object]] = []
    for name in names:
        if name == self_name:
            continue
        patterns = [
            rf"\.\./{re.escape(name)}/SKILL\.md",
            rf"`{re.escape(name)}`",
            rf"(?<![\w-])/{re.escape(name)}(?![\w-])",
        ]
        count = 0
        for pattern in patterns:
            count += len(re.findall(pattern, body, flags=re.I))
        if count:
            refs.append({"target": name, "mentions": count})
    return sorted(refs, key=lambda r: (-int(r["mentions"]), str(r["target"])))


def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0]
    return cut + "…"


def main() -> None:
    registry = json.loads(SOURCES.read_text(encoding="utf-8"))
    repos = [s for s in registry["sources"] if s["type"] == "skill-repo"]
    global_skills: list[dict[str, object]] = []

    for repo in repos:
        repo_dir = (ROOT / repo["local_path"]).resolve()
        skill_files = sorted(repo_dir.rglob("SKILL.md"))
        parsed = []
        for skill_file in skill_files:
            text = skill_file.read_text(encoding="utf-8")
            front, body = parse_frontmatter(text)
            name = str(front.get("name") or skill_file.parent.name)
            description = clean_description(front.get("description"))
            disable = str(front.get("disable-model-invocation", "")).lower() == "true"
            extra = {
                k: v
                for k, v in front.items()
                if k not in {"name", "description", "disable-model-invocation"}
            }
            support = support_files(skill_file.parent)
            parsed.append(
                {
                    "repo": repo["id"],
                    "name": name,
                    "description": description,
                    "category": category_for(repo_dir, skill_file),
                    "invocation": "user" if disable else "model",
                    "path": str(skill_file.relative_to(ROOT)).replace("\\", "/"),
                    "words": len(body.split()),
                    "frontmatter_extra": extra,
                    "support": support,
                }
            )

        names = [p["name"] for p in parsed]
        name_to_path = {p["name"]: p["path"] for p in parsed}
        for item in parsed:
            body = Path(ROOT / item["path"]).read_text(encoding="utf-8")
            item["references"] = explicit_references(body, names, str(item["name"]))
        for item in parsed:
            item["referenced_by"] = sorted(
                {
                    str(other["name"])
                    for other in parsed
                    if any(r["target"] == item["name"] for r in other["references"])
                }
            )

        repo_catalog = {
            "repo": repo["id"],
            "title": repo["title"],
            "url": repo["url"],
            "author": repo["author"],
            "license": repo["license"],
            "revision": repo["revision"],
            "retrieved_at": repo["retrieved_at"],
            "generated_at": date.today().isoformat(),
            "skill_count": len(parsed),
            "skills": parsed,
        }
        out_dir = ROOT / "sources" / "repos" / repo["id"]
        (out_dir / "catalog.json").write_text(
            json.dumps(repo_catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        by_category: dict[str, list[dict[str, object]]] = defaultdict(list)
        for item in parsed:
            by_category[str(item["category"])].append(item)
        invocations = Counter(str(i["invocation"]) for i in parsed)
        with_scripts = sum(1 for i in parsed if i["support"]["has_scripts"])
        with_playbooks = sum(1 for i in parsed if i["support"]["has_playbooks"])
        with_references = sum(1 for i in parsed if i["support"]["has_references"])

        lines = [
            f"# Index des skills — {repo['title']}",
            "",
            f"- **Repo** : [{repo['url']}]({repo['url']})",
            f"- **Auteur** : {repo['author']}",
            f"- **Révision** : `{repo['revision']}` ({repo['revision_date']})",
            f"- **Importé le** : {repo['retrieved_at']}",
            f"- **Licence** : {repo['license']}",
            f"- **Skills** : {len(parsed)}",
            f"- **Invocation** : {invocations.get('model', 0)} modèle, {invocations.get('user', 0)} utilisateur",
            f"- **Avec scripts** : {with_scripts} · **avec références** : {with_references} · **avec playbooks** : {with_playbooks}",
            "",
            "> Catalogue complet : [`catalog.json`](catalog.json). Les descriptions sont celles du frontmatter, tronquées ici.",
            "",
        ]
        for category in sorted(by_category):
            items = sorted(by_category[category], key=lambda i: str(i["name"]))
            lines += [
                f"## {category} ({len(items)})",
                "",
                "| Skill | Invocation | Description | Mots | Support |",
                "|---|---|---|---:|---|",
            ]
            for item in items:
                support = []
                if item["support"]["has_playbooks"]:
                    support.append("playbooks")
                if item["support"]["has_references"]:
                    support.append("references")
                if item["support"]["has_scripts"]:
                    support.append("scripts")
                link = f"[`{item['name']}`]({Path(os.path.relpath(ROOT / str(item['path']), out_dir)).as_posix()})"
                lines.append(
                    f"| {link} | {item['invocation']} | {md_escape(truncate(str(item['description']), 220))} | {item['words']} | {', '.join(support) or '—'} |"
                )
            lines.append("")

        edges = [
            (item["name"], ref["target"], ref["mentions"])
            for item in parsed
            for ref in item["references"]
        ]
        lines += ["## Références explicites entre skills", ""]
        if edges:
            lines += ["| Depuis | Vers | Mentions |", "|---|---|---:|"]
            for source, target, count in sorted(edges, key=lambda e: (-e[2], e[0], e[1]))[:40]:
                lines.append(f"| `{source}` | `{target}` | {count} |")
            lines += [
                "",
                f"{len(edges)} arêtes explicites au total. Elles surestiment les dépendances réelles : un skill peut citer un autre skill sans en dépendre.",
                "",
            ]
        else:
            lines += ["Aucune référence explicite détectée.", ""]
        (out_dir / "SKILLS-INDEX.md").write_text("\n".join(lines), encoding="utf-8")

        for item in parsed:
            global_skills.append(item)
        print(f"{repo['id']}: {len(parsed)} skills, {len(edges)} explicit edges")

    global_catalog = {
        "schema_version": 1,
        "generated_at": date.today().isoformat(),
        "skill_count": len(global_skills),
        "skills": global_skills,
    }
    (ROOT / "skill-catalog.json").write_text(
        json.dumps(global_catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# Catalogue global des skills",
        "",
        f"{len(global_skills)} skills importés depuis {len(repos)} repos. Index détaillés par repo dans `sources/repos/<repo>/SKILLS-INDEX.md`.",
        "",
        "| Repo | Skill | Catégorie | Invocation | Description |",
        "|---|---|---|---|---|",
    ]
    for item in sorted(global_skills, key=lambda i: (str(i["repo"]), str(i["category"]), str(i["name"]))):
        repo_id = str(item["repo"])
        name = str(item["name"])
        link = f"[`{name}`]({item['path']})"
        lines.append(
            f"| {repo_id} | {link} | {item['category']} | {item['invocation']} | {md_escape(truncate(str(item['description']), 160))} |"
        )
    (ROOT / "SKILL-CATALOG.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"global: {len(global_skills)} skills")


if __name__ == "__main__":
    main()
