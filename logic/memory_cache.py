# memory_cache.py

import os
import json

CACHE_DIR = "data/cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def get_cache_path(user_id):
    return os.path.join(CACHE_DIR, f"{user_id}_analysis.json")

def save_cached_analysis(user_id, analysis):
    try:
        path = get_cache_path(user_id)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("❌ خطأ أثناء حفظ الكاش:", e)

def load_cached_analysis(user_id):
    try:
        path = get_cache_path(user_id)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print("⚠️ خطأ أثناء تحميل الكاش:", e)
    return None
