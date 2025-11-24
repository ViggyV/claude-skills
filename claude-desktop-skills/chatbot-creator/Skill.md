---
name: "Chatbot Creator"
description: "You are an expert at building conversational AI chatbots for various use cases."
version: "1.0.0"
---

# Chatbot Creator

You are an expert at building conversational AI chatbots for various use cases.

## Activation

This skill activates when the user needs help with:
- Building chatbots from scratch
- Integrating LLMs into chat interfaces
- Conversation management
- Multi-turn dialogue systems
- Chatbot personality design

## Process

### 1. Chatbot Planning
Ask about:
- Use case (customer support, assistant, companion)
- Platform (web, mobile, Slack, Discord)
- Capabilities needed (FAQ, task completion, open chat)
- Personality/tone requirements
- Integration requirements

### 2. Architecture Patterns

**Simple Q&A Bot:**
```python
class SimpleBot:
    def __init__(self, llm_client):
        self.client = llm_client
        self.system_prompt = """You are a helpful assistant.
        Answer questions clearly and concisely."""

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
```

**Stateful Conversation Bot:**
```python
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class ConversationBot:
    client: any
    system_prompt: str
    history: List[Dict] = field(default_factory=list)
    max_history: int = 20

    def chat(self, user_message: str) -> str:
        self.history.append({"role": "user", "content": user_message})

        # Trim history if too long
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history[-self.max_history:])

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )

        assistant_message = response.choices[0].message.content
        self.history.append({"role": "assistant", "content": assistant_message})

        return assistant_message

    def reset(self):
        self.history = []
```

**Tool-Enabled Agent:**
```python
from typing import Callable, Dict

class AgentBot:
    def __init__(self, client, tools: Dict[str, Callable]):
        self.client = client
        self.tools = tools
        self.tool_schemas = self._generate_schemas()

    def chat(self, user_message: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": user_message}],
            tools=self.tool_schemas,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if message.tool_calls:
            # Execute tools and continue conversation
            tool_results = []
            for tool_call in message.tool_calls:
                result = self.tools[tool_call.function.name](
                    **json.loads(tool_call.function.arguments)
                )
                tool_results.append({
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                })
            # Continue with tool results...

        return message.content
```

### 3. Personality Design

**System Prompt Template:**
```
You are [Name], a [role] for [company/purpose].

PERSONALITY:
- Tone: [friendly/professional/casual/formal]
- Communication style: [concise/detailed/conversational]
- Quirks: [specific traits that make it memorable]

CAPABILITIES:
- You can help with: [list capabilities]
- You cannot: [list limitations]

GUIDELINES:
- Always [behavior1]
- Never [behavior2]
- When unsure, [fallback behavior]

EXAMPLES OF YOUR VOICE:
User: "Hi!"
You: "[example greeting in character]"

User: "I have a problem"
You: "[example empathetic response]"
```

### 4. Conversation Management

**Intent Detection:**
```python
INTENTS = {
    "greeting": ["hi", "hello", "hey"],
    "farewell": ["bye", "goodbye", "see you"],
    "help": ["help", "support", "issue"],
    "faq": ["how do i", "what is", "where can"]
}

def detect_intent(message: str) -> str:
    message_lower = message.lower()
    for intent, keywords in INTENTS.items():
        if any(kw in message_lower for kw in keywords):
            return intent
    return "general"
```

**Conversation State Machine:**
```python
from enum import Enum

class ConversationState(Enum):
    GREETING = "greeting"
    GATHERING_INFO = "gathering_info"
    PROCESSING = "processing"
    CONFIRMING = "confirming"
    COMPLETED = "completed"

class StatefulBot:
    def __init__(self):
        self.state = ConversationState.GREETING
        self.context = {}

    def transition(self, user_input: str):
        if self.state == ConversationState.GREETING:
            self.state = ConversationState.GATHERING_INFO
        # ... handle other transitions
```

## Output Format

Provide:
1. Architecture recommendation
2. Implementation code
3. System prompt design
4. Integration guide
5. Testing conversation flows
