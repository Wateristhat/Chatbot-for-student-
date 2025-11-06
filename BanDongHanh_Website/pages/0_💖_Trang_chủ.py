# File: 0_💖_Trang_chủ.py
import streamlit as st

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- LOGIC ĐĂNG NHẬP (Giữ nguyên) ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# Thêm CSS cơ bản cho đẹp mắt
st.markdown("""
<style>
    .brand-minimal-box {
        background: linear-gradient(110deg, #ff82ac 3%, #fd5e7c 97%);
        border-radius: 38px;
        padding: 2.3rem;
        margin-bottom: 2.5rem;
        max-width: 700px;
        box-shadow: 0 8px 32px rgba(255,88,88,0.08);
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


if not st.session_state.user_name:
    # --- Giao diện chưa đăng nhập ---
    st.markdown("""
    <div class="brand-minimal-box">
        Chào mừng bạn đến với Bạn Đồng Hành! 💖
    </div>
    """, unsafe_allow_html=True)

    st.title("👋 Chào bạn, mình là Bạn Đồng Hành")
    st.header("Trước khi bắt đầu, chúng mình làm quen nhé?")

    with st.form(key="welcome_form", clear_on_submit=True):
        name = st.text_input("📝 Bạn tên là gì?")
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        if submitted:
            if not name:
                st.warning("⚠️ Vui lòng cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state['user_id'] = name
                st.success("✅ Lưu thông tin thành công! Chào mừng bạn!")
                st.rerun()
else:
    # --- Giao diện đã đăng nhập ---
    st.markdown(f"""
    <div class="brand-minimal-box">
        Chào mừng {st.session_state.user_name} trở lại! 🌟
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## ✨ Khám phá các tính năng")
    st.info("Vui lòng sử dụng Menu ở thanh bên trái để điều hướng giữa các tính năng.")
    
    if st.button("❌ Đăng xuất", key="logout_btn"):
        st.session_state.user_name = None
        st.session_state.user_id = None
        st.rerun()

