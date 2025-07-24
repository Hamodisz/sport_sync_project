# app.py

import streamlit as st
import json
import uuid
import os
from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import continue_dynamic_chat
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="🎯 توصيتك الرياضية الذكية", layout="centered")
st.title("🎯 توصيتك الرياضية الذكية")

# اختيار اللغة
lang = st.radio("اختر اللغة / Choose Language", ["العربية", "English"])
path = f"questions/{'arabic_questions.json' if lang == 'العربية' else 'english_questions.json'}"
with open(path, "r", encoding="utf-8") as f:
    questions = json.load(f)

answers = {}
user_id = st.session_state.get("user_id", str(uuid.uuid4()))

# ---------------
# إعادة الاختبار
# ---------------
if st.button("🔄 أعد الاختبار من البداية"):
    st.session_state.clear()
    st.experimental_rerun()

# ---------------
# عرض الأسئلة
# ---------------
if "recommendations" not in st.session_state:
    for idx, q in enumerate(questions, 1):
        key = f"q{idx}"
        if q["type"] == "multiple":
            answers[key] = st.multiselect(q["question"], q["options"], key=key)
        else:
            answers[key] = st.radio(q["question"], q["options"], key=key)

        if q.get("allow_custom", False):
            custom = st.text_input("📝 إجابة أخرى (اختياري):", key=f"{key}_custom")
            if custom:
                if isinstance(answers[key], list):
                    answers[key].append(custom)
                else:
                    answers[key] = [answers[key], custom]

    answers["custom_input"] = st.text_area("✏ هل لديك شيء إضافي؟", "")

    if st.button("🔍 احصل على التوصية"):
        with st.spinner("جارٍ التحليل..."):
            recs = generate_sport_recommendation(answers, lang)
            st.session_state["recommendations"] = recs
            st.session_state["answers"] = answers
            st.session_state["user_id"] = user_id
            st.success("✅ تم توليد التوصيات!")

# ---------------
# عرض التوصيات
# ---------------
if "recommendations" in st.session_state:
    st.markdown("## 🏅 توصياتك الرياضية:")
    for i, rec in enumerate(st.session_state["recommendations"]):
        st.markdown(f"*التوصية {i+1}:*\n\n{rec}")

    st.markdown("---")
    st.markdown("### 💬 دردش مع مدرب الذكاء الرياضي")

    if "chat_history" not in st.session_state:
        # أول رسالة يتم إرسالها: نبدأ المحادثة مع الإجابات
        st.session_state["chat_history"] = [{
            "role": "user",
            "content": f"ابدأ تحليل عميق بناءً على الإجابات: answers={str(st.session_state['answers'])}"
        }]

    # عرض المحادثة
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"👤 *أنت*: {msg['content']}")
        else:
            st.markdown(f"🧠 *Sports Sync*: {msg['content']}")

    # إدخال المستخدم
    user_input = st.text_input("💬 أرسل رسالة إلى مدرب الذكاء:", key="user_input")
    if st.button("📨 إرسال"):
        if user_input.strip():
            st.session_state["chat_history"].append({"role": "user", "content": user_input})
            with st.spinner("🧠 Sports Sync يجيب..."):
                reply, updated_history = continue_dynamic_chat(
                    messages=st.session_state["chat_history"],
                    user_id=st.session_state["user_id"],
                    lang=lang
                )
                st.session_state["chat_history"] = updated_history
                st.experimental_rerun()
