import streamlit as st
import asyncio
import edge_tts
import os

# إعدادات الصفحة والجماليات
st.set_page_config(page_title="AI Voice Generator", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f9f9fb; }
    .stButton>button {
        width: 100%;
        border-radius: 25px;
        background: linear-gradient(45deg, #6C63FF, #3F3D56);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
    }
    .stTextArea textarea { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎙️ محول النصوص إلى أصوات ذكية")
st.write("حول نصوصك إلى مقاطع صوتية احترافية باستخدام تقنيات الذكاء الاصطناعي.")

# واجهة المدخلات
text = st.text_area("أدخل النص هنا:", placeholder="اكتب شيئاً ليتم تحويله...", height=150)

col1, col2 = st.columns(2)
with col1:
    voice_option = st.selectbox("اختر الشخصية الصوتية:", 
                                ["ar-EG-SalmaNeural (أنثى)", "ar-EG-ShakirNeural (ذكر)", "en-US-AvaNeural (English)"])
with col2:
    speed = st.slider("سرعة الصوت:", 0.5, 2.0, 1.0)

# الوظيفة البرمجية
async def generate_voice(text_to_speak, selected_voice, speed_rate):
    # تحويل السرعة للصيغة المطلوبة (+0% أو -10%)
    rate = f"+{int((speed_rate-1)*100)}%" if speed_rate >= 1 else f"-{int((1-speed_rate)*100)}%"
    voice_id = selected_voice.split(" ")[0]
    communicate = edge_tts.Communicate(text_to_speak, voice_id, rate=rate)
    await communicate.save("output.mp3")

# زر التشغيل
if st.button("توليد الملف الصوتي ✨"):
    if text.strip():
        with st.spinner("جاري إنشاء الصوت..."):
            try:
                asyncio.run(generate_voice(text, voice_option, speed))
                audio_file = open("output.mp3", "rb")
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.success("تم بنجاح!")
                st.download_button("تحميل الملف 📥", data=audio_bytes, file_name="ai_voice.mp3", mime="audio/mp3")
            except Exception as e:
                st.error(f"حدث خطأ: {e}")
    else:
        st.warning("يرجى إدخال نص أولاً!")

st.markdown("---")
st.caption("برمجة وتطوير باستخدام Streamlit & Edge-TTS")
