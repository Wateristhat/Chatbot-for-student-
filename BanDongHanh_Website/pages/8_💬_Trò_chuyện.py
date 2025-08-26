# pages/Trò_chuyện_cùng_Bot.py
import streamlit as st
import database as db
import google.generativeai as genai
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Trò chuyện cùng Bot", page_icon="💬", layout="centered")

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập và bắt đầu trò chuyện nhé! ❤️")
    st.stop()

# --- LẤY THÔNG TIN NGƯỜI DÙNG ---
user_id = st.session_state.user_id
user_name = st.session_state.user_name

# --- BỘ LỌC TỪ KHÓA NGUY HIỂM ---
CRISIS_KEYWORDS = [
    "tự tử", "tự sát", "kết liễu", "chấm dứt", "không muốn sống",
    "muốn chết", "kết thúc tất cả", "làm hại bản thân", "tự làm đau",
    "tuyệt vọng", "vô vọng", "không còn hy vọng"
]

# --- KẾT NỐI VỚI GEMINI AI ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False

# --- CÁC HÀM HỖ TRỢ ---
def check_for_crisis(text):
    lowered_text = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in lowered_text:
            return True
    return False

def get_ai_response(user_prompt):
    if not AI_ENABLED:
        return "Xin lỗi, tính năng AI hiện không khả dụng."
    context_history = db.get_chat_history(user_id, limit=10)
    gemini_history = [{"role": "user" if msg["sender"] == "user" else "model", "parts": [msg["text"]]} for msg in context_history]
    try:
        chat = gemini_model.start_chat(history=gemini_history)
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        return f"Xin lỗi, mình đang gặp chút sự cố kỹ thuật. Bạn thử lại sau nhé."

def add_message(sender, text):
    """Thêm tin nhắn vào state và database."""
    st.session_state.messages.append({"sender": sender, "text": text})
    db.add_chat_message(user_id, sender, text)

# --- KHỞI TẠO SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = db.get_chat_history(user_id)
if "chat_flow" not in st.session_state:
    st.session_state.chat_flow = "start" # Các trạng thái: start, selecting_mood, free_chat

# Tin nhắn chào mừng nếu chưa có lịch sử
if not st.session_state.messages:
    welcome_message = f"Chào {user_name}, mình là Bạn Đồng Hành đây! Bạn có điều gì muốn chia sẻ không?"
    add_message("bot", welcome_message)

# --- CÁC HÀM CALLBACK CHO NÚT BẤM ---
def start_tam_su():
    add_message("user", "Mình muốn tâm sự")
    add_message("bot", "Hôm nay bạn cảm thấy như thế nào nè? Mình luôn sẵn lòng lắng nghe bạn nha 🌟")
    st.session_state.chat_flow = "selecting_mood"

def select_mood(mood, initial_response):
    add_message("user", mood)
    add_message("bot", initial_response)
    st.session_state.chat_flow = "free_chat" # Sau khi chọn xong, chuyển sang chat tự do

# --- GIAO DIỆN CHÍNH ---
st.title(f"💬 Trò chuyện cùng Bot")

# Hiển thị lịch sử tin nhắn
for message in st.session_state.messages:
    with st.chat_message("user" if message["sender"] == "user" else "assistant"):
        st.markdown(message["text"])

# --- HIỂN THỊ CÁC NÚT ĐỊNH HƯỚNG DỰA TRÊN TRẠNG THÁI ---
if st.session_state.chat_flow == "start":
    st.button("Tâm sự 💌", on_click=start_tam_su, use_container_width=True)
    # Bạn có thể thêm nút "Luyện tập giao tiếp" ở đây nếu muốn

elif st.session_state.chat_flow == "selecting_mood":
    moods = {
        "😄 Vui": "Tuyệt vời quá! Có chuyện gì vui không, kể mình nghe với nè!",
        "😔 Buồn": "Ôi, mình nghe rồi nè, có chuyện gì làm bạn buồn vậy?",
        "😡 Tức giận": "Giận dữ làm mình khó chịu lắm. Bạn kể ra đi, đỡ hơn nhiều đó!",
    }
    cols = st.columns(len(moods))
    for i, (mood, response) in enumerate(moods.items()):
        cols[i].button(mood, on_click=select_mood, args=(mood, response), use_container_width=True)

# --- KHUNG NHẬP LIỆU CHAT TỰ DO ---
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    st.session_state.chat_flow = "free_chat" # Khi người dùng gõ, chuyển sang chat tự do
    add_message("user", prompt)

    # Hiển thị tin nhắn người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)

    # Xử lý phản hồi của bot
    with st.chat_message("assistant"):
        with st.spinner("Bot đang suy nghĩ..."):
            if check_for_crisis(prompt):
                response = "Mình nhận thấy bạn đang gặp phải những cảm xúc rất tiêu cực. Nếu bạn cần sự giúp đỡ ngay lập tức, hãy liên hệ với các chuyên gia qua trang **Hỗ Trợ Khẩn Cấp** nhé."
                st.error(response)
            else:
                response = get_ai_response(prompt)
                st.markdown(response)
    
    add_message("bot", response)
