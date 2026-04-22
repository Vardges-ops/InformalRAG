import redis
import json

# TODO make caching optional and add cache clear function

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def normalize(q: str):
    return q.strip().lower()


def get_cache(query: str):
    key = normalize(query)
    data = r.get(key)
    return json.loads(data) if data else None


def set_cache(query: str, value):
    key = normalize(query)
    r.set(key, json.dumps(value), ex=3600)
