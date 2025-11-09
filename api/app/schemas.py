from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    name: str
    phone: str
    locale: str = "en"


class UserCreate(UserBase):
    auth0_sub: str


class User(UserBase):
    id: int
    auth0_sub: str
    consent_location: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Contact schemas
class ContactBase(BaseModel):
    name: str
    phone: str
    lat: float
    lng: float
    radius_m: int = 500


class ContactCreate(ContactBase):
    pass


class Contact(ContactBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Incident schemas
class IncidentCreate(BaseModel):
    lat: float
    lng: float
    type: Optional[str] = None
    severity: Optional[str] = None


class Incident(BaseModel):
    id: int
    user_id: int
    lat: float
    lng: float
    type: Optional[str]
    severity: Optional[str]
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    incident_metadata: Optional[Dict[str, Any]] = None

    
    class Config:
        from_attributes = True


# Triage schemas
class TriageInput(BaseModel):
    text: str
    locale: str = "en"
    age_group: Optional[str] = None  # adult/child/elderly
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class StepDetail(BaseModel):
    title: str
    detail: str
    timer_s: Optional[int] = None
    cadence_bpm: Optional[int] = None
    critical: Optional[bool] = None


class TriageResult(BaseModel):
    type: str
    severity: str
    confidence: Optional[float] = None
    requires_sos: Optional[bool] = None
    requires_helpers: Optional[bool] = None
    sos_number: Optional[str] = None
    steps: List[StepDetail] = []  # Can be empty if needs clarification
    bring: List[str] = []
    helper_instructions: Optional[str] = None
    symptoms: Optional[List[str]] = None
    contraindications: Optional[List[str]] = None
    sources: Optional[List[str]] = None
    timestamp: Optional[str] = None
    # Clarification fields (when confidence is low)
    clarifying_questions: Optional[List[str]] = None
    possible_emergencies: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None

    # Allow extra fields from hybrid RAG
    class Config:
        extra = "allow"


# Alert schemas
class AlertInput(BaseModel):
    incident_id: int
    lat: float
    lng: float
    message: str
    radius_m: int = 500


class AlertResult(BaseModel):
    ok: bool
    count: int
    contacts_notified: List[str]


# Route schemas
class RouteInput(BaseModel):
    lat: float
    lng: float


class RouteResult(BaseModel):
    hospital_name: str
    hospital_address: str
    distance_km: float
    eta_minutes: int
    directions_url: str
