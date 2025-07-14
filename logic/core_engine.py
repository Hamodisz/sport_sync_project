import os
import csv
import json
from datetime import datetime

# استيراد الطبقات التحليلية
from analysis_layers.analysis_layers_1_40 import apply_layers_1_40
from analysis_layers.analysis_layers_41_80 import apply_layers_41_80
from analysis_layers.analysis_layers_81_110 import apply_layers_81_110
from analysis_layers.analysis_layers_111_141 import apply_layers_111_141

# استيراد الشخصية الأساسية
from logic.chat_personality import BASE_PERSONALITY

# مسارات الملفات
CSV_PATH = "data/user_sessions.csv"
OUTPUT_PATH = "data/weekly_analysis.json"

# قراءة بيانات المستخدمين من CSV
def read_user_sessions():
    if not os.path.exists(CSV_PATH):
        return []
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# تحليل مستخدم واحد
def analyze_user(user):
    full_text = ' '.join([user.get(f'q{i+1}', '') for i in range(20)]) + ' ' + user.get('custom_input', '')
    analysis = {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_110": apply_layers_81_110(full_text),
        "traits_111_141": apply_layers_111_141(full_text),
        "base_personality": BASE_PERSONALITY,
    }
    return {
        "user_id": user.get("user_id", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "analysis": analysis
    }

# تنفيذ التحليل الكامل لجميع المستخدمين
def run_weekly_analysis():
    users = read_user_sessions()
    results = []

    print(f"🔍 جاري تحليل {len(users)} مستخدم...")

    for user in users:
        try:
            result = analyze_user(user)
            results.append(result)
        except Exception as e:
            print(f"❌ خطأ مع المستخدم {user.get('user_id', 'unknown')}: {e}")

    with open(OUTPUT_PATH, mode='w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ تم حفظ نتائج التحليل الأسبوعي في {OUTPUT_PATH}")

# تشغيل يدوي عند الحاجة
if __name__ == "__main__":
    run_weekly_analysis()
