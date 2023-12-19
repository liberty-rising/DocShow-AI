from pydantic import BaseModel
from typing import List, Optional


class AnalyticsRequest(BaseModel):
    chat_id: Optional[int]
    table_names: List[str]
    prompt: str


class AnalyticsResponse(BaseModel):
    chat_id: int
    response: str
