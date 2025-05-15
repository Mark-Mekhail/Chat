#!/usr/bin/env bash

# A simple script to start the AI Chat application

# Check for required tools and install if possible
check_install_dependency() {
    local cmd=$1
    local name=$2
    local install_cmd=$3
    
    if ! command -v "$cmd" &> /dev/null; then
        echo "$name is not installed."
        if [[ "$install_cmd" != "skip" ]]; then
            echo "Attempting to install $name..."
            if eval "$install_cmd"; then
                echo "$name installed successfully."
            else
                echo "Failed to install $name. Please install it manually."
                exit 1
            fi
        else
            echo "Please install $name manually."
            exit 1
        fi
    else
        echo "✅ $name is installed."
    fi
}

# macOS specific installations using brew
if [[ "$(uname)" == "Darwin" ]]; then
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew is not installed. It's recommended for installing dependencies on macOS."
        echo "Install Homebrew? (y/n)"
        read -r install_brew
        if [[ "$install_brew" == "y" || "$install_brew" == "Y" ]]; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        else
            echo "Skipping Homebrew installation."
        fi
    fi
    
    # Use brew if available
    if command -v brew &> /dev/null; then
        check_install_dependency docker "Docker" "brew install --cask docker"
        # Python is needed for model download
        check_install_dependency python3 "Python" "brew install python"
    else
        check_install_dependency docker "Docker" "skip"
        check_install_dependency python3 "Python" "skip"
    fi
else
    # For Linux or other platforms
    check_install_dependency docker "Docker" "skip"
    check_install_dependency python3 "Python" "skip"
fi

# Check if Docker is running
if command -v docker &> /dev/null; then
    docker info &> /dev/null
    if [ $? -ne 0 ]; then
        echo "Docker is installed but not running. Starting Docker..."
        # Try to start Docker Desktop on macOS
        if [[ "$(uname)" == "Darwin" ]]; then
            open -a Docker
            echo "Waiting for Docker to start..."
            sleep 10  # Give Docker time to start
        else
            echo "Please start Docker manually."
            exit 1
        fi
    else
        echo "✅ Docker is running."
    fi
fi

# Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    echo "Error: Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create models directory if it doesn't exist
if [ ! -d "models" ]; then
    echo "Creating models directory..."
    mkdir -p models
fi

# Setup Python environment and install dependencies
setup_python_env() {
    echo "Setting up Python virtual environment..."
    
    # Create venv directory if it doesn't exist
    VENV_DIR=".venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating virtual environment in $VENV_DIR..."
        python3 -m venv "$VENV_DIR"
        if [ $? -ne 0 ]; then
            echo "Failed to create virtual environment. Trying with user site packages..."
            # Try with system site packages if regular venv fails
            python3 -m venv "$VENV_DIR" --system-site-packages
            if [ $? -ne 0 ]; then
                echo "❌ Failed to create Python virtual environment."
                echo "Please install the required packages manually:"
                echo "python3 -m pip install --user requests tqdm"
                return 1
            fi
        fi
    else
        echo "Using existing virtual environment in $VENV_DIR"
    fi
    
    # Activate the virtual environment
    if [[ "$(uname)" == "Darwin" ]] || [[ "$(uname)" == "Linux" ]]; then
        echo "Activating virtual environment..."
        source "$VENV_DIR/bin/activate"
    else
        # Windows
        source "$VENV_DIR/Scripts/activate"
    fi
    
    # Install dependencies in the virtual environment
    echo "Installing required Python packages in virtual environment..."
    pip install --upgrade pip
    pip install requests tqdm
    
    return $?
}

# Check if model file exists
if [ ! -f "models/llama-2-7b-chat.gguf" ]; then
    echo "Model file not found in models directory."
    echo "Downloading model automatically..."
    
    if [ -f "download_model.py" ]; then
        # Setup Python environment with required packages
        setup_python_env
        if [ $? -ne 0 ]; then
            echo "❌ Failed to set up Python environment."
            echo "You can try manually downloading a model from:"
            echo "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
            echo "and placing it in the models/ directory as llama-2-7b-chat.gguf"
            exit 1
        fi
        
        # Check system resources to decide on model size
        MEMORY_MB=$(( $(sysctl -n hw.memsize 2>/dev/null || free -m | grep Mem | awk '{print $2}' 2>/dev/null || echo 8000) / 1024 / 1024 ))
        
        if [ "$MEMORY_MB" -lt 8000 ]; then
            echo "Detected system with limited memory (${MEMORY_MB}MB). Using smaller model variant."
            python download_model.py --non-interactive --smaller-model
        else
            echo "Detected system with sufficient memory (${MEMORY_MB}MB)."
            python download_model.py --non-interactive
        fi
        
        if [ $? -ne 0 ]; then
            echo "Python-based download failed. Attempting direct download with curl..."
            
            # Fallback to curl or wget for direct download
            if command -v curl &> /dev/null; then
                MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
                echo "Downloading model with curl..."
                curl -L --progress-bar "$MODEL_URL" -o "models/llama-2-7b-chat.gguf"
                
                if [ $? -ne 0 ]; then
                    echo "❌ Direct download failed."
                    echo "You can try manually downloading a model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
                    echo "and placing it in the models/ directory as llama-2-7b-chat.gguf"
                    exit 1
                else
                    echo "✅ Model downloaded successfully with curl!"
                fi
            elif command -v wget &> /dev/null; then
                MODEL_URL="https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
                echo "Downloading model with wget..."
                wget -O "models/llama-2-7b-chat.gguf" "$MODEL_URL" --show-progress
                
                if [ $? -ne 0 ]; then
                    echo "❌ Direct download failed."
                    echo "You can try manually downloading a model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
                    echo "and placing it in the models/ directory as llama-2-7b-chat.gguf"
                    exit 1
                else
                    echo "✅ Model downloaded successfully with wget!"
                fi
            else
                echo "❌ Failed to download model automatically."
                echo "You can try manually downloading a model from: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF"
                echo "and placing it in the models/ directory as llama-2-7b-chat.gguf"
                exit 1
            fi
        fi
        
        # Deactivate virtual environment
        if command -v deactivate &> /dev/null; then
            deactivate
        fi
    else
        echo "Error: download_model.py script not found."
        exit 1
    fi
