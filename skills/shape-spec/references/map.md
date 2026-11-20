# Map

For a loose idea too big for one session, wrapped in fog: the way from here to the goal is not visible yet. The map finds the way; it does not build.

Its issues are **decisions**, not slices of a build. That keeps implementation from being split across agents, where work that looked independent turns out to be tangled.

## The map issue

One issue labeled `map`. Its decision issues are its children, linked as the tracker file says. The map is an index: each decision lives in one place, its issue, and the map gives one line and a link.

```markdown
## Destination
What reaching the end looks like: the spec, decision, or change this effort is finding its way to.

## Notes
The domain, the skills every session reads, standing preferences.

## Decisions so far
- [<closed decision issue title>](link): one-line gist of the answer

## Not yet specified
Questions you can tell are coming but cannot state sharply yet.

## Out of scope
- [<closed issue title>](link): why it is out
```

Refer to every issue by its title, with the link inside it. A wall of bare numbers is unreadable.

## Decision issues

Each issue holds one question, sized to one session, and a label for its type:

| Label | Type | Resolved by |
|---|---|---|
| `decision:grill` | a conversation with the user, the default | [grill.md](grill.md) with [domain.md](domain.md), user present |
| `decision:prototype` | "how should it look or behave?" | [investigate](../../investigate/SKILL.md) in prototype mode, user present |
| `decision:research` | a fact outside the repo | a fresh subagent, alone; findings on a branch that is never merged |
| `decision:task` | manual work that blocks a decision: an account, an access, a data export | the agent alone when it can, else the user |

A grill or prototype decision resolves only with the user. An agent never answers its own questions.

Blocking uses the tracker's own blocking link, as the tracker file says, so the user sees in the tracker what can start now. The **frontier** is the open, unblocked, unassigned decisions. A session claims one by assigning it first.

**Fog or issue?** Open an issue when you can state the question sharply now, even if it is blocked. Otherwise write it under Not yet specified. Do not pre-slice the fog.

## Chart the map

1. **Name the destination.** Grill the user until it is settled; it fixes the scope.
2. **Map the frontier.** Grill again, breadth first, across the whole space. If no fog appears and the work fits one session, stop: you need a spec, not a map.
3. **Create the map issue**, with the fog under Not yet specified.
4. **Create the decision issues** you can state now, then wire the blocking links in a second pass, once every issue has a number.
5. **Start the research.** One fresh subagent per research decision, in parallel.
6. **Stop.** Charting resolves nothing by hand.

## Work the map

1. Read the map issue, not every decision body.
2. Take the decision the user named, or the first one on the frontier. Assign it before any work.
3. Resolve it by its label.
4. Post the answer as a comment, close the issue, and add one line to Decisions so far.
5. Turn the fog the answer cleared into new decision issues and remove it from Not yet specified. A decision that turns out to be past the destination is closed and listed under Out of scope. Update or close decisions the answer made wrong.

One decision per session, except research. Other sessions may be working the map at the same time.

When no decision and no fog is left, the way is clear: write the destination, usually a spec as [spec.md](spec.md) describes.
