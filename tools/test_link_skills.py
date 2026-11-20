"""Tests for link_skills.py. Run: python -I -m unittest discover -s tools -v"""

from __future__ import annotations

import contextlib
import io
import os
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


if __name__ == "__main__":
    unittest.main()
