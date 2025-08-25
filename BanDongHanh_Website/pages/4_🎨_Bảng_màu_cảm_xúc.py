import streamlit as st
from streamlit_drawable_canvas import st_canvas

st.set_page_config(page_title="Bảng màu vui vẻ", page_icon="🎨", layout="wide")

st.info(
    """
    **Lưu ý:** Lần đầu sử dụng, bạn cần cài đặt thư viện cho tính năng này bằng lệnh: `pip install streamlit-drawable-canvas`
    """
)

st.title("🎨 Bảng màu vui vẻ")
st.markdown("""
Đây là không gian để bạn tự do thể hiện. Không cần phải vẽ đẹp, không cần phải có ý nghĩa. 
Hãy cứ để tay bạn di chuyển theo cảm xúc.
""")
st.write("---")

col1, col2 = st.columns([1, 1])
with col1:
    stroke_width = st.slider("Độ dày nét bút:", 1, 50, 10)
    drawing_mode = st.selectbox(
        "Công cụ:",
        ("freedraw", "line", "rect", "circle", "transform"),
    )
with col2:
    stroke_color = st.color_picker("Màu bút:", "#FF5733")
    bg_color = st.color_picker("Màu nền:", "#FFFFFF")

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
