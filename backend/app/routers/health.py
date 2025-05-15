from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.utils.model_utils import get_model_info

router = APIRouter(
    prefix="/health",
    tags=["health"],
)


class HealthResponse(BaseModel):
    status: str
    version: str
    model: dict


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Get the health status of the API and the LLM model.
    """
    # Get model info
    model_info = get_model_info()
    
    return HealthResponse(
        status="ok",
        version="0.1.0",
        model=model_info
    )
