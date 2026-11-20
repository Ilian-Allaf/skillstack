# design-for-the-consumer

**Apply when** you design an interface someone else uses: a screen, a CLI, an API, a library, a config format, an error message. And when implementation convenience competes with the consumer's result.

**Rule.** Choose the consumer's experience over the convenience of the implementation. The consumer is whoever uses the work: the end user of a screen, the colleague who imports a module, the engineer who maintains the code next.

## How

- Write the consumer's usage before the implementation: the quickstart, two or three call sites, the command they type. The usage is the spec; the types serve it.
- Every option, parameter, and control earns its place. Fewer, finished capabilities beat many rough ones.
- Get the details the consumer meets: defaults that work, names in their vocabulary, errors that say what to do next, the empty and failure states.
- Pull complexity into the callee, even when its implementation gets harder, so each caller stays simple.
- Explain the impact of a change from the consumer's side first, then what the next maintainer inherits.

## Test

Read the usage as the consumer, cold. Do they need to know an internal rule, pass a value they do not have, or handle a case the callee could handle?

## Sign it was skipped

An API that mirrors the implementation's steps. A required option every caller sets to the same value. An error message that names an internal function.

## Example

```ts
// Skipped: the caller drives the internal steps and handles a case the module owns.
const conn = await pool.acquire();
try {
  const raw = await conn.query(sql, params);
  return raw.rows.map(fromRow);
} finally {
  pool.release(conn);
}

// Applied: one call; the module owns the connection and the mapping.
const invoices = await invoicesRepo.unpaidFor(customerId);
```
