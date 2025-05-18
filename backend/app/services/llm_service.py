import os
from typing import List
from llama_cpp import ChatCompletionRequestMessage, Llama
from app.utils.model_utils import get_model_path, verify_model_exists


model_path = get_model_path()

if not verify_model_exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

llm = Llama(
    model_path=model_path,
    n_ctx=2048,
    n_threads=os.cpu_count(),  # Use all available CPU cores
    n_gpu_layers=-1,           # Use GPU layers if available, otherwise CPU
)

def get_llm_response(conversation: List[ChatCompletionRequestMessage]) -> str:
    try:
        if not conversation:
            raise ValueError("Conversation cannot be empty")

        response = llm.create_chat_completion(
            messages=conversation,
            stream=False,
        )

        return response["choices"][0]["message"]["content"].strip() # type: ignore
    
    except Exception as e:
        raise RuntimeError(f"Error generating response from LLM: {str(e)}")