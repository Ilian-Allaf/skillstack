"""Lint the framework's skills.

Usage: python -I tools/lint_skills.py [--root PATH]

Checks every skills/<name>/ folder:
  - frontmatter: required fields, name matches the folder, known kind, a hypothesis,
    declared calls point to real skills, the description names no other skill;
  - edges: a declared call is linked by path from SKILL.md, and every link into
    another skill's files is declared in metadata.calls or metadata.reads;
  - steps: a non-reference skill has a "## Steps" section, and every numbered step
    states its completion criterion with "Done when";
  - links: every relative Markdown link resolves, and every file under references/
    is linked from somewhere in the skill;
  - prose: no words from the banned vocabulary, no term from the glossary's Avoid
    column, no em dash, no curly quotes (code is skipped), and no external
    attribution (sources live in docs/sources.md);
  - size: SKILL.md over the word budget is a warning.

Exit code: 0 when there is no error (warnings allowed), 1 on errors, 2 on bad usage.
Standard library only, so it runs anywhere with `python -I`.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

KINDS = {"reference", "entry", "spine", "kit", "meta", "shaping"}
TOP_LEVEL_KEYS = {
    "name",
    "description",
    "disable-model-invocation",
    "metadata",
    "license",
    "compatibility",
    "allowed-tools",
    "argument-hint",
    "model",
}
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESCRIPTION_MAX = 1024
WORD_BUDGET = 800
GLOSSARY = Path("skills/constitution/references/glossary.md")

# pstack `unslop`, rules 7 and 31: words that read as AI tells, with the plain word to use.
BANNED_WORDS = {
    "additionally": "also, or start a new sentence",
    "crucial": "important, or say why",
    "delve": "look at, read",
    "enduring": "lasting",
    "enhance": "improve, or name the change",
    "fostering": "name the effect",
    "garner": "get",
    "interplay": "name the relation",
    "intricate": "complex, or name the parts",
    "pivotal": "important, or say why",
    "showcase": "show",
    "tapestry": "name the parts",
    "testament": "proof, or cut",
    "underscore": "show, or cut",
    "underscores": "shows, or cut",
    "vibrant": "cut",
    "utilize": "use",
    "leverage": "use",
    "facilitate": "help",
    "seamless": "name what works",
    "seamlessly": "name what works",
    "robust": "name the failure it survives",
}

EM_DASH = "—"
CURLY = {"‘": "'", "’": "'", "“": '"', "”": '"'}
# An agent that reads "Matt Pocock `grilling`" may go and run that skill instead of ours.
# Attribution lives in docs/sources.md, outside the skills.
EXTERNAL = re.compile(r"\b(pstack|tstack|cursor-pstack|poteto|Matt Pocock|Lauren Tan|Ray Amjad|Anthropic)\b|\bSources?( for [a-z ]+)?:", re.IGNORECASE)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
STEP_RE = re.compile(r"^\d+\.\s")


@dataclass
class Finding:
    path: Path
    line: int
    level: str  # "error" or "warning"
    code: str
    message: str

    def render(self, root: Path) -> str:
        try:
            shown = self.path.relative_to(root)
        except ValueError:
            shown = self.path
        return f"{shown.as_posix()}:{self.line}: {self.level} [{self.code}] {self.message}"


@dataclass
class Frontmatter:
    fields: dict[str, str] = field(default_factory=dict)
    metadata: dict[str, str] = field(default_factory=dict)
    lines: dict[str, int] = field(default_factory=dict)
    body_start: int = 0  # index of the first body line (0-based)


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(lines: list[str], path: Path, out: list[Finding]) -> Frontmatter | None:
    """Parse the YAML subset skills use: `key: value` and one level under `metadata:`."""
    if not lines or lines[0].strip() != "---":
        out.append(Finding(path, 1, "error", "F001", "SKILL.md must start with a '---' frontmatter block. Fix: add name, description, disable-model-invocation and metadata between two '---' lines."))
        return None
    fm = Frontmatter()
    in_metadata = False
    for i in range(1, len(lines)):
        raw = lines[i]
        if raw.strip() == "---":
            fm.body_start = i + 1
            return fm
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith((" ", "\t"))
        match = re.match(r"^\s*([A-Za-z0-9_-]+):\s*(.*)$", raw)
        if not match:
            out.append(Finding(path, i + 1, "error", "F002", f"cannot parse frontmatter line {raw.strip()!r}. Fix: write it as 'key: value' on one line."))
            continue
        key, value = match.group(1), match.group(2)
        if indented:
            if not in_metadata:
                out.append(Finding(path, i + 1, "error", "F002", f"indented key {key!r} outside metadata. Fix: only metadata takes nested keys."))
                continue
            fm.metadata[key] = unquote(value)
            fm.lines[f"metadata.{key}"] = i + 1
            continue
        in_metadata = key == "metadata"
        if in_metadata and value.strip():
            out.append(Finding(path, i + 1, "error", "F002", "metadata must be a block of indented 'key: value' lines."))
        fm.fields[key] = unquote(value)
        fm.lines[key] = i + 1
    out.append(Finding(path, 1, "error", "F001", "frontmatter is never closed. Fix: add a closing '---' line."))
    return None


def strip_code(lines: list[str]) -> list[tuple[int, str]]:
    """Return (line number, text) for prose lines, with fenced blocks and inline code removed."""
    prose: list[tuple[int, str]] = []
    fenced = False
    for number, raw in enumerate(lines, start=1):
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced:
            continue
        prose.append((number, INLINE_CODE_RE.sub("", raw)))
    return prose


def load_avoid_terms(root: Path) -> list[tuple[str, str]]:
    """Read (avoided term, preferred term) pairs from the glossary's Avoid column."""
    path = root / GLOSSARY
    if not path.exists():
        return []
    pairs: list[tuple[str, str]] = []
    header: list[str] | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.startswith("|"):
            continue
        cells = [c.strip() for c in raw.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            continue
        if set("".join(cells)) <= set("-: "):
            continue
        if "avoid" not in header or "term" not in header:
            return []
        avoid = cells[header.index("avoid")] if len(cells) > header.index("avoid") else ""
        term = cells[header.index("term")].strip("`")
        for item in re.findall(r"`([^`]+)`", avoid):
            pairs.append((item, term))
    return pairs


def check_prose(path: Path, lines: list[str], avoid: list[tuple[str, str]], is_glossary: bool, out: list[Finding]) -> None:
    for number, raw in enumerate(lines, start=1):
        if EM_DASH in raw:
            out.append(Finding(path, number, "error", "P003", "em dash. Fix: end the sentence, or use a comma (pstack unslop rule 13)."))
        for char, plain in CURLY.items():
            if char in raw:
                out.append(Finding(path, number, "error", "P004", f"curly quote {char!r}. Fix: use the straight quote {plain}."))
                break
        match = EXTERNAL.search(raw)
        if match:
            out.append(Finding(path, number, "error", "P005", f"external attribution {match.group(0)!r} in a skill: an agent may follow it out of the framework. Fix: move it to docs/sources.md and keep only the rule here."))
    for number, text in strip_code(lines):
        for word in re.findall(r"[A-Za-z]+", text):
            plain = BANNED_WORDS.get(word.lower())
            if plain:
                out.append(Finding(path, number, "error", "P001", f"banned word {word!r}. Fix: {plain} (pstack unslop)."))
        if is_glossary:
            continue
        for term, preferred in avoid:
            if re.search(rf"(?<![\w-]){re.escape(term)}(?![\w-])", text, re.IGNORECASE):
                out.append(Finding(path, number, "error", "P002", f"{term!r} is in the glossary's Avoid column. Fix: write {preferred!r}."))


def check_links(path: Path, lines: list[str], out: list[Finding]) -> set[Path]:
    targets: set[Path] = set()
    for number, text in strip_code(lines):
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target) or target.startswith("#"):
                continue
            file_part = target.split("#", 1)[0]
            if not file_part:
                continue
            resolved = (path.parent / file_part).resolve()
            if not resolved.exists():
                out.append(Finding(path, number, "error", "L001", f"broken link {target!r}. Fix: point it at an existing file, relative to this file."))
            else:
                targets.add(resolved)
    return targets


