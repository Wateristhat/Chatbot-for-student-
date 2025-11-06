# Sửa file: pages/8_💬_Trò_chuyện.py
import streamlit as st
import google.generativeai as genai
import random
import sys # ### <<< SỬA ĐỔI
import os  # ### <<< SỬA ĐỔI

# ### <<< SỬA ĐỔI: Import database >>>
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db 

# --- BẢO VỆ TRANG ---
### <<< SỬA ĐỔI: Thêm bảo vệ trang ở đầu file >>>
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() # Dừng chạy code của trang này

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI ---
current_user_id = st.session_state.user_id

# --- CẤU HÌNH TRANG VÀ CSS (Giữ nguyên) ---
st.set_page_config(
    page_title="Chatbot AI Đồng Hành",
    page_icon="🌈",
    layout="centered"
)
# (Toàn bộ CSS màu mè của bạn được giữ nguyên ở đây)
st.markdown("""<style> ... (CSS của bạn) ... </style>""", unsafe_allow_html=True)


# --- CẤU HÌNH DỮ LIỆU TƯƠNG TÁC (Giữ nguyên) ---
CONFIG = {
    "tam_su": {
        "intro_message": "Hôm nay bạn cảm thấy như thế nào nè? Mình luôn sẵn lòng lắng nghe bạn nha 🌟",
        "emotions": {
            "😄 Vui": "Tuyệt vời quá! Có chuyện gì vui không, kể mình nghe với nè!",
            "😐 Bình thường": "Vậy là một ngày bình yên. Nếu có gì muốn kể, mình nghe nè.",
            "😔 Buồn": "Ôi, mình nghe rồi nè, có chuyện gì làm bạn buồn vậy?",
            "😢 Tủi thân": "Tớ hiểu, cảm giác tủi thân không vui chút nào. Kể tớ nghe nha, mình ở đây rồi.",
            "😡 Tức giận": "Giận dữ làm mình khó chịu lắm. Bạn kể ra đi, đỡ hơn nhiều đó!",
        },
    },
    "giao_tiep": {
        "intro_message": "Hãy chọn một tình huống bên dưới để mình cùng luyện tập nhé!",
        "scenarios_basic": {
            "👋 Chào hỏi bạn bè": "Bạn có thể nói: ‘Chào bạn, hôm nay vui không?’ HoHoặc: ‘Tớ chào cậu nha, hôm nay học tốt không nè?’",
            "🙋 Hỏi bài thầy cô": "Bạn thử hỏi thầy/cô như vầy nha: ‘Thầy/cô ơi, em chưa hiểu phần này, thầy/cô giảng lại giúp em được không ạ?’",
            "🧑‍🤝‍🧑 Làm quen bạn mới": "Bạn có thể bắt đầu bằng: ‘Xin chào, tớ là A, còn bạn tên gì?’ Hoặc: ‘Mình mới vào lớp, cậu có thể chỉ mình vài điều không?’",
            "🙌 Xin lỗi": "Khi làm bạn buồn, bạn có thể nói: ‘Xin lỗi nha, mình không cố ý đâu.’ hoặc ‘Mình buồn vì đã làm bạn không vui, mong bạn tha lỗi.’",
            "🎉 Chúc mừng bạn": "Bạn có thể nói: ‘Chúc mừng nha, bạn làm tốt lắm!’ hoặc ‘Tuyệt vời quá, mình rất vui cho bạn!’",
        },
        "confirm_buttons": {
            "understood": "✅ Đã hiểu rồi!",
            "not_understood": "❓ Chưa rõ lắm!",
        }
    }
}

# --- KHỞI TẠO STATE VÀ CÁC HÀM HỖ TRỢ ---

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "main"

### <<< SỬA ĐỔI: Không dùng st.session_state.messages nữa >>>
# if "messages" not in st.session_state:
#     st.session_state.messages = [] # Sẽ đọc từ CSDL

# --- PHẦN CODE CHÍNH ---

st.title("✨ Chatbot AI Đồng Hành ✨")
st.caption(f"Trò chuyện với AI (Người dùng: {current_user_id})")

# Cấu hình Gemini AI (Giữ nguyên)
@st.cache_resource
def configure_gemini():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash") # Dùng 1.5 Flash nếu có thể
        return model
    except Exception as e:
        st.error("Lỗi: Vui lòng cấu hình GOOGLE_API_KEY trong file secrets.toml.")
        st.stop()

model = configure_gemini()

