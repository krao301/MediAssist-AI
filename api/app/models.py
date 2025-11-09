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
    incident_metadata = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="incidents")
    events = relationship("IncidentEvent", back_populates="incident")

class IncidentEvent(Base):
    __tablename__ = "incident_events"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    step = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    event_metadata = Column(JSON, nullable=True)
    
    incident = relationship("Incident", back_populates="events")


class AIPrediction(Base):
    """
    Stores AI predictions for learning and memory
    Every time AI classifies an emergency, we record it here
    """
    __tablename__ = "ai_predictions"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    user_input = Column(Text)  # What the user said
    predicted_type = Column(String)  # What AI predicted (e.g., "cardiac_arrest")
    predicted_severity = Column(String)  # CRITICAL, SEVERE, etc.
    confidence = Column(Float)  # 0.0 to 1.0
    sources_used = Column(Text)  # JSON: ["vector_db", "knowledge_graph", "gemini_ai"]
    vector_match = Column(Text, nullable=True)  # JSON: vector DB match details
    graph_match = Column(Text, nullable=True)  # JSON: knowledge graph match details
    llm_match = Column(Text, nullable=True)  # JSON: Gemini match details
    prediction_timestamp = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident")
    feedback = relationship("IncidentFeedback", back_populates="prediction", uselist=False)


class IncidentFeedback(Base):
    """
    Stores feedback on AI predictions
    User/EMT says whether AI was correct or not
    This is how AI learns from mistakes
    """
    __tablename__ = "incident_feedback"
    id = Column(Integer, primary_key=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"))
    prediction_id = Column(Integer, ForeignKey("ai_predictions.id"))
    was_correct = Column(Boolean)  # Was the AI prediction correct?
    actual_type = Column(String, nullable=True)  # If wrong, what was it actually?
    actual_severity = Column(String, nullable=True)  # Actual severity level
    user_notes = Column(Text, nullable=True)  # User's explanation
    verified_by = Column(String, default="user")  # "user", "emt", "doctor"
    feedback_timestamp = Column(DateTime, default=datetime.utcnow)
    
    incident = relationship("Incident")
    prediction = relationship("AIPrediction", back_populates="feedback")


class RetrainingData(Base):
    """
    Queue of examples to use for retraining the AI
    When AI makes a mistake and user corrects it,
    we add it here so AI can learn from it
    """
    __tablename__ = "retraining_data"
    id = Column(Integer, primary_key=True)
    user_input = Column(Text)  # The input text
    correct_type = Column(String)  # Correct emergency type
    correct_severity = Column(String)  # Correct severity
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True)
    added_timestamp = Column(DateTime, default=datetime.utcnow)
    used_for_training = Column(Boolean, default=False)  # Has this been used yet?
    training_timestamp = Column(DateTime, nullable=True)  # When was it used for training?
    
    incident = relationship("Incident")
