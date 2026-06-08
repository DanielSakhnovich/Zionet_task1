import json
import pathlib
from openai import OpenAI

from tools import TOOL_DEFINITIONS, execute_tool
from schema import FinalResponse


def _load_secrets(path: str = "secrets.md") -> dict:
    secrets = {}
    for line in pathlib.Path(path).read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            key, _, value = line.partition("=")
            secrets[key.strip()] = value.strip()
    return secrets


_secrets = _load_secrets()
openrouter_key = _secrets["openrouter_key"]

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key,
)

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Use the available tools to answer the user's question. You may call multiple tools across multiple turns.

When you have gathered all the information you need and are ready to give your final answer,
respond with ONLY a valid JSON object — no extra text, no markdown, no code fences — in this exact format:
{
  "answer": "<your complete answer to the user>",
  "tools_used": ["<tool1>", "<tool2>", ...],
  "reasoning": "<brief explanation of how you arrived at the answer>"
}"""


def run(user_prompt: str) -> FinalResponse:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]
    iteration = 0

    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        print(f"Sending {len(messages)} message(s) to the model...")

        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        choice = response.choices[0]
        print(f"finish_reason: {choice.finish_reason}")

        if choice.finish_reason == "tool_calls":
            messages.append(choice.message)

            for tool_call in choice.message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print(f"  Tool call: {name}({json.dumps(args)})")
                result = execute_tool(name, args)
                print(f"  Tool result: {result}")
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })

        else:
            final_text = choice.message.content
            print(f"  Final response received.")
            return FinalResponse.model_validate_json(final_text)
