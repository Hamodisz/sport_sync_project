import openai
import os
from logic.chat_personality import get_chat_personality

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id):
    personality = get_chat_personality(user_id)

    system_prompt = f"""
أنت {personality['name']}، ناطق باسم Sport Sync.
نبرتك: {personality['tone']}
أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
سمات المستخدم: {', '.join(personality['traits_summary']) if personality['traits_summary'] else "لم يتم تحديد سمات دقيقة."}

مهمتك: التفاعل مع المستخدم الذي لم يقتنع بالتوصية السابقة، وتحليل إجاباته بعمق، وإعادة بناء توصية أو رؤية أعمق بناءً على هويته.
❌ لا تعيد نفس التوصية السابقة أبدًا.
✅ كن صادقًا، عميقًا، ومقنعًا.
"""

    user_prompt = f"""
المستخدم لم يقتنع بالتوصية السابقة: {previous_recommendation}
إجابات المستخدم على الأسئلة كانت: {answers}

حلل بدقة وقدم رؤية جديدة تعكس شخصيته الحقيقية بشكل أعمق.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ]
    )

    return response.choices[0].message.content.strip()
