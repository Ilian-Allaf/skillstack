"""Run every check of the framework: the tests of the tools, the skill linter, and the reference checker.

Usage: python -I tools/check.py

Exit code: 0 when everything passes, 1 otherwise. This is the one command to run before a commit,
and the one CI runs.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
STEPS = [
    ("tests of the tools", [sys.executable, "-I", "-m", "unittest", "discover", "-s", str(TOOLS)]),
    ("skill linter", [sys.executable, "-I", str(TOOLS / "lint_skills.py")]),
    ("reference checker", [sys.executable, "-I", str(TOOLS / "check_refs.py")]),
]


def main() -> int:
    failed = []
    for name, command in STEPS:
        print(f"== {name}", flush=True)
        if subprocess.run(command).returncode != 0:
            failed.append(name)
    print()
    if failed:
        print("FAILED: " + ", ".join(failed))
        return 1
    print("All checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
