import asyncio
import logging
import time
from typing import AsyncIterator, Iterator, List, Optional, Dict, Any
from llama_cpp import ChatCompletionRequestMessage, CreateChatCompletionStreamResponse, Llama
from app.utils.model_utils import get_model_path, verify_model_exists, get_model_info
from app.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    _instance: Optional['LLMService'] = None

    model_path: str
    model_info: Dict[str, Any]
    start_time: float
    llm: Llama
    
    def __new__(cls):
        if cls._instance is None:
            logger.info("Initializing LLM service")
            cls._instance = super(LLMService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        self.model_path = get_model_path()
        self.model_info = get_model_info(self.model_path)
        self.start_time = time.time()
        
        verify_model_exists(self.model_path)
        
        logger.info(f"Loading model from {self.model_path}")
        logger.info(f"Model size: {self.model_info.get('size_mb', 'unknown')} MB")
        
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=settings.N_CTX,
                n_threads=settings.N_THREADS,
                n_gpu_layers=settings.N_GPU_LAYERS,
            )
            logger.info("LLM model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load LLM model: {e}")
            raise
    
    @staticmethod
    def _next_or_none(it: Iterator[CreateChatCompletionStreamResponse]) -> Optional[CreateChatCompletionStreamResponse]:
        """
        Get the next item from an iterator or None if StopIteration is raised.
        """
        try:
            return next(it)
        except StopIteration:
            return None
    
    async def get_llm_response_stream(self, conversation: List[ChatCompletionRequestMessage]) -> AsyncIterator[str]:
        """
        Stream responses from the LLM model based on the conversation history.
        
        Args:
            conversation: List of messages representing the conversation history.
            
        Yields:
            Chunks of the LLM response.
            
        Raises:
            ValueError: If the conversation is empty.
            RuntimeError: If there's an error streaming the response.
        """
        if not conversation:
            error_msg = "Conversation cannot be empty"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        try:
            logger.info(f"Generating LLM response for the following conversation: {conversation}")

            response_iter = self.llm.create_chat_completion(
                messages=conversation,
                stream=True,
                temperature=0.7,
                max_tokens=1024,
            )
            
            tokens_generated = 0
            start_time = time.time()
            
            while True:
                # This blocks only the helper thread, not the event loop
                chunk = await asyncio.to_thread(self._next_or_none, response_iter) # type: ignore
                if chunk is None:
                    break
                
                delta = chunk["choices"][0]["delta"]
                if "content" in delta and delta["content"]:
                    content = delta["content"]
                    tokens_generated += 1
                    yield content
            
            generation_time = time.time() - start_time
            logger.info(f"Generated response with {tokens_generated} chunks in {generation_time:.2f}s")
            
        except Exception as e:
            error_msg = f"Error streaming response from LLM: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RuntimeError(error_msg)
    
    def get_model_stats(self) -> Dict[str, Any]:
        uptime = time.time() - self.start_time
        return {
            "model_info": self.model_info,
            "context_window": settings.N_CTX,
            "threads": settings.N_THREADS,
            "gpu_layers": settings.N_GPU_LAYERS,
            "uptime_seconds": int(uptime),
            "uptime_formatted": f"{int(uptime // 3600)}h {int((uptime % 3600) // 60)}m {int(uptime % 60)}s",
        }


llm_service = LLMService()