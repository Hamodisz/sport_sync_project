import openai
import os
import json
from logic.backend_gpt import apply_all_analysis_layers
from logic.chat_personality import get_chat_personality
from logic.user_analysis import save_user_analysis  # ✅ تم إضافته

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id, lang="العربية"):
    # تحميل الشخصية حسب user_id
    personality = get_chat_personality(user_id)

    # تنفيذ جميع طبقات التحليل
    all_analysis = apply_all_analysis_layers(answers)

    # ✅ تخزين التحليل بعد توليده
    save_user_analysis(user_id, all_analysis)

    # إعداد برومبت النظام
    if lang == "العربية":
        system_prompt = f"""
أنت {personality['name']}، مدرب ذكي يتبع فلسفة Sport Sync.
نبرتك: {personality['tone']}
أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
سمات المستخدم: {', '.join(personality['traits_summary'])}

هدفك: فهم المستخدم وتحليل إجاباته وسماته النفسية.
❌ لا تكرر نفس التوصية السابقة.
✅ قدّم اقتراحًا أعمق يعكس هويته الفعلية.
"""
    else:
        system_prompt = f"""
You are {personality['name']}, a smart coach powered by Sport Sync.
Tone: {personality['tone']}
Style: {personality['style']}
Philosophy: {personality['philosophy']}
User traits: {', '.join(personality['traits_summary'])}

Your mission: Understand the user's personality and guide them to a better sport.
❌ Never repeat the previous suggestion.
✅ Provide a deeper, tailored recommendation that reflects the user's true identity.
"""

    user_prompt = f"""
📌 Previous recommendation: {previous_recommendation}
📋 User answers: {json.dumps(answers, ensure_ascii=False, indent=2)}
🧠 Analysis layers 1–141: {json.dumps(all_analysis, ensure_ascii=False, indent=2)}

Please suggest an alternative sport that fits the user better and explain why.
"""

    # إرسال إلى GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ]
    )

    return response.choices[0].message.content.strip()
