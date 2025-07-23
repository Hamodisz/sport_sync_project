# logic/dynamic_chat.py

import os
import json
import openai
from logic.backend_gpt import apply_all_analysis_layers
from logic.user_logger import log_user_insight
from logic.brand_signature import add_brand_signature

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# تعريف شخصية المدرب ديناميكيًا من المشروع
BASE_PERSONALITY = {
    "name": "Coach Sync",
    "tone": "عاطفي وتحفيزي",
    "style": "تحليلي وعميق",
    "philosophy": "أؤمن أن كل شخص يملك رياضة مخصصة له، ومهمتي مساعدته على اكتشافها بذكاء وشغف."
}

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
أنت {BASE_PERSONALITY['name']}، مدرب ذكي من مشروع Sports Sync.
نبرتك: {BASE_PERSONALITY['tone']} – أسلوبك: {BASE_PERSONALITY['style']}
فلسفتك: {BASE_PERSONALITY['philosophy']}
تحليلك يعتمد على طبقات نفسية (١ إلى ١٤١) تربط بين النية والسياق والتجربة.

🎯 مهمتك الآن:
1. تحليل سبب عدم رضا المستخدم عن التوصيات السابقة.
2. ربط إجاباته وسلوكه وتقييمه لاستخراج هويته العميقة.
3. تقديم توصية جديدة أعمق (من رياضة أو عدة رياضات مناسبة).
4. إذا شعرت أن هناك فجوة في الفهم، اطرح سؤالًا ذكيًا لاستكمال التحليل.

💡 لا تكرر أي رياضة ذُكرت سابقًا.
💡 إذا كانت الرياضة خطيرة أو صعبة الوصول، اقترح نسخة VR مناسبة.
💡 لا تبدو كآلة بل كمدرب يعرفه بذكاء.
        """
    else:
        system_prompt = f"""
You are {BASE_PERSONALITY['name']}, a smart coach from the Sports Sync project.
Tone: {BASE_PERSONALITY['tone']} – Style: {BASE_PERSONALITY['style']}
Philosophy: {BASE_PERSONALITY['philosophy']}
Your analysis is based on psychological layers (1–141), linking intention, context, and personal patterns.

🎯 Your mission:
1. Analyze why the user wasn’t satisfied with the previous recommendations.
2. Connect their answers, behavior, and ratings to extract their deeper identity.
3. Suggest a more tailored sport (or multiple) with strong emotional logic.
4. Ask a follow-up question if needed to enhance your understanding.

💡 Do not repeat any previously mentioned sport.
💡 Suggest VR alternatives for dangerous or inaccessible sports.
💡 Sound like a wise human coach, not a machine.
        """

    rating_text = ""
    if ratings:
        if lang == "العربية":
            rating_lines = [f"⭐ تقييم التوصية رقم {i+1}: {r}/10" for i, r in enumerate(ratings)]
        else:
            rating_lines = [f"⭐ Rating for recommendation {i+1}: {r}/10" for i, r in enumerate(ratings)]
        rating_text = "\n".join(rating_lines)

    user_prompt = f"""
📌 Previous Recommendations:
{previous_recommendation}

📋 User Answers:
{json.dumps(answers, ensure_ascii=False, indent=2)}

🧠 Full Trait Analysis (Layers 1–141):
{json.dumps(all_analysis, ensure_ascii=False, indent=2)}

{rating_text}

🔍 Task:
- Intelligently analyze why the user wasn't satisfied.
- Correlate each answer and trait to their core identity.
- Recommend an alternative sport (or more) in a smart, emotional way.
- If clarity is missing, ask a question and wait before continuing.

🎁 Make the recommendation feel like it was made just for them.
    """ if lang == "English" else f"""
📌 التوصيات السابقة:
{previous_recommendation}

📋 إجابات المستخدم:
{json.dumps(answers, ensure_ascii=False, indent=2)}

🧠 التحليل الكامل من الطبقات (1–141):
{json.dumps(all_analysis, ensure_ascii=False, indent=2)}

{rating_text}

🔍 المطلوب:
- حلل بذكاء سبب عدم الاقتناع.
- اربط بين كل إجابة وسمة وهوية داخلية للمستخدم.
- اقترح رياضة بديلة (أو أكثر) بأسلوب ذكي وعاطفي.
- إذا احتجت فهمًا أعمق، اطرح سؤالًا وانتظر منه إجابة لتكمل.

🎁 اجعل التوصية تشعره أنها صُممت له فقط.
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
