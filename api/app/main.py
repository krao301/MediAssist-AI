from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

from .database import init_db
from .routes import triage, alerts, route, incidents, contacts, voice, learning

# Initialize FastAPI app
app = FastAPI(
    title="MediAssist AI API",
    description="Emergency first-aid coach with hyperlocal alerts",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(triage.router)
app.include_router(alerts.router)
app.include_router(route.router)
app.include_router(incidents.router)
app.include_router(contacts.router)
app.include_router(voice.router)  # Voice call TwiML endpoints
app.include_router(learning.router)  # AI learning & feedback system


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    init_db()


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "MediAssist AI API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "endpoints": {
            "triage": "/triage",
            "alerts": "/alerts",
            "route": "/route",
            "incidents": "/incidents",
            "contacts": "/contacts",
        },
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
