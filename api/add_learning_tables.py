"""
Database migration to add AI learning tables

Run this script to add the new tables for AI memory and learning:
- ai_predictions: Stores all AI predictions
- incident_feedback: Stores feedback on predictions
- retraining_data: Queue of examples for retraining

Usage:
    python add_learning_tables.py
"""
from app.database import engine
from app.models import Base, AIPrediction, IncidentFeedback, RetrainingData

def migrate():
    """Create learning tables"""
    print("Creating AI learning tables...")
    
    try:
        # Create only the new tables (won't affect existing tables)
        AIPrediction.__table__.create(engine, checkfirst=True)
        print("✅ Created table: ai_predictions")
        
        IncidentFeedback.__table__.create(engine, checkfirst=True)
        print("✅ Created table: incident_feedback")
        
        RetrainingData.__table__.create(engine, checkfirst=True)
        print("✅ Created table: retraining_data")
        
        print("\n🎉 Migration complete! AI learning system is ready.")
        print("\nNew features available:")
        print("  - POST /learning/feedback - Submit feedback on AI predictions")
        print("  - POST /learning/retrain - Trigger AI retraining")
        print("  - GET /learning/stats - View AI performance statistics")
        print("  - GET /learning/similar-cases - Find similar past incidents")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise

if __name__ == "__main__":
    migrate()
