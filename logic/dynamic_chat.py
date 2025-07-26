import openai
import os
from logic.user_analysis import apply_all_analysis_layers
from logic.shared_utils import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality, save_cached_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# المحادثة التفاعلية الكاملة
# -------------------------------
def start_dynamic_chat(answers, previous_recommendation, ratings, user_id, lang="العربية", chat_history=[], user_message=""):
    try:
        # تحليل المستخدم
        user_analysis = apply_all_analysis_layers(str(answers))

        # توليد أو جلب شخصية المدرب
        personality = get_cached_personality(user_analysis, lang)
        if not personality:
            personality = build_dynamic_personality(user_analysis, lang)
            key = f"{lang}_{hash(str(user_analysis))}"
            save_cached_personality(key, personality)

        # بناء الرسائل
        messages = []

        # مقدمة سياقية في أول رسالة للنموذج
        intro_prompt = build_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            previous_recommendation=previous_recommendation,
            ratings=ratings,
            lang=lang
        )
        messages.append({"role": "system", "content": intro_prompt})

        # تضمين سجل المحادثة السابق (سؤال-جواب)
        for entry in chat_history:
            messages.append({"role": entry["role"], "content": entry["content"]})

        # تضمين رسالة المستخدم الأخيرة (رده الحالي)
        if user_message:
            messages.append({"role": "user", "content": user_message})

        # إرسال للموديل
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.9
        )

        reply = response.choices[0].message.content.strip()

        # حفظ التفاعل
        log_user_insight(
            user_id=user_id,
            content={
                "language": lang,
                "answers": answers,
                "ratings": ratings,
                "user_analysis": user_analysis,
                "previous_recommendation": previous_recommendation,
                "personality_used": personality,
                "user_message": user_message,
                "ai_reply": reply,
                "full_chat": chat_history + [{"role": "user", "content": user_message}, {"role": "assistant", "content": reply}]
            },
            event_type="chat_interaction"
        )

        return reply

    except Exception as e:
        return f"❌ حدث خطأ أثناء المحادثة الديناميكية: {str(e)}"

# -------------------------------
# توليد شخصية المدرب الديناميكية
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
