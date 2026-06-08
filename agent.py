import json
import pathlib
import anthropic

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
Daniels_secret_key = _secrets["Daniels_secret_key"]

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Use the available tools to answer the user's question. You may call multiple tools across multiple turns.

When you have gathered all the information you need and are ready to give your final answer,
respond with ONLY a valid JSON object — no extra text, no markdown, no code fences — in this exact format:
{
  "answer": "<your complete answer to the user>",
  "tools_used": ["<tool1>", "<tool2>", ...],
  "reasoning": "<brief explanation of how you arrived at the answer>"
}"""

client = anthropic.Anthropic(api_key=Daniels_secret_key)


def run(user_prompt: str) -> FinalResponse:
    messages = [{"role": "user", "content": user_prompt}]
    iteration = 0

    while True:
        iteration += 1
        print(f"\n--- Iteration {iteration} ---")
        print(f"Sending {len(messages)} message(s) to Claude...")

        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=TOOL_DEFINITIONS,
            messages=messages,
        )

        print(f"stop_reason: {response.stop_reason}")

        if response.stop_reason == "tool_use":
            tool_results = []
            assistant_content = response.content

            for block in assistant_content:
                if block.type == "tool_use":
                    print(f"  Tool call: {block.name}({json.dumps(block.input)})")
                    result = execute_tool(block.name, block.input)
                    print(f"  Tool result: {result}")
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            messages.append({"role": "assistant", "content": assistant_content})
            messages.append({"role": "user", "content": tool_results})

        else:
            final_text = next(
                (block.text for block in response.content if hasattr(block, "text")),
                "",
            )
            print(f"  Final response received.")
            return FinalResponse.model_validate_json(final_text)
