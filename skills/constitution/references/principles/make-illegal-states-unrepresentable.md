# make-illegal-states-unrepresentable

**Apply when** you design a type or a signature, in any typed language. The syntax for each language is in `languages/`, such as [typescript.md](../languages/typescript.md).

**Rule.** Make the compiler reject impossible states, mixed-up primitives, and unhandled variants. Define errors and special cases out of existence instead of adding handlers for them.

## How

- Model variants as a tagged union with one tag field, not a bag of optional fields.
- Brand semantic primitives. A `UserId` and an `OrderId` are both strings, but not interchangeable: give each its own type, a branded type or a newtype, made once by a function that checks it.
- External data is untyped until a parse function at the boundary turns it into the model (`validate-at-the-boundary`).
- Derive types from the schema that owns the shape: protocol buffers, OpenAPI, GraphQL, a migration, a design-token file. Never hand-write a parallel type.
- Make every switch over a variant exhaustive, so a new variant fails the build.
- Build the shape so the illegal value cannot be built: a non-empty list type, a start and a duration instead of two dates that must stay ordered.
- Keep the simplest type while every operation on it stays total. Strengthen it only where the loose type forces a cast, a `!`, or a "should never happen" throw.

## Test

List the states the code must never reach. For each, say what rules it out: a type, then a runtime check, then a comment, in that order of preference (`encode-lessons-in-structure`). A state ruled out only by a comment is a finding.

## Sign it was skipped

Optional fields that are always set in practice. Casts. Two parameters of the same primitive type that a caller can swap. A "should never happen" throw.

## Example

```ts
// Skipped: nothing stops a swap, and the comment holds the invariant.
function transfer(from: string, to: string, cents: number) {}
type Range = { start: Date; end: Date }; // start <= end

// Applied: the compiler holds both.
type AccountId = string & { readonly __brand: "AccountId" };
type Cents = number & { readonly __brand: "Cents" };
function transfer(args: { from: AccountId; to: AccountId; amount: Cents }) {}
type Range = { start: Date; durationMs: number };
```
