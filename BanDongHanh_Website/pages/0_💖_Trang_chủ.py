import streamlit as st
from PIL import Image

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS TÙY CHỈNH (TÙY CHỌN) ---
# Thêm một chút CSS để giao diện đẹp hơn
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .st-emotion-cache-1y4p8pa {
        padding-top: 4rem; /* Tăng khoảng cách cho tiêu đề chính */
    }
    h1, h2, h3 {
        color: #FF4B4B; /* Màu chủ đạo */
    }
</style>
""", unsafe_allow_html=True)

# --- PHẦN GIỚI THIỆU CHÍNH ---
col_img, col_title = st.columns([1, 4])
with col_img:
    # Bạn có thể thay thế 'logo.png' bằng đường dẫn đến file ảnh của bạn
    try:
        image = Image.open('logo.png') 
        st.image(image, width=150)
    except FileNotFoundError:
        st.markdown("💖", unsafe_allow_html=True) # Hiển thị icon nếu không có ảnh

with col_title:
    st.title("Chào mừng đến với Bạn Đồng Hành")
    st.markdown("### Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")

st.markdown("---")
st.markdown("#### Khám phá các tính năng của chúng mình ngay bây giờ nhé!")

# --- DANH SÁCH TÍNH NĂNG KÈM MÔ TẢ ---
col1, col2 = st.columns(2)

with col1:
    # TÍNH NĂNG 1: Liệu thuốc tinh thần
    with st.container(border=True):
        st.page_link("pages/1_✨_Liệu_thuốc_tinh_thần.py", label="### ✨ Liệu thuốc tinh thần")
        st.write("""
        Mỗi ngày, hãy nhận một "liều thuốc" tích cực! Đây là những thông điệp, trích dẫn, hoặc lời khuyên nhỏ 
        giúp bạn vực dậy tinh thần, tìm thấy niềm vui và động lực để bắt đầu một ngày mới thật hứng khởi.
        """)

    # TÍNH NĂNG 2: Góc an yên
    with st.container(border=True):
        st.page_link("pages/2_🍃_Góc_an_yên.py", label="### 🍃 Góc an yên")
        st.write("""
        Tìm về một không gian tĩnh lặng với những bản nhạc thư giãn và bài tập hít thở đơn giản. 
        Góc an yên giúp bạn giảm căng thẳng, xoa dịu tâm hồn và tái tạo năng lượng sau những giờ phút mệt mỏi.
        """)
        
    # TÍNH NĂNG 3: Lọ biết ơn
    with st.container(border=True):
        st.page_link("pages/3_💌_Lọ_biết_ơn.py", label="### 💌 Lọ biết ơn")
        st.write("""
        Thực hành lòng biết ơn mỗi ngày bằng cách ghi lại những điều nhỏ bé khiến bạn hạnh phúc. 
        "Lọ biết ơn" sẽ lưu giữ những khoảnh khắc ấy, nhắc nhở bạn rằng cuộc sống luôn có những điều tốt đẹp đáng trân trọng.
        """)

    # TÍNH NĂNG 4: Trò chuyện cùng Bot
    with st.container(border=True):
        st.page_link("pages/8_💬_Trò_chuyện_cùng_Bot.py", label="### 💬 Trò chuyện cùng Bot")
        st.write("""
        Bạn cần một người lắng nghe? Chatbot thông minh luôn ở đây 24/7 để trò chuyện, chia sẻ và
        giúp bạn gỡ rối những suy nghĩ trong lòng. Mọi cuộc trò chuyện đều được bảo mật và riêng tư.
        """)


with col2:
    # TÍNH NĂNG 5: Bảng màu cảm xúc
    with st.container(border=True):
        st.page_link("pages/4_🎨_Bảng_màu_cảm_xúc.py", label="### 🎨 Bảng màu cảm xúc")
        st.write("""
        Theo dõi và nhận diện cảm xúc của bản thân mỗi ngày. Việc ghi lại "màu sắc" cảm xúc giúp bạn
        hiểu rõ hơn về thế giới nội tâm và quản lý sức khỏe tinh thần của mình một cách hiệu quả hơn.
        """)

    # TÍNH NĂNG 6: Nhanh tay lẹ mắt
    with st.container(border=True):
        st.page_link("pages/5_🏃‍♀️_Nhanh_tay_lẹ_mắt.py", label="### 🏃‍♀️ Nhanh tay lẹ mắt")
        st.write("""
        Giải trí và rèn luyện sự tập trung với một trò chơi đơn giản nhưng không kém phần thú vị. 
        Một cách tuyệt vời để "reset" bộ não và tạm quên đi những lo âu, phiền muộn.
        """)

    # TÍNH NĂNG 7: Góc nhỏ
    with st.container(border=True):
        st.page_link("pages/6_🏠_Góc_nhỏ.py", label="### 🏠 Góc nhỏ")
        st.write("""
        Không gian riêng tư của bạn, nơi bạn có thể viết nhật ký, đặt mục tiêu cá nhân và lưu giữ
        những suy nghĩ, ý tưởng của riêng mình. Đây là nơi bạn được là chính mình một cách trọn vẹn nhất.
        """)

st.markdown("---")
st.success("💖 **Bạn Đồng Hành** luôn ở đây để lắng nghe và hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần!")
