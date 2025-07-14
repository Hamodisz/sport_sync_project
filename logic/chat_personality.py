import random
import json
import os

def get_chat_personality(user_id):
    # تحميل تحليل السمات من ملف التحليل المحفوظ
    file_path = f"data/{user_id}_analysis.json"
    if not os.path.exists(file_path):
        return default_personality()

    with open(file_path, "r", encoding="utf-8") as f:
        traits = json.load(f)

    # توليد ملخص السمات لاستخدامه في البرومبت
    traits_summary = [trait for trait in traits]

    return {
        "name": random.choice(["نورا", "مالك", "ليلى", "آدم", "سارة"]),
        "tone": random.choice(["هادئة ومتفهمة", "تحفيزية ومليئة بالطاقة", "عقلانية وواقعية"]),
        "style": random.choice(["أسلوب عميق فلسفي", "أسلوب مباشر وواضح", "أسلوب قصصي وتخيّلي"]),
        "philosophy": "الرياضة ليست هدفًا، بل وسيلة لاكتشاف الذات والتعبير عنها.",
        "traits_summary": traits_summary[:10]  # نختصر لأفضل 10 سمات لتحسين البرومبت
    }

def default_personality():
    return {
        "name": "آدم",
        "tone": "واقعية وتحليلية",
        "style": "أسلوب مباشر وواضح",
        "philosophy": "نساعد كل شخص يكتشف رياضته الخاصة عبر تحليل نواياه العميقة.",
        "traits_summary": ["لا يوجد تحليل سابق"]
    }
