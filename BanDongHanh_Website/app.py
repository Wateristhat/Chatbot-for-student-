import streamlit as st
from datetime import datetime

# Cấu hình trang chính
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS TÙY CHỈNH ---
st.markdown("""
<style>
    .main-container {
        padding: 2rem;
    }
    .welcome-form {
        background-color: #F0F2F5;
        border-radius: 10px;
        padding: 2rem;
        margin-top: 2rem;
    }
    .feature-card {
        background-color: #F0F2F5;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        text-align: center;
        transition: all 0.3s;
        border: 2px solid transparent;
        color: #050505;
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
        font-size: 4rem;
    }
</style>
""", unsafe_allow_html=True)


# --- LOGIC HIỂN THỊ ---

# Kiểm tra xem thông tin người dùng đã được lưu chưa
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# Nếu chưa có thông tin, hiển thị form "làm quen"
if not st.session_state.user_name:
    st.title("Chào bạn, mình là Bạn Đồng Hành 💖")
    st.header("Trước khi bắt đầu, chúng mình làm quen nhé?")

    with st.form(key="welcome_form", clear_on_submit=True):
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        
        name = st.text_input("Bạn tên là gì?")
        
        # Tạo danh sách các năm sinh để người dùng lựa chọn
        current_year = datetime.now().year
        birth_year = st.selectbox(
            "Bạn sinh năm bao nhiêu?",
            options=range(current_year - 5, current_year - 25, -1) # Cho học sinh từ 5 đến 25 tuổi
        )
        
        school = st.text_input("Bạn đang học ở trường nào?")
        
        issues = st.text_area(
            "Gần đây, có điều gì khiến bạn cảm thấy khó khăn không? (trong học tập hoặc cuộc sống)",
            placeholder="Bạn có thể chia sẻ ở đây, mình luôn lắng nghe..."
        )
        
        submitted = st.form_submit_button("Bắt đầu hành trình!")
        
        if submitted:
            if not name:
                st.warning("Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state.user_info = {
                    "year": birth_year,
                    "school": school,
                    "issues": issues
                }
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

# Nếu đã có thông tin, hiển thị trang giới thiệu được cá nhân hóa
else:
    st.title(f"Chào mừng {st.session_state.user_name} đến với Bạn Đồng Hành 💖")
    st.header("Một không gian an toàn cho sức khỏe tinh thần của bạn")
    st.markdown("---")

    st.markdown(
        """
        "Bạn Đồng Hành" được tạo ra với mong muốn trở thành một người bạn thấu cảm, 
        luôn ở bên cạnh để hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần.
        """
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown('<div class="feature-card"><div class="feature-card-icon">💬</div><h2>Trò chuyện</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="feature-card"><div class="feature-card-icon">🍯</div><h2>Lọ Biết Ơn</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="feature-card"><div class="feature-card-icon">🧘</div><h2>Góc An Yên</h2></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="feature-card"><div class="feature-card-icon">🎲</div><h2>Trò Chơi</h2></div>', unsafe_allow_html=True)

    st.info("👈 **Hãy chọn một tính năng từ thanh điều hướng bên trái để bắt đầu nhé!**", icon="😊")
