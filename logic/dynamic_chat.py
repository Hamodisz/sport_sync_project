import os
from openai import OpenAI

# إعداد العميل من openai 1.30.1
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# الدالة الرئيسية للدردشة الذكية
def start_dynamic_chat(user_message, previous_context=[]):
    messages = []

    # مقدمة النظام لتحديد أسلوب الشات
    system_message = {
        "role": "system",
        "content": (
            "أنت مستشار ذكي في تحديد الرياضة المناسبة بناءً على تحليل الشخصية. "
            "يجب أن تكون متفهمًا، عميق التحليل، وتستخدم السياق الكامل لفهم نية المستخدم. "
            "إذا عبّر المستخدم عن عدم رضاه عن التوصية السابقة، اربط بين إجاباته الأصلية وتحليلك الحالي، "
            "وقدّم بديلًا منطقيًا ومقنعًا مع تفسير أعمق."
        )
    }

    messages.append(system_message)

    # إضافة السياق السابق إن وجد
    for msg in previous_context:
        messages.append({"role": msg["role"], "content": msg["content"]})

    # إضافة رسالة المستخدم الأخيرة
    messages.append({"role": "user", "content": user_message})

    # إرسال المحادثة إلى GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.75,
    )

    reply = response.choices[0].message.content.strip()
    return reply
