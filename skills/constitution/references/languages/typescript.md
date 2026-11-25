# Language rules: TypeScript

Read when the diff touches a `.ts`, `.tsx`, `.mts`, or `.cts` file, as the builder in `build` and as the verifier in the `standards` lane. A documented repo standard wins over this file. Rules a linter already enforces are not repeated in review.

Each rule has an id. The user decides per id, for each repo, in `lint/typescript.md` of the project folder: a rule turned off there is neither checked nor judged in review. A rule with a check also runs in the lint pass on the lines a change adds or edits; [lint.md](../lint.md) says how, and what blocks.

| Id | Rule | Check |
|---|---|---|
| `discriminated-unions` | Model variants with a `kind` literal so impossible states cannot be represented. No bags of optional fields. | review |
| `branded-types` | Brand primitives (`string & { readonly __brand: "UserId" }`) so they cannot be mixed up. A brand comes from a type guard that checks, never from `as`. | review |
| `constructive-types` | Build the shape so the illegal value cannot be built: `[T, ...T[]]` for non-empty, `start` plus `duration` for a range. | review |
| `simplest-total-type` | Keep `T[]` while every operation stays total. Strengthen it only where the loose type forces `!`, a cast, or a "should never happen" throw. | review |
| `unknown-at-the-boundary` | External data is `unknown`, never `any`, until parsed, and it is parsed where it enters. | review |
| `no-unknown-parameters` | A parameter is never `unknown`, except the subject of a type guard and an error's `cause`. | lint |
| `no-unknown-returns` | A function never returns `unknown`, `Promise<unknown>`, or an alias of them: it returns the parsed type. | lint |
| `no-unknown-type-aliases` | No alias resolves to `unknown`. | lint |
| `no-unsafe-dictionary-type` | No dictionary of `unknown`, `any`, `object`, or `{}` values, such as `Record<string, unknown>`, as a contract. A generic bound may use one. | lint |
| `no-object-parameters` | A parameter is never typed `object`: it names the type it needs. | lint |
| `schemas-before-guards` | Use the repo's runtime schema library and infer the type from it before writing a guard by hand. | review |
| `no-as` | Cast only after validation, and only for a fact the types cannot say. | review |
| `require-safety-comment-for-type-assertion` | An `as` other than `as const` has a `// SAFETY: <invariant>` comment just above it that says why it holds. | lint |
| `no-chained-type-assertions` | Never chain casts (`x as object as User`): that builds a type no check proved. | lint |
| `no-widen-then-assert` | Never widen a known value to `unknown`, `any`, or `object`, then cast it back. | lint |
| `narrowing-order` | Discriminant switch, then `in` or `instanceof`, then a schema or a type guard, then `as` last. | review |
| `no-runtime-typeof` | `typeof` narrows only inside a type guard, or to probe that a global exists (`typeof window === "undefined"`). Elsewhere, parse at the boundary. | lint |
| `honest-guards` | A guard named `isX` checks every claim it makes. A lying guard is worse than `as`. | review |
| `exhaustiveness` | `const _exhaustive: never = x;` in default arms, so a new variant fails the build. | review |
| `satisfies-over-as` | Checks the value without widening literal types. | review |
| `no-known-value-widening` | Do not annotate a known value with a wider type (`const handlers: Record<string, Handler> = { start }` loses the key `start`); keep inference, or use `satisfies`. | lint |
| `no-reflect-get` | Read a property by typed access, or parse the value first; never `Reflect.get`. | lint |
| `no-reflect-apply` | Call the function; never `Reflect.apply`. | lint |
| `derived-types` | `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof` before a new interface. | review |
| `object-arguments` | Pass an object, not positional arguments, except on hot paths. | review |
| `no-conditional-empty-object-spread` | No `...(cond ? { a } : {})`: omitting a key and setting it to `undefined` differ, so write which one you mean. | lint |
| `no-reduce-accumulator-copy` | A reducer mutates the fresh accumulator it owns and returns it; copying it at each step is quadratic. | lint |
| `real-tests` | Do not mock what can run locally. | review |
| `no-module-mocking` | No `vi.mock` or `jest.mock`: pass the dependency through a seam the test can fill. | lint |
| `structured-logs` | A structured logger with enough context to debug from an id. No `console.log` in shipped code. | review |

