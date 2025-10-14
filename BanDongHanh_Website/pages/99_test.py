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
        
        # SỬA Ở ĐÂY: Đổi tên model thành "gemini-1.5-flash" hoặc "gemini-pro"
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        
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
# --- ĐOẠN CODE KIỂM TRA MODEL ---
st.subheader("Kiểm tra các model AI có sẵn")
st.markdown("Nhấn nút bên dưới để xem danh sách các model mà API key của bạn có thể sử dụng.")

if st.button("Liệt kê các model AI có thể dùng"):
    try:
        st.info("Đang lấy danh sách...")
        models_found = []
        # Lặp qua tất cả model mà Google cung cấp
        for m in genai.list_models():
            # Chỉ lấy những model hỗ trợ phương thức 'generateContent' (dùng để chat)
            if 'generateContent' in m.supported_generation_methods:
                models_found.append(m.name)

        if models_found:
            st.success("✅ Các model có thể sử dụng (đã lọc):")
            # Hiển thị danh sách dưới dạng code để dễ sao chép
            st.code('\n'.join(models_found))
            st.warning("Hãy sao chép một tên model từ danh sách trên (ví dụ: 'models/gemini-1.5-flash-001') và thay thế vào dòng `genai.GenerativeModel(...)` trong code của bạn.")
        else:
            st.error("Không tìm thấy model nào phù hợp. Vui lòng kiểm tra lại API key.")
            
    except Exception as e:
        st.error(f"Lỗi khi lấy danh sách model: {e}")
