import openai
import os

# تعيين مفتاح API بالطريقة الصحيحة للنسخة 1.30.1
openai.api_key = os.getenv("OPENAI_API_KEY")

# الدالة الرئيسية لتوليد التوصية الرياضية
def generate_sport_recommendation(answers, lang):
    if lang == "العربية":
        prompt = f"""هذه إجابات مستخدم على استبيان تحليل الشخصية الرياضية. استخرج السمات النفسية والرياضية من كل إجابة ثم رشح له رياضة واحدة تناسبه، ووضح السبب.
الإجابات: {answers}
التوصية:"""
    else:
        prompt = f"""These are user answers to a personality-based sports questionnaire. Extract psychological and athletic traits from each answer, then recommend ONE sport that suits them best, with a justification.
Answers: {answers}
Recommendation:"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "أنت مساعد خبير في علم النفس الرياضي وتحديد الرياضات المناسبة حسب الشخصية."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"حدث خطأ أثناء توليد التوصية: {str(e)}"
