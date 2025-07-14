import openai
import os
import json

# إعداد المفتاح مباشرة (نظام OpenAI القديم)
openai.api_key = os.getenv("OPENAI_API_KEY")

# استيراد الطبقات التحليلية من مجلد analysis
from analysis.analysis_layers_1_40 import apply_layers_1_40
from analysis.analysis_layers_41_80 import apply_layers_41_80
from analysis.analysis_layers_81_100 import apply_layers_81_100
from analysis.analysis_layers_101_141 import apply_layers_101_141

# دمج جميع الطبقات التحليلية
def apply_all_analysis_layers(user_answers):
    analysis_1_40 = apply_layers_1_40(user_answers)
    analysis_41_80 = apply_layers_41_80(user_answers)
    analysis_81_100 = apply_layers_81_100(user_answers)
    analysis_101_141 = apply_layers_101_141(user_answers)

    return {
        "1-40": analysis_1_40,
        "41-80": analysis_41_80,
        "81-100": analysis_81_100,
        "101-141": analysis_101_141,
    }

# توليد التوصية الرياضية بناءً على التحليل
def generate_sport_recommendation(user_answers, lang):
    all_layers = apply_all_analysis_layers(user_answers)

    prompt = f"""
    هذه إجابات المستخدم على استبيان تحليل الشخصية الرياضية، مع التحليل الناتج من 141 طبقة نفسية وسلوكية:

    {json.dumps(all_layers, ensure_ascii=False, indent=2)}

    استنادًا إلى هذا التحليل، رشّح له رياضة واحدة فقط، واشرح لماذا تناسبه تحديدًا.
    اكتب الإجابة باللغة: {lang}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "أنت مساعد خبير في علم النفس الرياضي."},
            {"role": "user", "content": prompt}
        ]
    )

    return response['choices'][0]['message']['content'].strip()