def check_steps(path: Path, lines: list[str], start: int, out: list[Finding]) -> None:
    body = lines[start:]
    heading = next((i for i, l in enumerate(body) if l.strip().lower() == "## steps"), None)
    if heading is None:
        out.append(Finding(path, start + 1, "error", "S001", "no '## Steps' section. Fix: add one; every non-reference skill lists its steps there."))
        return
    steps: list[tuple[int, list[str]]] = []
    for i in range(heading + 1, len(body)):
        line = body[i]
        if line.startswith("## "):
            break
        if STEP_RE.match(line):
            steps.append((start + i + 1, [line]))
        elif steps:
            steps[-1][1].append(line)
    if not steps:
        out.append(Finding(path, start + heading + 1, "error", "S002", "'## Steps' has no numbered steps. Fix: write them as '1. ...'."))
    for number, text in steps:
        if "done when" not in " ".join(text).lower():
            out.append(Finding(path, number, "error", "S003", "step has no completion criterion. Fix: end it with 'Done when: <observable condition>'."))


def lint_skill(skill_dir: Path, names: set[str], avoid: list[tuple[str, str]], root: Path) -> list[Finding]:
    out: list[Finding] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists() and (skill_dir / "README.md").exists():
        return lint_shared(skill_dir, avoid, root)
    if not skill_md.exists():
        return [Finding(skill_dir, 1, "error", "F000", "folder has no SKILL.md. Fix: add one, or a README.md for a shared folder that is not a skill, or remove the folder.")]
    lines = skill_md.read_text(encoding="utf-8").splitlines()
    fm = parse_frontmatter(lines, skill_md, out)

    if fm is not None:
        line_of = lambda key: fm.lines.get(key, 1)  # noqa: E731
        for key in fm.fields:
            if key not in TOP_LEVEL_KEYS:
                out.append(Finding(skill_md, line_of(key), "error", "F003", f"unknown frontmatter key {key!r}. Fix: move it under metadata, or check the spelling."))
        name = fm.fields.get("name", "")
        if not name:
            out.append(Finding(skill_md, 1, "error", "F004", "missing name. Fix: add 'name: <folder name>'."))
        elif name != skill_dir.name:
            out.append(Finding(skill_md, line_of("name"), "error", "F005", f"name {name!r} differs from folder {skill_dir.name!r}. Fix: make them equal."))
        elif not NAME_RE.match(name) or len(name) > NAME_MAX:
            out.append(Finding(skill_md, line_of("name"), "error", "F006", f"name {name!r} is not lowercase-hyphenated or exceeds {NAME_MAX} chars."))
        description = fm.fields.get("description", "")
        if not description:
            out.append(Finding(skill_md, 1, "error", "F007", "missing description. Fix: one line on what the skill does."))
        elif len(description) > DESCRIPTION_MAX:
            out.append(Finding(skill_md, line_of("description"), "error", "F008", f"description is {len(description)} chars. Fix: cut it under {DESCRIPTION_MAX}."))
        for other in sorted(names - {skill_dir.name}):
            if re.search(rf"(?<![\w-]){re.escape(other)}(?![\w-])", description):
                out.append(Finding(skill_md, line_of("description"), "error", "F009", f"description names the skill {other!r}. Fix: declare the edge in metadata.calls; descriptions name no other skill."))
        invocation = fm.fields.get("disable-model-invocation")
        if invocation not in {"true", "false"}:
            out.append(Finding(skill_md, line_of("disable-model-invocation"), "error", "F010", "disable-model-invocation must be true or false. Fix: set it explicitly; internal nodes use true."))
        kind = fm.metadata.get("kind", "")
        if kind not in KINDS:
            out.append(Finding(skill_md, line_of("metadata.kind"), "error", "F011", f"metadata.kind is {kind!r}. Fix: use one of {', '.join(sorted(KINDS))}."))
        if not fm.metadata.get("hypothesis", "").strip():
            out.append(Finding(skill_md, line_of("metadata"), "error", "F012", "missing metadata.hypothesis. Fix: state the model weakness this skill compensates for, so it can be removed when the weakness is gone."))
        calls = split_list(fm.metadata.get("calls", ""))
        reads = split_list(fm.metadata.get("reads", ""))
        for call in calls:
            if call.startswith("repo:"):
                if not NAME_RE.match(re.sub(r"<[a-z]+>", "x", call[5:])):
                    out.append(Finding(skill_md, line_of("metadata.calls"), "error", "F013", f"bad target-repo skill {call!r}. Fix: write 'repo:<skill-name>'."))
            elif call not in names:
                out.append(Finding(skill_md, line_of("metadata.calls"), "error", "F013", f"metadata.calls names {call!r}, which is not a skill here. Fix: create it, fix the name, or prefix a target-repo skill with 'repo:'."))
        for read in reads:
            if read not in names:
                out.append(Finding(skill_md, line_of("metadata.reads"), "error", "F013", f"metadata.reads names {read!r}, which is not a skill here. Fix: fix the name, or drop it."))
        if kind and kind != "reference":
            check_steps(skill_md, lines, fm.body_start, out)
        words = len(re.findall(r"\S+", "\n".join(lines[fm.body_start:])))
        if words > WORD_BUDGET:
            out.append(Finding(skill_md, 1, "warning", "W001", f"SKILL.md body has {words} words, over the {WORD_BUDGET} budget. Fix: move reference material to references/."))

    linked: set[Path] = set()
    for md in sorted(skill_dir.rglob("*.md")):
        md_lines = md.read_text(encoding="utf-8").splitlines() if md != skill_md else lines
        is_glossary = md.resolve() == (root / GLOSSARY).resolve()
        check_prose(md, md_lines, avoid, is_glossary, out)
        linked |= check_links(md, md_lines, out)
    references = skill_dir / "references"
    if references.is_dir():
        for ref in sorted(references.rglob("*")):
            if ref.is_file() and ref.resolve() not in linked:
                out.append(Finding(ref, 1, "error", "L002", "orphan reference: no file in this skill links to it. Fix: link it from SKILL.md with the condition for reading it, or delete it."))
    if fm is not None:
        check_edges(skill_dir, skill_md, fm, calls, reads, linked, out)
    return out


