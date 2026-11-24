---
name: show-me
description: "Shows you the current topic visually, with the smallest diagram, tree, or diff that makes the key point clear."
disable-model-invocation: true
argument-hint: "<the topic to show, in your own words; nothing for the current topic>"

metadata:
  kind: entry
  consumes: "the current topic of conversation: a reply, a design, a diff, a question"
  produces: "one small visual beside the short text it supports, or one focused HTML artifact shown to you"
  hypothesis: "A dense reply in prose is the slowest way to hand over a shape; the same point in a diagram lands at once, so topics stay undecided while they stay in words."
---

# Show me

Read [the constitution](../constitution/README.md) first.

You explain the current topic visually instead of in prose. Skip the preamble and keep the words brief. [The catalog of views](references/views.md) holds each view with an example; read it once per run.

## Steps

1. **Pick the smallest view that makes the key point clear.** Logic or an algorithm becomes pseudocode, runtime control flow a call tree, UI structure a component tree, file responsibility a shallow file tree, interaction or data flow a Mermaid diagram, and a change a diff. A visual UI, layout, state comparison, or concept too dense for Mermaid becomes one focused HTML artifact.
   Done when: you can name the view you picked and the one point it must make clear.

2. **Draw only what answers the current question.** Keep only the calls, files, props, states, and boundaries the point needs; leave the rest out. Use one view, or several when the topic needs them, never all of them.
   Done when: every line of the visual earns its place against the question.

3. **Place the visual next to the short text it supports.** A diagram, tree, or diff goes inline in the reply. An HTML artifact is written as one file, then shown to you through the harness's preview, the shared view that renders an HTML file; open the file in the system browser when the harness has none.
   Done when: each visual sits beside the sentence it supports, and the reply around them stays brief.

## Reply

The short text, each visual next to the part it supports.
