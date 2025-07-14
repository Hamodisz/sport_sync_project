import os
from openai import OpenAI

# ✅ إعداد عميل OpenAI (نسخة 1.30.1 وما فوق)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ الدالة الرئيسية للتوصية الرياضية
def generate_sport_recommendation(answers, lang):
    prompt = build_prompt(answers, lang)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "أنت مساعد ذكي متخصص في تحليل الشخصية وتحديد الرياضة المناسبة لكل شخص."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )
    
    return response.choices[0].message.content.strip()

# ✅ بناء البرومبت بناءً على اللغة
def build_prompt(answers, lang):
    joined = "\n".join([f"{i+1}. {a}" for i, a in enumerate(answers)])
    if lang == "العربية":
        return f"هذه إجابات مستخدم على استبيان لتحديد الرياضة المناسبة:\n{joined}\n\nبناءً على هذه الإجابات، ما هي الرياضة أو الأنشطة التي تناسبه ولماذا؟"
    else:
        return f"These are a user's answers to a sports recommendation survey:\n{joined}\n\nBased on these answers, what sport or activity would suit them best and why?"
