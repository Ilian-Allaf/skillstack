"""Run the rule tests of every language pack in skills/constitution/lint/.

Usage: python -I tools/run_lint_packs.py

Each pack's tests run on Node, in a copy of the pack under tools/.cache/ (ignored by git), so its
installed tools never sit inside skills/, which the linters scan.
Without a Node its tools support, the step is skipped with a warning on a laptop and fails in CI,
where CI is set. Exit code: 0 when every suite passes or is skipped, 1 otherwise.
"""

from __future__ import annotations

import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = ROOT / "tools" / ".cache" / "lint-packs"
SPEC = importlib.util.spec_from_file_location("lint_diff", ROOT / "skills/constitution/lint/lint_diff.py")
LINT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LINT  # dataclasses look their module up there
SPEC.loader.exec_module(LINT)


def main() -> int:
    node, npm = shutil.which("node"), shutil.which("npm")
    failed = []
    for language, pack in sorted(LINT.load_packs().items()):
        version = subprocess.run([node, "--version"], capture_output=True, text=True).stdout.strip() if node else ""
        if not (node and npm and LINT.node_supported(version, pack["node"])):
            wanted = " or ".join(f"{m}+" for m in pack["node"])
            reason = f"the {language} pack needs Node {wanted}, found {version or 'no node'}"
            if os.environ.get("CI"):
                print(f"FAILED: {reason}. Fix: set up that Node in the workflow.")
                failed.append(language)
            else:
                print(f"SKIPPED: {reason}. CI runs these tests; to run them here, upgrade Node.js.")
            continue
        folder = WORK / language
        manifest = (pack["dir"] / "package.json").read_bytes()
        if not (folder / "package.json").is_file() or (folder / "package.json").read_bytes() != manifest:
            shutil.rmtree(folder, ignore_errors=True)
            folder.mkdir(parents=True)
            (folder / "package.json").write_bytes(manifest)
            install = subprocess.run([npm, "install", "--no-audit", "--no-fund", "--no-package-lock"], cwd=folder)
            if install.returncode != 0:
                failed.append(language)
                continue
        # The pack's files, fresh each run; node_modules stays.
        shutil.rmtree(folder / "plugin", ignore_errors=True)
        shutil.copytree(pack["dir"] / "plugin", folder / "plugin")
        shutil.copy2(pack["dir"] / "run-tests.mjs", folder / "run-tests.mjs")
        if subprocess.run([npm, "test", "--silent"], cwd=folder).returncode != 0:
            failed.append(language)
    if failed:
        print("FAILED packs: " + ", ".join(failed))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
