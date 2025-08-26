# pages/Lo_biet_on.py
import streamlit as st
import database as db
import html
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Lọ Biết Ơn", page_icon="🍯", layout="centered")

# --- KIỂM TRA ĐĂNG NHẬP ---
# Đảm bảo người dùng đã đăng nhập trước khi truy cập
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

# --- LẤY DỮ LIỆU TỪ SESSION STATE ---
user_id = st.session_state.user_id
user_name = st.session_state.user_name

# --- GIAO DIỆN CHÍNH ---
st.title("🍯 Lọ Biết Ơn")

# *** ĐÃ THÊM: Liên kết quay về Trang chủ ***
st.page_link("Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown(f"Chào **{user_name}**, hôm nay có điều gì khiến bạn mỉm cười không?")

# Khu vực nhập liệu
note_text = st.text_area(
    "Viết điều bạn biết ơn vào đây...", 
    height=100, 
    key="gratitude_input"
)

if st.button("Thêm vào lọ biết ơn", type="primary", use_container_width=True):
    if note_text:
        db.add_gratitude_note(user_id, note_text)
        st.success("Đã thêm một hạt mầm biết ơn vào lọ! 🌱")
        st.balloons()
        time.sleep(1) # Chờ 1 giây để người dùng thấy thông báo
        st.rerun()
    else:
        st.warning("Bạn hãy viết gì đó nhé!")

st.write("---")

# --- HIỂN THỊ CÁC GHI CHÚ ĐÃ CÓ ---
# Lấy danh sách ghi chú từ database
gratitude_notes = db.get_gratitude_notes(user_id)

if gratitude_notes:
    st.subheader("Những điều bạn biết ơn:")
    
    # Đảo ngược danh sách để hiển thị ghi chú mới nhất lên đầu
    gratitude_notes.reverse()
    
    # Lặp qua từng ghi chú và hiển thị cùng nút xóa
    for note_id, note_content in gratitude_notes:
        col1, col2 = st.columns([10, 1]) # Chia cột, cột 2 chứa nút xóa
        
        with col1:
            # Sử dụng html.escape để tránh lỗi bảo mật XSS
            safe_content = html.escape(note_content)
            st.markdown(
                f'<div style="background-color: #FFF8DC; border-left: 5px solid #FFD700; padding: 1rem; border-radius: 5px; margin-bottom: 10px; min-height: 50px; display: flex; align-items: center;">'
                f'<p style="color: #333; margin: 0;">{safe_content}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
        
        with col2:
            # Nút xóa cho từng ghi chú, sử dụng note_id làm key duy nhất
            if st.button("🗑️", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                db.delete_gratitude_note(note_id)
                st.toast("Đã xóa ghi chú!")
                time.sleep(1)
                st.rerun()

else:
    st.info("Chiếc lọ của bạn đang chờ những điều biết ơn đầu tiên. ❤️")
