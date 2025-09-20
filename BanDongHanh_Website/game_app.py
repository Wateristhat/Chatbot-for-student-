import streamlit as st
import os

st.set_page_config(page_title="Trò chơi tránh vật cản", page_icon="🎮")

st.title("🎮 Trò chơi Tránh Vật Cản")
st.markdown(
    "<div style='font-size:1.15rem'>"
    "Hãy nhấn phím SPACE để chơi trò chơi! Tránh các vật cản để ghi điểm.<br>"
    "<b>Chúc bạn chơi vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Nhúng trò chơi HTML5
# Đường dẫn đến file game.html
game_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "game.html")

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
    
    # Fallback: Hiển thị thông báo
    st.warning("Đang tải game bằng phương pháp dự phòng...")
    game_html = """
    <iframe src="game.html" width="480" height="400" frameborder="0"></iframe>
    """
    st.components.v1.html(game_html, height=400)
