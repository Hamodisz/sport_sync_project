# logic/backend_gpt.py

import os
import openai
import json
from logic.prompt_engine import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality
from logic.user_analysis import analyze_user_from_answers

# إعداد مفتاح OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# توليد التوصيات الرياضية الذكية
# -------------------------------
def generate_sport_recommendation(answers, lang="العربية"):
    try:
        # تحليل المستخدم من الإجابات
        user_analysis = analyze_user_from_answers(answers)
        personality = get_cached_personality(user_analysis, lang=lang)

        # توليد البرومبت الكامل (مع مفاتيح محسّنة لتوافق الديناميك)
        prompt = build_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            previous_recommendation=None,
            ratings=None,
            lang=lang
        )

        # إرسال الطلب إلى OpenAI
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
        )

        full_response = completion.choices[0].message.content.strip()

        # تقسيم التوصيات (يجب أن يحتوي الرد على 3 توصيات مفصولة بعناوين واضحة)
        recs = split_recommendations(full_response)

        # حفظ في اللوج
       log_user_insight(
    content="initial_recommendation",  # أو أي نوع محتوى مناسب
    data={
        "answers": answers,
        "language": lang,
        "recommendations": recs,
        "user_analysis": user_analysis,
        "personality_used": personality,
    }
)

        return recs
    except Exception as e:
        return [f"حدث خطأ أثناء توليد التوصية: {str(e)}"]

# -------------------------------
# تقسيم التوصيات من الرد الكامل
# -------------------------------
def split_recommendations(full_text):
    # طريقة ذكية لتقسيم النص إلى 3 أجزاء
    recs = []
    lines = full_text.splitlines()
    buffer = []
    for line in lines:
        if "التوصية" in line and len(buffer) > 0:
            recs.append("\n".join(buffer).strip())
            buffer = [line]
        else:
            buffer.append(line)
    if buffer:
        recs.append("\n".join(buffer).strip())
    return recs[:3]  # نضمن فقط 3 توصيات كحد أقصى
