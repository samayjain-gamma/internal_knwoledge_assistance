# core/config.py

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central configuration for the Internal Knowledge Assistant.
    Loaded from environment variables or .env file.
    """

    # App Info
    APP_NAME: str = "Internal Knowledge Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    ## LLM (Ollama - Phi)
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "phi3"
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_TOKENS: int = 512
    # LLM_TIMEOUT: int = 60

    ## Embedding Model (Ollama or other)
    EMBEDDING_MODEL: str = "nomic-embed-text"

    ## Vector Database (Chroma)
    CHROMA_COLLECTION_NAME: str = "company_documents"
    CHROMA_PERSIST_DIR: Path = Path("./chroma_db")

    ## Retrieval
    RETRIEVAL_TOP_K: int = 4
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    ## Memory
    MAX_HISTORY_TURNS: int = 5

    ## Guardrails
    MAX_QUERY_LENGTH: int = 1000
    # MAX_RETRIES: int = 2
    # ENABLE_INJECTION_DETECTION: bool = True
    # ENABLE_GROUNDING_VALIDATION: bool = True
    # ENABLE_CITATION_VALIDATION: bool = True

    ## Monitoring
    ENABLE_METRICS: bool = True
    LATENCY_WARNING_THRESHOLD: float = 5.0  # seconds

    class Config:
        env_file = ".env"
        # env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Prevents reloading environment repeatedly.
    """
    return Settings()
