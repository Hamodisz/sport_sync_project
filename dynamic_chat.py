import json
import os
from openai import OpenAI  # ✅ التعديل هنا

# إعداد العميل باستخدام openai 1.3.0
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# تحميل تحليل المستخدم من ملف user_analysis.json
def load_user_analysis():
    try:
        with open("data/user_analysis.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("summary", "")
    except:
        return ""

# المحادثة التفاعلية بعد رفض التوصية الأولى
def start_dynamic_chat(answers, previous_recommendation):
    user_analysis = load_user_analysis()

    user_text = "\n".join([f"{k}: {v}" for k, v in answers.items()])

    system_prompt = f"""
أنت مساعد ذكي مختص في تحليل الشخصية الرياضية وتوليد توصيات رياضية دقيقة.
- هذا ملخص تحليل الشخصية للمستخدم (من 141 طبقة تحليلية): 
{user_analysis}

- وهذه التوصية السابقة التي لم تعجبه: 
{previous_recommendation}

- وهذه إجاباته الكاملة:
{user_text}

مهمتك:
- تحليل نية المستخدم وراء رفض التوصية.
- لا تكرر نفس الرياضة السابقة إطلاقًا.
- اربط بين إجابات المستخدم وتحليل شخصيته لتقديم توصية جديدة أعمق وأكثر تخصيصًا.
- برّر التوصية الجديدة بذكاء ووضّح كيف تعكس سماته الحقيقية.
"""

    user_prompt = "لم تعجبني الرياضة التي اقترحتها لي، أرغب بشيء أقرب لشخصيتي فعلاً."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.8
    )

    return response.choices[0].message.content.strip()