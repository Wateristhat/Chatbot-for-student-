import streamlit as st
import database as db
import html
import time 

st.set_page_config(page_title="Lọ Biết Ơn", page_icon="🍯", layout="centered")
st.title("🍯 Lọ Biết Ơn")

# --- KIỂM TRA VÀ KHÔI PHỤC SESSION STATE ---
# Kiểm tra query parameters để khôi phục session state nếu cần
query_params = st.query_params
if 'user_id' in query_params and not st.session_state.get('user_id'):
    try:
        # Khôi phục session state từ query parameters
        user_id = int(query_params['user_id'])
        user_name = query_params.get('user_name', '')
        if user_id and user_name:
            st.session_state.user_id = user_id
            st.session_state.user_name = user_name
    except (ValueError, KeyError):
        pass

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

# --- LẤY DỮ LIỆU TỪ DB ---
user_id = st.session_state.user_id
gratitude_notes = db.get_gratitude_notes(user_id)

st.markdown(f"Chào {st.session_state.user_name}, hôm nay có điều gì khiến bạn mỉm cười không?")

note = st.text_area("Viết điều bạn biết ơn vào đây...", height=100)

if st.button("Thêm vào lọ biết ơn", type="primary"):
    if note:
        db.add_gratitude_note(user_id, note)
        st.success("Đã thêm một hạt mầm biết ơn vào lọ! 🌱")
        st.balloons()
        time.sleep(1) # Dòng này bây giờ sẽ hoạt động bình thường
        st.rerun()
    else:
        st.warning("Bạn hãy viết gì đó nhé!")

st.write("---")

if gratitude_notes:
    st.subheader("Những điều bạn biết ơn:")
    for n in gratitude_notes:
        st.markdown(
            f'<div style="background-color: #FFF8DC; border-left: 5px solid #FFD700; padding: 10px; border-radius: 5px; margin-bottom: 10px;"><p style="color: #333;">{html.escape(n)}</p></div>',
            unsafe_allow_html=True
        )
else:
    st.write("Chiếc lọ của bạn đang chờ những điều biết ơn đầu tiên. ❤️")

