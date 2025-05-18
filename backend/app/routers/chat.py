from fastapi import APIRouter, HTTPException
from llama_cpp import ChatCompletionRequestAssistantMessage, ChatCompletionRequestMessage, ChatCompletionRequestUserMessage
from pydantic import BaseModel
from typing import List, Literal
from app.services.llm_service import get_llm_response

Role = Literal["user", "assistant"]

class ChatMessage(BaseModel):
    role: Role
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    response: str


router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        conversation = [create_conversation_message(msg.role, msg.content) for msg in request.messages]
        llm_response = get_llm_response(conversation)

        return ChatResponse(response=llm_response)
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