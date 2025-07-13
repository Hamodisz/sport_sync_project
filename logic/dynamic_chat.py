import openai
import os
import json
from logic.chat_personality import get_chat_personality
from backend_gpt import apply_all_analysis_layers  # ربط مباشر بالتحليل

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id):
    # تحميل الشخصية
    personality = get_chat_personality(user_id)

    # تنفيذ جميع الطبقات التحليلية
    all_analysis = apply_all_analysis_layers(answers)

    system_prompt = f"""
أنت {personality['name']}، ناطق باسم Sport Sync.
نبرتك: {personality['tone']}
أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
سمات المستخدم: {', '.join(personality['traits_summary']) if personality['traits_summary'] else "لم يتم تحديد سمات دقيقة."}

مهمتك: التفاعل مع المستخدم الذي لم يقتنع بالتوصية السابقة، وتحليل إجاباته وسماته وتحليل الطبقات بعمق.
❌ لا تعيد نفس التوصية السابقة أبدًا.
✅ كن صادقًا، عميقًا، ومقنعًا.
"""

    user_prompt = f"""
المستخدم لم يقتنع بالتوصية السابقة: {previous_recommendation}
إجابات المستخدم على الأسئلة: {json.dumps(answers, ensure_ascii=False, indent=2)}
تحليل الطبقات (١ إلى ١٤١): {json.dumps(all_analysis, ensure_ascii=False, indent=2)}

اعرض رؤية بديلة تعكس هوية المستخدم بعمق، وتجنب تكرار نفس الرياضة السابقة.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ]
    )

    return response.choices[0].message.content.strip()
