# The skill graph

The main flow first, the side flows next, and the reference tables last. For the reasons behind each step, read [How the framework works](README.md).

## At a glance

What you usually do, in order. You launch steps 1, 2, 3, and 7; `ship` runs 4 and 5 itself.

```mermaid
flowchart TB
  setup["<b>1. setup-repo</b><br/>Once per repo: tracker, glossary, app driver"]
  shape["<b>2. shape-spec</b><br/>Only when the idea is loose: it becomes a spec issue"]
  ship["<b>3. ship</b><br/>One task to a proven PR; ship-queue for a list"]
  verify["<b>4. verify-pr</b><br/>A fresh agent tries to break the PR"]
  babysit["<b>5. babysit-pr</b><br/>Review, CI, conflicts, until ready"]
  merge[["6. ready: you merge"]]
  learn["<b>7. learn-from-mistakes</b><br/>Find the layer that missed the bug, and fix it"]

  setup --> shape --> ship --> verify --> babysit --> merge
  merge -->|a bug got through| learn

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  class merge ready

  click setup "#7-preparing-a-repo"
  click shape "#8-shaping-a-spec"
  click ship "#2-the-eight-steps"
  click verify "#6-steps-7-and-8-verdict-and-babysitting"
  click babysit "#6-steps-7-and-8-verdict-and-babysitting"
  click learn "#12-learning-from-a-mistake"
```

