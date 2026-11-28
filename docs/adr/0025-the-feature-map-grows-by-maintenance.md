# 0025. The feature map grows by maintenance, not by a check

- **Status**: accepted, 2026-11-28. Amends [0021](0021-the-skill-graph-is-the-executed-map.md): a feature map is no longer one of its executed docs.
- **Applies to**: `skills/create-app-driver/`, `skills/maintain-app-driver/`, `skills/constitution/references/coverage.md`, `skills/learn-from-mistakes/`
- **Enforced by**: review; `maintain-app-driver` finds the features the map lacks at each pass

## Context

ADR 0021, after 0013, keeps a doc only if a check fails when it disagrees with the code, and counted the "Declared in" line of a feature map as one: `create-app-driver` wrote a check that failed when an entry point the code declares had no feature file. The same step asked for the top 3 to 5 features only. On a large app, with dozens of routes, the check failed on the first day, and the only way to pass it was to map the whole app in the first run, which takes hours.

pstack, where the driver comes from, has no such check. Its map starts with a few features and is completed by a maintenance pass that reads every feature from the source, drives every one live, and runs often.

## Decision

- `create-app-driver` maps 3 to 5 features and writes no entry-point check. A feature file lists its entry points by hand, from the user's point of view.
- `maintain-app-driver`, a skill of its own, replaces the maintain mode of `create-app-driver`. Each pass checks every feature file against the source, drives every feature, and maps at most five features the map lacks, those a `learn-from-mistakes` row named first.
- A feature map is the one doc kept by maintenance instead of a check: `Last driven` dates each file, and a file whose code changed after it is stale until driven again.
- The user launches it whenever the app has changed, by hand or from a schedule of their own, as [ADR 0026](0026-a-schedule-is-the-users-own.md) allows.
- A path the map lacks is still caught in a task: coverage finds the callers of the changed code in the code itself, and adds a missing path to the map where the driver lives: in the PR when the driver is in the repo, in the project folder otherwise.

## Alternatives rejected

- **Keep the check, with a baseline of the entry points unmapped on the first day**: it keeps the map executed, but adds a file to keep beside the map, and still blocks the first PR that touches an unmapped route on mapping it.
- **Keep the maintain mode inside `create-app-driver`**: the two jobs share no trigger and no output. `create-app-driver` runs once, when a surface has no driver, and ends with a driver; the maintenance pass runs often, over every driver, takes a `learn-from-mistakes` row as its argument, and ends on `clean`, `changed`, or `blocked`. As a mode, it could not be launched by name, by the user or by a schedule of theirs, nor routed to by `learn-from-mistakes` and `choose-skill` without naming the mode too; and its steps doubled the length of a skill most runs use once. No other skill reads the source of each feature and drives it live.
- **Map the whole app in the first run**: hours on a large app before the first proof, and most of the map is never driven again before it goes stale.

## Consequences

Between two passes, a new route can sit outside the map unseen; the next pass finds it. A stale map shows in the frame through `Last driven`, as before. An incomplete one shows in the reply of the last pass, which lists the features still missing with their source paths; `Last driven` dates only the files that exist. ADR 0021's Enforced by line still names the entry-point check this ADR removes; for the feature map, this ADR holds. `tools/check_refs.py` lists the removed `references/maintain.md` under `REMOVED`.
