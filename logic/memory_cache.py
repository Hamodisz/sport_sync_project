# logic/memory_cache.py

import os
import json

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# -------------------------
# مسارات التخزين
# -------------------------
def _get_analysis_path(user_id):
    return os.path.join(CACHE_DIR, f"{user_id}_analysis.json")

def _get_personality_path(user_id):
    return os.path.join(CACHE_DIR, f"{user_id}_personality.json")

# -------------------------
# تحميل وحفظ التحليل
# -------------------------
def load_cached_analysis(user_id):
    path = _get_analysis_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def save_cached_analysis(user_id, analysis):
    path = _get_analysis_path(user_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

# -------------------------
# تحميل وحفظ شخصية المدرب
# -------------------------
def get_cached_personality(user_analysis, lang="العربية"):
    # توليد اسم مميز حسب اللغة والسمات
    key = f"{lang}_{hash(json.dumps(user_analysis, sort_keys=True))}"
    path = _get_personality_path(key)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return build_dynamic_personality(user_analysis, lang)

def save_cached_personality(key, personality):
    path = _get_personality_path(key)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(personality, f, ensure_ascii=False, indent=2)

# -------------------------
# بناء ديناميكي لشخصية المدرب
# -------------------------
def build_dynamic_personality(user_analysis, lang="العربية"):
    # يتم توليد الشخصية بناءً على التحليل
    # (يمكن تعديل هذا النموذج لاحقًا للتخصيص العميق)
    if lang == "العربية":
        personality = {
            "name": "مدرب Sports Sync",
            "tone": "حنون لكن مباشر",
            "style": "عاطفي، عميق، واقعي",
            "philosophy": "نبحث عن الرياضة التي تكشف جوهرك وتمنحك معنى، مش مجرد نشاط عابر."
        }
    else:
        personality = {
            "name": "Coach Sports Sync",
            "tone": "Caring yet Direct",
            "style": "Emotional, Deep, Practical",
            "philosophy": "We search for the sport that brings out your core—not just another activity."
        }

    # تخزينها في الذاكرة
    key = f"{lang}_{hash(json.dumps(user_analysis, sort_keys=True))}"
    save_cached_personality(key, personality)
    return personality
