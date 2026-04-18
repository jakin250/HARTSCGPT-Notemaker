import os

from dotenv import load_dotenv


load_dotenv()


def _as_bool(value, default=False):
    if value is None:
        return default

    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_config():
    return {
        "note_reduction_ratio": min(
            max(float(os.getenv("NOTE_REDUCTION_RATIO", "0.5")), 0.1),
            0.5,
        ),
        "max_input_chars": int(os.getenv("LRW_MAX_INPUT_CHARS", "120000")),
        "max_upload_mb": int(os.getenv("MAX_UPLOAD_MB", "20")),
        "secret_key": os.getenv("FLASK_SECRET_KEY", "xai-notemaker-local-dev"),
        "host": os.getenv("FLASK_HOST", "0.0.0.0"),
        "port": int(os.getenv("FLASK_PORT", "5000")),
        "debug": _as_bool(os.getenv("FLASK_DEBUG"), default=False),
        "input_folder": "input_pdfs",
        "output_folder": "output",
        "log_folder": "logs",
    }
