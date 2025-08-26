import streamlit as st
from datetime import datetime

# ----------------- CẤU HÌNH TRANG -----------------
st.set_page_config(
    page_title="Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# ----------------- CSS PHONG CÁCH THỜI TRANG -----------------
st.markdown("""
<style>
    /* Toàn bộ nền trắng tinh, font sang trọng */
    body {
        background-color: #ffffff;
        font-family: 'Helvetica Neue', sans-serif;
        color: #222;
    }
    /* Tiêu đề lớn giống hero banner */
    .big-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        text-align: center;
        margin-top: 2rem;
    }
    /* Form trong khung tối giản */
    .form-container {
        background-color: #f9f9f9;
        border-radius: 15px;
        padding: 2rem 3rem;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    /* Nút bấm */
    .stButton>button {
        background-color: black;
        color: white;
        font-size: 1rem;
        border-radius: 30px;
        padding: 0.6rem 2rem;
        letter-spacing: 1px;
        border: none;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #444;
        transform: scale(1.02);
    }
    /* Mục tính năng như card */
    .feature-card {
        background-color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        transition: transform 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-4px);
    }
</style>
""", unsafe_allow_html=True)

# ----------------- LOGIC -----------------
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

if not st.session_state.user_name:
    st.markdown("<div class='big-title'>Chào mừng đến với Bạn Đồng Hành 💖</div>", unsafe_allow_html=True)
    st.markdown("### Hãy để chúng mình biết một chút về bạn")

    with st.form(key="welcome_form", clear_on_submit=True):
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)

        name = st.text_input("👤 Tên của bạn")
        current_year = datetime.now().year
        birth_year = st.selectbox("📅 Năm sinh", options=range(current_year - 5, current_year - 25, -1))
        school = st.text_input("🏫 Trường học")
        issues = st.text_area("💬 Chia sẻ điều khiến bạn bận tâm gần đây", placeholder="Mình luôn sẵn sàng lắng nghe...")

        submitted = st.form_submit_button("Bắt đầu hành trình")

        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not name:
                st.warning("Vui lòng cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state.user_info = {"year": birth_year, "school": school, "issues": issues}
                st.rerun()

else:
    st.markdown(f"<div class='big-title'>Xin chào, {st.session_state.user_name}</div>", unsafe_allow_html=True)
    st.write("✨ **Bạn Đồng Hành** muốn mang đến trải nghiệm chăm sóc tinh thần tinh tế như cách các thương hiệu thời trang chăm chút từng chi tiết.")

    st.markdown("---")
    st.subheader("Khám phá các tính năng")

    cols = st.columns(4)
    features = [
        ("✨ Liều Thuốc Tinh Thần", "Nhận những thông điệp tích cực mỗi ngày."),
        ("🧘 Góc An Yên", "Thư giãn và giảm căng thẳng."),
        ("🍯 Lọ Biết Ơn", "Ghi lại điều khiến bạn mỉm cười."),
        ("🎨 Vải Bố Vui Vẻ", "Thỏa sức sáng tạo.")
    ]

    for col, (title, desc) in zip(cols, features):
        with col:
            st.markdown(f"<div class='feature-card'><h3>{title}</h3><p>{desc}</p></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.info("Chọn một tính năng ở thanh bên trái để bắt đầu 🌸", icon="💡")
