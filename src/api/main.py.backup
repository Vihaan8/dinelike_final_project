"""
FastAPI main application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .routes import restaurants, quiz, community, results

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="DineLike API",
    description="Restaurant recommendation and taste twin matching API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(restaurants.router)
app.include_router(quiz.router)
app.include_router(community.router)
app.include_router(results.router)

@app.get("/")
async def root():
    return {
        "message": "DineLike API",
        "version": "1.0.0",
        "endpoints": {
            "restaurants": "/api/restaurants",
            "quiz": "/api/quiz",
            "community": "/api/community",
            "results": "/api/results",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
