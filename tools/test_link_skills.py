"""Tests for link_skills.py. Run: python -I -m unittest discover -s tools -v"""

from __future__ import annotations

import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import link_skills  # noqa: E402


class LinkSkillsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        base = Path(self.tmp.name)
        self.repo = base / "repo"
        for rel in ("skills/ship/SKILL.md", "skills/verify-pr/SKILL.md", "skills/constitution/README.md", "skills/notes/draft.txt"):
            path = self.repo / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("x", encoding="utf-8")
        self.dest = base / "home" / ".agents" / "skills"

    def tearDown(self) -> None:
        for dst in self.dest.iterdir() if self.dest.is_dir() else []:
            if link_skills.link_target(dst) is not None:
                link_skills.remove_link(dst)
        self.tmp.cleanup()

    def run_tool(self, **kwargs) -> list[str]:
        with contextlib.redirect_stdout(io.StringIO()):
            return link_skills.run(self.repo, [self.dest], **kwargs)

    def run_tool_capture(self, **kwargs) -> tuple[list[str], str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            problems = link_skills.run(self.repo, [self.dest], **kwargs)
        return problems, out.getvalue()

    def test_links_every_skill_and_shared_folder(self) -> None:
        self.assertEqual(self.run_tool(), [])
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ["constitution", "ship", "verify-pr"])
        self.assertTrue((self.dest / "ship" / "SKILL.md").exists())
        self.assertEqual(link_skills.link_target(self.dest / "ship"), (self.repo / "skills" / "ship").resolve())

    def test_a_skill_reads_the_constitution_by_relative_path(self) -> None:
        self.run_tool()
        self.assertTrue((self.dest / "ship" / ".." / "constitution" / "README.md").exists())

    def test_second_run_changes_nothing(self) -> None:
        self.run_tool()
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(link_skills.run(self.repo, [self.dest]), [])
        self.assertNotIn("link ", out.getvalue())

    def test_real_folder_is_never_touched(self) -> None:
        (self.dest / "ship").mkdir(parents=True)
        (self.dest / "ship" / "mine.md").write_text("keep", encoding="utf-8")
        problems = self.run_tool()
        self.assertEqual(len(problems), 1)
        self.assertEqual((self.dest / "ship" / "mine.md").read_text(encoding="utf-8"), "keep")

    def test_stale_link_is_replaced(self) -> None:
        other = Path(self.tmp.name) / "old-ship"
        other.mkdir()
        self.dest.mkdir(parents=True)
        link_skills.make_link(other, self.dest / "ship")
        self.assertEqual(self.run_tool(), [])
        self.assertEqual(link_skills.link_target(self.dest / "ship"), (self.repo / "skills" / "ship").resolve())

    def test_destination_linked_into_the_repo_is_refused(self) -> None:
        self.dest.parent.mkdir(parents=True)
        link_skills.make_link(self.repo / "skills", self.dest)
        try:
            self.assertEqual(len(self.run_tool()), 1)
            self.assertFalse((self.repo / "skills" / "ship" / "ship").exists())
        finally:
            link_skills.remove_link(self.dest)

    @unittest.skipUnless(os.name == "nt", "junctions exist only on Windows")
    def test_junction_when_symlinks_are_refused(self) -> None:
        def refuse(*args, **kwargs):
            raise OSError("symlinks need Developer Mode")

        real = os.symlink
        os.symlink = refuse
        try:
            self.assertEqual(self.run_tool(), [])
        finally:
            os.symlink = real
        self.assertTrue((self.dest / "ship" / "SKILL.md").exists())
        self.assertEqual(link_skills.link_target(self.dest / "ship"), (self.repo / "skills" / "ship").resolve())
        self.assertEqual(self.run_tool(unlink=True), [])
        self.assertEqual(list(self.dest.iterdir()), [])

    def test_dry_run_changes_nothing(self) -> None:
        self.assertEqual(self.run_tool(dry_run=True), [])
        self.assertFalse(self.dest.exists())

    def test_unlink_removes_only_links_into_the_repo(self) -> None:
        self.run_tool()
        (self.dest / "mine").mkdir()
        self.assertEqual(self.run_tool(unlink=True), [])
        self.assertEqual(sorted(p.name for p in self.dest.iterdir()), ["mine"])
        self.assertTrue((self.repo / "skills" / "ship" / "SKILL.md").exists())

    def test_quiet_prints_only_changes(self) -> None:
        self.run_tool()
        problems, out = self.run_tool_capture(quiet=True)
        self.assertEqual(problems, [])
        self.assertNotIn("ok ", out)
        new_skill = self.repo / "skills" / "new-skill"
        new_skill.mkdir()
        (new_skill / "SKILL.md").write_text("x", encoding="utf-8")
        problems, out = self.run_tool_capture(quiet=True)
        self.assertEqual(problems, [])
        self.assertIn("new-skill", out)
        self.assertNotIn("ok ", out)