def check_edges(skill_dir: Path, skill_md: Path, fm: "Frontmatter", calls: list[str], reads: list[str], linked: set[Path], out: list[Finding]) -> None:
    """The graph in metadata matches the links: skills route by path (pstack), so a declared call
    is a link to that skill's SKILL.md, and every link into another skill is a declared edge."""
    skills_root = skill_dir.parent.resolve()
    linked_skills: dict[str, set[str]] = {}
    for target in linked:
        try:
            rel = target.relative_to(skills_root)
        except ValueError:
            continue
        other = rel.parts[0]
        if other == skill_dir.name or not (skills_root / other / "SKILL.md").exists():  # shared folders need no edge
            continue
        linked_skills.setdefault(other, set()).add(rel.as_posix())
    for other, files in sorted(linked_skills.items()):
        if other in calls:
            continue
        if f"{other}/SKILL.md" in files:
            out.append(Finding(skill_md, fm.lines.get("metadata.calls", 1), "error", "F014", f"links to the skill {other!r} but metadata.calls does not declare it. Fix: add it to metadata.calls."))
        elif other not in reads:
            out.append(Finding(skill_md, fm.lines.get("metadata", 1), "error", "F014", f"links to files of the skill {other!r} ({', '.join(sorted(files))}) but declares no edge. Fix: add it to metadata.reads, or to metadata.calls if it runs that skill."))
    own_lines = skill_md.read_text(encoding="utf-8")
    for call in calls:
        if call.startswith("repo:") or call not in {p.name for p in skills_root.iterdir() if p.is_dir()}:
            continue
        if f"../{call}/SKILL.md" not in own_lines:
            out.append(Finding(skill_md, fm.lines.get("metadata.calls", 1), "error", "F015", f"metadata.calls declares {call!r} but SKILL.md never links ../{call}/SKILL.md. Fix: link the skill where a step runs it; skills are read by path, not found by name."))


