# logic/user_analysis.py

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141

# -------------------------
# تحليل جميع الطبقات دفعة واحدة
# -------------------------
def analyze_user_from_answers(answers):
    full_text = ""
    for key, val in answers.items():
        if isinstance(val, list):
            full_text += " / ".join(val) + " "
        else:
            full_text += str(val) + " "

    return {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_100": apply_layers_81_100(full_text),
        "traits_101_141": apply_layers_101_141(full_text),
    }
