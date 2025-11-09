"""
Nearby Helper Notification System
- Find people near emergency location
- Send notifications via free services (SMS/Push)
- Provide first-aid guidance to helpers
"""

import os
import requests
from typing import List, Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session
from ..models import Contact
from .geo import haversine_distance
from .notify import send_sms_alert
import json

# Free notification services
# We'll use Twilio (you already have it) for SMS
# For push notifications, we can use Firebase Cloud Messaging (FCM) - free tier

class NearbyHelperService:
    """Service to find and notify nearby helpers"""

    def __init__(self, db: Session):
        self.db = db
        self.search_radius_meters = 500  # Default 500m radius

    def find_nearby_contacts(
        self,
        user_id: int,
        emergency_lat: float,
        emergency_lng: float,
        radius_m: int = None
    ) -> List[Dict[str, Any]]:
        """
        Find all contacts within radius of emergency location

        Args:
            user_id: User's ID
            emergency_lat: Emergency latitude
            emergency_lng: Emergency longitude
            radius_m: Search radius in meters (default: 500m)

        Returns:
            List of contacts within radius with distance
        """

        radius = radius_m or self.search_radius_meters

        # Get all user's contacts from database
        contacts = self.db.query(Contact).filter(Contact.user_id == user_id).all()

        nearby_contacts = []

        for contact in contacts:
            if contact.lat and contact.lng:
                # Calculate distance using Haversine formula
                distance = haversine_distance(
                    emergency_lat, emergency_lng,
                    contact.lat, contact.lng
                )

                # Check if within radius
                if distance <= radius:
                    nearby_contacts.append({
                        "id": contact.id,
                        "name": contact.name,
                        "phone": contact.phone,
                        "distance_meters": round(distance, 2),
                        "lat": contact.lat,
                        "lng": contact.lng
                    })

        # Sort by distance (closest first)
        nearby_contacts.sort(key=lambda x: x["distance_meters"])

        return nearby_contacts

    def notify_nearby_helpers(
        self,
        nearby_contacts: List[Dict[str, Any]],
        emergency_info: Dict[str, Any],
        victim_name: str = "Someone"
    ) -> Dict[str, Any]:
        """
        Send notifications to nearby contacts with emergency details

        Args:
            nearby_contacts: List of nearby contacts
            emergency_info: Emergency classification info
            victim_name: Name of person in emergency

        Returns:
            Notification results
        """

        if not nearby_contacts:
            return {
                "success": False,
                "message": "No nearby contacts found",
                "notified": 0
            }

        emergency_type = emergency_info.get("type", "unknown emergency")
        severity = emergency_info.get("severity", "UNKNOWN")
        location_lat = emergency_info.get("latitude")
        location_lng = emergency_info.get("longitude")

        # Prepare emergency message for helpers
        helper_instructions = emergency_info.get("helper_instructions", "")

        notifications_sent = []
        failed_notifications = []

        for contact in nearby_contacts[:5]:  # Notify up to 5 closest helpers
            distance = contact["distance_meters"]

            # Create urgent SMS message
            message = self._create_helper_notification_message(
                victim_name=victim_name,
                emergency_type=emergency_type,
                severity=severity,
                distance=distance,
                location_lat=location_lat,
                location_lng=location_lng,
                helper_instructions=helper_instructions
            )

            # Send SMS via Twilio
            try:
                result = send_sms_alert(
                    to_number=contact["phone"],
                    message=message
                )

                if result.get("success"):
                    notifications_sent.append({
                        "contact_name": contact["name"],
                        "contact_phone": contact["phone"],
                        "distance_meters": distance,
                        "message_sid": result.get("message_sid")
                    })
                else:
                    failed_notifications.append({
                        "contact_name": contact["name"],
                        "error": result.get("error")
                    })

            except Exception as e:
                failed_notifications.append({
                    "contact_name": contact["name"],
                    "error": str(e)
                })

        return {
            "success": len(notifications_sent) > 0,
            "notified": len(notifications_sent),
            "failed": len(failed_notifications),
            "notifications": notifications_sent,
            "failures": failed_notifications
        }

    def _create_helper_notification_message(
        self,
        victim_name: str,
        emergency_type: str,
        severity: str,
        distance: float,
        location_lat: float,
        location_lng: float,
        helper_instructions: str
    ) -> str:
        """Create urgent notification message for nearby helpers"""

        # Create Google Maps link for navigation
        maps_link = f"https://maps.google.com/?q={location_lat},{location_lng}"

        message = f"""🚨 EMERGENCY ALERT - {severity} 🚨

{victim_name} needs IMMEDIATE HELP!

Emergency Type: {emergency_type.upper().replace('_', ' ')}
Distance: {distance:.0f} meters from you

WHAT TO DO:
{helper_instructions}

Location: {maps_link}

911 has been called. You are the nearest person who can help while waiting for EMS.

Time is critical - please respond if you can help!

-MediAssist AI Emergency System"""

        return message

    def send_first_aid_guidance(
        self,
        helper_phone: str,
        emergency_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Send detailed first-aid steps to helper who responded

        Args:
            helper_phone: Phone number of helper
            emergency_info: Full emergency classification with steps

        Returns:
            SMS send result
        """

        steps = emergency_info.get("steps", [])
        contraindications = emergency_info.get("contraindications", [])

        # Create step-by-step guidance
        message = "FIRST AID STEPS:\n\n"

        for i, step in enumerate(steps[:3], 1):  # First 3 critical steps
            title = step.get("title", "")
            detail = step.get("detail", "")
            message += f"{i}. {title}\n{detail}\n\n"

        if contraindications:
            message += "⚠️ DO NOT:\n"
            for warning in contraindications[:2]:
                message += f"- {warning}\n"

        message += "\nHelp is on the way. You're doing great!"

        return send_sms_alert(helper_phone, message)


def notify_emergency_services(
    emergency_info: Dict[str, Any],
    location: Dict[str, float],
    victim_info: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Notify emergency services (911 / POC: 7166170427)

    Args:
        emergency_info: Emergency classification
        location: {"lat": float, "lng": float}
        victim_info: {"name": str, "age": str, "phone": str}

    Returns:
        Call/SMS result
    """

    sos_number = emergency_info.get("sos_number", "7166170427")
    emergency_type = emergency_info.get("type", "unknown")
    severity = emergency_info.get("severity", "UNKNOWN")

    # Create emergency message
    message = f"""🚨 EMERGENCY - {severity}

Type: {emergency_type.upper().replace('_', ' ')}

Victim: {victim_info.get('name', 'Unknown')}
Age: {victim_info.get('age', 'Unknown')}
Contact: {victim_info.get('phone', 'Unknown')}

Location:
Lat: {location.get('lat')}
Lng: {location.get('lng')}
Maps: https://maps.google.com/?q={location.get('lat')},{location.get('lng')}

Reported by MediAssist AI at {emergency_info.get('timestamp', 'Unknown time')}

IMMEDIATE RESPONSE REQUIRED"""

    try:
        # Send SMS to emergency number (POC)
        result = send_sms_alert(sos_number, message)

        # In production, this would also trigger voice call via Twilio
        # For POC, SMS is sufficient

        return {
            "success": result.get("success", False),
            "sos_number": sos_number,
            "message_sid": result.get("message_sid"),
            "timestamp": emergency_info.get("timestamp")
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "sos_number": sos_number
        }


def find_public_helpers_nearby(
    latitude: float,
    longitude: float,
    radius_km: float = 0.5
) -> List[Dict[str, Any]]:
    """
    Find public places or people who might help (police stations, fire stations, hospitals)
    Uses OpenStreetMap Overpass API (FREE)

    Args:
        latitude: Emergency location latitude
        longitude: Emergency location longitude
        radius_km: Search radius in kilometers

    Returns:
        List of nearby public emergency resources
    """

    # Overpass API query for emergency services
    # FREE and no API key required!
    overpass_url = "https://overpass-api.de/api/interpreter"

    # Query for hospitals, police, fire stations within radius
    query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:{radius_km * 1000},{latitude},{longitude});
      node["amenity"="police"](around:{radius_km * 1000},{latitude},{longitude});
      node["amenity"="fire_station"](around:{radius_km * 1000},{latitude},{longitude});
      node["amenity"="doctors"](around:{radius_km * 1000},{latitude},{longitude});
    );
    out body;
    """

    try:
        response = requests.post(
            overpass_url,
            data={"data": query},
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            elements = data.get("elements", [])

            public_helpers = []

            for element in elements:
                tags = element.get("tags", {})
                element_lat = element.get("lat")
                element_lng = element.get("lon")

                if element_lat and element_lng:
                    distance = haversine_distance(
                        latitude, longitude,
                        element_lat, element_lng
                    )

                    public_helpers.append({
                        "name": tags.get("name", f"{tags.get('amenity', 'Unknown')} facility"),
                        "type": tags.get("amenity", "unknown"),
                        "distance_meters": round(distance, 2),
                        "lat": element_lat,
                        "lng": element_lng,
                        "address": tags.get("addr:street", "Unknown address")
                    })

            # Sort by distance
            public_helpers.sort(key=lambda x: x["distance_meters"])

            return public_helpers[:5]  # Return 5 closest

    except Exception as e:
        print(f"Error finding public helpers: {e}")

    return []
