# Design note

The one page that goes with the chosen sketch. The builder writes it in step 5 of [design.md](design.md), fills Deviations during the build, and puts it in the PR's Design section. It lets the user and the verifier judge the shape without rebuilding it, and lets `learn-from-mistakes` find a design that failed. Keep the headings below, in this order, and replace each line under them with the content.

```markdown
### Problem
One paragraph: what the change must do, and what in the existing code or its constraints makes the shape non-obvious. Name what grounding found: types to interoperate with, callers that cannot break, ADRs that bind.

### Usage
The caller's view, written before the types: the quickstart, and two or three call sites. The sketch derives from it.

### Shape
Data structures first, then how data flows through the signatures. The load-bearing decisions, each with the principle id behind it: which invariants live in types, where validation lives, who owns each piece of state, what the system does not do on purpose. What the public surface hides, and why it is no larger.

### Choice
Which of the two sketches won and why, and what was taken from the other. When a prototype decided, its observation and where it lives.

### Tradeoffs accepted
One line each: "we accept X in exchange for Y". Name anything a later reader could take for an oversight.

### Alternatives rejected
The other sketch, and any other whole shape considered, and why each lost, judged on what it exposes to callers and what it hides. When the constraints forced the answer: "the only viable shape, because ...". Variants of one shape do not count.

### Deviations
Filled during the build: each place the code left the sketch, and whether the sketch, the requirement, or the code was wrong. A scrap goes here with its tells. "None" when the code followed the sketch.

### Questions before the merge
What the user should weigh, phrased as questions. A one-way door also goes on the PR's Risk line.
```
