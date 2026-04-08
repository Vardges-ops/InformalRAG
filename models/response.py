from pydantic import BaseModel
from typing import List, Optional

class Result(BaseModel):
    text: str
    title: Optional[str]
    score: float


class SearchResponse(BaseModel):
    query: str
    results: List[Result]
    warning: Optional[str] = None