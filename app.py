# app.py

import streamlit as st
import json
import uuid
import pandas as pd
from datetime import datetime

from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat

# ---------------------
# تحميل الأسئلة
# ---------------------
def load_questions(lang):
    path = f"questions/{'arabic_questions.json' if lang == 'العربية' else 'english_questions.json'}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------------
# تخزين البيانات
# ---------------------
def save_user_data(user_id, lang, answers, recommendation, rating=None, liked=None):
    data = {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "language": lang,
        "answers": json.dumps(answers, ensure_ascii=False),
        "recommendation": recommendation,
        "rating": rating,
        "liked": liked
    }
    df = pd.DataFrame([data])
    df.to_csv("data/user_sessions.csv", mode="a", index=False, header=not pd.read_csv("data/user_sessions.csv").shape[0], encoding="utf-8")

# ---------------------
# واجهة المستخدم
# ---------------------
st.set_page_config(page_title="توصية رياضية", layout="centered")
st.title("🎯 توصيتك الرياضية الذكية")

# اختيار اللغة
lang = st.radio("اختر اللغة / Choose Language", ["العربية", "English"])
questions = load_questions(lang)
answers = {}
user_id = st.session_state.get("user_id", str(uuid.uuid4()))

# ---------------------
# عرض الأسئلة
# ---------------------
if "recommendations" not in st.session_state:
    for idx, q in enumerate(questions, 1):
        q_key = f"q{idx}"
        if q["type"] == "multiple":
            selected = st.multiselect(q["question"], q["options"], key=q_key)
            answers[q_key] = selected
        else:
            selected = st.radio(q["question"], q["options"], key=q_key)
            answers[q_key] = selected

        if q.get("free", False) or q.get("allow_custom", False):
            custom_input = st.text_input("📝 إجابة أخرى (اختياري):", key=f"{q_key}_custom")
            if custom_input:
                if isinstance(answers[q_key], list):
                    answers[q_key].append(custom_input)
                else:
                    answers[q_key] = [answers[q_key], custom_input]

    answers["custom_input"] = st.text_area("✏️ هل هناك شيء تحب إضافته؟", "")

    if st.button("🔍 احصل على توصيتي الرياضية"):
        with st.spinner("جاري تحليل إجاباتك..."):
            recommendations = generate_sport_recommendation(answers, lang)
            if not isinstance(recommendations, list):
                recommendations = [recommendations]

            st.session_state["recommendations"] = recommendations
            st.session_state["answers"] = answers
            st.session_state["user_id"] = user_id
            st.success("✅ تم إنشاء التوصيات!")

# ---------------------
# عرض التوصيات + التقييم + الشات
# ---------------------
if "recommendations" in st.session_state:
    ratings = []
    for i, rec in enumerate(st.session_state["recommendations"]):
        with st.expander(f"🎽 التوصية رقم {i+1}"):
            st.markdown(rec)
            rating = st.slider(f"ما مدى رضاك عن التوصية رقم {i+1}؟", 1, 10, 7, key=f"rating_{i}")
            ratings.append(rating)
            save_user_data(
                st.session_state["user_id"],
                lang,
                st.session_state["answers"],
                rec,
                rating=rating
            )

    if st.button("🔁 أريد توصية أعمق"):
        with st.spinner("نقوم بتحليل تقييماتك وإجاباتك لإعطاء توصية أذكى..."):
            deeper_response = start_dynamic_chat(
                answers=st.session_state["answers"],
                previous_recommendation="\n".join(st.session_state["recommendations"]),
                ratings=ratings,
                user_id=st.session_state["user_id"],
                lang=lang
            )
            st.markdown("### 💬 شات الذكاء الرياضي (Sports Sync AI Coach):")
            st.markdown(deeper_response)

# ---------------------
# روابط المشاركة
# ---------------------
st.markdown("---")
st.markdown(f"[🔗 رابط عام لمشاركة النتيجة](https://sport-sync.onrender.com/share/{user_id})")
st.markdown(f"[📨 دعوة صديق لتجربة الاختبار](https://sport-sync.onrender.com)")
