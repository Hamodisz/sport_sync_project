# logic/user_analysis.py

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141

# -----------------------------
# تطبيق كل الطبقات التحليلية
# -----------------------------
def apply_all_analysis_layers(full_text):
    return {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_100": apply_layers_81_100(full_text),
        "traits_101_141": apply_layers_101_141(full_text),
    }

# -----------------------------
# تحليل المستخدم من الإجابات
# -----------------------------
def analyze_user_from_answers(answers):
    try:
        # تحويل الإجابات إلى نص كامل موحّد لتحليل أعمق
        combined = ""
        for key, value in answers.items():
            if isinstance(value, list):
                combined += " ".join(value) + " "
            elif isinstance(value, str):
                combined += value + " "
            else:
                combined += str(value) + " "
        return apply_all_analysis_layers(combined.strip())
    except Exception as e:
        print("❌ خطأ أثناء تحليل المستخدم:", e)
        return {}
