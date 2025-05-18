"""
Utility functions for model management.
"""
import os


def get_model_path() -> str:
    return os.environ.get("MODEL_PATH", "/app/models/llama-2-7b-chat.gguf")


def verify_model_exists(model_path: str) -> bool:
    return os.path.exists(model_path)
