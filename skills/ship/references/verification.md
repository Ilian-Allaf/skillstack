# Verification setup and evidence record

## Before implementation

For each required proof, name the driver, command, expected result, environment, access needed, and capture method. Start the app and run a harmless read through each touched surface on the base. Try the capture command too when a demo is required. Save commands and outputs as replayable scripts and artifacts. A missing setup goes to the driver preparation already described in [proof.md](../../constitution/references/proof.md).

Check that a fresh verifier can use that setup: include safe startup commands, driver paths, and how it obtains access, never credentials or the builder's conclusions. When isolation or access differs, try the harmless read there too; an untried environment stays an explicit limit. Keep the baseline capture before implementation.

A required proof that cannot start is a blocker to full verification. Prepare the driver or access first, or show the user the missing capability and remedy before proceeding. Work continued with a disclosed limit stays unverified; it cannot become `ready` through repetition of the same blocked review. Retry that lane only after its command, access, or environment changed.

## Before opening or handing back the PR

Reconstruct the step list from the launched skill and applicable references, then compare it with recorded activity, commands, outputs, and subagent results. Include actions the summary omitted, such as a comment hunter already run. Reading a guide proves the read, not its application. Inspect the resulting diff or artifact too. See [decision-log.md](../../constitution/references/decision-log.md) for long runs.

Write a JSON evidence record in the work directory, out of git. It is an index of existing artifacts, not a second narrative. Export the relevant activity and command outputs to files; paths below resolve from the record's directory. Copy every case id from the agreed case list and every step name from the launched skill. For a spec task, list the spec's story, promise, and visual target ids in `spec_ids`; each must also be a case id, so a journey, a promise, or a target cannot drop out of the table. Include required captures in `required_artifacts`, even if missing. Cross-check both lists against their originals; the script cannot discover an omitted case or step.

```json
{
  "spec_ids": ["S1", "P1", "V1"],
  "cases": [
    {"id": "S1", "level": 5, "evidence": ["runs/s1-demo.mp4"], "not_verified": ""},
    {"id": "P1", "level": 4, "evidence": ["runs/p1-prove.txt"], "not_verified": ""},
    {"id": "V1", "level": 5, "evidence": ["runs/v1-side-by-side.png"], "not_verified": ""},
    {"id": "1", "level": 1, "evidence": [], "not_verified": "Live access unavailable; grant the verifier test access"}
  ],
  "steps": [
    {"name": "Frame", "status": "done", "result": "Base run red", "trace": "activity/frame.txt"},
    {"name": "Analyze impact", "status": "skip", "result": "Low risk", "trace": ""}
  ],
  "required_artifacts": ["demo.mp4"],
  "verdict": null
}
```

After verification, `verdict` holds `{"patch_id": "<full stable patch id>", "base_sha": "<full base SHA>", "head_sha": "<full head SHA>"}` from the verdict comment. Fetch the current base and head SHAs from the code host and compute their patch id as [verdict.md](../../verify-pr/references/verdict.md#verdict-validity) describes. Pass these independently obtained current values, not the values copied from the old verdict:

```text
python -I <ship-folder>/scripts/check_evidence.py <record.json> --patch-id <current-full-patch-id> --base-sha <current-full-base-sha> --head-sha <current-full-head-sha>
```

Use the installed folder containing this reference for `<ship-folder>`. The check rejects a spec id that is not a case id, invalid certainty levels, missing or empty local artifacts, completed steps without a result and trace, and an existing verdict for another base, head, or patch id. Older records with only a patch id need a new verdict with both SHAs. Every case needs evidence or a `not_verified` reason. Fix discrepancies in the source evidence and PR, then update the index. A passing check confirms structure and file presence only; inspect whether artifacts show the expected result. Unverified cases remain visible and readiness still follows the verifier's axes.

When a discrepancy cannot be resolved, preserve the failing check output and link it under Not verified in a draft PR in state `needs-human`. Missing mandatory captures stay in the record; removing them to obtain a passing check does not complete the proof.

If session activity is unavailable, retain command outputs and subagent reports and disclose the missing activity in the PR's Not verified section. Mark affected steps `unverified` with that reason. Never reconstruct a successful action from memory alone.
