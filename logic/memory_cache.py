# logic/memory_cache.py

import os
import json
import hashlib

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ----------------------------------------
# توليد اسم ملف بناء على user_id
# ----------------------------------------
def _get_cache_path(user_id, suffix):
    hashed = hashlib.md5(user_id.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{hashed}_{suffix}.json")

# ----------------------------------------
# حفظ التحليل المؤقت
# ----------------------------------------
def save_cached_analysis(user_id, analysis):
    path = _get_cache_path(user_id, "analysis")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

# ----------------------------------------
# تحميل التحليل المؤقت
# ----------------------------------------
def load_cached_analysis(user_id):
    path = _get_cache_path(user_id, "analysis")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ----------------------------------------
# حفظ الشخصية المحسوبة
# ----------------------------------------
def save_cached_personality(user_id, personality):
    path = _get_cache_path(user_id, "personality")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(personality, f, ensure_ascii=False, indent=2)

# ----------------------------------------
# تحميل الشخصية من الذاكرة
# ----------------------------------------
def get_cached_personality(user_analysis, lang="العربية"):
    user_id = user_analysis.get("user_id", "default")
    path = _get_cache_path(user_id, "personality")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "name": "مدرب Sports Sync",
        "tone": "ذكي وتحفيزي",
        "style": "واقعي وشخصي",
        "philosophy": "الرياضة طريق لاكتشاف الذات، وليس فقط وسيلة للياقة."
    }
