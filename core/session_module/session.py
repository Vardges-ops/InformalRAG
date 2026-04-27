from collections import defaultdict, deque
from typing import Deque, Dict, List

MAX_HISTORY = 10

_sessions: Dict[str, Deque[dict]] = defaultdict(lambda: deque(maxlen=MAX_HISTORY))


def get_history(session_id: str) -> List[dict]:
    """Returns a copy of the message history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session.
    Returns:
        List[dict]: A list of messages in the session history, where each message is a
        dictionary with 'role' and 'content' keys.
    """
    return list(_sessions[session_id])


def add_message(session_id: str, role: str, content: str):
    """Adds a message to the session history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session.
        role (str): The role of the message sender (e.g., 'user', 'assistant').
        content (str): The content of the message.
    """
    _sessions[session_id].append({"role": role, "content": content})


def clear_session(session_id: str):
    """Clears the session history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session to be cleared."""
    _sessions.pop(session_id, None)
