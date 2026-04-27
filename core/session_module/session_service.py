from core.session_module import session


def get_session_context(session_id: str):
    """Returns the message history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session.
    Returns:
        List[dict]: A list of messages in the session history, where each message is a
        dictionary with 'role' and 'content' keys."""
    history = session.get_history(session_id)
    return history


def append_user_message(session_id: str, message: str):
    """Appends a user message to the session history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session.
        message (str): The content of the user message to be added."""
    session.add_message(session_id, "user", message)


def append_assistant_message(session_id: str, message: str):
    """Appends an assistant message to the session history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session.
        message (str): The content of the assistant message to be added."""
    session.add_message(session_id, "assistant", message)


def clear_session_context(session_id: str):
    """Clears the session history for the given session_id.
    Args:
        session_id (str): The unique identifier for the session to be cleared."""
    session.clear_session(session_id)
