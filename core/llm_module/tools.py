import requests

from core.config import LLM_MODEL_NAME, LLM_URL


def generate_response(prompt: str) -> str:
    response = requests.post(
        LLM_URL,
        json={
            "model": LLM_MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def build_context(results):
    return "\n\n".join([r["text"] for r in results])


def build_prompt(query: str, context: str) -> str:
    return f"""
    You are an assistant that answers questions based on the provided context.

    Use provided context to answer the question, if you can't find the answer then use your own knowledge to answer.
    
    Only say "I don't know" if the answer is completely missing.
    
    Context:
    {context}
    
    Question:
    {query}
    
    Answer:
    """
