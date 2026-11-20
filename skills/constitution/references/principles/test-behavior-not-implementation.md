# test-behavior-not-implementation

**Apply when** you write, change, or keep a test.

**Rule.** A test is a claim about what the code does for its users: a caller, an end user, or another service. Assert what they can observe through the interface they use, so the test fails when that behavior breaks and keeps passing when only the internals change.

## How

- Behavior is what users observe: return values, errors, state they can read back, and effects outside the code, such as a request sent, a row written, or a message emitted. Implementation is what they cannot: private helpers, internal call order, intermediate data, which collaborator did the work.
- Drive the code through its users' interface with a concrete input. Derive the expected value from the requirement, a known literal, or a worked example, never from a run of the code.
- Assert what the contract promises, no less and no more. An exact error message pins wording no caller reads; the error type callers branch on is the contract.
- The payload a mocked external service receives is behavior, because that service observes it. A call to an internal helper is implementation.
- When a test asserts that something did not happen, pair it with a case where it does, so the test shows it can see it.
- A test can pin an invariant instead of a call, such as a key that must exist in two tables. The invariant is the behavior.

## Test

Judge each test against two imagined edits:

1. **Break the behavior**: return a wrong value, skip an effect, or do it twice. If the test still passes, it proves nothing. The usual causes: an assertion looser than the contract, an expected value computed by the code under test, a restated constant the code never reads, an assertion on data the test built itself.
2. **Change the internals**: keep every observable result and restructure underneath. If the test now fails, it is pinned to the implementation and blocks every refactoring.

Keep a test that catches the first edit and survives the second. Rewrite or delete the rest.

## Sign it was skipped

Mocks of internal collaborators. A test that asserts a private method was called. A snapshot of an internal data structure. A test nobody saw fail.

## Example

```ts
// Skipped: pinned to the internals, blind to the result.
it("applies the discount", () => {
  const spy = vi.spyOn(pricing, "computeRate");
  checkout(cart);
  expect(spy).toHaveBeenCalled();
});

// Applied: the expected value comes from the requirement, through the public interface.
it("takes 10% off a cart over 100 euros", () => {
  const cart = cartOf({ price: euros(120) });
  expect(checkout(cart).total).toEqual(euros(108));
});
```