fi

# Install docker-compose if needed (using virtual env if necessary)
if ! docker compose version &> /dev/null; then
    echo "Docker Compose not found as 'docker compose'..."
    
    if command -v docker-compose &> /dev/null; then
        echo "Found legacy 'docker-compose' command instead."
        # Create an alias or function to use docker-compose instead
        docker() {
            if [ "$1" = "compose" ]; then
                shift
                command docker-compose "$@"
            else
                command docker "$@"
            fi
        }
        export -f docker
    elif command -v python3 &> /dev/null; then
        echo "Attempting to install docker-compose..."
        
        # Create and use virtual environment for pip installation
        VENV_DIR=".venv"
        if [ -d "$VENV_DIR" ]; then
            # Use existing venv
            if [[ "$(uname)" == "Darwin" ]] || [[ "$(uname)" == "Linux" ]]; then
                source "$VENV_DIR/bin/activate"
            else
                source "$VENV_DIR/Scripts/activate"
            fi
            pip install docker-compose
            
            if command -v deactivate &> /dev/null; then
                deactivate
            fi
        else
            # Try user installation
            python3 -m pip install --user docker-compose
        fi
    fi
    
    # Final check for docker compose
    if ! docker compose version &> /dev/null && ! command -v docker-compose &> /dev/null; then
        echo "❌ Error: Docker Compose not available. Please install Docker Compose first."
        exit 1
    fi
fi

# Verify model exists before starting
if [ ! -f "models/llama-2-7b-chat.gguf" ]; then
    echo "Error: Model file still not found. Cannot continue."
    exit 1
fi

echo "✅ Model file found: models/llama-2-7b-chat.gguf"

# Pull latest Docker images
echo "Pulling latest Docker images..."
docker compose pull

# Start the application
echo "Starting AI Chat application..."
docker compose up -d --build

# Check for build errors
build_success=$(docker compose ps | grep -c "ai-chat")
if [ "$build_success" -eq 0 ]; then
    echo "⚠️ Build may have failed. Checking logs..."
    docker compose logs frontend
    
    echo "Would you like to view detailed build logs? (y/n)"
    read -r view_logs
    if [[ "$view_logs" == "y" || "$view_logs" == "Y" ]]; then
        docker compose logs --tail=100 frontend
    fi
    
    echo "Would you like to try building again? (y/n)"
    read -r rebuild
    if [[ "$rebuild" == "y" || "$rebuild" == "Y" ]]; then
        echo "Rebuilding frontend container..."
        docker compose build frontend
        docker compose up -d
    fi
fi    # Check if services are running
    echo "Checking if services are running..."
    max_attempts=5
    attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "Attempt $attempt of $max_attempts..."
        
        # Use docker container ls instead of docker compose ps to check container status
        if docker container ls | grep -q "ai-chat-backend" && docker container ls | grep -q "ai-chat-frontend"; then
            echo "✅ AI Chat application is running successfully!"
            echo "You can access it at http://localhost:80"
            echo ""
            echo "To view logs: docker compose logs -f"
            echo "To stop the application: docker compose down"
            
            if command -v open &> /dev/null; then
                echo "Opening app in browser..."
                open http://localhost:80
            fi
            
            exit 0
        fi
        
        echo "Services not fully running yet. Waiting..."
        sleep 3
        ((attempt++))
    done

echo "echo "❌ Error: Failed to detect running application properly, but containers may still be running."
echo "Checking container status:"
docker container ls | grep "ai-chat"
echo
echo "Checking logs:"
docker compose logs --tail=10"
echo "Checking container status:"
docker compose ps
echo ""
echo "Checking logs:"
docker compose logs
exit 1
