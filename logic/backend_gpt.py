import openai
import os

# إعداد مفتاح OpenAI من البيئة
openai.api_key = os.getenv("OPENAI_API_KEY")

# الدالة الرئيسية لتوليد التوصية الرياضية
def generate_sport_recommendation(answers, lang):
    if lang == "العربية":
        prompt = "هذه إجابات مستخدم على استبيان تحليل الشخصية والاهتمامات لتحديد الرياضة المناسبة:\n\n"
    else:
        prompt = "These are a user's answers to a personality and interest questionnaire to find the best sport:\n\n"

    # بناء البروبمت من الإجابات
    for i, ans in enumerate(answers, 1):
        prompt += f"{i}. {ans}\n"

    prompt += "\nBased on this, suggest the most suitable sport and justify why."

    # استدعاء واجهة Chat Completions من openai
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional sports psychologist and AI coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
