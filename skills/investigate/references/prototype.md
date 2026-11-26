# Mode: prototype

For a decision a quick experiment can settle: which layout, which interaction, which density, which motion, which approach behaves or times better. The output is the decision and a throwaway artifact, not shippable code.

This is the one mode where speed beats polish: no tests, no abstractions, no production framework. The rigor is in choosing the right design cheaply.

Before asking the user "which approach?", check whether running something would answer it. If it would, prototype instead of asking. Keep the question for product and taste calls that no experiment can settle.

## Duties

1. **Name the decision.** Write the one decision the prototype exists to make. No decision, no prototype: the request is a feature, a task for `ship`.
2. **Gather references** when the design space is open: prior art, then a short summary of directions for the user to pick from. Skip when the direction is set. For a visual decision, ask for the user's own first: screenshots, sites, apps, and videos for motion. With none, or too few, propose five to eight from a library of real UI references when the harness has one (see [harness.md](../../constitution/references/harness.md)), else from the web, or from a real site driven in a browser. Show each with one line on what to take from it: the layout, the color, the type, the density, the motion. The user keeps some and drops the rest.
3. **Read each motion reference frame by frame**, with the frame-cutting capability of harness.md or its fallback: write its effect list, one line per effect: the trigger, what moves, the duration, the easing, the direction. Take from several references, and copy no element one to one.
4. **Build throwaway, outside the source tree.** For a visual decision, plain HTML, CSS, and JS, or the lightest stack that renders the idea, in the design mode of [ui.md](../../constitution/references/ui.md#the-design-system-comes-from-the-code): with the repo's real tokens and components under `follow` and `extend`. For behavior or timing, the smallest script that exercises the question.
5. **Several variants behind one switch.** Buttons or a key that switch between labeled variants, including ones the user did not ask for. Three for a visual decision.
6. **Observe each variant.** Screenshot each one, at the desktop and the phone width of ui.md for a visual decision, record it when it moves, and drive the interaction; for behavior or timing, log the timing or print the output. The observation is the test.
7. **Make feedback specific**, for a visual decision. Ask what to change, where, and how. When the user feels something is off but cannot name it, describe in plain words how you built that part, its layout, fonts, colors, spacing, timing, so they have the words. Change the variants and show them again. After three showings with no pick, ask which variant is closest and why, and narrow to it.

## Shape of the answer

The variants, the evidence for each, the tradeoffs, your pick, and the scratch path. Say plainly that the prototype is throwaway. When `shape-spec` asked for it, the user's pick is the decision it records. The proposed task names the `feature` playbook of `ship`.
