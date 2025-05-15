from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat, health

app = FastAPI(
    title="Simple AI Chat API",
    description="A simple API for chatting with an open-source LLM",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(health.router)
app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Simple AI Chat API. Go to /docs for documentation."}