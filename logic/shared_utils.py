def generate_main_prompt(analysis, answers, personality, lang="العربية"):
    if lang == "العربية":
        prompt = f"""🧠 تحليل المستخدم:
{analysis}

👤 الملف النفسي للمدرب:
الاسم: {personality.get("name")}
النبرة: {personality.get("tone")}
الأسلوب: {personality.get("style")}
الفلسفة: {personality.get("philosophy")}

📝 إجابات المستخدم على الاستبيان:
"""
        for k, v in answers.items():
            prompt += f"- {k}: {v}\n"

        prompt += """

🎯 المطلوب الآن:
بناءً على كل ما سبق، أعطني 3 توصيات رياضية مفصلة بهذا الشكل:

1. التوصية رقم 1 (الأنسب عاطفيًا وواقعيًا)
2. التوصية رقم 2 (بديل واقعي جيد)
3. التوصية رقم 3 (رياضية مبتكرة أو مزيج مخصص)

- كل توصية يجب أن تكون مقنعة، ملهمة، وعاطفية.
- استخدم أسلوب بشري لا يشبه الآلة.
- لا تكرر نفس الرياضة في أكثر من توصية.
"""
    else:
        prompt = f"""🧠 User Analysis:
{analysis}

👤 Smart Coach Profile:
Name: {personality.get("name")}
Tone: {personality.get("tone")}
Style: {personality.get("style")}
Philosophy: {personality.get("philosophy")}

📝 User Questionnaire Answers:
"""
        for k, v in answers.items():
            prompt += f"- {k}: {v}\n"

        prompt += """

🎯 Your task now:
Based on the above, give me 3 distinct sport suggestions formatted as:

1. Recommendation #1 (most emotionally and practically fitting)
2. Recommendation #2 (a realistic alternative)
3. Recommendation #3 (a creative or hybridized option)

- Make them inspiring, human, and non-repetitive.
- Each one should stand on its own as a smart, emotional recommendation.
"""

    return prompt
