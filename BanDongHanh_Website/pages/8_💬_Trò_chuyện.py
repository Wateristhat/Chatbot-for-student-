# Sửa file: pages/8_💬_Trò_chuyện.py
import streamlit as st
import google.generativeai as genai
import random
import sys 
import os 
import database as db 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- BẢO VỆ TRANG ---
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() 

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI ---
current_user_id = st.session_state.user_id

# --- CẤU HÌNH TRANG VÀ CSS TÙY CHỈNH (ĐÃ SỬA MÀU) ---
st.set_page_config(
    page_title="Chatbot AI Đồng Hành",
    page_icon="🌈",
    layout="centered"
)

# <<< SỬA ĐỔI MÀU NỀN VÀ BONG BÓNG CHAT >>>
st.markdown("""
<style>
    /* Nền và font chữ tổng thể */
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        /* Tông: Hoàng hôn Mơ mộng (Hồng phấn -> Xanh baby) */
        background: linear-gradient(135deg, #FFC8DD, #BDE0FE);
    }
    /* Tiêu đề chính */
    h1 {
        font-size: 2.5em;
        text-align: center;
        background: linear-gradient(to right, #FF70A6, #8D5FFF); /* Màu nổi bật */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    /* Bong bóng chat USER (Giữ nguyên trắng, sửa border) */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-user"]) {
        background-color: #ffffff;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #ffafcc; /* Border hồng nhạt */
    }
    /* Bong bóng chat ASSISTANT (Gradient Xanh lá nhạt, màu trung tính) */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, #B5EAD7, #CDEBCC); /* Gradient Xanh lá/Mint nhạt */
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #1e1e1e;
        border: 1px solid #99c9b3;
    }
    /* Ô nhập liệu chat (Giữ nguyên) */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        padding: 5px 15px;
    }
    /* Nút bấm lớn (Giữ nguyên) */
    .stButton > button {
        border-radius: 12px;
        font-size: 1.1em;
        font-weight: bold;
        padding: 10px 20px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


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

# --- KHỞI TẠO STATE VÀ CÁC HÀM HỖ TRỢ (Giữ nguyên) ---

if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "main"

# --- PHẦN CODE CHÍNH (Giữ nguyên) ---

st.title("✨ Chatbot AI Đồng Hành ✨")
st.caption(f"Trò chuyện với AI (Người dùng: {current_user_id})")

# Cấu hình Gemini AI
@st.cache_resource
def configure_gemini():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.5-flash") # SỬA LỖI 404 Ở ĐÂY
        return model
    except Exception as e:
        st.error("Lỗi: Vui lòng cấu hình GOOGLE_API_KEY trong file secrets.toml.")
        st.stop()

model = configure_gemini()

# Tải lịch sử chat cũ của user này
chat_history_from_db = db.get_chat_history(current_user_id)

# Bắt đầu session chat với lịch sử từ CSDL
chat = model.start_chat(history=chat_history_from_db)

# Hàm trợ giúp để lưu tin nhắn
def add_message_to_db_and_rerun(role, content):
    """Lưu tin nhắn vào CSDL và tải lại trang"""
    db.add_chat_message(current_user_id, role, content)
    st.rerun()

# --- GIAO DIỆN NÚT BẤM TƯƠNG TÁC (Giữ nguyên logic) ---
button_container = st.container()
with button_container:
    if st.session_state.chat_mode == "main":
        col1, col2 = st.columns(2)
        if col1.button("💖 Tâm sự"):
            st.session_state.chat_mode = "tam_su_selection"
            add_message_to_db_and_rerun("assistant", CONFIG["tam_su"]["intro_message"])

        if col2.button("🗣️ Giao tiếp"):
            st.session_state.chat_mode = "giao_tiep_selection"
            add_message_to_db_and_rerun("assistant", CONFIG["giao_tiep"]["intro_message"])
            
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
                add_message_to_db_and_rerun("assistant", response_text)

    elif st.session_state.chat_mode == "giao_tiep_selection":
        st.write("Chọn tình huống bạn muốn luyện tập:")
        for scenario, example in CONFIG["giao_tiep"]["scenarios_basic"].items():
            if st.button(scenario, key=scenario):
                st.session_state.chat_mode = "giao_tiep_practice"
                add_message_to_db_and_rerun("assistant", example)
        if st.button("↩️ Quay lại"):
             st.session_state.chat_mode = "main"
             st.rerun()

    elif st.session_state.chat_mode == "giao_tiep_practice":
        col1, col2 = st.columns(2)
        if col1.button(CONFIG["giao_tiep"]["confirm_buttons"]["understood"]):
            st.session_state.chat_mode = "main"
            add_message_to_db_and_rerun("assistant", "Tuyệt vời! Bạn làm tốt lắm. Khi nào cần cứ tìm mình nhé.")
        if col2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"]):
            db.add_chat_message(current_user_id, "assistant", "Không sao cả, mình nói lại nhé. Bạn hãy đọc kỹ lại câu mẫu phía trên nha.")
            st.rerun()


# --- HIỂN THỊ LỊCH SỬ CHAT TỪ CSDL (Giữ nguyên logic) ---
display_messages = db.get_chat_history(current_user_id) 

for message in display_messages:
    role = "assistant" if message["role"] == "model" else "user"
    with st.chat_message(role):
        st.markdown(message["parts"][0]) 

# --- NHẬN INPUT VĂN BẢN (Giữ nguyên logic) ---
if prompt := st.chat_input("Hoặc gõ tin nhắn tự do ở đây..."):
    db.add_chat_message(current_user_id, "user", prompt)
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi tin nhắn tới Gemini và nhận phản hồi
    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = chat.send_message(prompt)
                response_text = response.text
                st.markdown(response_text)
                
                db.add_chat_message(current_user_id, "assistant", response_text)
                
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra: {e}")
