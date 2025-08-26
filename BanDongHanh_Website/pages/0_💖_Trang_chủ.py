# pages/0_Trang_chu.py
import streamlit as st
import database as db
import time

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

st.title("Chào mừng đến với Bạn Đồng Hành 💖")
st.markdown("Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")

if not st.session_state.get('user_id'):
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập", placeholder="Nhập tên của bạn...")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...")
            submitted = st.form_submit_button("Vào thôi!")
            if submitted:
                if not username or not password:
                    st.error("Vui lòng điền đầy đủ tên đăng nhập và mật khẩu.")
                else:
                    user = db.check_user(username, password)
                    if user:
                        st.session_state.user_id = user[0]
                        st.session_state.user_name = user[1]
                        st.rerun()
                    else:
                        st.error("Tên đăng nhập hoặc mật khẩu không chính xác!")

    with tab2:
        with st.form(key="signup_form"):
            name = st.text_input("📝 Bạn tên là gì?", placeholder="Tên bạn sẽ hiển thị trong ứng dụng")
            password_reg = st.text_input("🔑 Mật khẩu của bạn", type="password", placeholder="Chọn một mật khẩu an toàn")

            if st.form_submit_button("💖 Tạo tài khoản và bắt đầu!"):
                if not name or not password_reg:
                    st.warning("⚠️ Tên và mật khẩu không được để trống bạn nhé!")
                else:
                    if db.add_user(name, password_reg):
                        st.success(f"Tài khoản '{name}' đã được tạo! Vui lòng qua tab Đăng nhập.")
                    else:
                        st.error("Tên này đã có người dùng. Vui lòng chọn tên khác.")

else:
    st.title(f"Hôm nay bạn thế nào, {st.session_state.user_name}? ✨")
    st.markdown("Chào mừng bạn đã trở lại! Hãy khám phá các tính năng của chúng mình nhé.")

    st.markdown("---")
    st.subheader("Các tính năng chính của ứng dụng:")

    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/1_Lieu_thuoc_tinh_than.py", label="Liệu thuốc tinh thần", icon="✨")
        st.page_link("pages/2_Goc_an_yen.py", label="Góc an yên", icon="🍃")
        st.page_link("pages/3_Lo_biet_on.py", label="Lọ biết ơn", icon="💌")
    with col2:
        st.page_link("pages/4_Bang_mau_cam_xuc.py", label="Bảng màu cảm xúc", icon="🎨")
        st.page_link("pages/5_Nhanh_tay_le_mat.py", label="Nhanh tay lẹ mắt", icon="🏃‍♀️")
        st.page_link("pages/6_Goc_nho.py", label="Góc nhỏ", icon="🏠")
        st.page_link("pages/8_Tro_chuyen_cung_Bot.py", label="Trò chuyện cùng Bot", icon="💬")

    st.markdown("---")

    if st.button("🚪 Đăng xuất", type="primary"):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
