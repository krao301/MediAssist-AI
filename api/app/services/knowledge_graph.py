"""
Medical Knowledge Graph
- Maps relationships between symptoms, conditions, and treatments
- Enables logical inference and severity escalation
- Age-based risk assessment
"""

import networkx as nx
from typing import List, Dict, Any, Set, Tuple
from enum import Enum

class NodeType(Enum):
    EMERGENCY = "emergency"
    SYMPTOM = "symptom"
    AGE_GROUP = "age_group"
    SEVERITY = "severity"
    TREATMENT = "treatment"
    CONTRAINDICATION = "contraindication"
    RISK_FACTOR = "risk_factor"

class RelationType(Enum):
    HAS_SYMPTOM = "has_symptom"
    CAUSED_BY = "caused_by"
    LEADS_TO = "leads_to"
    REQUIRES = "requires"
    ESCALATES_WITH = "escalates_with"
    CONTRAINDICATED_BY = "contraindicated_by"
    INCREASES_RISK = "increases_risk"
    SIMILAR_TO = "similar_to"

class MedicalKnowledgeGraph:
    """
    Knowledge graph for medical emergency relationships
    """

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_medical_graph()

    def _build_medical_graph(self):
        """Build comprehensive medical knowledge graph"""

        # ==================== CARDIAC ARREST ====================
        self.graph.add_node("cardiac_arrest",
            type=NodeType.EMERGENCY,
            severity="CRITICAL",
            time_critical_minutes=4
        )

        # Symptoms
        symptoms_cardiac = [
            "unconscious", "not_breathing", "no_pulse",
            "collapsed", "unresponsive", "blue_lips"
        ]
        for symptom in symptoms_cardiac:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "cardiac_arrest",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.95
            )

        # Age-based risk
        self.graph.add_edge("elderly", "cardiac_arrest",
            relation=RelationType.INCREASES_RISK,
            risk_multiplier=2.5
        )

        # Treatments
        self.graph.add_node("cpr", type=NodeType.TREATMENT)
        self.graph.add_node("aed", type=NodeType.TREATMENT)
        self.graph.add_edge("cardiac_arrest", "cpr",
            relation=RelationType.REQUIRES,
            priority=1
        )
        self.graph.add_edge("cardiac_arrest", "aed",
            relation=RelationType.REQUIRES,
            priority=2
        )

        # Contraindications
        self.graph.add_node("no_food_or_water", type=NodeType.CONTRAINDICATION)
        self.graph.add_edge("cardiac_arrest", "no_food_or_water",
            relation=RelationType.CONTRAINDICATED_BY
        )

        # ==================== HEART ATTACK (Chest Pain Cardiac) ====================
        self.graph.add_node("heart_attack",
            type=NodeType.EMERGENCY,
            severity="CRITICAL",
            time_critical_minutes=30
        )

        symptoms_heart_attack = [
            "chest_pain", "chest_pressure", "shortness_of_breath",
            "pain_radiating_arm", "pain_radiating_jaw", "sweating",
            "nausea", "crushing_feeling"
        ]
        for symptom in symptoms_heart_attack:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "heart_attack",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.85
            )

        # Heart attack can lead to cardiac arrest
        self.graph.add_edge("heart_attack", "cardiac_arrest",
            relation=RelationType.LEADS_TO,
            probability=0.40
        )

        # Age risk
        self.graph.add_edge("elderly", "heart_attack",
            relation=RelationType.INCREASES_RISK,
            risk_multiplier=3.0
        )
        self.graph.add_edge("adult", "heart_attack",
            relation=RelationType.INCREASES_RISK,
            risk_multiplier=1.5
        )

        # Treatments
        self.graph.add_node("aspirin", type=NodeType.TREATMENT)
        self.graph.add_node("nitroglycerin", type=NodeType.TREATMENT)
        self.graph.add_edge("heart_attack", "aspirin",
            relation=RelationType.REQUIRES,
            priority=1
        )

        # ==================== CHOKING ====================
        self.graph.add_node("choking",
            type=NodeType.EMERGENCY,
            severity="CRITICAL",
            time_critical_minutes=3
        )

        symptoms_choking = [
            "cant_breathe", "hands_on_throat", "turning_blue",
            "gasping", "wheezing", "unable_to_speak"
        ]
        for symptom in symptoms_choking:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "choking",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.90
            )

        # Choking can lead to cardiac arrest
        self.graph.add_edge("choking", "cardiac_arrest",
            relation=RelationType.LEADS_TO,
            probability=0.60
        )

        # Treatment
        self.graph.add_node("heimlich", type=NodeType.TREATMENT)
        self.graph.add_edge("choking", "heimlich",
            relation=RelationType.REQUIRES,
            priority=1
        )

        # Age considerations
        self.graph.add_edge("child", "choking",
            relation=RelationType.INCREASES_RISK,
            risk_multiplier=1.8
        )

        # ==================== SEVERE BLEEDING ====================
        self.graph.add_node("severe_bleeding",
            type=NodeType.EMERGENCY,
            severity="SEVERE",
            time_critical_minutes=10
        )

        symptoms_bleeding = [
            "blood_gushing", "heavy_bleeding", "deep_cut",
            "arterial_bleeding", "blood_spurting", "blood_pooling"
        ]
        for symptom in symptoms_bleeding:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "severe_bleeding",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.88
            )

        # Can lead to shock
        self.graph.add_node("shock", type=NodeType.EMERGENCY, severity="CRITICAL")
        self.graph.add_edge("severe_bleeding", "shock",
            relation=RelationType.LEADS_TO,
            probability=0.35
        )

        # Treatment
        self.graph.add_node("direct_pressure", type=NodeType.TREATMENT)
        self.graph.add_edge("severe_bleeding", "direct_pressure",
            relation=RelationType.REQUIRES,
            priority=1
        )

        # ==================== STROKE ====================
        self.graph.add_node("stroke",
            type=NodeType.EMERGENCY,
            severity="CRITICAL",
            time_critical_minutes=60
        )

        symptoms_stroke = [
            "facial_drooping", "arm_weakness", "speech_difficulty",
            "sudden_confusion", "vision_problems", "severe_headache",
            "loss_of_balance"
        ]
        for symptom in symptoms_stroke:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "stroke",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.92
            )

        # Age risk
        self.graph.add_edge("elderly", "stroke",
            relation=RelationType.INCREASES_RISK,
            risk_multiplier=4.0
        )

        # ==================== FAINTING ====================
        self.graph.add_node("fainting",
            type=NodeType.EMERGENCY,
            severity="MODERATE",
            time_critical_minutes=None
        )

        symptoms_fainting = [
            "passed_out", "dizzy", "lightheaded",
            "lost_consciousness_brief", "pale"
        ]
        for symptom in symptoms_fainting:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "fainting",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.75
            )

        # Escalation with age
        self.graph.add_edge("elderly", "fainting",
            relation=RelationType.ESCALATES_WITH,
            severity_increase="MODERATE to SEVERE"
        )

        # Can indicate serious condition
        self.graph.add_edge("fainting", "heart_attack",
            relation=RelationType.SIMILAR_TO,
            check_for=["chest_pain", "shortness_of_breath"]
        )

        # ==================== BURNS ====================
        self.graph.add_node("burn",
            type=NodeType.EMERGENCY,
            severity="MODERATE",
            time_critical_minutes=None
        )

        symptoms_burn = [
            "red_skin", "blisters", "charred_skin",
            "white_areas", "severe_pain", "burned_area"
        ]
        for symptom in symptoms_burn:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "burn",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.80
            )

        # Age escalation
        self.graph.add_edge("child", "burn",
            relation=RelationType.ESCALATES_WITH,
            severity_increase="MODERATE to SEVERE"
        )
        self.graph.add_edge("elderly", "burn",
            relation=RelationType.ESCALATES_WITH,
            severity_increase="MODERATE to SEVERE"
        )

        # ==================== BREATHING DIFFICULTY ====================
        self.graph.add_node("breathing_difficulty",
            type=NodeType.EMERGENCY,
            severity="SEVERE",
            time_critical_minutes=5
        )

        symptoms_breathing = [
            "cant_breathe", "gasping", "wheezing",
            "chest_tight", "rapid_breathing", "blue_lips"
        ]
        for symptom in symptoms_breathing:
            self.graph.add_node(symptom, type=NodeType.SYMPTOM)
            self.graph.add_edge(symptom, "breathing_difficulty",
                relation=RelationType.HAS_SYMPTOM,
                weight=0.87
            )

        # Can lead to cardiac arrest
        self.graph.add_edge("breathing_difficulty", "cardiac_arrest",
            relation=RelationType.LEADS_TO,
            probability=0.30
        )

    def find_emergency_by_symptoms(self, symptoms: List[str]) -> List[Tuple[str, float]]:
        """
        Find possible emergencies based on symptoms

        Args:
            symptoms: List of symptom strings

        Returns:
            List of (emergency_type, confidence_score) tuples
        """

        normalized_symptoms = [s.lower().replace(" ", "_") for s in symptoms]

        emergency_scores = {}

        # Find all emergency nodes
        emergency_nodes = [
            n for n, d in self.graph.nodes(data=True)
            if d.get('type') == NodeType.EMERGENCY
        ]

        for emergency in emergency_nodes:
            score = 0.0
            matched_symptoms = 0

            # Get all symptoms that point to this emergency
            for symptom in normalized_symptoms:
                if self.graph.has_edge(symptom, emergency):
                    edge_data = self.graph[symptom][emergency]
                    weight = edge_data.get('weight', 0.5)
                    score += weight
                    matched_symptoms += 1

            if matched_symptoms > 0:
                # Normalize score
                confidence = score / len(normalized_symptoms)
                emergency_scores[emergency] = confidence

        # Sort by confidence
        results = sorted(emergency_scores.items(), key=lambda x: x[1], reverse=True)
        return results

    def escalate_severity_by_age(self, emergency_type: str, age_group: str) -> Dict[str, Any]:
        """
        Check if severity should be escalated based on age

        Args:
            emergency_type: Type of emergency
            age_group: Patient age group (child, adult, elderly)

        Returns:
            Dictionary with escalation info
        """

        if not self.graph.has_edge(age_group, emergency_type):
            return {"should_escalate": False}

        edge_data = self.graph[age_group][emergency_type]
        relation = edge_data.get('relation')

        if relation == RelationType.ESCALATES_WITH:
            return {
                "should_escalate": True,
                "severity_change": edge_data.get('severity_increase'),
                "reason": f"{age_group.title()} patients are at higher risk for {emergency_type.replace('_', ' ')}"
            }
        elif relation == RelationType.INCREASES_RISK:
            return {
                "should_escalate": True,
                "risk_multiplier": edge_data.get('risk_multiplier', 1.5),
                "reason": f"{age_group.title()} patients have {edge_data.get('risk_multiplier', 1.5)}x higher risk"
            }

        return {"should_escalate": False}

    def get_treatments(self, emergency_type: str) -> List[Dict[str, Any]]:
        """Get recommended treatments for emergency"""

        if emergency_type not in self.graph:
            return []

        treatments = []

        for successor in self.graph.successors(emergency_type):
            node_data = self.graph.nodes[successor]
            edge_data = self.graph[emergency_type][successor]

            if edge_data.get('relation') == RelationType.REQUIRES:
                if node_data.get('type') == NodeType.TREATMENT:
                    treatments.append({
                        "name": successor,
                        "priority": edge_data.get('priority', 999)
                    })

        # Sort by priority
        treatments.sort(key=lambda x: x['priority'])
        return treatments

    def get_contraindications(self, emergency_type: str) -> List[str]:
        """Get contraindications for emergency"""

        if emergency_type not in self.graph:
            return []

        contraindications = []

        for successor in self.graph.successors(emergency_type):
            node_data = self.graph.nodes[successor]
            edge_data = self.graph[emergency_type][successor]

            if edge_data.get('relation') == RelationType.CONTRAINDICATED_BY:
                if node_data.get('type') == NodeType.CONTRAINDICATION:
                    contraindications.append(successor.replace("_", " ").title())

        return contraindications

    def check_progression_risk(self, emergency_type: str) -> List[Dict[str, Any]]:
        """Check what this emergency might lead to"""

        if emergency_type not in self.graph:
            return []

        progressions = []

        for successor in self.graph.successors(emergency_type):
            edge_data = self.graph[emergency_type][successor]

            if edge_data.get('relation') == RelationType.LEADS_TO:
                node_data = self.graph.nodes[successor]
                progressions.append({
                    "condition": successor,
                    "probability": edge_data.get('probability', 0.0),
                    "severity": node_data.get('severity', 'UNKNOWN')
                })

        return progressions

    def get_time_criticality(self, emergency_type: str) -> int:
        """Get time-critical window in minutes"""

        if emergency_type not in self.graph:
            return None

        return self.graph.nodes[emergency_type].get('time_critical_minutes')
