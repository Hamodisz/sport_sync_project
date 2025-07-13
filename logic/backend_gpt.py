import os
import json
import openai

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141
from logic.chat_personality import chat_identity

# إعداد العميل باستخدام openai 1.3.0+
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# حفظ التحليل الكامل في ملف
def save_user_analysis(summary):
    os.makedirs("data", exist_ok=True)
    with open("data/user_analysis.json", "w", encoding="utf-8") as f:
        json.dump({"summary": summary}, f, ensure_ascii=False, indent=2)

# توليد التوصية الرياضية
def generate_sport_recommendation(answers, lang):
    user_text = " ".join(str(v) for v in answers.values())

    # تحليل السمات من الطبقات
    traits = []
    traits += apply_layers_1_40(user_text)
    traits += apply_layers_41_80(user_text)
    traits += apply_layers_81_100(user_text)
    traits += apply_layers_101_141(user_text)
    traits = list(set(traits))  # إزالة التكرار

    # بناء البرومبت الكامل
    system_prompt = f"""
أنت مساعد ذكي متخصص في تحليل الشخصية الرياضية.
مهمتك:
- تحليل إجابات المستخدم واستنتاج سماته النفسية والسلوكية.
- ثم اقتراح رياضة واحدة تناسبه بدقة وتعكس شخصيته.
- يجب أن تكون التوصية مبررة تحليليًا وبشكل فلسفي عميق.
- لا تعطه خيارات متعددة، بل رياضة واحدة فقط.
- لا تخترع اسم الرياضة، فقط صف طبيعتها.

السمات المستخرجة من التحليل:
{traits if traits else "لم يتم استخراج سمات واضحة."}

إجابات المستخدم:
{answers}
"""

    user_prompt = f"أنا أبحث عن رياضة تناسبني. لغتي: {lang}. أجب بناءً على شخصيتي."

    # طلب التوصية من GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt}
        ]
    )

    recommendation = response.choices[0].message.content.strip()

    # حفظ التحليل الكامل
    full_analysis = f"السمات: {traits}\n\nالإجابات:\n{answers}\n\nالتوصية: {recommendation}"
    save_user_analysis(full_analysis)

    return recommendation
