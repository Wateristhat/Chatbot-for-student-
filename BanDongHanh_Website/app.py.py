import streamlit as st

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS TÙY CHỈNH CHO CÁC THẺ TÍNH NĂNG ---
st.markdown("""
<style>
    /* Ẩn thanh điều hướng mặc định của Streamlit khi không cần */
    .st-emotion-cache-16txtl3 {
        padding-top: 2rem; /* Thêm khoảng trống ở trên */
    }
    .feature-card {
        background-color: #F0F2F5;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        border: 2px solid #0084FF;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .feature-card h2 {
        font-size: 1.5rem;
        color: #050505;
        margin-top: 1rem;
    }
    .feature-card-icon {
        font-size: 4rem; /* Kích thước icon lớn */
    }
</style>
""", unsafe_allow_html=True)


# --- NỘI DUNG TRANG GIỚI THIỆU ---

st.title("Chào mừng đến với Bạn Đồng Hành 💖")
st.header("Mình ở đây để cùng bạn trò chuyện và khám phá cảm xúc!")

st.write("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">💬</div>
            <h2>Trò chuyện</h2>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">📔</div>
            <h2>Nhật ký Cảm xúc</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-card-icon">🧘</div>
            <h2>Góc Thư giãn</h2>
        </div>
    """, unsafe_allow_html=True)

st.write("---")

st.info("👈 **Hãy chọn một người bạn ở thanh bên trái để bắt đầu nhé!**", icon="😊")
