# logic/memory_cache.py

import json
import os

CACHE_DIR = "data/user_sessions_cache"

os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(user_id):
    return os.path.join(CACHE_DIR, f"{user_id}.json")

def get_cached_analysis(user_id):
    path = get_cache_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("analysis", "")
    return ""

def save_cached_analysis(user_id, analysis_data):
    path = get_cache_path(user_id)
    data = {"analysis": analysis_data}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_cached_personality(user_id):
    path = get_cache_path(user_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("personality", {})
    return {}

def save_cached_personality(user_id, personality_data):
    path = get_cache_path(user_id)
    existing = {}
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    existing["personality"] = personality_data
    with open(path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