@unittest.skipUnless(shutil.which("git"), "git is required to install hooks")
class HookTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "repo"
        skill = self.repo / "skills" / "ship"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("x", encoding="utf-8")
        (self.repo / "tools").mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def hooks_dir(self) -> Path:
        return self.repo / ".git" / "hooks"

    def test_install_hook_writes_post_merge_and_post_checkout(self) -> None:
        self.assertEqual(self.install(self.repo), [])
        for name in ("post-merge", "post-checkout"):
            content = (self.hooks_dir() / name).read_text(encoding="utf-8")
            self.assertNotIn(link_skills.HOOK_PLACEHOLDER, content)
            self.assertIn("link_skills.py", content)
            self.assertIn("--quiet", content)
            self.assertNotIn("\r", content)

    def install(self, repo: Path, **kwargs) -> list[str]:
        with contextlib.redirect_stdout(io.StringIO()):
            return link_skills.install_hook(repo, **kwargs)

    def git(self, *args: str) -> None:
        subprocess.run(["git", "-C", str(self.repo), "-c", "user.name=t", "-c", "user.email=t@example.invalid", "-c", "commit.gpgsign=false", *args], check=True, capture_output=True)

    def test_installed_from_a_worktree_the_hook_points_at_the_main_clone(self) -> None:
        self.git("add", ".")
        self.git("commit", "-q", "-m", "base")
        worktree = Path(self.tmp.name) / "worktree"
        self.git("worktree", "add", "-q", "--detach", str(worktree))
        self.assertEqual(self.install(worktree), [])
        content = (self.hooks_dir() / "post-merge").read_text(encoding="utf-8")
        self.assertIn((self.repo / "tools" / "link_skills.py").as_posix(), content)
        self.assertNotIn(worktree.as_posix(), content)

    def test_a_hook_of_the_users_is_never_overwritten(self) -> None:
        self.hooks_dir().mkdir(parents=True, exist_ok=True)
        mine = "#!/bin/sh\necho mine\n"
        (self.hooks_dir() / "post-merge").write_text(mine, encoding="utf-8")
        problems = self.install(self.repo)
        self.assertEqual(len(problems), 1)
        self.assertIn("post-merge", problems[0])
        self.assertEqual((self.hooks_dir() / "post-merge").read_text(encoding="utf-8"), mine)
        self.assertIn("link_skills.py", (self.hooks_dir() / "post-checkout").read_text(encoding="utf-8"))

    def test_install_again_replaces_our_own_hook(self) -> None:
        self.assertEqual(self.install(self.repo), [])
        self.assertEqual(self.install(self.repo), [])

    def test_dry_run_writes_no_hook(self) -> None:
        self.assertEqual(self.install(self.repo, dry_run=True), [])
        for name in ("post-merge", "post-checkout"):
            self.assertFalse((self.hooks_dir() / name).exists())

    def test_remove_hook_deletes_only_our_hooks(self) -> None:
        self.install(self.repo)
        (self.hooks_dir() / "pre-push").write_text("#!/bin/sh\necho keep\n", encoding="utf-8")
        self.assertEqual(link_skills.remove_hook(self.repo), [])
        self.assertFalse((self.hooks_dir() / "post-merge").exists())
        self.assertFalse((self.hooks_dir() / "post-checkout").exists())
        self.assertTrue((self.hooks_dir() / "pre-push").exists())

    def test_remove_hook_without_hooks_is_ok(self) -> None:
        self.assertEqual(link_skills.remove_hook(self.repo), [])


class NotACloneTest(unittest.TestCase):
    def test_install_hook_outside_a_git_clone_reports_a_problem(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "plain" / "repo"
            repo.mkdir(parents=True)
            problems = link_skills.install_hook(repo)
        self.assertEqual(len(problems), 1)
        self.assertIn("not a git clone", problems[0])


if __name__ == "__main__":
    unittest.main()
