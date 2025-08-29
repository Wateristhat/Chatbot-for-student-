import streamlit as st
from datetime import datetime

# Cấu hình trang chính
st.set_page_config(
    page_title="Chào mừng - Trang chủ",
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
</style>
""", unsafe_allow_html=True)


# --- LOGIC HIỂN THỊ ---

# Khởi tạo session_state nếu chưa có
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# ---- GIAO DIỆN KHI CHƯA CÓ THÔNG TIN ----
if not st.session_state.user_name:
    st.title("Chào bạn, mình là Bạn Đồng Hành 💖")
    st.header("Trước khi bắt đầu, chúng mình làm quen nhé?")

    with st.form(key="welcome_form", clear_on_submit=True):
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        
        name = st.text_input("Bạn tên là gì?")
        
        current_year = datetime.now().year
        birth_year = st.selectbox(
            "Bạn sinh năm bao nhiêu?",
            options=range(current_year - 5, current_year - 25, -1)
        )
        
        school = st.text_input("Bạn đang học ở trường nào?")
        
        issues = st.text_area(
            "Gần đây, có điều gì khiến bạn cảm thấy khó khăn không? (trong học tập hoặc cuộc sống)",
            placeholder="Bạn có thể chia sẻ ở đây, mình luôn lắng nghe..."
        )
        
        submitted = st.form_submit_button("Lưu thông tin và bắt đầu!")
        
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

# ---- GIAO DIỆN SAU KHI ĐÃ CÓ THÔNG TIN ----
else:
    st.title(f"Chào mừng {st.session_state.user_name} đến với Bạn Đồng Hành 💖")
    
    st.markdown(
        """
        "Bạn Đồng Hành" được tạo ra với mong muốn trở thành một người bạn thấu cảm, 
        luôn ở bên cạnh để hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần.
        """
    )

    st.markdown("---")
    st.header("Khám phá các tính năng")
    st.markdown(
        """
        Dưới đây là các tính năng chính được thiết kế để giúp bạn cảm thấy tốt hơn mỗi ngày. 

        - **✨ Liều Thuốc Tinh Thần:** Nhận những thông điệp tích cực mỗi ngày.
        - **🧘 Góc An Yên:** Thực hành các bài tập hít thở để giảm căng thẳng.
        - **🍯 Lọ Biết Ơn:** Ghi lại những điều nhỏ bé khiến bạn mỉm cười.
        - **🎨 Vải Bố Vui Vẻ:** Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.
        - **🎲 Trò Chơi Trí Tuệ:** Thử thách bản thân với các trò chơi nhẹ nhàng.
        - **❤️ Góc Tự Chăm Sóc:** Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.
        - **💬 Trò chuyện cùng Bot:** Một người bạn AI luôn sẵn sàng lắng nghe bạn.
        - **🆘 Hỗ Trợ Khẩn Cấp:** Danh sách các nguồn lực và đường dây nóng đáng tin cậy.
        """
    )
    st.markdown("---")
    st.info("👈 **Hãy chọn một tính năng từ thanh điều hướng bên trái để bắt đầu!**", icon="😊")
