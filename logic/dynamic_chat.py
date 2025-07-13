import openai
import os
from logic.chat_personality import get_chat_personality

# إعداد العميل
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# الشات التفاعلي بعد "لم تعجبني التوصية"
def start_dynamic_chat(answers, previous_recommendation, user_id="default"):
    user_text = " ".join(str(v) for v in answers.values())
    traits_text = f"بعض السمات المستنتجة: {user_text[:400]}..."

    # تحميل شخصية الشات
    persona = get_chat_personality(user_id)
    name = persona.get("name", "Sport Sync")
    tone = persona.get("tone", "تحفيزي")
    style = persona.get("style", "تحليلي وإنساني")
    philosophy = persona.get("philosophy", "الرياضة مرآة للهوية.")
    traits_summary = ", ".join(persona.get("traits_summary", []))

    system_prompt = f"""
أنت الآن تتحدث باسم شخصية افتراضية اسمها "{name}".
أسلوبك: {style}، نبرتك: {tone}.
فلسفتك: "{philosophy}".

- اجعل ردك تحليليًا ومرتبطًا بشخصية المستخدم.
- اربط بين ما اختاره من إجابات وبين التوصية السابقة.
- لا تكرر نفس الرياضة، واقترح شيئًا أعمق يناسب شخصيته الفعلية.
- استعمل نبرة إنسانية، وتحدث كأنك تعرف المستخدم جيدًا.
- هذه سمات المستخدم المستنتجة: {traits_summary}
- هذه إجاباته: {answers}
- وهذه كانت التوصية السابقة: {previous_recommendation}
"""

    user_prompt = "لم تعجبني التوصية السابقة. أرغب بتحليل أعمق وتوصية بديلة توضح لي من أنا رياضيًا."

    # توليد الرد
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt}
        ]
    )

    return response.choices[0].message.content.strip()
