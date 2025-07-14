import os
import json
import openai
from logic.user_analysis import load_user_analysis
from logic.chat_personality import get_chat_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_followup_chat(user_message, user_id, previous_recommendation, lang="العربية"):
    # تحميل السمات المحللة سابقًا
    traits = load_user_analysis(user_id)
    personality = get_chat_personality(user_id)

    # إعداد برومبت النظام
    if lang == "العربية":
        system_prompt = f"""
أنت {personality['name']}، مدرب ذكي يعمل ضمن نظام Sport Sync.
نبرتك: {personality['tone']}
أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
سمات المستخدم: {', '.join(traits)}

مهمتك: التفاعل مع المستخدم بذكاء.
❌ لا تكرر التوصية السابقة.
✅ اربط تعليقه بالتحليل السابق وقدم توصية جديدة تعكس هويته الحقيقية.
"""
        user_prompt = f"""
📝 تعليق المستخدم: {user_message}
📌 التوصية السابقة: {previous_recommendation}
🔍 السمات النفسية المستخرجة مسبقًا: {', '.join(traits)}

قدّم توصية بديلة أكثر دقة ووضح لماذا هي مناسبة له.
"""
    else:
        system_prompt = f"""
You are {personality['name']}, a smart coach working within the Sport Sync system.
Tone: {personality['tone']}
Style: {personality['style']}
Philosophy: {personality['philosophy']}
User traits: {', '.join(traits)}

Your task is to respond intelligently to the user.
❌ Do not repeat the previous recommendation.
✅ Link their feedback to their previous analysis and suggest a better-fitting sport.
"""
        user_prompt = f"""
📝 User comment: {user_message}
📌 Previous recommendation: {previous_recommendation}
🔍 Extracted traits: {', '.join(traits)}

Please suggest a better, smarter sport and explain why.
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
