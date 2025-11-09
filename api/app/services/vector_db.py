"""
Vector Database Service using ChromaDB
- Semantic search for emergency cases
- Embedding-based similarity matching
- Handles synonyms and typos
"""

import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional
import json

class VectorDatabase:
    """
    Vector database for semantic search of emergency cases
    """

    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize ChromaDB and embedding model

        Args:
            persist_directory: Where to store vector database
        """

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False
            )
        )

        # Load sentence transformer model (384-dimensional embeddings)
        # This model is small, fast, and works offline
        print("Loading sentence transformer model...")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        print("✓ Embedding model loaded")

        # Get or create collection
        try:
            self.collection = self.client.get_collection("emergency_cases")
            print(f"✓ Loaded existing collection with {self.collection.count()} cases")
        except:
            self.collection = self.client.create_collection(
                name="emergency_cases",
                metadata={"description": "Medical emergency cases with embeddings"}
            )
            print("✓ Created new emergency_cases collection")
            self._populate_initial_cases()

    def _populate_initial_cases(self):
        """Populate database with initial medical emergency cases"""

        print("Populating vector database with medical cases...")

        # Comprehensive list of emergency case examples
        training_cases = [
            # ===== CARDIAC ARREST =====
            {
                "id": "ca_001",
                "description": "Person collapsed and isn't breathing",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["collapsed", "not breathing", "unconscious"]
            },
            {
                "id": "ca_002",
                "description": "Someone fell down and has no pulse",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["fell", "no pulse", "unresponsive"]
            },
            {
                "id": "ca_003",
                "description": "My dad collapsed unconscious and won't wake up",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["collapsed", "unconscious", "won't wake"]
            },
            {
                "id": "ca_004",
                "description": "Person stopped breathing suddenly",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["stopped breathing", "sudden"]
            },
            {
                "id": "ca_005",
                "description": "Someone is unresponsive with blue lips",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["unresponsive", "blue lips", "cyanosis"]
            },

            # ===== HEART ATTACK =====
            {
                "id": "ha_001",
                "description": "Severe chest pain and shortness of breath",
                "emergency_type": "chest_pain_cardiac",
                "severity": "CRITICAL",
                "keywords": ["chest pain", "shortness of breath"]
            },
            {
                "id": "ha_002",
                "description": "Crushing feeling in chest radiating to arm",
                "emergency_type": "chest_pain_cardiac",
                "severity": "CRITICAL",
                "keywords": ["crushing chest", "radiating", "arm pain"]
            },
            {
                "id": "ha_003",
                "description": "Person has chest pressure and is sweating heavily",
                "emergency_type": "chest_pain_cardiac",
                "severity": "CRITICAL",
                "keywords": ["chest pressure", "sweating", "diaphoresis"]
            },
            {
                "id": "ha_004",
                "description": "My grandfather is having chest pain and feels nauseous",
                "emergency_type": "chest_pain_cardiac",
                "severity": "CRITICAL",
                "keywords": ["chest pain", "nauseous", "elderly"]
            },

            # ===== CHOKING =====
            {
                "id": "ch_001",
                "description": "Someone is choking on food and can't breathe",
                "emergency_type": "choking",
                "severity": "CRITICAL",
                "keywords": ["choking", "can't breathe", "food"]
            },
            {
                "id": "ch_002",
                "description": "Person has hands on throat and turning blue",
                "emergency_type": "choking",
                "severity": "CRITICAL",
                "keywords": ["hands on throat", "turning blue", "choking sign"]
            },
            {
                "id": "ch_003",
                "description": "Child is gagging and can't speak",
                "emergency_type": "choking",
                "severity": "CRITICAL",
                "keywords": ["gagging", "can't speak", "child"]
            },
            {
                "id": "ch_004",
                "description": "Someone choked on something and is gasping",
                "emergency_type": "choking",
                "severity": "CRITICAL",
                "keywords": ["choked", "gasping", "airway obstruction"]
            },

            # ===== SEVERE BLEEDING =====
            {
                "id": "sb_001",
                "description": "Deep cut on arm with heavy bleeding",
                "emergency_type": "severe_bleeding",
                "severity": "SEVERE",
                "keywords": ["deep cut", "heavy bleeding", "arm"]
            },
            {
                "id": "sb_002",
                "description": "Blood is gushing from a wound",
                "emergency_type": "severe_bleeding",
                "severity": "SEVERE",
                "keywords": ["blood gushing", "wound", "arterial"]
            },
            {
                "id": "sb_003",
                "description": "Person has a deep cut that won't stop bleeding",
                "emergency_type": "severe_bleeding",
                "severity": "SEVERE",
                "keywords": ["deep cut", "won't stop bleeding"]
            },
            {
                "id": "sb_004",
                "description": "Bleeding heavily from laceration",
                "emergency_type": "severe_bleeding",
                "severity": "SEVERE",
                "keywords": ["bleeding heavily", "laceration"]
            },

            # ===== BURNS =====
            {
                "id": "bu_001",
                "description": "Burned hand on hot stove",
                "emergency_type": "burn",
                "severity": "MODERATE",
                "keywords": ["burned", "hot stove", "hand"]
            },
            {
                "id": "bu_002",
                "description": "Scalded by hot water",
                "emergency_type": "burn",
                "severity": "MODERATE",
                "keywords": ["scalded", "hot water"]
            },
            {
                "id": "bu_003",
                "description": "Chemical burn on skin",
                "emergency_type": "burn",
                "severity": "SEVERE",
                "keywords": ["chemical burn", "skin"]
            },
            {
                "id": "bu_004",
                "description": "Large burn area from fire",
                "emergency_type": "burn",
                "severity": "CRITICAL",
                "keywords": ["large burn", "fire"]
            },

            # ===== FAINTING =====
            {
                "id": "fa_001",
                "description": "Person fainted and fell down",
                "emergency_type": "fainting",
                "severity": "MODERATE",
                "keywords": ["fainted", "fell down"]
            },
            {
                "id": "fa_002",
                "description": "Someone passed out briefly",
                "emergency_type": "fainting",
                "severity": "MODERATE",
                "keywords": ["passed out", "brief", "syncope"]
            },
            {
                "id": "fa_003",
                "description": "Elderly person collapsed from dizziness",
                "emergency_type": "fainting",
                "severity": "SEVERE",
                "keywords": ["elderly", "collapsed", "dizziness"]
            },
            {
                "id": "fa_004",
                "description": "Felt lightheaded and lost consciousness",
                "emergency_type": "fainting",
                "severity": "MODERATE",
                "keywords": ["lightheaded", "lost consciousness"]
            },

            # ===== BREATHING DIFFICULTY =====
            {
                "id": "bd_001",
                "description": "Can't breathe properly, wheezing",
                "emergency_type": "breathing_difficulty",
                "severity": "SEVERE",
                "keywords": ["can't breathe", "wheezing"]
            },
            {
                "id": "bd_002",
                "description": "Asthma attack, short of breath",
                "emergency_type": "breathing_difficulty",
                "severity": "SEVERE",
                "keywords": ["asthma attack", "short of breath"]
            },
            {
                "id": "bd_003",
                "description": "Difficulty breathing and chest feels tight",
                "emergency_type": "breathing_difficulty",
                "severity": "SEVERE",
                "keywords": ["difficulty breathing", "chest tight"]
            },

            # ===== MINOR CUT =====
            {
                "id": "mc_001",
                "description": "Small cut on finger from knife",
                "emergency_type": "minor_cut",
                "severity": "MILD",
                "keywords": ["small cut", "finger", "knife"]
            },
            {
                "id": "mc_002",
                "description": "Paper cut that's bleeding a little",
                "emergency_type": "minor_cut",
                "severity": "MILD",
                "keywords": ["paper cut", "bleeding little"]
            },
            {
                "id": "mc_003",
                "description": "Scraped knee, minor bleeding",
                "emergency_type": "minor_cut",
                "severity": "MILD",
                "keywords": ["scraped", "knee", "minor bleeding"]
            },

            # ===== VARIATIONS & SYNONYMS =====
            {
                "id": "var_001",
                "description": "Heart stopped beating",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["heart stopped"]
            },
            {
                "id": "var_002",
                "description": "Not responding to anything",
                "emergency_type": "cardiac_arrest",
                "severity": "CRITICAL",
                "keywords": ["not responding", "unresponsive"]
            },
            {
                "id": "var_003",
                "description": "Something stuck in throat, can't breathe",
                "emergency_type": "choking",
                "severity": "CRITICAL",
                "keywords": ["stuck in throat", "can't breathe"]
            },
        ]

        # Generate embeddings and add to collection
        for case in training_cases:
            embedding = self.embedder.encode(case["description"]).tolist()

            self.collection.add(
                ids=[case["id"]],
                embeddings=[embedding],
                documents=[case["description"]],
                metadatas=[{
                    "emergency_type": case["emergency_type"],
                    "severity": case["severity"],
                    "keywords": json.dumps(case["keywords"])
                }]
            )

        print(f"✓ Added {len(training_cases)} cases to vector database")

    def search_similar_cases(
        self,
        query: str,
        n_results: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Search for similar emergency cases using semantic similarity

        Args:
            query: User's emergency description
            n_results: Number of top results to return

        Returns:
            List of similar cases with confidence scores
        """

        # Generate embedding for query
        query_embedding = self.embedder.encode(query).tolist()

        # Search collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        # Format results
        similar_cases = []
        if results and results['ids']:
            for i, case_id in enumerate(results['ids'][0]):
                metadata = results['metadatas'][0][i]
                distance = results['distances'][0][i]

                # Convert distance to confidence (0.0 = identical, 2.0 = very different)
                # Lower distance = higher confidence
                confidence = max(0.0, 1.0 - (distance / 2.0))

                similar_cases.append({
                    "case_id": case_id,
                    "emergency_type": metadata["emergency_type"],
                    "severity": metadata["severity"],
                    "description": results['documents'][0][i],
                    "confidence": round(confidence, 3),
                    "distance": round(distance, 3)
                })

        return similar_cases

    def add_case(
        self,
        case_id: str,
        description: str,
        emergency_type: str,
        severity: str,
        keywords: List[str] = None
    ):
        """Add a new case to the vector database"""

        embedding = self.embedder.encode(description).tolist()

        self.collection.add(
            ids=[case_id],
            embeddings=[embedding],
            documents=[description],
            metadatas=[{
                "emergency_type": emergency_type,
                "severity": severity,
                "keywords": json.dumps(keywords or [])
            }]
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics"""

        return {
            "total_cases": self.collection.count(),
            "collection_name": self.collection.name,
            "embedding_model": "all-MiniLM-L6-v2",
            "embedding_dimensions": 384
        }
