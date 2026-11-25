# Mode: prototype

For a decision a quick experiment can settle: which layout, which interaction, which density, which approach behaves or times better. The output is the decision and a throwaway artifact, not shippable code.

This is the one mode where speed beats polish: no tests, no abstractions, no production framework. The rigor is in choosing the right design cheaply.

Before asking the user "which approach?", check whether running something would answer it. If it would, prototype instead of asking. Keep the question for product and taste calls that no experiment can settle.

## Duties

1. **Name the decision.** Write the one decision the prototype exists to make. No decision, no prototype: the request is a feature, a task for `ship`.
2. **Gather references** when the design space is open: prior art, then a short summary of directions for the user to pick from. Skip when the direction is set. For a visual decision, the user's references come first; with none, propose some from a library of real product screens when the harness has one, else from the web.
3. **Build throwaway, outside the source tree.** For a visual decision, plain HTML, CSS, and JS, or the lightest stack that renders the idea. When the design must follow or extend the repo's design system, use its real tokens and components, in the lightest way that renders them, and drop the defaults [ui.md](../../constitution/references/ui.md) lists. For behavior or timing, the smallest script that exercises the question.
4. **Several variants behind one switch.** Buttons or a key that switch between labeled variants, including ones the user did not ask for.
5. **Observe each variant.** Screenshot each one, at a desktop and a phone width for a visual decision, and drive the interaction; for behavior or timing, log the timing or print the output. The observation is the test.

## Shape of the answer

The variants, the evidence for each, the tradeoffs, your pick, and the scratch path. Say plainly that the prototype is throwaway. When `shape-spec` asked for it, the user's pick is the decision it records. The proposed task names the `feature` playbook of `ship`.
