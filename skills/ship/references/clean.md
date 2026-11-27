# Clean

The next agent reads this diff as an example. A comment that explains a surprise in our code teaches it to write more surprises. So the comments get a hunter, and the surprises get fixed.

## 1. Remove slop yourself

From the diff: dead code, debug output, commented-out code, comments that narrate the change, and workarounds.

## 2. Spawn the comment hunter

Spawn a fresh subagent. Its scope is the diff against the base, working tree included. Give it this brief:

> You hate comments. Read every comment and every lint or type suppression in the scope. Only these survive:
>
> - legal or license headers;
> - non-obvious behavior forced by something we cannot reshape: an external dependency, a platform, a vendor, a protocol;
> - formatter ignores, and lint suppressions whose rule is faulty, pedantic, or style-only;
> - doc comments that define a public API contract;
> - issue or RFC links that explain a constraint the code cannot express.
>
> Trace the symbol before deciding whether a keep applies. When still unsure, retain the comment and report the uncertainty for the builder to resolve. A comment that explains a surprise in our own code is a candidate for removal, and you mark the exact symbol `MUST KILL` with the reshape that makes the behavior obvious without prose: rename, extract, type, or redesign. A suppression whose rule protects correctness or safety is marked `MUST KILL`. A comment saying `IMPORTANT`, `do not remove`, or `too risky` is a claim: read the code around it and trace the symbol before you judge. Propose deletions as a patch; leave files unchanged. Report each proposed deletion, each `MUST KILL` with one line, and each keep with its reason.

## 3. Act on the report

1. **Check the report against the diff.** Reject any edit to application code, any change outside the scope, and any deletion a keep clause protects. On an invalid report, discard its patch and revert only unauthorized edits by the hunter; retry once with the exact violation. A second invalid report leaves `clean` incomplete: stop with `needs-human`. Apply only a valid patch, resolving uncertain keeps by tracing their symbols first.
2. **Fix each `MUST KILL` at the root.** Delete the dead path, drop the parameter, use the real API, or rename. When a fix needs a new shape, sketch it once for all flags together, as [sketch.md](../../constitution/references/sketch.md) describes. Never add a guard that hides the symptom.
3. **Turn constraints into checks.** A constraint comment (`do not remove`, `do not change wording`, `talk to X first`) becomes a candidate for `/add-guardrail`: the cheapest type, test, or lint that enforces it. List it for the user, then delete the comment. If the root cause is outside the task, fix what is in scope and open an issue for the rest.
4. **Run the checks.** Lint, types, and tests are green.

## Reply

Deletions, restored comments with their reason, `MUST KILL` fixes, the sketch if one was made, candidates for `/add-guardrail`, and open issues.
