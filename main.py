import json
from agent import run

USER_PROMPT = "What is the weather today in Beer-Sheva? Also, what is the result of 18*18?"

if __name__ == "__main__":
    print("=== Agent Loop Starting ===")
    print(f"User prompt: {USER_PROMPT}\n")

    result = run(USER_PROMPT)

    print("\n=== Final Structured Response ===")
    print(json.dumps(result.model_dump(), indent=2))
