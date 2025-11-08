import os
import json
from typing import Dict, Any, List
import google.generativeai as genai

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

# First-aid knowledge base
FIRST_AID_KB = {
    "cardiac_arrest": {
        "keywords": ["not breathing", "unconscious", "no pulse", "collapsed", "unresponsive"],
        "severity": "critical",
        "steps": [
            {
                "title": "Check responsiveness",
                "detail": "Tap shoulders firmly and shout 'Are you okay?' Check for normal breathing.",
                "timer_s": 10
            },
            {
                "title": "Call 911 immediately",
                "detail": "Put phone on speaker and keep line open. Tell them: cardiac arrest, CPR in progress.",
                "timer_s": 15
            },
            {
                "title": "Start chest compressions",
                "detail": "Place heel of hand on center of chest. Push hard and fast, at least 2 inches deep. Let chest recoil completely between compressions.",
                "cadence_bpm": 110,
                "timer_s": 120
            },
            {
                "title": "Continue CPR",
                "detail": "Keep going until help arrives or person shows signs of life. Count compressions out loud to maintain rhythm.",
                "cadence_bpm": 110
            }
        ],
        "bring": ["AED if available", "water", "blanket"]
    },
    "choking": {
        "keywords": ["choking", "can't breathe", "hands on throat", "coughing"],
        "severity": "critical",
        "steps": [
            {
                "title": "Assess severity",
                "detail": "Can they cough or speak? If yes, encourage coughing. If no, proceed immediately.",
                "timer_s": 5
            },
            {
                "title": "Call 911",
                "detail": "Have someone call 911 or put on speaker. Tell them: choking emergency.",
                "timer_s": 10
            },
            {
                "title": "Perform Heimlich maneuver",
                "detail": "Stand behind them. Make a fist above navel. Grasp fist with other hand. Give quick, upward thrusts. Repeat 5 times.",
                "timer_s": 30
            },
            {
                "title": "Check airway",
                "detail": "Did object come out? Can they breathe? If still choking, repeat Heimlich.",
                "timer_s": 10
            }
        ],
        "bring": ["water", "tissues"]
    },
    "severe_bleeding": {
        "keywords": ["bleeding", "blood", "cut", "wound", "gushing"],
        "severity": "urgent",
        "steps": [
            {
                "title": "Call 911",
                "detail": "Call immediately for severe bleeding. Keep phone nearby.",
                "timer_s": 15
            },
            {
                "title": "Apply direct pressure",
                "detail": "Use clean cloth or gauze. Press firmly on wound. Don't remove cloth if blood soaks through—add more on top.",
                "timer_s": 60
            },
            {
                "title": "Maintain pressure",
                "detail": "Keep pressing for at least 10 minutes without checking. Elevate wound above heart if possible.",
                "timer_s": 600
            }
        ],
        "bring": ["clean towels", "gauze", "water"]
    },
    "burn": {
        "keywords": ["burn", "burnt", "scalded", "fire"],
        "severity": "urgent",
        "steps": [
            {
                "title": "Stop the burning",
                "detail": "Remove from heat source. Remove jewelry and tight clothing before swelling starts.",
                "timer_s": 30
            },
            {
                "title": "Cool the burn",
                "detail": "Run cool (not cold) water over burn for 10-20 minutes. Do NOT use ice.",
                "timer_s": 600
            },
            {
                "title": "Call 911 if severe",
                "detail": "Call if burn is large (bigger than hand), on face/genitals/joints, or looks deep/charred.",
                "timer_s": 15
            },
            {
                "title": "Cover loosely",
                "detail": "Use clean, dry cloth. Don't apply creams, ointments, or butter.",
                "timer_s": 30
            }
        ],
        "bring": ["clean cloth", "bottled water", "ice pack (not for direct application)"]
    },
    "fainting": {
        "keywords": ["fainted", "passed out", "dizzy", "lightheaded", "collapsed"],
        "severity": "mild",
        "steps": [
            {
                "title": "Ensure safety",
                "detail": "Check for injuries from fall. Move person to safe area if needed.",
                "timer_s": 20
            },
            {
                "title": "Position properly",
                "detail": "Lay person flat on back. Elevate legs 12 inches if possible. Loosen tight clothing.",
                "timer_s": 30
            },
            {
                "title": "Check responsiveness",
                "detail": "If not waking up after 1 minute, call 911. Check breathing.",
                "timer_s": 60
            },
            {
                "title": "Recovery",
                "detail": "When awake, keep lying down for several minutes. Give water or juice if alert.",
                "timer_s": 180
            }
        ],
        "bring": ["water", "juice", "cool cloth"]
    }
}

def classify_and_plan(text: str, locale: str = "en", age_group: str = None) -> Dict[str, Any]:
    """
    Use Gemini to classify emergency and generate first-aid plan
    Falls back to keyword matching if API unavailable
    """
    text_lower = text.lower()
    
    # Try Gemini classification first
    try:
        if os.getenv("GEMINI_API_KEY"):
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""You are a medical triage AI. Analyze this emergency description and classify it.

Emergency description: "{text}"
Age group: {age_group or 'adult'}

Classify into ONE of these categories:
- cardiac_arrest (not breathing, no pulse, collapsed)
- choking (can't breathe, hands on throat)
- severe_bleeding (heavy blood loss)
- burn (thermal injury)
- fainting (briefly unconscious)
- other

Respond with ONLY a JSON object:
{{
  "type": "cardiac_arrest|choking|severe_bleeding|burn|fainting|other",
  "confidence": 0.0-1.0,
  "reasoning": "brief explanation"
}}"""
            
            response = model.generate_content(prompt)
            result = json.loads(response.text.strip().replace("```json", "").replace("```", ""))
            incident_type = result.get("type", "other")
            
            if incident_type in FIRST_AID_KB:
                kb_entry = FIRST_AID_KB[incident_type]
                return {
                    "type": incident_type,
                    "severity": kb_entry["severity"],
                    "steps": kb_entry["steps"],
                    "bring": kb_entry["bring"],
                    "ai_reasoning": result.get("reasoning", "")
                }
    except Exception as e:
        print(f"Gemini API error: {e}")
    
    # Fallback: keyword matching
    for incident_type, data in FIRST_AID_KB.items():
        if any(keyword in text_lower for keyword in data["keywords"]):
            return {
                "type": incident_type,
                "severity": data["severity"],
                "steps": data["steps"],
                "bring": data["bring"]
            }
    
    # Default response for unrecognized emergencies
    return {
        "type": "unknown",
        "severity": "urgent",
        "steps": [
            {
                "title": "Call 911 immediately",
                "detail": "Describe the situation to emergency services.",
                "timer_s": 30
            },
            {
                "title": "Keep person calm and safe",
                "detail": "Stay with them. Keep them still and comfortable.",
                "timer_s": 120
            },
            {
                "title": "Monitor condition",
                "detail": "Watch for changes in breathing, consciousness, or symptoms.",
            }
        ],
        "bring": ["water", "blanket", "phone"]
    }
