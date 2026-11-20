# State chart

How to draw and check the state chart that [coverage.md](coverage.md) asks for. The chart shows how a flow moves between states in the words of its reader, so the user can judge whether the behavior is right. Check a model with the repo's model checker, or run TLC directly.

## Two depths

| Depth | When | What |
|---|---|---|
| drawn | every stateful journey a PR touches | a Mermaid chart written from the code and the cases |
| checked | a hard zone of [proof.md](proof.md) that moves between states, such as sync, retries, or a connection lifecycle | a TLA+ model checked by TLC, and the chart drawn from the model's states |

A drawn chart can be wrong; only a checked one shows that no order of steps breaks a rule.

## Write the model (checked)

- Work in a scratch directory outside the repo.
- Each rule the user agrees to is an `INVARIANT`: about a screen, a result, a stored value, or a message. If the model has no variable for a rule, add the variable. Never weaken a rule to make it hold.
- Write `Next` as a disjunction of named actions, so each step has a name.
- An end state with no step out breaks deadlock checking. Add an action true only in end states that changes nothing.
- Every part of the model points at the code it stands for. What the model treats as one atomic step is one atomic step in the code.
- A rule never seen failing proves nothing: break the model once (remove a guard, reorder two steps) and watch TLC report it.

## Draw the chart

- Label each state with what the reader sees or cares about, such as "Paying" or "Saved, sync pending". Keep variable names out of labels.
- Label each arrow with what happens, as the user sees it: "you press save", "the connection drops". End a conditional arrow with its condition in brackets: "you press play [while the file loads]".
- Aim for about 20 arrows. Merge states that act the same and drop details the reader does not need, but never merge two states that break different rules, and keep every state of a bug path.
- Every state is reachable from a start state, and every state with a step out in the model keeps an arrow out.
- Mark each arrow with the case number that covers it, per coverage.md. A state where a rule breaks is marked in the chart.

## Report

When TLC finds a violation, tell it as the shortest sequence of steps in the code's words, then show the chart with the breaking state marked. Do not weaken the model until it passes. When a run passes, say the bounds it ran under and what the model leaves out.
