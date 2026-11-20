# minimize-reader-load

**Apply when** you shape code, add a layer or a piece of state, or review a diff.

**Rule.** The cost of code is the work a reader does to understand it, on two axes: the layers between a question and its answer, and the state the reader must hold in their head. Lines of code and complexity scores are proxies. A change that lowers neither is reverted.

## How

- Collapse a layer that costs more than it saves: a wrapper with one caller, an adapter with one implementation, an indirection added for a need that never came.
- Each layer changes the abstraction. A layer that repeats the methods and arguments of the next one is a pass-through: remove it.
- Prefer a small interface that hides real decisions over a wide one the reader must learn on top of the implementation.
- Shrink the scope of state: a return value over a mutation, a local over a field, a field over module state, module state over a global. Derive a value instead of keeping two copies in sync.
- Name an invariant once, at the boundary that holds it, not in every consumer.
- Following one flow takes three files at most. If it takes more, flatten.
- Before you add a layer or a piece of state, check that it removes at least as much reader load elsewhere.

## Test

A new reader answers "where does X come from?" and "what can change X?" in under 30 seconds.

## Sign it was skipped

A chain of functions that pass the same arguments down. A flag set in one module and read in another. A cache kept in sync by hand.

## Example

```ts
// Skipped: two layers that add nothing, and a count kept in sync by hand.
class CartService { add(item: Item) { return this.repo.add(item); } }
class CartRepo { add(item: Item) { this.items.push(item); this.count++; } }

// Applied: one owner, and the count is derived.
class Cart {
  private items: Item[] = [];
  add(item: Item) { this.items.push(item); }
  get count() { return this.items.length; }
}
```
