# Nectar — How Anthropic verifies code

Dated analysis, 2026-11-23. Source: [Ray Amjad](SOURCE.md); [transcript](transcript.md); [timestamped notes](notes.md).

## Contribution beyond the article

Amjad supplies concrete examples of verification environments, integration accounts, recorded user journeys and browser-specific coverage. Our interpretation: a verifier's missing capability can look like application coverage while actually leaving the important user path untested. Recording what could not be exercised is as useful as recording a successful run.

His Safari example makes a useful research question concrete: when an escaped bug exposes a missing environment, can the next check be triggered by the affected code rather than imposed on every change?

## Questions for later work

These are our research questions, not adopted skill changes:

- Does each claimed user journey have the accounts, initial state and dependencies needed to exercise it?
- Does the evidence show the real interaction, or only the final database state?
- Can concurrent checks interfere through shared state?
- Can a known defect and a clean comparison change distinguish verifier detection from over-reporting?

The proposed split between setup, driving and checking is a decomposition of work to evaluate, not a reason to add three permanent agent roles. [SCOPE.md](../../../../SCOPE.md) still governs such a proposal.

Automatic merging and scheduled work described in the video conflict with our boundaries in [ADR 0001](../../../../docs/adr/0001-the-user-always-merges.md) and [ADR 0014](../../../../docs/adr/0014-a-launched-task-runs-to-a-ready-pr.md). Adding this source does not adopt those practices.
