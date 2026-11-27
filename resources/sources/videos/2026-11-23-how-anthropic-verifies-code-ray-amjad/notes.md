# Reading notes — How Anthropic Verifies Code Written by Claude

Recorded on 2026-11-23 from [Ray Amjad's video](https://www.youtube.com/watch?v=DNwMbJf5SAI). Paraphrased from automatic English captions; see [provenance](SOURCE.md).

| Chapter | Notes |
|---|---|
| [01:39](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=99s) | Amjad presents verification feedback as a way to reduce manual checking while delegating development. |
| [03:10](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=190s) | His example asks an agent to exercise agent creation in a running application and return a recording. |
| [04:03](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=243s) | The check should use the interface a user actually encounters: browser, API, CLI or mobile application. An easier internal check can miss that behavior. |
| [05:16](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=316s) | He turns a successful exploratory run into reusable launch and verification instructions, and prepares dependencies in an environment template. |
| [06:16](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=376s) | Separate environments prevent parallel verification flows from interfering through shared databases or other state. |
| [07:07](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=427s) | He separates preparing state, driving the user journey, and checking evidence. The checker looks for shortcuts and incidental defects even when the main journey succeeds. |
| [08:23](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=503s) | Testing integrations may require dedicated external accounts. He discusses credential handling outside skill text. |
| [10:33](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=633s) | A broader exploratory exercise distributes flows across environments and returns a report grouped by severity. |
| [15:09](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=909s) | A verification skill can itself be tested by planting defects in past changes and checking both detection and false alarms. |
| [17:25](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=1045s) | He describes regression checks mixing deterministic operations with agent-driven actions and assertions. His deletion of unit tests is a personal example, not a universal prescription. |
| [20:01](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=1201s) | Exploratory variations on recorded user behavior seek cases missing from scripted journeys. |
| [21:02](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=1262s) | A reported Safari video failure exposed Chromium-only coverage. He adds WebKit checks for changes to the player. |
| [22:25](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=1345s) | He relates this targeted browser check to the article's incident-derived checks selected by a diff. |
| [23:22](https://www.youtube.com/watch?v=DNwMbJf5SAI&t=1402s) | He proposes replayable benchmarks and contradiction checks as verification instructions and environments evolve. |

The video also advocates persistent automation and describes automatic merging. Those are the presenter's practices, not instructions for this framework.
