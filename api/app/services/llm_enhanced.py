"""
Enhanced LLM Service for MediAssist AI
- Advanced prompt engineering with few-shot learning
- RAG (Retrieval Augmented Generation)
- Conversational follow-up for mild cases
- Severity-based routing
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
import google.generativeai as genai
from datetime import datetime

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

# Emergency SOS Number (POC - not real 911)
EMERGENCY_SOS_NUMBER = "7166170427"

# Severity Levels
class Severity:
    CRITICAL = "CRITICAL"      # Immediate 911 call + SOS
    SEVERE = "SEVERE"          # 911 call + nearby helpers
    MODERATE = "MODERATE"      # Nearby helpers + first aid guidance
    MILD = "MILD"              # Self-help with AI guidance

# Enhanced Medical Knowledge Base with RAG
MEDICAL_KNOWLEDGE_BASE = {
    "cardiac_arrest": {
        "keywords": ["not breathing", "unconscious", "no pulse", "collapsed", "unresponsive", "heart attack", "chest pain severe"],
        "severity": Severity.CRITICAL,
        "requires_sos": True,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Check responsiveness immediately",
                "detail": "Tap shoulders firmly and shout 'Are you okay?' Check if they're breathing normally.",
                "timer_s": 10,
                "critical": True
            },
            {
                "title": "Call 911 NOW - DO NOT DELAY",
                "detail": "Put phone on speaker. Tell them: cardiac arrest, CPR needed, give exact location.",
                "timer_s": 15,
                "critical": True
            },
            {
                "title": "Start chest compressions immediately",
                "detail": "Place heel of hand on center of chest between nipples. Push HARD and FAST at least 2 inches deep. Let chest fully recoil. Don't stop.",
                "cadence_bpm": 110,
                "timer_s": 120,
                "critical": True
            },
            {
                "title": "Continue CPR until help arrives",
                "detail": "Keep compressions going. Count out loud to maintain rhythm. Switch with someone if you get tired. Do NOT stop.",
                "cadence_bpm": 110,
                "critical": True
            }
        ],
        "bring": ["AED if available", "water", "blanket"],
        "helper_instructions": "You are responding to a CARDIAC ARREST emergency. The person is not breathing and may have no pulse. You must start CPR IMMEDIATELY. Follow these steps exactly.",
        "symptoms": ["sudden collapse", "no normal breathing", "no response to touch or voice", "possibly blue lips/face"],
        "contraindications": ["Do NOT give food or water", "Do NOT leave them alone", "Do NOT wait to see if they improve"]
    },
    "choking": {
        "keywords": ["choking", "can't breathe", "hands on throat", "coughing", "gagging", "something stuck throat"],
        "severity": Severity.CRITICAL,
        "requires_sos": True,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Assess if they can cough or speak",
                "detail": "Ask 'Are you choking?' If they can speak/cough forcefully, encourage coughing. If they cannot speak or breathe, ACT IMMEDIATELY.",
                "timer_s": 5,
                "critical": True
            },
            {
                "title": "Call 911 immediately if severe",
                "detail": "Have someone call 911 NOW. Tell them: choking emergency, person cannot breathe.",
                "timer_s": 10,
                "critical": True
            },
            {
                "title": "Perform Heimlich maneuver (abdominal thrusts)",
                "detail": "Stand behind them. Make fist above navel, below ribcage. Grasp fist with other hand. Give 5 quick, upward thrusts. Check if object came out.",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Repeat until object dislodges or help arrives",
                "detail": "Keep doing Heimlich. If they become unconscious, start CPR. Do NOT stop trying.",
                "critical": True
            }
        ],
        "bring": ["water (for after object is removed)", "tissues"],
        "helper_instructions": "You are responding to a CHOKING emergency. The person cannot breathe. Perform the Heimlich maneuver immediately.",
        "symptoms": ["universal choking sign (hands on throat)", "inability to speak", "weak cough", "high-pitched breathing sounds"],
        "contraindications": ["Do NOT slap back first for adults", "Do NOT give water while choking", "Do NOT perform Heimlich on pregnant women - use chest thrusts"]
    },
    "severe_bleeding": {
        "keywords": ["bleeding heavily", "blood gushing", "deep cut", "won't stop bleeding", "arterial bleeding", "blood spurting"],
        "severity": Severity.SEVERE,
        "requires_sos": True,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Call 911 for severe bleeding",
                "detail": "Call immediately if blood is spurting or won't stop. Keep phone nearby.",
                "timer_s": 15,
                "critical": True
            },
            {
                "title": "Apply direct pressure immediately",
                "detail": "Use clean cloth, gauze, or even your bare hand. Press HARD directly on wound. Do NOT lift to check - keep pressing.",
                "timer_s": 60,
                "critical": True
            },
            {
                "title": "Add more cloth if blood soaks through",
                "detail": "Do NOT remove first cloth. Add more cloth on top. Keep pressing firmly for at least 10 minutes straight.",
                "timer_s": 600,
                "critical": False
            },
            {
                "title": "Elevate and maintain pressure",
                "detail": "If possible, raise wounded area above heart level. Keep pressing. Watch for shock symptoms (pale, cold, confused).",
                "critical": False
            }
        ],
        "bring": ["clean towels/gauze", "gloves if available", "water", "blanket"],
        "helper_instructions": "You are responding to severe bleeding. Apply direct pressure immediately and call 911.",
        "symptoms": ["rapid blood loss", "blood pooling", "pale skin", "rapid heartbeat", "confusion"],
        "contraindications": ["Do NOT use tourniquet unless trained", "Do NOT remove embedded objects", "Do NOT clean wound - just stop bleeding"]
    },
    "burn": {
        "keywords": ["burn", "burnt", "scalded", "fire", "hot water", "chemical burn", "electrical burn"],
        "severity": Severity.MODERATE,
        "requires_sos": False,  # Only if severe
        "requires_helpers": False,
        "steps": [
            {
                "title": "Stop the burning process",
                "detail": "Remove person from heat source. Remove jewelry and tight clothing BEFORE swelling starts (unless stuck to skin).",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Cool the burn with water",
                "detail": "Run cool (NOT cold or ice) water over burn for 10-20 minutes. This reduces damage and pain.",
                "timer_s": 600,
                "critical": True
            },
            {
                "title": "Assess severity - call 911 if needed",
                "detail": "Call 911 if: burn is bigger than your hand, on face/genitals/joints, looks deep/charred, or caused by chemicals/electricity.",
                "timer_s": 15,
                "critical": False
            },
            {
                "title": "Cover burn loosely",
                "detail": "Use clean, dry, non-stick cloth. Do NOT apply ice, butter, ointments, or break blisters.",
                "timer_s": 30,
                "critical": False
            }
        ],
        "bring": ["clean cloth", "bottled water", "ice pack (NOT for direct application)", "burn gel if available"],
        "helper_instructions": "You are helping someone with a burn. Cool it with water first, then assess if 911 is needed.",
        "symptoms": ["red skin", "blisters", "white/charred areas", "severe pain or no pain (deep burn)"],
        "contraindications": ["NEVER use ice directly", "NEVER apply butter/oil", "NEVER break blisters", "NEVER remove stuck clothing"]
    },
    "minor_cut": {
        "keywords": ["small cut", "minor bleeding", "scrape", "scratch", "paper cut"],
        "severity": Severity.MILD,
        "requires_sos": False,
        "requires_helpers": False,
        "steps": [
            {
                "title": "Wash your hands first",
                "detail": "Clean your hands with soap and water before touching the wound.",
                "timer_s": 30
            },
            {
                "title": "Stop the bleeding",
                "detail": "Apply gentle pressure with clean cloth for 2-3 minutes.",
                "timer_s": 180
            },
            {
                "title": "Clean the wound",
                "detail": "Rinse with cool running water. Gently clean around the cut with soap.",
                "timer_s": 60
            },
            {
                "title": "Apply antibiotic ointment and bandage",
                "detail": "Apply thin layer of antibiotic cream, then cover with bandage.",
                "timer_s": 30
            }
        ],
        "bring": ["bandages", "antibiotic ointment", "soap", "water"],
        "follow_up_questions": [
            "Is the bleeding stopping with pressure?",
            "Can you see how deep the cut is?",
            "Is the cut clean or is there dirt in it?",
            "Do you have bandages available?"
        ]
    },
    "fainting": {
        "keywords": ["fainted", "passed out", "dizzy", "lightheaded", "collapsed", "syncope"],
        "severity": Severity.MODERATE,
        "requires_sos": False,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Ensure safety and check for injuries",
                "detail": "Check if they hit their head or got injured in the fall. Move them to safe area if needed.",
                "timer_s": 20,
                "critical": False
            },
            {
                "title": "Position them properly",
                "detail": "Lay person flat on back. Elevate legs 12 inches if possible. Loosen tight clothing around neck.",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Check if they're waking up",
                "detail": "If NOT waking up after 1 minute, call 911 immediately. Check breathing. If not breathing normally, start CPR.",
                "timer_s": 60,
                "critical": True
            },
            {
                "title": "Recovery and monitoring",
                "detail": "Once awake, keep lying down for several minutes. Give water or juice if fully alert. Watch for another fainting spell.",
                "timer_s": 180,
                "critical": False
            }
        ],
        "bring": ["water", "juice", "cool cloth", "pillow"],
        "helper_instructions": "You are helping someone who fainted. Keep them lying down and check if they're responsive.",
        "symptoms": ["brief loss of consciousness", "pale skin", "sweating", "rapid recovery"],
        "contraindications": ["Do NOT give food/water if unconscious", "Do NOT make them sit up quickly"]
    },
    "chest_pain_cardiac": {
        "keywords": ["chest pain", "heart attack", "chest pressure", "pain radiating", "crushing chest pain", "chest hurts breathing"],
        "severity": Severity.CRITICAL,
        "requires_sos": True,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Call 911 immediately",
                "detail": "Chest pain with breathing difficulty may be heart attack. Every second counts. Call 911 NOW.",
                "timer_s": 15,
                "critical": True
            },
            {
                "title": "Help person sit down and rest",
                "detail": "Have them sit in comfortable position, slightly upright. Loosen tight clothing around neck and chest.",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Ask about aspirin and nitroglycerin",
                "detail": "If they have prescribed nitroglycerin, help them take it. If not allergic and conscious, give 1 adult aspirin (chew, don't swallow whole).",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Monitor and prepare for CPR",
                "detail": "Stay with them. If they become unconscious and stop breathing, start CPR immediately.",
                "critical": True
            }
        ],
        "bring": ["aspirin if available", "nitroglycerin if prescribed", "phone for 911", "water"],
        "helper_instructions": "You are responding to a possible HEART ATTACK. Keep the person calm and seated. 911 is on the way.",
        "symptoms": ["chest pain", "shortness of breath", "sweating", "nausea", "pain in arm/jaw/back"],
        "contraindications": ["Do NOT give aspirin if allergic", "Do NOT let them drive themselves", "Do NOT leave them alone"]
    },
    "breathing_difficulty": {
        "keywords": ["can't breathe", "short of breath", "wheezing", "asthma attack", "chest tight"],
        "severity": Severity.SEVERE,
        "requires_sos": True,
        "requires_helpers": True,
        "steps": [
            {
                "title": "Call 911 immediately",
                "detail": "Severe breathing difficulty is life-threatening. Call 911 now.",
                "timer_s": 15,
                "critical": True
            },
            {
                "title": "Help them sit upright",
                "detail": "Sitting upright helps breathing. Lean them slightly forward. Loosen tight clothing.",
                "timer_s": 20,
                "critical": True
            },
            {
                "title": "Ask about inhaler or medication",
                "detail": "If they have asthma inhaler or prescribed medication, help them use it now.",
                "timer_s": 30,
                "critical": True
            },
            {
                "title": "Keep calm and monitor",
                "detail": "Stay with them. Keep them calm. Watch for blue lips or worsening - tell 911 immediately if this happens.",
                "critical": True
            }
        ],
        "bring": ["inhaler if available", "water", "phone for 911"],
        "helper_instructions": "You are helping someone with severe breathing difficulty. Keep them calm and sitting upright while waiting for 911.",
        "symptoms": ["gasping for air", "unable to speak in full sentences", "blue lips/fingernails", "panic"],
        "contraindications": ["Do NOT make them lie down", "Do NOT leave them alone"]
    }
}

# Few-shot learning examples for Gemini
FEW_SHOT_EXAMPLES = """
Example 1:
User: "My friend just collapsed on the ground and isn't moving or breathing"
Classification: {
  "emergency_type": "cardiac_arrest",
  "severity": "CRITICAL",
  "confidence": 0.95,
  "requires_sos": true,
  "requires_helpers": true,
  "reasoning": "Collapse with no breathing indicates cardiac arrest - immediate CPR and 911 required"
}

