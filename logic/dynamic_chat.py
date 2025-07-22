import os
import json
import openai

from logic.backend_gpt import apply_all_analysis_layers
from logic.chat_personality import get_chat_personality
from logic.user_analysis import save_user_analysis
from logic.user_logger import log_user_insight
from logic.brand_signature import add_brand_signature

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id, lang="العربية", ratings=None):
    if lang not in ["العربية", "English"]:
        lang = "English"

    # تحويل الإجابات إلى نص واحد
    full_text = ' '.join(
        ' / '.join(v) if isinstance(v, list) else str(v)
        for v in answers.values()
    )

    # تحليل الإجابات
    analysis = apply_all_analysis_layers(full_text)
    save_user_analysis(user_id, analysis)

    # حفظ اللغة والسمات للذكاء المستمر
    log_user_insight(user_id, {
        "lang": lang,
        "traits": analysis
    })

    # تقييم التوصيات السابقة
    rating_text = ""
    if ratings:
        rating_lines = [f"⭐ تقييم التوصية رقم {i+1}: {r}/10" for i, r in enumerate(ratings)]
        rating_text = "\n".join(rating_lines)

    # استخراج شخصية المدرب
    personality = get_chat_personality(user_id)

    # تجهيز البرومبت
    if lang == "العربية":
        system_prompt = f"""
أنت {personality['name']}، مدرب ذكي من فريق Sport Sync.
نبرتك: {personality['tone']} – أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
تحليلك يعتمد على طبقات نفسية من 1 إلى 141.

🎯 مهمتك:
1. تحليل سبب عدم رضا المستخدم عن التوصيات السابقة.
2. فهم شخصيته ونيته الحقيقية من خلال التقييمات والإجابات.
3. اقتراح رياضة (أو أكثر) بديلة أعمق تعبر عنه.
4. إذا شعرت أن هناك فجوة، اسأله سؤال واحد ذكي.

💡 لا تكرر رياضة ذُكرت سابقًا.
💡 إذا كانت الرياضة نادرة أو خطيرة، اقترح نسخة VR منها.
💡 اجعل الرد إنساني وعاطفي.
"""
    else:
        system_prompt = f"""
You are {personality['name']}, a smart coach from the Sport Sync team.
Tone: {personality['tone']} – Style: {personality['style']}
Philosophy: {personality['philosophy']}
You analyze using 141 psychological layers and trait-based reasoning.

🎯 Your task:
1. Analyze why the previous suggestions didn't work.
2. Understand the user's deeper intent from their answers and ratings.
3. Recommend an alternative (real or VR) that fits them better.
4. If needed, ask one smart follow-up question.

💡 Don't repeat any previous sport.
💡 Be emotional, insightful, and human.
"""

    user_prompt = f"""
📌 التوصيات السابقة:
{previous_recommendation}

📋 إجابات المستخدم:
{json.dumps(answers, ensure_ascii=False, indent=2)}

🧠 التحليل الكامل:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

{rating_text}

🔍 المطلوب:
- حلل سبب عدم رضا المستخدم.
- استخرج عمق شخصيته.
- اقترح رياضة بديلة تشعره بأنها له فقط.
- إذا احتجت، اسأله سؤالًا واحدًا لتعميق الفهم.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()}
            ]
        )
        return add_brand_signature(response.choices[0].message.content.strip())
    except Exception as e:
        return f"❌ حدث خطأ أثناء الاتصال بـ GPT: {str(e)}"
