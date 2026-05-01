from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse

from models.api import ChatRequest, ChatResponse
from services.pipeline import run
from core.session_module.session_service import (
    get_session_context,
    append_user_message,
    append_assistant_message,
    clear_session_context,
)

from core.logging_config import get_logger
from services.tts import synthesize_to_wav

logger = get_logger("backend", "backend_logs.log")

app = FastAPI(title="WikiRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


# ---- Chat endpoint
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        session_id = req.session_id or "default"

        logger.info(f"Session={session_id} | Query={req.query}")

        result = run(req.query)
        logger.info(f"Session={session_id} | fetched session query result")

        answer = result.answer
        warning = result.warning

        append_user_message(session_id, req.query)
        append_assistant_message(session_id, answer)

        if req.response_format == "audio":
            logger.info(f"Session={session_id} | Synthesizing response to audio")
            wav_path = synthesize_to_wav(answer)
            logger.info(f"Session={session_id} | Returning audio response")
            return FileResponse(
                wav_path,
                media_type="audio/wav",
                filename=f"response_{session_id}.wav"
            )
        logger.info(f"Session={session_id} | Returning text response")
        return ChatResponse(
            query=req.query,
            answer=answer,
            warning=warning,
            session_id=session_id,
        )

    except Exception as e:
        logger.error("Chat error: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    return {"session_id": session_id, "history": get_session_context(session_id)}


@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    clear_session_context(session_id)
    return {"status": "cleared", "session_id": session_id}
