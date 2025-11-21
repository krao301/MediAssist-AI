from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from ..models import Incident, IncidentEvent

def generate_incident_summary(db: Session, incident_id: int) -> Dict[str, Any]:
    """
    Generate a timeline summary of incident for EMS/family
    """
    incident = db.query(Incident).filter(Incident.id == incident_id).first()
    
    if not incident:
        return {"error": "Incident not found"}
    
    events = db.query(IncidentEvent).filter(
        IncidentEvent.incident_id == incident_id
    ).order_by(IncidentEvent.timestamp).all()
    
    duration = None
    if incident.ended_at:
        duration = (incident.ended_at - incident.started_at).total_seconds()
    
    timeline = []
    for event in events:
        elapsed = (event.timestamp - incident.started_at).total_seconds()
        timeline.append({
            "time": event.timestamp.isoformat(),
            "elapsed_seconds": int(elapsed),
            "step": event.step,
            "metadata": event.event_metadata
        })
    
    return {
        "incident_id": incident.id,
        "type": incident.type,
        "severity": incident.severity,
        "status": incident.status,
        "started_at": incident.started_at.isoformat(),
        "ended_at": incident.ended_at.isoformat() if incident.ended_at else None,
        "duration_seconds": int(duration) if duration else None,
        "location": {
            "lat": incident.lat,
            "lng": incident.lng
        },
        "timeline": timeline,
        "total_steps": len(timeline)
    }

def export_to_text(summary: Dict[str, Any]) -> str:
    """
    Export summary as plain text for sharing
    """
    lines = [
        "=" * 50,
        "EMERGENCY INCIDENT SUMMARY",
        "=" * 50,
        f"Incident ID: {summary['incident_id']}",
        f"Type: {summary['type'].upper()}",
        f"Severity: {summary['severity'].upper()}",
        f"Status: {summary['status']}",
        "",
        f"Started: {summary['started_at']}",
        f"Ended: {summary['ended_at'] or 'In progress'}",
        f"Duration: {summary['duration_seconds']}s" if summary['duration_seconds'] else "Ongoing",
        "",
        f"Location: {summary['location']['lat']}, {summary['location']['lng']}",
        "",
        "TIMELINE:",
        "-" * 50
    ]
    
    for event in summary['timeline']:
        elapsed_min = event['elapsed_seconds'] // 60
        elapsed_sec = event['elapsed_seconds'] % 60
        lines.append(f"[+{elapsed_min:02d}:{elapsed_sec:02d}] {event['step']}")
        if event.get('metadata'):
            lines.append(f"         Details: {event['metadata']}")
    
    lines.extend([
        "-" * 50,
        f"Total steps completed: {summary['total_steps']}",
        "",
        "This summary is for informational purposes only.",
        "Please provide to emergency medical services.",
        "=" * 50
    ])
    
    return "\n".join(lines)
