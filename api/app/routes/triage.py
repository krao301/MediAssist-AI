from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas import TriageInput, TriageResult
from ..deps.auth import require_auth, demo_auth
from ..services.hybrid_rag import HybridRAGSystem
from ..services.voice_call import make_emergency_call
from ..database import get_db

router = APIRouter(prefix="/triage", tags=["triage"])

# Initialize Hybrid RAG System (singleton)
_rag_system = None

def get_rag_system():
    """Get or initialize Hybrid RAG System"""
    global _rag_system
    if _rag_system is None:
        print("Initializing Hybrid RAG System...")
        _rag_system = HybridRAGSystem()
    return _rag_system

@router.post("", response_model=TriageResult)
def triage_incident(
    body: TriageInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)  # Change to require_auth for Auth0
):
    """
    Triage emergency using Hybrid RAG System
    (Vector DB + Knowledge Graph + Gemini AI)
    Returns incident type, severity, and step-by-step guidance
    
    AUTO-TRIGGERS SOS CALL for CRITICAL emergencies
    """
    rag = get_rag_system()

    # Prepare location if available
    location = None
    if hasattr(body, 'latitude') and hasattr(body, 'longitude'):
        if body.latitude and body.longitude:
            location = {"lat": body.latitude, "lng": body.longitude}

    # Classify using hybrid RAG
    result = rag.classify_emergency(
        user_input=body.text,
        age_group=body.age_group or "adult",
        location=location
    )

    # AUTO-TRIGGER SOS CALL for CRITICAL/SEVERE emergencies
    if result.get("requires_sos") and result.get("sos_number"):
        emergency_type = result.get("type", "unknown")
        severity = result.get("severity", "UNKNOWN")
        
        print(f"🚨 CRITICAL EMERGENCY DETECTED: {emergency_type} ({severity})")
        print(f"   Auto-triggering SOS call to {result['sos_number']}")
        
        # Make emergency call in background (non-blocking)
        background_tasks.add_task(
            make_emergency_call,
            to_number=result["sos_number"],
            incident_id=0,  # Will be updated when incident is created
            emergency_type=emergency_type,
            severity=severity,
            location=location or {}
        )

    return TriageResult(**result)

@router.post("/voice")
def triage_voice(
    audio_data: bytes,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Triage from voice input (Whisper STT)
    Stretch feature - for now returns placeholder
    """
    # TODO: Implement Whisper STT on DigitalOcean Gradient
    # For MVP, use Web Speech API on frontend
    
    return {
        "message": "Voice triage not implemented yet. Use Web Speech API on frontend.",
        "suggestion": "Use /triage endpoint with text transcription from frontend"
    }
