"""Run the lint pass of the framework's language rules on the lines a change adds or edits.

Usage, from the root of the target repo:
  python -I <this file> --base <ref>          the diff against the base, working tree and new files included
  python -I <this file> --all                 every file of the repo, findings counted per rule, for setup-repo
  python -I <this file> --export <dir>        the built plugin and its license, for a repo that shares the rules
Options: --language <name> (default: every pack the diff touches), --project-folder <path>
(default: ~/.agents/projects/<project>/, named as constitution/references/target-repo.md says).

Each folder beside this file with a pack.json is a language pack: its rule ids, its checks, and the
plugin that holds them. The user's decisions live in <project folder>/lint/<language>.md, read as
constitution/references/lint.md says. The tools install once, outside every repo, in
~/.agents/cache/lint/.

Exit code: 0 when nothing blocks, 1 when a blocking finding remains, 2 when the pass could not run;
the message then says why and how to fix it.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".agents" / "cache" / "lint"
ROUTE = re.compile(r"^This lives in the repo at (\S+?)\.? Read it there instead\.?$")
CODE = re.compile(r"^([\w@/-]+)\((.+)\)$")
HUNK = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
DECISIONS = {"on", "off"}


class PassError(Exception):
    """The pass cannot run; the message says how to fix it."""


@dataclass
class Entry:
    path: Path
    kind: str  # missing, route, off, private
    decisions: dict[str, str] = field(default_factory=dict)
    exceptions: list[tuple[str, str]] = field(default_factory=list)
    route: str = ""


@dataclass
class Finding:
    file: str
    line: int
    rule: str  # the rule id of the language file
    message: str
    blocking: bool


# ---------- the project folder and the user's decisions ----------


def git(repo: Path, *args: str) -> str:
    run = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True, encoding="utf-8")
    if run.returncode != 0:
        raise PassError(f"git {' '.join(args)} failed: {run.stderr.strip()}. Fix: run from the target repo, with the base fetched.")
    return run.stdout


def project_name(remote: str, common_dir: str) -> str:
    """target-repo.md: the remote's path after the host, without .git, lowercase, '/' as '__';
    without a remote, the folder that holds the main checkout."""
    remote = remote.strip()
    if remote:
        path = re.sub(r"^[a-z+]+://[^/]+/", "", remote)
        if path == remote:
            path = remote.split(":", 1)[-1]
        path = re.sub(r"\.git/?$", "", path.strip("/"))
        return path.lower().replace("/", "__")
    return Path(common_dir.strip()).parent.name.lower()


def project_folder(repo: Path) -> Path:
    remote = subprocess.run(["git", "remote", "get-url", "origin"], cwd=repo, capture_output=True, text=True).stdout
    common = git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path.home() / ".agents" / "projects" / project_name(remote, common)


def cells(line: str) -> list[str]:
    return [c.strip().strip("`").strip() for c in line.strip().strip("|").split("|")]


def parse_entry(path: Path, text: str | None) -> Entry:
    """Read lint/<language>.md: a route, or a Pass line, a Rules table, and an Exceptions table."""
    if text is None:
        return Entry(path, "missing")
    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) == 1 and (match := ROUTE.match(lines[0].strip())):
        return Entry(path, "route", route=match.group(1))
    entry = Entry(path, "")
    section = ""
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            section = stripped.lstrip("#").strip().lower()
            continue
        if match := re.match(r"^pass:\s*(\w+)", stripped, re.IGNORECASE):
            entry.kind = match.group(1).lower()
            continue
        if not stripped.startswith("|") or set(stripped) <= set("|-: "):
            continue
        row = cells(stripped)
        if row[0].lower() in {"rule", "id"}:
            continue
        if section == "rules" and len(row) >= 2:
            decision = row[1].lower()
            if decision not in DECISIONS:
                raise PassError(f"{path}: rule {row[0]!r} has decision {row[1]!r}. Fix: write on or off.")
            entry.decisions[row[0]] = decision
        elif section == "exceptions" and len(row) >= 2:
            entry.exceptions.append((row[0], row[1]))
    if entry.kind not in {"private", "off"}:
        raise PassError(f"{path}: no 'Pass: private' or 'Pass: off' line. Fix: add one, as constitution/references/lint.md shows.")
    return entry


def read_entry(folder: Path, language: str) -> Entry:
    path = folder / "lint" / f"{language}.md"
    return parse_entry(path, path.read_text(encoding="utf-8") if path.is_file() else None)


# ---------- the diff ----------


def parse_diff(text: str) -> dict[str, dict[int, str]]:
    """The added and edited lines of a unified diff with no context, by file: line number to text."""
    out: dict[str, dict[int, str]] = {}
    current: dict[int, str] | None = None
    number = 0
    for line in text.splitlines():
        if line.startswith("+++ "):
            target = line[4:].strip()
            current = None if target == "/dev/null" else out.setdefault(target[2:] if target.startswith("b/") else target, {})
        elif match := HUNK.match(line):
            number = int(match.group(1))
        elif current is not None and line.startswith("+"):
            current[number] = line[1:]
            number += 1
    return out


def changed_lines(repo: Path, base: str) -> dict[str, dict[int, str] | None]:
    """Lines added or edited since the merge base, working tree included; None means the whole file is new."""
    merge_base = git(repo, "merge-base", base, "HEAD").strip()
    diff = git(repo, "diff", "-U0", "--no-color", "--no-ext-diff", "--diff-filter=AMR", merge_base, "--")
    out: dict[str, dict[int, str] | None] = dict(parse_diff(diff))
    for name in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
        out[name.strip()] = None
    return out


# ---------- the pack and its tools ----------


def load_packs() -> dict[str, dict]:
    packs = {}
    for manifest in sorted(HERE.glob("*/pack.json")):
        pack = json.loads(manifest.read_text(encoding="utf-8"))
        pack["dir"] = manifest.parent
        packs[pack["language"]] = pack
    return packs


def node_supported(version: str, minimums: list[str]) -> bool:
    """'v22.12.0' against ['20.19', '22.12']: each minimum covers its major; majors above the last are fine."""
    major, minor = (int(part) for part in version.lstrip("v").split(".")[:2])
    floors = [tuple(int(p) for p in m.split(".")) for m in minimums]
    if major > floors[-1][0]:
        return True
    return any(major == fmajor and minor >= fminor for fmajor, fminor in floors)


def tool(name: str) -> str:
    found = shutil.which(name)
    if not found:
        raise PassError(f"{name} is not on the PATH. Fix: install Node.js, which brings node and npm.")
    return found


def pack_hash(pack: dict) -> str:
    digest = hashlib.sha256()
    for path in sorted([pack["dir"] / "package.json", *(pack["dir"] / "plugin").rglob("*.ts")]):
        digest.update(path.relative_to(pack["dir"]).as_posix().encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()[:12]


def ensure_tools(pack: dict) -> Path:
    """Install the pack's pinned tools and build its plugin once, in the cache, keyed by the pack's content."""
    node = tool("node")
    version = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip()
    if not node_supported(version, pack["node"]):
        wanted = " or ".join(f"{m}+" for m in pack["node"])
        raise PassError(f"Node {version} is too old for the {pack['language']} pack, whose tools need Node {wanted}. Fix: upgrade Node.js, then run again.")
    home = CACHE / f"{pack['language']}-{pack_hash(pack)}"
    if (home / ".ready").is_file():
        return home
    if home.exists():
        shutil.rmtree(home)
    shutil.copytree(pack["dir"] / "plugin", home / "plugin", ignore=shutil.ignore_patterns("*.test.ts"))
    shutil.copy2(pack["dir"] / "package.json", home / "package.json")
    shutil.copy2(pack["dir"] / "LICENSE", home / "LICENSE")
    steps = [
        [tool("npm"), "install", "--omit=dev", "--no-audit", "--no-fund", "--no-package-lock"],
        [node, "node_modules/esbuild/bin/esbuild", pack["plugin"]["entry"], "--bundle", "--format=esm", "--platform=node",
         "--external:@oxlint/plugins", "--outfile=dist/plugin.mjs", "--log-level=warning"],
        [node, "node_modules/oxlint/bin/oxlint", "--version"],
    ]
    for step in steps:
        run = subprocess.run(step, cwd=home, capture_output=True, text=True, encoding="utf-8", errors="replace")
        if run.returncode != 0:
            raise PassError(f"installing the {pack['language']} tools failed at `{' '.join(step[1:3])}`: {(run.stderr or run.stdout).strip()[-600:]}. Fix: read the error; delete {home} and run again.")
    (home / ".ready").write_text("ok\n", encoding="utf-8")
    return home


def levels(pack: dict, entry: Entry, everything: bool) -> tuple[dict[str, str], set[str]]:
    """The level of each check: error when decided on, warn when not decided yet, absent when off."""
    out: dict[str, str] = {}
    undecided: set[str] = set()
    for rule, checks in pack["rules"].items():
        decision = "on" if everything else entry.decisions.get(rule)
        if decision == "off":
            continue
        if decision is None:
            undecided.add(rule)
        for check in checks:
            out[check] = "error" if decision == "on" else "warn"
    return out, undecided


def build_config(pack: dict, check_levels: dict[str, str], plugin: Path) -> dict:
    off = {name: "off" for name in ["correctness", "suspicious", "pedantic", "perf", "style", "restriction", "nursery"]}
    rules = {check: [level, pack["options"][check]] if check in pack.get("options", {}) else level for check, level in check_levels.items()}
    return {
        "categories": off,
        "jsPlugins": [{"name": pack["plugin"]["name"], "specifier": plugin.as_posix()}],
        "rules": rules,
    }


def check_of(code: str) -> str:
    """'typescript-rules(no-unknown-returns)' as 'typescript-rules/no-unknown-returns'."""
    match = CODE.match(code)
    return f"{match.group(1)}/{match.group(2)}" if match else code


def run_oxlint(home: Path, config: dict, repo: Path, targets: list[str]) -> list[dict]:
    config_path = home / "run-config.json"
    config_path.write_text(json.dumps(config, indent=2), encoding="utf-8")
    diagnostics: list[dict] = []
    for start in range(0, len(targets), 200):
        command = [tool("node"), str(home / "node_modules/oxlint/bin/oxlint"), "-c", str(config_path),
                   "--disable-nested-config", "--format", "json", *targets[start:start + 200]]
        run = subprocess.run(command, cwd=repo, capture_output=True, text=True, encoding="utf-8", errors="replace")
        try:
            diagnostics.extend(json.loads(run.stdout)["diagnostics"])
        except (json.JSONDecodeError, KeyError):
            raise PassError(f"oxlint gave no report: {(run.stderr or run.stdout).strip()[-600:]}. Fix: read the error; delete {home} and run again.")
    return diagnostics


# ---------- findings ----------


def rule_ids(pack: dict) -> dict[str, str]:
    return {check: rule for rule, checks in pack["rules"].items() for check in checks}


def to_findings(diagnostics: list[dict], pack: dict) -> list[Finding]:
    owners = rule_ids(pack)
    out = []
    for item in diagnostics:
        check = check_of(item.get("code", ""))
        label = (item.get("labels") or [{}])[0].get("span", {})
        out.append(Finding(item.get("filename", "").replace("\\", "/"), int(label.get("line", 0)), owners.get(check, check),
                           item.get("message", ""), item.get("severity") == "error"))
    return out


def keep(findings: list[Finding], changed: dict[str, dict[int, str] | None], exceptions: list[tuple[str, str]]) -> list[Finding]:
    """Only findings on added or edited lines, minus the user's exceptions."""
    out = []
    for finding in findings:
        lines = changed.get(finding.file, {})
        if lines is not None and finding.line not in lines:
            continue
        if any(rule == finding.rule and fnmatch.fnmatch(finding.file, pattern) for rule, pattern in exceptions):
            continue
        out.append(finding)
    return out


