from pydantic import BaseModel
from typing import Optional


class SearchResponse(BaseModel):
    query: str
    answer: str
    warning: Optional[str] = None
