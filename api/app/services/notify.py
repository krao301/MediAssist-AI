import os
from typing import List, Tuple, Dict, Any
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Say
from ..models import Contact
import math
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula
    
    Returns:
        Distance in meters
    """
    # Earth's radius in meters
    R = 6371000
    
    # Convert to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    
    # Haversine formula
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c


def find_nearby_contacts(
    incident_lat: float,
    incident_lng: float,
    db,
    radius_meters: int = 500,
    user_id: int = None
) -> List[Dict[str, Any]]:
    """
    Find emergency contacts within radius of incident location
    
    Args:
        incident_lat: Latitude of emergency
        incident_lng: Longitude of emergency
        db: Database session
        radius_meters: Search radius in meters (default 500m)
        user_id: Optional user_id to get specific user's contacts
    
    Returns:
        List of nearby contacts with distance info
    """
    print(f"      DEBUG: Querying database for contacts...")
    print(f"      DEBUG: DB session active: {db is not None}")
    
    # WORKAROUND: If db session returns empty, try creating fresh session
    # This fixes Neon pooler connection issues
    all_contacts = []
    
    try:
        # First try with provided session
        query = db.query(Contact).filter(
            Contact.lat.isnot(None),
            Contact.lng.isnot(None)
        )
        
        # Optionally filter by user (disabled for demo - find ALL contacts)
        # if user_id:
        #     query = query.filter(Contact.user_id == user_id)
        
        print(f"      DEBUG: Executing query with provided session...")
        all_contacts = query.all()
        print(f"      DEBUG: Query returned {len(all_contacts)} contacts")
        
        # If empty, try with fresh session (Neon pooler workaround)
        if len(all_contacts) == 0:
            print(f"      DEBUG: Retrying with fresh database session...")
            from ..database import SessionLocal
            fresh_db = SessionLocal()
            try:
                fresh_query = fresh_db.query(Contact).filter(
                    Contact.lat.isnot(None),
                    Contact.lng.isnot(None)
                )
                all_contacts = fresh_query.all()
                print(f"      DEBUG: Fresh session returned {len(all_contacts)} contacts")
            finally:
                fresh_db.close()
        
        print(f"      DEBUG: Found {len(all_contacts)} total contacts in database (user_id filter: {'ON' if user_id else 'OFF'})")
    except Exception as e:
        print(f"      DEBUG: Database query error: {e}")
        import traceback
        print(f"      DEBUG: Full traceback: {traceback.format_exc()}")
        return []
    
    # Calculate distances and filter by radius
    nearby = []
    for contact in all_contacts:
        distance = haversine_distance(
            incident_lat, incident_lng,
            contact.lat, contact.lng
        )
        print(f"      DEBUG: {contact.name} is {distance:.1f}m away (radius={radius_meters}m)")
        
        if distance <= radius_meters:
            nearby.append({
                "id": contact.id,
                "name": contact.name,
                "phone": contact.phone,
                "distance_meters": round(distance, 1),
                "lat": contact.lat,
                "lng": contact.lng
            })
    
    # Sort by distance (closest first)
    return sorted(nearby, key=lambda x: x["distance_meters"])


def send_emergency_sms(
    to_number: str,
    emergency_type: str,
    severity: str,
    location: Dict[str, float],
    instructions: str = None
) -> dict:
    """
    Send SMS with emergency details and location
    
    Args:
        to_number: Recipient phone number
        emergency_type: Type of emergency (e.g., "cardiac_arrest")
        severity: Severity level (e.g., "CRITICAL")
        location: Dict with lat, lng
        instructions: Optional first aid instructions for responders
    
    Returns:
        dict with success status
    """
    # Format emergency type for display
    emergency_display = emergency_type.replace("_", " ").title()
    
    # Build Google Maps link
    maps_link = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
    
    # Build message
    if instructions:
        # For nearby responders - include instructions
        message = (
            f"🚨 MEDICAL EMERGENCY\n"
            f"Type: {emergency_display}\n"
            f"Severity: {severity}\n"
            f"Location: {maps_link}\n\n"
            f"HELP NEEDED:\n{instructions}\n\n"
            f"Ambulance dispatched. Reply ETA if you can help."
        )
    else:
        # For SOS contacts/hospitals - just alert
        message = (
            f"🚨 EMERGENCY ALERT\n"
            f"Type: {emergency_display}\n"
            f"Severity: {severity}\n"
            f"Location: {maps_link}\n\n"
            f"Emergency services have been notified."
        )
    
    return send_sms_alert(to_number, message)


def send_emergency_email(
    to_email: str,
    subject: str,
    emergency_type: str,
    severity: str,
    location: Dict[str, float],
    instructions: str = None,
    incident_id: int = None
) -> dict:
    """
    Send emergency email notification via Gmail SMTP
    
    Args:
        to_email: Recipient email address
        subject: Email subject line
        emergency_type: Type of emergency (e.g., "cardiac_arrest")
        severity: Severity level (e.g., "CRITICAL")
        location: Dict with lat, lng
        instructions: Optional first aid instructions for responders
        incident_id: Optional incident ID
    
    Returns:
        dict with success status
    """
    gmail_address = os.getenv('GMAIL_ADDRESS')
    gmail_password = os.getenv('GMAIL_APP_PASSWORD')
    
    if not all([gmail_address, gmail_password]):
        print("⚠️ Gmail credentials not configured, skipping email")
        return {
            "success": False,
            "error": "Gmail credentials not configured"
        }
    
    try:
        # Format emergency type for display
        emergency_display = emergency_type.replace("_", " ").title()
        
        # Build Google Maps link
        maps_link = f"https://www.google.com/maps?q={location['lat']},{location['lng']}"
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"🚨 {subject}"
        msg['From'] = f"MediAssist Emergency <{gmail_address}>"
        msg['To'] = to_email
        
        # Build HTML content
        instructions_html = ""
        if instructions:
            # Split instructions into lines
            instruction_lines = instructions.split('\n')
            instructions_html = "<h3>First Aid Instructions:</h3><ul>"
            for line in instruction_lines:
                if line.strip():
                    instructions_html += f"<li>{line.strip()}</li>"
            instructions_html += "</ul>"
        
        incident_html = f"<p><strong>Incident ID:</strong> #{incident_id}</p>" if incident_id else ""
        
        html = f"""
        <html>
          <head>
            <style>
              body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
              .header {{ background-color: #dc2626; color: white; padding: 20px; text-align: center; }}
              .content {{ padding: 20px; }}
              .alert-box {{ background-color: #fef2f2; border-left: 4px solid #dc2626; padding: 15px; margin: 20px 0; }}
              .severity {{ color: #dc2626; font-weight: bold; font-size: 1.2em; }}
              .button {{ display: inline-block; background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }}
              .footer {{ color: #666; font-size: 12px; text-align: center; padding: 20px; border-top: 1px solid #ddd; margin-top: 30px; }}
              ul {{ background-color: #f9fafb; padding: 15px 15px 15px 35px; border-radius: 5px; }}
            </style>
          </head>
          <body>
            <div class="header">
              <h1>🚨 EMERGENCY ALERT</h1>
            </div>
            <div class="content">
              <div class="alert-box">
                <p><strong>Emergency Type:</strong> {emergency_display}</p>
                <p><strong>Severity:</strong> <span class="severity">{severity}</span></p>
                {incident_html}
                <p><strong>Location:</strong></p>
                <a href="{maps_link}" class="button">📍 View Location on Google Maps</a>
              </div>
              
              {instructions_html}
              
              <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; margin: 20px 0;">
                <p><strong>✅ Emergency Services Notified</strong></p>
                <p>Ambulance has been dispatched to the location. If you can assist, please respond immediately.</p>
              </div>
            </div>
            <div class="footer">
              <p>🏥 Sent by MediAssist AI Emergency Response System</p>
              <p>This is an automated emergency notification. Time: {emergency_display}</p>
            </div>
          </body>
        </html>
        """
        
        msg.attach(MIMEText(html, 'html'))
        
        # Send via Gmail SMTP
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_address, gmail_password)
            server.send_message(msg)
        
        print(f"✅ Email sent to {to_email}")
        return {
            "success": True,
            "method": "email",
            "to": to_email
        }
        
    except Exception as e:
        print(f"❌ Email failed to {to_email}: {e}")
        return {
            "success": False,
            "error": str(e),
            "to": to_email
        }


def make_emergency_call(
    to_number: str,
    incident_id: int,
    emergency_type: str,
    severity: str,
    location: Dict[str, float]
) -> dict:
    """
    Make automated voice call for emergency alert
    
    Args:
        to_number: Phone number to call
        incident_id: Incident ID
        emergency_type: Type of emergency
        severity: Severity level
        location: Dict with lat, lng
    
    Returns:
        dict with success status and call_sid
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
        
        # Format emergency type for voice
        emergency_display = emergency_type.replace("_", " ")
        
        # Create TwiML response
        response = VoiceResponse()
        response.say(
            f"Emergency alert. Medical emergency detected. "
            f"Type: {emergency_display}. "
            f"Severity: {severity}. "
            f"Check your messages for location and details. "
            f"This is incident number {incident_id}.",
            voice='alice',
            language='en-US'
        )

        call = client.calls.create(
            twiml=str(response),
            to=to_number,
            from_=from_number
        )

        print(f"✅ Emergency call initiated to {to_number}: {call.sid}")
        
        return {
            "success": True,
            "call_sid": call.sid,
            "to": to_number,
            "incident_id": incident_id
        }
    except Exception as e:
        print(f"❌ Failed to make emergency call: {e}")
        return {
            "success": False,
            "error": str(e),
            "to": to_number
        }


def notify_hospital(
    hospital_phone: str,
    incident_id: int,
    emergency_type: str,
    severity: str,
    patient_location: Dict[str, float],
    eta_minutes: int = 15
) -> dict:
    """
    Call hospital to alert them about incoming patient
    
    Args:
        hospital_phone: Hospital phone number
        incident_id: Incident ID
        emergency_type: Type of emergency
        severity: Severity level
        patient_location: Dict with lat, lng
        eta_minutes: Estimated time for ambulance arrival
    
    Returns:
        dict with success status
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
        
        # Format emergency for voice
        emergency_display = emergency_type.replace("_", " ")
        
        # Create TwiML for hospital
        response = VoiceResponse()
        response.say(
            f"Hospital alert. Incoming patient. "
            f"Emergency type: {emergency_display}. "
            f"Severity: {severity}. "
            f"Estimated time of arrival: {eta_minutes} minutes. "
            f"Incident number {incident_id}. "
            f"Check emergency dispatch system for details.",
            voice='alice',
            language='en-US'
        )

        call = client.calls.create(
            twiml=str(response),
            to=hospital_phone,
            from_=from_number
        )

        print(f"🏥 Hospital notified: {call.sid}")
        
        # Also send SMS with details
        maps_link = f"https://www.google.com/maps?q={patient_location['lat']},{patient_location['lng']}"
        sms_message = (
            f"🏥 INCOMING PATIENT\n"
            f"Type: {emergency_display}\n"
            f"Severity: {severity}\n"
            f"ETA: ~{eta_minutes} min\n"
            f"Location: {maps_link}\n"
            f"Incident #{incident_id}"
        )
        
        sms_result = send_sms_alert(hospital_phone, sms_message)
        if sms_result.get("success"):
            print(f"✅ Hospital SMS sent: {sms_result.get('message_sid')}")
        else:
            print(f"❌ Hospital SMS failed: {sms_result.get('error')}")
        
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
