import os
from pathlib import Path
from llama_cpp import Llama
from app.utils.model_utils import get_model_path, verify_model_exists

# Initialize LLM model (lazily loaded)
_llm = None

def get_llm():
    """
    Lazily load the LLM model
    """
    global _llm
    if _llm is None:
        # Get the model path
        model_path = get_model_path()
        
        # Check if model exists
        if not verify_model_exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        # Load the model
        _llm = Llama(
            model_path=model_path,
            n_ctx=2048,  # Context window size
            n_threads=os.cpu_count(),  # Use all available CPU cores
        )
    return _llm

def get_llm_response(user_message: str, conversation_context: str = "") -> str:
    """
    Get a response from the LLM model for the user message
    """
    try:
        llm = get_llm()
        
        # Create prompt based on whether we have context or not
        if conversation_context:
            prompt = f"""
Previous conversation:
{conversation_context}

User: {user_message}
Assistant: """
        else:
            prompt = f"""
User: {user_message}
Assistant: """
        
        # Generate response
        response = llm(
            prompt,
            max_tokens=512,
            stop=["User:", "\n\n"],
            echo=False,
            temperature=0.7
        )
        
        # Extract the generated text
        return response["choices"][0]["text"].strip()
    
    except Exception as e:
        print(f"Error generating LLM response: {str(e)}")
        return f"Sorry, I encountered an error: {str(e)}"