from typing import List, Dict
from dotenv import load_dotenv

from core import (
    get_client,
    get_model,
    get_reranker,
    get_cache,
    set_cache
)

load_dotenv()

client = get_client()
model = get_model()
reranker = get_reranker()


def search(query: str) -> List[Dict]:

    cached = get_cache(query)
    if cached:
        print("CACHE HIT")
        return cached

    print("CACHE MISS")

    q_emb = model.encode(
        f"Represent this question for retrieving relevant documents: {query}",
        normalize_embeddings=True
    )

    res = client.query_points(
        collection_name="wiki_chunks",
        query=q_emb,
        limit=10
    )

    pairs = [(query, r.payload["text"]) for r in res.points]
    scores = reranker.predict(pairs)

    ranked = sorted(
        zip(res.points, scores),
        key=lambda x: x[1],
        reverse=True
    )

    top_results = ranked[:2]

    serialized = [
        {
            "score": float(score),
            "text": point.payload["text"],
            "title": point.payload.get("title"),
        }
        for point, score in top_results
    ]

    set_cache(query, serialized)

    return serialized



if __name__ == "__main__":
    query = "who is programmer?"

    results = search(query)

    for r in results:
        print("-" * 40)
        print(r["score"])
        print(r["text"])