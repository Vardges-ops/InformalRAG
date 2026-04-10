from core.llm.tools import generate_response, build_context, build_prompt
from models.response import SearchResponse
from services.search import search
from services.guardrail.quadrail import guardrail_decision


def run(query: str):
    decision = guardrail_decision(query)

    if decision["status"] == "blocked":
        return decision

    results = search(query)

    context = build_context(results)

    prompt = build_prompt(query, context)

    answer = generate_response(prompt)
    return SearchResponse(
        query=query,
        answer=answer,
        warning=decision.get("warning")
    )
