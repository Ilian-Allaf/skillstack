# Coverage

The user reviews the evidence in the PR, not the code. Whatever the evidence does not show, the user does not see. So the evidence covers every case, and says plainly what it does not cover.

Exhaustive in coverage, not in footage: every case has evidence, and each case gets the kind of evidence that shows it best.

## The case list

`frame` writes the list before any code changes, and the user sees it in the frame. It holds:

- the main case from `done_when`;
- when the task is a spec issue, one case per user story of the spec;
- one case per entry point of the touched feature: those its feature file's Declared in points to, and those the file lists by hand (button, shortcut, command, import, API call);
- one case per path a user can reach that calls the changed code, found in the code itself (a search for its callers, `analyze-impact` step 1), not only in the map. A path the map lacks is added to its feature file in this PR, so the builder and the verifier do not share the map's blind spot;
- the edge cases of the hard zones the change touches: double action, retry, error path, empty and long input, reload or back navigation mid-action, two users or two tabs;
- for a bug, the reported case on the base and on the head;
- the property of each formal check that covers a touched file, found as [proof.md](proof.md#drivers-and-formal-checks) says, with its check run as evidence; a check stale on the base proves nothing, so its case goes under Not verified, as [formal.md](formal.md#in-a-task) says.

A feature file whose code changed after the commit it was last driven at may be stale: say so in the frame, and drive its entry points before you trust it. Cases that what the code already forbids (a type, a lint) need no evidence; name the check instead. `analyze-impact` and the verifier may add cases; each one added goes in the table.

## The coverage table

The PR opens with a table that has one row per case:

```markdown
| # | Case | Evidence | Level |
|---|---|---|---|
| 1 | Double click on Save creates one note | demo 0:00-0:18, `notes` table read back | 5 |
| 2 | Ctrl+S during save | demo 0:18-0:31 | 5 |
| 3 | Save fails offline, button comes back | `npm test -- save.offline` | 4 |
| 4 | Import of a note file | not covered: see Not verified | - |
```

The agent picks the evidence per case: a video chapter for a journey, a screenshot for a static state, command output for what is not visual. A case without evidence stays in the table and points to Not verified. No case is left out of the table.

## The demo video

Required when a case is a user journey on a visual surface (web, desktop, mobile, or TUI), a bug included. Otherwise the table holds screenshots and command output.

- **Scripted, never filmed by hand.** Each case is a scripted journey in `drive-<app>`. The video is the recording of those scripts, so anyone can replay it.
- **One chapter per case**, in the table's order, with a caption strip under the picture naming the case and the expected result. Captions are burned in and readable at chat size.
- **Before and after.** For a bug, each case shows the base, then the head. For a feature, show the base only when the absence matters.
- **Short.** Speed up the waits. Aim under three minutes; past that, split by feature.
- **Clean.** Test data only. Run the secret scan on the frames before upload.

## The state chart

When the touched journey moves between states (saving, syncing, connecting, paying), add a Mermaid state chart in the PR, from the user's point of view: each state is what the user sees, each arrow is what the user or the system does. Mark each arrow with the case number that covers it. An arrow with no case is a gap in plain sight. Draw it, and in hard zones check it with a TLA+ model, as [statechart.md](statechart.md) describes.

## Not verified

Every case without evidence, and every kind of case the list did not consider, goes under Not verified with the reason. The user knows what they are not seeing.
