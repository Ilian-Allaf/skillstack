"""Check that every reference in the framework points at something that exists.

Usage: python -I tools/check_refs.py [--root PATH]

A reference is any place where one text names another thing:
  - R001 a Markdown link whose file does not exist (docs outside skills/; lint_skills.py covers skills/);
  - R002 a link whose #anchor matches no heading in the target file;
  - R003 a path in backticks, such as `ship/references/design.md` or `tools/lint_skills.py`,
         that names a framework file that does not exist; a file the repo removed on purpose
         stays allowed in the dated docs (the changelog, docs/sources.md, the ADRs), which keep their history;
  - R004 a kebab-case name in backticks in a skill, such as `fix-root-causes`, that is not a skill,
         a principle id, a playbook, a glossary term, or a generated skill;
  - R005 a skill name that was retired by a rename, so an agent never looks for a skill that is gone;
  - R006 a skill without its row in the table of skills/GRAPH.md, so the graph cannot fall behind the skills;
  - R007 .claude-plugin/plugin.json not listing exactly the skills, so the plugin ships every skill and no ghost;
  - R008 a skill the top-level README.md does not link, so the reference list stays whole;
  - R009 a skill the router, choose-skill, never names as a command, so it cannot point at a skill it forgot;
  - R010 a principle id in principles.md without its full form in principles/<id>.md, or a full form without its row,
         so an agent that reads an id always finds the whole rule;
  - R011 a command in the user guide, docs/guide.md, code blocks included, that names no skill,
         so a prompt the user copies always launches something;
  - R012 a row of that table whose Runs or Run by disagrees with the skills' `calls:` frontmatter,
         so the graph draws no edge a skill does not declare, and misses none.

Scanned: skills/, the root docs (README, AGENTS, SCOPE, CHANGELOG, CODING_STANDARDS), docs/ and evals/.
Not scanned: knowledge/ (third-party sources) and docs/history/ (frozen design notes),
which keep the names of their time on purpose.

Exit code: 0 when every reference resolves, 1 otherwise, 2 on bad usage. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DOCS = ["README.md", "AGENTS.md", "SCOPE.md", "CHANGELOG.md", "CODING_STANDARDS.md", "docs/sources.md", "docs/guide.md"]
GUIDE = Path("docs/guide.md")
COMMAND_RE = re.compile(r"(?:^|[\s`(])/([a-z][a-z0-9-]*)(?![\w/.-])")
DOC_DIRS = ["evals", "docs/adr", "docs/agents"]
FRAMEWORK_DIRS = {"skills", "design", "tools", "evals", "knowledge", ".github"}
PRINCIPLES = Path("skills/constitution/references/principles.md")
PRINCIPLE_DIR = Path("skills/constitution/references/principles")
GLOSSARY = Path("skills/constitution/references/glossary.md")
PLAYBOOKS = Path("skills/ship/references/playbooks")

# Renamed on 2026-11-19. An old name in a skill sends the agent looking for a skill that is gone.
RETIRED = {
    "shape": "shape-spec",
    "probe": "analyze-impact",
    "verify": "verify-pr",
    "babysit": "babysit-pr",
    "reflect": "learn-from-mistakes",
    "correct": "add-guardrail",
    "create-verify-app": "create-app-driver",
    "verify-<app>": "drive-<app>",
    "verify-<area>-formal": "prove-<area>",
}
# Skills the framework generates in the target repo, named with a placeholder.
GENERATED_RE = re.compile(r"^(drive|prove)-<[a-z]+>$")
# Files the design names before they are built. Remove a line once its file exists.
PLANNED = {
    "tools/graph.py": "roadmap step 4",
    "evals/e2e/": "end-to-end cases, decided on the testbed",
}
# Files removed on purpose, each with what replaced it. Living docs must not name them; dated docs may.
REMOVED = {
    "skills/README.md": "skills/GRAPH.md",
}
DATED_DOCS = {"CHANGELOG.md", "docs/sources.md"}
GRAPH = Path("skills/GRAPH.md")
# A row of the skill table in GRAPH.md: | [name](name/SKILL.md) | what it does | runs | run by |
GRAPH_ROW_RE = re.compile(r"(?m)^\| \[([a-z0-9-]+)\]\(\1/SKILL\.md\) \|[^|]*\|([^|]*)\|([^|]*)\|\s*$")
CALLS_RE = re.compile(r'(?m)^\s+calls:\s*"([^"]*)"')
# Literal names from code that are not framework vocabulary, each with why it is here.
CODE_NAMES = {
    "record-demo": "the demo helper a drive-<app> skill ships",
    "site-packages": "the Python install directory read by analyze-impact",
}

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")
KEBAB_RE = re.compile(r"^/?[a-z][a-z0-9]*(-[a-z0-9<>]+)+$")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass
class Finding:
    path: Path
    line: int
    code: str
    message: str

    def render(self, root: Path) -> str:
        try:
            shown = self.path.relative_to(root).as_posix()
        except ValueError:
            shown = self.path.as_posix()
        return f"{shown}:{self.line}: error [{self.code}] {self.message}"


def text_lines(lines: list[str]) -> list[tuple[int, str]]:
    """Lines outside fenced code blocks, with their numbers."""
    out, fenced = [], False
    for number, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append((number, raw))
    return out


def slug(heading: str) -> str:
    """GitHub's anchor for a heading: lowercase, punctuation dropped, spaces to hyphens."""
    text = re.sub(r"[`*_\[\]()]", lambda m: "_" if m.group(0) == "_" else "", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


_anchors: dict[Path, set[str]] = {}


def anchors(path: Path) -> set[str]:
    if path not in _anchors:
        found: set[str] = set()
        seen: dict[str, int] = {}
        for _, raw in text_lines(path.read_text(encoding="utf-8").splitlines()):
            m = HEADING_RE.match(raw)
            if m:
                s = slug(m.group(2))
                n = seen.get(s, 0)
                found.add(s if n == 0 else f"{s}-{n}")
                seen[s] = n + 1
        _anchors[path] = found
    return _anchors[path]


def principle_ids(root: Path) -> dict[str, int]:
    """The ids of the principle index, each with its line: the first cell of a table row, in backticks."""
    ids: dict[str, int] = {}
    if (root / PRINCIPLES).exists():
        for number, line in enumerate((root / PRINCIPLES).read_text(encoding="utf-8").splitlines(), 1):
            m = re.match(r"^\| `([a-z0-9-]+)` \|", line)
            if m:
                ids[m.group(1)] = number
    return ids


def vocabulary(root: Path) -> set[str]:
    names = {p.name for p in (root / "skills").iterdir() if (p / "SKILL.md").exists()}
    names |= set(principle_ids(root))
    if (root / PLAYBOOKS).is_dir():
        names |= {p.stem for p in (root / PLAYBOOKS).glob("*.md")}
    if (root / GLOSSARY).exists():
        for line in (root / GLOSSARY).read_text(encoding="utf-8").splitlines():
            if line.startswith("| ") and not line.startswith("| Term"):
                # The Term and Avoid columns, and every name the meanings define in backticks.
                cells = line.split("|")
                names |= {t for t in re.findall(r"[a-z][a-z0-9<>-]*", cells[1]) if "-" in t}
                names |= {t for t in re.findall(r"`([a-z][a-z0-9<>-]*)`", line) if "-" in t}
    return names | set(CODE_NAMES)


def framework_path(token: str, root: Path) -> Path | None:
    """The file a backticked path names, or None when it is not a framework path."""
    if " " in token or "*" in token or "<" in token or "://" in token:
        return None
    if not re.search(r"\.(md|py|yml|json|html)$|/$", token):
        return None
    first = token.split("/", 1)[0]
    if first in {".", ".."}:  # relative to some other file: only a link can be resolved
        return None
    if first in FRAMEWORK_DIRS:
        return root / token
    if (root / "skills" / first / "SKILL.md").exists() or (root / "skills" / first / "README.md").exists():
        return root / "skills" / token
    return None


def is_dated(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    return rel in DATED_DOCS or rel.startswith("docs/adr/")


def check_file(path: Path, root: Path, vocab: set[str], in_skills: bool, out: list[Finding]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    # lint_skills.py checks the links of each skill folder (L001); a file at the top of skills/ is ours.
    linted = in_skills and path.parent != root / "skills"
    dated = is_dated(path, root)
    for number, raw in text_lines(lines):
        for target in LINK_RE.findall(raw):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            file_part, _, anchor = target.partition("#")
            resolved = (path.parent / file_part).resolve() if file_part else path
            if file_part and not resolved.exists():
                if not linted:
                    out.append(Finding(path, number, "R001", f"link {target!r} points at a file that does not exist. Fix: point it at an existing file, relative to this one."))
                continue
            if anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
                out.append(Finding(path, number, "R002", f"anchor #{anchor} matches no heading in {resolved.name}. Fix: use one of {sorted(anchors(resolved))[:8]}, or rename the heading."))
        for token in CODE_SPAN_RE.findall(raw):
            target = framework_path(token, root)
            if target is not None and not target.exists() and token not in PLANNED:
                if token in REMOVED:
                    if not dated:
                        out.append(Finding(path, number, "R003", f"path `{token}` names a file the repo removed. Fix: write `{REMOVED[token]}`, or remove the reference."))
                else:
                    out.append(Finding(path, number, "R003", f"path `{token}` names a framework file that does not exist. Fix: correct the path, or remove the reference."))
            if not in_skills:
                continue
            bare = token.lstrip("/")
            if bare in RETIRED:
                out.append(Finding(path, number, "R005", f"`{token}` is a retired skill name. Fix: write `{RETIRED[bare]}`."))
            elif KEBAB_RE.match(token) and bare not in vocab and not GENERATED_RE.match(bare):
                out.append(Finding(path, number, "R004", f"`{token}` is not a skill, principle id, playbook, glossary term, or generated skill. Fix: correct the name, or define it in the glossary."))
            elif token.startswith("/") and KEBAB_RE.match(token) is None and re.fullmatch(r"/[a-z][a-z0-9-]*", token) and bare not in vocab:
                out.append(Finding(path, number, "R004", f"`{token}` is a command for a skill that does not exist. Fix: use the name of a skill in skills/."))


def declared_calls(root: Path, skills: list[str]) -> dict[str, set[str]]:
    """The skills each skill runs, from its `calls:` frontmatter; repo skills such as drive-<app> are left out."""
    calls: dict[str, set[str]] = {}
    for name in skills:
        text = (root / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
        front = text.split("---", 2)[1] if text.startswith("---") else ""
        match = CALLS_RE.search(front)
        listed = {c.strip() for c in match.group(1).split(",")} if match else set()
        calls[name] = {c for c in listed if c in skills}
    return calls


def check_graph(root: Path, out: list[Finding]) -> None:
    """The skill table in skills/GRAPH.md matches the frontmatter, so it is checked like code, not trusted like prose."""
    graph = root / GRAPH
    if not graph.exists():
        return
    text = graph.read_text(encoding="utf-8")
    skills = skill_names(root)
    rows = {m.group(1): (m.group(2), m.group(3), text.count("\n", 0, m.start()) + 1) for m in GRAPH_ROW_RE.finditer(text)}
    calls = declared_calls(root, skills)

    def named(cell: str) -> set[str]:
        return {t for t in re.findall(r"[a-z][a-z0-9-]*", cell) if t in skills}

    for skill in skills:
        if skill not in rows:
            out.append(Finding(graph, 1, "R006", f"the skill {skill!r} has no row in the table. Fix: add `| [{skill}]({skill}/SKILL.md) | what it does | runs | run by |`, and its node and edges to the diagram of its flow."))
            continue
        runs, run_by, line = rows[skill]
        callers = {other for other in skills if skill in calls[other]}
        if named(runs) != calls[skill]:
            out.append(Finding(graph, line, "R012", f"{skill!r} runs {sorted(calls[skill])} by its calls:, the table says {sorted(named(runs))}. Fix: correct the Runs cell and the diagrams, or the frontmatter."))
        if named(run_by) != callers:
            out.append(Finding(graph, line, "R012", f"{skill!r} is run by {sorted(callers)} by their calls:, the table says {sorted(named(run_by))}. Fix: correct the Run by cell and the diagrams, or the frontmatter."))


def skill_names(root: Path) -> list[str]:
    return sorted(p.name for p in (root / "skills").iterdir() if (p / "SKILL.md").exists())


def check_lists(root: Path, out: list[Finding]) -> None:
    """Every list of the skills names all of them, so adding or renaming a skill cannot leave one behind."""
    skills = skill_names(root)
    plugin = root / ".claude-plugin" / "plugin.json"
    if plugin.exists():
        try:
            listed = json.loads(plugin.read_text(encoding="utf-8")).get("skills", [])
        except json.JSONDecodeError as error:
            out.append(Finding(plugin, error.lineno, "R007", f"plugin.json is not valid JSON: {error.msg}. Fix: correct it, then run `claude plugin validate . --strict`."))
            listed = None
        if listed is not None:
            expected = {f"./skills/{name}" for name in skills}
            for path in sorted(expected - set(listed)):
                out.append(Finding(plugin, 1, "R007", f"the skill {path[9:]!r} is missing from plugin.json, so the plugin does not ship it. Fix: add {path!r} to skills."))
            for path in sorted(set(listed) - expected):
                out.append(Finding(plugin, 1, "R007", f"plugin.json lists {path!r}, which is not a skill folder. Fix: remove it, or correct the path."))
    readme = root / "README.md"
    if readme.exists():
        text = readme.read_text(encoding="utf-8")
        for name in skills:
            if f"(skills/{name}/SKILL.md)" not in text:
                out.append(Finding(readme, 1, "R008", f"the skill {name!r} is missing from the README. Fix: add its line to Reference, linked to skills/{name}/SKILL.md."))
    router = root / "skills" / "choose-skill" / "SKILL.md"
    if router.exists():
        text = router.read_text(encoding="utf-8")
        for name in skills:
            if name != "choose-skill" and not re.search(rf"`/{re.escape(name)}(?![\w-])", text):
                out.append(Finding(router, 1, "R009", f"the router never names `/{name}`, so it can never send the user there. Fix: add the situations that call for it to the table."))


def check_principles(root: Path, out: list[Finding]) -> None:
    """The index and the folder of full forms list the same principles, so neither can fall behind the other."""
    ids = principle_ids(root)
    if not ids:
        return
    folder = root / PRINCIPLE_DIR
    files = {p.stem for p in folder.glob("*.md")} if folder.is_dir() else set()
    for name, number in ids.items():
        if name not in files:
            out.append(Finding(root / PRINCIPLES, number, "R010", f"the principle `{name}` has no full form. Fix: write {PRINCIPLE_DIR.as_posix()}/{name}.md, or remove its row."))
    for name in sorted(files - ids.keys()):
        out.append(Finding(folder / f"{name}.md", 1, "R010", f"the principle `{name}` has no row in principles.md. Fix: add its row, or rename the file to the id of an existing row."))


def check_guide(root: Path, out: list[Finding]) -> None:
    """Every command in the guide launches a skill, code blocks included, since those are the prompts the user copies."""
    guide = root / GUIDE
    if not guide.exists():
        return
    skills = set(skill_names(root))
    for number, line in enumerate(guide.read_text(encoding="utf-8").splitlines(), 1):
        for name in COMMAND_RE.findall(line):
            if name not in skills:
                out.append(Finding(guide, number, "R011", f"`/{name}` names no skill. Fix: use the name of a skill in skills/, or remove the command."))


def check(root: Path) -> list[Finding]:
    if not (root / "skills").is_dir():
        return [Finding(root / "skills", 1, "R000", "no skills/ folder.")]
    _anchors.clear()
    vocab = vocabulary(root)
    out: list[Finding] = []
    for path in sorted((root / "skills").rglob("*.md")):
        check_file(path, root, vocab, True, out)
    docs = [root / d for d in DOCS if (root / d).exists()]
    for d in DOC_DIRS:
        if (root / d).is_dir():
            docs += sorted((root / d).rglob("*.md"))
    for path in docs:
        check_file(path, root, vocab, False, out)
    check_graph(root, out)
    check_lists(root, out)
    check_principles(root, out)
    check_guide(root, out)
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check that every reference in the framework resolves.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="framework root (default: this repo)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    findings = check(root)
    for finding in findings:
        print(finding.render(root))
    print(f"{len(findings)} broken reference(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
