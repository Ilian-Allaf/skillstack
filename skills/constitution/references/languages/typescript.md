# Language rules: TypeScript

Read when the diff touches a `.ts` or `.tsx` file, as the builder in `build` and as the verifier in the `standards` lane. A documented repo standard wins over this file. Rules a linter already enforces are not repeated in review.

| Rule | Summary |
|---|---|
| discriminated unions | Model variants with a `kind` literal so impossible states cannot be represented. No bags of optional fields. |
| branded types | Brand primitives (`string & { readonly __brand: "UserId" }`) so they cannot be mixed up. A brand comes from a type guard that checks, never from `as`. |
| constructive types | Build the shape so the illegal value cannot be built: `[T, ...T[]]` for non-empty, `start` plus `duration` for a range. |
| simplest total type | Keep `T[]` while every operation stays total. Strengthen it only where the loose type forces `!`, a cast, or a "should never happen" throw. |
| `unknown` over `any` | External data is `unknown` until parsed. |
| schemas before guards | Use the repo's runtime schema library and infer the type from it before writing a guard by hand. |
| no `as` | Cast only after validation. |
| narrowing order | discriminant switch, then `in`, then `typeof` or `instanceof`, then a type guard, then `as` last. |
| honest guards | A guard named `isX` checks every claim it makes. A lying guard is worse than `as`. |
| exhaustiveness | `const _exhaustive: never = x;` in default arms, so a new variant fails the build. |
| `satisfies` over `as` | Checks the value without widening literal types. |
| parse at the boundary | Data that crosses in becomes a named domain type at the boundary. Inside, trust the types. |
| derived types | `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, `typeof` before a new interface. |
| object arguments | Pass an object, not positional arguments, except on hot paths. |
| real tests | Do not mock what can run locally. |
| structured logs | A structured logger with enough context to debug from an id. No `console.log` in shipped code. |

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

// Applied: the repo's schema library validates, and the type is inferred from it.
const UserSchema = z.object({ id: z.string().uuid(), role: z.enum(["admin", "member"]) });
type User = z.infer<typeof UserSchema>;
const parseUser = (input: unknown): User => UserSchema.parse(input);

// When the type comes first, annotate the schema with it, so a schema that proves less fails to compile.
const userSchema: z.ZodType<User> = z.object({ id: z.string().uuid(), role: z.enum(["admin", "member"]) });
```

To remove an `as` from existing code, find why the compiler cannot infer: a missing tag (add one), a source type too wide (narrow it), an untyped boundary (parse it), or a fact the types cannot say (brand it, or use `satisfies`).

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

Another language gets its own file here, in the same shape, when a target repo needs it.
