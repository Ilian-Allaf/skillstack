# The video

A short, silent, subtitled video of slides that shows what happened, in place of the reply's step 2. It is rendered outside the repo; if rendering fails, say so in one line and give only the calls.

## Slides

Build from the screenshots, recordings, diffs, and data the work produced, not from the conversation's prose. Before you draw, write the one sentence the user should leave with and one line per slide; drop each slide that does not change what the user knows. Ten slides at most; fewer is better.

- Each slide makes one point. Keep one picture and change it from slide to slide rather than cut to an unrelated one. A color or a shape means the same thing on every slide.
- Show the work as pictures: how a system works, a stack of PRs with each state, a before and after, options side by side. Point at what changed with arrows and highlights.
- A slide is never a bullet list, a table, or boxes with nothing connecting them. Labels sit on the thing they name, in plain words.
- Show what came of each thing the user asked for and its state. Never show done what still waits on the user. A visible change with no screenshot says so on its slide.
- Draw only from facts you have.

## Subtitles

One line per slide, about ten words, that says the slide's point as you would say it to the user. It sits in a strip below the slide, the same height on every slide, so it never covers the picture. Small, but readable at chat size.

## Render

One landscape video, such as an mp4, made from the slide images, never from a screen recording, for example with `ffmpeg`. Burn each subtitle into its slide's frames. Hold each slide at least one second per three words it adds: its subtitle, and each word that was not on the slide before. Words inside a screenshot do not count.

## Check before you embed

Look at one frame of each slide at chat size: the subtitle is readable and covers nothing. Measure each hold from the file's frames, and compare it with the words the slide adds. Fix any slide that cannot be read in its hold, render again, and check again.
