from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "DevOps RAG Assistant API"
    VECTOR_STORE_PATH: str = "../data/vector_store"
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"
    OLLAMA_MODEL: str = "llama3.2:1b"
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    TEMPERATURE: float = 0.2
    TOP_K: int = 4

    model_config = SettingsConfigDict(env_file="backend/.env", extra="ignore")

settings = Settings()