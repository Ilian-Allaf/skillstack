"""Check that every reference in the framework points at something that exists.

Usage: python -I tools/check_refs.py [--root PATH]

A reference is any place where one text names another thing:
  - R001 a Markdown link whose file does not exist (docs outside skills/; lint_skills.py covers skills/);
  - R002 a link whose #anchor matches no heading in the target file;
  - R003 a path in backticks, such as `ship/references/design.md` or `tools/lint_skills.py`,
         that names a framework file that does not exist;
  - R004 a kebab-case name in backticks in a skill, such as `fix-root-causes`, that is not a skill,
         a principle id, a playbook, a glossary term, or a generated skill;
  - R005 a skill name that was retired by a rename, so an agent never looks for a skill that is gone;
  - R006 a skill missing from the map in skills/README.md, so the diagram cannot fall behind the skills.

Scanned: skills/, the root docs (README, AGENTS, SCOPE, CHANGELOG, CODING_STANDARDS), docs/ and evals/.
Not scanned: knowledge/ (third-party sources) and docs/history/ (frozen design notes),
which keep the names of their time on purpose.

Exit code: 0 when every reference resolves, 1 otherwise, 2 on bad usage. Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

DOCS = ["README.md", "AGENTS.md", "SCOPE.md", "CHANGELOG.md", "CODING_STANDARDS.md", "docs/sources.md"]
DOC_DIRS = ["evals", "docs/adr", "docs/agents"]
FRAMEWORK_DIRS = {"skills", "design", "tools", "evals", "knowledge", ".github"}
PRINCIPLES = Path("skills/constitution/references/principles.md")
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


def vocabulary(root: Path) -> set[str]:
    names = {p.name for p in (root / "skills").iterdir() if (p / "SKILL.md").exists()}
    if (root / PRINCIPLES).exists():
        for line in (root / PRINCIPLES).read_text(encoding="utf-8").splitlines():
            m = re.match(r"^\| `([a-z0-9-]+)` \|", line)
            if m:
                names.add(m.group(1))
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


def check_file(path: Path, root: Path, vocab: set[str], in_skills: bool, out: list[Finding]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    for number, raw in text_lines(lines):
        for target in LINK_RE.findall(raw):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            file_part, _, anchor = target.partition("#")
            resolved = (path.parent / file_part).resolve() if file_part else path
            if file_part and not resolved.exists():
                if not in_skills:  # lint_skills.py reports these inside skills/ (L001)
                    out.append(Finding(path, number, "R001", f"link {target!r} points at a file that does not exist. Fix: point it at an existing file, relative to this one."))
                continue
            if anchor and resolved.suffix == ".md" and anchor not in anchors(resolved):
                out.append(Finding(path, number, "R002", f"anchor #{anchor} matches no heading in {resolved.name}. Fix: use one of {sorted(anchors(resolved))[:8]}, or rename the heading."))
        for token in CODE_SPAN_RE.findall(raw):
            target = framework_path(token, root)
            if target is not None and not target.exists() and token not in PLANNED:
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


def check_map(root: Path, out: list[Finding]) -> None:
    """The diagram in skills/README.md names every skill, so it is checked like code, not trusted like prose."""
    readme = root / "skills" / "README.md"
    if not readme.exists():
        return
    diagram = " ".join(re.findall(r"```mermaid\r?\n(.*?)```", readme.read_text(encoding="utf-8"), re.S))
    for skill in sorted(p.name for p in (root / "skills").iterdir() if (p / "SKILL.md").exists()):
        if not re.search(rf"(?<![\w-]){re.escape(skill)}(?![\w-])", diagram):
            out.append(Finding(readme, 1, "R006", f"the skill {skill!r} is missing from the map. Fix: add its node and its edges to the first mermaid diagram."))


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
    check_map(root, out)
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