def suppressions(pack: dict, changed: dict[str, dict[int, str] | None], repo: Path) -> list[Finding]:
    """A disable comment that names a check of the pack, on an added line: exceptions live in the entry."""
    names = "|".join(re.escape(check) for check in rule_ids(pack))
    pattern = re.compile(rf"(?:eslint|oxlint)-disable[^\n]*?({names})")
    out = []
    for name, lines in changed.items():
        if not name.endswith(tuple(pack["extensions"])):
            continue
        if lines is None:
            path = repo / name
            text = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""
            lines = dict(enumerate(text.splitlines(), start=1))
        for number, text in lines.items():
            if match := pattern.search(text):
                rule = rule_ids(pack)[match.group(1)]
                out.append(Finding(name, number, rule, "a disable comment for a framework rule. Fix: remove it; an exception goes in the Exceptions table of the entry, with its reason.", True))
    return out


# ---------- modes ----------


def run_diff(repo: Path, base: str, folder: Path, languages: list[str], packs: dict[str, dict]) -> int:
    changed = changed_lines(repo, base)
    blocked = False
    for language in languages:
        pack = packs[language]
        targets = sorted(name for name in changed if name.endswith(tuple(pack["extensions"])) and (repo / name).is_file())
        if not targets:
            continue
        entry = read_entry(folder, language)
        if entry.kind == "missing":
            print(f"{language}: no decision in {entry.path}. The pass did not run. Fix: run /setup-repo, which asks whether to apply the {language} rules.")
            continue
        if entry.kind == "route":
            print(f"{language}: the rules are shared in the repo ({entry.route}); its own lint command applies them.")
            continue
        if entry.kind == "off":
            print(f"{language}: the pass is off for this repo ({entry.path}).")
            continue
        home = ensure_tools(pack)
        check_levels, undecided = levels(pack, entry, everything=False)
        findings = suppressions(pack, changed, repo)
        if check_levels:
            diagnostics = run_oxlint(home, build_config(pack, check_levels, home / "dist/plugin.mjs"), repo, targets)
            findings += keep(to_findings(diagnostics, pack), changed, entry.exceptions)
        for finding in sorted(findings, key=lambda f: (f.file, f.line)):
            tag = "blocking" if finding.blocking else "not decided"
            print(f"{finding.file}:{finding.line}: [{tag}] {finding.rule}: {finding.message}")
        blocking = sum(f.blocking for f in findings)
        pending = sorted({f.rule for f in findings if not f.blocking})
        print(f"{language}: {len(targets)} file(s), {blocking} blocking finding(s), {len(findings) - blocking} on rules not decided yet.")
        if pending:
            print(f"Rules not decided yet in {entry.path}: {', '.join(pending)}. Fix: the user writes on or off for each; until then they do not block.")
        elif undecided:
            print(f"Rules not decided yet, with no finding here: {', '.join(sorted(undecided))}.")
        blocked |= blocking > 0
    return 1 if blocked else 0


