# Simple AI Chat Application

A containerized AI chat application with a React frontend and FastAPI backend that communicates with an open-source LLM.

## Features

- Simple, responsive chat interface
- FastAPI backend with LLM integration
- Docker containerization for easy deployment
- Uses open-source LLM (Llama 2 7B Chat)

## Prerequisites

- Docker and Docker Compose
- A compatible LLM model file (e.g., llama-2-7b-chat.gguf)

## Quick Start

1. **Run the automated setup script**

   The simplest way to get started is to use the provided setup script, which will:
   - Check for required dependencies (Docker, Python)
   - Install necessary tools if possible
   - Automatically download the LLM model if not present
   - Start the application
   
   ```bash
   # Make the script executable
   chmod +x start.sh
   
   # Run the setup script
   ./start.sh
   ```

2. **Alternative: Manual Setup**

   If you prefer to set up manually:
   
   a. Download a compatible GGUF model:
   ```bash
   # Download the model
   python3 download_model.py
   ```
   
   b. Start the application with Docker Compose:
   ```bash
   docker compose up -d
   ```

3. **Access the application**
   
   Open your browser and navigate to:
   - Frontend: http://localhost:80
   - API documentation: http://localhost:8000/docs

## Development

### Frontend

The frontend is built with:
- React 19
- TypeScript
- Vite

To run the frontend locally:

```bash
cd frontend
npm install
npm run dev
```

### Backend

The backend is built with:
- FastAPI
- llama-cpp-python

To run the backend locally:

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Model Configuration

The model configuration can be adjusted in the `docker-compose.yml` file:

```yaml
environment:
  - MODEL_DIR=/app/models
  - MODEL_PATH=/app/models/llama-2-7b-chat.gguf
```

## License

MIT