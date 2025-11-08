from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from ..models import Contact
from ..schemas import ContactCreate, Contact as ContactSchema
from ..deps.auth import demo_auth
from ..database import get_db

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.post("/", response_model=ContactSchema)
def create_contact(
    body: ContactCreate,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Add a new trusted contact
    """
    user_id = 1  # Demo - in production, look up by user['sub']
    
    contact = Contact(
        user_id=user_id,
        name=body.name,
        phone=body.phone,
        lat=body.lat,
        lng=body.lng,
        radius_m=body.radius_m
    )
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return contact

@router.get("/", response_model=List[ContactSchema])
def list_contacts(
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Get all contacts for current user
    """
    user_id = 1  # Demo
    
    contacts = db.query(Contact).filter(Contact.user_id == user_id).all()
    return contacts

@router.delete("/{contact_id}")
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Remove a contact
    """
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    
    db.delete(contact)
    db.commit()
    
    return {"ok": True, "deleted_id": contact_id}
