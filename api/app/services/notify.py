import os
from typing import List, Tuple
from twilio.rest import Client
from ..models import Contact

def send_alerts(
    contacts: List[Tuple[Contact, float]],
    message: str,
    incident_lat: float,
    incident_lng: float,
    base_url: str = None
) -> List[str]:
    """
    Send SMS alerts to nearby contacts via Twilio
    Returns list of phone numbers successfully notified
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    base_url = base_url or os.getenv("BASE_URL", "http://localhost:8000")
    
    if not all([account_sid, auth_token, from_number]):
        print("Twilio credentials not configured, skipping SMS")
        return []
    
    try:
        client = Client(account_sid, auth_token)
        notified = []
        
        for contact, distance_m in contacts:
            distance_str = f"{int(distance_m)}m" if distance_m < 1000 else f"{distance_m/1000:.1f}km"
            
            # Create share link
            share_url = f"{base_url}/share?lat={incident_lat}&lng={incident_lng}"
            
            # Format message
            sms_body = (
                f"🚨 EMERGENCY ALERT 🚨\n"
                f"{contact.name}: {message}\n"
                f"Distance: {distance_str}\n"
                f"Location: {share_url}\n"
                f"Open link for directions and real-time updates."
            )
            
            try:
                message_obj = client.messages.create(
                    body=sms_body,
                    from_=from_number,
                    to=contact.phone
                )
                notified.append(contact.phone)
                print(f"SMS sent to {contact.name} ({contact.phone}): {message_obj.sid}")
            except Exception as e:
                print(f"Failed to send SMS to {contact.phone}: {e}")
        
        return notified
    
    except Exception as e:
        print(f"Twilio error: {e}")
        return []

def send_voice_call(phone: str, message: str) -> bool:
    """
    Make an automated voice call (optional stretch feature)
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        return False

    try:
        client = Client(account_sid, auth_token)

        # TwiML for voice message
        twiml = f"""
        <Response>
            <Say voice="alice">Emergency alert. {message}. Please check your messages for details.</Say>
        </Response>
        """

        call = client.calls.create(
            twiml=twiml,
            to=phone,
            from_=from_number
        )
        return True
    except Exception as e:
        print(f"Voice call error: {e}")
        return False

def send_sms_alert(to_number: str, message: str) -> dict:
    """
    Send SMS alert via Twilio

    Args:
        to_number: Recipient phone number
        message: SMS message content

    Returns:
        dict with success status and message_sid
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    from_number = os.getenv("TWILIO_FROM_NUMBER")

    if not all([account_sid, auth_token, from_number]):
        return {
            "success": False,
            "error": "Twilio credentials not configured"
        }

    try:
        client = Client(account_sid, auth_token)

        message_obj = client.messages.create(
            body=message,
            from_=from_number,
            to=to_number
        )

        return {
            "success": True,
            "message_sid": message_obj.sid,
            "to": to_number
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "to": to_number
        }
