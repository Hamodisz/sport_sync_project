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
        # تحليل إجابات المستخدم
        user_analysis = apply_all_analysis_layers(str(answers))

        # توليد أو استرجاع شخصية المدرب
        personality = get_cached_personality(user_analysis, lang)
        if not personality:
            personality = build_dynamic_personality(user_analysis, lang)
            save_cached_personality(f"{lang}_{hash(str(user_analysis))}", personality)

        # بناء البرومبت الكامل
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

        return reply

    except Exception as e:
        return f"❌ حدث خطأ أثناء المحادثة: {str(e)}"

# توليد شخصية الذكاء حسب اللغة
def build_dynamic_personality(user_analysis, lang="العربية"):
    if lang == "العربية":
        return {
            "name": "مدرب Sports Sync",
            "tone": "تحفيزي، عاطفي، وعميق",
            "style": "محادثة تحليلية ذكية بأسلوب إنساني واقعي",
            "philosophy": "الرياضة مرآة للذات، والهدف الحقيقي هو التوازن لا الكمال."
        }
    else:
        return {
            "name": "Coach Sports Sync",
            "tone": "Motivational, Emotional, and Deep",
            "style": "Smart analytical conversation with a human tone",
            "philosophy": "Sport is a mirror to the self. The real goal is balance, not perfection."
        }
