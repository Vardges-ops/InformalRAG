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
    You are a helpful assistant.
    
    Answer the question using ONLY the provided context.
    If the answer is not in the context, say: "I don't know based on the given information."
    
    Context:
    {context}
    
    Question:
    {query}
    
    Answer:
    """