### <<< SỬA ĐỔI: Tải lịch sử chat từ CSDL >>>
# Lấy lịch sử chat cũ của user này
chat_history_from_db = db.get_chat_history(current_user_id)

# Bắt đầu session chat với lịch sử từ CSDL
chat = model.start_chat(history=chat_history_from_db)

# Hàm trợ giúp để lưu tin nhắn
def add_message_to_db_and_rerun(role, content):
    """Lưu tin nhắn vào CSDL và tải lại trang"""
    db.add_chat_message(current_user_id, role, content)
    st.rerun()

# --- GIAO DIỆN NÚT BẤM TƯƠNG TÁC ---
button_container = st.container()
with button_container:
    if st.session_state.chat_mode == "main":
        col1, col2 = st.columns(2)
        if col1.button("💖 Tâm sự"):
            st.session_state.chat_mode = "tam_su_selection"
            # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
            add_message_to_db_and_rerun("assistant", CONFIG["tam_su"]["intro_message"])

        if col2.button("🗣️ Giao tiếp"):
            st.session_state.chat_mode = "giao_tiep_selection"
            # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
            add_message_to_db_and_rerun("assistant", CONFIG["giao_tiep"]["intro_message"])
            
        # ### <<< SỬA ĐỔI: Thêm nút Xóa lịch sử >>>
        if st.button("🗑️ Xóa lịch sử trò chuyện", key="clear_chat"):
            db.clear_chat_history(current_user_id)
            st.success("Đã xóa lịch sử trò chuyện!")
            st.rerun()

    elif st.session_state.chat_mode == "tam_su_selection":
        st.write("Hôm nay bạn cảm thấy thế nào?")
        emotions = list(CONFIG["tam_su"]["emotions"].keys())
        cols = st.columns(len(emotions))
        for i, emotion in enumerate(emotions):
            if cols[i].button(emotion):
                response_text = CONFIG["tam_su"]["emotions"][emotion]
                st.session_state.chat_mode = "main"
                # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
                add_message_to_db_and_rerun("assistant", response_text)

    elif st.session_state.chat_mode == "giao_tiep_selection":
        st.write("Chọn tình huống bạn muốn luyện tập:")
        for scenario, example in CONFIG["giao_tiep"]["scenarios_basic"].items():
            if st.button(scenario, key=scenario):
                st.session_state.chat_mode = "giao_tiep_practice"
                # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
                add_message_to_db_and_rerun("assistant", example)
        if st.button("↩️ Quay lại"):
             st.session_state.chat_mode = "main"
             st.rerun()

    elif st.session_state.chat_mode == "giao_tiep_practice":
        col1, col2 = st.columns(2)
        if col1.button(CONFIG["giao_tiep"]["confirm_buttons"]["understood"]):
            st.session_state.chat_mode = "main"
            # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
            add_message_to_db_and_rerun("assistant", "Tuyệt vời! Bạn làm tốt lắm. Khi nào cần cứ tìm mình nhé.")
        if col2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"]):
            # ### <<< SỬA ĐỔI: Lưu vào CSDL >>>
            # (Không cần quay về main, chỉ gửi tin nhắn)
            db.add_chat_message(current_user_id, "assistant", "Không sao cả, mình nói lại nhé. Bạn hãy đọc kỹ lại câu mẫu phía trên nha.")
            st.rerun()


# --- HIỂN THỊ LỊCH SỬ CHAT TỪ CSDL ---
### <<< SỬA ĐỔI: Đọc lại từ CSDL (để lấy tin nhắn mới nhất từ nút bấm) >>>
# (Chúng ta phải đọc lại lần nữa vì st.rerun đã chạy)
display_messages = db.get_chat_history(current_user_id) # Hàm này trả về format của Gemini

for message in display_messages:
    # Chuyển đổi format Gemini (model/user) sang format Streamlit (assistant/user)
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]) # Lấy nội dung text

# --- NHẬN INPUT VĂN BẢN ---
if prompt := st.chat_input("Hoặc gõ tin nhắn tự do ở đây..."):
    # ### <<< SỬA ĐỔI: Lưu tin nhắn USER vào CSDL >>>
    db.add_chat_message(current_user_id, "user", prompt)
    
    # Hiển thị tin nhắn user (tạm thời)
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi tin nhắn tới Gemini và nhận phản hồi
    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = chat.send_message(prompt)
                response_text = response.text
                st.markdown(response_text)
                
                # ### <<< SỬA ĐỔI: Lưu tin nhắn ASSISTANT vào CSDL >>>
                db.add_chat_message(current_user_id, "assistant", response_text)
                
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra: {e}")
