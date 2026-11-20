# Where grep stops

Places a symbol search misses. Check each one that applies to the change.

| Place | What to check | How |
|---|---|---|
| Library source | the function you call does what its name says, at the version the repo pins, with any local patch | read the installed source under `node_modules`, `site-packages`, or the vendored copy; check the lockfile version |
| Execution order | when the code runs: microtasks, event loop turns, mount and unmount, teardown, retries | trace the call from its trigger; write a script that logs the order |
| Data on the wire | the JSON an API returns or accepts, headers, status codes | read the serializer and the client; call the endpoint |
| Data at rest | database columns, migrations, cached values, files on disk, local storage | read the schema and the migration; query a seeded database |
| Other readers | another service, a script, a job, or another language reading the same bytes | search the whole repo and its sibling repos for the table, key, or field name |
| Flags and config | feature flags, environment variables, build-time constants that change the path | find every place the flag is read; run with it on and off |
| Distance | callers two or three hops away, and code that receives the result | follow the return value, not only the call sites |
| Concurrency | two users, two tabs, a double click, a retry while the first call is still running | run the action twice at once in a script or in the app |
| Formal checks | a project-local `prove-<area>` skill lists a touched file among the files it covers | run its check. Green proves its property at level 4. Red is a confirmed risk with the counterexample, unless the covered files changed after the commit the skill recorded: then the model is stale, which is a note; when the builder runs this skill, it also opens an issue for the user to run the maintain pass, and the verifier never does |
| Error paths | what happens when the call fails, times out, or returns empty | force the failure: cut the network, return an error, pass empty input |

A place that does not apply is skipped by name, so the reader knows it was considered.
