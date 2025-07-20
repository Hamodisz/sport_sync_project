import os
import csv
import json
from datetime import datetime

from analysis.analysis_layers_1_40 import apply_layers_1_40
from analysis.analysis_layers_41_80 import apply_layers_41_80
from analysis.analysis_layers_81_100 import apply_layers_81_100
from analysis.analysis_layers_101_141 import apply_layers_101_141
from logic.chat_personality import BASE_PERSONALITY

CSV_PATH = "data/user_sessions.csv"
OUTPUT_PATH = "data/weekly_analysis.json"

def read_user_sessions():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def analyze_user(user):
    full_text = ' '.join([user.get(f'q{i+1}', '') for i in range(20)]) + ' ' + user.get('custom_input', '')
    analysis = {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_100": apply_layers_81_100(full_text),
        "traits_101_141": apply_layers_101_141(full_text),
        "base_personality": BASE_PERSONALITY,
    }
    return {
        "user_id": user.get("user_id", "unknown
