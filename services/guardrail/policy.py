import re
from enum import Enum


class Category(str, Enum):
    SAFE = "safe"
    SENSITIVE = "sensitive"
    FORBIDDEN = "forbidden"


FORBIDDEN_PATTERNS = [
    r"\bhow to (hack|exploit|ddos|bypass)\b",
    r"\bmake (a )?bomb\b",
    r"\bsteal (passwords?|data)\b",
]

SENSITIVE_PATTERNS = [
    r"\bmedical advice\b",
    r"\blegal advice\b",
    r"\bdosage\b",
    r"\bdiagnose\b",
]


def normalize(q: str) -> str:
    return q.strip().lower()


def match_any(patterns, text):
    return any(re.search(p, text) for p in patterns)


def classify_query(query: str) -> Category:
    q = normalize(query)

    if match_any(FORBIDDEN_PATTERNS, q):
        return Category.FORBIDDEN

    if match_any(SENSITIVE_PATTERNS, q):
        return Category.SENSITIVE

    return Category.SAFE
