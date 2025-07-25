import streamlit as st
import json
from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat
from logic.memory_cache import get_cached_analysis
from logic.user_logger import log_user_insight

# إعداد الصفحة
st.set_page_config(page_title="توصيتك الرياضية الذكية", layout="centered")

# اختيار اللغة
lang = st.radio("🌐 اختر اللغة / Choose Language", ["العربية", "English"])

# تهيئة الحالة
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_001"
if "ratings" not in st.session_state:
    st.session_state.ratings = {}

# -------------------------------
# عرض الأسئلة
# -------------------------------
if not st.session_state.answers:
    st.markdown("## 📝 " + ("الأسئلة التحليلية" if lang == "العربية" else "Personality Questionnaire"))

    question_file = "questions/arabic_questions.json" if lang == "العربية" else "questions/english_questions.json"
    with open(question_file, "r", encoding="utf-8") as f:
        questions = json.load(f)

    with st.form("questionnaire"):
        for q in questions:
            key = q["key"]
            label = q["question_ar"] if lang == "العربية" else q["question_en"]
            options = q["options"]
            allow_custom = q.get("allow_custom", False)

            answer = st.multiselect(label, options, key=key)

            if allow_custom:
                custom = st.text_input("✏ " + ("إجابة مخصصة" if lang == "العربية" else "Custom answer"), key=f"{key}_custom")
                if custom.strip():
                    answer.append(custom.strip())

            st.session_state.answers[key] = answer

        submitted = st.form_submit_button("🔍 تحليل الآن" if lang == "العربية" else "🔍 Analyze Now")
        if not submitted:
            st.stop()

# -------------------------------
# عرض التوصيات الثلاثة
# -------------------------------
st.markdown("## ✅ " + ("نتائج التوصيات" if lang == "العربية" else "Your Recommendations"))

def display_recommendation(title, key, method, box_type="default"):
    if key not in st.session_state:
        try:
            recs = generate_sport_recommendation(st.session_state.answers, lang)
            methods = {
                "standard": recs[0] if len(recs) > 0 else "⚠ لا توجد توصية.",
                "alternative": recs[1] if len(recs) > 1 else "⚠ لا توجد توصية.",
                "creative": recs[2] if len(recs) > 2 else "⚠ لا توجد توصية.",
            }
            st.session_state[key] = methods[method]
        except Exception as e:
            st.session_state[key] = f"⚠ خطأ: {str(e)}"

    st.subheader(title)
    if box_type == "success":
        st.success(st.session_state[key])
    elif box_type == "info":
        st.info(st.session_state[key])
    else:
        st.warning(st.session_state[key])

    # عرض التقييم
    st.session_state.ratings[key] = st.slider(
        "⭐ " + ("قيّم هذه التوصية" if lang == "العربية" else "Rate this recommendation"),
        1, 5, key=f"rating_{key}"
    )

# عرض التوصيات الثلاثة
display_recommendation("🥇 التوصية رقم 1", "recommendation_1", "standard", box_type="success")
display_recommendation("🌿 التوصية رقم 2", "recommendation_2", "alternative", box_type="info")
display_recommendation("🌌 التوصية رقم 3 (ابتكارية)", "recommendation_3", "creative", box_type="default")

# -------------------------------
# شات الذكاء التفاعلي
# -------------------------------
st.markdown("---")
st.markdown("## 🧠 " + ("تحدث مع الذكاء الرياضي" if lang == "العربية" else "Talk to the AI Coach"))

for entry in st.session_state.chat_history:
    role, content = entry["role"], entry["content"]
    if role == "user":
        st.markdown(f"🧍‍♂ أنت: {content}", unsafe_allow_html=True)
    else:
        st.markdown(f"🤖 Sports Sync: {content}", unsafe_allow_html=True)

user_input = st.chat_input("🗨 " + ("اكتب ردك أو اسأل أي سؤال..." if lang == "العربية" else "Type your response or ask a question..."))

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    reply = start_dynamic_chat(
        answers=st.session_state.answers,
        previous_recommendation=[
            st.session_state.get("recommendation_1", ""),
            st.session_state.get("recommendation_2", ""),
            st.session_state.get("recommendation_3", ""),
        ],
        ratings=st.session_state.ratings,
        user_id=st.session_state.user_id,
        lang=lang
    )

    st.session_state.chat_history.append({"role": "assistant", "content": reply})

    log_user_insight(st.session_state.user_id, {
        "type": "chat_interaction",
        "user_message": user_input,
        "ai_reply": reply,
        "lang": lang,
        "full_chat": st.session_state.chat_history
    })

    st.rerun()
