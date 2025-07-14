import openai
import os

# تعيين المفتاح مباشرة حسب طريقة openai الجديدة
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_sport_recommendation(answers, lang):
    if lang == "العربية":
        prompt = "هذه إجابات مستخدم على استبيان تحليل الشخصية والاهتمامات لاختيار الرياضة الأنسب له:\n\n"
    else:
        prompt = "These are a user's answers to a personality and interest questionnaire to find the best sport:\n\n"

    for i, ans in enumerate(answers, 1):
        prompt += f"{i}. {ans}\n"

    prompt += "\nBased on this, suggest the most suitable sport and justify why."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional sports psychologist and AI coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
