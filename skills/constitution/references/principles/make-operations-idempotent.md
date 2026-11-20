# make-operations-idempotent

**Apply when** you design a command, a lifecycle step, a migration, a sync, or a loop that runs amid crashes and retries, and for every step of a skill that can be rerun.

**Rule.** An operation converges to the same end state however many times it runs and wherever the last run stopped.

## How

- Derive each step from the state that exists, not from what the last run meant to do: read the current state, compare it with the goal, and apply only the difference. A repeat then finds nothing left to do.
- Anything a run leaves behind, such as a lock, a temporary file, a half-written record, or a claimed job, must be recognizable as stale by the next run, from evidence that holds wherever the last run stopped.
- Write to a temporary path and rename it into place. Compare artifacts by content, not by creation order. Key a side effect by an id the caller chooses, so a retry is recognized.

## Test

What happens if it runs twice in a row? What happens if the last run crashed at each possible point? If an answer is "it depends on what was left behind", the operation needs a reconciliation step.

## Sign it was skipped

A rerun fails on "already exists". A crash needs a manual cleanup before the next run. A retry charges twice.

## Example

```ts
// Skipped: a retry after a timeout sends a second invoice.
async function sendInvoice(orderId: OrderId) {
  await mailer.send(renderInvoice(orderId));
  await db.orders.update(orderId, { invoiced: true });
}

// Applied: the effect is keyed by the order, and the state says what is left to do.
async function sendInvoice(orderId: OrderId) {
  const order = await db.orders.get(orderId);
  if (order.invoiceSentAt) return;
  await mailer.send(renderInvoice(order), { idempotencyKey: `invoice-${orderId}` });
  await db.orders.update(orderId, { invoiceSentAt: clock.now() });
}
```