def split_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def lint_shared(folder: Path, avoid: list[tuple[str, str]], root: Path) -> list[Finding]:
    """A shared folder (README.md, no SKILL.md) holds rules every skill reads by path. No harness lists it,
    so it has no frontmatter; its prose and links follow the same rules as a skill's."""
    out: list[Finding] = []
    readme = folder / "README.md"
    lines = readme.read_text(encoding="utf-8").splitlines()
    if lines and lines[0].strip() == "---":
        out.append(Finding(readme, 1, "error", "F016", "a shared folder's README.md has frontmatter, so a harness may list it as a skill. Fix: remove the frontmatter, or rename the file SKILL.md if it is a skill."))
    linked: set[Path] = set()
    for md in sorted(folder.rglob("*.md")):
        md_lines = md.read_text(encoding="utf-8").splitlines()
        check_prose(md, md_lines, avoid, md.resolve() == (root / GLOSSARY).resolve(), out)
        linked |= check_links(md, md_lines, out)
    references = folder / "references"
    if references.is_dir():
        for ref in sorted(references.rglob("*")):
            if ref.is_file() and ref.resolve() not in linked:
                out.append(Finding(ref, 1, "error", "L002", "orphan reference: no file in this folder links to it. Fix: link it from README.md with the condition for reading it, or delete it."))
    return out


def lint(root: Path) -> list[Finding]:
    skills_root = root / "skills"
    if not skills_root.is_dir():
        return [Finding(skills_root, 1, "error", "R001", "no skills/ folder.")]
    dirs = sorted(p for p in skills_root.iterdir() if p.is_dir())
    names = {p.name for p in dirs if (p / "SKILL.md").exists()}
    avoid = load_avoid_terms(root)
    findings: list[Finding] = []
    for skill_dir in dirs:
        findings.extend(lint_skill(skill_dir, names, avoid, root))
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Lint the framework's skills.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent, help="framework root (default: this repo)")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    findings = lint(root)
    for finding in findings:
        print(finding.render(root))
    errors = sum(f.level == "error" for f in findings)
    warnings = len(findings) - errors
    skills = len([p for p in (root / "skills").glob("*/SKILL.md")]) if (root / "skills").is_dir() else 0
    print(f"{skills} skill(s), {errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
