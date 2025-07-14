import openai
import os
import json

# إعداد العميل لمكتبة openai v1.3.0
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ----------------------------
# توليد التوصية الرياضية
# ----------------------------
def generate_sport_recommendation(answers, lang):
    if lang == "العربية":
        prompt = "هذه إجابات مستخدم على استبيان تحليل الشخصية والاهتمامات بهدف معرفة أنسب رياضة:\n\n"
    else:
        prompt = "These are a user's answers to a personality and interest questionnaire to find the best sport:\n\n"

    for i, ans in enumerate(answers, 1):
        prompt += f"{i}. {ans}\n"

    prompt += "\nBased on this, suggest the most suitable sport and justify why."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a professional sports psychologist and AI coach."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()


# ----------------------------
# تحليل جميع الطبقات (للاستخدام في الشات الديناميكي)
# ----------------------------
def apply_all_analysis_layers(answers):
    layers = {}

    # مثال على تحليل بسيط (يمكنك التوسيع لاحقًا)
    traits = []
    for a in answers:
        if any(word in a for word in ["خطر", "سرعة", "قتال", "مرتفعات", "adrenaline", "fight", "cliff", "extreme"]):
            traits.append("يميل للأدرينالين")
        if any(word in a for word in ["تفكير", "تركيز", "هدوء", "صمت", "استراتيجية", "شطرنج"]):
            traits.append("يميل للرياضات الذهنية")
        if any(word in a for word in ["جماعي", "فريق", "مجموعة", "تواصل"]):
            traits.append("يميل للرياضات الاجتماعية")
        if any(word in a for word in ["طبيعة", "خارج", "هواء", "جبل", "بحر"]):
            traits.append("يرتاح في البيئة الطبيعية")

    layers["layer_1_keywords"] = list(set(traits)) or ["لم يتم اكتشاف ميول واضحة بعد"]

    # يمكنك لاحقًا استدعاء طبقات من ملفات منفصلة هنا لو وسّعت النظام
    # layers.update(layer_2_intention(...))
    # layers.update(layer_3_conflict_detection(...))
    
    return layers
