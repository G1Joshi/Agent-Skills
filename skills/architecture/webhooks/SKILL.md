---
name: webhooks
description: Expert Webhooks architecture assistance covering HMAC signature verification, idempotent delivery, exponential backoff retries, and ingestion queues. Use when building webhook consumers, sending webhook notifications to third parties, or processing asynchronous event callbacks.
---

# Webhooks

Webhooks are "user-defined HTTP callbacks". They are triggered by some event in a source system (e.g., Stripe, GitHub) and sent to a destination system (Your API) to notify it.

## When to Use

- **Third-Party Event Notification**: Consuming real-time notifications from payment providers (Stripe), Git hosts (GitHub), and SaaS platforms.
- **Asynchronous System Integration**: Triggering external partner workflows when business events occur in your application.
- **Decoupled API Callback Architecture**: Notifying long-running asynchronous clients when requested tasks finish without polling.
- **Event-Driven Microservice Ingestion**: Ingesting incoming webhook events into queue buffers for asynchronous worker processing.

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

#Cryptographic Signature Verification (HMAC-SHA256)

Validates that webhook payloads originate from authentic senders and were not tampered with in transit:

```typescript
import crypto from "crypto";

export function verifyWebhookSignature(
  payload: string,
  signatureHeader: string,
  secret: string,
): boolean {
  const expectedSignature = crypto
    .createHmac("sha256", secret)
    .update(payload)
    .digest("hex");

  // Constant-time comparison prevents timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signatureHeader),
    Buffer.from(expectedSignature),
  );
}
```

#Instant 200 OK Acknowledgment with Ingestion Queues

Acknowledge incoming webhooks immediately (< 500ms) and offload heavy processing to background queues:

```typescript
app.post(
  "/webhooks/stripe",
  express.raw({ type: "application/json" }),
  async (req, res) => {
    const signature = req.headers["stripe-signature"] as string;
    if (
      !verifyWebhookSignature(req.body.toString(), signature, WEBHOOK_SECRET)
    ) {
      return res.status(400).send("Invalid signature");
    }

    // Push to Redis queue immediately
    await webhookQueue.add(
      "process-stripe-event",
      JSON.parse(req.body.toString()),
    );
    res.status(200).send("Received");
  },
);
```

#Exponential Backoff Retry Strategy

Senders automatically retry failed delivery attempts with exponential delay:

```
Attempt 1: Immediately
Attempt 2: 15 seconds later
Attempt 3: 1 minute later
Attempt 4: 15 minutes later
Attempt 5: 1 hour later -> DLQ
```

## Common Patterns

### Idempotent Webhook Processing with Deduping

**Problem**: Webhook providers retry delivery on timeout, causing duplicate state changes or double processing.

**Solution**:
Check incoming delivery event IDs against a fast cache or database before executing business logic:

```typescript
import { Request, Response } from "express";

export async function handleWebhook(req: Request, res: Response) {
  const eventId = req.headers["x-webhook-id"] as string;
  const isDuplicate = await redisClient.set(`webhook:${eventId}`, "1", {
    NX: true,
    EX: 86400, // 24-hour expiration
  });

  if (!isDuplicate) {
    return res.status(200).json({ status: "already_processed" });
  }

  // Enqueue for asynchronous background worker processing
  await taskQueue.add("process-event", req.body);
  return res.status(202).json({ status: "accepted" });
}
```

## Best Practices (2026)

**Do**:

- **Verify Signatures Using Raw Unparsed Request Bodies**: Never verify HMAC signatures on parsed JSON objects; whitespace discrepancies break hashes.
- **Implement Idempotency Handling**: Record incoming webhook event IDs in Redis or database unique indexes to discard duplicates.
- **Respond with 200 OK Immediately**: Queue the event for background processing; third parties time out after 5-10 seconds.
- **Expose Webhook Delivery Logs**: Provide dashboard interfaces where customers can view delivery status, response codes, and manual retries.

**Don't**:

- **Don't perform heavy business logic in the HTTP handler**: Long processing times cause webhook timeouts and unnecessary retries.
- **Don't accept webhooks over insecure HTTP**: Enforce TLS (HTTPS) on all webhook ingestion endpoints.
- **Don't trust unverified webhook headers**: Always use cryptographic signatures rather than relying on IP whitelists alone.

## Troubleshooting

| Error                           | Cause                       | Solution                                                        |
| :------------------------------ | :-------------------------- | :-------------------------------------------------------------- |
| `Signature Verification Failed` | Body parsing issue.         | Ensure you verify the **Raw Body**, not the parsed JSON object. |
| `Timeout`                       | Processing taking too long. | Move logic to a background job; return 200 immediately.         |

## References

- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Standard Webhooks](https://www.standardwebhooks.com/)
