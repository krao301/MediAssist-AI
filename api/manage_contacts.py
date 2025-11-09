#!/usr/bin/env python3
"""
Manage emergency contacts in database

Usage:
    # List all contacts
    python manage_contacts.py list
    
    # Delete all contacts
    python manage_contacts.py clear
    
    # Add a contact
    python manage_contacts.py add "Contact Name" "+17166170427" 42.96 -78.73
    
    # Add contact within specific distance
    python manage_contacts.py add "Nearby Person" "+17166170427" 42.9605 -78.7305  # ~69m away
"""

import sys
import math
from app.database import SessionLocal
from app.models import Contact

def haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance between two GPS coordinates in meters"""
    R = 6371000  # Earth's radius in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)
    a = math.sin(delta_phi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def list_contacts(emergency_lat=42.96, emergency_lng=-78.73):
    """List all contacts with distances from emergency location"""
    db = SessionLocal()
    contacts = db.query(Contact).all()
    
    print(f"\n{'='*80}")
    print(f"Total contacts in database: {len(contacts)}")
    print(f"Emergency reference location: {emergency_lat}, {emergency_lng}")
    print(f"{'='*80}\n")
    
    if not contacts:
        print("❌ No contacts in database")
        db.close()
        return
    
    for c in contacts:
        print(f"ID: {c.id}")
        print(f"Name: {c.name}")
        print(f"Phone: {c.phone}")
        if c.lat and c.lng:
            distance = haversine_distance(emergency_lat, emergency_lng, c.lat, c.lng)
            within_500m = "✅ WITHIN 500m" if distance <= 500 else "❌ TOO FAR"
            print(f"Location: {c.lat}, {c.lng}")
            print(f"Distance from emergency: {distance:.1f}m {within_500m}")
        else:
            print(f"Location: ❌ NO GPS COORDINATES")
        print(f"User ID: {c.user_id}")
        print(f"Created: {c.created_at}")
        print("-" * 80)
    
    db.close()

def clear_contacts():
    """Delete all contacts from database"""
    db = SessionLocal()
    count = db.query(Contact).count()
    
    if count == 0:
        print("✅ No contacts to delete")
        db.close()
        return
    
    confirm = input(f"⚠️  DELETE all {count} contacts? Type 'yes' to confirm: ")
    if confirm.lower() != 'yes':
        print("❌ Cancelled")
        db.close()
        return
    
    db.query(Contact).delete()
    db.commit()
    print(f"✅ Deleted {count} contacts")
    db.close()

def add_contact(name, phone, lat, lng, user_id=1):
    """Add a new contact to database"""
    db = SessionLocal()
    
    # Validate coordinates
    try:
        lat = float(lat)
        lng = float(lng)
        if not (-90 <= lat <= 90 and -180 <= lng <= 180):
            raise ValueError("Invalid coordinates")
    except ValueError as e:
        print(f"❌ Invalid coordinates: {e}")
        db.close()
        return
    
    # Calculate distance from reference emergency location
    emergency_lat, emergency_lng = 42.96, -78.73
    distance = haversine_distance(emergency_lat, emergency_lng, lat, lng)
    
    # Create contact
    contact = Contact(
        user_id=user_id,
        name=name,
        phone=phone,
        lat=lat,
        lng=lng,
        radius_m=500,
        created_at=None  # Will auto-generate
    )
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    within_500m = "✅ WITHIN 500m" if distance <= 500 else "⚠️ TOO FAR (won't be alerted)"
    print(f"\n✅ Contact added successfully!")
    print(f"   ID: {contact.id}")
    print(f"   Name: {name}")
    print(f"   Phone: {phone}")
    print(f"   Location: {lat}, {lng}")
    print(f"   Distance from emergency: {distance:.1f}m {within_500m}")
    
    db.close()

def add_sample_contacts():
    """Add 3 sample contacts: 1 near, 2 far"""
    db = SessionLocal()
    
    # Clear existing
    db.query(Contact).delete()
    db.commit()
    
    contacts = [
        # Contact within 500m (100m away)
        Contact(
            user_id=1,
            name="Sarah Nearby",
            phone="+17166170427",
            lat=42.9609,  # ~100m north
            lng=-78.7300,
            radius_m=500
        ),
        # Contact far away (5km away)
        Contact(
            user_id=1,
            name="Mike Faraway",
            phone="+17166170427",
            lat=42.9150,  # ~5km south
            lng=-78.7300,
            radius_m=500
        ),
        # Contact very far (10km away)
        Contact(
            user_id=1,
            name="Jessica Distant",
            phone="+17166170427",
            lat=42.8700,  # ~10km south
            lng=-78.7300,
            radius_m=500
        ),
    ]
    
    for contact in contacts:
        db.add(contact)
    
    db.commit()
    
    print("\n✅ Added 3 sample contacts:")
    print("   1. Sarah Nearby (~100m) - WILL BE ALERTED ✅")
    print("   2. Mike Faraway (~5km) - TOO FAR ❌")
    print("   3. Jessica Distant (~10km) - TOO FAR ❌")
    print("\nOnly Sarah Nearby should be alerted (within 500m)")
    
    db.close()

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_contacts()
    
    elif command == "clear":
        clear_contacts()
    
    elif command == "add":
        if len(sys.argv) < 6:
            print("Usage: python manage_contacts.py add <name> <phone> <lat> <lng>")
            print('Example: python manage_contacts.py add "John Doe" "+17166170427" 42.9605 -78.7305')
            return
        name = sys.argv[2]
        phone = sys.argv[3]
        lat = sys.argv[4]
        lng = sys.argv[5]
        add_contact(name, phone, lat, lng)
    
    elif command == "sample":
        add_sample_contacts()
    
    else:
        print(f"Unknown command: {command}")
        print(__doc__)

if __name__ == "__main__":
    main()
