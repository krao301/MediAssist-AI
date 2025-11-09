from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas import TriageInput, TriageResult
from ..deps.auth import require_auth, demo_auth
from ..services.hybrid_rag import HybridRAGSystem
from ..services.notify import (
    make_emergency_call,
    notify_hospital,
    find_nearby_contacts,
    send_emergency_sms,
    send_emergency_email,
)
from ..services.geo import find_nearest_hospital
from ..services.instructions import (
    generate_first_aid_instructions,
    format_instructions_for_sms,
)
from ..services.ai_learning import ai_memory
from ..database import get_db
import os

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
    user: Dict[str, Any] = Depends(demo_auth),  # Change to require_auth for Auth0
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
    if hasattr(body, "latitude") and hasattr(body, "longitude"):
        if body.latitude and body.longitude:
            location = {"lat": body.latitude, "lng": body.longitude}

    # Classify using hybrid RAG
    result = rag.classify_emergency(
        user_input=body.text, age_group=body.age_group or "adult", location=location
    )

    emergency_type = result.get("type", "unknown")
    severity = result.get("severity", "UNKNOWN")

    # Demo phone numbers and emails for testing
    sos_phone = "+17166170427"  # For SOS calls and SMS (MUST have +1 prefix)
    sos_email = "sankinenihrithikesh@gmail.com"  # For SOS email
    hospital_phone = "+17169085212"  # For hospital calls and SMS (MUST have +1 prefix)
    hospital_email = "shritikesh8999@gmail.com"  # For hospital email
    responder_phone = (
        "+17166170427"  # For nearby people calls and SMS (MUST have +1 prefix)
    )
    responder_email = "sankinenihrithikesh@gmail.com"  # For nearby people email

    # CRITICAL FLOW: Auto-trigger complete emergency response
    if result.get("requires_sos"):
        print(f"🚨 CRITICAL EMERGENCY DETECTED: {emergency_type} ({severity})")
        print(f"   Initiating full emergency response...")

        # 1. CALL SOS CONTACT
        print(f"   📞 Calling SOS contact: {sos_phone}")
        background_tasks.add_task(
            make_emergency_call,
            to_number=sos_phone,
            incident_id=0,
            emergency_type=emergency_type,
            severity=severity,
            location=location or {},
        )

        # 2. SMS SOS CONTACT with situation details
        print(f"   💬 Sending SOS SMS to {sos_phone}")

        def send_sos_sms():
            try:
                result = send_emergency_sms(
                    to_number=sos_phone,
                    emergency_type=emergency_type,
                    severity=severity,
                    location=location or {},
                    instructions=None,
                )
                print(f"   ✅ SOS SMS sent: {result}")
            except Exception as e:
                print(f"   ❌ SOS SMS failed: {e}")

        background_tasks.add_task(send_sos_sms)

        # 2b. EMAIL SOS CONTACT (backup notification)
        print(f"   📧 Sending SOS Email to {sos_email}")

        def send_sos_email():
            try:
                result = send_emergency_email(
                    to_email=sos_email,
                    subject="EMERGENCY ALERT - Immediate Response Required",
                    emergency_type=emergency_type,
                    severity=severity,
                    location=location or {},
                    instructions=None,
                    incident_id=0,
                )
                print(f"   ✅ SOS Email sent: {result}")
            except Exception as e:
                print(f"   ❌ SOS Email failed: {e}")

        background_tasks.add_task(send_sos_email)

        # 3. NOTIFY NEAREST HOSPITAL
        if location:
            print(f"   🏥 Finding and notifying nearest hospital...")
            try:
                maps_api_key = os.getenv("MAPS_API_KEY")
                hospital = find_nearest_hospital(
                    lat=location["lat"], lng=location["lng"], maps_api_key=maps_api_key
                )

                if hospital:
                    hospital_name = hospital.get("name", "Nearest Hospital")
                    print(f"      Hospital: {hospital_name} (calling {hospital_phone})")

                    # Call hospital
                    background_tasks.add_task(
                        notify_hospital,
                        hospital_phone=hospital_phone,
                        incident_id=0,
                        emergency_type=emergency_type,
                        severity=severity,
                        patient_location=location,
                        eta_minutes=hospital.get("eta_minutes", 15),
                    )

                    # SMS hospital (already done in notify_hospital function)

                    # Email hospital (backup notification)
                    def send_hospital_email():
                        try:
                            eta = hospital.get("eta_minutes", 15)
                            result = send_emergency_email(
                                to_email=hospital_email,
                                subject=f"INCOMING PATIENT - ETA {eta} minutes",
                                emergency_type=emergency_type,
                                severity=severity,
                                location=location,
                                instructions=f"Patient ETA: {eta} minutes. Prepare emergency bay.",
                                incident_id=0,
                            )
                            print(f"      ✅ Hospital Email sent: {result}")
                        except Exception as e:
                            print(f"      ❌ Hospital Email failed: {e}")

                    background_tasks.add_task(send_hospital_email)
                else:
                    print(f"      ⚠️ No hospital found")
            except Exception as e:
                print(f"      ⚠️ Hospital notification error: {e}")

        # 4. FIND & ALERT NEARBY PEOPLE (within 500m)
        if location:
            print(f"   👥 Finding nearby people to alert...")

            # HARDCODED DEMO CONTACTS (bypasses database issues)
            # Using hardcoded contacts for reliable demo
            import math

            def calc_distance(lat1, lng1, lat2, lng2):
                """Calculate distance in meters"""
                R = 6371000
                phi1, phi2 = math.radians(lat1), math.radians(lat2)
                delta_phi = math.radians(lat2 - lat1)
                delta_lambda = math.radians(lng2 - lng1)
                a = (
                    math.sin(delta_phi / 2) ** 2
                    + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
                )
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                return R * c

            # Demo contacts with distances
            demo_contacts = [
                {
                    "name": "Sarah Nearby",
                    "phone": responder_phone,
                    "email": responder_email,
                    "lat": 42.9609,
                    "lng": -78.7300,
                },
                {
                    "name": "Mike Faraway",
                    "phone": responder_phone,
                    "email": responder_email,
                    "lat": 42.9150,
                    "lng": -78.7300,
                },
                {
                    "name": "Jessica Distant",
                    "phone": responder_phone,
                    "email": responder_email,
                    "lat": 42.8700,
                    "lng": -78.7300,
                },
            ]

            # Calculate distances and filter
            nearby_people = []
            for contact in demo_contacts:
                distance = calc_distance(
                    location["lat"], location["lng"], contact["lat"], contact["lng"]
                )
                print(f"      {contact['name']}: {distance:.1f}m away")
                if distance <= 500:
                    nearby_people.append(
                        {
                            "name": contact["name"],
                            "phone": contact["phone"],
                            "email": contact["email"],
                            "distance_meters": round(distance, 1),
                        }
                    )

            try:

                print(f"      Found {len(nearby_people)} people within 500m")

                # Generate stabilization instructions for responders
                first_aid = generate_first_aid_instructions(
                    emergency_type=emergency_type,
                    severity=severity,
                    user_description=body.text,
                    age_group=body.age_group,
                )

                instructions_text = format_instructions_for_sms(first_aid)

                for person in nearby_people[:5]:  # Limit to 5 closest people
                    print(
                        f"      Alerting: {person['name']} ({person['distance_meters']}m away) at {responder_phone}"
                    )

                    # CALL nearby person
                    def call_responder(name=person["name"]):
                        try:
                            make_emergency_call(
                                to_number=responder_phone,
                                incident_id=0,
                                emergency_type=emergency_type,
                                severity=severity,
                                location=location,
                            )
                            print(f"      ✅ Called {name}")
                        except Exception as e:
                            print(f"      ❌ Call to {name} failed: {e}")

                    background_tasks.add_task(call_responder)

                    # SMS with INSTRUCTIONS on what to do
                    def sms_responder(name=person["name"]):
                        try:
                            result = send_emergency_sms(
                                to_number=responder_phone,
                                emergency_type=emergency_type,
                                severity=severity,
                                location=location,
                                instructions=instructions_text,
                            )
                            print(f"      ✅ SMS sent to {name}: {result}")
                        except Exception as e:
                            print(f"      ❌ SMS to {name} failed: {e}")

                    background_tasks.add_task(sms_responder)

                    # EMAIL with detailed instructions (backup)
                    def email_responder(
                        name=person["name"], distance=person["distance_meters"]
                    ):
                        try:
                            result = send_emergency_email(
                                to_email=responder_email,
                                subject=f"HELP NEEDED - Medical Emergency {distance}m away",
                                emergency_type=emergency_type,
                                severity=severity,
                                location=location,
                                instructions=instructions_text,
                                incident_id=0,
                            )
                            print(f"      ✅ Email sent to {name}: {result}")
                        except Exception as e:
                            print(f"      ❌ Email to {name} failed: {e}")

                    background_tasks.add_task(email_responder)

            except Exception as e:
                print(f"      ⚠️ Error finding nearby people: {e}")

        print(f"   ✅ Emergency response initiated successfully")

    # MINOR FLOW: Just provide first aid instructions (no calls/alerts)
    else:
        print(f"ℹ️ MINOR EMERGENCY: {emergency_type} ({severity})")
        print(f"   Generating first aid instructions...")

        # Generate first aid instructions using LLM
        instructions = generate_first_aid_instructions(
            emergency_type=emergency_type,
            severity=severity,
            user_description=body.text,
            age_group=body.age_group,
        )

        # Add instructions to result
        result["first_aid_instructions"] = instructions

        print(f"   ✅ Instructions ready for display")

    # RECORD AI PREDICTION FOR LEARNING (Memory System)
    # Skip recording if no incident_id yet - will be recorded when incident is created
    # This prevents foreign key errors since triage can be called before incident creation

    return TriageResult(**result)


@router.post("/voice")
def triage_voice(
    audio_data: bytes,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth),
):
    """
    Triage from voice input (Whisper STT)
    Stretch feature - for now returns placeholder
    """
    # TODO: Implement Whisper STT on DigitalOcean Gradient
    # For MVP, use Web Speech API on frontend

    return {
        "message": "Voice triage not implemented yet. Use Web Speech API on frontend.",
        "suggestion": "Use /triage endpoint with text transcription from frontend",
    }
