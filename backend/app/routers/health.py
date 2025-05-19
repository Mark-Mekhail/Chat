import logging
import platform
import psutil
import time
from fastapi import APIRouter
from typing import Dict, Any

from app.services.llm_service import llm_service
from app.config import settings

logger = logging.getLogger(__name__)

SERVER_START_TIME = time.time()

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


def get_system_info() -> Dict[str, Any]:
    uptime = time.time() - SERVER_START_TIME
    
    return {
        "system": {
            "platform": platform.system(),
            "platform_version": platform.version(),
            "python_version": platform.python_version(),
            "cpu_count": psutil.cpu_count(),
            "cpu_usage_percent": psutil.cpu_percent(),
            "memory_total": psutil.virtual_memory().total,
            "memory_available": psutil.virtual_memory().available,
            "memory_used_percent": psutil.virtual_memory().percent,
            "uptime_seconds": int(uptime),
            "uptime_formatted": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s",
        }
    }

@router.get("/")
def health_check() -> Dict[str, Any]:
    system_info = get_system_info()
    
    try:
        model_stats = llm_service.get_model_stats()
        model_status = "healthy"
    except Exception as e:
        logger.error(f"Error getting model stats: {e}", exc_info=True)
        model_stats = {"error": str(e)}
        model_status = "unhealthy"
    
    return {
        "version": settings.API_VERSION,
        "model_status": model_status,
        "model_info": model_stats,
        "system_info": system_info
    }
