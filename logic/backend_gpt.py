import os
import openai
import json
from logic.shared_utils import generate_main_prompt  # ✅ دالة البرومبت المخصصة للتوصيات الثلاث
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality
from logic.user_analysis import analyze_user_from_answers

# إعداد العميل
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ------------------------------
# [1] توليد التوصيات الرياضية
# ------------------------------
def generate_sport_recommendation(answers, lang="العربية"):
    try:
        # تحليل المستخدم وبناء الشخصية
        user_analysis = analyze_user_from_answers(answers)
        personality = get_cached_personality(user_analysis, lang=lang)

        # بناء البرومبت الذكي للتوصيات الثلاثة
        prompt = generate_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            lang=lang
        )

        # استدعاء نموذج GPT
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1000  # يضمن استجابة كافية
        )

        # استخراج الرد الكامل وتقسيم التوصيات
        full_response = completion.choices[0].message.content.strip()
        recs = split_recommendations(full_response)

        # حفظ التوصيات في سجل التحليل
        log_user_insight(
            user_id="N/A",
            content={
                "answers": answers,
                "language": lang,
                "recommendations": recs,
                "user_analysis": user_analysis,
                "personality_used": personality,
            },
            event_type="initial_recommendation"
        )

        return recs

    except Exception as e:
        return [f"❌ حدث خطأ أثناء توليد التوصية: {str(e)}"]

# ------------------------------
# [2] تقسيم التوصيات الثلاثة
# ------------------------------
def split_recommendations(full_text):
    recs = []
    lines = full_text.splitlines()
    buffer = []

    for line in lines:
        if "التوصية" in line and buffer:
            recs.append("\n".join(buffer).strip())
            buffer = [line]
        else:
            buffer.append(line)

    if buffer:
        recs.append("\n".join(buffer).strip())

    # إكمال العدد إلى 3 توصيات دائمًا
    while len(recs) < 3:
        recs.append("⚠ لا توجد توصية.")

    return recs[:3]
