# backend_gpt.py

import os
import json
import openai

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141

from logic.user_analysis import save_user_analysis
from logic.prompt_engine import build_main_prompt
from logic.brand_signature import add_brand_signature
from logic.memory_cache import load_cached_analysis, save_cached_analysis
from logic.chat_personality_static import BASE_PERSONALITY
from logic.user_logger import log_user_insight

openai.api_key = os.getenv("OPENAI_API_KEY")

# تنظيف الكائن من الدوال قبل التخزين
def clean_for_logging(obj):
    if isinstance(obj, dict):
        return {k: clean_for_logging(v) for k, v in obj.items() if not callable(v)}
    elif isinstance(obj, list):
        return [clean_for_logging(v) for v in obj if not callable(v)]
    elif callable(obj):
        return str(obj)
    return obj

# تحليل الطبقات
def apply_all_analysis_layers(full_text):
    return {
        "traits_1_40": apply_layers_1_40(full_text),
        "traits_41_80": apply_layers_41_80(full_text),
        "traits_81_100": apply_layers_81_100(full_text),
        "traits_101_141": apply_layers_101_141(full_text),  # ✅ مهم
    }

# تجهيز النص الكامل من الإجابات
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

# توليد التوصية الرياضية الذكية
def generate_sport_recommendation(answers, lang="العربية"):
    user_id = answers.get("user_id", "unknown")
    full_text = format_answers_for_prompt(answers)

    # تحميل التحليل من الذاكرة المؤقتة أو تنفيذه
    analysis = load_cached_analysis(user_id)
    if not analysis:
        analysis = apply_all_analysis_layers(full_text)
        save_user_analysis(user_id, analysis)
        save_cached_analysis(user_id, analysis)

    # حفظ سجل الذكاء المستمر
    log_user_insight(user_id, {
        "lang": lang,
        "traits": analysis,
        "personality": clean_for_logging(BASE_PERSONALITY)
    })

    # بناء البرومبت النهائي
    prompt = build_main_prompt(analysis, lang)
    prompt = add_brand_signature(prompt)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
        )
        content = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("❌ خطأ أثناء الاتصال بـ OpenAI:", str(e))
        return ["عذرًا، حدث خطأ أثناء توليد التوصية. يرجى المحاولة لاحقًا."]

    # استخراج التوصيات المفصولة
    recommendations = []
    for line in content.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            recommendations.append(line.strip())

    # fallback: إذا النظام ما فصلها
    if len(recommendations) < 3:
        recommendations = [content]

    return recommendations
