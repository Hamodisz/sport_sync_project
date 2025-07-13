import streamlit as st
import json
import uuid
import pandas as pd
from datetime import datetime

from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat
from logic.chat_personality import chat_identity

# ---------------------
# تحميل الأسئلة
# ---------------------
def load_questions(lang):
    path = f"questions/{'arabic_questions.json' if lang == 'العربية' else 'english_questions.json'}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------
# حفظ الجلسة
# ---------------------
def store_user_session(user_id, answers, recommendation, lang):
    row = {
        "user_id": user_id,
        "timestamp": datetime.now(),
        "language": lang,
        "answers": json.dumps(answers, ensure_ascii=False),
        "recommendation": recommendation
    }
    df = pd.DataFrame([row])
    df.to_csv("data/user_data.csv", mode="a", index=False, header=False, encoding="utf-8")

# ---------------------
# واجهة المستخدم
# ---------------------
st.set_page_config(page_title="🔍 توصية رياضية ذكية", layout="centered")
st.title("🎯 نظام التوصية الرياضية الذكية")

# اختيار اللغة
lang = st.radio("اختر اللغة / Choose Language", ["العربية", "English"])
questions = load_questions(lang)

# تهيئة المتغيرات
answers = {}
user_id = str(uuid.uuid4())[:8]

# عرض الأسئلة
for q in questions:
    question = q["question"]
    options = q["options"]
    multi = q.get("multi", False)
    allow_free = q.get("free", False)

    if multi:
        selected = st.multiselect(question, options, key=question)
    else:
        selected = st.selectbox(question, options, key=question)

    # خانة الإجابة الحرة
    other = st.text_input(f"{question} (إجابة حرة)", key=question + "_free") if allow_free else ""

    if other:
        if isinstance(selected, list):
            selected.append(other)
        else:
            selected = f"{selected}, {other}"

    answers[question] = selected

# ---------------------
# توليد التوصية
# ---------------------
if st.button("🔎 احصل على توصيتك"):
    with st.spinner("جاري التحليل..."):
        recommendation = generate_sport_recommendation(answers, lang)
        store_user_session(user_id, answers, recommendation, lang)
        st.success("✨ هذه هي الرياضة الأنسب لك:")
        st.write(recommendation)

        # زر نسخ
        st.code(recommendation, language=None)
        st.button("📋 نسخ التوصية", on_click=st.toast, args=("✅ تم نسخ التوصية",))

        # رابط مشاركة
        share_url = f"https://your-app-url.com/?user={user_id}"
        st.markdown(f"🔗 رابط المشاركة: `{share_url}`")

        # دعوة صديق
        if st.button("📨 دعوة صديق"):
            st.markdown("انسخ الرابط وشاركه مع صديقك ليجرب: https://your-app-url.com")

        # زر لم تعجبني التوصية
        if st.button("🤔 لم أقتنع بالنتيجة"):
            with st.spinner("جاري إعادة التحليل بناءً على إجاباتك وتحليل شخصيتك..."):
                followup = start_dynamic_chat(answers, recommendation)
                st.subheader("🔁 تحليل أعمق:")
                st.write(followup)

# ---------------------
# عرض التحليل الجانبي
# ---------------------
try:
    with open("data/user_analysis.json", "r", encoding="utf-8") as f:
        user_analysis = json.load(f)
        st.sidebar.markdown("🧠 تحليل شخصيتك:")
        st.sidebar.write(user_analysis.get("summary", ""))
except:
    pass
