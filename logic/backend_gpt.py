import os
from openai import OpenAI

# إنشاء العميل باستخدام الطريقة الجديدة
client = OpenAI()

# دالة التوصية الذكية
def generate_sport_recommendation(answers, lang):
    if lang == "العربية":
        system_message = "أنت خبير في تحليل الشخصية وتقديم توصيات رياضية مناسبة بدقة."
        prompt = (
            "هذه إجابات مستخدم على استبيان تحليل الشخصية والاهتمامات:\n"
            f"{answers}\n"
            "استخرج السمات النفسية والرياضية وقدّم توصية ذكية لرياضة واحدة أو أكثر تناسبه، واشرح السبب بوضوح."
        )
    else:
        system_message = "You are an expert in personality analysis and sports recommendations."
        prompt = (
            "Here are a user's answers to a personality and interest survey:\n"
            f"{answers}\n"
            "Extract key traits and give a smart recommendation for one or more sports that fit, with clear reasoning."
        )

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
