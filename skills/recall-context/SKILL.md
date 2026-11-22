---
name: recall-context
description: "Rebuilds where things stand on a topic from your past sessions and the repo's record, before you start or resume work, as a short brief."
disable-model-invocation: true
argument-hint: "<the topic, and a window such as 'last week'>"
metadata:
  kind: entry
  calls: "resume-task"
  consumes: "a topic, or nothing for recent work"
  produces: "a brief: where things stand, each thread's state, the recurring problems, the next move"
  hypothesis: "A new session starts from zero: it repeats a fix that was reverted, misses what users keep reporting, and asks the user what the record already holds."
---

# Recall context

Read [the constitution](../constitution/README.md) first.

You rebuild the context before work starts and hand back a short brief. It lives in two records: the user's past sessions, which hold what was done and decided, and the repo's record (commits, PRs, reviews, issues, reverts, ADRs, decision logs), which holds what happened around the same code under other names. Read only what the topic needs, then stop.

## Steps

1. **Pick the route.** One task an earlier session left mid-way is [resume-task](../resume-task/SKILL.md), not this. When the user already gave the state (paths, branch, the change), use it and skip to step 5.
   Done when: you named the route, or switched to `resume-task`.

2. **Fix the scope.** The window (7 days by default; "recent" is a real range), the topic, and this repo only: never another project's sessions unless asked. Say the scope back in one line.
   Done when: the scope is in your first message.

3. **Mine the past sessions.** Find them where the harness keeps transcripts (see [harness.md](../constitution/references/harness.md)). Order them by modification time, search for the topic first, and read only the matching sessions and their relevant parts, skipping this session. For more than two sessions, spread them over subagents on the bulk-reading model of the harness's Model per role; each returns one block per session: the topic, the user's goal, the decisions, the open threads, the corrections the user made, and the artifacts (PRs, issues, branches), each citing its session. The transcripts stay in the subagents.
   Done when: every session in scope that matches the topic has its block, or none matched.

4. **Sweep the repo's record** whenever the topic names a feature, a file, an area, or a bug, in parallel with step 3: `git log` and `git blame` on the code, the PRs and their reviews, the issues (as `~/.agents/projects/<project>/issue-tracker.md` says), reverted commits, the ADRs, and the decision logs. Ask each source what the state is now, what was tried and did not hold, and what users still report. Skip this step only for "what did I do this week", with no named topic. A source that has nothing is a finding.
   Done when: each source answered, or is named as empty or unreachable.

5. **Check the live state** of each PR, branch, and issue that steps 3 and 4 surfaced, from the code host and `git`, not from what a session said.
   Done when: every thread's state comes from the live record.

6. **Write the brief.**
   - **Where things stand**: at most 5 bullets.
   - **Threads**: one line each, with one tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[uncommitted, verified]`, `[reverted #N]`, or `[planned, not started]`.
   - **Problems**: at most 5 recurring ones, including what users keep reporting and any fix that was reverted, so the next attempt starts where the last one failed.
   - **Next move**: the single most useful next action, concrete.

   Cite each finding by its session or its source (PR, issue, commit). Leave out what is next to the topic unless it blocks it.
   Done when: the brief fits on one screen and every line has its source.

## Reply

The brief.
