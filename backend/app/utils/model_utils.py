"""
Utility functions for model management.
"""
import os
from pathlib import Path
from typing import Optional


def get_model_path() -> str:
    """
    Get the model path from environment variables or use the default path.
    This is helpful for both local development and containerized environments.
    """
    # First try to get the model path from environment variables
    model_path = os.environ.get("MODEL_PATH")
    
    if not model_path:
        # For local development, check the LOCAL_MODEL_PATH
        local_model_path = os.environ.get("LOCAL_MODEL_PATH")
        if local_model_path and os.path.exists(local_model_path):
            return local_model_path
            
        # Otherwise use the default path
        model_dir = os.environ.get("MODEL_DIR", "/app/models")
        model_path = os.path.join(model_dir, "llama-2-7b-chat.gguf")
    
    return model_path


def verify_model_exists(model_path: Optional[str] = None) -> bool:
    """
    Verify that the model file exists.
    """
    if not model_path:
        model_path = get_model_path()
    
    return os.path.exists(model_path)


def get_model_info(model_path: Optional[str] = None) -> dict:
    """
    Get information about the model file.
    """
    if not model_path:
        model_path = get_model_path()
    
    if not os.path.exists(model_path):
        return {"error": f"Model file not found at {model_path}"}
    
    file_size = os.path.getsize(model_path)
    file_size_mb = file_size / (1024 * 1024)  # Convert to MB
    
    return {
        "path": model_path,
        "size": f"{file_size_mb:.2f} MB",
        "exists": True
    }
