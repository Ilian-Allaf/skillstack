# Guide: how to work with the skills

How to write a prompt, prompts to copy for each kind of work, and the mistakes that cost the most. `tools/check_refs.py` checks that every command here names a skill that exists (R011). Which skill does what is in the [README](../README.md#reference) and the [map](../skills/README.md); when unsure, run `/choose-skill`.

## What to put in a prompt

The skill supplies the steps, so a few plain sentences beat a spec. Put in:

- **The goal.** What is wrong, or what you want.
- **The done check.** Something that passes or fails. "Make it better" and "work on it for an hour" are not checks.
- **The proof you want to see.** The real command output, a video of the flow, the stored value, a before and after number.
- **What you already know.** A symptom, a repro step, a log line, a link. It saves the agent a search.
- **The real constraints.** "Repro first", "no behavior change", "show me the design before code" each change what the agent does.

Leave out:

- **The how.** Say what to achieve, and leave the agent room to find a better way. `/sharpen-prompt` names the methods an expert would use as the bar the result must reach, not as steps to follow.
- **A list of skills or steps.** The skill already orders them; a hand-written order drops or reorders steps. Name a skill only to override one choice.
- **Your theory of the cause, at first.** A stated guess narrows the search to where you pointed. Let the agent restate the problem, then share your hunch.

Once a task runs, it does not wait for a go: it shows you its frame and goes on to a ready PR. Stop it, or redirect it, at any time.

## Prompts to copy

Swap in the real paths, numbers, and checks.

### Understand

```text
/recall-context the export pipeline, last two weeks
/investigate how does the export retry work? are we sure a retry cannot write twice?
/investigate why does memory grow after each sync? here is the heap snapshot: <path>
/investigate prototype two layouts for the settings page, screenshots of each, and pick one
/sharpen-prompt write a migration guide for the v2 config format
```

### Build one change

```text
/ship the export writes duplicate rows when a retry lands mid-run. repro first. done means the 60k-row fixture exports each row once. show me the row counts before and after.
/ship add a --json flag to the report command. the text output stays byte-identical. verify both forms.
/ship move parsing into one module, no behavior change. pin the current output first.
/ship startup takes 1.8s on the sample project. trace it, fix the measured cause, show me before and after.
/ship get p50 of the search endpoint under 40 ms on the large fixture, at least 10 attempts.
/ship migrate the buttons to the new design system. the screenshots must match pixel for pixel.
/ship add rate limiting to the public webhooks. show me the design before code.
```

### Build many changes

```text
/ship-queue
fix #41: the avatar upload fails on files over 5 MB
fix #42: the date picker ignores the user's time zone
add #45: export the audit log as CSV
```

### Step away and come back

```text
/pause-task
/resume-task
/catch-me-up
/catch-me-up video
```

The agent also pauses on its own when its context or your usage limit is about to run out; `/resume-task` picks the task up in a new session.

### Review and land

```text
/verify-pr 123
/analyze-impact 123
/babysit-pr 123
```

You merge. A stack merges from the bottom.

### Make the next run better

```text
/add-guardrail agents keep calling the database client directly instead of the repository layer
/learn-from-mistakes 123
/test-skill-change the new feature playbook in branch better-feature-playbook
/clean-worktrees
```

## Steer with principle names

One principle name redirects the agent more precisely than a paragraph; see [Steer with principle names](../README.md#steer-with-principle-names) and the [list](../skills/constitution/references/principles.md).

## Mistakes that cost the most

- **A duration instead of a done check.** "Work on it for four hours" gives the agent nothing to check; you get four hours of motion instead of a result.
- **Listing skills in the prompt.** "Use investigate, then ship, then verify" reorders what the skill already sequences.
- **Taking the first design.** One attempt locks in the first shape the model thought of. Ask to see the design, or a prototype of two options.
- **Reviewing an abstract plan.** A plan with no code behind it invites invented risks. Settle open questions with prototypes, then review what got built.
- **Correcting the same mistake by hand.** A correction in chat helps one run. `/add-guardrail` makes it fail the next time.
- **Trusting a number nobody vetted.** A warm cache or a skipped path can fake a speedup. The `perf` and `hillclimb` playbooks check every number; ask for the run count and the spread.
- **Reporting success off a green build.** A build proves it compiles. Ask for the real flow, the stored value, or the video.
- **Two agents in one worktree.** They overwrite each other. `/ship-queue` gives each task its own.
