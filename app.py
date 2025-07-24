# app.py

import streamlit as st
from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat
from logic.memory_cache import get_cached_analysis
from logic.user_logger import log_user_insight

st.set_page_config(page_title="توصيتك الرياضية الذكية", layout="centered")

# -------------------------------------
# إعداد واجهة المستخدم
# -------------------------------------
st.markdown("<h1 style='text-align: center;'>🎯 توصيتك الرياضية الذكية</h1>", unsafe_allow_html=True)

lang = st.radio("🌐 اختر اللغة / Choose Language", ["العربية", "English"])
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_001"  # مؤقتًا

# -------------------------------------
# عرض التوصيات العادية (1 و 2)
# -------------------------------------
st.subheader("🌱 التوصية رقم 1")
if "recommendation_1" not in st.session_state:
    try:
        st.session_state.recommendation_1 = generate_sport_recommendation(
            st.session_state.answers, lang, method="standard"
        )
    except:
        st.session_state.recommendation_1 = "⚠ لم يتم العثور على توصية."

st.markdown(st.session_state.recommendation_1)

st.subheader("🌿 التوصية رقم 2")
if "recommendation_2" not in st.session_state:
    try:
        st.session_state.recommendation_2 = generate_sport_recommendation(
            st.session_state.answers, lang, method="alternative"
        )
    except:
        st.session_state.recommendation_2 = "⚠ لم يتم العثور على توصية."

st.markdown(st.session_state.recommendation_2)

# -------------------------------------
# قسم التوصية الأعمق - محادثة شات
# -------------------------------------
st.markdown("---")
st.markdown("## 🧠 تحدث مع الذكاء الرياضي")

# عرض المحادثة السابقة
for entry in st.session_state.chat_history:
    role, content = entry["role"], entry["content"]
    if role == "user":
        st.markdown(f"🧍‍♂ *أنت:* {content}", unsafe_allow_html=True)
    else:
        st.markdown(f"🤖 *Sports Sync:* {content}", unsafe_allow_html=True)

# إدخال المستخدم الجديد
user_input = st.chat_input("🗨 اكتب ردك أو اسأل أي سؤال...")

if user_input:
    # حفظ رسالة المستخدم
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    # تحليل سابق محفوظ
    analysis = get_cached_analysis(st.session_state.user_id)

    # استدعاء الذكاء لإكمال المحادثة
    reply = start_dynamic_chat(
        user_id=st.session_state.user_id,
        user_message=user_input,
        previous_chat=st.session_state.chat_history,
        analysis=analysis,
        answers=st.session_state.answers,
        lang=lang
    )

    # حفظ رد الذكاء
    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # حفظ التفاعل في سجل التوصيات
    log_user_insight(st.session_state.user_id, {
        "type": "chat_interaction",
        "user_message": user_input,
        "ai_reply": reply,
        "lang": lang,
        "full_chat": st.session_state.chat_history
    })

    st.rerun()
