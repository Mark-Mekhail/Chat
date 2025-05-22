from unittest.mock import MagicMock, patch
from typing import Dict, Any, List, AsyncIterator
import json
import asyncio

class MockLLM:
    @staticmethod
    def get_mock_model_stats() -> Dict[str, Any]:
        return {
            "model_name": "test-model",
            "n_params": 7000000000,
            "n_ctx": 4096,
            "model_size": "7B",
            "loaded_in_4bit": True,
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
    
    @staticmethod
    def create_mock_response() -> str:
        return json.dumps({
            "id": "test-completion-id",
            "object": "chat.completion.chunk",
            "created": 1716201234,
            "model": "test-model",
            "choices": [
                {
                    "index": 0,
                    "delta": {"content": "This is a test response"},
                    "finish_reason": "stop"
                }
            ]
        })
    
    @staticmethod
    async def get_mock_stream() -> AsyncIterator[str]:
        responses = [
            json.dumps({
                "id": "test-completion-id",
                "object": "chat.completion.chunk",
                "created": 1716201234,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": "This is "},
                        "finish_reason": None
                    }
                ]
            }),
            json.dumps({
                "id": "test-completion-id",
                "object": "chat.completion.chunk",
                "created": 1716201235,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": "a test "},
                        "finish_reason": None
                    }
                ]
            }),
            json.dumps({
                "id": "test-completion-id",
                "object": "chat.completion.chunk",
                "created": 1716201236,
                "model": "test-model",
                "choices": [
                    {
                        "index": 0,
                        "delta": {"content": "response."},
                        "finish_reason": "stop"
                    }
                ]
            })
        ]
        
        for response in responses:
            yield response
            await asyncio.sleep(0.01)

    @staticmethod
    def setup_mock_llm() -> List[Any]:
        patches: List[Any] = []
        
        patches.append(patch('app.utils.model_utils.verify_model_exists', return_value=True))
        patches.append(patch('app.utils.model_utils.get_model_path', return_value="test_model_path"))
        patches.append(patch('app.utils.model_utils.get_model_info', 
                          return_value=MockLLM.get_mock_model_stats()))
        
        mock_llama = MagicMock()
        mock_llama_instance = MagicMock()
        mock_llama.return_value = mock_llama_instance
        mock_llama_instance.tokenize.return_value = [1, 2, 3, 4]
        
        patches.append(patch('llama_cpp.Llama', new=mock_llama))
        
        for p in patches:
            p.start()
            
        return patches