def run_all(repo: Path, languages: list[str], packs: dict[str, dict]) -> int:
    for language in languages:
        pack = packs[language]
        home = ensure_tools(pack)
        check_levels, _ = levels(pack, Entry(Path(), "private"), everything=True)
        findings = [f for f in to_findings(run_oxlint(home, build_config(pack, check_levels, home / "dist/plugin.mjs"), repo, ["."]), pack)
                    if f.file.endswith(tuple(pack["extensions"]))]
        print(f"{language}: findings per rule over the whole repo")
        for rule in pack["rules"]:
            hits = [f for f in findings if f.rule == rule]
            print(f"  {rule}: {len(hits)} finding(s) in {len({f.file for f in hits})} file(s)")
    return 0


def run_export(out_dir: Path, languages: list[str], packs: dict[str, dict]) -> int:
    for language in languages:
        pack = packs[language]
        home = ensure_tools(pack)
        target = out_dir / pack["plugin"]["name"]
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(home / "dist/plugin.mjs", target / "index.mjs")
        shutil.copy2(home / "LICENSE", target / "LICENSE")
        version = json.loads((pack["dir"] / "package.json").read_text(encoding="utf-8"))["dependencies"]["@oxlint/plugins"]
        print(f"{language}: wrote {target / 'index.mjs'} and its LICENSE.")
        print(f"  It imports @oxlint/plugins: add it to the repo's dev dependencies at exactly {version}.")
        prefix = pack["plugin"]["name"] + "/"
        checks = [c for cs in pack["rules"].values() for c in cs]
        print(f"  Register it as the plugin {pack['plugin']['name']!r}; its checks: {', '.join(c for c in checks if c.startswith(prefix))}.")
        native = [c for c in checks if not c.startswith(prefix)]
        if native:
            print(f"  Built into Oxlint, not in the plugin: {', '.join(native)}. Turn them on where the repo runs Oxlint; ESLint has no built-in equivalent.")
        if pack.get("options"):
            print(f"  Options: {json.dumps(pack['options'])}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the framework's language rules on the lines a change touches.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--base", help="the base ref of the change")
    mode.add_argument("--all", action="store_true", help="count findings per rule over the whole repo")
    mode.add_argument("--export", type=Path, help="write the built plugin to this folder")
    parser.add_argument("--language", action="append", help="a pack to run (default: every pack)")
    parser.add_argument("--project-folder", type=Path, help="default: ~/.agents/projects/<project>/")
    parser.add_argument("--repo", type=Path, default=Path.cwd(), help="the target repo (default: the current folder)")
    args = parser.parse_args(argv)
    packs = load_packs()
    languages = args.language or sorted(packs)
    try:
        unknown = [name for name in languages if name not in packs]
        if unknown:
            raise PassError(f"no pack for {', '.join(unknown)}. Fix: use one of {', '.join(sorted(packs))}.")
        repo = args.repo.resolve()
        if args.export:
            return run_export(args.export.resolve(), languages, packs)
        if args.all:
            return run_all(repo, languages, packs)
        folder = args.project_folder or project_folder(repo)
        return run_diff(repo, args.base, folder, languages, packs)
    except PassError as error:
        print(f"lint pass could not run: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
