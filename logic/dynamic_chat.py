import json
import os
from openai import OpenAI
from logic.chat_personality import get_chat_personality

# إعداد العميل باستخدام openai 1.3.0
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# تحميل تحليل المستخدم من ملف user_analysis.json
def load_user_analysis():
    try:
        with open("data/user_analysis.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("summary", "")
    except:
        return ""

# المحادثة التفاعلية بعد رفض التوصية الأولى
def start_dynamic_chat(answers, previous_recommendation):
    user_analysis = load_user_analysis()
    personality = get_chat_personality("user")  # لا تحتاج ID لأن الملف ثابت حالياً

    tone = personality.get("tone", "محايد")
    style = personality.get("style", "تحليلي")
    philosophy = personality.get("philosophy", "")
    name = personality.get("name", "Sport Sync")

    user_text = '\n'.join([f"{k}: {v}" for k, v in answers.items()])

    system_prompt = f"""
أهلاً، أنا {name}.
أنا هنا لمساعدتك بناءً على تحليل شخصيتك الرياضية العميق. أسلوبي {style}، ونبرتي {tone}.
{philosophy}

هذا التحليل الكامل الذي تم بناؤه من 141 طبقة تحليلية:
{user_analysis}

وهذه كانت التوصية التي لم تعجبك:
{previous_recommendation}

وهذه إجاباتك الكاملة:
{user_text}

دعني أقدم لك اقتراحًا بديلًا مبنيًا على كل ما سبق، وبنبرة تناسب شخصيتك.
"""

    return system_prompt
