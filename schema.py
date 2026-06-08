from pydantic import BaseModel


class FinalResponse(BaseModel):
    answer: str
    tools_used: list[str]
    reasoning: str
