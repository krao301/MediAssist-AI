"""
Voice Call Routes - TwiML responses for Twilio
"""
from fastapi import APIRouter, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse
from sqlalchemy.orm import Session
from fastapi import Depends
from ..database import get_db
from ..models import Incident

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/emergency-call")
async def emergency_call_twiml(request: Request, db: Session = Depends(get_db)):
    """
    TwiML response for emergency SOS call
    This is what the person who answers will hear
    """
    # Get query parameters
    params = dict(request.query_params)
    incident_id = params.get("incident_id")
    emergency_type = params.get("type", "unknown").replace("_", " ")
    severity = params.get("severity", "UNKNOWN")
    
    # Create voice response
    response = VoiceResponse()
    
    # Emergency message
    response.say(
        f"Emergency alert from MediAssist AI. "
        f"This is a {severity} severity {emergency_type} emergency. "
        f"Incident ID {incident_id}. "
        f"Emergency medical assistance is required immediately. "
        f"Please respond to the location coordinates provided in the SMS.",
        voice='alice',
        language='en-US'
    )
    
    # Repeat the message
    response.pause(length=1)
    response.say(
        f"Repeating: {severity} {emergency_type} emergency. Incident {incident_id}. "
        f"Immediate assistance needed.",
        voice='alice',
        language='en-US'
    )
    
    return Response(content=str(response), media_type="application/xml")


@router.post("/contact-alert")
async def contact_alert_twiml(request: Request):
    """
    TwiML response for alerting nearby emergency contacts
    """
    params = dict(request.query_params)
    incident_id = params.get("incident_id")
    emergency_type = params.get("type", "unknown").replace("_", " ")
    contact_name = params.get("contact_name", "Emergency Contact")
    
    response = VoiceResponse()
    
    response.say(
        f"Hello {contact_name}. This is MediAssist AI emergency alert system. "
        f"Someone near you needs immediate help. "
        f"Emergency type: {emergency_type}. "
        f"Incident ID {incident_id}. "
        f"Check your phone for the exact location. "
        f"Please respond immediately if you can assist.",
        voice='alice',
        language='en-US'
    )
    
    # Offer option to confirm response
    gather = response.gather(num_digits=1, action=f'/voice/contact-confirm?incident_id={incident_id}', timeout=10)
    gather.say(
        "Press 1 if you can respond to this emergency. Press 2 if you cannot.",
        voice='alice',
        language='en-US'
    )
    
    # If no input, leave message
    response.say(
        "No response received. Please check your messages for emergency details.",
        voice='alice',
        language='en-US'
    )
    
    return Response(content=str(response), media_type="application/xml")


@router.post("/contact-confirm")
async def contact_confirm(request: Request):
    """
    Handle contact's response to emergency alert
    """
    form_data = await request.form()
    digits = form_data.get("Digits")
    params = dict(request.query_params)
    incident_id = params.get("incident_id")
    
    response = VoiceResponse()
    
    if digits == "1":
        response.say(
            "Thank you for confirming. Emergency location details have been sent to your phone. "
            "Please proceed safely to the location.",
            voice='alice',
            language='en-US'
        )
    elif digits == "2":
        response.say(
            "Understood. We will alert other nearby contacts. Thank you.",
            voice='alice',
            language='en-US'
        )
    else:
        response.say(
            "Invalid input. Please check your messages for emergency details.",
            voice='alice',
            language='en-US'
        )
    
    return Response(content=str(response), media_type="application/xml")


@router.post("/call-status")
async def call_status(request: Request):
    """
    Webhook to receive call status updates from Twilio
    """
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")
    
    print(f"📞 Call {call_sid}: {call_status}")
    
    # Log to database if needed
    # Update incident with call status
    
    return {"ok": True}
