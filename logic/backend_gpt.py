import os
import json
from openai import OpenAI

from logic.analysis_layers.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers.analysis_layers_101_141 import apply_layers_101_141
from logic.user_analysis import save_user_analysis
from logic.prompt_engine import build_main_prompt  # تأكد أنك أنشأت هذا الملف

# إعداد عميل OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# طبقات التحليل الكاملة
def apply_all_analysis_layers(text):
    return {
        "traits_1_40": apply_layers_1_40(text),
        "traits_41_80": apply_layers_41_80(text),
        "traits_81_100": apply_layers_81_100(text),
        "traits_101_141": apply_layers_101_141(text),
    }

# تنسيق الإجابات لاستخدامها كنص موحّد
def format_answers_for_prompt(answers):
    parts = []
    for i in range(20):
        val = answers.get(f'q{i+1}', '')
        if isinstance(val, list):
            parts.append(f"Q{i+1}: {' / '.join(val)}")
        else:
            parts.append(f"Q{i+1}: {str(val)}")
    extra = answers.get("custom_input", "")
    if extra:
        parts.append(f"Extra: {extra}")
    return '\n'.join(parts)

# الوظيفة الأساسية: توليد توصية ذكية
def generate_sport_recommendation(answers, lang="العربية"):
    user_id = answers.get("user_id", "unknown")
    full_text = format_answers_for_prompt(answers)

    # تحليل الإجابات
    analysis = apply_all_analysis_layers(full_text)
    save_user_analysis(user_id, analysis)

    # بناء البرومبت النهائي للتوصية
    prompt = build_main_prompt(analysis, lang)

    # إرسال الطلب إلى GPT
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ خطأ أثناء الاتصال بـ OpenAI:", str(e))
        return ["عذرًا، حدث خطأ أثناء توليد التوصية. يرجى المحاولة لاحقًا."]

    # استخراج التوصيات 1-2-3
    recommendations = []
    for line in content.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            recommendations.append(line.strip())

    if len(recommendations) < 3:
        recommendations = [content]

    return recommendations
