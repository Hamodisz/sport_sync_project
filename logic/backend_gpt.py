def generate_sport_recommendation(answers, lang="العربية"):
    # تأمين النص الكامل من الإجابات
    parts = []
    for i in range(20):
        val = answers.get(f'q{i+1}', '')
        if isinstance(val, list):
            parts.append(' / '.join(val))
        else:
            parts.append(str(val))
    full_text = ' '.join(parts) + ' ' + answers.get("custom_input", "")

    # استخراج التحليل
    analysis = apply_all_analysis_layers(full_text)
    user_id = answers.get("user_id", "unknown")

    # حفظ التحليل
    save_user_analysis(user_id, analysis)

    # تجهيز البرومبت
    if lang == "العربية":
        prompt = f"""
أنت نظام ذكي لتحليل الشخصية الرياضية. المستخدم أجاب على استبيان طويل، وهذه السمات التي استنتجتها من تحليله:

🔍 السمات النفسية والسلوكية:
{json.dumps(analysis, ensure_ascii=False, indent=2)}

🎯 مهمتك:
اقترح 3 رياضات مختلفة تمامًا لهذا المستخدم، بأسلوب إنساني عاطفي يحاكي مشاعره ويعكس شخصيته بصدق. 
ابدأ كل توصية بسبب مقنع جدًا مبني على واحدة من سماته، ثم اربط الرياضة المختارة بتلك السمة بذكاء.
إذا كانت الرياضة نادرة أو خطيرة أو صعبة الوصول، اقترح نسخة VR منها كبديل واقعي وذكي.
فكّر بشكل إبداعي ولا تلتزم بالرياضات التقليدية فقط. لا تُكرر رياضات متشابهة. اجعل كل توصية مميزة ومستقلة تمامًا.

✅ في نهاية الرسالة، أضف هذه الجملة:
"وإن شعرت أن هذه الرياضات لا تعبر عنك تمامًا، اضغط على زر (لم تعجبني التوصية) لأتعرف عليك أكثر، وأبحث لك عن ما يناسبك فعلًا."

📌 أجب فقط بهذا الشكل، دون أي مقدمات إضافية:
1. اسم الرياضة – السبب
2. ...
3. ...
        """
    else:
        prompt = f"""
You are an intelligent sport personality analyzer. The user completed a deep survey. These are the traits you extracted:

🧠 Traits:
{json.dumps(analysis, indent=2)}

🎯 Your task:
Suggest 3 completely different sports based on the user's personality.
Each recommendation must:
- Start with a deeply personal reason based on the user's traits.
- Clearly explain why this sport is a great fit.
- If the sport is rare, dangerous, or hard to access, suggest a VR alternative.
Be creative and emotionally expressive. Don’t just give popular or cliché sports. Each recommendation should feel custom-made.

✅ End with this:
"If you feel these don’t truly reflect who you are, click 'Not satisfied' and I’ll explore more to find what truly fits you."

📌 Format your answer like this:
1. Sport – explanation
2. ...
3. ...
        """

    # إرسال الطلب والتعامل مع الخطأ
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt.strip()}],
            temperature=0.85,
        )
        content = response.choices[0].message.content.strip()
    except Exception as e:
        print("❌ خطأ أثناء الاتصال بـ OpenAI:", str(e))
        return ["عذرًا، حدث خطأ أثناء توليد التوصية. يرجى المحاولة لاحقًا."]

    # تقسيم التوصيات
    recommendations = []
    for line in content.split("\n"):
        if line.strip().startswith(("1.", "2.", "3.")):
            recommendations.append(line.strip())

    # Fallback
    if len(recommendations) < 3:
        recommendations = [content]

    return recommendations
