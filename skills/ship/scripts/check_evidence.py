"""Check a local evidence index, not the truth of its claims.

Usage: python -I check_evidence.py record.json --patch-id <full patch id> --base-sha <full base SHA> --head-sha <full head SHA>
Paths resolve from the record's directory. No network access or dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def check(record: object, root: Path, patch_id: str, base_sha: str, head_sha: str) -> list[str]:
    errors: list[str] = []

    def fail(where: str, fix: str) -> None:
        errors.append(f"{where}: Fix: {fix}")

    def present(value: object) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def artifact(value: object, where: str) -> None:
        if not present(value):
            fail(where, "supply a local artifact path")
            return
        try:
            path = root / value
            valid = path.is_file() and path.stat().st_size > 0
        except (OSError, ValueError):
            valid = False
        if not valid:
            fail(where, f"save a nonempty artifact at {value}")

    def rows(key: str, identity: str) -> list[dict]:
        values = record.get(key)
        if not isinstance(values, list) or not values:
            fail(key, "supply a nonempty list from the agreed case list or skill steps")
            return []
        seen = set()
        valid = []
        for index, row in enumerate(values):
            where = f"{key}[{index}]"
            if not isinstance(row, dict):
                fail(where, "supply an object")
                continue
            name = row.get(identity)
            if not present(name) or name in seen:
                fail(where, f"supply a unique nonempty {identity}")
            else:
                seen.add(name)
            valid.append(row)
        return valid

    if not isinstance(record, dict):
        return ["record: Fix: supply a JSON object"]
    current = {"patch_id": patch_id, "base_sha": base_sha, "head_sha": head_sha}
    for name, value in current.items():
        if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value):
            fail(name, f"compute and pass the full current {name}")
    cases = rows("cases", "id")
    if "spec_ids" in record:
        spec_ids = record["spec_ids"]
        if not isinstance(spec_ids, list) or not spec_ids:
            fail("spec_ids", "list the spec's story, promise, and visual target ids, such as S1, P1, and V1, or drop the key for a task without a spec")
            spec_ids = []
        case_ids = {row.get("id") for row in cases if isinstance(row.get("id"), str)}
        seen_spec = set()
        for spec_id in spec_ids:
            if not isinstance(spec_id, str) or not re.fullmatch(r"[SPV][0-9]+[a-z]?", spec_id) or spec_id in seen_spec:
                fail(f"spec id {spec_id!r}", "use each id once, as the spec numbers it: S1, S1b, P1, V1")
                continue
            seen_spec.add(spec_id)
            if spec_id not in case_ids:
                fail(f"spec id {spec_id}", f"add a case with id {spec_id}, with evidence or a not_verified reason")
    for row in cases:
        where = f"case {row.get('id')}"
        level = row.get("level")
        if type(level) is not int or not 1 <= level <= 5:
            fail(where, "set level to an integer from 1 to 5")
        evidence = row.get("evidence")
        if not isinstance(evidence, list):
            fail(where, "supply evidence as a list of local artifact paths")
        else:
            for path in evidence:
                artifact(path, where)
            if not evidence and not present(row.get("not_verified")):
                fail(where, "attach evidence or explain not_verified")
    for row in rows("steps", "name"):
        where = f"step {row.get('name')}"
        if row.get("status") not in ("done", "skip", "unverified"):
            fail(where, "set status to done, skip, or unverified")
        if not present(row.get("result")):
            fail(where, "record the result or the reason for skip or unverified")
        if row.get("status") == "done":
            artifact(row.get("trace"), where)
    required = record.get("required_artifacts")
    if not isinstance(required, list):
        fail("required_artifacts", "list required captures, or use an empty list when none apply")
    else:
        for path in required:
            artifact(path, "required_artifacts")
    verdict = record.get("verdict")
    if verdict is not None:
        if not isinstance(verdict, dict) or any(verdict.get(name) != value for name, value in current.items()):
            fail("verdict", "obtain a verdict for the current base SHA, head SHA, and patch id")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record", type=Path)
    parser.add_argument("--patch-id", required=True)
    parser.add_argument("--base-sha", required=True)
    parser.add_argument("--head-sha", required=True)
    args = parser.parse_args()
    try:
        record = json.loads(args.record.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"record: Fix: supply a readable JSON file ({exc})")
        return 1
    errors = check(record, args.record.resolve().parent, args.patch_id, args.base_sha, args.head_sha)
    for error in errors:
        print(error)
    if errors:
        return 1
    print("Evidence index checked. Inspect content and unverified cases before judging readiness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
