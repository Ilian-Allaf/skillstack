# 0024. The architecture is shaped apart from the intent

- **Status**: accepted, 2026-11-27; amended by [0027](0027-behavior-is-settled-in-the-spec-the-shape-in-the-architecture.md).
- **Extends**:
  - in [0019](0019-the-spec-sets-the-bar-and-a-task-builds-the-proof-it-lacks.md), "writes nothing technical in the spec": the means of proof stay out of the spec, but a technical decision the user made goes in;
  - in [0014](0014-a-launched-task-runs-to-a-ready-pr.md), the stop for a one-way door: a door a technical decision of the spec settled needs no stop, since the user made that call.

  The rest of these ADRs stands.
- **Applies to**: `skills/shape-architecture/`, `skills/shape-spec/` (SKILL.md, `references/spec.md`, `references/grill.md`, `references/domain.md`), `skills/ship/` (`references/design.md`, `references/frame.md`, `references/design-note.md`, `references/clean.md`), `skills/verify-pr/references/` (`lanes.md` `spec` and `standards`, `verdict.md`), `skills/constitution/references/` (`architecture.md`, `sketch.md`, `glossary.md`, `target-repo.md`), `skills/setup-repo/references/trackers/`
- **Enforced by**: `tools/check_refs.py` (R003 fails on a path to `skills/ship/references/sketch.md` in a living doc, R006 to R009 and R012 on a missing row or edge of the new skill). The rest by review.

## Context

On 2026-11-27 the user asked whether the framework always hands the architecture to the builder. Reading the skills showed that it does, without saying so:

- The spec template had a Decisions section for modules, interfaces, schema changes, and architecture choices. But no branch of `shape-spec`'s grill asked about them, and the grill and the skill both said the spec holds nothing technical. The section stayed empty, or held the agent's guesses, which is what `shape-spec`'s hypothesis exists to prevent.
- `ship`'s design method (ground, two sketches, the red flags) is the framework's best tool for a shape, but it runs inside the task. The user sees the shape before code only through a one-way door or on request, and as a go or a pushback, not as a choice between shapes.
- A one-way door was found in `ship`'s design step, mid-task, when it could have been settled in the interview the user was already in.

The user wants the architecture decided with them when they want it, through what the framework already does well: the grill to ask, and the design method to advise. It must stay optional, and `ship` must know what was decided before it.

## Decision

### A skill of its own, optional
`shape-architecture` takes a spec issue. It sketches two shapes, puts the decisions they carry to the user in rounds, and writes the ones the user makes into the spec. A separate command makes the optional step visible, and lets the user run it later, or let someone other than the author of the intent run it.

### The design method moves to the constitution
Steps 1 to 4 of `ship`'s design (name the data shape, ground, sketch twice, screen) and the red flags move to `constitution/references/architecture.md`, and `sketch.md` moves beside it. `ship` follows them to pick a shape itself; `shape-architecture` follows them to put the choice to the user. `ship`'s design.md keeps what belongs to the build: how much design a change needs, the note, the stop before code, building against the sketch, and the scrap.

### Think in code, ask in decisions
`shape-architecture` sketches in code, as `ship` does, since a sketch in prose hides what makes a shape fail. The user is asked only what carries the shape: the choice between whole shapes, each one-way door, and each trade-off with a consequence for the product. An inner detail goes to the builder unasked. Every question offers "leave it to the builder".

### The decisions live in the spec
- The spec gains a section, Technical decisions, whose default says the shape is left to the builder.
- A decision the user makes is numbered `D1`, `D2`, with its reason, the shape it rejected, and any ADR. What they leave open is listed under Left to the builder.
- The section names the base commit it was grounded on and the modules the decisions touch, so any machine can tell a stale decision. The sketches, with their paths, are saved to `sketches/<spec>/` in the project folder, never shared, as input to `ship`'s grounding on the same machine, never as its draft.
- A decision on the shape the user states in `shape-spec`'s grill goes in the same section. The old Decisions section keeps the product decisions only.
- The spec issue is edited in place, so `ship` and the verifier read one issue. The trackers gain the operation Edit an issue.

### `shape-spec` offers it, on a signal
Before its hand over, `shape-spec` has a subagent look for four signals in the code the spec touches: a one-way door, two viable whole shapes, a piece of state that changes owner or a new boundary, an accepted ADR the spec comes close to. With one, it names it and asks; on a yes, it runs `shape-architecture` in the same session, which is the user's launch ([ADR 0006](0006-skills-are-launched-by-the-user-and-route-by-path.md)). Without one, it hands over `/ship` and says the builder picks the shape alone. The signals live in `shape-architecture`, once. Launched with a signal, `shape-architecture` goes on without asking again; it never reshapes a spec a `ship` task is building, and its ADRs and terms land as `shape-spec`'s domain.md says.

### `ship` builds within the decisions
- The frame names them and what they leave open. When a module the Grounded on line names changed since its commit, or the line is missing, `ship` grounds it again and checks each decision.
- Both sketches keep every decision and differ only on what is open. With nothing open across a boundary, there is one sketch.
- A one-way door a decision settled needs no stop before code.
- A decision the code contradicts is evidence against what the user asked for, one of rule 11's existing stops. Found before any body is filled, it stops the task. Found during the build, it goes under Deviations with its id, and the PR opens `needs-human`.
- The user's answer replaces the decision: `ship` writes it into the section under a new id that names the old one and quotes the answer, supersedes any ADR the old one linked, and builds within it.
- A decision the builder would rather change, with no evidence against it, stays, and the builder's case goes under Questions before the merge.

### The verifier checks them
The `spec` lane checks the diff against each decision the spec holds now. A breach is proven by quoting the decision and the hunk, as for an ADR, and graded `should`, whether or not Deviations names it: a builder cannot excuse its own breach. A replaced decision has left the spec, and its replacement quotes the user's answer, which the lane checks.

## Alternatives rejected

- **A mode of `shape-spec`**: one skill fewer, but an optional step hidden in a mode is one the user does not find or does not know when to run. The user chose the separate command.
- **An architecture branch in `shape-spec`'s grill, always visited**: it makes every spec pay for a design interview, and mixes what with how in one session.
- **A copy of the design method in the new skill**: two copies drift on the first change; the method has one home.
- **The decisions as a comment on the spec**: a second place for `ship` and the verifier to look, and a rerun would add a comment instead of replacing the section.
- **Two strengths of decision, the user's and the agent's recommendation accepted**: the line rested on how the user answered, which no reader can see later. "Leave it to the builder" draws the line explicitly.
- **`ship` going on past a contradicted decision found before code**: it builds a PR on a premise the user ruled out; the stop then costs only the frame.

## Consequences

- Every spec hand over costs one subagent that looks for the signals. A spec with one takes one more question, and, on a yes, one more interview.
- A tracker file written from a template before this ADR has no Edit an issue: the first skill that needs it copies the heading from the template, as the tracker README now says. A file written from `other.md` gets it from the user.
- The sketches stay on the machine that made them. Another machine reads the decisions and their Grounded on line, which is enough to build and to check staleness.
- A `ship` run on a spec without technical decisions behaves as before.
- These ideas are ours, from the session of 2026-11-27. The design method keeps its sources, pstack's `architect` (Lauren Tan); the rounds keep theirs, Matt Pocock's `grilling`.
