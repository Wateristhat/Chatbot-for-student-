import streamlit as st
import database as db  # Import file database
import html
import time

st.set_page_config(page_title="Lọ Biết Ơn", page_icon="🍯", layout="centered")
st.title("🍯 Lọ Biết Ơn")

# --- BƯỚC 1: KIỂM TRA XEM NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP CHƯA ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()  # Dừng chạy code nếu chưa đăng nhập

# --- BƯỚC 2: LẤY DỮ LIỆU CỦA ĐÚNG NGƯỜI DÙNG TỪ DATABASE ---
user_id = st.session_state.user_id
gratitude_notes = db.get_gratitude_notes(user_id)

st.markdown(f"Chào {st.session_state.user_name}, hôm nay có điều gì khiến bạn mỉm cười không?")

note = st.text_area("Viết điều bạn biết ơn vào đây...", height=100)

if st.button("Thêm vào lọ biết ơn", type="primary"):
    if note:
        # --- BƯỚC 3: LƯU GHI CHÚ MỚI VÀO DATABASE ---
        db.add_gratitude_note(user_id, note)
        st.success("Đã thêm một hạt mầm biết ơn vào lọ! 🌱")
        st.balloons()
        time.sleep(1) # Chờ 1 giây để người dùng thấy hiệu ứng
        st.rerun()
    else:
        st.warning("Bạn hãy viết gì đó nhé!")

st.write("---")

if gratitude_notes:
    st.subheader("Những điều bạn biết ơn:")
    # Hiển thị các ghi chú đã lấy từ database
    for n in gratitude_notes:
        st.markdown(
            f'<div style="background-color: #FFF8DC; border-left: 5px solid #FFD700; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><p style="color: #333;">{html.escape(n)}</p></div>',
            unsafe_allow_html=True
        )
else:
    st.write("Chiếc lọ của bạn đang chờ những điều biết ơn đầu tiên. ❤️")
