from typing import Optional

from pydantic import BaseModel


class AnalyticsRequest(BaseModel):
    chat_id: Optional[int]
    prompt: str


class AnalyticsResponse(BaseModel):
    chat_id: int
    response: str
