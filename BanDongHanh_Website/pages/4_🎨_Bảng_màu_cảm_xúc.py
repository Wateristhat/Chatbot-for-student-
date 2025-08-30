import streamlit as st
from streamlit_drawable_canvas import st_canvas

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Bảng màu cảm xúc", page_icon="🎨", layout="wide")

# --- GIAO DIỆN CHÍNH ---
st.title("🎨 Bảng màu cảm xúc")

# *** SỬA LẠI ĐÚNG ĐƯỜNG DẪN ***
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown("""
Đây là không gian để bạn tự do thể hiện. Không cần phải vẽ đẹp, không cần phải có ý nghĩa.  
Hãy chọn một **màu sắc** thể hiện cảm xúc của bạn lúc này và để tay bạn di chuyển một cách tự nhiên.
""")
st.write("---")

# --- KHU VỰC TÙY CHỌN CÔNG CỤ VẼ ---
col1, col2 = st.columns(2)
with col1:
    stroke_width = st.slider("Độ dày nét bút:", min_value=1, max_value=50, value=10)
    drawing_mode = st.selectbox(
        "Công cụ:",
        ("freedraw", "line", "rect", "circle", "transform"),
        help="Chọn 'freedraw' để vẽ tự do, các công cụ khác để vẽ hình học."
    )
with col2:
    stroke_color = st.color_picker("Màu bút:", "#FF5733")
    bg_color = st.color_picker("Màu nền:", "#FFFFFF")

# --- KHUNG VẼ CANVAS ---
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
    background_color=bg_color,
    height=500,
    drawing_mode=drawing_mode,
    key="canvas",
    display_toolbar=True,
)

# --- THÔNG BÁO HƯỚNG DẪN CÀI ĐẶT ---
with st.expander("Gặp lỗi khi chạy trang này?"):
    st.info(
        """
        **Lưu ý:** Lần đầu sử dụng, bạn cần cài đặt thư viện cho tính năng này.
        Mở Terminal hoặc Command Prompt và chạy lệnh sau:
        ```bash
        pip install streamlit-drawable-canvas
        ```
        Sau đó, hãy làm mới lại trang web.
        """
    )
