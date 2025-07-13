import json
import os

# تحميل تحليل الشخصية من ملف user_analysis.json داخل مجلد data
def load_user_analysis():
    path = "data/user_analysis.json"
    if not os.path.exists(path):
        return []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("detected_traits", [])

# توليد هوية الشات بناءً على تحليل المستخدم
def get_chat_personality():
    traits = load_user_analysis()

    personality = {
        "name": "Sport Sync",
        "tone": "يعكس حالتك النفسية ويخاطبك بأسلوب مناسب",
        "style": "عميق وتحليلي لكن إنساني ومرن",
        "philosophy": "الرياضة انعكاس لهويتك، وليست مجرد نشاط جسدي. مهمتي مساعدتك على اكتشاف رياضتك الحقيقية.",
        "traits_summary": traits,
    }

    # تخصيص الأسلوب بناءً على السمات
    if "يحب التحدي" in traits:
        personality["tone"] = "تنافسي ومُلهم"
    if "يميل للهدوء" in traits:
        personality["tone"] = "واعي ومتزن"
    if "يميل للمخاطرة" in traits:
        personality["tone"] = "جريء ومشعل للحماس"
    if "مفكر" in traits:
        personality["style"] = "تحليلي وعقلي"
    if "مبدع" in traits:
        personality["style"] = "إبداعي ومُلهم"

    return personality

# هوية الشات الأساسية تُستخدم عند الحاجة العامة (في البداية)
chat_identity = {
    "name": "Sport Sync",
    "philosophy": "كل شخص لديه رياضته الفريدة... وأنا هنا لأساعدك على اكتشافها.",
}
