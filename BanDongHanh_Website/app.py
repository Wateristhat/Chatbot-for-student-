import streamlit as st
import random
import re
import time
import html
import database as db
import google.generativeai as genai
from gtts import gTTS
from io import BytesIO
import base64

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

user_id = st.session_state.user_id
user_name = st.session_state.user_name

# --- BỘ LỌC TỪ KHÓA NGUY HIỂM ---
CRISIS_KEYWORDS = [
    "tự tử", "tự sát", "kết liễu", "chấm dứt", "không muốn sống",
    "muốn chết", "kết thúc tất cả", "làm hại bản thân", "tự làm đau",
    "tuyệt vọng", "vô vọng", "không còn hy vọng"
]

# --- CÁC HẰNG SỐ VÀ CẤU HÌNH ---
CHAT_STATE_MAIN = 'main'
CHAT_STATE_TAM_SU_SELECTION = 'tam_su_selection'
CHAT_STATE_TAM_SU_CHAT = 'tam_su_chat'
CHAT_STATE_GIAO_TIEP_SELECTION_BASIC = 'giao_tiep_selection_basic'
CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED = 'giao_tiep_selection_extended'
CHAT_STATE_GIAO_TIEP_PRACTICE = 'giao_tiep_practice'
CHAT_STATE_AWAITING_FOLLOWUP = 'awaiting_followup'

@st.cache_data
def get_config():
    # (Toàn bộ config của bạn có thể dán vào đây)
    return { "ui": { "title": "Bạn đồng hành 💖", "input_placeholder": "Nhập tin nhắn..." } } # Ví dụ rút gọn
CONFIG = get_config()

try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False

st.set_page_config(page_title=CONFIG["ui"]["title"], layout="wide")
st.markdown(r"""<style>...</style>""", unsafe_allow_html=True) # Giữ nguyên CSS của bạn

# --- KHỞI TẠO VÀ TẢI DỮ LIỆU ---
if "chat_initialized" not in st.session_state:
    st.session_state.chat_state = CHAT_STATE_MAIN
    st.session_state.history = db.get_chat_history(user_id)
    if not st.session_state.history:
        initial_message = f"Chào {user_name}, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"
        st.session_state.history = [{"sender": "bot", "text": initial_message}]
        db.add_chat_message(user_id, "bot", initial_message)
    st.session_state.turns = 0
    st.session_state.current_mood = None
    st.session_state.current_scenario = None
    st.session_state.user_input = ""
    st.session_state.chat_initialized = True

# --- CÁC HÀM TIỆN ÍCH ---
def check_for_crisis(text):
    lowered_text = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in lowered_text:
            return True
    return False

def render_crisis_response():
    st.error("Mình nghe thấy bạn đang thực sự rất khó khăn. Điều quan trọng nhất ngay bây giờ là bạn được an toàn. Dưới đây là những người có thể giúp đỡ bạn ngay lập tức.", icon="❤️")
    st.markdown("""
        <div style="background-color: #FFFFE0; border-left: 6px solid #FFC107; padding: 15px; border-radius: 5px;">
            <h4>Vui lòng liên hệ một trong những số điện thoại sau:</h4>
            <ul>
                <li><strong>Tổng đài Quốc gia Bảo vệ Trẻ em:</strong> <strong style="font-size: 1.2em;">111</strong> (Miễn phí, 24/7)</li>
                <li><strong>Đường dây nóng Ngày Mai:</strong> <strong style="font-size: 1.2em;">096.357.9488</strong> (Hỗ trợ người trầm cảm)</li>
            </ul>
            <p><strong>Làm ơn hãy gọi nhé. Bạn không đơn độc đâu.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    st.stop()

def add_message_and_save(sender, text):
    st.session_state.history.append({"sender": sender, "text": text})
    db.add_chat_message(user_id, sender, text)

# (Các hàm khác như text_to_speech, call_gemini_with_memory... giữ nguyên)

# --- GIAO DIỆN CHÍNH ---
st.title("💬 Trò chuyện cùng Bot")

if st.session_state.get('crisis_detected'):
    render_crisis_response()

# Hiển thị lịch sử chat
for message in st.session_state.history:
    with st.chat_message("user" if message["sender"] == "user" else "assistant"):
        st.markdown(message["text"])

# Thanh nhập liệu
if prompt := st.chat_input("Nhập tin nhắn..."):
    if check_for_crisis(prompt):
        add_message_and_save("user", prompt)
        st.session_state.crisis_detected = True
        st.rerun()
    else:
        add_message_and_save("user", prompt)
        # (Logic gọi AI và xử lý input thông thường của bạn)
        st.rerun()
