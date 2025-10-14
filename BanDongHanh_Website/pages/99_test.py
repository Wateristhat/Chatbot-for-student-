import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH TRANG VÀ CSS TÙY CHỈNH ---
st.set_page_config(
    page_title="Chatbot AI Đầy Màu Sắc",
    page_icon="🌈",
    layout="centered"
)

# CSS để làm cho giao diện màu mè, giống phong cách bạn muốn
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
        background: linear-gradient(to right, #6a11cb, #2575fc); /* Gradient tím và xanh cho chữ */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }

    /* Bong bóng chat của người dùng (user) */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-user"]) {
        background-color: #ffffff; /* Nền trắng */
        border-radius: 20px 20px 5px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-right: 10%; /* Thu hẹp lại một chút */
        border: 1px solid #e0e0e0;
    }

    /* Bong bóng chat của trợ lý (assistant) */
    [data-testid="stChatMessage"]:has([data-testid="stAvatarIcon-assistant"]) {
        background: linear-gradient(to right, #d2b4de, #a0d2eb); /* Gradient tím nhạt và xanh nhạt */
        border-radius: 20px 20px 20px 5px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-left: 10%; /* Thu hẹp lại một chút */
        color: #1e1e1e; /* Màu chữ tối để dễ đọc */
    }

    /* Ô nhập liệu chat */
    [data-testid="stChatInput"] {
        background-color: #ffffff;
        border-radius: 25px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        padding: 5px 15px;
    }

    /* Nút gửi tin nhắn */
    [data-testid="stChatInput"] button {
        background-color: #8e44ad; /* Màu tím đậm */
        border-radius: 50%;
        color: white;
    }
    [data-testid="stChatInput"] button:hover {
        background-color: #9b59b6; /* Tím nhạt hơn khi hover */
    }
</style>
""", unsafe_allow_html=True)


# --- 2. CODE GỐC CỦA BẠN (GIỮ NGUYÊN) ---

st.title("✨ Chatbot AI Đồng Hành ✨")
st.caption("Trò chuyện với mô hình AI Gemini của Google.")

# --- CẤU HÌNH GEMINI AI ---
# Sử dụng @st.cache_resource để chỉ khởi tạo model một lần
@st.cache_resource
def configure_gemini():
    """
    Cấu hình và trả về model Gemini.
    Hiển thị lỗi nếu API key không được cung cấp.
    """
    try:
        # Lấy API key từ Streamlit secrets
        api_key = st.secrets["GOOGLE_API_KEY"]
        genai.configure(api_key=api_key)
        
        # Dòng này bạn đã sửa để dùng model chính xác
        model = genai.GenerativeModel("models/gemini-2.5-pro")
        
        return model
    except (KeyError, ValueError) as e:
        st.error("Lỗi: Vui lòng cấu hình GOOGLE_API_KEY trong file secrets.toml.")
        st.info("Xem hướng dẫn tại: [Link hướng dẫn nếu có]")
        st.stop() # Dừng ứng dụng nếu không có key

# Khởi tạo model
model = configure_gemini()

# --- KHỞI TẠO LỊCH SỬ CHAT ---
# Bắt đầu một session chat mới với Gemini
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# --- HIỂN THỊ CÁC TIN NHẮN CŨ ---
# Lấy lịch sử từ session chat của Gemini
for message in st.session_state.chat.history:
    # Phân biệt vai trò "user" (người dùng) và "model" (AI)
    role = "assistant" if message.role == "model" else message.role
    with st.chat_message(role):
        st.markdown(message.parts[0].text)

# --- NHẬN INPUT TỪ NGƯỜI DÙNG VÀ XỬ LÝ ---
if prompt := st.chat_input("Hỏi AI bất cứ điều gì..."):
    # Hiển thị tin nhắn của người dùng ngay lập tức
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gửi tin nhắn tới Gemini và nhận phản hồi
    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                # Gửi prompt và nhận response
                response = st.session_state.chat.send_message(prompt)
                # Hiển thị phản hồi từ AI
                st.markdown(response.text)
            except Exception as e:
                # Xử lý các lỗi có thể xảy ra (ví dụ: lỗi kết nối, nội dung bị chặn)
                st.error(f"Đã có lỗi xảy ra: {e}")