## Examples

Each pair shows the rule skipped, then applied. The principle behind them is `make-illegal-states-unrepresentable`.

### Discriminated unions

```ts
// Skipped: a flag and optional fields allow contradictory states.
type DiffState = { loading: boolean; diff?: GitDiff; error?: string };

// Applied: only valid states exist. Pick one tag name (`kind`) and keep it.
type DiffState =
  | { kind: "loading" }
  | { kind: "ready"; diff: GitDiff }
  | { kind: "error"; error: string };
```

### Branded types

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function isAgentId(input: string): input is AgentId {
  return isUuid(input);
}

function parseAgentId(input: string): AgentId {
  if (!isAgentId(input)) throw new Error(`Invalid agent id: ${input}`);
  return input;
}
```

### Constructive types and the simplest total type

```ts
type NonEmpty<T> = [T, ...T[]];
const isNonEmpty = <T>(xs: T[]): xs is NonEmpty<T> => xs.length > 0;

// Skipped: the loose type forces a lie at the use site.
const newest = (sessions: Session[]): Session => sessions[0]!;

// Applied: the input type carries the fact; the `!` disappears.
const newest = (sessions: NonEmpty<Session>): Session => sessions[0];

// Keep `T[]` where every operation is total: an empty list sums to 0.
const sum = (xs: number[]) => xs.reduce((a, b) => a + b, 0);
```

### `unknown`, schemas, and no `as`

```ts
// Skipped: a cast, or a guard that checks less than it claims.
const user = data as User;
const isUser = (d: unknown): d is User => typeof d === "object" && d !== null && "id" in d;

// Applied: the repo's schema library validates where the data enters, and the type is inferred from it.
const UserSchema = z.object({ id: z.string().uuid(), role: z.enum(["admin", "member"]) });
type User = z.infer<typeof UserSchema>;
const user = UserSchema.parse(await response.json());

// When the type comes first, annotate the schema with it, so a schema that proves less fails to compile.
const userSchema: z.ZodType<User> = z.object({ id: z.string().uuid(), role: z.enum(["admin", "member"]) });
```

No helper takes `unknown` and passes it on (`parseUser(input: unknown)`): the schema is called at the boundary itself, so `unknown` never reaches a signature.

To remove an `as` from existing code, find why the compiler cannot infer: a missing tag (add one), a source type too wide (narrow it), an untyped boundary (parse it), or a fact the types cannot say (brand it, or use `satisfies`). An `as` that survives says why it holds:

```ts
// SAFETY: the map was filled from the same ids one line above, so every lookup hits.
const owner = owners.get(id) as Owner;
```

### Exhaustiveness

```ts
function area(s: Shape): number {
  switch (s.kind) {
    case "circle":
      return Math.PI * s.radius ** 2;
    case "rect":
      return s.width * s.height;
    default: {
      const _exhaustive: never = s;
      return _exhaustive;
    }
  }
}
```

### `satisfies` over `as`

```ts
const config = { theme: "dark", cols: 3 } as Config; // Skipped: widened, and unchecked
const config = { theme: "dark", cols: 3 } satisfies Config; // Applied: checked; `theme` stays "dark"
```

### Derived types

```ts
// Skipped: a copy of the generated type, which drifts when the schema changes.
type CheckSummary = { totalCount: number; checks: { name: string; status: string }[] };

// Applied: derived from the type the schema generates.
type CheckSummary = Pick<ChecksMessage, "totalCount" | "checks">;
```

### Object arguments

```ts
openFile(uri, 10, 1, 10, 1); // Skipped: swap two numbers and it still compiles
openFile({ uri, selection: { startLine: 10, startColumn: 1, endLine: 10, endColumn: 1 } }); // Applied
```

Another language gets its own file here, in the same shape and with ids, when a target repo needs it; its checks, if a linter can hold some of its rules, go in a pack of their own, as [lint.md](../lint.md) says.
