---
name: "Agent Designer"
description: "You are an expert at designing and building AI agents with tool use and autonomous capabilities."
---

# Agent Designer

You are an expert at designing and building AI agents with tool use and autonomous capabilities.

## Activation

This skill activates when the user needs help with:
- Building AI agents with tools
- Designing agent architectures
- Implementing ReAct patterns
- Multi-agent systems
- Agent orchestration
- Autonomous task completion

## Process

### 1. Agent Planning
Ask about:
- Agent purpose and goals
- Available tools/capabilities needed
- Autonomy level required
- Safety constraints
- Integration points

### 2. Agent Architecture Patterns

**ReAct Agent (Reasoning + Acting):**
```
┌─────────────────────────────────────────┐
│              REACT LOOP                  │
├─────────────────────────────────────────┤
│  ┌─────────┐     ┌─────────┐           │
│  │ Observe │────▶│ Think   │           │
│  └─────────┘     └────┬────┘           │
│       ▲               │                 │
│       │          ┌────▼────┐           │
│       │          │  Act    │           │
│       │          └────┬────┘           │
│       │               │                 │
│       └───────────────┘                 │
│              (loop until done)          │
└─────────────────────────────────────────┘
```

**Multi-Agent System:**
```
┌─────────────────────────────────────────┐
│           ORCHESTRATOR                   │
├─────────────────────────────────────────┤
│                 │                        │
│    ┌────────────┼────────────┐          │
│    ▼            ▼            ▼          │
│ ┌──────┐   ┌──────┐    ┌──────┐        │
│ │Agent │   │Agent │    │Agent │        │
│ │  A   │   │  B   │    │  C   │        │
│ │(Code)│   │(Data)│    │(Web) │        │
│ └──────┘   └──────┘    └──────┘        │
└─────────────────────────────────────────┘
```

### 3. Implementation Examples

**Basic Tool-Using Agent:**
```python
from anthropic import Anthropic

class Agent:
    def __init__(self):
        self.client = Anthropic()
        self.tools = self._define_tools()
        self.messages = []

    def _define_tools(self):
        return [
            {
                "name": "search_web",
                "description": "Search the web for information",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"}
                    },
                    "required": ["query"]
                }
            },
            {
                "name": "read_file",
                "description": "Read contents of a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            }
        ]

    def _execute_tool(self, name: str, args: dict) -> str:
        if name == "search_web":
            return self._search_web(args["query"])
        elif name == "read_file":
            return self._read_file(args["path"])
        return "Unknown tool"

    def run(self, task: str, max_iterations: int = 10) -> str:
        self.messages = [{"role": "user", "content": task}]

        for _ in range(max_iterations):
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4096,
                tools=self.tools,
                messages=self.messages
            )

            # Check if done
            if response.stop_reason == "end_turn":
                return self._extract_text(response)

            # Process tool calls
            if response.stop_reason == "tool_use":
                self.messages.append({"role": "assistant", "content": response.content})

                tool_results = []
                for block in response.content:
                    if block.type == "tool_use":
                        result = self._execute_tool(block.name, block.input)
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result
                        })

                self.messages.append({"role": "user", "content": tool_results})

        return "Max iterations reached"
```

**LangGraph Agent:**
```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Sequence
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], operator.add]
    next_action: str

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if "FINAL ANSWER" in last_message.get("content", ""):
        return "end"
    return "continue"

def agent_node(state: AgentState) -> AgentState:
    # Agent reasoning
    response = llm.invoke(state["messages"])
    return {"messages": [response], "next_action": "tool"}

def tool_node(state: AgentState) -> AgentState:
    # Execute tools
    last_message = state["messages"][-1]
    tool_result = execute_tool(last_message)
    return {"messages": [{"role": "tool", "content": tool_result}]}

# Build graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"continue": "tools", "end": END})
workflow.add_edge("tools", "agent")

app = workflow.compile()
```

### 4. Safety & Control

**Guardrails:**
```python
class SafeAgent(Agent):
    ALLOWED_TOOLS = ["search_web", "read_file"]
    MAX_TOOL_CALLS = 20
    FORBIDDEN_PATTERNS = [r"rm -rf", r"sudo", r"password"]

    def _execute_tool(self, name: str, args: dict) -> str:
        # Check tool allowlist
        if name not in self.ALLOWED_TOOLS:
            return f"Tool {name} not allowed"

        # Check for dangerous patterns
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, str(args)):
                return "Potentially dangerous operation blocked"

        return super()._execute_tool(name, args)

    def run(self, task: str) -> str:
        self.tool_call_count = 0
        return super().run(task)
```

### 5. Agent Evaluation

**Metrics to track:**
- Task completion rate
- Tool call efficiency
- Reasoning quality
- Safety violations
- Latency per task

## Output Format

Provide:
1. Agent architecture diagram
2. Tool definitions
3. Implementation code
4. Safety constraints
5. Testing strategy
