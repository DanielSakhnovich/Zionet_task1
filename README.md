# Zionet Task 1 — LLM Tool-Calling Agent Loop

A Python project demonstrating an agentic tool-calling loop using [OpenRouter](https://openrouter.ai) (OpenAI-compatible API). The agent can call multiple tools across multiple turns and returns a final structured JSON response validated by Pydantic.

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

2. **Get an OpenRouter API key** at [openrouter.ai/keys](https://openrouter.ai/keys) and add it to `secrets.md`:
   ```
   openrouter_key = sk-or-...
   ```

3. **Run**
   ```bash
   python main.py
   ```

## Example Output

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
  "answer": "The weather in Beer-Sheva today is clear skies with a temperature of 20°C, humidity at 50%, and a wind speed of 10 km/h from the north. The result of 18 * 18 is 324.",
  "tools_used": ["functions.get_weather", "functions.calculator"],
  "reasoning": "I used the 'get_weather' tool to gather the current weather in Beer-Sheva and the 'calculator' tool to compute the product of 18 and 18."
}
```

## Response Schema

```python
class FinalResponse(BaseModel):
    answer: str            # Human-readable answer
    tools_used: list[str]  # Names of tools called
    reasoning: str         # How the answer was derived
```
