# Trong file app.py
import streamlit as st
import database as db

# --- 1. KHỞI TẠO TRẠNG THÁI NHẠC NỀN (Chỉ làm ở app.py) ---
# Dán đoạn code này vào đây:
if 'music_playing' not in st.session_state:
    st.session_state.music_playing = False # Bắt đầu ở trạng thái TẮT 
if 'music_url' not in st.session_state:
    # ⚠️ Đây là link nhạc CỦA BẠN (đã được tạo):
    st.session_state.music_url = "https://cdn.jsdelivr.net/gh/Wateristhat/chatbot-for-student-/BanDongHanh_Website/lofi-piano-beat-305563.mp3" 
# ---------------------------------------------------------

db.create_tables() # <-- Giữ nguyên ở đây

st.switch_page("pages/0_💖_Trang_chủ.py") # <-- Giữ nguyên ở cuối cùng
