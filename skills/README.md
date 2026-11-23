# Skills

You launch every skill yourself; the ones in the middle run inside a task. Not sure which to launch? `/choose-skill`. Every skill reads [the constitution](constitution/README.md) first.

## The map

```mermaid
flowchart TB
  you(("You"))

  subgraph launch ["You launch"]
    direction LR
    choose["choose-skill<br/><i>which skill?</i>"]
    setup["setup-repo<br/><i>first time in a repo:<br/>tracker, labels, docs</i>"]
    shape["shape-spec<br/><i>idea → spec</i>"]
    investigate["investigate<br/><i>answer, no PR</i>"]
    ship["ship<br/><i>try verification · build · audit evidence → ready PR</i>"]
    queue["ship-queue<br/><i>tasks → ready PRs, one owner each</i>"]
    pause["pause-task<br/><i>stop cleanly</i>"]
    resume["resume-task<br/><i>pick up where it stopped</i>"]
    recall["recall-context<br/><i>where things stand on a topic</i>"]
    catchup["catch-me-up<br/><i>what changed, what waits on you</i>"]
    cleanwt["clean-worktrees<br/><i>free disk, keep unsaved work</i>"]
    guard["add-guardrail<br/><i>mistake → check</i>"]
    cva["create-app-driver<br/><i>teach the agent your app</i>"]
    cfv["create-formal-verification<br/><i>prove one property, every case</i>"]
    mfv["maintain-formal-verification<br/><i>formal check back in line</i>"]
    learn["learn-from-mistakes<br/><i>recorded activity → fix the layer</i>"]
    testskill["test-skill-change<br/><i>old vs new skill, judged blind</i>"]
    sharpen["sharpen-prompt<br/><i>a deeper prompt</i>"]
    plain["say-it-plainly<br/><i>last reply, plain words</i>"]
  end

  subgraph task ["Inside a task"]
    direction LR
    impact["analyze-impact<br/><i>what else breaks?</i>"]
    verify["verify-pr<br/><i>independent findings · then replay proof</i>"]
    babysit["babysit-pr<br/><i>conflicts, review, CI</i>"]
  end

  subgraph repo ["In your repo"]
    direction LR
    drive[("drive-#lt;app#gt;<br/><i>launch · drive · observe</i>")]
    prove[("prove-#lt;area#gt;<br/><i>formal check</i>")]
    checks[("lints · types · tests")]
    tracker[("issue tracker")]
    pr[["PR labeled ready"]]
  end

  merge(("You merge"))

  constitution[/"constitution · read by every skill<br/><i>proof, coverage, glossary, PR format</i>"/]

  you --> launch
  choose -.->|points you to| ship
  setup --> cva
  setup -->|audit| guard
  shape -->|prototype| investigate
  shape -->|spec issue| tracker
  shape -.->|"you run /ship #spec"| ship
  ship -->|medium, high| impact
  ship -->|diagnose, or prototype a choice| investigate
  ship -.->|too big, open decisions| shape
  verify -->|breakage lane| impact
  ship --> verify
  ship --> babysit
  babysit -->|patch changed| verify
  task -->|drive the app| drive
  investigate --> drive
  impact -->|covered file| prove
  babysit --> pr
  ship -.->|context or quota runs low| pause
  pause -.->|next session| resume
  resume -->|carries on| ship
  resume -->|carries on| investigate
  resume -->|carries on| shape
  resume -->|carries on| babysit
  resume -->|carries on| queue
  recall -.->|one stopped task| resume
  queue -->|one owner per task| ship
  queue -.->|leaves worktrees| cleanwt
  queue -.->|reply shape| catchup
  catchup -->|reads| pr
  learn -.->|test a proposed fix| testskill
  sharpen -.->|you send it| ship
  pr --> merge
  cva --> drive
  cfv --> prove
  mfv --> prove
  ship -.->|stale check: issue| mfv
  ship -->|covered file: run, update| prove
  setup -.->|hard zones| cfv
  guard --> checks
  learn --> guard
  learn -->|feature map gap| cva
  learn -.->|verifier calibration| verify

  classDef person fill:#16a34a,stroke:#16a34a,color:#fff
  classDef entry fill:#eff6ff,stroke:#2563eb,color:#1e3a8a
  classDef inner fill:#f0fdfa,stroke:#0d9488,color:#134e4a
  classDef repoNode fill:#faf5ff,stroke:#7c3aed,color:#4c1d95,stroke-dasharray:4 3
  classDef shared fill:#f4f4f5,stroke:#71717a,color:#27272a
  class you,merge person
  class choose,setup,shape,investigate,ship,queue,pause,resume,recall,catchup,cleanwt,guard,cva,cfv,mfv,learn,testskill,sharpen,plain entry
  class impact,verify,babysit inner
  class drive,prove,checks,tracker,pr repoNode
  class constitution shared
```

## One task, from your words to your merge

```mermaid
flowchart TB
  go(("You:<br/>/ship task"))
  frame["1 · Frame, shown to you<br/><i>try verification setup,<br/>done_when red, cases, risk; high or hard zone:<br/>a verifier reads done_when first</i>"]
  design["2a · Design<br/><i>data shape; two sketches<br/>and a note when it crosses<br/>a function boundary</i>"]
  door{"One-way door,<br/>or you asked?"}
  shown{"You approve<br/>the design?"}
  build["2b · Build<br/><i>playbook, red → green,<br/>3 attempts</i>"]
  clean["3 · Clean<br/><i>comment hunter proposes a patch</i>"]
  proofs["4 · Prove every case<br/><i>base and head, on the app</i>"]
  impact["5 · Analyze impact<br/><i>medium, high</i>"]
  open["6 · Audit evidence and open the PR"]
  verdict{"7 · Fresh verifier:<br/>PASS?"}
  babysit["8 · Babysit<br/><i>conflicts, review, CI</i>"]
  ready[["ready"]]
  merge(("You<br/>merge"))
  human[["PR open, needs-human<br/><i>the call, a default,<br/>and what you could say</i>"]]

  go --> frame --> design --> door
  door -->|no| build
  door -->|yes| shown
  shown -->|yes| build
  shown -->|change it| design
  build -->|scrap the sketch, once| design
  build --> clean --> proofs --> impact --> open --> verdict
  build -->|"3 attempts spent,<br/>or a second scrap"| human
  verdict -->|first FAIL| build
  verdict -->|PASS| babysit --> ready --> merge
  verdict -->|"2 FAILs, FAIL upheld,<br/>or INCONCLUSIVE"| human
  babysit -->|"5 rounds, FAIL budget spent,<br/>INCONCLUSIVE, or a call for you"| human
  human -.->|your answer, in your words| build

  classDef you fill:#16a34a,stroke:#16a34a,color:#fff
  classDef stop fill:#fef2f2,stroke:#dc2626,color:#7f1d1d
  class go,shown,merge you
  class human stop
```

Green is you: you launch, you approve a design only when it goes through a one-way door or you asked to see it, and you merge. The task also stops for what only you can decide: a product or preference call no run can settle, or evidence that rules out what you asked for (rule 11 of the constitution). Nothing starts without you.

Every PR a skill opens, not only `ship`'s, goes through `verify-pr` and `babysit-pr` before it is `ready` (rule 2).
