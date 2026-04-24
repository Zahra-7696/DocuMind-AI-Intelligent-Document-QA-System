"""Project configuration."""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CHROMA_PERSIST_DIR = os.getenv(
    "CHROMA_PERSIST_DIR",
    str(BASE_DIR / "chroma_db")
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://127.0.0.1:11434"
)

OLLAMA_LLM_MODEL = os.getenv(
    "OLLAMA_LLM_MODEL",
    "llama3.1:8b"
)

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "mxbai-embed-large"
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

GRADIO_HOST = os.getenv(
    "GRADIO_HOST",
    "127.0.0.1"
)

GRADIO_PORT = int(os.getenv("GRADIO_PORT", "7860"))