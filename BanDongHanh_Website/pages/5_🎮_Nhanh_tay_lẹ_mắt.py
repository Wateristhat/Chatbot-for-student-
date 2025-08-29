# pages/5_🎮_Nhanh_tay_le_mat.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Nhanh Tay Lẹ Mắt", page_icon="🎮", layout="centered")

# --- LOGIN CHECK REMOVED - All features now accessible without login ---

# --- GIAO DIỆN CHÍNH ---
st.title("🎮 Nhanh Tay Lẹ Mắt")

# *** SỬA LẠI ĐÚNG ĐƯỜNG DẪN ***
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown(
    "<div style='font-size:1.15rem'>"
    "Hãy nhấn phím **SPACE** để bắt đầu và giúp nhân vật nhảy qua các chướng ngại vật.<br>"
    "<b>Chúc bạn có những giây phút thư giãn vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# --- NHÚNG GAME HTML5 ---
game_url = "https://wateristhat.github.io/Chatbot-for-student-/BanDongHanh_Website/game.html"
game_html = f"""
<iframe src="{game_url}" width="480" height="400" frameborder="0" scrolling="no"></iframe>
"""

# Hiển thị game bằng st.components.v1.html
st.components.v1.html(game_html, height=410)