Example 2:
User: "Someone is coughing really hard and holding their throat, can't seem to talk"
Classification: {
  "emergency_type": "choking",
  "severity": "CRITICAL",
  "confidence": 0.92,
  "requires_sos": true,
  "requires_helpers": true,
  "reasoning": "Unable to talk while holding throat = severe choking, needs Heimlich immediately"
}

Example 3:
User: "I cut my finger while cooking, it's bleeding a little bit"
Classification: {
  "emergency_type": "minor_cut",
  "severity": "MILD",
  "confidence": 0.88,
  "requires_sos": false,
  "requires_helpers": false,
  "reasoning": "Small cut with minor bleeding - can be treated with self-care first aid",
  "needs_follow_up": true
}

Example 4:
User: "My dad is having chest pain and can't catch his breath"
Classification: {
  "emergency_type": "cardiac_arrest",
  "severity": "CRITICAL",
  "confidence": 0.90,
  "requires_sos": true,
  "requires_helpers": true,
  "reasoning": "Chest pain + breathing difficulty suggests heart attack - immediate 911 required"
}

Example 5:
User: "I burned my hand on the stove, it really hurts"
Classification: {
  "emergency_type": "burn",
  "severity": "MODERATE",
  "confidence": 0.85,
  "requires_sos": false,
  "requires_helpers": false,
  "reasoning": "Burn needs cooling and assessment, likely not severe enough for 911 unless large area",
  "needs_follow_up": true
}
"""

def get_enhanced_classification_prompt(user_input: str, age_group: str = "adult", location: str = None) -> str:
    """Generate enhanced prompt with few-shot learning and detailed context"""

    prompt = f"""You are MediAssist AI, an expert emergency medical triage system. Your role is to quickly and accurately classify medical emergencies and determine the appropriate response level.

