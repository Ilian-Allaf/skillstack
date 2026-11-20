# validate-at-the-boundary

**Apply when** you wire validation, error handling, parsing, or a framework adapter.

**Rule.** Validate where data enters or leaves the system, trust it inside, and keep business logic in pure functions.

## How

- Boundaries are where data enters or leaves the system: CLI arguments, config files, environment variables, network and RPC payloads, files, database rows, IPC, external APIs. There, validate, parse into a domain type, and return errors.
- Inside, the data is typed and errors propagate. Nothing is validated twice, and no null check repeats what the boundary already ruled out.
- Business logic is pure functions with no framework dependency. Parsing turns raw input into typed state; scoring turns state into a result; rendering turns structured state into a string. The shell around them is thin and mechanical, so the logic is tested without the framework.
- Across a module boundary, expose domain concepts, never the transport, storage, framework, or wire types behind them. General mechanism goes inside; special-purpose policy stays at the edge.

## Test

For each check: is this data crossing a boundary right now? If not, the check is redundant. For each function that holds logic: could the shell call it as a pure function? If yes, extract it.

## Sign it was skipped

The same null check at three depths. A function that mixes a network call with a business rule. A database row type in a public signature.

## Example

```ts
// Skipped: the handler parses, decides, and writes; the rule cannot be tested without HTTP and a database.
app.post("/refund", async (req, res) => {
  const order = await db.orders.find(req.body.orderId);
  if (order && order.total > 0 && Date.now() - order.paidAt < 30 * DAY) {
    await db.refunds.insert({ orderId: order.id });
    res.send(200);
  } else res.send(400);
});

// Applied: parse at the edge, decide in a pure function, act in a thin shell.
const RefundRequest = z.object({ orderId: OrderIdSchema });

function refundDecision(order: Order, now: Instant): Refund | Refusal {
  if (order.total.isZero()) return { kind: "refused", reason: "nothing-paid" };
  if (now.since(order.paidAt) > REFUND_WINDOW) return { kind: "refused", reason: "window-closed" };
  return { kind: "refund", orderId: order.id, amount: order.total };
}

app.post("/refund", async (req, res) => {
  const { orderId } = RefundRequest.parse(req.body);
  const decision = refundDecision(await orders.get(orderId), clock.now());
  res.send(await refunds.apply(decision));
});
```
