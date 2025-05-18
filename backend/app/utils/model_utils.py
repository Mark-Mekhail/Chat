"""
Utility functions for model management.
"""
import os
from typing import Optional


def get_model_path() -> str:
    return os.environ.get("MODEL_PATH", "/app/models/llama-2-7b-chat.gguf")


def verify_model_exists(model_path: Optional[str] = None) -> bool:
    if not model_path:
        model_path = get_model_path()
    
    return os.path.exists(model_path)
