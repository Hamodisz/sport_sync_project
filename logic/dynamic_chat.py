# logic/dynamic_chat.py

import os
import json
import openai
from logic.backend_gpt import apply_all_analysis_layers
from logic.chat_personality_static import BASE_PERSONALITY
from logic.user_logger import log_user_insight
from logic.brand_signature import add_brand_signature

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id, lang="العربية", ratings=None):
    if lang not in ["العربية", "English"]:
        lang = "English"

    # إعداد النص الكامل للإجابات
    full_text = ' '.join(
        ' / '.join(v) if isinstance(v, list) else str(v)
        for v in answers.values()
    )

    # التحليل الكامل
    all_analysis = apply_all_analysis_layers(full_text)

    # حفظ السمات واللغة في سجل التعلم
    log_user_insight(user_id, {
        "lang": lang,
        "traits": all_analysis,
        "personality": BASE_PERSONALITY
    })

    # بناء برومبت الشخصية
    if lang == "العربية":
        system_prompt = f"""
أنت {BASE_PERSONALITY['name']}، مدرب ذكي تابع لفلسفة Sports Sync.
نبرتك: {BASE_PERSONALITY['tone']} – أسلوبك: {BASE_PERSONALITY['style']}
فلسفتك: {BASE_PERSONALITY['philosophy']}
تحليلك يعتمد على طبقات نفسية (١ إلى ١٤١) تربط بين النية والسياق والتجربة.

🎯 مهمتك الآن:
1. تحليل سبب عدم رضا المستخدم عن التوصيات السابقة.
2. ربط إجاباته وسلوكه وتقييمه لاستخراج هويته العميقة.
3. تقديم توصية جديدة أعمق (من رياضة أو عدة رياضات مناسبة).
4. إذا شعرت أن هناك فجوة في الفهم، اطرح سؤال أو أكثر لتقوية التوصية.

💡 لا تكرر أي رياضة ذكرت سابقًا.
💡 إذا كانت الرياضة خطيرة أو صعبة الوصول، اقترح نسخة VR مناسبة.
💡 لا تبدو كآلة بل كمدرب يعرفه بذكاء.
        """
    else:
        system_prompt = f"""
You are {BASE_PERSONALITY['name']}, a smart coach from Sports Sync philosophy.
Tone: {BASE_PERSONALITY['tone']} – Style: {BASE_PERSONALITY['style']}
Philosophy: {BASE_PERSONALITY['philosophy']}
Your analysis is based on psychological layers (1–141), connecting intention, context, and personality.

🎯 Your mission:
1. Analyze why the previous recommendations were unsatisfying.
2. Use answers and ratings to uncover the user's deeper identity.
3. Suggest new, more fitting sports (real or VR alternative).
4. Ask follow-up questions if needed to refine the recommendation.

💡 Do not repeat previous sports.
💡 Suggest VR versions for inaccessible or extreme sports.
💡 Respond like a wise human coach, not a machine.
        """

    rating_text = ""
    if ratings:
        rating_lines = [f"⭐ تقييم التوصية رقم {i+1}: {r}/10" for i, r in enumerate(ratings)]
        rating_text = "\n".join(rating_lines)

    user_prompt = f"""
📌 التوصيات السابقة:
{previous_recommendation}

📋 إجابات المستخدم:
{json.dumps(answers, ensure_ascii=False, indent=2)}

🧠 التحليل الكامل من الطبقات (1–141):
{json.dumps(all_analysis, ensure_ascii=False, indent=2)}

{rating_text}

🔍 المطلوب:
- حلل بذكاء سبب عدم الاقتناع.
- اربط بين كل إجابة وتقييم وتحليل لهوية المستخدم.
- اقترح رياضة بديلة (أو أكثر) بأسلوب ذكي وعاطفي.
- إذا احتجت فهمًا أعمق، اسأله الآن ثم انتظر إجابته لتكمل.

🎁 اجعل التوصية تشعره أنها صنعت له فقط.
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
