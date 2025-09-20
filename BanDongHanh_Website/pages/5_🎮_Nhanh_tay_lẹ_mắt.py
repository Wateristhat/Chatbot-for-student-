import streamlit as st
import os

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Nhanh Tay Lẹ Mắt", page_icon="🎮", layout="centered")

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
# Đường dẫn đến file game.html
game_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.html")

try:
    # Đọc nội dung file game.html và nhúng trực tiếp
    with open(game_file_path, "r", encoding="utf-8") as file:
        game_html_content = file.read()
    
    # Hiển thị game bằng st.components.v1.html với nội dung HTML trực tiếp
    st.components.v1.html(game_html_content, height=420)
    
except FileNotFoundError:
    st.error("Không tìm thấy file game.html. Vui lòng kiểm tra lại đường dẫn file.")
    st.info("File game.html cần được đặt trong thư mục BanDongHanh_Website.")
except Exception as e:
    st.error(f"Có lỗi xảy ra khi tải game: {str(e)}")
    
    # Fallback: Hiển thị iframe với GitHub Pages URL (nếu được bật)
    st.info("Đang thử tải game từ GitHub Pages...")
    game_url = "https://wateristhat.github.io/Chatbot-for-student-/BanDongHanh_Website/game.html"
    game_html = f"""
    <iframe src="{game_url}" width="480" height="400" frameborder="0" scrolling="no"></iframe>
    """
    st.components.v1.html(game_html, height=410)
