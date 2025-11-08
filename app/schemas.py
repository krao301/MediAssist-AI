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
    metadata: Optional[Dict[str, Any]]
    
    class Config:
        from_attributes = True

# Triage schemas
class TriageInput(BaseModel):
    text: str
    locale: str = "en"
    age_group: Optional[str] = None  # adult/child/infant

class StepDetail(BaseModel):
    title: str
    detail: str
    timer_s: Optional[int] = None
    cadence_bpm: Optional[int] = None

class TriageResult(BaseModel):
    type: str
    severity: str
    steps: List[StepDetail]
    bring: List[str] = []

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
