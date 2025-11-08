from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas import TriageInput, TriageResult
from ..deps.auth import require_auth, demo_auth
from ..services.llm import classify_and_plan
from ..database import get_db

router = APIRouter(prefix="/triage", tags=["triage"])

@router.post("", response_model=TriageResult)
def triage_incident(
    body: TriageInput,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)  # Change to require_auth for Auth0
):
    """
    Triage emergency based on user description
    Returns incident type, severity, and step-by-step guidance
    """
    result = classify_and_plan(body.text, body.locale, body.age_group)
    
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
