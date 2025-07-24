# app.py

import streamlit as st
import json
import uuid
import pandas as pd
import os
from datetime import datetime
from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat

# تحميل الأسئلة
def load_questions(lang):
    path = f"questions/{'arabic_questions.json' if lang == 'العربية' else 'english_questions.json'}"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# حفظ بيانات المستخدم
def save_user_data(user_id, lang, answers, recommendation, rating=None, liked=None):
    path = "data/user_sessions.csv"
    os.makedirs("data", exist_ok=True)
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
    try:
        file_exists = os.path.exists(path) and pd.read_csv(path).shape[0] > 0
    except pd.errors.EmptyDataError:
        file_exists = False
    df.to_csv(path, mode="a", index=False, header=not file_exists, encoding="utf-8")

# إعداد الصفحة
st.set_page_config(page_title="توصية رياضية", layout="centered")
st.title("🎯 توصيتك الرياضية الذكية")

lang = st.radio("اختر اللغة / Choose Language", ["العربية", "English"])
questions = load_questions(lang)
user_id = st.session_state.get("user_id", str(uuid.uuid4()))
answers = {}

# عرض الأسئلة
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

    answers["custom_input"] = st.text_area("✏ هل هناك شيء تحب إضافته؟", "")

    if st.button("🔍 احصل على توصيتي الرياضية"):
        with st.spinner("جاري تحليل إجاباتك..."):
            response = generate_sport_recommendation(answers, lang)
            if isinstance(response, str):
                recs = response.split("التوصية")
                recs = [f"التوصية {i+1} {r}".strip() for i, r in enumerate(recs) if r.strip()]
            else:
                recs = response

            st.session_state["recommendations"] = recs[:3]
            st.session_state["answers"] = answers
            st.session_state["user_id"] = user_id
            st.success("✅ تم إنشاء التوصيات!")

# عرض التوصيات والتقييم
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

    st.markdown("---")

    # المحادثة الديناميكية (شات)
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
        st.session_state.awaiting_response = False

    if st.button("🧠 أريد توصية أعمق (ابدأ المحادثة)"):
        with st.spinner("🔄 يتم تجهيز المحادثة..."):
            first_msg = start_dynamic_chat(
                answers=st.session_state["answers"],
                previous_recommendation="\n".join(st.session_state["recommendations"]),
                ratings=ratings,
                user_id=st.session_state["user_id"],
                lang=lang
            )
            st.session_state.chat_history.append(("assistant", first_msg))
            st.session_state.awaiting_response = True

    if st.session_state.get("chat_history"):
        st.markdown("## 💬 المحادثة مع مدرب الذكاء الرياضي")

        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"👤 *أنت:* {msg}")
            else:
                st.markdown(f"🤖 *المدرب:* {msg}")

        if st.session_state.awaiting_response:
            user_reply = st.text_input("✍ ردك على المدرب:")
            if user_reply:
                st.session_state.chat_history.append(("user", user_reply))
                with st.spinner("🧠 المدرب يفكر في الرد..."):
                    new_response = start_dynamic_chat(
                        answers=st.session_state["answers"],
                        previous_recommendation="\n".join(st.session_state["recommendations"]),
                        ratings=ratings,
                        user_id=st.session_state["user_id"],
                        lang=lang
                    )
                    st.session_state.chat_history.append(("assistant", new_response))

# روابط
st.markdown("---")
st.markdown(f"[🔗 رابط عام لمشاركة النتيجة](https://sport-sync.onrender.com/share/{user_id})")
st.markdown(f"[📨 دعوة صديق لتجربة الاختبار](https://sport-sync.onrender.com)")
