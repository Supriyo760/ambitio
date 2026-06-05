import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Grounded Legal Drafting Assistant"
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_api_key: str = os.getenv("LLM_API_KEY", "")
    chroma_db_dir: str = os.getenv("CHROMA_DB_DIR", "./chroma_db")
    upload_dir: str = os.getenv("UPLOAD_DIR", "./uploads")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    class Config:
        env_file = ".env"

settings = Settings()
