#!/usr/bin/env bash
# Handle model download and management

# Source utils
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/utils.sh"

check_and_download_model() {
  MODEL_DIR="../models"
  MODEL_PATH="$MODEL_DIR/llama-2-7b-chat.gguf"
  
  # Different model sizes based on system memory
  MEMORY_MB=$(get_system_memory)
  if [ "$MEMORY_MB" -lt 8000 ]; then
    print_message "info" "Detected system with limited memory (${MEMORY_MB}MB). Using smaller model variant."
    MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_S.gguf"
  else
    print_message "info" "Detected system with sufficient memory (${MEMORY_MB}MB)."
    MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
  fi

  cd "$SCRIPT_DIR"
  
  ensure_directory "$MODEL_DIR"
  
  if [ ! -f "$MODEL_PATH" ]; then
    print_message "warning" "Model file not found in models directory."
    print_message "info" "Downloading model automatically..."
    
    download_model
  else
    print_message "success" "Model file found: $MODEL_PATH"
  fi
  
  if [ ! -f "$MODEL_PATH" ]; then
    print_message "error" "Error: Model file still not found. Cannot continue."
    return 1
  fi
  
  return 0
}

download_model() {
  MODEL_DIR="../models"
  MODEL_PATH="$MODEL_DIR/llama-2-7b-chat.gguf"
  
  if command_exists curl; then
    print_message "info" "Downloading model with curl..."
    curl -L --progress-bar "$MODEL_URL" -o "$MODEL_PATH"
    
    if [ $? -ne 0 ]; then
      print_message "error" "Direct download with curl failed."
      try_wget_download
    else
      print_message "success" "Model downloaded successfully with curl!"
      return 0
    fi
  else
    try_wget_download
  fi
}

try_wget_download() {
  if command_exists wget; then
    print_message "info" "Downloading model with wget..."
    wget -O "$MODEL_PATH" "$MODEL_URL" --show-progress
    
    if [ $? -ne 0 ]; then
      print_message "error" "Direct download with wget failed."
      print_message "info" "You can try manually downloading a model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
      print_message "info" "and placing it in the models/ directory as llama-2-7b-chat.gguf"
      return 1
    else
      print_message "success" "Model downloaded successfully with wget!"
      return 0
    fi
  else
    print_message "error" "Failed to download model automatically. Neither curl nor wget is available."
    print_message "info" "You can try manually downloading a model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
    print_message "info" "and placing it in the models/ directory as llama-2-7b-chat.gguf"
    return 1
  fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  check_and_download_model
fi
