import streamlit as st
import asyncio
import edge_tts
import os

# --- الإعدادات الجمالية والبيانات الثابتة ---
st.set_page_config(page_title="AI Voice Assistant", page_icon="🎙️")

# "قاعدة بيانات" صغيرة لأسئلة وأجوبة محددة (اختياري)
QA_DATA = {
    "من أنت؟": "أنا المساعد الذكي الخاص بك، تم تطويري لتحويل النصوص إلى أصوات واقعية.",
    "ما هو هدف المشروع؟": "تسهيل إنتاج المحتوى الصوتي باستخدام الذكاء الاصطناعي.",
    "أهلاً": "أهلاً بك! كيف يمكنني مساعدتك اليوم؟"
}

st.markdown("""
    <style>
    .stApp { background-color: #fdfdfd; }
    .stButton>button { width: 100%; border-radius: 20px; background: #6C63FF; color: white; }
    .stTextArea textarea { border-radius: 15px; border: 1px solid #6C63FF; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ محول النصوص الذكي")

# قسم البيانات الجاهزة (قاعدة البيانات الصغيرة)
with st.expander("💡 أسئلة شائعة (إجابات جاهزة)"):
    selected_q = st.selectbox("اختر سؤالاً ليتم تحويل إجابته لصوت:", [""] + list(QA_DATA.keys()))
    if selected_q:
        text_to_process = QA_DATA[selected_q]
        st.write(f"**الإجابة:** {text_to_process}")
    else:
        text_to_process = ""

# قسم الإدخال الحر
st.markdown("---")
user_text = st.text_area("أو اكتب النص الذي تريده هنا:", value=text_to_process if text_to_process else "")

# اختيار الصوت
voice = st.selectbox("اختر الشخصية الصوتية:", ["ar-EG-SalmaNeural", "ar-EG-ShakirNeural", "en-US-AvaNeural"])

async def run_tts(t, v):
    communicate = edge_tts.Communicate(t, v)
    await communicate.save("speech.mp3")

if st.button("تحويل النص إلى صوت ✨"):
    if user_text:
        with st.spinner("جاري المعالجة..."):
            asyncio.run(run_tts(user_text, voice))
            st.audio("speech.mp3")
            st.success("تم بنجاح!")
    else:
        st.warning("من فضلك اختر سؤالاً أو اكتب نصاً أولاً")
