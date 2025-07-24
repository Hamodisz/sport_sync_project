# logic/shared_utils.py

def build_main_prompt(analysis, answers, personality, previous_recommendation, ratings, lang="العربية"):
    if lang == "العربية":
        prompt = f"""👤 *تحليل شخصية المستخدم*:
{analysis}

🧠 *ملف المدرب الذكي*:
الاسم: {personality.get("name")}
النبرة: {personality.get("tone")}
الأسلوب: {personality.get("style")}
الفلسفة: {personality.get("philosophy")}

📝 *إجابات المستخدم*:
"""
        for k, v in answers.items():
            prompt += f"- {k}: {v}\n"

        prompt += f"""

📊 *تقييم المستخدم للتوصيات السابقة*:
{ratings}

📌 *التوصية السابقة التي قُدمت له*:
{previous_recommendation}

🎯 المطلوب الآن:
بناءً على كل ما سبق، اعطني توصية أعمق وأصدق. لا تكرر نفس التوصيات، ولا تذكر الرياضات الثلاثة السابقة. وجهه إلى شيء يلائم أعماقه ويحفز روحه. إذا لم تكن هناك رياضة حقيقية تناسبه، يمكنك اختراع أو دمج رياضة جديدة خصيصًا له.

- استخدم أسلوب إنساني، عاطفي، وغير مباشر.
- يجب أن تكون التوصية ذكية، واقعية، ومقنعة.
"""

    else:
        prompt = f"""👤 *User Personality Analysis*:
{analysis}

🧠 *Smart Coach Profile*:
Name: {personality.get("name")}
Tone: {personality.get("tone")}
Style: {personality.get("style")}
Philosophy: {personality.get("philosophy")}

📝 *User's Questionnaire Answers*:
"""
        for k, v in answers.items():
            prompt += f"- {k}: {v}\n"

        prompt += f"""

📊 *User's Ratings on Previous Recommendations*:
{ratings}

📌 *Previous Recommendation Given*:
{previous_recommendation}

🎯 Your task now:
Based on everything above, give a deeper, more meaningful sport suggestion.
Avoid repeating the same previous three recommendations.
If no real sport fits them perfectly, invent or hybridize one that does.

- Be emotionally intelligent and human.
- Make it realistic, innovative, and inspiring.
"""

    return prompt
