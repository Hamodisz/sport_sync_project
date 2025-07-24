import streamlit as st
import json
import uuid
import os
import pandas as pd
from datetime import datetime

from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat

# إعداد الصفحة
st.set_page_config(page_title="توصية رياضية ذكية", layout="centered")
st.title("🤖 توصيتك الرياضية الشخصية")

# اختيار اللغة
lang = st.radio("🌍 اختر اللغة / Choose Language:", ["العربية", "English"])

# تحميل الأسئلة
def load_questions(lang):
    file = "arabic_questions.json" if lang == "العربية" else "english_questions.json"
    with open(f"questions/{file}", encoding="utf-8") as f:
        return json.load(f)

questions = load_questions(lang)
answers = {}
user_id = st.session_state.get("user_id", str(uuid.uuid4()))

# عرض الأسئلة
if "recommendations" not in st.session_state:
    for idx, q in enumerate(questions, 1):
        key = f"q{idx}"
        if q["type"] == "multiple":
            answers[key] = st.multiselect(q["question"], q["options"], key=key)
        else:
            answers[key] = st.radio(q["question"], q["options"], key=key)
        
        if q.get("free", False) or q.get("allow_custom", False):
            custom_input = st.text_input("📝 إجابة أخرى (اختياري):", key=f"{key}_custom")
            if custom_input:
                if isinstance(answers[key], list):
                    answers[key].append(custom_input)
                else:
                    answers[key] = [answers[key], custom_input]

    answers["custom_input"] = st.text_area("✏ هل هناك شيء تحب إضافته؟", "")

    if st.button("🎯 احصل على توصية رياضية"):
        with st.spinner("⏳ يتم تحليل إجاباتك..."):
            recs = generate_sport_recommendation(answers, lang)
            st.session_state["recommendations"] = recs
            st.session_state["answers"] = answers
            st.session_state["user_id"] = user_id
            st.session_state["chat_history"] = []
            st.success("✅ تم إنشاء توصيات ذكية!")

# عرض التوصيات + تقييمات + شات ديناميكي
if "recommendations" in st.session_state:
    st.markdown("## 🧠 توصياتك الذكية")
    ratings = []
    for i, rec in enumerate(st.session_state["recommendations"]):
        with st.expander(f"🎽 التوصية رقم {i+1}"):
            st.markdown(rec)
            rating = st.slider(f"ما رأيك في التوصية رقم {i+1}؟", 1, 10, 7, key=f"rate_{i}")
            ratings.append(rating)

    # زر بدء الشات الذكي
    st.markdown("---")
    st.markdown("## 💬 تحدث مع الذكاء الرياضي")
    if "chat_mode" not in st.session_state:
        if st.button("🔁 أريد توصية أعمق / شات تفاعلي"):
            st.session_state["chat_mode"] = True
            st.session_state["chat_history"] = []
            with st.spinner("🧠 يفكر الذكاء الرياضي في إجابة مخصصة لك..."):
                first_msg = start_dynamic_chat(
                    answers=st.session_state["answers"],
                    previous_recommendation="\n".join(st.session_state["recommendations"]),
                    ratings=ratings,
                    user_id=st.session_state["user_id"],
                    lang=lang
                )
                st.session_state["chat_history"].append({"role": "assistant", "content": first_msg})
    
    # عرض سجل المحادثة (الشات الفعلي)
    if "chat_mode" in st.session_state:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"*أنت:* {msg['content']}")
            else:
                st.markdown(f"*Sports Sync:* {msg['content']}")

        user_input = st.text_input("✏ ردك:", key="user_reply")
        if st.button("📩 إرسال الرد"):
            if user_input:
                st.session_state["chat_history"].append({"role": "user", "content": user_input})

                # بناء الحوار الكامل كمحادثة
                history = [{"role": m["role"], "content": m["content"]} for m in st.session_state["chat_history"]]

                with st.spinner("🤖 يكتب لك ردًا..."):
                    import openai
                    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=history,
                        temperature=0.9
                    )
                    reply = response.choices[0].message.content.strip()
                    st.session_state["chat_history"].append({"role": "assistant", "content": reply})
                    st.experimental_rerun()

# رابط المشاركة
st.markdown("---")
st.markdown(f"📤 شارك تجربتك: [sports-sync.onrender.com/share/{user_id}](https://sports-sync.onrender.com/share/{user_id})")
