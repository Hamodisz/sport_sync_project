import json
import os

# تحميل تحليل الشخصية من ملف user_id_analysis.json
def load_user_analysis(user_id):
    path = f"data/{user_id}_analysis.json"
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("traits", [])

# توليد هوية الشات بناءً على التحليل
def get_chat_personality(user_id):
    traits = load_user_analysis(user_id)

    personality = {
        "name": "مساعد رياضي ذكي",
        "tone": "تحفيزي وعاكس لشخصية المستخدم",
        "style": "عميق وتحليلي ولكن إنساني",
        "philosophy": "الرياضة ليست مجرد نشاط، بل انعكاس لهويتك العميقة.",
        "traits_summary": traits,
    }

    # تخصيص أسلوب الشات حسب السمات
    if "يحب التحدي" in traits:
        personality["tone"] = "تنافسي ومُلهم"
    if "يميل للهدوء" in traits:
        personality["tone"] = "هادئ وواعٍ"
    if "يميل للمخاطرة" in traits:
        personality["tone"] = "جريء ومتحفز"
    if "مفكر" in traits:
        personality["style"] = "تحليلي وعقلي"
    if "مبدع" in traits:
        personality["style"] = "إبداعي وملهم"

    return personality

# ❗️يُستخدم هذا داخل واجهة Streamlit
chat_identity = {
    "name": "مساعد رياضي ذكي",
    "philosophy": "كل إنسان يملك رياضته الفريدة. مهمتي مساعدتك على اكتشافها.",
}