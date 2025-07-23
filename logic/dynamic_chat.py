# logic/dynamic_chat.py

import openai
import os
from logic.user_analysis import apply_all_analysis_layers
from logic.prompt_engine import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality, save_cached_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, ratings, user_id, lang="العربية"):
    try:
        # تحليل شامل لإجابات المستخدم
        user_analysis = apply_all_analysis_layers(str(answers))

        # جلب شخصية الشات الذكية (أو توليد واحدة إذا لم تكن محفوظة)
        personality = get_cached_personality(user_analysis, lang)
        if not personality:
            # توليد شخصية مدرب مخصصة حسب اللغة والتحليل
            personality = build_dynamic_personality(user_analysis, lang)
            key = f"{lang}_{hash(str(user_analysis))}"
            save_cached_personality(key, personality)

        # توليد البرومبت الكامل بناء على التحليل والشخصية والتقييمات
        prompt = build_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            previous_recommendation=previous_recommendation,
            ratings=ratings,
            lang=lang
        )

        # إرسال إلى OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        reply = response.choices[0].message.content.strip()

        # حفظ في سجل التوصيات
        log_user_insight(
            user_id=user_id,
            content={
                "language": lang,
                "answers": answers,
                "ratings": ratings,
                "user_analysis": user_analysis,
                "previous_recommendation": previous_recommendation,
                "deeper_recommendation": reply,
                "personality_used": personality
            },
            event_type="deeper_recommendation"
        )

        return reply

    except Exception as e:
        return f"❌ حدث خطأ أثناء توليد التوصية الأعمق: {str(e)}"


# -------------------------------
# توليد شخصية الشات ديناميكيًا
# -------------------------------
def build_dynamic_personality(user_analysis, lang="العربية"):
    if lang == "العربية":
        return {
            "name": "مدرب Sports Sync",
            "tone": "هادئ، عاطفي، وصادق",
            "style": "تحليل نفسي عميق بأسلوب إنساني",
            "philosophy": "الرياضة وسيلة لاكتشاف الذات، وليست فقط لتحسين الشكل الخارجي."
        }
    else:
        return {
            "name": "Coach Sports Sync",
            "tone": "Calm, Emotional, and Honest",
            "style": "Deep psychological analysis with a human tone",
            "philosophy": "Sport is a way to discover yourself, not just to improve your appearance."
        }
