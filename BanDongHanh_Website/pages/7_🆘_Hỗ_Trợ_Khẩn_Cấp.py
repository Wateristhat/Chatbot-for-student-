# pages/Trò_chuyện_cùng_Bot.py
import streamlit as st
import database as db
import google.generativeai as genai
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Trò chuyện cùng Bot", page_icon="💬", layout="centered")

# --- KIỂM TRA ĐĂNG NHẬP ---
# Yêu cầu người dùng phải đăng nhập để bảo mật cuộc trò chuyện
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
    # Lấy API key từ Streamlit secrets
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception:
    AI_ENABLED = False
    st.error("Không thể kết nối đến dịch vụ AI. Vui lòng kiểm tra lại API Key.")

# --- CÁC HÀM HỖ TRỢ ---
def check_for_crisis(text):
    """Kiểm tra xem văn bản có chứa từ khóa khủng hoảng không."""
    lowered_text = text.lower()
    for keyword in CRISIS_KEYWORDS:
        if keyword in lowered_text:
            return True
    return False

def get_ai_response(user_prompt):
    """Gọi API của Gemini để nhận phản hồi."""
    if not AI_ENABLED:
        return "Xin lỗi, tính năng AI hiện không khả dụng."

    # Lấy 10 tin nhắn gần nhất làm ngữ cảnh
    context_history = db.get_chat_history(user_id, limit=10)
    
    # Tạo định dạng lịch sử phù hợp cho Gemini
    gemini_history = []
    for msg in context_history:
        role = "user" if msg["sender"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["text"]]})

    try:
        # Bắt đầu cuộc trò chuyện với lịch sử
        chat = gemini_model.start_chat(history=gemini_history)
        
        # Gửi tin nhắn mới của người dùng
        response = chat.send_message(user_prompt)
        return response.text
    except Exception as e:
        st.error(f"Đã xảy ra lỗi khi gọi AI: {e}")
        return "Xin lỗi, mình đang gặp chút sự cố. Bạn thử lại sau nhé."

# --- GIAO DIỆN CHÍNH ---
st.title(f"💬 Trò chuyện cùng Bot")
st.markdown(f"Chào **{user_name}**, bạn có điều gì muốn chia sẻ không?")

# --- KHỞI TẠO LỊCH SỬ TRÒ CHUYỆN ---
if "messages" not in st.session_state:
    # Tải lịch sử từ DB khi bắt đầu phiên
    st.session_state.messages = db.get_chat_history(user_id)
    if not st.session_state.messages:
        # Nếu chưa có tin nhắn nào, thêm tin nhắn chào mừng
        initial_message = {"sender": "bot", "text": f"Chào {user_name}, mình là Bạn Đồng Hành đây! Mình luôn sẵn lòng lắng nghe bạn."}
        db.add_chat_message(user_id, initial_message["sender"], initial_message["text"])
        st.session_state.messages.append(initial_message)

# --- HIỂN THỊ LỊCH SỬ TRÒ CHUYỆN ---
for message in st.session_state.messages:
    # Sử dụng st.chat_message để hiển thị tin nhắn theo vai trò (user/bot)
    with st.chat_message("user" if message["sender"] == "user" else "assistant"):
        st.markdown(message["text"])

# --- KHUNG NHẬP LIỆU CỦA NGƯỜI DÙNG ---
if prompt := st.chat_input("Nhập tin nhắn của bạn..."):
    # 1. Thêm tin nhắn của người dùng vào state và DB
    st.session_state.messages.append({"sender": "user", "text": prompt})
    db.add_chat_message(user_id, "user", prompt)
    
    # 2. Hiển thị tin nhắn của người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)

    # 3. Kiểm tra khủng hoảng trước khi xử lý
    if check_for_crisis(prompt):
        crisis_response = "Mình nhận thấy bạn đang gặp phải những cảm xúc rất tiêu cực. Nếu bạn cần sự giúp đỡ ngay lập tức, hãy liên hệ với các chuyên gia qua trang **Hỗ Trợ Khẩn Cấp** nhé."
        st.session_state.messages.append({"sender": "bot", "text": crisis_response})
        db.add_chat_message(user_id, "bot", crisis_response)
        with st.chat_message("assistant"):
            st.error(crisis_response) # Hiển thị dưới dạng lỗi để nổi bật
    else:
        # 4. Lấy phản hồi từ AI và hiển thị
        with st.chat_message("assistant"):
            with st.spinner("Bot đang suy nghĩ..."):
                response = get_ai_response(prompt)
                st.markdown(response)
        
        # 5. Thêm phản hồi của bot vào state và DB
        st.session_state.messages.append({"sender": "bot", "text": response})
        db.add_chat_message(user_id, "bot", response)
