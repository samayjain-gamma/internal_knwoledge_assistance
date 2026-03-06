from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Ollama  modl -> tinyllama , phi
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "phi"
    LLM_TEMPERATURE: float = 0.2

    EMBEDDING_MODEL: str = "nomic-embed-text"

    CHROMA_COLLECTION_NAME: str = "company_documents"
    CHROMA_PERSIST_DIR: Path = Path("./chroma_db")

    RETRIEVAL_TOP_K: int = 2
    CHUNK_SIZE: int = 800
    CHUNK_OVERLAP: int = 150

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Prevents reloading environment repeatedly.
    """
    return Settings()
