import os
import json
import openai

from logic.analysis_layers_1_40 import apply_layers_1_40
from logic.analysis_layers_41_80 import apply_layers_41_80
from logic.analysis_layers_81_100 import apply_layers_81_100
from logic.analysis_layers_101_141 import apply_layers_101_141

# إعداد العميل باستخدام openai 1.3.0+
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# حفظ التحليل في ملف بناءً على user_id
def save_user_analysis(user_id, traits, answers, recommendation):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{user_id}_analysis.json", "w", encoding="utf-8") as f:
        json.dump({
            "traits": traits,
            "summary": f"السمات: {traits}\n\nالإجابات:\n{answers}\n\nالتوصية: {recommendation}"
        }, f, ensure_ascii=False, indent=2)

# توليد التوصية الرياضية
def generate_sport_recommendation(answers, lang, user_id):
    user_text = " ".join(str(v) for v in answers.values())

    # تحليل السمات من جميع الطبقات
    traits = list(set(
        apply_layers_1_40(user_text)
        + apply_layers_41_80(user_text)
        + apply_layers_81_100(user_text)
        + apply_layers_101_141(user_text)
    ))

    # بناء البرومبت
    system_prompt = f"""
أنت مساعد ذكي من Sport Sync.
مهمتك:
- تحليل إجابات المستخدم.
- استنتاج سماته النفسية.
- اقتراح رياضة واحدة تناسبه تمامًا.
- يجب أن تكون التوصية مبررة بعمق فلسفي.

السمات المستخرجة:
{traits if traits else "لم يتم استخراج سمات واضحة."}

إجابات المستخدم:
{answers}
    """.strip()

    user_prompt = f"أريد رياضة تناسب شخصيتي. اللغة: {lang}."

    # إرسال للذكاء الاصطناعي
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    recommendation = response.choices[0].message.content.strip()

    # حفظ التحليل
    save_user_analysis(user_id, traits, answers, recommendation)

    return recommendation
