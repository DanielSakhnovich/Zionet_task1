import json
import pathlib
from langchain_core.tools import StructuredTool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from tools import get_weather, calculator, get_current_time
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

TOOLS = [
    StructuredTool.from_function(get_weather, description="Get the current weather for a given city. Returns mocked weather data."),
    StructuredTool.from_function(calculator, description="Evaluate a simple arithmetic expression and return the result."),
    StructuredTool.from_function(get_current_time, description="Get the current date and time."),
]

SYSTEM_PROMPT = """You are a helpful assistant with access to tools.

Use the available tools to answer the user's question. You may call multiple tools.

When you have gathered all the information you need and are ready to give your final answer,
respond with ONLY a valid JSON object — no extra text, no markdown, no code fences — in this exact format:
{
  "answer": "<your complete answer to the user>",
  "tools_used": ["<tool1>", "<tool2>", ...],
  "reasoning": "<brief explanation of how you arrived at the answer>"
}"""

llm = ChatOpenAI(
    model="openai/gpt-4o-mini",
    base_url="https://openrouter.ai/api/v1",
    api_key=openrouter_key,
)

agent = create_react_agent(llm, TOOLS, prompt=SYSTEM_PROMPT)


def run(user_prompt: str) -> FinalResponse:
    iteration = 0
    last_chunk = None

    for chunk in agent.stream({"messages": [("user", user_prompt)]}):
        iteration += 1
        node = list(chunk.keys())[0]
        messages = chunk[node]["messages"]
        print(f"\n--- Iteration {iteration} [{node}] ---")
        for msg in messages:
            print(f"  {msg.type}: {msg.content or '[tool call]'}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"    -> {tc['name']}({json.dumps(tc['args'])})")
        last_chunk = chunk

    final_content = last_chunk["agent"]["messages"][-1].content
    return FinalResponse.model_validate_json(final_content)
