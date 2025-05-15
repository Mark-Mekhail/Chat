from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.llm_service import get_llm_response

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)


class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]


class ChatResponse(BaseModel):
    response: str


@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat with the LLM model.
    """
    try:
        # Extract the last user message
        user_messages = [msg.content for msg in request.messages if msg.role == "user"]
        if not user_messages:
            raise HTTPException(status_code=400, detail="No user message provided")
        
        last_user_message = user_messages[-1]
        
        # Get the conversation history as context
        conversation_history = [f"{msg.role}: {msg.content}" for msg in request.messages[:-1]]
        conversation_context = "\n".join(conversation_history) if conversation_history else ""
        
        # Get response from LLM
        llm_response = get_llm_response(last_user_message, conversation_context)
        
        return ChatResponse(response=llm_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))