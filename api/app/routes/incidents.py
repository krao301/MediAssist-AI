from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from ..models import Incident, IncidentEvent
from ..schemas import IncidentCreate, Incident as IncidentSchema
from ..deps.auth import demo_auth
from ..database import get_db
from ..services.summary import generate_incident_summary, export_to_text

router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.post("/create", response_model=IncidentSchema)
def create_incident(
    body: IncidentCreate,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Create a new emergency incident
    """
    # Get or create user
    user_id = 1  # Demo - in production, look up by user['sub']

    incident = Incident(
        user_id=user_id,
        lat=body.lat,
        lng=body.lng,
        type=body.type,
        severity=body.severity,
        status="ACTIVE",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.get("/{incident_id}", response_model=IncidentSchema)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Get incident details
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident


class IncidentEventCreate(BaseModel):
    step: str
    metadata: Optional[Dict[str, Any]] = None


@router.post("/{incident_id}/event")
def add_incident_event(
    incident_id: int,
    body: IncidentEventCreate,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Log an event/step in the incident timeline
    """
    # Check if incident exists
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail=f"Incident {incident_id} not found")
    
    event = IncidentEvent(
        incident_id=incident_id, step=body.step, event_metadata=body.metadata
    )

    db.add(event)
    db.commit()

    return {"ok": True, "event_id": event.id}


@router.post("/{incident_id}/resolve")
def resolve_incident(
    incident_id: int,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Mark incident as resolved
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.status = "RESOLVED"
    incident.ended_at = datetime.utcnow()
    db.commit()

    return {"ok": True, "incident_id": incident_id}


@router.get("/{incident_id}/summary")
def get_incident_summary(
    incident_id: int,
    format: str = "json",  # json or text
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Get incident summary/timeline for EMS or family
    """
    summary = generate_incident_summary(db, incident_id)

    if "error" in summary:
        raise HTTPException(status_code=404, detail=summary["error"])

    if format == "text":
        return {"summary": export_to_text(summary)}

    return summary
