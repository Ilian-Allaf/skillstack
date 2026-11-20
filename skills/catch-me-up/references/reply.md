# The reply

Spend words on the calls, not on the story.

## Voice

Plain words and short sentences, as one person catching up another. Say what changed for the user, not how you did it: "the tests pass", not "CI is green". Leave out hashes, file paths, commands, and counts unless the user needs one to act. Call each PR, branch, or agent by a name the user knows, not one you invented. A fact that needs context gets its context, or is left out. The rest of [writing.md](../../constitution/references/writing.md) applies.

## Shape

1. **One opening sentence** that names what waits on the user, or says nothing does. If nothing happened and nothing waits, say so and stop.
2. **What happened, pictures first.** Embed inline the screenshots and videos the work produced, the PRs' demo videos first, then any diagram that explains a change. Then one short bullet per thing the user asked for: what came of it, and whether it is done, still running, failed, or not checked. Write each bullet as you would say it aloud: "Search was slow from a missing index", not "Search: done". Name any bug found and fixed on the way. Never mark done what still waits on the user. Keep this part under 100 words, pictures aside.
3. **At most three lines** that change what the user knows or must do, then one line for the work left that you can do yourself.
4. **The calls.** About 30 words each, riskiest first; the reply grows with their number, and none is cut or replaced by a count or a bare link.
   - One call about one item: one bullet with the call, your pick, what it changes for users, the evidence, and the risk, even when low ("Low risk: only the colors change").
   - Items that share a call, such as PRs ready to merge: the call and your pick once, then one bullet per item with its link, what it changes, its evidence, and its risk.
   - A call between options: every option you weighed, each with what it gets the user and what it costs. Under a screenshot of each option when you have one.
   - Say what waiting costs only when it is more than a delay: a deadline, lost data.

## Visuals

A visual is a screenshot, a video, a Mermaid diagram, a chart, or a generated image; a Markdown table is not. Draw when a picture lands faster than words: how a design works, a stack of PRs with each one's state, a before and after, options side by side. Never draw a status list or boxes with nothing connecting them. At most six boxes, at most eight plain words in each. A visible change with no screenshot is marked "No screenshot yet", with what changed on screen. Draw only from facts you have: never invent a number, never draw a screen you did not capture, and link only artifacts that exist.
