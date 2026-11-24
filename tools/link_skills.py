"""Link this repo's skills into the folders where harnesses look for a user's skills.

Usage: python -I tools/link_skills.py [--dest DIR ...] [--dry-run] [--unlink] [--quiet]
       python -I tools/link_skills.py --install-hook | --remove-hook

Each skill folder of skills/ (one with a SKILL.md), and each shared folder (one with a README.md,
such as constitution/), gets a link of the same name in every destination:
  - ~/.agents/skills: Codex and the other harnesses that read the Agent Skills convention;
  - ~/.claude/skills: Claude Code, which does not read ~/.agents/.
The links point into this repo, so a `git pull` updates every installed skill. Run it again after
adding, removing, or renaming a skill, or install the hook once so it never needs a manual run:

  --install-hook writes post-merge and post-checkout hooks into the clone's git hooks, so every
  pull, merge, or checkout re-runs the linking and a skill added or renamed since the last run
  is linked without a command. The hook links the main clone (the parent of the git common dir),
  never a temporary worktree, prints only changes, and never blocks the git operation.
  --remove-hook deletes those hooks.

Shared folders sit beside the skills because skills read them by relative path
(`../constitution/README.md`); they have no SKILL.md, so no harness lists them.

On Windows, a directory symlink needs Developer Mode or admin rights; without them, a junction is
made instead, which works the same for reading.

Safe by construction: an existing link is replaced, a real folder of the same name is never
touched (it is reported, and left as it is), and a destination that is itself a link into this
repo is refused, so the links never land inside skills/.

Exit code: 0 when every link is in place, 1 when a name was skipped or a destination refused,
2 on bad usage. Standard library only.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DESTS = [Path.home() / ".agents" / "skills", Path.home() / ".claude" / "skills"]


def sources(repo: Path) -> list[Path]:
    """The folders to link: every skill, and every shared folder skills read by path."""
    root = repo / "skills"
    return sorted(p for p in root.iterdir() if p.is_dir() and ((p / "SKILL.md").exists() or (p / "README.md").exists()))


def link_target(path: Path) -> Path | None:
    """Where a symlink or a junction points, or None when the path is not a link."""
    try:
        raw = os.readlink(path)
    except (OSError, ValueError):
        return None
    if raw.startswith("\\\\?\\"):  # a Windows junction reads back with the extended-path prefix
        raw = raw[4:]
    return Path(os.path.realpath(raw))


def inside(path: Path, folder: Path) -> bool:
    try:
        path.resolve().relative_to(folder.resolve())
        return True
    except ValueError:
        return False


def make_link(src: Path, dst: Path) -> str:
    try:
        os.symlink(src, dst, target_is_directory=True)
        return "symlink"
    except OSError:
        if os.name != "nt":
            raise
        import _winapi  # Windows only: a junction needs no privilege

        _winapi.CreateJunction(str(src), str(dst))
        return "junction"


def remove_link(path: Path) -> None:
    # A directory symlink or a junction on Windows is removed with rmdir; elsewhere with unlink.
    if os.name == "nt":
        os.rmdir(path)
    else:
        os.unlink(path)


def run(repo: Path, dests: list[Path], dry_run: bool = False, unlink: bool = False, quiet: bool = False) -> list[str]:
    """Link (or unlink) every source into every destination. Returns the problems found."""
    problems: list[str] = []
    for dest in dests:
        if link_target(dest) is not None and inside(dest, repo):
            problems.append(f"{dest} is a link into this repo; links made there would land inside skills/. Fix: remove it (it is only a link) and run again.")
            continue
        if not dry_run and not unlink:
            dest.mkdir(parents=True, exist_ok=True)
        for src in sources(repo):
            dst = dest / src.name
            current = link_target(dst)
            if unlink:
                if current is not None and inside(current, repo):
                    print(f"unlink {dst}")
                    if not dry_run:
                        remove_link(dst)
                continue
            if current is not None:
                if current == src.resolve():
                    if not quiet:
                        print(f"ok      {dst}")
                    continue
                print(f"replace {dst} (was a link to {current})")
                if not dry_run:
                    remove_link(dst)
            elif dst.exists():
                problems.append(f"{dst} is a real folder, not a link; left as it is. Fix: move it away, then run again.")
                continue
            if dry_run:
                print(f"link    {dst} -> {src}")
            else:
                kind = make_link(src, dst)
                print(f"link    {dst} -> {src} ({kind})")
    return problems


HOOK_NAMES = ("post-merge", "post-checkout")
HOOK_PLACEHOLDER = "__LINK_SKILLS__"
# The hook runs in Git Bash on Windows and in sh elsewhere, so it is always written with LF.
# The fallback without --quiet keeps the hook working while the clone still has an older tool.
HOOK_TEMPLATE = (
    "#!/bin/sh\n"
    "# Installed by `python -I tools/link_skills.py --install-hook` as post-merge and post-checkout.\n"
    "# Re-links the user-level skills after a pull, merge, or checkout, so a skill added or\n"
    "# renamed in this clone needs no manual run. The links point at the main clone, never at\n"
    "# a temporary worktree, and a failure here never blocks the git operation.\n"
    'python -I "' + HOOK_PLACEHOLDER + '" --quiet || python -I "' + HOOK_PLACEHOLDER + '" || true\n'
)


def git_common_dir(repo: Path) -> Path | None:
    """The common git dir of the clone, or None when repo is not inside a git clone."""
    for extra in (["--path-format=absolute"], []):
        result = subprocess.run(["git", "-C", str(repo), "rev-parse", *extra, "--git-common-dir"], capture_output=True, text=True)
        if result.returncode == 0:
            return Path(result.stdout.strip())
    return None


def install_hook(repo: Path) -> list[str]:
    """Write the re-linking hooks into the clone's hooks dir. Returns the problems found."""
    common = git_common_dir(repo)
    if common is None:
        return [f"{repo} is not a git clone (git rev-parse failed). Fix: run --install-hook from a clone of this repo."]
    main = common.parent if common.name == ".git" else common
    script = (main / "tools" / "link_skills.py").as_posix()
    content = HOOK_TEMPLATE.replace(HOOK_PLACEHOLDER, script)
    hooks_dir = common / "hooks"
    hooks_dir.mkdir(parents=True, exist_ok=True)
    for name in HOOK_NAMES:
        path = hooks_dir / name
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
        if os.name != "nt":
            path.chmod(0o755)
    return []


