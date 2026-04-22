from pydantic import BaseModel, Field
from typing import Optional


class ChatRequest(BaseModel):
    query: str = Field(str, min_length=1)
    session_id: Optional[str] = Field(default="default")


class ChatResponse(BaseModel):
    query: str
    answer: str
    warning: Optional[str] = None
    session_id: str
