---
name: webhooks
description: Webhooks HTTP callbacks for events. Use for integrations.
---

# Webhooks

Webhooks are "user-defined HTTP callbacks". They are triggered by some event in a source system (e.g., Stripe, GitHub) and sent to a destination system (Your API) to notify it.

## When to Use

- **Payment Confirmations**: Stripe notifying you a payment Succeeded.
- **CI/CD**: GitHub notifying Jenkins that code was pushed.
- **Async Processing**: A 3rd party AI service notifying you that generation is complete.

## Quick Start

```typescript
// Your Webhook Handler (Receiver)
app.post(
  "/webhooks/stripe",
  express.raw({ type: "application/json" }),
  (req, res) => {
    const signature = req.headers["stripe-signature"];

    try {
      // Verify the event came from Stripe and hasn't been tampered
      const event = stripe.webhooks.constructEvent(
        req.body,
        signature,
        START_SECRET,
      );

      if (event.type === "payment_intent.succeeded") {
        fulfillOrder(event.data.object);
      }

      res.json({ received: true });
    } catch (err) {
      res.status(400).send(`Webhook Error: ${err.message}`);
    }
  },
);
```

## Core Concepts

### Verification (Security)

Since Webhook endpoints are public, anyone can POST to them. You must verify the **Signature** (HMAC) usually sent in a header to prove the sender's identity.

### Retries

If your server returns an error (500) or times out, the sender usually retries with exponential backoff. Your endpoint must be **Idempotent**.

## Best Practices

**Do**:

- Respond **Immediately (200 OK)**. Don't process the business logic in the request. Queue it (SQS/Redis) and process async. If you timeout, the sender will retry.
- **Verify Signatures** rigorously.
- Support **Payload Versioning**.

**Don't**:

- Don't rely on the order of delivery.
- Don't assume you will receive the event only once (Idempotency is key).

## Troubleshooting

| Error                           | Cause                       | Solution                                                        |
| :------------------------------ | :-------------------------- | :-------------------------------------------------------------- |
| `Signature Verification Failed` | Body parsing issue.         | Ensure you verify the **Raw Body**, not the parsed JSON object. |
| `Timeout`                       | Processing taking too long. | Move logic to a background job; return 200 immediately.         |

## References

- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Standard Webhooks](https://www.standardwebhooks.com/)
