# pages/9_📖_Người_Kể_Chuyện.py
import streamlit as st
import random
from gtts import gTTS
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Người Kể Chuyện", page_icon="📖", layout="wide")

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé! ❤️")
    st.stop()

# --- CSS GIAO DIỆN HOÀN CHỈNH ---
st.markdown("""
<style>
/* CSS chung cho các nút bấm */
.stButton > button {
    padding: 0.8rem 1.2rem; font-size: 1.15rem; font-weight: 600; width: 100%;
    margin-bottom: 0.7rem; border-radius: 12px; border: 2px solid #b39ddb;
    background-color: #f9f9fb; color: #6d28d9;
}
.stButton > button:hover { background-color: #f3e8ff; border-color: #5d3fd3; color: #5d3fd3; }

/* CSS cho tiêu đề và khung trợ lý ảo */
.nkc-title-feature {
    font-size: 2.6rem; font-weight: 700; color: #5d3fd3; text-align: center;
    margin-bottom: 1.4rem; margin-top: 0.7rem; display: flex; align-items: center;
    justify-content: center; gap: 1.1rem;
}
.nkc-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom: 2.3rem; margin-top: 0.2rem;
    text-align: center; border: 3.5px solid #b39ddb; max-width: 1700px;
    margin-left: auto; margin-right: auto;
}
.nkc-assist-icon { font-size: 3.2rem; margin-bottom: 0.7rem; }
.nkc-assist-text { font-size: 1.7rem; font-weight: 700; color: #6d28d9; margin-bottom: 1.1rem; }

/* --- CSS MỚI SỬA LỖI MẤT CHỮ VÀ LÀM TO Ô CHỌN --- */
.selectbox-label {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: #333 !important;
    padding-bottom: 0.5rem !important;
}
/* Style cho cái hộp */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
    padding-top: 1rem !important;
    padding-bottom: 1rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    border-radius: 12px !important;
    border: 2px solid #b39ddb !important;
    background-color: #FFFFFF !important;
}
/* Style cho chữ bên trong hộp */
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div > div {
    font-size: 1.3rem !important;
    color: #333 !important; /* << DÒNG QUAN TRỌNG ĐỂ HIỆN CHỮ */
}
</style>
""", unsafe_allow_html=True)

# --- NỘI DUNG TRUYỆN ---
@st.cache_data
def load_stories():
    # ... (Nội dung truyện của bạn giữ nguyên) ...
    return { "Truyện truyền cảm hứng": [...], "Truyện ngụ ngôn": [...], "Truyện chữa lành": [...] }
STORIES = load_stories()

# --- TRỢ LÝ ẢO ---
ASSISTANT_MESSAGES = [
    ("📖", "Hãy chọn một thể loại và lắng nghe một câu chuyện nhỏ để xoa dịu tâm hồn nhé."),
    ("✨", "Mỗi câu chuyện là một bài học. Cùng khám phá với Bee nào!"),
    ("🎧", "Sẵn sàng lắng nghe chưa? Bee sẽ kể cho bạn những câu chuyện hay nhất!"),
]
if "nkc_assistant_message" not in st.session_state:
    st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
avatar, msg = st.session_state.nkc_assistant_message

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="nkc-title-feature">...</div>', unsafe_allow_html=True) # Rút gọn
st.markdown(f"""<div class="nkc-assist-bigbox">...</div>""", unsafe_allow_html=True) # Rút gọn

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("💬 Thông điệp mới", key="new_msg_story"):
        st.session_state.nkc_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe trợ lý ảo", key="tts_msg_story"):
        # ... (logic nghe trợ lý ảo) ...
        pass

st.markdown("⬅️ [Quay về Trang chủ](/)", unsafe_allow_html=True)
st.write("---")

# --- PHẦN CHỌN TRUYỆN ĐÃ SỬA ---
st.markdown("<p class='selectbox-label'>Chọn thể loại truyện bạn muốn nghe:</p>", unsafe_allow_html=True)
selected_category = st.selectbox(
    "selectbox_for_stories",
    options=list(STORIES.keys()),
    label_visibility="collapsed"
)
st.write("---")

# --- PHẦN HIỂN THỊ TRUYỆN ---
if selected_category:
    st.subheader(f"Các câu chuyện về {selected_category.lower()}:")
    for i, story in enumerate(STORIES[selected_category]):
        with st.expander(f"**{story['title']}**"):
            st.markdown(f"<p style='font-size: 1.1rem; line-height: 1.6;'>{story['content']}</p>", unsafe_allow_html=True)
            
            if st.button("Nghe truyện 🎧", key=f"listen_{selected_category}_{i}"):
                with st.spinner("Đang chuẩn bị âm thanh..."):
                    # ... (logic nghe truyện) ...
                    pass
