"""Mock setup for application tests."""
import os
import asyncio
from typing import List, Dict, Any, AsyncIterator, Iterator
from unittest.mock import patch

# Set testing environment variables
os.environ["ENVIRONMENT"] = "test"
os.environ["MODEL_PATH"] = "/app/models/test-model.gguf"
os.environ["MODEL_DIR"] = "/app/models"
os.environ["TESTING"] = "true"

PatchType = Any
_active_patches: List[PatchType] = []

def _add_patch(target: str, **kwargs: Any) -> PatchType:
    p = patch(target, **kwargs)
    p.start()
    _active_patches.append(p)
    return p

# Mock model utilities
_add_patch('app.utils.model_utils.verify_model_exists', return_value=True)
_add_patch('app.utils.model_utils.get_model_path', return_value="/app/models/test-model.gguf")

mock_model_info: Dict[str, Any] = {
    "model_name": "test-model",
    "n_params": 7000000000,
    "n_ctx": 4096,
    "model_size": "7B",
    "loaded_in_4bit": True
}
_add_patch('app.utils.model_utils.get_model_info', return_value=mock_model_info)

class MockLlamaClass:
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.model_path: str = kwargs.get("model_path", "/app/models/test-model.gguf")
        
    def create_chat_completion_stream(self, messages: List[Dict[str, Any]], **kwargs: Any) -> Any:
        class Streamer:
            def __iter__(self) -> Iterator[Dict[str, Any]]:
                chunks: List[Dict[str, Any]] = [
                    {
                        "id": "test-chat-completion",
                        "object": "chat.completion.chunk",
                        "created": 1716201234,
                        "model": "test-model",
                        "choices": [{
                            "index": 0,
                            "delta": {"content": "This is "},
                            "finish_reason": None
                        }]
                    },
                    {
                        "id": "test-chat-completion",
                        "object": "chat.completion.chunk",
                        "created": 1716201235,
                        "model": "test-model",
                        "choices": [{
                            "index": 0, 
                            "delta": {"content": "a test "},
                            "finish_reason": None
                        }]
                    },
                    {
                        "id": "test-chat-completion",
                        "object": "chat.completion.chunk",
                        "created": 1716201236,
                        "model": "test-model",
                        "choices": [{
                            "index": 0,
                            "delta": {"content": "response"},
                            "finish_reason": "stop"
                        }]
                    }
                ]
                for chunk in chunks:
                    yield chunk

        return Streamer()

_add_patch('llama_cpp.Llama', new=MockLlamaClass)

async def mock_llm_stream(*args: Any, **kwargs: Any) -> AsyncIterator[str]:
    chunks = [
        '{"id":"test-id","choices":[{"delta":{"content":"This is "},"finish_reason":null}]}',
        '{"id":"test-id","choices":[{"delta":{"content":"a test "},"finish_reason":null}]}',
        '{"id":"test-id","choices":[{"delta":{"content":"response"},"finish_reason":"stop"}]}'
    ]
    
    for chunk in chunks:
        yield chunk
        await asyncio.sleep(0.01)

def apply_service_patches() -> bool:
    try:
        _add_patch('app.services.llm_service.llm_service.get_model_stats', 
                return_value=mock_model_info)
        
        _add_patch('app.services.llm_service.llm_service.get_llm_response_stream', 
                return_value=mock_llm_stream())
                
        return True
    except ImportError:
        return False

def stop_all_patches() -> None:
    for p in _active_patches:
        p.stop()
    _active_patches.clear()
