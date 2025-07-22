# weekly_batch_engine.py

import os
import csv
import json
from datetime import datetime

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141

from logic.chat_personality_static import BASE_PERSONALITY

CSV_PATH = "data/user_sessions.csv"
OUTPUT_PATH = "data/weekly_analysis.json"

def read_user_sessions():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def analyze_user(user):
    full_text = ' '.join([user.get(f"q{i+1}", "") for i in range(20)]) + ' ' + user.get("custom_input", "")
    analysis = {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_100": apply_layers_81_100(full_text),
        "traits_101_141": apply_layers_101_141(full_text),
        "base_personality": BASE_PERSONALITY,
    }
    return {
        "user_id": user.get("user_id", "unknown"),
        "analysis": analysis,
        "timestamp": datetime.utcnow().isoformat()
    }

def run_batch_analysis():
    sessions = read_user_sessions()
    all_results = [analyze_user(user) for user in sessions]
    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"â ØªÙ Ø­ÙØ¸ ØªØ­ÙÙÙ {len(all_results)} ÙØ³ØªØ®Ø¯Ù ÙÙ {OUTPUT_PATH}")

if __name__ == "__main__":
    run_batch_analysis()
