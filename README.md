# Zionet Task 1 — LLM Tool-Calling Agent Loop

Two implementations of an agentic tool-calling loop using [OpenRouter](https://openrouter.ai):
- **Task 1** — manual loop with the raw OpenAI-compatible SDK
- **Task 2 (Bonus)** — same agent re-implemented with [LangGraph](https://langchain-ai.github.io/langgraph/)

Both use the same 3 mock tools and return the same structured JSON response validated by Pydantic.

## Features

- **Agentic loop** — runs until the model has no more tool calls to make
- **3 mock tools** — `get_weather`, `calculator`, `get_current_time`
- **Structured output** — final response is parsed into a Pydantic schema
- **Per-iteration logging** — every step is logged to stdout

## Project Structure

```
Zionet_task1/
├── main.py               # Task 1 entry point (manual loop)
├── agent.py              # Task 1 — manual agentic loop
├── main_langgraph.py     # Task 2 entry point (LangGraph)
├── agent_langgraph.py    # Task 2 — LangGraph re-implementation
├── tools.py              # Tool definitions and mock implementations (shared)
├── schema.py             # Pydantic response schema (shared)
├── requirements.txt      # Dependencies
└── secrets.md            # API key (local only, git-ignored)
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Get an OpenRouter API key** at [openrouter.ai/keys](https://openrouter.ai/keys) and add it to `secrets.md`:
   ```
   openrouter_key = sk-or-...
   ```

3. **Run Task 1** (manual loop)
   ```bash
   python main.py
   ```

4. **Run Task 2** (LangGraph)
   ```bash
   python main_langgraph.py
   ```

## Task 1 — Manual Loop Output

```
=== Agent Loop Starting ===
User prompt: What is the weather today in Beer-Sheva? Also, what is the result of 18*18?

--- Iteration 1 ---
Sending 2 message(s) to the model...
finish_reason: tool_calls
  Tool call: get_weather({"city": "Beer-Sheva"})
  Tool result: Clear skies, 20°C, humidity 50%, wind 10 km/h N
  Tool call: calculator({"expr": "18*18"})
  Tool result: 324

--- Iteration 2 ---
Sending 5 message(s) to the model...
finish_reason: stop
  Final response received.

=== Final Structured Response ===
{
  "answer": "The weather in Beer-Sheva today is clear skies at 20°C. The result of 18 * 18 is 324.",
  "tools_used": ["functions.get_weather", "functions.calculator"],
  "reasoning": "Used get_weather and calculator tools to answer both questions."
}
```

## Task 2 — LangGraph Output

```
=== LangGraph Agent Loop Starting ===
User prompt: What is the weather today in Beer-Sheva? Also, what is the result of 18*18?

--- Iteration 1 [agent] ---
  ai: [tool call]
    -> get_weather({"city": "Beer-Sheva"})
    -> calculator({"expr": "18*18"})

--- Iteration 2 [tools] ---
  tool: Clear skies, 20°C, humidity 50%, wind 10 km/h N

--- Iteration 3 [tools] ---
  tool: 324

--- Iteration 4 [agent] ---
  ai: { "answer": "...", "tools_used": [...], "reasoning": "..." }

=== Final Structured Response ===
{
  "answer": "The weather in Beer-Sheva today is clear skies at 20°C. The result of 18 * 18 is 324.",
  "tools_used": ["functions.get_weather", "functions.calculator"],
  "reasoning": "Used get_weather and calculator tools to answer both questions."
}

--- What LangGraph hid ---
The while loop, finish_reason routing, and messages state accumulation.
```

## What LangGraph Hides

| | Task 1 (manual) | Task 2 (LangGraph) |
|---|---|---|
| Loop | `while True` | Graph edges |
| Routing | `if finish_reason == "tool_calls"` | `tools_condition` |
| State | Manual `messages.append()` | `MessagesState` |

## Response Schema

```python
class FinalResponse(BaseModel):
    answer: str            # Human-readable answer
    tools_used: list[str]  # Names of tools called
    reasoning: str         # How the answer was derived
```
