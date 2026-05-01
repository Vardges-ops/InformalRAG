import pyttsx3
import tempfile
from pathlib import Path
from core.logging_config import get_logger

_engine = None
logger = get_logger("audio_generator", "tts.log")


def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 180)
    return _engine


def synthesize_to_wav(text: str) -> Path:
    """
    Returns path to a temporary .wav file containing speech.
    """
    engine = _get_engine()

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp_path = Path(tmp.name)
    tmp.close()
    logger.info(f"Synthesizing text to audio at {tmp_path}")

    engine.save_to_file(text, str(tmp_path))
    logger.info("Running TTS engine to generate audio")

    engine.runAndWait()

    return tmp_path