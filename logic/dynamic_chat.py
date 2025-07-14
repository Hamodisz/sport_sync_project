import os
import openai

# إعداد المفتاح بالطريقة الصحيحة
openai.api_key = os.getenv("OPENAI_API_KEY")

# دالة المحادثة الديناميكية
def start_dynamic_chat(user_message, lang="العربية"):
    if lang == "العربية":
        system_prompt = "أنت مساعد ذكي وداعم، تساعد المستخدم في فهم الرياضة المناسبة له بناءً على تحليله السابق."
    else:
        system_prompt = "You are a smart and supportive assistant helping the user understand the best sport for them based on previous analysis."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
    )

    return response.choices[0].message.content
