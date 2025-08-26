# pages/Nhanh_tay_le_mat.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Nhanh Tay Lẹ Mắt", page_icon="🎮", layout="centered")

# --- KIỂM TRA ĐĂNG NHẬP ---
# Đảm bảo người dùng đã đăng nhập trước khi truy cập
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

# --- GIAO DIỆN CHÍNH ---
st.title("🎮 Nhanh Tay Lẹ Mắt")

# --- Liên kết quay về Trang chủ ---
st.page_link("Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown(
    "<div style='font-size:1.15rem'>"
    "Hãy nhấn phím **SPACE** để bắt đầu và giúp nhân vật nhảy qua các chướng ngại vật.<br>"
    "<b>Chúc bạn có những giây phút thư giãn vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# --- NHÚNG GAME HTML5 ---
# *** SỬA LỖI QUAN TRỌNG: URL của game ***
# Sử dụng URL từ GitHub Pages (github.io) thay vì raw.githubusercontent.com để game hiển thị chính xác.
game_url = "https://wateristhat.github.io/Chatbot-for-student-/BanDongHanh_Website/game.html"
game_html = f"""
<iframe src="{game_url}" width="480" height="400" frameborder="0" scrolling="no"></iframe>
"""

# Hiển thị game bằng st.components.v1.html
st.components.v1.html(game_html, height=410)
