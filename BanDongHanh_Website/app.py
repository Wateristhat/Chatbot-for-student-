import streamlit as st

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS TÙY CHỈNH CHO GIAO DIỆN TỐI GIẢN ---
st.markdown("""
<style>
    .stApp {
        background-color: #E7F3FF; /* Nền xanh dương nhạt */
    }
    .main-container {
        padding: 2rem 4rem;
    }
    h1, h3 {
        color: #005A9C; /* Màu xanh đậm cho tiêu đề */
    }
</style>
""", unsafe_allow_html=True)


# --- NỘI DUNG TRANG GIỚI THIỆU ---
st.markdown("<div class='main-container'>", unsafe_allow_html=True)

st.title("Chào mừng đến với Bạn Đồng Hành 💖")

st.markdown(
    """
    **Bạn Đồng Hành** là một không gian an toàn, được xây dựng với mục tiêu hỗ trợ và nâng cao 
    [cite_start]năng lực giao tiếp cho các bạn học sinh hòa nhập tại Việt Nam. [cite: 2]
    
    [cite_start]Mình ở đây để trở thành một người bạn thấu cảm, luôn bên cạnh để giúp bạn tự tin hơn và giảm bớt những áp lực trong cuộc sống. [cite: 4, 5]
    """
)

st.markdown("---")

st.header("Các tính năng chính")

st.markdown(
    """
    Dưới đây là các tính năng được thiết kế để giúp bạn cảm thấy tốt hơn mỗi ngày. 
    Hãy chọn một mục từ thanh điều hướng bên trái để bắt đầu nhé!

    - [cite_start]**💬 Trò chuyện cùng Bot**: Một người bạn AI luôn sẵn sàng lắng nghe tâm sự, luyện tập giao tiếp và trò chuyện về mọi chủ đề. [cite: 31, 33]

    - **📔 Nhật ký cảm xúc**: Ghi lại cảm xúc mỗi ngày để hiểu rõ hơn về bản thân.

    - **🧘 Góc thư giãn**: Các bài tập đơn giản giúp bạn bình tĩnh và giải tỏa căng thẳng.
    
    - *(Và còn nhiều tính năng thú vị khác đang chờ bạn khám phá!)*
    """
)

st.markdown("</div>", unsafe_allow_html=True)
