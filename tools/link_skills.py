"""Link this repo's skills into the folders where harnesses look for a user's skills.

Usage: python -I tools/link_skills.py [--dest DIR ...] [--dry-run] [--unlink]

Each skill folder of skills/ (one with a SKILL.md), and each shared folder (one with a README.md,
such as constitution/), gets a link of the same name in every destination:
  - ~/.agents/skills: Codex and the other harnesses that read the Agent Skills convention;
  - ~/.claude/skills: Claude Code, which does not read ~/.agents/.
The links point into this repo, so a `git pull` updates every installed skill. Run it again after
adding, removing, or renaming a skill. Shared folders sit beside the skills because skills read
them by relative path (`../constitution/README.md`); they have no SKILL.md, so no harness lists them.

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


def run(repo: Path, dests: list[Path], dry_run: bool = False, unlink: bool = False) -> list[str]:
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Link this repo's skills into the harnesses' skill folders.")
    parser.add_argument("--dest", type=Path, action="append", help="a destination folder (repeatable; default: ~/.agents/skills and ~/.claude/skills)")
    parser.add_argument("--dry-run", action="store_true", help="say what would change, change nothing")
    parser.add_argument("--unlink", action="store_true", help="remove the links that point into this repo")
    args = parser.parse_args(argv)
    problems = run(REPO, args.dest or DEFAULT_DESTS, args.dry_run, args.unlink)
    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