CRITICAL CONTEXT:
- Current time: {datetime.now().isoformat()}
- Patient age group: {age_group}
- Location: {location or "Unknown"}

EMERGENCY SEVERITY LEVELS:
1. CRITICAL: Life-threatening, requires immediate 911 + CPR/first aid (cardiac arrest, choking, severe trauma)
2. SEVERE: Serious injury/illness, requires 911 + nearby helpers (severe bleeding, breathing difficulty)
3. MODERATE: Needs first aid + possible medical attention (burns, sprains, moderate injuries)
4. MILD: Can be handled with self-care guidance (minor cuts, bruises, mild pain)

FEW-SHOT EXAMPLES:
{FEW_SHOT_EXAMPLES}

AVAILABLE EMERGENCY CATEGORIES:
{json.dumps(list(MEDICAL_KNOWLEDGE_BASE.keys()), indent=2)}

USER'S EMERGENCY DESCRIPTION:
"{user_input}"

ANALYZE THIS EMERGENCY AND RESPOND WITH ONLY A JSON OBJECT (no markdown, no code blocks):
{{
  "emergency_type": "<one of the available categories or 'unknown'>",
  "severity": "CRITICAL|SEVERE|MODERATE|MILD",
  "confidence": 0.0-1.0,
  "requires_sos": true/false,
  "requires_helpers": true/false,
  "reasoning": "<brief medical reasoning>",
  "needs_follow_up": true/false,
  "follow_up_question": "<question to ask if needs_follow_up=true>",
  "key_symptoms_identified": ["<list of symptoms>"],
  "red_flags": ["<any concerning signs>"]
}}

