---
name: webhook-creator
description: Webhook Creator
---

# Webhook Creator

You are an expert at designing and implementing webhook systems.

## Activation

This skill activates when the user needs help with:
- Creating webhook endpoints
- Webhook delivery systems
- Event notification systems
- Webhook security
- Retry and reliability

## Process

### 1. Webhook Assessment
Ask about:
- Events to expose
- Expected consumers
- Delivery guarantees needed
- Security requirements
- Scale expectations

### 2. Webhook Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEBHOOK SYSTEM                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐                 │
│  │  Event   │────▶│  Queue   │────▶│ Delivery │                 │
│  │ Producer │     │ (Kafka)  │     │  Worker  │                 │
│  └──────────┘     └──────────┘     └────┬─────┘                 │
│                                         │                        │
│                                    ┌────▼─────┐                  │
│                                    │  Retry   │                  │
│                                    │  Queue   │                  │
│                                    └────┬─────┘                  │
│                                         │                        │
│         ┌───────────────────────────────┼───────────────────┐   │
│         │                               │                   │   │
│         ▼                               ▼                   ▼   │
│  ┌──────────┐                    ┌──────────┐        ┌──────────┐
│  │ Consumer │                    │ Consumer │        │ Consumer │
│  │    A     │                    │    B     │        │    C     │
│  └──────────┘                    └──────────┘        └──────────┘
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Webhook Endpoint (Receiving)

```python
from fastapi import FastAPI, Request, HTTPException, Header
import hmac
import hashlib

app = FastAPI()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature."""
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)

@app.post("/webhooks/github")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(None),
    x_github_event: str = Header(None)
):
    """Receive GitHub webhook."""
    payload = await request.body()

    # Verify signature
    if not verify_signature(payload, x_hub_signature_256, WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid signature")

    data = await request.json()

    # Process based on event type
    if x_github_event == "push":
        await handle_push_event(data)
    elif x_github_event == "pull_request":
        await handle_pr_event(data)

    return {"status": "received"}

@app.post("/webhooks/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None)
):
    """Receive Stripe webhook."""
    import stripe

    payload = await request.body()

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=401, detail="Invalid signature")

    # Handle events
    if event["type"] == "payment_intent.succeeded":
        await handle_payment_success(event["data"]["object"])
    elif event["type"] == "payment_intent.failed":
        await handle_payment_failure(event["data"]["object"])

    return {"received": True}
```

### 4. Webhook Delivery System (Sending)

```python
from dataclasses import dataclass
from datetime import datetime
import asyncio
import httpx

@dataclass
class WebhookSubscription:
    id: str
    url: str
    secret: str
    events: list[str]
    is_active: bool = True

@dataclass
class WebhookDelivery:
    id: str
    subscription_id: str
    event_type: str
    payload: dict
    attempt: int = 0
    status: str = "pending"
    response_code: int = None
    created_at: datetime = None

class WebhookService:
    def __init__(self, db, queue):
        self.db = db
        self.queue = queue

    def sign_payload(self, payload: str, secret: str) -> str:
        """Generate HMAC signature."""
        return hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    async def trigger_event(self, event_type: str, payload: dict):
        """Trigger webhook for an event."""
        subscriptions = await self.db.get_subscriptions_for_event(event_type)

        for sub in subscriptions:
            delivery = WebhookDelivery(
                id=str(uuid.uuid4()),
                subscription_id=sub.id,
                event_type=event_type,
                payload=payload,
                created_at=datetime.utcnow()
            )
            await self.queue.enqueue(delivery)

    async def deliver(self, delivery: WebhookDelivery):
        """Deliver a webhook."""
        subscription = await self.db.get_subscription(delivery.subscription_id)

        payload_json = json.dumps(delivery.payload)
        signature = self.sign_payload(payload_json, subscription.secret)

        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}",
            "X-Webhook-Event": delivery.event_type,
            "X-Webhook-Delivery": delivery.id,
            "X-Webhook-Timestamp": str(int(datetime.utcnow().timestamp()))
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    subscription.url,
                    content=payload_json,
                    headers=headers
                )

            delivery.response_code = response.status_code
            delivery.status = "success" if response.is_success else "failed"

        except Exception as e:
            delivery.status = "failed"
            delivery.error = str(e)

        await self.db.update_delivery(delivery)

        # Retry if failed
        if delivery.status == "failed" and delivery.attempt < 5:
            await self.schedule_retry(delivery)

    async def schedule_retry(self, delivery: WebhookDelivery):
        """Schedule retry with exponential backoff."""
        delivery.attempt += 1
        delay_seconds = 2 ** delivery.attempt * 60  # 2, 4, 8, 16, 32 minutes

        await self.queue.enqueue(delivery, delay=delay_seconds)
```

### 5. Webhook Event Format

```python
# Standard webhook payload
{
    "id": "evt_abc123",
    "type": "order.created",
    "created": 1705312800,
    "data": {
        "object": {
            "id": "ord_xyz789",
            "user_id": "usr_123",
            "total": 99.99,
            "status": "pending"
        }
    },
    "api_version": "2024-01-15"
}

# Event types convention
"""
resource.action format:
- order.created
- order.updated
- order.completed
- order.cancelled
- payment.succeeded
- payment.failed
- user.created
- user.deleted
"""
```

### 6. Webhook Management API

```python
@app.post("/webhook-subscriptions", response_model=Subscription)
async def create_subscription(request: CreateSubscriptionRequest):
    """Register a new webhook subscription."""
    secret = secrets.token_hex(32)

    subscription = await webhook_service.create_subscription(
        url=request.url,
        events=request.events,
        secret=secret
    )

    # Return secret only on creation
    return {**subscription.dict(), "secret": secret}

@app.get("/webhook-subscriptions/{id}/deliveries")
async def list_deliveries(id: str, limit: int = 20):
    """List recent webhook deliveries."""
    return await webhook_service.get_deliveries(id, limit)

@app.post("/webhook-subscriptions/{id}/test")
async def test_webhook(id: str):
    """Send a test webhook."""
    await webhook_service.trigger_event(
        subscription_id=id,
        event_type="test.ping",
        payload={"message": "Test webhook"}
    )
    return {"status": "sent"}
```

## Output Format

Provide:
1. Webhook endpoint implementation
2. Signature verification
3. Event payload structure
4. Retry strategy
5. Management API
