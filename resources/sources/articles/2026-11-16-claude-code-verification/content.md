# Reading notes — How the Claude Code team thinks about verification

Recorded on 2026-11-23 from [Addy Osmani's article](https://claude.dev/blog/how-the-claude-code-team-thinks-about-verification/), published 2026-11-16. These are paraphrased notes, not the full article.

Osmani recommends exercising real user journeys, generating inputs against invariants, and comparing replacement systems with their predecessors. Verification infrastructure needs the same care as application code.

The team uses local execution, checks selected by changes, accumulated review context, and rules loaded from a protected base. Results belong to the commit reviewed. Owners maintain checks and explain why a failure needs attention.

New gates first record their effects without blocking. Reviewer evaluations use historical bugs and stable changes, with separate tuning and test sets. Measuring intermediate review stages helps locate missed findings. Repeated incidents inform rules; outdated rules need pruning.

The article also describes team-specific retry limits, bypasses, and treatment of flaky tests. These describe Anthropic's process and are not automatically suitable for another repository.