IMPORTANT RULES:
1. If confidence < 0.7 OR unclear, ask clarifying questions
2. Always err on the side of caution - if unsure, escalate severity
3. For chest pain, breathing difficulty, unconsciousness → always CRITICAL
4. For children/elderly, increase severity by one level
5. Return ONLY valid JSON, no other text"""

    return prompt

def classify_emergency_enhanced(
    text: str,
    locale: str = "en",
    age_group: str = "adult",
    location: Dict[str, float] = None,
    conversation_history: List[Dict] = None
) -> Dict[str, Any]:
    """
    Enhanced emergency classification with RAG, few-shot learning, and follow-up

    Args:
        text: User's emergency description
        locale: Language locale
        age_group: Patient age group (child, adult, elderly)
        location: {"lat": float, "lng": float}
        conversation_history: Previous messages for context

    Returns:
        Comprehensive emergency assessment with actions
    """

    text_lower = text.lower()

    # Try Gemini API with enhanced prompt
    try:
        if os.getenv("GEMINI_API_KEY"):
            # Use latest Gemini 2.5 Flash for speed and efficiency
            model = genai.GenerativeModel('gemini-2.5-flash')

            # Build context from conversation history
            context = ""
            if conversation_history:
                context = "\n\nPREVIOUS CONVERSATION:\n"
                for msg in conversation_history[-3:]:  # Last 3 messages for context
                    role = msg.get("role", "user")
                    content = msg.get("content", "")
                    context += f"{role.upper()}: {content}\n"

            location_str = None
            if location:
                location_str = f"Lat: {location.get('lat')}, Lng: {location.get('lng')}"

            prompt = get_enhanced_classification_prompt(text, age_group, location_str) + context

            response = model.generate_content(prompt)
            response_text = response.text.strip()

            # Clean up response (remove markdown if present)
            response_text = response_text.replace("```json", "").replace("```", "").strip()

            result = json.loads(response_text)

            # Retrieve relevant knowledge from KB using RAG
            emergency_type = result.get("emergency_type", "unknown")

            if emergency_type in MEDICAL_KNOWLEDGE_BASE:
                kb_entry = MEDICAL_KNOWLEDGE_BASE[emergency_type]

                # Build comprehensive response
                return {
                    "type": emergency_type,
                    "severity": result.get("severity", kb_entry["severity"]),
                    "confidence": result.get("confidence", 0.0),
                    "requires_sos": kb_entry.get("requires_sos", False),
                    "requires_helpers": kb_entry.get("requires_helpers", False),
                    "sos_number": EMERGENCY_SOS_NUMBER if kb_entry.get("requires_sos") else None,
                    "steps": kb_entry["steps"],
                    "bring": kb_entry.get("bring", []),
                    "helper_instructions": kb_entry.get("helper_instructions", ""),
                    "symptoms": kb_entry.get("symptoms", []),
                    "contraindications": kb_entry.get("contraindications", []),
                    "ai_reasoning": result.get("reasoning", ""),
                    "needs_follow_up": result.get("needs_follow_up", False),
                    "follow_up_question": result.get("follow_up_question"),
                    "key_symptoms": result.get("key_symptoms_identified", []),
                    "red_flags": result.get("red_flags", []),
                    "timestamp": datetime.now().isoformat()
                }
            else:
                # Unknown emergency - needs follow-up
                return {
                    "type": "unknown",
                    "severity": "SEVERE",  # Default to severe for safety
                    "confidence": result.get("confidence", 0.0),
                    "requires_sos": result.get("requires_sos", False),
                    "requires_helpers": result.get("requires_helpers", True),
                    "needs_follow_up": True,
                    "follow_up_question": result.get("follow_up_question", "Can you describe the symptoms in more detail? Is the person conscious and breathing?"),
                    "ai_reasoning": result.get("reasoning", ""),
                    "steps": generate_generic_emergency_steps(),
                    "timestamp": datetime.now().isoformat()
                }

    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fall through to keyword matching

    # Fallback: Enhanced keyword matching with RAG
    best_match = None
    best_score = 0

    for emergency_type, data in MEDICAL_KNOWLEDGE_BASE.items():
        score = sum(1 for keyword in data["keywords"] if keyword in text_lower)
        if score > best_score:
            best_score = score
            best_match = emergency_type

    if best_match:
        kb_entry = MEDICAL_KNOWLEDGE_BASE[best_match]
        return {
            "type": best_match,
            "severity": kb_entry["severity"],
            "confidence": min(best_score / len(kb_entry["keywords"]), 0.9),
            "requires_sos": kb_entry.get("requires_sos", False),
            "requires_helpers": kb_entry.get("requires_helpers", False),
            "sos_number": EMERGENCY_SOS_NUMBER if kb_entry.get("requires_sos") else None,
            "steps": kb_entry["steps"],
            "bring": kb_entry.get("bring", []),
            "helper_instructions": kb_entry.get("helper_instructions", ""),
            "symptoms": kb_entry.get("symptoms", []),
            "contraindications": kb_entry.get("contraindications", []),
            "source": "keyword_matching"
        }

    # Default: Unknown emergency
    return {
        "type": "unknown",
        "severity": Severity.SEVERE,
        "confidence": 0.0,
        "requires_sos": True,  # Default to safe side
        "requires_helpers": True,
        "sos_number": EMERGENCY_SOS_NUMBER,
        "steps": generate_generic_emergency_steps(),
        "bring": ["phone", "water", "blanket"],
        "needs_follow_up": True,
        "follow_up_question": "I need more information to help you properly. Can you tell me: Is the person conscious? Are they breathing normally? Are they bleeding?",
        "source": "default_fallback"
    }

def generate_generic_emergency_steps() -> List[Dict]:
    """Generic emergency response steps when type is unknown"""
    return [
        {
            "title": "Assess the situation",
            "detail": "Check if the person is conscious and breathing. Look for obvious injuries or bleeding.",
            "timer_s": 15,
            "critical": True
        },
        {
            "title": "Call 911 immediately if needed",
            "detail": "If unconscious, not breathing normally, severe bleeding, or chest pain - call 911 NOW.",
            "timer_s": 20,
            "critical": True
        },
        {
            "title": "Keep the person safe and comfortable",
            "detail": "Don't move them unless in immediate danger. Keep them warm. Talk to them if conscious.",
            "timer_s": 60,
            "critical": False
        },
        {
            "title": "Monitor and wait for help",
            "detail": "Watch for changes in breathing, consciousness, or condition. Note what happened for EMS.",
            "critical": False
        }
    ]

def generate_follow_up_response(
    original_input: str,
    user_answer: str,
    emergency_type: str
) -> Dict[str, Any]:
    """
    Generate intelligent follow-up based on user's answers for MILD cases
    Uses Gemini for conversational AI
    """

    try:
        if os.getenv("GEMINI_API_KEY"):
            model = genai.GenerativeModel('gemini-2.5-flash')

            kb_entry = MEDICAL_KNOWLEDGE_BASE.get(emergency_type, {})

            prompt = f"""You are MediAssist AI helping with a {emergency_type} situation.

ORIGINAL PROBLEM: {original_input}
USER'S ANSWER: {user_answer}

Based on their answer, provide:
1. Next step or advice
2. Whether they should call 911
3. Another follow-up question if needed

KNOWLEDGE BASE STEPS:
{json.dumps(kb_entry.get('steps', []), indent=2)}

Respond with ONLY a JSON object:
{{
  "advice": "<clear, actionable advice>",
  "should_call_911": true/false,
  "reasoning": "<why this advice>",
  "next_question": "<another question or null>",
  "severity_updated": "CRITICAL|SEVERE|MODERATE|MILD"
}}"""

            response = model.generate_content(prompt)
            response_text = response.text.strip().replace("```json", "").replace("```", "").strip()

            return json.loads(response_text)

    except Exception as e:
        print(f"Follow-up generation error: {e}")

    return {
        "advice": "Please provide more details so I can help you better.",
        "should_call_911": False,
        "next_question": "Can you describe what happened and how you're feeling now?"
    }
