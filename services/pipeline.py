from models.response import SearchResponse, Result
from services.search import search
from services.quadrail import guardrail_decision

def run(query: str) -> SearchResponse:
    decision = guardrail_decision(query)

    if decision["status"] == "blocked":
        return decision

    results = search(query)

    return SearchResponse(
        query=query,
        results=[Result(**r) for r in results],
        warning=decision.get("warning")
    )