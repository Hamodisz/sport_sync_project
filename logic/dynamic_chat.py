import openai
import os
import json
from logic.backend_gpt import apply_all_analysis_layers
from logic.chat_personality import get_chat_personality

# إعداد عميل OpenAI
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# دالة المحادثة الذكية بعد زر "لم تعجبني التوصية"
def start_dynamic_chat(answers, previous_recommendation, user_id, lang="العربية", ratings=None):
    personality = get_chat_personality(user_id)
    all_analysis = apply_all_analysis_layers(answers)

    # تقييم التوصيات السابقة
    rating_text = ""
    if ratings:
        rating_lines = [f"⭐ تقييم التوصية رقم {i+1}: {r}/10" for i, r in enumerate(ratings)]
        rating_text = "\n".join(rating_lines)

    # رسالة النظام (System Prompt)
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

    # برومبت المستخدم
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

    # إرسال الطلب إلى GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()}
        ]
    )

    return response.choices[0].message.content.strip()
