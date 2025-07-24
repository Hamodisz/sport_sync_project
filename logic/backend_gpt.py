# logic/backend_gpt.py

import os
import openai
from logic.user_analysis import apply_all_analysis_layers
from logic.memory_cache import get_cached_personality, save_cached_personality
from logic.user_logger import log_user_insight
from logic.prompt_engine import build_main_prompt_from_data  # ← هذه دالة بديلة سيتم شرحها تحت

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sport_recommendation(answers, lang="العربية"):
    try:
        analysis = apply_all_analysis_layers(str(answers))
        personality = get_cached_personality(analysis, lang)
        if not personality:
            personality = {
                "name": "مدرب Sports Sync" if lang == "العربية" else "Coach Sports Sync",
                "tone": "هادئ، صادق" if lang == "العربية" else "Calm and sincere",
                "style": "تحليل نفسي بأسلوب إنساني" if lang == "العربية" else "Human-centered psychological tone",
                "philosophy": "الرياضة أداة لاكتشاف الذات" if lang == "العربية" else "Sport is a tool for self-discovery"
            }
            save_cached_personality(f"{lang}_{hash(str(analysis))}", personality)

        prompt = build_main_prompt_from_data(analysis, answers, personality, [], "", lang)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        reply = response.choices[0].message.content.strip()

        log_user_insight(user_id="unknown", content={
            "answers": answers,
            "language": lang,
            "recommendation": reply
        }, event_type="initial_recommendation")

        return reply
    except Exception as e:
        return f"❌ خطأ: {e}"
