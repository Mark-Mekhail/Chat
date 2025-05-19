import os

from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Model settings
    MODEL_PATH: str = os.environ.get("MODEL_PATH", "/app/models/llama-2-7b-chat.gguf")
    N_CTX: int = int(os.environ.get("N_CTX", "2048"))
    N_THREADS: Optional[int] = os.cpu_count()  # Use all available CPU cores
    N_GPU_LAYERS: int = int(os.environ.get("N_GPU_LAYERS", "-1"))  # -1 means use all if available
    
    # API settings
    API_PREFIX: str = "/api"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = os.environ.get("DEBUG", "False").lower() == "true"
    
    # CORS settings
    CORS_ORIGINS: list[str] = ["*"]  # In production, specify exact origins
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
