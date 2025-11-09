"""
Hybrid RAG System - Triple Layer Architecture
Combines:
1. Vector Database         # If still no age group, ask for clarification
        if not age_group:
            return {
                "type": "needs_age_clarification",
                "severity": Severity.MILD,  # Low severity since we need more info
                "confidence": 0.0,
                "requires_sos": False,
                "requires_helpers": False,
                "sos_number": None,
                "steps": [],
                "bring": [],
                "clarifying_questions": [
                    "How old is the person?",
                    "Is this for a child, adult, or elderly person?"
                ],
                "message": "I need to know the patient's age to provide accurate guidance. Please specify if this is for a child, adult, or elderly person.",
                "sources": [],
                "timestamp": datetime.now().isoformat()
            }. Knowledge Graph (Relationship Reasoning)
3. Gemini AI (LLM Reasoning)

This is the most advanced RAG implementation
"""

import os
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import google.generativeai as genai
import json

from .vector_db import VectorDatabase
from .knowledge_graph import MedicalKnowledgeGraph
from .llm_enhanced import (
    MEDICAL_KNOWLEDGE_BASE,
    get_enhanced_classification_prompt,
    generate_generic_emergency_steps,
    EMERGENCY_SOS_NUMBER,
    Severity,
)


class HybridRAGSystem:
    """
    Triple-layer RAG system for emergency medical triage
    """

    def __init__(self):
        print("\n" + "=" * 80)
        print("INITIALIZING HYBRID RAG SYSTEM")
        print("=" * 80)

        # Layer 1: Vector Database
        print("\n[1/3] Initializing Vector Database...")
        self.vector_db = VectorDatabase()

        # Layer 2: Knowledge Graph
        print("\n[2/3] Building Medical Knowledge Graph...")
        self.knowledge_graph = MedicalKnowledgeGraph()
        print("✓ Knowledge graph built with medical relationships")

        # Layer 3: Gemini LLM
        print("\n[3/3] Configuring Gemini AI...")
        genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))
        self.llm = genai.GenerativeModel("gemini-2.5-flash")
        print("✓ Gemini 2.5 Flash configured")

        print("\n" + "=" * 80)
        print("✅ HYBRID RAG SYSTEM READY")
        print("=" * 80 + "\n")

    def classify_emergency(
        self,
        user_input: str,
        age_group: Optional[str] = None,
        location: Optional[Dict[str, float]] = None,
        conversation_history: Optional[List[Dict]] = None,
    ) -> Dict[str, Any]:
        """
        Main classification function using triple-layer RAG

        Args:
            user_input: User's emergency description
            age_group: Patient age (child, adult, elderly) - if None, will be extracted or asked
            location: {"lat": float, "lng": float}
            conversation_history: Previous conversation for context

        Returns:
            Comprehensive emergency assessment
        """

        # Extract age group from text if not provided
        if not age_group:
            age_group = self._extract_age_group(user_input)

        # If still no age group, ask for clarification
        if not age_group:
            return {
                "type": "needs_age_clarification",
                "severity": "unknown",
                "confidence": 0.0,
                "requires_sos": False,
                "requires_helpers": False,
                "sos_number": None,
                "steps": [],
                "bring": [],
                "clarifying_questions": [
                    "How old is the person?",
                    "Is this for a child, adult, or elderly person?",
                ],
                "message": "I need to know the patient's age to provide accurate guidance. Please specify if this is for a child, adult, or elderly person.",
                "sources": [],
                "timestamp": datetime.now().isoformat(),
            }

        print(f'\n🔍 Classifying Emergency: "{user_input}"')
        print(f"   Age Group: {age_group}")
        print("-" * 80)

        # ===== LAYER 1: VECTOR DATABASE SEARCH =====
        print("\n[Layer 1] Vector Database - Semantic Search...")
        vector_results = self.vector_db.search_similar_cases(user_input, n_results=3)

        if vector_results:
            print(f"✓ Found {len(vector_results)} similar cases:")
            for i, result in enumerate(vector_results, 1):
                print(
                    f"  {i}. {result['emergency_type']} ({result['confidence']:.2%} match)"
                )
                print(f"     \"{result['description']}\"")

        vector_best_match = vector_results[0] if vector_results else None
        vector_confidence = (
            vector_best_match["confidence"] if vector_best_match else 0.0
        )

        # ===== LAYER 2: KNOWLEDGE GRAPH ANALYSIS =====
        print("\n[Layer 2] Knowledge Graph - Relationship Analysis...")

        # Extract symptoms from input
        symptoms = self._extract_symptoms(user_input)
        print(f"✓ Extracted symptoms: {symptoms}")

        # Find emergencies by symptoms
        graph_matches = self.knowledge_graph.find_emergency_by_symptoms(symptoms)

        if graph_matches:
            print(f"✓ Graph matches:")
            for emergency, score in graph_matches[:3]:
                print(f"  • {emergency}: {score:.2%}")

        graph_best_match = graph_matches[0] if graph_matches else (None, 0.0)
        graph_emergency, graph_confidence = graph_best_match

        # ===== LAYER 3: GEMINI LLM REASONING =====
        print("\n[Layer 3] Gemini AI - Deep Reasoning...")

        llm_result = self._llm_classify(
            user_input=user_input,
            age_group=age_group,
            location=location,
            vector_context=vector_results[:2],
            graph_context=graph_matches[:2],
        )

        if llm_result:
            print(f"✓ Gemini classification: {llm_result.get('emergency_type')}")
            print(f"  Severity: {llm_result.get('severity')}")
            print(f"  Confidence: {llm_result.get('confidence', 0.0):.2%}")
            print(f"  Reasoning: {llm_result.get('reasoning', 'N/A')[:100]}...")

        # ===== ENSEMBLE DECISION =====
        print("\n[Ensemble] Combining all 3 layers...")
        final_result = self._ensemble_decision(
            user_input=user_input,
            age_group=age_group,
            vector_result=vector_best_match,
            graph_result=graph_best_match,
            llm_result=llm_result,
        )

        print(
            f"\n✅ FINAL DECISION: {final_result['type']} ({final_result['severity']})"
        )
        print(f"   Confidence: {final_result.get('confidence', 0.0):.2%}")
        print(f"   Sources: {', '.join(final_result.get('sources', []))}")
        print("-" * 80)

        return final_result

    def _extract_symptoms(self, text: str) -> List[str]:
        """Extract symptoms from text using simple keyword matching"""

        text_lower = text.lower()

        # Common symptom keywords
        symptom_map = {
            "unconscious": [
                "unconscious",
                "unresponsive",
                "won't wake",
                "not responding",
            ],
            "not_breathing": ["not breathing", "stopped breathing", "no breath"],
            "no_pulse": ["no pulse", "heart stopped"],
            "chest_pain": ["chest pain", "chest hurts", "chest pressure"],
            "shortness_of_breath": [
                "shortness of breath",
                "can't breathe",
                "short of breath",
            ],
            "bleeding": ["bleeding", "blood", "gushing"],
            "choking": ["choking", "choked", "stuck in throat"],
            "dizzy": ["dizzy", "lightheaded"],
            "fainted": ["fainted", "passed out"],
            "burned": ["burned", "burn", "scalded"],
        }

        symptoms = []
        for symptom, keywords in symptom_map.items():
            if any(kw in text_lower for kw in keywords):
                symptoms.append(symptom)

        return symptoms

    def _llm_classify(
        self,
        user_input: str,
        age_group: str,
        location: Optional[Dict],
        vector_context: List[Dict],
        graph_context: List[Tuple],
    ) -> Optional[Dict[str, Any]]:
        """Use Gemini with enhanced context from vector DB and graph"""

        try:
            # Build enhanced prompt with all context
            location_str = None
            if location:
                location_str = f"Lat: {location.get('lat')}, Lng: {location.get('lng')}"

            # Add vector and graph context to prompt
            context = "\n\nCONTEXT FROM VECTOR DATABASE (Similar Cases):\n"
            for i, case in enumerate(vector_context, 1):
                context += f"{i}. {case['emergency_type']} ({case['confidence']:.0%} match): \"{case['description']}\"\n"

            context += "\nCONTEXT FROM KNOWLEDGE GRAPH (Symptom Analysis):\n"
            for emergency, score in graph_context:
                context += f"• {emergency}: {score:.0%} match based on symptoms\n"

            prompt = get_enhanced_classification_prompt(
                user_input, age_group, location_str
            )
            prompt += context

            response = self.llm.generate_content(prompt)
            response_text = (
                response.text.strip().replace("```json", "").replace("```", "").strip()
            )

            import json

            result = json.loads(response_text)
            return result

        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
            return None

    def _ensemble_decision(
        self,
        user_input: str,
        age_group: str,
        vector_result: Optional[Dict],
        graph_result: Tuple[Optional[str], float],
        llm_result: Optional[Dict],
    ) -> Dict[str, Any]:
        """
        Ensemble logic to combine all three sources

        Decision rules:
        1. If all 3 agree → Use with highest confidence
        2. If 2/3 agree → Use majority
        3. If all disagree:
           - If any says CRITICAL → Use CRITICAL (err on side of caution)
           - Otherwise use LLM result (most sophisticated)
        """

        sources = []

        # Extract results
        vector_type = vector_result["emergency_type"] if vector_result else None
        vector_conf = vector_result["confidence"] if vector_result else 0.0

        graph_type, graph_conf = graph_result if graph_result else (None, 0.0)

        llm_type = llm_result.get("emergency_type") if llm_result else None
        llm_conf = llm_result.get("confidence", 0.0) if llm_result else 0.0

        # Weighted Voting - Give more weight to more reliable sources
        votes = {}
        weights = {
            "vector_db": 0.3,      # 30% weight - good for similar cases
            "knowledge_graph": 0.4, # 40% weight - symptom-based, very reliable
            "gemini_ai": 0.5        # 50% weight - most sophisticated reasoning
        }
        
        if vector_type:
            weighted_score = vector_conf * weights["vector_db"]
            votes[vector_type] = votes.get(vector_type, 0) + weighted_score
            sources.append("vector_db")
            
        if graph_type:
            weighted_score = graph_conf * weights["knowledge_graph"]
            votes[graph_type] = votes.get(graph_type, 0) + weighted_score
            sources.append("knowledge_graph")
            
        if llm_type:
            weighted_score = llm_conf * weights["gemini_ai"]
            votes[llm_type] = votes.get(llm_type, 0) + weighted_score
            sources.append("gemini_ai")

        # Get winner with normalized confidence
        if votes:
            winner = max(votes.items(), key=lambda x: x[1])
            final_type = winner[0]
            
            # Calculate weighted average confidence
            total_weight = sum(weights[s] for s in sources if s in weights)
            final_confidence = winner[1] / total_weight if total_weight > 0 else 0.0
            
            # Boost confidence if multiple sources agree
            agreeing_sources = [
                s for s in sources 
                if (s == "vector_db" and vector_type == final_type) or
                   (s == "knowledge_graph" and graph_type == final_type) or
                   (s == "gemini_ai" and llm_type == final_type)
            ]
            if len(agreeing_sources) >= 2:
                final_confidence = min(final_confidence * 1.2, 0.99)  # Boost by 20%, cap at 99%
        else:
            final_type = "unknown"
            final_confidence = 0.0

        # Get knowledge from knowledge base
        kb_entry = MEDICAL_KNOWLEDGE_BASE.get(final_type, {})

        # Check for age-based severity escalation using knowledge graph
        severity = kb_entry.get("severity", Severity.SEVERE)
        escalation = self.knowledge_graph.escalate_severity_by_age(
            final_type, age_group
        )

        if escalation.get("should_escalate"):
            print(f"⚠️  Severity escalated due to age: {escalation.get('reason')}")
            if "MODERATE to SEVERE" in escalation.get("severity_change", ""):
                severity = Severity.SEVERE
            elif "MODERATE to CRITICAL" in escalation.get("severity_change", ""):
                severity = Severity.CRITICAL

        # CONFIDENCE THRESHOLD CHECK - Ask for more info if confidence is too low
        # Lower threshold = more decisive, fewer clarification requests
        CONFIDENCE_THRESHOLD = 0.35  # 35% minimum confidence (was 50%)

        if final_confidence < CONFIDENCE_THRESHOLD:
            # Generate clarifying questions based on top candidates
            clarifying_questions = self._generate_clarifying_questions(
                votes, user_input
            )

            return {
                "type": "needs_clarification",
                "severity": Severity.MODERATE,  # Moderate since it could be serious
                "confidence": round(final_confidence, 3),
                "requires_sos": False,
                "requires_helpers": False,
                "sos_number": None,
                "steps": [],
                "bring": [],
                "clarifying_questions": clarifying_questions,
                "possible_emergencies": [
                    {"type": etype, "confidence": round(conf / len(sources), 3)}
                    for etype, conf in sorted(
                        votes.items(), key=lambda x: x[1], reverse=True
                    )[:3]
                ],
                "message": "I need more information to accurately assess the situation. Please answer these questions:",
                "sources": sources,
                "timestamp": datetime.now().isoformat(),
            }

        # SOS LOGIC: Trigger for ANY CRITICAL/SEVERE emergency
        # Whether person is responsive or not doesn't matter - if it's severe, call SOS
        should_trigger_sos = kb_entry.get("requires_sos", True)
        
        if should_trigger_sos:
            print(f"🚨 SOS WILL BE TRIGGERED: {severity} emergency detected ({final_type})")
        
        # Build final response
        result = {
            "type": final_type,
            "severity": severity,
            "confidence": round(final_confidence, 3),
            "requires_sos": should_trigger_sos,
            "requires_helpers": kb_entry.get("requires_helpers", True),
            "sos_number": (
                EMERGENCY_SOS_NUMBER if should_trigger_sos else None
            ),
            "steps": kb_entry.get("steps", generate_generic_emergency_steps()),
            "bring": kb_entry.get("bring", []),
            "helper_instructions": kb_entry.get("helper_instructions", ""),
            "symptoms": kb_entry.get("symptoms", []),
            "contraindications": kb_entry.get("contraindications", []),
            "sources": sources,
            "vector_match": (
                {"type": vector_type, "confidence": round(vector_conf, 3)}
                if vector_type
                else None
            ),
            "graph_match": (
                {"type": graph_type, "confidence": round(graph_conf, 3)}
                if graph_type
                else None
            ),
            "llm_match": (
                {
                    "type": llm_type,
                    "confidence": round(llm_conf, 3),
                    "reasoning": llm_result.get("reasoning") if llm_result else None,
                }
                if llm_type
                else None
            ),
            "age_escalation": escalation if escalation.get("should_escalate") else None,
            "timestamp": datetime.now().isoformat(),
        }

        # Add graph insights
        progressions = self.knowledge_graph.check_progression_risk(final_type)
        if progressions:
            result["progression_risks"] = progressions

        time_critical = self.knowledge_graph.get_time_criticality(final_type)
        if time_critical:
            result["time_critical_minutes"] = time_critical

        return result

    def _extract_age_group(self, text: str) -> Optional[str]:
        """
        Extract age group from user input text

        Returns:
            'child', 'adult', 'elderly', or None if cannot determine
        """
        import re

        text_lower = text.lower()

        # Elderly keywords
        elderly_patterns = [
            r"\belderly\b",
            r"\bsenior\b",
            r"\bold\s+(man|woman|person|lady|gentleman)\b",
            r"\bgrandpa\b",
            r"\bgrandma\b",
            r"\bgrandfather\b",
            r"\bgrandmother\b",
            r"\baged\b",
            r"\b(7[0-9]|8[0-9]|9[0-9])\s*(years?\s*old|y\.?o\.?)\b",
        ]

        for pattern in elderly_patterns:
            if re.search(pattern, text_lower):
                return "elderly"

        # Child keywords (0-17 years)
        child_patterns = [
            r"\bchild\b",
            r"\bkid\b",
            r"\bbaby\b",
            r"\binfant\b",
            r"\btoddler\b",
            r"\bboy\b",
            r"\bgirl\b",
            r"\bson\b",
            r"\bdaughter\b",
            r"\bteen\b",
            r"\byoung\b",
            r"\bminor\b",
            r"\bnewborn\b",
            r"\b([1-9]|1[0-7])\s*(years?\s*old|y\.?o\.?|months?\s*old)\b",
        ]

        for pattern in child_patterns:
            if re.search(pattern, text_lower):
                return "child"

        # Adult keywords (18-64 years) or default
        adult_patterns = [
            r"\badult\b",
            r"\bman\b",
            r"\bwoman\b",
            r"\bperson\b",
            r"\b(1[8-9]|[2-6][0-9])\s*(years?\s*old|y\.?o\.?)\b",
        ]

        for pattern in adult_patterns:
            if re.search(pattern, text_lower):
                return "adult"

        # Cannot determine from text
        return None

    def _detect_unresponsiveness(self, text: str) -> bool:
        """
        Detect if the person is unresponsive/unconscious from user input
        
        Returns True if person appears unable to help themselves
        """
        import re
        
        text_lower = text.lower()
        
        # Unresponsiveness indicators
        unresponsive_patterns = [
            r"\bunresponsive\b",
            r"\bunconscious\b",
            r"\bnot\s+responding\b",
            r"\bnot\s+breathing\b",
            r"\bstopped\s+breathing\b",
            r"\bno\s+breath\b",
            r"\bpassed\s+out\b",
            r"\bcollapsed\b",
            r"\bnot\s+moving\b",
            r"\blimp\b",
            r"\blifeless\b",
            r"\bfainted\b",
            r"\bno\s+pulse\b",
            r"\bnot\s+waking\b",
            r"\bcan'?t\s+wake\b",
            r"\bno\s+response\b",
        ]
        
        for pattern in unresponsive_patterns:
            if re.search(pattern, text_lower):
                return True
        
        # First-person indicators (user is the patient, not someone helping)
        first_person_patterns = [
            r"\bi\s+(have|feel|am|got)\b",
            r"\bmy\s+(chest|arm|head|leg|heart)\b",
            r"\bi'?m\s+(feeling|having|experiencing)\b",
        ]
        
        for pattern in first_person_patterns:
            if re.search(pattern, text_lower):
                return False  # User can help themselves, no auto-SOS
        
        return False  # Default: don't trigger SOS unless clear unresponsiveness

    def _generate_clarifying_questions(
        self, votes: Dict[str, float], user_input: str
    ) -> List[str]:
        """
        Generate clarifying questions based on ambiguous classification

        Args:
            votes: Emergency type candidates with their confidence scores
            user_input: Original user input

        Returns:
            List of clarifying questions to ask the user
        """
        questions = []

        # Get top 3 candidates
        top_candidates = sorted(votes.items(), key=lambda x: x[1], reverse=True)[:3]

        if not top_candidates:
            return [
                "Can you describe what happened in more detail?",
                "Is the person conscious and breathing?",
                "Are there any visible injuries?",
            ]

        # Emergency-specific questions
        emergency_questions = {
            "cardiac_arrest": [
                "Is the person breathing?",
                "Are they responsive when you tap their shoulders?",
                "Do you feel a pulse?",
            ],
            "choking": [
                "Can the person speak or cough?",
                "Are they clutching their throat?",
                "Is their face turning blue?",
            ],
            "bleeding": [
                "Where is the bleeding coming from?",
                "Is blood spurting or flowing steadily?",
                "Can you see the source of bleeding?",
            ],
            "heart_attack": [
                "Is there chest pain or pressure?",
                "Does the pain radiate to the arm, jaw, or back?",
                "Is the person sweating or nauseous?",
            ],
            "stroke": [
                "Can the person smile evenly?",
                "Can they raise both arms?",
                "Is their speech slurred or confused?",
            ],
            "seizure": [
                "Is the person shaking or jerking?",
                "Have they lost consciousness?",
                "How long has the seizure lasted?",
            ],
            "diabetic_emergency": [
                "Does the person have diabetes?",
                "Are they confused or acting strangely?",
                "When did they last eat?",
            ],
            "allergic_reaction": [
                "Is there difficulty breathing or swelling?",
                "Did they recently eat or get stung?",
                "Do they have an EpiPen?",
            ],
            "poisoning": [
                "What did they ingest?",
                "How much and when?",
                "Do you have the container?",
            ],
            "burn": [
                "What caused the burn?",
                "How large is the affected area?",
                "Are there blisters?",
            ],
            "fracture": [
                "Can they move the injured area?",
                "Is the limb deformed or at an odd angle?",
                "When did the injury occur?",
            ],
            "fainting": [
                "Did they hit their head when falling?",
                "Are they conscious now?",
                "Were there any warning signs before fainting?",
            ],
            "hypothermia": [
                "What's the person's body temperature?",
                "Are they shivering?",
                "How long were they exposed to cold?",
            ],
            "heat_stroke": [
                "What's the person's body temperature?",
                "Are they sweating or is their skin dry?",
                "Are they confused or disoriented?",
            ],
        }

        # Add questions for top candidate
        if top_candidates:
            top_type = top_candidates[0][0]
            if top_type in emergency_questions:
                questions.extend(emergency_questions[top_type][:2])  # Add 2 questions

        # Add generic assessment question
        questions.append("Can you describe any other symptoms you're observing?")

        return questions[:3]  # Return max 3 questions

    def get_system_stats(self) -> Dict[str, Any]:
        """Get statistics about the RAG system"""

        return {
            "vector_db": self.vector_db.get_stats(),
            "knowledge_graph": {
                "total_nodes": self.knowledge_graph.graph.number_of_nodes(),
                "total_edges": self.knowledge_graph.graph.number_of_edges(),
                "emergency_types": len(
                    [
                        n
                        for n, d in self.knowledge_graph.graph.nodes(data=True)
                        if d.get("type").value == "emergency"
                    ]
                ),
            },
            "llm": {"model": "gemini-2.5-flash", "provider": "Google"},
        }
