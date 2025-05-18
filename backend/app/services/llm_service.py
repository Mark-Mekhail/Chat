import asyncio
import os
from typing import AsyncIterator, Iterator, List
from llama_cpp import ChatCompletionRequestMessage, CreateChatCompletionStreamResponse, Llama
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

def _next_or_none(it: Iterator[CreateChatCompletionStreamResponse]) -> CreateChatCompletionStreamResponse | None:
    try:
        return next(it)
    except StopIteration:
        return None

async def get_llm_response_stream(conversation: List[ChatCompletionRequestMessage]) -> AsyncIterator[str]:
    try:
        if not conversation:
            raise ValueError("Conversation cannot be empty")

        response_iter: Iterator[CreateChatCompletionStreamResponse] = llm.create_chat_completion(
            messages=conversation,
            stream=True,
        ) # type: ignore

        while True:
            # this blocks only the helper thread, not the event loop
            chunk = await asyncio.to_thread(_next_or_none, response_iter)
            if chunk is None:
                break

            delta = chunk["choices"][0]["delta"]
            if "content" in delta and delta["content"]:
                yield delta["content"]
    except Exception as e:
        raise RuntimeError(f"Error streaming response from LLM: {str(e)}")