import openai
import os
import json

from logic.backend_gpt import apply_all_analysis_layers
from logic.chat_personality import get_chat_personality
from logic.user_analysis import save_user_analysis
from logic.brand_signature import append_brand_signature
from logic.insights_log import log_insight

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def start_dynamic_chat(answers, previous_recommendation, user_id, lang="العربية", ratings=None):
    if lang not in ["العربية", "English"]:
        lang = "English"

    full_text = ' '.join(
        ' / '.join(v) if isinstance(v, list) else str(v)
        for v in answers.values()
    )

    all_analysis = apply_all_analysis_layers(full_text)
    all_analysis["language"] = lang  # 🧠 حفظ اللغة المفضلة
    save_user_analysis(user_id, all_analysis)

    rating_text = ""
    if ratings:
        rating_lines = [f"⭐ تقييم التوصية رقم {i+1}: {r}/10" for i, r in enumerate(ratings)]
        rating_text = "\n".join(rating_lines)

    personality = get_chat_personality(user_id)

    if lang == "العربية":
        system_prompt = f"""
أنت {personality['name']}، مدرب ذكي تابع لفلسفة Sport Sync.
نبرتك: {personality['tone']} – أسلوبك: {personality['style']}
فلسفتك: {personality['philosophy']}
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
You are {personality['name']}, a Sport Sync smart coach.
Tone: {personality['tone']} – Style: {personality['style']}
Philosophy: {personality['philosophy']}
Your analysis uses layered interpretation (1–141), intent, and personal context.

🎯 Your mission:
1. Understand why the previous recommendations didn’t resonate.
2. Extract the user's deeper personality and intentions.
3. Suggest better-fitting sports (real or VR version if inaccessible).
4. If needed, ask 1–3 smart follow-up questions.

💡 Never repeat previous sports.
💡 Be personal, insightful, and emotionally intelligent.
        """

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

        final_reply = response.choices[0].message.content.strip()

        # 🔁 تسجيل الإنسايت للتعلم المستمر
        log_insight("dynamic_chat_response", user_id, {
            "lang": lang,
            "answers": answers,
            "analysis": all_analysis,
            "previous_recommendation": previous_recommendation,
            "ratings": ratings,
            "final_reply": final_reply
        })

        return add_brand_signature(final_reply)

    except Exception as e:
        return f"❌ حدث خطأ أثناء الاتصال بـ GPT: {str(e)}"
