# logic/memory_cache.py

import json
import os

CACHE_DIR = "data/user_sessions_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(key):
    return os.path.join(CACHE_DIR, f"{key}.json")

# -------------------------------
# تحليل المستخدم
# -------------------------------
def get_cached_analysis(key):
    path = get_cache_path(key)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("analysis", "")
    return ""

def save_cached_analysis(key, analysis_data):
    path = get_cache_path(key)
    data = {"analysis": analysis_data}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# -------------------------------
# شخصية المدرب
# -------------------------------
def get_cached_personality(user_analysis, lang):
    key = f"{lang}_{hash(str(user_analysis))}"
    path = get_cache_path(key)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("personality", {})
    return {}

def save_cached_personality(key, personality_data):
    path = get_cache_path(key)
    existing = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing["personality"] = personality_data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
