from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    auth0_sub = Column(String, unique=True, index=True)
    name = Column(String)
    phone = Column(String)
    locale = Column(String, default="en")
    consent_location = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    contacts = relationship("Contact", back_populates="user")
    incidents = relationship("Incident", back_populates="user")

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    phone = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    radius_m = Column(Integer, default=500)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="contacts")

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lat = Column(Float)
    lng = Column(Float)
    type = Column(String)  # e.g., "cardiac_arrest", "choking"
    severity = Column(String)  # "critical" | "urgent" | "mild"
    status = Column(String, default="ACTIVE")  # ACTIVE | RESOLVED | CANCELLED
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="incidents")
    events = relationship("IncidentEvent", back_populates="incident")

class IncidentEvent(Base):
    __tablename__ = "incident_events"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    step = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    metadata = Column(JSON, nullable=True)
    
    incident = relationship("Incident", back_populates="events")
