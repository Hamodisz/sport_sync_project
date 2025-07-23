# logic/user_analysis.py

import hashlib

def analyze_user_from_answers(answers):
    user_id = str(abs(hash(str(answers))))[:10]

    return {
        "user_id": user_id,
        "keywords": extract_keywords(answers),
        "mental_traits": detect_mental_traits(answers),
        "physical_preferences": detect_physical_preferences(answers),
        "language": detect_language(answers),
    }

def extract_keywords(answers):
    text = json.dumps(answers, ensure_ascii=False)
    return [word for word in ["تفكير", "طاقة", "استكشاف", "هدوء"] if word in text]

def detect_mental_traits(answers):
    traits = []
    for val in answers.values():
        if isinstance(val, str) and "عقلي" in val:
            traits.append("Strategic thinker")
    return traits

def detect_physical_preferences(answers):
    prefs = []
    for val in answers.values():
        if isinstance(val, list):
            if any("ماء" in v for v in val):
                prefs.append("Water-based sports")
    return prefs

def detect_language(answers):
    return "العربية"
