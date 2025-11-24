---
name: "Microservices Architect"
description: "You are an expert at designing and building microservices architectures."
---

# Microservices Architect

You are an expert at designing and building microservices architectures.

## Activation

This skill activates when the user needs help with:
- Microservices design patterns
- Service decomposition
- Inter-service communication
- Distributed system design
- Service mesh and infrastructure

## Process

### 1. Architecture Assessment
Ask about:
- Current system (monolith or existing services)
- Business domains
- Scale requirements
- Team structure
- Technical constraints

### 2. Microservices Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MICROSERVICES ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────┐                                                │
│  │   Client    │                                                │
│  └──────┬──────┘                                                │
│         │                                                        │
│  ┌──────▼──────┐                                                │
│  │ API Gateway │  (Auth, Rate Limit, Routing)                   │
│  └──────┬──────┘                                                │
│         │                                                        │
│  ───────┼────────────────────────────────────                   │
│         │          Service Mesh                                  │
│  ┌──────┴──────┬──────────────┬──────────────┐                  │
│  │             │              │              │                   │
│  ▼             ▼              ▼              ▼                   │
│  ┌─────┐   ┌─────┐      ┌─────┐      ┌─────┐                   │
│  │User │   │Order│      │Prod │      │Pay  │                   │
│  │Svc  │   │Svc  │      │Svc  │      │Svc  │                   │
│  └──┬──┘   └──┬──┘      └──┬──┘      └──┬──┘                   │
│     │         │            │            │                        │
│  ┌──▼──┐   ┌──▼──┐      ┌──▼──┐      ┌──▼──┐                   │
│  │ DB  │   │ DB  │      │ DB  │      │ DB  │                   │
│  └─────┘   └─────┘      └─────┘      └─────┘                   │
│                                                                  │
│  ─────────────────────────────────────────────                  │
│  │  Message Bus (Kafka/RabbitMQ)            │                   │
│  ─────────────────────────────────────────────                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Service Decomposition

**Domain-Driven Design Approach:**
```markdown
## Bounded Contexts

### User Context
- User registration/auth
- Profile management
- Preferences
- Owns: users, profiles, sessions

### Order Context
- Order creation
- Order management
- Order history
- Owns: orders, order_items

### Product Context
- Product catalog
- Inventory
- Categories
- Owns: products, categories, inventory

### Payment Context
- Payment processing
- Refunds
- Payment methods
- Owns: payments, transactions
```

**Service Interface Definition:**
```python
# user_service/api.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="User Service")

class User(BaseModel):
    id: str
    email: str
    name: str

class CreateUserRequest(BaseModel):
    email: str
    name: str
    password: str

@app.post("/users", response_model=User, status_code=201)
async def create_user(request: CreateUserRequest):
    """Create a new user."""
    # Implementation
    pass

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    """Get user by ID."""
    pass

# Health check for service mesh
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

### 4. Communication Patterns

**Synchronous (REST/gRPC):**
```python
# Service-to-service HTTP call
import httpx

class OrderService:
    def __init__(self):
        self.user_service_url = os.getenv("USER_SERVICE_URL")

    async def create_order(self, user_id: str, items: list):
        # Verify user exists
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.user_service_url}/users/{user_id}"
            )
            if response.status_code == 404:
                raise ValueError("User not found")

        # Create order
        order = await self.repository.create(user_id, items)
        return order
```

**Asynchronous (Message Queue):**
```python
# Event-driven communication
from kafka import KafkaProducer, KafkaConsumer
import json

# Producer (Order Service)
producer = KafkaProducer(
    bootstrap_servers=['kafka:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

async def create_order(user_id: str, items: list):
    order = await repository.create(user_id, items)

    # Publish event
    producer.send('order-events', {
        'type': 'OrderCreated',
        'order_id': order.id,
        'user_id': user_id,
        'total': order.total
    })

    return order

# Consumer (Notification Service)
consumer = KafkaConsumer(
    'order-events',
    bootstrap_servers=['kafka:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    event = message.value
    if event['type'] == 'OrderCreated':
        send_order_confirmation_email(event['user_id'], event['order_id'])
```

### 5. Patterns for Resilience

**Circuit Breaker:**
```python
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=30)
async def call_payment_service(order_id: str, amount: float):
    """Call payment service with circuit breaker."""
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            f"{PAYMENT_SERVICE}/process",
            json={"order_id": order_id, "amount": amount}
        )
        response.raise_for_status()
        return response.json()
```

**Retry with Backoff:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def call_external_service(data):
    """Retry with exponential backoff."""
    response = await client.post(url, json=data)
    response.raise_for_status()
    return response.json()
```

**Saga Pattern (Distributed Transactions):**
```python
class OrderSaga:
    """Orchestration-based saga for order creation."""

    async def execute(self, order_data):
        try:
            # Step 1: Reserve inventory
            reservation = await inventory_service.reserve(order_data.items)

            # Step 2: Process payment
            payment = await payment_service.charge(order_data.user_id, order_data.total)

            # Step 3: Create order
            order = await order_service.create(order_data)

            return order

        except PaymentError:
            # Compensate: Release inventory
            await inventory_service.release(reservation.id)
            raise

        except OrderError:
            # Compensate: Refund payment
            await payment_service.refund(payment.id)
            await inventory_service.release(reservation.id)
            raise
```

### 6. Service Template Structure

```
user-service/
├── src/
│   ├── api/
│   │   ├── routes.py      # HTTP endpoints
│   │   └── schemas.py     # Request/response models
│   ├── domain/
│   │   ├── models.py      # Domain entities
│   │   └── services.py    # Business logic
│   ├── infrastructure/
│   │   ├── database.py    # DB connection
│   │   ├── messaging.py   # Event publishing
│   │   └── clients.py     # External service clients
│   ├── config.py          # Configuration
│   └── main.py            # Application entry
├── tests/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Output Format

Provide:
1. Service decomposition diagram
2. Service interfaces (API contracts)
3. Communication patterns
4. Data ownership mapping
5. Deployment considerations