def remove_hook(repo: Path) -> list[str]:
    """Delete the hooks installed by install_hook, and only those. Returns the problems found."""
    common = git_common_dir(repo)
    if common is None:
        return [f"{repo} is not a git clone (git rev-parse failed). Fix: delete post-merge and post-checkout from the clone's hooks by hand."]
    for name in HOOK_NAMES:
        path = common / "hooks" / name
        if path.is_file() and "link_skills.py" in path.read_text(encoding="utf-8"):
            path.unlink()
    return []


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Link this repo's skills into the harnesses' skill folders.")
    parser.add_argument("--dest", type=Path, action="append", help="a destination folder (repeatable; default: ~/.agents/skills and ~/.claude/skills)")
    parser.add_argument("--dry-run", action="store_true", help="say what would change, change nothing")
    parser.add_argument("--unlink", action="store_true", help="remove the links that point into this repo")
    parser.add_argument("--quiet", action="store_true", help="print only changes and errors, not the links already in place")
    parser.add_argument("--install-hook", action="store_true", help="install post-merge and post-checkout hooks that re-link after every pull, merge, or checkout; links now too")
    parser.add_argument("--remove-hook", action="store_true", help="remove the hooks installed by --install-hook")
    args = parser.parse_args(argv)
    problems: list[str] = []
    if args.remove_hook:
        problems += remove_hook(REPO)
    elif args.install_hook:
        problems += install_hook(REPO)
    if not args.remove_hook:
        problems += run(REPO, args.dest or DEFAULT_DESTS, args.dry_run, args.unlink, args.quiet)
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
