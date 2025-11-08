from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from ..schemas import RouteInput, RouteResult
from ..deps.auth import demo_auth
from ..services.geo import find_nearest_hospital
from ..database import get_db
import os

router = APIRouter(prefix="/route", tags=["route"])

@router.post("", response_model=RouteResult)
def get_nearest_hospital(
    body: RouteInput,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Find nearest hospital/ER and provide directions
    """
    maps_api_key = os.getenv("MAPS_API_KEY", "")
    
    result = find_nearest_hospital(body.lat, body.lng, maps_api_key)
    
    return RouteResult(
        hospital_name=result["name"],
        hospital_address=result["address"],
        distance_km=result["distance_km"],
        eta_minutes=result["eta_minutes"],
        directions_url=result["directions_url"]
    )
