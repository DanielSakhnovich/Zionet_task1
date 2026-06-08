# Zionet Task 1 — LLM Tool-Calling Agent Loop

A Python project demonstrating an agentic tool-calling loop using the Anthropic SDK. The agent can call multiple tools across multiple turns and returns a final structured JSON response validated by Pydantic.

## Features

- **Agentic loop** — runs until the model has no more tool calls to make
- **3 mock tools** — `get_weather`, `calculator`, `get_current_time`
- **Structured output** — final response is parsed into a Pydantic schema
- **Per-iteration logging** — every round-trip with the LLM is logged to stdout

## Project Structure

```
Zionet_task1/
├── main.py          # Entry point
├── agent.py         # Agentic loop logic
├── tools.py         # Tool definitions and mock implementations
├── schema.py        # Pydantic response schema
├── requirements.txt # Dependencies
└── secrets.md       # API key (local only, git-ignored)
```

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Add your Anthropic API key** to `secrets.md`:
   ```
   Daniels_secret_key = sk-ant-...
   ```

3. **Run**
   ```bash
   python main.py
   ```

## Example Output

```
=== Agent Loop Starting ===
User prompt: What is the weather in Tokyo? Also, what is 128 * 3? And what time is it right now?

--- Iteration 1 ---
Sending 1 message(s) to Claude...
stop_reason: tool_use
  Tool call: get_weather({"city": "Tokyo"})
  Tool result: Partly cloudy, 22°C, humidity 68%, wind 12 km/h NE
  Tool call: calculator({"expr": "128 * 3"})
  Tool result: 384
  Tool call: get_current_time({})
  Tool result: 2026-06-08 10:30:00 UTC (mocked)

--- Iteration 2 ---
Sending 3 message(s) to Claude...
stop_reason: end_turn
  Final response received.

=== Final Structured Response ===
{
  "answer": "The weather in Tokyo is partly cloudy at 22°C. 128 * 3 = 384. The current time is 2026-06-08 10:30:00 UTC.",
  "tools_used": ["get_weather", "calculator", "get_current_time"],
  "reasoning": "Called all three tools in one turn to gather weather, math result, and time."
}
```

## Response Schema

```python
class FinalResponse(BaseModel):
    answer: str          # Human-readable answer
    tools_used: list[str]  # Names of tools called
    reasoning: str       # How the answer was derived
```
