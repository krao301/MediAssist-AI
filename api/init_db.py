#!/usr/bin/env python3
"""
Initialize database tables
"""
from dotenv import load_dotenv
from app.database import init_db, engine
from app.models import Base

# Load environment variables
load_dotenv()

def main():
    """Create all database tables"""
    print("=" * 60)
    print("Initializing MediAssist AI Database")
    print("=" * 60)
    print(f"\nDatabase URL: {engine.url}")
    print("\nCreating tables...")

    try:
        # Create all tables
        init_db()

        print("\n✓ Successfully created tables:")
        print("  - users")
        print("  - contacts")
        print("  - incidents")
        print("  - incident_events")

        print("\n" + "=" * 60)
        print("Database initialization complete!")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
