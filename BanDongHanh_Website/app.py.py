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
    
    /* MODIFIED: Thêm style cho thẻ link để bỏ gạch chân */
    a.feature-card-link {
        text-decoration: none;
    }

    .feature-card {
        background-color: #F0F2F5;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s;
        border: 2px solid transparent;
        color: #050505; /* Đảm bảo chữ có màu */
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

# MODIFIED: Bọc mỗi thẻ trong một thẻ link <a> với thuộc tính href
# target="_self" để đảm bảo trang được mở trên cùng một tab
with col1:
    st.markdown("""
        <a href="/Trò_chuyện" target="_self" class="feature-card-link">
            <div class="feature-card">
                <div class="feature-card-icon">💬</div>
                <h2>Trò chuyện</h2>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <a href="/Nhật_ký_cảm_xúc" target="_self" class="feature-card-link">
            <div class="feature-card">
                <div class="feature-card-icon">📔</div>
                <h2>Nhật ký Cảm xúc</h2>
            </div>
        </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <a href="/Góc_thư_giãn" target="_self" class="feature-card-link">
            <div class="feature-card">
                <div class="feature-card-icon">🧘</div>
                <h2>Góc Thư giãn</h2>
            </div>
        </a>
    """, unsafe_allow_html=True)

st.write("---")

st.info("👈 **Bạn cũng có thể chọn một tính năng từ thanh bên trái!**", icon="😊")
