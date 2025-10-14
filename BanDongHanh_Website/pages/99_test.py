import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="Chatbot AI Gemini", page_icon="✨")
st.title("✨ Chatbot AI với Gemini")
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
        # Chọn model, "gemini-1.5-flash-latest" nhanh và hiệu quả
        model = genai.GenerativeModel("gemini-1.5-flash-latest")
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
