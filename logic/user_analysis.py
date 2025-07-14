import json
import os

def save_user_analysis(user_id, analysis):
    # تأكد أن مجلد data موجود
    os.makedirs("data", exist_ok=True)

    file_path = f"data/{user_id}_analysis.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)
