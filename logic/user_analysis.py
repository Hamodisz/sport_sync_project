import os
import json
from datetime import datetime

# مسار الحفظ
SAVE_PATH = "data/insights_log.json"

# دالة مساعدة لتحويل الكائنات إلى شيء قابل للتخزين JSON
def convert_to_serializable(obj):
    try:
        json.dumps(obj)
        return obj
    except TypeError:
        return str(obj)

# دالة لحفظ التحليل لكل مستخدم
def save_user_analysis(user_id, analysis):
    # التأكد أن المسار موجود
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

    # إذا الملف موجود، نقرأه، وإذا لا نبدأ بملف جديد
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    # نحول كل القيم إلى صيغ قابلة للتخزين
    serializable_analysis = {
        k: convert_to_serializable(v)
        for k, v in analysis.items()
    }

    # نضيف معلومات جديدة
    data.append({
        "user_id": user_id,
        "analysis": serializable_analysis,
        "timestamp": datetime.now().isoformat()
    })

    # نحفظ الملف
    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
