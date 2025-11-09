"""
Feedback & Learning API Routes
- Submit feedback on AI predictions
- Trigger retraining
- View AI performance stats
- Get similar past cases
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from pydantic import BaseModel
from ..database import get_db
from ..services.ai_learning import ai_memory
from ..deps.auth import demo_auth

router = APIRouter(prefix="/learning", tags=["learning"])


class FeedbackInput(BaseModel):
    incident_id: int
    was_correct: bool
    actual_type: Optional[str] = None
    actual_severity: Optional[str] = None
    user_notes: Optional[str] = None
    verified_by: Optional[str] = "user"


class RetrainRequest(BaseModel):
    min_confidence: float = 0.8
    max_examples: int = 100


@router.post("/feedback")
def submit_feedback(
    feedback: FeedbackInput,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Submit feedback on AI prediction
    
    Tell the AI if it was right or wrong
    If wrong, provide the correct classification
    
    Example:
    POST /learning/feedback
    {
        "incident_id": 123,
        "was_correct": false,
        "actual_type": "heart_attack",
        "actual_severity": "CRITICAL",
        "user_notes": "Patient had chest pain, not panic attack",
        "verified_by": "emt"
    }
    """
    
    try:
        ai_memory.record_feedback(
            db=db,
            incident_id=feedback.incident_id,
            was_correct=feedback.was_correct,
            actual_type=feedback.actual_type,
            actual_severity=feedback.actual_severity,
            user_notes=feedback.user_notes,
            verified_by=feedback.verified_by
        )
        
        return {
            "success": True,
            "message": "Feedback recorded successfully",
            "incident_id": feedback.incident_id,
            "learning": "AI will learn from this feedback" if not feedback.was_correct else "AI confidence boosted"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to record feedback: {str(e)}")


@router.post("/retrain")
def trigger_retraining(
    request: RetrainRequest,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Manually trigger AI retraining
    
    This adds all verified correct predictions to the vector database
    AI gets smarter by learning from real incidents
    
    Example:
    POST /learning/retrain
    {
        "min_confidence": 0.8,
        "max_examples": 100
    }
    """
    
    try:
        # Import vector DB from hybrid RAG system
        from ..services.hybrid_rag import HybridRAGSystem
        
        rag = HybridRAGSystem()
        
        result = ai_memory.retrain_vector_db(
            db=db,
            vector_db=rag.vector_db
        )
        
        return {
            "success": True,
            **result,
            "message": f"Retraining complete. Added {result['examples_added']} new examples to AI knowledge base."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retraining failed: {str(e)}")


@router.get("/stats")
def get_ai_stats(
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Get AI performance statistics
    
    Returns:
    - Overall accuracy
    - Accuracy by emergency type
    - Common mistakes
    - Improvement over time
    - Feedback coverage
    
    Example:
    GET /learning/stats
    """
    
    try:
        stats = ai_memory.get_accuracy_stats(db)
        
        return {
            "success": True,
            **stats,
            "summary": f"AI is {stats['overall_accuracy']:.1f}% accurate across {stats['total_predictions']} predictions"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@router.get("/similar-cases")
def get_similar_cases(
    user_input: str,
    limit: int = 5,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Find similar past incidents with known outcomes
    
    This gives AI 'memory' - it can reference past cases
    
    Example:
    GET /learning/similar-cases?user_input=chest pain&limit=5
    
    Returns past incidents similar to "chest pain" that were verified
    """
    
    try:
        similar = ai_memory.get_similar_past_cases(
            db=db,
            user_input=user_input,
            limit=limit
        )
        
        return {
            "success": True,
            "query": user_input,
            "similar_cases": similar,
            "count": len(similar),
            "message": f"Found {len(similar)} similar past cases" if similar else "No similar cases found"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to find similar cases: {str(e)}")


@router.get("/learning-queue")
def get_learning_queue(
    min_confidence: float = 0.8,
    limit: int = 50,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Get examples waiting to be used for retraining
    
    Shows high-quality verified incidents ready to teach the AI
    
    Example:
    GET /learning/learning-queue?min_confidence=0.8&limit=50
    """
    
    try:
        candidates = ai_memory.get_learning_candidates(
            db=db,
            min_confidence=min_confidence,
            limit=limit
        )
        
        return {
            "success": True,
            "candidates": candidates,
            "count": len(candidates),
            "message": f"{len(candidates)} high-quality examples ready for training",
            "action": "POST /learning/retrain to add these to AI knowledge base"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get learning queue: {str(e)}")


@router.get("/mistakes")
def get_common_mistakes(
    limit: int = 10,
    db: Session = Depends(get_db),
    user: Dict[str, Any] = Depends(demo_auth)
):
    """
    Get most common AI mistakes
    
    Shows what AI frequently gets wrong
    This helps prioritize training improvements
    
    Example:
    GET /learning/mistakes?limit=10
    """
    
    try:
        stats = ai_memory.get_accuracy_stats(db)
        mistakes = stats.get("common_mistakes", [])
        
        return {
            "success": True,
            "common_mistakes": mistakes[:limit],
            "count": len(mistakes),
            "message": "These are the emergency types AI most frequently confuses",
            "action": "Focus training on these areas"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get mistakes: {str(e)}")
