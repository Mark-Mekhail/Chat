import os
import logging
from typing import Dict, Any
from app.config import settings


logger = logging.getLogger(__name__)


def get_model_path() -> str:
    model_path = settings.MODEL_PATH
    logger.info(f"Using model path: {model_path}")
    return model_path

def verify_model_exists(model_path: str) -> None:
    exists = os.path.exists(model_path)
    if not exists:
        err_msg = f"Model not found at path: {model_path}"
        logger.error(err_msg)
        raise FileNotFoundError(err_msg)
    else:
        logger.info(f"Model verified at path: {model_path}")

def get_model_info(model_path: str) -> Dict[str, Any]:
    try:
        verify_model_exists(model_path)

        size_bytes = os.path.getsize(model_path)
        size_mb = size_bytes / (1024 * 1024)
        
        return {
            "size_bytes": size_bytes,
            "size_mb": round(size_mb, 2),
            "path": model_path,
            "filename": os.path.basename(model_path)
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        return {
            "error": str(e)
        }
