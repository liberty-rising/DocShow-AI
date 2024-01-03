from pydantic import BaseModel
from typing import Optional


class AnalyticsRequest(BaseModel):
    chat_id: Optional[int]
    prompt: str


class AnalyticsResponse(BaseModel):
    chat_id: int
    response: str
