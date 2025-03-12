from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from typing import List, Optional
import os

# Import routers
from routers import auth, users, docs, agents

# Create FastAPI app
app = FastAPI(
    title="Studi API",
    description="API for Studi - AI-Powered Learning Assistant",
    version="0.1.0",
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://studi.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(docs.router, prefix="/api/docs", tags=["Documentation"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Studi API",
        "docs": "/docs",
        "redoc": "/redoc",
    }

# Health check endpoint
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    ) 