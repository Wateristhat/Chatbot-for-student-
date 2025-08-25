import streamlit as st
import google.generativeai as genai
import time

st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="centered")

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False

@st.cache_data
def generate_story(prompt):
    if not AI_ENABLED:
        return "Lỗi: Không thể kết nối tới AI. Vui lòng kiểm tra API Key."
    try:
        creative_prompt = (
            f"Hãy viết một câu chuyện cổ tích thật ngắn (khoảng 4-5 câu), "
            f"với nội dung thật trong sáng, vui vẻ và có một kết thúc tốt đẹp dành cho trẻ em. "
            f"Chủ đề của câu chuyện là: '{prompt}'"
        )
        response = gemini_model.generate_content(creative_prompt)
        return response.text
    except Exception:
        return "Rất tiếc, mình không thể nghĩ ra câu chuyện ngay lúc này."

# --- Giao diện trang ---
st.title("📖 Người Kể Chuyện")
st.markdown("Hãy cho mình biết bạn muốn nghe câu chuyện về điều gì nhé!")

if 'story_topic' not in st.session_state:
    st.session_state.story_topic = ""
if 'generated_story' not in st.session_state:
    st.session_state.generated_story = ""

topic = st.text_input(
    "Chủ đề câu chuyện (ví dụ: một chú thỏ dũng cảm...)", 
    value=st.session_state.story_topic
)

if st.button("Kể chuyện cho mình nghe!", type="primary"):
    if topic:
        st.session_state.story_topic = topic
        with st.spinner("Mình đang nghĩ ý tưởng..."):
            story = generate_story(topic)
            st.session_state.generated_story = story
    else:
        st.warning("Bạn ơi, hãy cho mình biết chủ đề câu chuyện nhé!")

if st.session_state.generated_story:
    st.write("---")
    st.subheader(f"Câu chuyện về '{st.session_state.story_topic}'")
    st.write(st.session_state.generated_story)
    st.success("Chúc bạn đọc truyện vui vẻ!", icon="🎉")
