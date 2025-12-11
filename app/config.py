# app/config.py

from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    faiss_index_path: str = "storage/faiss_index.bin"
    sqlite_db: str = "storage/pharmatrack.db"

    embed_model: str = "all-MiniLM-L6-v2"

    chunk_tokens: int = 500
    chunk_overlap: int = 50

    similarity_threshold: float = 0.65
    top_k: int = 8

    class Config:
        env_file = ".env"


settings = Settings()
