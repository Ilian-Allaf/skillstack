---
name: catch-me-up
description: "Tells you, in plain words with the screenshots and videos the work produced, what changed while you were away, and every call waiting on you with a recommendation."
disable-model-invocation: true
argument-hint: "<nothing for this session, PR numbers, or 'video'>"
metadata:
  kind: entry
  consumes: "the work done since the user's last message, or the PRs they name"
  produces: "a reply: what changed, with its evidence, then each call waiting on the user"
  hypothesis: "After a long run the user cannot rebuild what changed from the transcript, so calls wait, or get made without the evidence."
---

# Catch me up

Read [the constitution](../constitution/README.md) first.

You catch the user up as one person catches up another: what changed for them, the evidence they can look at, and the calls only they can make, each decidable from your reply alone. You change nothing: no code, no push, no comment, no job started. The one exception is the video, rendered outside the repo.

## Steps

1. **Fix the window.** By default, everything since the last message the user wrote in this session; notifications and subagent reports are not their messages. When they name PRs, or launch this in a new session, the window is those PRs, or the open PRs of the tasks they launched, since their last activity.
   Done when: you can say in one line what the window covers.

2. **Gather what changed.** Your own work, your subagents' reports, and what others posted. Then read the live state of each PR, check run, and agent in the window from the code host, not from a report. Collect the evidence each PR holds: the demo video, the screenshots, the coverage table, the verdict. Check every number you will show against what it comes from.
   Done when: each item has its current state from the code host, and its evidence links.

3. **List the calls waiting on the user.** A call is what only the user can do: a merge, a design to approve at a one-way door, a product or preference choice, an access you lack. Work you can still do yourself is not a call. For each: its link, what it changes for users, the evidence behind your pick, its risk, and your pick. Write "unknown" for a fact you lack.
   Done when: every call is listed, including those raised before the window, and none is invented.

4. **Write the reply** in the shape of [references/reply.md](references/reply.md). When the user asked for a video, render it as [references/video.md](references/video.md) describes, and the reply keeps only the opening sentence, the video, the work you can still do, and the calls.
   Done when: the user can make each call from the reply alone.

## Reply

As step 4 shapes it.
