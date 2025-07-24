# logic/dynamic_chat.py

import os
import openai
from logic.user_analysis import apply_all_analysis_layers
from logic.prompt_engine import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality, save_cached_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# بدء المحادثة الديناميكية
# -----------------------------
def continue_dynamic_chat(messages, user_id, lang="العربية"):
    try:
        # استخراج إجابات المستخدم من أول رسالة
        answers = extract_answers_from_messages(messages)
        user_analysis = apply_all_analysis_layers(str(answers))

        # توليد أو جلب الشخصية الذكية
        personality = get_cached_personality(user_analysis, lang)
        if not personality:
            personality = build_dynamic_personality(user_analysis, lang)
            save_cached_personality(f"{lang}_{hash(str(user_analysis))}", personality)

        # بناء أول برومبت فقط لو هي أول رسالة
        if len(messages) == 1:
            full_prompt = build_main_prompt(
                analysis=user_analysis,
                answers=answers,
                personality=personality,
                previous_recommendation=None,
                ratings=None,
                lang=lang
            )
            messages = [{"role": "user", "content": full_prompt}]

        # إرسال إلى OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.85,
        )

        reply = response.choices[0].message.content.strip()
        messages.append({"role": "assistant", "content": reply})

        # حفظ التفاعل
        log_user_insight(
            user_id=user_id,
            content={
                "language": lang,
                "full_conversation": messages,
                "last_user_message": messages[-2]["content"] if len(messages) >= 2 else None,
                "last_ai_reply": reply,
            },
            event_type="chat_interaction"
        )

        return reply, messages

    except Exception as e:
        return f"❌ حدث خطأ: {str(e)}", messages

# -----------------------------
# توليد شخصية الشات الديناميكية
# -----------------------------
def build_dynamic_personality(user_analysis, lang="العربية"):
    if lang == "العربية":
        return {
            "name": "مدرب Sports Sync",
            "tone": "هادئ، عاطفي، وصادق",
            "style": "تحليل نفسي بأسلوب إنساني",
            "philosophy": "الرياضة وسيلة لاكتشاف الذات، لا فقط لتحسين المظهر."
        }
    else:
        return {
            "name": "Coach Sports Sync",
            "tone": "Calm, Emotional, and Honest",
            "style": "Deep psychological tone with empathy",
            "philosophy": "Sport is a tool to understand yourself, not just your body."
        }

# -----------------------------
# استخراج الإجابات من أول رسالة
# -----------------------------
def extract_answers_from_messages(messages):
    for msg in messages:
        if "answers" in msg.get("content", ""):
            try:
                return eval(msg["content"].split("answers=")[-1].strip())
            except:
                continue
    return {}
