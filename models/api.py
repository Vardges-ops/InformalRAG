from pydantic import BaseModel, Field
from typing import Optional, Literal


class ChatRequest(BaseModel):
    query: str = Field(str, min_length=1)
    session_id: Optional[str] = Field(default="default")
    response_format: Literal["text", "audio"] = "text"
    voice: Optional[str] = "en-US"  # engine-specific


class ChatResponse(BaseModel):
    query: str
    answer: str
    warning: Optional[str] = None
    session_id: str
