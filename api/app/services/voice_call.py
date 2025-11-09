"""
Twilio Voice Call Service
Handles automated voice calls to emergency services and contacts
"""
import os
from twilio.rest import Client
from typing import Optional

# Initialize Twilio client
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def make_emergency_call(
    to_number: str,
    incident_id: int,
    emergency_type: str,
    severity: str,
    location: dict
) -> dict:
    """
    Make an automated voice call to emergency services or contact
    
    Args:
        to_number: Phone number to call (E.164 format)
        incident_id: ID of the incident
        emergency_type: Type of emergency (cardiac_arrest, choking, etc.)
        severity: CRITICAL, SEVERE, MODERATE, MILD
        location: {"lat": float, "lng": float}
    
    Returns:
        dict with call SID and status
    """
    
    # Check if Twilio is configured
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print("⚠️  Twilio not configured. Skipping voice call.")
        return {
            "success": False,
            "error": "Twilio credentials not configured",
            "call_sid": None
        }
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Create TwiML URL that Twilio will call to get voice instructions
        twiml_url = f"{BASE_URL}/voice/emergency-call?incident_id={incident_id}&type={emergency_type}&severity={severity}"
        
        # Make the call
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_FROM_NUMBER,
            url=twiml_url,
            method='POST',
            status_callback=f"{BASE_URL}/voice/call-status",
            status_callback_event=['initiated', 'ringing', 'answered', 'completed']
        )
        
        print(f"✅ Emergency call initiated to {to_number}")
        print(f"   Call SID: {call.sid}")
        print(f"   Status: {call.status}")
        
        return {
            "success": True,
            "call_sid": call.sid,
            "status": call.status,
            "to": to_number,
            "from": TWILIO_FROM_NUMBER
        }
        
    except Exception as e:
        print(f"❌ Failed to make emergency call: {e}")
        return {
            "success": False,
            "error": str(e),
            "call_sid": None
        }


def make_contact_alert_call(
    to_number: str,
    to_name: str,
    incident_id: int,
    emergency_type: str,
    location: dict
) -> dict:
    """
    Make a voice call to alert nearby emergency contact
    
    Args:
        to_number: Contact's phone number
        to_name: Contact's name
        incident_id: Incident ID
        emergency_type: Type of emergency
        location: Location dict with lat/lng
    
    Returns:
        dict with call result
    """
    
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print("⚠️  Twilio not configured. Skipping contact call.")
        return {"success": False, "error": "Twilio not configured"}
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # TwiML URL for contact alert
        twiml_url = f"{BASE_URL}/voice/contact-alert?incident_id={incident_id}&type={emergency_type}&contact_name={to_name}"
        
        call = client.calls.create(
            to=to_number,
            from_=TWILIO_FROM_NUMBER,
            url=twiml_url,
            method='POST'
        )
        
        print(f"✅ Alert call to {to_name} ({to_number}): {call.sid}")
        
        return {
            "success": True,
            "call_sid": call.sid,
            "contact": to_name
        }
        
    except Exception as e:
        print(f"❌ Failed to call {to_name}: {e}")
        return {
            "success": False,
            "error": str(e)
        }


def notify_hospital(
    hospital_phone: str,
    incident_id: int,
    emergency_type: str,
    severity: str,
    patient_location: dict,
    eta_minutes: int
) -> dict:
    """
    Notify hospital of incoming emergency patient
    
    Args:
        hospital_phone: Hospital emergency department phone number
        incident_id: Incident ID
        emergency_type: Type of emergency
        severity: Emergency severity level
        patient_location: {"lat": float, "lng": float}
        eta_minutes: Estimated time of arrival
    
    Returns:
        dict with notification status
    """
    
    # Check if Twilio is configured
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER]):
        print("⚠️  Twilio not configured. Hospital notification skipped.")
        return {
            "success": False,
            "error": "Twilio not configured"
        }
    
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Create TwiML URL for hospital notification
        twiml_url = (
            f"{BASE_URL}/voice/hospital-alert?"
            f"incident_id={incident_id}&"
            f"type={emergency_type}&"
            f"severity={severity}&"
            f"eta={eta_minutes}"
        )
        
        # Make automated call to hospital
        call = client.calls.create(
            to=hospital_phone,
            from_=TWILIO_FROM_NUMBER,
            url=twiml_url,
            method='POST',
            status_callback=f"{BASE_URL}/voice/call-status"
        )
        
        print(f"✅ Hospital notification sent: {call.sid}")
        
        return {
            "success": True,
            "call_sid": call.sid,
            "hospital_phone": hospital_phone
        }
        
    except Exception as e:
        print(f"❌ Failed to notify hospital: {e}")
        return {
            "success": False,
            "error": str(e)
        }
