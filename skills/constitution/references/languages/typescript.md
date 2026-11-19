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

Another language gets its own file here, in the same shape, when a target repo needs it.
