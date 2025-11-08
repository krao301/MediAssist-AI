from math import radians, cos, sin, asin, sqrt
from typing import List, Tuple
from sqlalchemy.orm import Session
from ..models import Contact

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in meters
    r = 6371000
    return c * r

def contacts_within_radius(
    db: Session,
    user_id: int,
    incident_lat: float,
    incident_lng: float,
    radius_m: int = 500
) -> List[Tuple[Contact, float]]:
    """
    Find all contacts within specified radius of incident location
    Returns list of (contact, distance_m) tuples sorted by distance
    """
    contacts = db.query(Contact).filter(Contact.user_id == user_id).all()
    
    nearby = []
    for contact in contacts:
        distance = haversine(incident_lng, incident_lat, contact.lng, contact.lat)
        if distance <= radius_m:
            nearby.append((contact, distance))
    
    # Sort by distance (closest first)
    nearby.sort(key=lambda x: x[1])
    return nearby

def find_nearest_hospital(lat: float, lng: float, maps_api_key: str) -> dict:
    """
    Use Google Maps Places API to find nearest hospital
    """
    import requests
    
    if not maps_api_key:
        # Fallback for demo
        return {
            "name": "Nearest Emergency Room",
            "address": "Use Google Maps to find nearest ER",
            "distance_km": 0,
            "eta_minutes": 0,
            "directions_url": f"https://www.google.com/maps/search/hospital/@{lat},{lng},15z"
        }
    
    try:
        # Places API Nearby Search
        url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        params = {
            "location": f"{lat},{lng}",
            "rankby": "distance",
            "type": "hospital",
            "keyword": "emergency",
            "key": maps_api_key
        }
        
        response = requests.get(url, params=params)
        data = response.json()
        
        if data.get("results"):
            place = data["results"][0]
            place_loc = place["geometry"]["location"]
            
            # Calculate distance
            distance_m = haversine(lng, lat, place_loc["lng"], place_loc["lat"])
            distance_km = distance_m / 1000
            
            # Estimate ETA (assuming 40 km/h average speed in emergency)
            eta_minutes = int((distance_km / 40) * 60)
            
            directions_url = f"https://www.google.com/maps/dir/?api=1&origin={lat},{lng}&destination={place_loc['lat']},{place_loc['lng']}&travelmode=driving"
            
            return {
                "name": place.get("name", "Hospital"),
                "address": place.get("vicinity", ""),
                "distance_km": round(distance_km, 2),
                "eta_minutes": max(1, eta_minutes),
                "directions_url": directions_url
            }
    except Exception as e:
        print(f"Maps API error: {e}")
    
    # Fallback
    return {
        "name": "Nearest Emergency Room",
        "address": "Search for nearest hospital",
        "distance_km": 0,
        "eta_minutes": 0,
        "directions_url": f"https://www.google.com/maps/search/hospital/@{lat},{lng},15z"
    }
