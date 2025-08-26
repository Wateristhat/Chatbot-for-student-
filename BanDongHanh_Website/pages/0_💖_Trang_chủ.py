# pages/0_💖_Trang_chủ.py
import streamlit as st
import database as db
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS (Giữ nguyên) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* (Toàn bộ CSS của bạn được giữ nguyên ở đây) */
</style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO SESSION STATE ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- GIAO DIỆN CHÍNH ---
st.title("Chào mừng đến với Bạn Đồng Hành 💖")

# GIAO DIỆN KHI CHƯA ĐĂNG NHẬP
if not st.session_state.get('user_id'):
    st.markdown("Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])

    # --- Tab Đăng nhập ---
    with tab1:
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập", placeholder="Nhập tên của bạn...")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...")
            submitted = st.form_submit_button("Vào thôi!")
            if submitted:
                user = db.check_user(username, password)
                if user:
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không chính xác!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Tab Đăng ký ---
    with tab2:
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        with st.form(key="signup_form"):
            name = st.text_input("📝 Bạn tên là gì?", placeholder="Tên bạn sẽ hiển thị trong ứng dụng")
            password_reg = st.text_input("🔑 Mật khẩu của bạn", type="password", placeholder="Chọn một mật khẩu an toàn")
            
            if st.form_submit_button("💖 Tạo tài khoản và bắt đầu!"):
                if not name or not password_reg:
                    st.warning("⚠️ Tên và mật khẩu không được để trống bạn nhé!")
                else:
                    # Chỉ truyền 2 tham số như hàm trong database.py yêu cầu
                    if db.add_user(name, password_reg):
                        st.success(f"Tài khoản '{name}' đã được tạo! Vui lòng qua tab Đăng nhập.")
                        time.sleep(2)
                    else:
                        st.error("Tên này đã có người dùng. Vui lòng chọn tên khác.")
        st.markdown("</div>", unsafe_allow_html=True)

# GIAO DIỆN KHI ĐÃ ĐĂNG NHẬP
else:
    # (Phần này giữ nguyên như cũ)
    st.title(f"Hôm nay bạn thế nào, {st.session_state.user_name}? ✨")
    # ... (phần hiển thị các tính năng)

