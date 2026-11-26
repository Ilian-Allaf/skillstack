# Glossary

One word per idea. Skills, PRs, and verdicts use the English term. The French column is how the user says it. `tools/lint_skills.py` fails on any term in the Avoid column outside this file.

The target repo can have its own glossary of domain terms. The builder and the verifier read it too.

| Term | Français | Meaning | Avoid |
|---|---|---|---|
| task | tâche | what the user asks for and launches, in one `/ship` | `ticket` |
| unit | unité | one PR of a task, green on its own check; a task is one unit, or several when it spans several PRs, stacked | `work item` |
| issue tracker | issue tracker | the tool where tasks, specs, maps, and bugs live, such as GitHub Issues, GitLab, Linear, or markdown files; `issue-tracker.md` in the project folder says which and how | `ticket tracker` |
| issue | issue | one item in the issue tracker | |
| code host | code host | where the repo, its pull requests, and its CI live, such as GitHub | |
| builder | builder | the agent that carries a PR from `frame` to ready | `implementer`, `coder agent` |
| verifier | vérificateur | the fresh agent that tries to break a PR, with no write access | `QA agent`, `checker agent` |
| subagent | sous-agent | an agent spawned with a brief and a fresh context | `sub-agent`, `child agent` |
| `done_when` | fini quand | the observable finish condition, red on the base | `acceptance criteria`, `definition of done` |
| run | exécution | the proof of a claim or a finding: the exact command, the output it printed, and the output the task requires | |
| evidence | preuve | something observed in this session, replayable | `proof of work` |
| certainty level | niveau de certitude | 1 said, 2 pointed, 3 reasoned, 4 ran, 5 reproduced | `confidence score` |
| safety fact | fait de sûreté | the one fact a change is safe because of | |
| risk class | classe de risque | `low`, `medium`, or `high`; sets how deep verification goes | `risk level` |
| hard zone | zone difficile | where models fail most; the one list is in `proof.md` | |
| lane | lane | one question the verifier answers, such as `live` or `spec` | `check type` |
| verdict | verdict | PASS, FAIL, or INCONCLUSIVE, per axis, on one base and head pair | `LGTM` |
| axis | axe | behavior or code; each gets its own verdict | |
| note | note | a finding that does not block; listed in the verdict comment, an issue only when the user asks | |
| ready | prête | the PR needs nothing but the user's merge; label `ready` | `merge-ready` |
| round | round | one pass of `babysit-pr` after something changed on the PR | |
| `needs-human` | needs-human | a label: the run stopped on a call only the user can make; the user's answer, in their own words, restarts it | `escalated` |
| escaped | échappé | a bug found after merge; label `escaped` | |
| door | porte | `two-way` if a choice can be undone cheaply, `one-way` if not | `reversibility` |
| case | cas | one situation the evidence must show: an entry point, an edge case, the main path | `scenario` |
| journey | parcours | the steps a user takes on one surface and the result they expect; a spec states one per user story, and each is a case | `user flow` |
| promise | promesse | what must never break, in one product sentence with the harm when it breaks; a spec lists them under Promises, and each is a case. One about every order of steps or every input is a property, which a formal check can prove | `guarantee` |
| heavy visual change | changement visuel lourd | a story that adds a screen, redesigns one, or builds a page whose look is the point; a small change on an existing screen is not one | |
| visual target | cible visuelle | what a user picked from prototypes: a still, a screen captured at a state and a width, or a motion, a recording with its effect list; a spec lists them under Visual targets, and each is a case | `mockup` |
| effect list | liste d'effets | a motion read frame by frame, one line per effect: the trigger, what moves, the duration, the easing, the direction | |
| design mode | mode de design | how a visual change uses the repo's design system: `follow`, `extend`, or `break away`; the spec states it | |
| target loop | boucle de cible | the passes `ship` makes until the head holds up next to each visual target, each pass scored by critics | |
| critic | critique | a fresh subagent that scores one pass of the target loop from side-by-side images, the criteria, and a motion target's effect list alone; its score steers the loop, at proof level 1 | |
| case list | liste des cas | the numbered cases `frame` fixes before any code, shown in the frame | |
| seam | seam | a public interface the tests drive, agreed in `frame` or the spec | |
| patch id | patch id | the hash of the diff, `git patch-id --stable`; unchanged does not make a verdict reusable | |
| coverage table | table de couverture | the PR's table of cases, each with its evidence and certainty level | `test matrix` |
| coverage gap | trou de couverture | a case missing from the coverage table that the verifier drove and found correct | |
| demo | démo | the video assembled from one scripted clip per case, with captions | `screencast` |
| formal check | check formel | a project-local `prove-<area>` skill that checks one property over every order of steps, or every input up to a bound; `create-formal-verification` writes it | |
| sync commit | commit de synchro | the commit at which a formal check was last confirmed to describe the code it covers, with its date and the content id of each covered file | |
| stale | périmé | said of a formal check whose covered files no longer match the content ids it records, or of a feature file whose code changed after the commit it was last driven at; what it says proves nothing until it is checked again | |
| feature map | feature map | one file per user-facing feature in `drive-<app>` | `feature list` |
| seeded defect | défaut semé | a bug planted in a real PR to test the verifier | `fake bug` |
| pin | pin | a test, snapshot, or script that captures today's behavior before a refactoring moves structure | `golden master` |
| sketch | esquisse | types, signatures, and module layout with empty bodies, made before code | |
| design note | note de conception | the one-page rationale of a sketch: usage, shape, tradeoffs, rejected alternatives, deviations; in the PR's Design section | |
| comment hunter | chasseur de commentaires | the fresh subagent in `clean` that deletes comments and flags `MUST KILL` | |
| `MUST KILL` | MUST KILL | a symbol the comment hunter flags for a reshape that makes a comment unneeded | |
| spec | spec | an issue labeled `spec`: problem, solution, `done_when`, user stories with their journeys, promises, seams, decisions; written by `shape-spec` | `PRD` |
| map | carte | an issue labeled `map` that charts decisions for work too big for one session | `roadmap issue` |
| decision issue | issue de décision | one question on a map, resolved in one session | `decision ticket` |
| frontier | frontière | the open decisions whose prerequisites are settled | |
| swarm | essaim | several workers on slices of one job, or racing on one brief; one report | |
| decision log | journal de décisions | the append-only TSV of decisions of a long run | `audit trail` |
| repo glossary | glossaire du repo | the target repo's own domain terms: `glossary.md` in the project folder, or the team's file it routes to | |
| ADR | ADR | a dated file in `adr/` of the project folder, or the team's folder it routes to, recording a decision that is hard to reverse, with its status and the paths it applies to; superseded, never rewritten | |
| project folder | dossier projet | `~/.agents/projects/<project>/`, outside the repo: the working files the framework keeps for one repo, private unless the user shares an entry with the team | `home repo` |
| route | route | a file of the project folder whose one line says the entry lives in the repo, and where | `pointer file` |
| playbook | playbook | the proof duties of `build` for one kind of task | |
