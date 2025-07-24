import os
import openai
import json
from logic.shared_utils import build_main_prompt
from logic.user_logger import log_user_insight
from logic.memory_cache import get_cached_personality
from logic.user_analysis import analyze_user_from_answers

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_sport_recommendation(answers, lang="العربية"):
    try:
        user_analysis = analyze_user_from_answers(answers)
        personality = get_cached_personality(user_analysis, lang=lang)

        prompt = build_main_prompt(
            analysis=user_analysis,
            answers=answers,
            personality=personality,
            previous_recommendation=None,
            ratings=None,
            lang=lang
        )

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
        )

        full_response = completion.choices[0].message.content.strip()
        recs = split_recommendations(full_response)

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

def split_recommendations(full_text):
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
    return recs[:3]
