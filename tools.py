import re

TOOL_DEFINITIONS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a given city. Returns mocked weather data.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get weather for.",
                }
            },
            "required": ["city"],
        },
    },
    {
        "name": "calculator",
        "description": "Evaluate a simple arithmetic expression and return the result.",
        "input_schema": {
            "type": "object",
            "properties": {
                "expr": {
                    "type": "string",
                    "description": "A arithmetic expression to evaluate, e.g. '15 * 7' or '(100 + 50) / 3'.",
                }
            },
            "required": ["expr"],
        },
    },
    {
        "name": "get_current_time",
        "description": "Get the current date and time.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

_WEATHER_DATA = {
    "tokyo": "Partly cloudy, 22°C, humidity 68%, wind 12 km/h NE",
    "paris": "Sunny, 18°C, humidity 45%, wind 8 km/h W",
    "new york": "Overcast, 15°C, humidity 72%, wind 20 km/h SW",
    "london": "Rainy, 12°C, humidity 85%, wind 25 km/h NW",
}


def get_weather(city: str) -> str:
    return _WEATHER_DATA.get(city.lower(), f"Clear skies, 20°C, humidity 50%, wind 10 km/h N")


def calculator(expr: str) -> str:
    safe_expr = re.sub(r"[^\d\s\+\-\*\/\(\)\.\%]", "", expr)
    if not safe_expr.strip():
        return "Error: invalid expression"
    try:
        result = eval(safe_expr, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def get_current_time() -> str:
    return "2026-06-08 10:30:00 UTC (mocked)"


def execute_tool(name: str, input_dict: dict) -> str:
    if name == "get_weather":
        return get_weather(input_dict["city"])
    elif name == "calculator":
        return calculator(input_dict["expr"])
    elif name == "get_current_time":
        return get_current_time()
    else:
        return f"Error: unknown tool '{name}'"
