from collections import defaultdict, deque
from typing import Deque, Dict, List

MAX_HISTORY = 10

_sessions: Dict[str, Deque[dict]] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


def get_history(session_id: str) -> List[dict]:
    return list(_sessions[session_id])


def add_message(session_id: str, role: str, content: str):
    _sessions[session_id].append({
        "role": role,
        "content": content
    })


def clear_session(session_id: str):
    _sessions.pop(session_id, None)
