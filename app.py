import streamlit as st
import json
import uuid
import pandas as pd
from datetime import datetime

from logic.backend_gpt import generate_sport_recommendation
from logic.dynamic_chat import start_dynamic_chat
from logic.chat_personality import get_chat_personality

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
def save_user_data(user_id, lang, answers, recommendation):
    data = {
        "user_id": user_id,
        "timestamp": datetime.now().isoformat(),
        "language": lang,
        "answers": answers,
        "recommendation": recommendation
    }
    df = pd.DataFrame([data])
    df.to_csv("data/user_sessions.csv", mode="a", index=False, header=False, encoding="utf-8")

# ---------------------
# واجهة المستخدم
# ---------------------
st.set_page_config(page_title="توصية رياضية", layout="centered")
st.title("🎯 توصيتك الرياضية الذكية")

# اختيار اللغة
lang = st.radio("اختر اللغة / Choose Language", ["العربية", "English"])

questions = load_questions(lang)
answers = {}
user_id = str(uuid.uuid4())

# عرض الأسئلة
for idx, q in enumerate(questions, 1):
    q_key = f"q{idx}"
    if q["type"] == "multiple":
        selected = st.multiselect(q["question"], q["options"], key=q_key)
        answers[q_key] = selected
    else:
        answer = st.radio(q["question"], q["options"], key=q_key)
        answers[q_key] = answer

    # إجابة حرة
    if q.get("allow_custom"):
        custom_input = st.text_input("إجابة أخرى (اختياري):", key=f"{q_key}_custom")
        if custom_input:
            answers[q_key].append(custom_input) if isinstance(answers[q_key], list) else answers.update({q_key: custom_input})

# خانة الإدخال المفتوحة في النهاية
answers["custom_input"] = st.text_area("✏️ هل هناك شيء تحب إضافته؟", "")

# ---------------------
# التوصية
# ---------------------
if st.button("🔍 احصل على توصيتي الرياضية"):
    with st.spinner("جاري تحليل إجاباتك..."):
        recommendation = generate_sport_recommendation(answers, lang)
        st.session_state["recommendation"] = recommendation
        st.session_state["answers"] = answers
        st.session_state["user_id"] = user_id
        st.success("✅ تم إنشاء التوصية!")
        st.markdown(f"### 🎽 توصيتك:\n\n{recommendation}")
        save_user_data(user_id, lang, answers, recommendation)

        # زر نسخ
        st.code(recommendation, language="markdown")
        st.button("📋 نسخ التوصية", on_click=lambda: st.toast("تم النسخ ✔️"))

        # رابط عام (محاكى - ليس فعلي)
        st.markdown(f"[🔗 رابط عام لمشاركة النتيجة](https://sport-sync.vercel.app/share/{user_id})")

        # دعوة صديق
        st.markdown(f"[📨 دعوة صديق لتجربة الاختبار](https://sport-sync.vercel.app)")

        # زر "لم أقتنع"
        if st.button("❌ لم أقتنع بالنتيجة"):
            with st.spinner("إعادة التحليل بعمق..."):
                new_rec = start_dynamic_chat(answers, recommendation, user_id, lang)
                st.markdown("### 🔁 توصية بديلة مخصصة:")
                st.markdown(new_rec)
