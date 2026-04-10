from typing import Dict
from services.guardrail.policy import classify_query, Category

def guardrail_decision(query: str) -> Dict:
    category = classify_query(query)

    if category == Category.FORBIDDEN:
        return {
            "status": "blocked",
            "category": category,
            "message": "I can’t help with that request."
        }

    if category == Category.SENSITIVE:
        return {
            "status": "allow_with_warning",
            "category": category,
            "message": "I may provide general information, not professional advice."
        }

    return {
        "status": "allow",
        "category": category,
        "message": None
    }