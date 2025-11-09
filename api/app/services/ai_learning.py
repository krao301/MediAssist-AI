"""
AI Learning & Feedback System
- Stores AI predictions vs actual outcomes
- Learns from user feedback
- Continuously improves over time
- Memory of past incidents
"""
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from ..models import Incident
from ..database import get_db
import json


class AIMemory:
    """
    Memory system for the AI to learn from past incidents
    Stores successful classifications and user feedback
    """
    
    def __init__(self):
        self.learning_data = []
        self.accuracy_stats = {
            "total_classifications": 0,
            "correct_classifications": 0,
            "false_positives_critical": 0,
            "missed_critical": 0,
            "user_corrections": []
        }
    
    def record_prediction(
        self,
        db: Session,
        incident_id: int,
        user_input: str,
        predicted_type: str,
        predicted_severity: str,
        confidence: float,
        sources_used: List[str],
        vector_match: Optional[Dict] = None,
        graph_match: Optional[Dict] = None,
        llm_match: Optional[Dict] = None
    ) -> None:
        """
        Record an AI prediction for future learning
        
        This creates a 'memory' of what the AI predicted
        Later we can compare it to what actually happened
        """
        
        from ..models import AIPrediction
        
        prediction = AIPrediction(
            incident_id=incident_id,
            user_input=user_input,
            predicted_type=predicted_type,
            predicted_severity=predicted_severity,
            confidence=confidence,
            sources_used=json.dumps(sources_used),
            vector_match=json.dumps(vector_match) if vector_match else None,
            graph_match=json.dumps(graph_match) if graph_match else None,
            llm_match=json.dumps(llm_match) if llm_match else None,
            prediction_timestamp=datetime.now()
        )
        
        db.add(prediction)
        db.commit()
        
        print(f"💾 AI prediction recorded: {predicted_type} ({confidence:.2%} confidence)")
    
    def record_feedback(
        self,
        db: Session,
        incident_id: int,
        was_correct: bool,
        actual_type: Optional[str] = None,
        actual_severity: Optional[str] = None,
        user_notes: Optional[str] = None,
        verified_by: Optional[str] = None  # EMT, doctor, user
    ) -> None:
        """
        Record feedback on whether AI was correct
        
        This is how the AI learns:
        - User/EMT says "this was actually a heart attack, not panic attack"
        - AI learns from the correction
        - Next time, it will be smarter
        """
        
        from ..models import AIPrediction, IncidentFeedback
        
        # Get the prediction
        prediction = db.query(AIPrediction).filter(
            AIPrediction.incident_id == incident_id
        ).first()
        
        if not prediction:
            print(f"⚠️  No prediction found for incident {incident_id}")
            return
        
        # Create feedback entry
        feedback = IncidentFeedback(
            incident_id=incident_id,
            prediction_id=prediction.id,
            was_correct=was_correct,
            actual_type=actual_type or prediction.predicted_type,
            actual_severity=actual_severity or prediction.predicted_severity,
            user_notes=user_notes,
            verified_by=verified_by or "user",
            feedback_timestamp=datetime.now()
        )
        
        db.add(feedback)
        db.commit()
        
        # Update accuracy stats
        self.accuracy_stats["total_classifications"] += 1
        if was_correct:
            self.accuracy_stats["correct_classifications"] += 1
        else:
            self.accuracy_stats["user_corrections"].append({
                "predicted": prediction.predicted_type,
                "actual": actual_type,
                "user_input": prediction.user_input
            })
        
        accuracy_pct = (
            self.accuracy_stats["correct_classifications"] / 
            self.accuracy_stats["total_classifications"] * 100
        )
        
        print(f"📊 Feedback recorded. Current accuracy: {accuracy_pct:.1f}%")
        
        # If incorrect, add to retraining queue
        if not was_correct and actual_type:
            self._add_to_retraining_queue(
                db=db,
                user_input=prediction.user_input,
                correct_type=actual_type,
                correct_severity=actual_severity or prediction.predicted_severity,
                incident_id=incident_id
            )
    
    def _add_to_retraining_queue(
        self,
        db: Session,
        user_input: str,
        correct_type: str,
        correct_severity: str,
        incident_id: int
    ) -> None:
        """
        Add corrected example to retraining queue
        These will be used to retrain the vector DB
        """
        
        from ..models import RetrainingData
        
        retraining_entry = RetrainingData(
            user_input=user_input,
            correct_type=correct_type,
            correct_severity=correct_severity,
            incident_id=incident_id,
            added_timestamp=datetime.now(),
            used_for_training=False
        )
        
        db.add(retraining_entry)
        db.commit()
        
        print(f"🎓 Added to retraining queue: {correct_type}")
    
    def get_learning_candidates(
        self,
        db: Session,
        min_confidence: float = 0.8,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Get high-quality incidents to add to training data
        
        Only include:
        - High confidence predictions (>80%)
        - Verified as correct by user/EMT
        - Not already used for training
        """
        
        from ..models import AIPrediction, IncidentFeedback, RetrainingData
        
        # Get all verified correct predictions
        query = db.query(
            AIPrediction, IncidentFeedback
        ).join(
            IncidentFeedback,
            AIPrediction.id == IncidentFeedback.prediction_id
        ).filter(
            IncidentFeedback.was_correct == True,
            AIPrediction.confidence >= min_confidence
        )
        
        # Exclude already used for training
        used_ids = db.query(RetrainingData.incident_id).filter(
            RetrainingData.used_for_training == True
        ).all()
        used_ids = [id[0] for id in used_ids]
        
        if used_ids:
            query = query.filter(
                AIPrediction.incident_id.notin_(used_ids)
            )
        
        results = query.limit(limit).all()
        
        learning_data = []
        for prediction, feedback in results:
            learning_data.append({
                "user_input": prediction.user_input,
                "emergency_type": prediction.predicted_type,
                "severity": prediction.predicted_severity,
                "confidence": prediction.confidence,
                "verified_by": feedback.verified_by,
                "incident_id": prediction.incident_id
            })
        
        return learning_data
    
    def retrain_vector_db(
        self,
        db: Session,
        vector_db
    ) -> Dict[str, Any]:
        """
        Retrain vector database with new learned examples
        
        This is the core of continuous learning:
        - Take all verified correct predictions
        - Add them to vector DB as training examples
        - AI gets smarter over time
        """
        
        learning_data = self.get_learning_candidates(db)
        
        if not learning_data:
            return {
                "success": True,
                "message": "No new learning data available",
                "examples_added": 0
            }
        
        added_count = 0
        for example in learning_data:
            try:
                # Add to vector DB
                vector_db.add_document(
                    text=example["user_input"],
                    emergency_type=example["emergency_type"],
                    metadata={
                        "severity": example["severity"],
                        "verified": True,
                        "source": "real_incident",
                        "confidence": example["confidence"]
                    }
                )
                
                # Mark as used for training
                from ..models import RetrainingData
                retraining_entry = RetrainingData(
                    user_input=example["user_input"],
                    correct_type=example["emergency_type"],
                    correct_severity=example["severity"],
                    incident_id=example["incident_id"],
                    added_timestamp=datetime.now(),
                    used_for_training=True
                )
                db.add(retraining_entry)
                
                added_count += 1
                
            except Exception as e:
                print(f"⚠️  Error adding example to vector DB: {e}")
        
        db.commit()
        
        print(f"🎓 Retraining complete: Added {added_count} verified examples to vector DB")
        
        return {
            "success": True,
            "message": f"Successfully added {added_count} examples",
            "examples_added": added_count,
            "total_available": len(learning_data)
        }
    
    def get_accuracy_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get AI performance statistics
        
        Shows:
        - Overall accuracy
        - Accuracy by emergency type
        - Common mistakes
        - Improvement over time
        """
        
        from ..models import AIPrediction, IncidentFeedback
        from sqlalchemy import func
        
        # Overall stats
        total_predictions = db.query(AIPrediction).count()
        
        total_with_feedback = db.query(IncidentFeedback).count()
        
        correct_predictions = db.query(IncidentFeedback).filter(
            IncidentFeedback.was_correct == True
        ).count()
        
        overall_accuracy = (
            correct_predictions / total_with_feedback * 100 
            if total_with_feedback > 0 else 0
        )
        
        # Accuracy by emergency type
        from sqlalchemy import Integer as IntegerType
        type_accuracy = db.query(
            AIPrediction.predicted_type,
            func.count(IncidentFeedback.id).label("total"),
            func.sum(func.cast(IncidentFeedback.was_correct, IntegerType)).label("correct")
        ).join(
            IncidentFeedback,
            AIPrediction.id == IncidentFeedback.prediction_id
        ).group_by(
            AIPrediction.predicted_type
        ).all()
        
        type_stats = {}
        for pred_type, total, correct in type_accuracy:
            type_stats[pred_type] = {
                "total": total,
                "correct": correct or 0,
                "accuracy": (correct or 0) / total * 100 if total > 0 else 0
            }
        
        # Common mistakes (most frequently corrected)
        common_mistakes = db.query(
            AIPrediction.predicted_type,
            IncidentFeedback.actual_type,
            func.count(IncidentFeedback.id).label("count")
        ).join(
            IncidentFeedback,
            AIPrediction.id == IncidentFeedback.prediction_id
        ).filter(
            IncidentFeedback.was_correct == False
        ).group_by(
            AIPrediction.predicted_type,
            IncidentFeedback.actual_type
        ).order_by(
            func.count(IncidentFeedback.id).desc()
        ).limit(10).all()
        
        mistakes = [
            {
                "predicted": pred,
                "actual": actual,
                "count": count
            }
            for pred, actual, count in common_mistakes
        ]
        
        # Improvement over time (last 7 days vs previous 7 days)
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        two_weeks_ago = today - timedelta(days=14)
        
        recent_accuracy = db.query(IncidentFeedback).filter(
            IncidentFeedback.feedback_timestamp >= week_ago,
            IncidentFeedback.was_correct == True
        ).count()
        
        recent_total = db.query(IncidentFeedback).filter(
            IncidentFeedback.feedback_timestamp >= week_ago
        ).count()
        
        previous_accuracy = db.query(IncidentFeedback).filter(
            IncidentFeedback.feedback_timestamp >= two_weeks_ago,
            IncidentFeedback.feedback_timestamp < week_ago,
            IncidentFeedback.was_correct == True
        ).count()
        
        previous_total = db.query(IncidentFeedback).filter(
            IncidentFeedback.feedback_timestamp >= two_weeks_ago,
            IncidentFeedback.feedback_timestamp < week_ago
        ).count()
        
        recent_pct = recent_accuracy / recent_total * 100 if recent_total > 0 else 0
        previous_pct = previous_accuracy / previous_total * 100 if previous_total > 0 else 0
        improvement = recent_pct - previous_pct
        
        return {
            "overall_accuracy": round(overall_accuracy, 2),
            "total_predictions": total_predictions,
            "predictions_with_feedback": total_with_feedback,
            "correct_predictions": correct_predictions,
            "accuracy_by_type": type_stats,
            "common_mistakes": mistakes,
            "recent_improvement": {
                "last_7_days_accuracy": round(recent_pct, 2),
                "previous_7_days_accuracy": round(previous_pct, 2),
                "improvement": round(improvement, 2),
                "trend": "improving" if improvement > 0 else "declining" if improvement < 0 else "stable"
            },
            "feedback_coverage": round(total_with_feedback / total_predictions * 100, 2) if total_predictions > 0 else 0
        }
    
    def get_similar_past_cases(
        self,
        db: Session,
        user_input: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find similar past incidents with known outcomes
        
        This gives the AI 'memory' - it can reference past cases:
        "This is similar to incident #123 which was a heart attack"
        """
        
        from ..models import AIPrediction, IncidentFeedback
        
        # For now, simple text matching
        # TODO: Use vector similarity search
        
        keywords = user_input.lower().split()
        
        similar_cases = []
        
        # Get all verified incidents
        verified = db.query(
            AIPrediction, IncidentFeedback
        ).join(
            IncidentFeedback,
            AIPrediction.id == IncidentFeedback.prediction_id
        ).filter(
            IncidentFeedback.was_correct == True
        ).all()
        
        for prediction, feedback in verified:
            # Calculate similarity (simple keyword matching)
            pred_text = prediction.user_input.lower()
            matches = sum(1 for word in keywords if word in pred_text)
            similarity = matches / len(keywords) if keywords else 0
            
            if similarity > 0.3:  # At least 30% keyword overlap
                similar_cases.append({
                    "incident_id": prediction.incident_id,
                    "user_input": prediction.user_input,
                    "emergency_type": feedback.actual_type,
                    "severity": feedback.actual_severity,
                    "similarity": similarity,
                    "verified_by": feedback.verified_by
                })
        
        # Sort by similarity
        similar_cases.sort(key=lambda x: x["similarity"], reverse=True)
        
        return similar_cases[:limit]


# Global AI Memory instance
ai_memory = AIMemory()
