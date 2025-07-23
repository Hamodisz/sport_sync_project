# dynamic_chat.py

import openai
import os
from logic.user_analysis import apply_all_analysis_layers
from logic.prompt_engine import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, ratings, user_id, lang="العربية"):
    try:
        # تحليل شامل لإجابات المستخدم
        user_analysis = apply_all_analysis_layers(str(answers))

        # توليد شخصية ذكية ديناميكية بناء على اللغة والتحليل
        personality = get_cached_personality(user_analysis, lang=lang) or {
            "name": "Sports Sync",
            "tone": "تحفيزي وواقعي",
            "style": "يستخدم التعاطف والمنطق معًا لإقناع المستخدم",
            "philosophy": "الرياضة ليست فقط لتحسين الجسم، بل لفهم النفس واكتشاف القدرات الداخلية."
        }

        # توليد البرومبت العاطفي الذكي
        prompt = build_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            previous_recommendation=previous_recommendation,
            ratings=ratings,
            lang=lang
        )

        # إرسال الطلب إلى OpenAI
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )

        reply = response.choices[0].message.content.strip()

        # حفظ في اللوج الذكي
        log_user_insight({
            "user_id": user_id,
            "language": lang,
            "answers": answers,
            "ratings": ratings,
            "user_analysis": user_analysis,
            "previous_recommendation": previous_recommendation,
            "deeper_recommendation": reply,
            "personality_used": personality
        })

        return reply

    except Exception as e:
        return f"❌ حدث خطأ أثناء توليد التوصية الأعمق: {str(e)}"
