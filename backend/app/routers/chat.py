from asyncio import to_thread
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestUserMessage
from pydantic import BaseModel
from typing import List, Literal
from app.services.llm_service import get_llm_response_stream

Role = Literal["user", "assistant"]

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/")
async def chat_stream(request: ChatRequest) -> StreamingResponse:
    try:
        conversation = [create_conversation_message(msg.role, msg.content) for msg in request.messages]
        
        async def stream_generator():
            async for text_chunk in get_llm_response_stream(conversation):
                yield f"data: {text_chunk}\n\n"
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def create_conversation_message(role: Role, content: str) -> ChatCompletionRequestMessage:
    match role:
        case "user":
            return ChatCompletionRequestUserMessage(role="user", content=content)
        case "assistant":
            return ChatCompletionRequestAssistantMessage(role="assistant", content=content)
        case _:
            raise ValueError(f"Invalid role: {role}")