Open a step: [setup-repo](#7-preparing-a-repo) · [shape-spec](#8-shaping-a-spec) · [ship](#2-the-eight-steps) · [verify-pr and babysit-pr](#6-steps-7-and-8-verdict-and-babysitting) · [learn-from-mistakes](#12-learning-from-a-mistake)

At any time: `/choose-skill` names the skill to launch, `/investigate` answers a question without a PR, `/recall-context` and `/catch-me-up` tell you where things stand, and `/pause-task` and `/resume-task` stop a task and pick it up.

## Legend

| You see | It means |
|---|---|
| a solid arrow | the skill runs the other one as one of its steps; in [At a glance](#at-a-glance) only, what comes next |
| a thick arrow | the skill writes or updates a tool in your repo |
| a dashed arrow | in the main flow: a stop, the task hands back to you |
| a blue cylinder | a tool generated in your repo: `drive-<app>` launches and drives the app, `prove-<area>` runs one formal check |
| a green box | `ready`: the PR waits for your merge |
| an orange box | `needs-human`: the PR waits for your answer |
| a red box | a stop with no PR |

## The main flow: delivering one task

`ship` carries one task to a PR labeled `ready`, which you merge. First the skills it runs, then its eight steps, then a zoom on each step that loops. Each zoom links the file that holds its rules.

### 1. The skills ship runs

Each arrow names the step of `ship` that runs the other skill.

```mermaid
flowchart TB
  ship["<b>ship</b><br/>One task to a ready PR"]
  investigate["<b>investigate</b><br/>Answer, diagnose, prototype"]
  impact["<b>analyze-impact</b><br/>What breaks outside the diff"]
  verify["<b>verify-pr</b><br/>Independent verdict on a PR"]
  babysit["<b>babysit-pr</b><br/>Conflicts, review, CI to ready"]

  ship -->|"steps 1-2: a symptom or a choice"| investigate
  ship -->|"step 5: medium or high risk"| impact
  ship -->|"step 7: the PR is open"| verify
  ship -->|"step 8: both axes PASS"| babysit
  babysit -->|a new base or head| verify
  verify -->|its breakage lane| impact

  click ship "#2-the-eight-steps"
  click verify "#6-steps-7-and-8-verdict-and-babysitting"
  click babysit "#6-steps-7-and-8-verdict-and-babysitting"
```

Open: [ship's eight steps](#2-the-eight-steps) · [verify-pr and babysit-pr](#6-steps-7-and-8-verdict-and-babysitting) · [investigate](investigate/SKILL.md) · [analyze-impact](analyze-impact/SKILL.md)

### 2. The eight steps

The main path, top to bottom. A dashed arrow is a stop; [the budget table](#every-loop-and-its-budget) lists every one.

```mermaid
flowchart TB
  start(("/ship #lt;task#gt;"))
  frame["<b>1. Frame</b><br/>done_when red on the base, cases, risk, playbook"]
  build["<b>2. Build</b><br/>Design, then the playbook's loop"]
  clean["<b>3. Clean</b><br/>Remove slop; a comment hunter flags the surprises"]
  prove["<b>4. Prove</b><br/>Every case, on the base and the head"]
  impact["<b>5. analyze-impact</b><br/>What breaks outside the diff"]
  open["<b>6. Open the PR</b><br/>Evidence check, then push"]
  verdict{"<b>7. verify-pr</b><br/>Both axes PASS?"}
  babysit["<b>8. babysit-pr</b><br/>Conflicts, review, CI; reverifies each push"]
  ready[["ready: you merge"]]
  human[["needs-human: you answer"]]
  shapestop[["stop: propose /shape-spec"]]
  nopr[["stop, no PR"]]

  start --> frame --> build --> clean --> prove
  prove -->|medium or high risk| impact --> open
  prove -->|low risk| open
  open --> verdict
  verdict -->|PASS| babysit --> ready
  verdict -->|"FAIL: fix it, 2 FAILs max"| build
  frame -.->|several open decisions| shapestop
  frame -.->|a symptom that never fires| nopr
  build -.->|"3 attempts spent, or a second sketch scrapped"| human
  verdict -.->|"INCONCLUSIVE, or the FAIL budget spent"| human
  babysit -.->|"5 rounds spent, or a call only you can make"| human

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  classDef human fill:#fff1c2,stroke:#9a6700,color:#1f2328
  classDef stop fill:#ffe0e0,stroke:#cf222e,color:#1f2328
  class ready ready
  class human human
  class nopr,shapestop stop

  click frame "#3-step-1-framing"
  click build "#4-step-2-design-and-build"
  click verdict "#6-steps-7-and-8-verdict-and-babysitting"
  click babysit "#6-steps-7-and-8-verdict-and-babysitting"
  click shapestop "#8-shaping-a-spec"
  click nopr "#every-loop-and-its-budget"
  click human "#every-loop-and-its-budget"
```

Zoom in: [1. Frame](#3-step-1-framing) · [2. Build](#4-step-2-design-and-build) · [the playbooks](#5-the-playbooks) · [7-8. Verdict and babysitting](#6-steps-7-and-8-verdict-and-babysitting) · [every stop and budget](#every-loop-and-its-budget)

Your answer to a `needs-human` PR, in the session or as a PR comment, removes the label and restarts the loop that stopped, with a fresh budget (rule 11 of [the constitution](constitution/README.md)).

### 3. Step 1, framing

[↑ The eight steps](#2-the-eight-steps)

Before the frame, `ship` checks what already exists, reproduces a bug, and settles what is unclear. [frame.md](ship/references/frame.md)

```mermaid
flowchart TB
  task(("the task"))
  exists{"A branch or PR<br/>already exists?"}
  resume["Resume at the first step<br/>whose Done when fails"]
  bug{"A bug?"}
  repro["<b>Reproduce the symptom</b><br/>with drive-#lt;app#gt;"]
  diag["<b>investigate</b>, diagnosis<br/>Find a trigger that fires"]
  nopr[["stop, no PR<br/>with what would make it fire"]]
  clear{"Clear enough for an<br/>observable done_when?"}
  proto["<b>investigate</b>, prototype<br/>Settle the one decision"]
  shape[["stop: propose /shape-spec"]]
  frame["<b>Write the frame</b><br/>done_when red on the base, cases, risk, playbook"]
  lacks["<b>Build the missing proof first</b><br/>create-app-driver, create- or maintain-formal-verification"]
  pre["<b>verify-pr, before build</b><br/>Reads done_when; you fix its flags"]
  go(("step 2"))

  task --> exists
  exists -->|yes| resume
  exists -->|no| bug
  bug -->|yes| repro
  bug -->|no| clear
  repro -->|it fires| clear
  repro -->|it does not| diag
  diag -->|a trigger fires| clear
  diag -->|none fires| nopr
  clear -->|yes| frame
  clear -->|one decision first| proto --> frame
  clear -->|"several open decisions, too big, or a heavy visual change with no target"| shape
  frame -->|"a surface with no driver, a promise with no check, a stale check"| lacks --> go
  frame -->|high risk or a hard zone| pre --> go
  frame -->|otherwise| go

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  classDef human fill:#fff1c2,stroke:#9a6700,color:#1f2328
  classDef stop fill:#ffe0e0,stroke:#cf222e,color:#1f2328
  class nopr,shape stop

  click shape "#8-shaping-a-spec"
  click lacks "#9-building-the-projects-tools"
  click go "#4-step-2-design-and-build"
```

Next: [step 2, design and build](#4-step-2-design-and-build) · Leads to: [shaping a spec](#8-shaping-a-spec) · [building the project's tools](#9-building-the-projects-tools)

### 4. Step 2, design and build

[↑ The eight steps](#2-the-eight-steps)

A change inside one function body names its data shape and builds. A change that crosses a function boundary runs the whole design loop. [design.md](ship/references/design.md)

```mermaid
flowchart TB
  data["<b>1. Name the data shape</b><br/>In the glossary's words"]
  ground["<b>2. Ground</b><br/>How each touched module works today"]
  sketch["<b>3. Sketch twice</b><br/>Two different shapes"]
  proto["<b>investigate</b>, prototype<br/>A run picks the sketch"]
  pick["<b>4-5. Screen and pick</b><br/>Red flags; the design note"]
  show{"<b>6. Show you the design?</b><br/>One-way door, or you asked"}
  you["You approve,<br/>or push back"]
  build["<b>7. Build against the sketch</b><br/>The playbook's loop; each deviation logged"]
  scrap["<b>8. Scrap the sketch</b><br/>Deviations form a pattern; redesign smaller"]
  check{"done_when green,<br/>every playbook duty met?"}
  human[["needs-human"]]
  next(("step 3"))

  data -->|crosses a function boundary| ground --> sketch --> pick --> show
  sketch -->|a run can settle it| proto --> pick
  show -->|yes| you
  show -->|no| build
  you -->|go| build
  build --> check
  check -->|yes| next
  data -->|one function body| build
  check -->|"no: try again, 3 attempts; before the 3rd, test the premise they share"| build
  check -.->|3 attempts spent| human
  build -->|a pattern of deviations| scrap
  scrap -->|once: sketch again| sketch
  scrap -.->|a second time| human
  you -->|pushback| ground

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  classDef human fill:#fff1c2,stroke:#9a6700,color:#1f2328
  classDef stop fill:#ffe0e0,stroke:#cf222e,color:#1f2328
  class human human

  click build "#5-the-playbooks"
  click human "#every-loop-and-its-budget"
```

The playbook's loop: [the playbooks](#5-the-playbooks) · Stops: [every loop and its budget](#every-loop-and-its-budget)

### 5. The playbooks

[↑ The eight steps](#2-the-eight-steps)

Step 1 picks one playbook per task, step 2 follows it, and `verify-pr` checks its duties. A task that fits two rows is two units, one PR each, the second stacked on the first. [frame.md](ship/references/frame.md#playbooks)

| Playbook | Pick it when | `done_when` | The loop inside | The verifier checks |
|---|---|---|---|---|
| [bug-fix](ship/references/playbooks/bug-fix.md) | a behavior is wrong | the symptom you reported | a command that goes red on this bug; rule out causes by runtime evidence; fix the root; look for siblings | the repro commit comes before the fix, red on the base and green on the head; missed siblings |
| [feature](ship/references/playbooks/feature.md) | a behavior is missing, or a screen to build | the new journey works | one vertical slice at a time: one test, the least code, the next test; then the [target loop](ship/references/visual-loop.md) for visual targets | each new test fails with the code reverted; every entry point; the bolt-on it rejected |
| [refactoring](ship/references/playbooks/refactoring.md) | the structure changes, the behavior does not | the target structure, red on the base; a pin, green on both | small steps, the pin green after each one | the pin on base and head; no added behavior; where reading got easier |
| [perf](ship/references/playbooks/perf.md) | a path is too slow | a number on a named path | measure, try the cheapest fix, measure again, one attempt at a time | the measurement replayed; each number's checks |
| [hillclimb](ship/references/playbooks/hillclimb.md) | one metric must reach a target over many attempts | a target and a floor on attempts | keep or revert each attempt, on a frozen harness, logged | the harness replayed; each kept commit moved the metric past the noise |
| [visual-parity](ship/references/playbooks/visual-parity.md) | the UI must look the same after a migration | the migration target, red on the base; an image diff of zero | diff each component, fix each changed pixel, diff again until zero | the harness rerun; the baseline and harness untouched |
| [bespoke](ship/references/playbooks/bespoke.md) | none of the above: a wide migration, a change in several parts | a yes-or-no check on the real product | stacked units, each its own PR through steps 2 to 7; one `babysit-pr` over the stack | each PR green alone; no caller of the old form left |

`hillclimb`, the target loop of `feature`, and each unit of `bespoke` run the same experiment loop. `perf` runs it too, one measured attempt at a time.

```mermaid
flowchart TB
  hyp["<b>Hypothesis</b><br/>Grounded in a mechanism; after several reverts, a new kind"]
  change["<b>One change</b><br/>The smallest"]
  measure["<b>Measure</b><br/>Same frozen check"]
  keep{"Past the noise,<br/>gate green?"}
  commit["Keep it:<br/>one commit"]
  revert["Revert it<br/>in full"]
  log["Log the attempt"]
  done[["Stop: the target is met"]]

  hyp --> change --> measure --> keep
  keep -->|yes| commit --> log
  keep -->|no| revert --> log
  log -->|not yet| hyp
  log -->|met| done

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  classDef human fill:#fff1c2,stroke:#9a6700,color:#1f2328
  classDef stop fill:#ffe0e0,stroke:#cf222e,color:#1f2328
  class done ready
```

### 6. Steps 7 and 8, verdict and babysitting

[↑ The eight steps](#2-the-eight-steps)

The verifier is a fresh agent that tries to break the PR. A FAIL goes back to the builder, and every push goes back to the verifier. [verify-pr](verify-pr/SKILL.md), [babysit-pr](babysit-pr/SKILL.md)

```mermaid
flowchart TB
  open(("PR open"))
  verify["<b>verify-pr</b><br/>A fresh verifier tries to break it"]
  verdict{"Verdict on<br/>behavior and code"}
  fix["<b>Fix the FAIL</b><br/>In step 2 during ship, in the next round after"]
  dispute["<b>Dispute it, once per PR</b><br/>A new verifier reruns both runs"]
  state{"Anything open?<br/>Conflict, thread, red CI"}
  round["<b>One babysit round</b><br/>Rebase, triage comments, fix CI, reprove; one push"]
  ready[["ready"]]
  human[["needs-human"]]

  open --> verify --> verdict
  verdict -->|PASS| state
  verdict -->|FAIL| fix --> verify
  verdict -->|a FAIL you can refute| dispute
  dispute -->|overturned| state
  dispute -.->|it stands| human
  verdict -.->|"INCONCLUSIVE, or a 2nd FAIL"| human
  state -->|no| ready
  state -->|yes| round
  round -->|pushed: a new head| verify
  round -->|replies only| state
  round -.->|"5 rounds spent, or an ask for you"| human

  classDef ready fill:#d3f5dc,stroke:#1a7f37,color:#1f2328
  classDef human fill:#fff1c2,stroke:#9a6700,color:#1f2328
  classDef stop fill:#ffe0e0,stroke:#cf222e,color:#1f2328
  class ready ready
  class human human

  click human "#every-loop-and-its-budget"
```

Stops: [every loop and its budget](#every-loop-and-its-budget)

### Every loop and its budget

Rule 7 of [the constitution](constitution/README.md) holds for each: inside the budget, a plateau means change the approach; before the last attempt, write the premise the attempts share and test it; never relax `done_when`.

| Loop | Where | Budget | When it runs out |
|---|---|---|---|
| Build attempts | `ship` step 2 | 3 | the PR still opens, `needs-human` |
| Scrapped sketch | `ship` step 2, [design.md](ship/references/design.md) step 8 | 1 | a second scrap: the PR opens `needs-human` |
| Comment hunter report | `ship` step 3, [clean.md](ship/references/clean.md) | 1 retry | `needs-human` |
| Target loop | `feature` duty 8, [visual-loop.md](ship/references/visual-loop.md) | 10 passes for stills, 10 for motion | a measured check fails: `needs-human`; only the scores fall short: the PR goes on with its gaps |
| FAIL verdicts | `ship` step 7 and `babysit-pr` | 2 per PR, counted across both; 1 dispute | `needs-human` |
| Babysit rounds | `babysit-pr` | 5 | `needs-human`, with the premise the rounds shared |
| CI flake | `babysit-pr` step 4 | 1 rerun | reported as a flake |
| Waiting with no PR watcher | `babysit-pr` | a check every 5 to 10 minutes, for 2 hours | `needs-human`, with what the PR waits on |

Three stops are not loops: a frame with several decisions still open for you and a symptom no trigger makes fire, both before any PR, and an evidence check that finds discrepancies when the PR opens, which leaves a draft labeled `needs-human`.

## Side flows

Each one runs when its situation comes up, around the main flow. With [the skills ship runs](#1-the-skills-ship-runs), these pieces hold every `calls:` edge of the frontmatter; [the table below](#every-skill-with-its-edges) lists them per skill.

### 7. Preparing a repo

Once per repo, before the first task: the tracker, the labels, the glossary, the standards, and the driver if you chose it.

```mermaid
flowchart LR
  setup["<b>setup-repo</b><br/>Prepare a new repo"]
  driver["<b>create-app-driver</b><br/>Write the app driver"]
  guard["<b>add-guardrail</b><br/>Turn a mistake into a check"]

  setup -->|if you chose it| driver
  setup -->|if you chose it| guard

  click driver "#9-building-the-projects-tools"
```

### 8. Shaping a spec

When an idea is too loose for `ship` to frame: several open decisions only you can make, a task too big to frame, or a heavy visual change with no visual target. `shape-spec` interviews you and writes a spec issue that `ship` then takes.

```mermaid
flowchart LR
  shape["<b>shape-spec</b><br/>Idea to spec issue"]
  investigate["<b>investigate</b><br/>Answer, diagnose, prototype"]

  shape -->|prototype a decision| investigate
```

### 9. Building the project's tools

When step 1 of `ship` finds the proof lacking, the task builds it before it changes the code.

```mermaid
flowchart LR
  ship["<b>ship</b><br/>One task to a ready PR"]
  driver["<b>create-app-driver</b><br/>Write the app driver"]
  createfv["<b>create-formal-verification</b><br/>Prove one property"]
  maintainfv["<b>maintain-formal-verification</b><br/>Resync formal checks"]
  drive[("<b>drive-#lt;app#gt;</b><br/>Launch and drive the app")]
  prove[("<b>prove-#lt;area#gt;</b><br/>One formal check")]

  ship -->|a touched surface has no driver| driver
  ship -->|your promise in a hard zone, no check| createfv
  ship -->|a check is stale on the base| maintainfv
  driver ==> drive
  createfv ==> prove
  maintainfv ==> prove

  classDef tool fill:#ddf4ff,stroke:#0969da,color:#1f2328
  class drive,prove tool

  click ship "#2-the-eight-steps"
```

### 10. Using the project's tools

Every skill that must see the app runs `drive-<app>`; `analyze-impact` also runs the formal checks of the code it follows.

```mermaid
flowchart LR
  ship["<b>ship</b><br/>One task to a ready PR"]
  investigate["<b>investigate</b><br/>Answer, diagnose, prototype"]
  impact["<b>analyze-impact</b><br/>What breaks outside the diff"]
  verify["<b>verify-pr</b><br/>Independent verdict on a PR"]
  babysit["<b>babysit-pr</b><br/>Conflicts, review, CI to ready"]
  drive[("<b>drive-#lt;app#gt;</b><br/>Launch and drive the app")]
  prove[("<b>prove-#lt;area#gt;</b><br/>One formal check")]

  ship --> drive
  investigate --> drive
  impact --> drive
  verify --> drive
  babysit --> drive
  impact --> prove

  classDef tool fill:#ddf4ff,stroke:#0969da,color:#1f2328
  class drive,prove tool
```

### 11. Resuming work

When a session ended mid-task, or you come back to a topic. `resume-task` hands the task back to the skill that owns it, at its first unfinished step.

```mermaid
flowchart TB
  recall["<b>recall-context</b><br/>Where a topic stands"]
  resume["<b>resume-task</b><br/>Continue a stopped task"]
  queue["<b>ship-queue</b><br/>Many tasks to many PRs"]
  ship["<b>ship</b><br/>One task to a ready PR"]
  shape["<b>shape-spec</b><br/>Idea to spec issue"]
  investigate["<b>investigate</b><br/>Answer, diagnose, prototype"]
  babysit["<b>babysit-pr</b><br/>Conflicts, review, CI to ready"]

  recall -->|one task left mid-way| resume
  resume --> ship
  resume --> queue
  resume --> shape
  resume --> investigate
  resume --> babysit
  queue -->|one owner per task| ship

  click ship "#2-the-eight-steps"
  click shape "#8-shaping-a-spec"
  click babysit "#6-steps-7-and-8-verdict-and-babysitting"
```

### 12. Learning from a mistake

When a bug got through to you: `learn-from-mistakes` finds the layer that missed it and, once you approve, has the fix built.

```mermaid
flowchart LR
  learn["<b>learn-from-mistakes</b><br/>Fix the layer that missed it"]
  guard["<b>add-guardrail</b><br/>Turn a mistake into a check"]
  driver["<b>create-app-driver</b><br/>Write the app driver"]

  learn -->|approved code-level lesson| guard
  learn -->|approved feature-map gap| driver

  click driver "#9-building-the-projects-tools"
```

## Reference

### Skills that work alone

These run no other skill. Launch them when the situation fits.

| Skill | What it does |
|---|---|
| [choose-skill](choose-skill/SKILL.md) | Tells you which skill to launch and with what command; launches nothing |
| [sharpen-prompt](sharpen-prompt/SKILL.md) | Rewrites a prompt you are about to send so it asks for deeper work |
| [pause-task](pause-task/SKILL.md) | Stops the running task at a safe point and leaves a resume note |
| [catch-me-up](catch-me-up/SKILL.md) | Tells you what changed while you were away, and each call waiting on you |
| [clean-worktrees](clean-worktrees/SKILL.md) | Removes the worktrees of finished tasks, never losing unsaved work |
| [say-it-plainly](say-it-plainly/SKILL.md) | Says the last reply again, shorter, with no jargon |
| [show-me](show-me/SKILL.md) | Shows the current topic as the smallest clear diagram or diff |
| [test-skill-change](test-skill-change/SKILL.md) | Tests blind whether a skill change makes the agent work better |

### Every skill, with its edges

| Skill | What it does | Runs | Run by |
|---|---|---|---|
| [add-guardrail](add-guardrail/SKILL.md) | Turns a repeated mistake into a check, proven red on the real mistake | | setup-repo, learn-from-mistakes |
| [analyze-impact](analyze-impact/SKILL.md) | Finds what a change breaks outside its diff and proves the fact it is safe because of | drive-\<app\>, prove-\<area\> | ship, verify-pr |
| [babysit-pr](babysit-pr/SKILL.md) | Drives an open PR to ready: conflicts, review, CI; stops before the merge | verify-pr, drive-\<app\> | ship, resume-task |
| [catch-me-up](catch-me-up/SKILL.md) | Tells you what changed while you were away, and each call waiting on you | | |
| [choose-skill](choose-skill/SKILL.md) | Tells you which skill to launch | | |
| [clean-worktrees](clean-worktrees/SKILL.md) | Removes finished worktrees safely | | |
| [create-app-driver](create-app-driver/SKILL.md) | Writes `drive-<app>`, the skill that launches and drives the app like a user, with its feature map | writes drive-\<app\> | ship, setup-repo, learn-from-mistakes |
| [create-formal-verification](create-formal-verification/SKILL.md) | Proves one property where a bug costs most, and writes `prove-<area>` | writes prove-\<area\> | ship |
| [investigate](investigate/SKILL.md) | Answers a question, diagnoses a symptom, or settles a choice by prototype; opens no PR | drive-\<app\> | ship, shape-spec, resume-task |
| [learn-from-mistakes](learn-from-mistakes/SKILL.md) | Finds the layer that missed a mistake and proposes its fix; applies nothing unapproved | add-guardrail, create-app-driver | |
| [maintain-formal-verification](maintain-formal-verification/SKILL.md) | Brings formal checks back in line with the code; says drift or bug for each failure | updates prove-\<area\> | ship |
| [pause-task](pause-task/SKILL.md) | Stops a task safely with a resume note | | |
| [recall-context](recall-context/SKILL.md) | Rebuilds where a topic stands from past sessions and the repo | resume-task | |
| [resume-task](resume-task/SKILL.md) | Continues a task an earlier session left, without redoing what was done | ship, investigate, shape-spec, babysit-pr, ship-queue | recall-context |
| [say-it-plainly](say-it-plainly/SKILL.md) | Restates the last reply in plain words | | |
| [setup-repo](setup-repo/SKILL.md) | Prepares a repo the first time: tracker, labels, glossary, standards, driver | create-app-driver, add-guardrail | |
| [shape-spec](shape-spec/SKILL.md) | Turns a loose idea into a spec issue through an interview, or a map of decisions | investigate | resume-task |
| [sharpen-prompt](sharpen-prompt/SKILL.md) | Rewrites a prompt to ask for deeper work | | |
| [ship](ship/SKILL.md) | Turns one task into a ready-to-merge PR, proven and independently verified | investigate, analyze-impact, verify-pr, babysit-pr, create-app-driver, create-formal-verification, maintain-formal-verification, drive-\<app\> | ship-queue, resume-task |
| [ship-queue](ship-queue/SKILL.md) | Turns a list of tasks into as many PRs, one owner per task | ship | resume-task |
| [show-me](show-me/SKILL.md) | Shows the topic as the smallest clear visual | | |
| [test-skill-change](test-skill-change/SKILL.md) | Compares the old and new version of a skill blind | | |
| [verify-pr](verify-pr/SKILL.md) | Tries to break a PR and gives a verdict on behavior and on code | analyze-impact, drive-\<app\> | ship, babysit-pr |

Four skills also read part of another without running it, through `reads:`: `learn-from-mistakes` reads `ship` and `verify-pr`, to know where a lesson lands; `setup-repo` reads the glossary rules of `shape-spec`; `ship-queue` reads the reply format of `catch-me-up`; `verify-pr` reads the playbook duties and design red flags of `ship`.

`drive-<app>` and `prove-<area>` are not shipped by this framework: they are written for each repo, by the skills that point to them.
