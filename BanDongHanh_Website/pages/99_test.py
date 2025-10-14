import streamlit as st
import google.generativeai as genai
import random
# 1. ADD THIS NEW IMPORT LINE
from google.generativeai.types import Content, Part

# --- CẤU HÌNH TRANG VÀ CSS TÙY CHỈNH (Giữ nguyên giao diện màu mè) ---
st.set_page_config(
    page_title="Chatbot AI Đồng Hành",
    page_icon="🌈",
    layout="centered"
)

# CSS để làm cho giao diện màu mè
st.markdown("""
<style>
    /* Nền và font chữ tổng thể */
    body {
        font-family: 'Segoe UI', sans-serif;
    }
    .stApp {
        background: linear-gradient(to right, #fde4f2, #e6e6fa); /* Gradient nền hồng và tím lavender */
    }
    /* Tiêu đề chính */
    h1 {
        font-size: 2.5em;
        text-align: center;
        background: linear-gradient(to right, #6a11cb, #2575fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    /* Bong bóng chat */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-user"]) {
        background-color: #ffffff;
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
    }
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-assistant"]) {
        background: linear-gradient(to right, #d2b4de, #a0d2eb);
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #1e1e1e;
    }
    /* Ô nhập liệu chat */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        padding: 5px 15px;
    }
    /* Nút bấm lớn */
    .stButton > button {
        border-radius: 12px;
        font-size: 1.1em;
        font-weight: bold;
        padding: 10px 20px;
        width: 100%; /* Giúp các nút bằng nhau */
    }
</style>
""", unsafe_allow_html=True)

# --- CẤU HÌNH DỮ LIỆU TỪ SƯỜN CODE ---
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
        "positive_affirmations": [
            "Bạn đã làm rất tốt khi chia sẻ cảm xúc của mình. Khi nào cần, mình vẫn luôn ở đây nha 💫",
            "Bạn thật mạnh mẽ khi đối mặt với cảm xúc của mình. Mình tự hào về bạn!",
            "Mỗi bước nhỏ bạn đi đều là một thành công lớn. Cố lên nhé!",
            "Bạn xứng đáng được yêu thương và hạnh phúc.",
        ]
    },
    "giao_tiep": {
        "intro_message": "Hãy chọn một tình huống bên dưới để mình cùng luyện tập nhé!",
        "scenarios_basic": {
            "👋 Chào hỏi bạn bè": "Bạn có thể nói: ‘Chào bạn, hôm nay vui không?’ Hoặc: ‘Tớ chào cậu nha, hôm nay học tốt không nè?’",
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

if "chat" not in st.session_state:
    st.session_state.chat = None

# 2. CORRECT THIS FUNCTION
def add_bot_message_to_history(text):
    """Hàm này thêm tin nhắn của bot vào lịch sử chat của Gemini."""
    # Use Content() and Part() directly without the 'genai.types' prefix
    st.session_state.chat.history.append(Content(
        parts=[Part(text=text)],
        role="model"
    ))

# --- PHẦN CODE CHÍNH ---
st.title("✨ Chatbot AI Đồng Hành ✨")
st.caption("Trò chuyện với mô hình AI Gemini của Google.")

@st.cache_resource
def configure_gemini():
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("models/gemini-2.5-pro")
        return model
    except Exception as e:
        st.error("Lỗi: Vui lòng cấu hình GOOGLE_API_KEY trong file secrets.toml.")
        st.stop()

model = configure_gemini()

if st.session_state.chat is None:
    st.session_state.chat = model.start_chat(history=[])

# --- GIAO DIỆN NÚT BẤM TƯƠNG TÁC ---
button_container = st.container()
with button_container:
    if st.session_state.chat_mode == "main":
        col1, col2 = st.columns(2)
        if col1.button("💖 Tâm sự"):
            st.session_state.chat_mode = "tam_su_selection"
            add_bot_message_to_history(CONFIG["tam_su"]["intro_message"])
            st.rerun()

        if col2.button("🗣️ Giao tiếp"):
            st.session_state.chat_mode = "giao_tiep_selection"
            add_bot_message_to_history(CONFIG["giao_tiep"]["intro_message"])
            st.rerun()

    elif st.session_state.chat_mode == "tam_su_selection":
        st.write("Hôm nay bạn cảm thấy thế nào?")
        emotions = list(CONFIG["tam_su"]["emotions"].keys())
        cols = st.columns(len(emotions))
        for i, emotion in enumerate(emotions):
            if cols[i].button(emotion):
                response_text = CONFIG["tam_su"]["emotions"][emotion]
                add_bot_message_to_history(response_text)
                st.session_state.chat_mode = "main" 
                st.rerun()

    elif st.session_state.chat_mode == "giao_tiep_selection":
        st.write("Chọn tình huống bạn muốn luyện tập:")
        for scenario, example in CONFIG["giao_tiep"]["scenarios_basic"].items():
            if st.button(scenario, key=scenario):
                st.session_state.chat_mode = "giao_tiep_practice"
                add_bot_message_to_history(example)
                st.rerun()
        if st.button("↩️ Quay lại"):
             st.session_state.chat_mode = "main"
             st.rerun()

    elif st.session_state.chat_mode == "giao_tiep_practice":
        col1, col2 = st.columns(2)
        if col1.button(CONFIG["giao_tiep"]["confirm_buttons"]["understood"]):
            add_bot_message_to_history("Tuyệt vời! Bạn làm tốt lắm. Khi nào cần cứ tìm mình nhé.")
            st.session_state.chat_mode = "main"
            st.rerun()
        if col2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"]):
            add_bot_message_to_history("Không sao cả, mình nói lại nhé. Bạn hãy đọc kỹ lại câu mẫu phía trên nha.")
            st.rerun()

# --- HIỂN THỊ LỊCH SỬ CHAT ---
for message in st.session_state.chat.history:
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- NHẬN INPUT VĂN BẢN ---
if prompt := st.chat_input("Hoặc gõ tin nhắn tự do ở đây..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                response = st.session_state.chat.send_message(prompt)
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Đã có lỗi xảy ra: {e}")
