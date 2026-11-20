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
    ship["ship<br/><i>task → ready PR</i>"]
    queue["ship-queue<br/><i>tasks → ready PRs, one owner each</i>"]
    pause["pause-task<br/><i>stop cleanly</i>"]
    resume["resume-task<br/><i>pick up where it stopped</i>"]
    recall["recall-context<br/><i>where things stand on a topic</i>"]
    catchup["catch-me-up<br/><i>what changed, what waits on you</i>"]
    cleanwt["clean-worktrees<br/><i>free disk, keep unsaved work</i>"]
    guard["add-guardrail<br/><i>mistake → check</i>"]
    cva["create-app-driver<br/><i>teach the agent your app</i>"]
    learn["learn-from-mistakes<br/><i>bug got through → fix the layer</i>"]
    testskill["test-skill-change<br/><i>old vs new skill, judged blind</i>"]
    sharpen["sharpen-prompt<br/><i>a deeper prompt</i>"]
    plain["say-it-plainly<br/><i>last reply, plain words</i>"]
  end

  subgraph task ["Inside a task"]
    direction LR
    impact["analyze-impact<br/><i>what else breaks?</i>"]
    verify["verify-pr<br/><i>fresh verifier tries to break it</i>"]
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
  ship -->|prototype a choice| investigate
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
  recall -.->|one stopped task| resume
  queue -->|one owner per task| ship
  queue -.->|leaves worktrees| cleanwt
  queue -.->|reply shape| catchup
  catchup -->|reads| pr
  learn -.->|test a proposed fix| testskill
  sharpen -.->|you send it| ship
  pr --> merge
  cva --> drive
  cva -->|formal mode| prove
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
  class choose,setup,shape,investigate,ship,queue,pause,resume,recall,catchup,cleanwt,guard,cva,learn,testskill,sharpen,plain entry
  class impact,verify,babysit inner
  class drive,prove,checks,tracker,pr repoNode
  class constitution shared
```

## One task, from your words to your merge

```mermaid
flowchart TB
  go(("You:<br/>/ship task"))
  frame["1 · Frame, shown to you<br/><i>done_when red on the base,<br/>cases, risk</i>"]
  design["2a · Design<br/><i>data shape; two sketches<br/>and a note when it crosses<br/>a function boundary</i>"]
  door{"One-way door,<br/>or you asked?"}
  shown{"You approve<br/>the design?"}
  build["2b · Build<br/><i>playbook, red → green,<br/>3 attempts</i>"]
  clean["3 · Clean<br/><i>comment hunter</i>"]
  proofs["4 · Prove every case<br/><i>base and head, on the app</i>"]
  impact["5 · Analyze impact<br/><i>medium, high</i>"]
  open["6 · Open the PR"]
  verdict{"7 · Fresh verifier:<br/>PASS?"}
  babysit["8 · Babysit<br/><i>conflicts, review, CI</i>"]
  ready[["ready"]]
  merge(("You<br/>merge"))
  human[["PR open,<br/>needs-human"]]

  go --> frame --> design --> door
  door -->|no| build
  door -->|yes| shown
  shown -->|yes| build
  shown -->|change it| design
  build -->|scrap the sketch, once| design
  build --> clean --> proofs --> impact --> open --> verdict
  build -->|"3 attempts spent,<br/>or a second scrap"| human
  verdict -->|"FAIL, 2 at most"| build
  verdict -->|PASS| babysit --> ready --> merge
  verdict -->|"2 FAILs, FAIL upheld,<br/>or INCONCLUSIVE"| human
  babysit -->|5 rounds spent| human

  classDef you fill:#16a34a,stroke:#16a34a,color:#fff
  classDef stop fill:#fef2f2,stroke:#dc2626,color:#7f1d1d
  class go,shown,merge you
  class human stop
```

Green is you: you launch, you approve a design only when it goes through a one-way door or you asked to see it, and you merge. Nothing else waits on you, and nothing starts without you.
