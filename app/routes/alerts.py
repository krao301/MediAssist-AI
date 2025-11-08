from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas import AlertInput, AlertResult
from ..deps.auth import require_auth, demo_auth
from ..services.geo import contacts_within_radius
from ..services.notify import send_alerts
from ..database import get_db
import os

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("", response_model=AlertResult)
def send_alert(
    body: AlertInput,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)  # Change to require_auth for Auth0
):
    """
    Send hyperlocal alerts to nearby contacts within radius
    """
    # Get user_id from auth
    # For demo, we'll use a placeholder
    user_id = 1  # In production: get from database using user['sub']
    
    # Find nearby contacts
    nearby_contacts = contacts_within_radius(
        db, user_id, body.lat, body.lng, body.radius_m
    )
    
    if not nearby_contacts:
        return AlertResult(
            ok=True,
            count=0,
            contacts_notified=[]
        )
    
    # Send alerts via Twilio
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    notified = send_alerts(
        nearby_contacts,
        body.message,
        body.lat,
        body.lng,
        base_url
    )
    
    return AlertResult(
        ok=True,
        count=len(notified),
        contacts_notified=notified
    )
