from core.llm_module.tools import generate_response, build_context, build_prompt
from models.response import SearchResponse
from services.search import search
from services.guardrail.quadrail import guardrail_decision


def run(query: str) -> SearchResponse | dict:
    """Runs the search pipeline for the given query.
    Args:
        query (str): The user's search query.
    Returns:
        SearchResponse: An object containing the original query, the generated answer, and any warnings if applicable."""
    decision = guardrail_decision(query)

    if decision["status"] == "blocked":
        return decision

    results = search(query)

    context = build_context(results)

    prompt = build_prompt(query, context)

    answer = generate_response(prompt)
    return SearchResponse(query=query, answer=answer, warning=decision.get("warning"))
