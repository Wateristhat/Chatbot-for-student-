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
                # Lưu thông tin vào session state
                st.session_state.user_name = name
                st.session_state.user_info = {
                    "year": birth_year,
                    "school": school,
                    "issues": issues
                }
                st.rerun() # Tải lại trang để hiển thị giao diện mới
                
        st.markdown("</div>", unsafe_allow_html=True)

# ---- GIAO DIỆN SAU KHI ĐÃ CÓ THÔNG TIN ----
else:
    st.title(f"Chào mừng {st.session_state.user_name} đến với Bạn Đồng Hành 💖")
    
    st.markdown(
        """
        **Bạn Đồng Hành** là một không gian an toàn, được xây dựng với mục tiêu hỗ trợ và nâng cao 
        năng lực giao tiếp cho các bạn học sinh hòa nhập tại Việt Nam. 
        
        Mình ở đây để trở thành một người bạn thấu cảm, luôn bên cạnh để hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần.
        """
    )

    st.markdown("---")

    st.header("Khám phá các tính năng")

    st.markdown(
        """
        Dưới đây là 9 tính năng chính được thiết kế để giúp bạn cảm thấy tốt hơn mỗi ngày. 
        Hãy chọn một mục từ thanh điều hướng bên trái để bắt đầu nhé!

        **1. ✨ Liều Thuốc Tinh Thần:**
        Nhận một thông điệp tích cực ngẫu nhiên, một sự thật vui vẻ hoặc một lời nhắc nhở nhẹ nhàng để bắt đầu ngày mới đầy năng lượng.

        **2. 🧘 Góc An Yên:**
        Tìm đến sự bình yên với các bài tập hít thở có hướng dẫn, các bài tập thiền định đơn giản và âm thanh thiên nhiên giúp thư giãn tâm trí.

        **3. 🍯 Lọ Biết Ơn:**
        Thực hành lòng biết ơn bằng cách ghi lại những điều nhỏ bé trong cuộc sống khiến bạn mỉm cười.

        **4. 🎨 Vải Bố Vui Vẻ:**
        Một không gian sáng tạo tự do, nơi bạn có thể vẽ nguệch ngoạc để giải tỏa cảm xúc mà không cần lo nghĩ về kết quả.

        **5. 🎲 Trò Chơi Trí Tuệ:**
        Rèn luyện sự tập trung và trí nhớ với trò chơi nối hình đơn giản, vui vẻ và không áp lực.

        **6. ❤️ Góc Tự Chăm Sóc:**
        Xây dựng một kế hoạch chăm sóc bản thân với danh sách các hành động nhỏ và dễ thực hiện mỗi ngày.

        **7. 🆘 Hỗ Trợ Khẩn Cấp:**
        Danh sách các số điện thoại và nguồn lực hỗ trợ tâm lý khẩn cấp, đáng tin cậy tại Việt Nam.

        **8. 💬 Trò chuyện cùng Bot:**
        Trái tim của ứng dụng! Một người bạn AI luôn sẵn sàng lắng nghe tâm sự, luyện tập giao tiếp và trò chuyện về mọi chủ đề.

        **9. 📖 Người Kể Chuyện AI:**
        Kích thích trí tưởng tượng bằng cách đưa ra một chủ đề và để AI sáng tác một câu chuyện cổ tích ngắn dành riêng cho bạn.
        """
    )

    st.markdown("---")

    st.info("👈 **Hãy chọn một tính
