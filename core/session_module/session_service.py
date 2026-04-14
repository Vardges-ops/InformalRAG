from core.session_module import session


def get_session_context(session_id: str):
    history = session.get_history(session_id)
    return history


def append_user_message(session_id: str, message: str):
    session.add_message(session_id, "user", message)


def append_assistant_message(session_id: str, message: str):
    session.add_message(session_id, "assistant", message)


def clear_session_context(session_id: str):
    session.clear_session(session_id)
