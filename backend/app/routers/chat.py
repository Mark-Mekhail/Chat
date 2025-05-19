import logging
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestSystemMessage, ChatCompletionRequestUserMessage
from pydantic import BaseModel
from typing import Any, Dict, List, Literal
from app.services.llm_service import llm_service


Role = Literal["user", "assistant", "system"]

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


logger = logging.getLogger(__name__)


@router.get("/model-info")
async def get_model_info() -> Dict[str, Any]:
    try:
        return {
            "status": "success", 
            "data": llm_service.get_model_stats()
        }
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get model info: {str(e)}")

@router.post("/")
async def chat_stream(request: ChatRequest, client_request: Request) -> StreamingResponse:
    """
    Stream chat completions from the LLM based on the conversation history.
    
    Args:
        request: The chat request containing the conversation history.
        client_request: The original FastAPI request object.
        
    Returns:
        A streaming response with the LLM's replies.
    """
    client_host = client_request.client.host if client_request.client else "unknown"
    logger.info(f"Chat request received from {client_host} with {len(request.messages)} messages")
    
    try:
        conversation = [create_conversation_message(msg.role, msg.content) for msg in request.messages]
        
        async def stream_generator():
            try:
                async for text_chunk in llm_service.get_llm_response_stream(conversation):
                    yield f"data: {text_chunk}\n\n"
                yield "data: [DONE]\n\n"
            except Exception as e:
                logger.error(f"Error in stream generator: {str(e)}", exc_info=True)
                yield f"data: [ERROR] {str(e)}\n\n"
                yield "data: [DONE]\n\n"
            
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache", 
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
    except ValueError as e:
        logger.warning(f"Validation error in chat request: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in chat_stream: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

def create_conversation_message(role: Role, content: str) -> ChatCompletionRequestMessage:
    """
    Create a conversation message compatible with the llama-cpp library.
    """
    match role:
        case "user":
            return ChatCompletionRequestUserMessage(role="user", content=content)
        case "assistant":
            return ChatCompletionRequestAssistantMessage(role="assistant", content=content)
        case "system":
            return ChatCompletionRequestSystemMessage(role="system", content=content)
        case _:
            raise ValueError(f"Invalid role: {role}")