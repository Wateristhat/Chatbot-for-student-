import streamlit as st
# from PIL import Image # Bỏ comment dòng này nếu bạn có file logo

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- GIAO DIỆN CHÍNH ---

# Phần tiêu đề được cải tiến
col_img, col_title = st.columns([1, 5])
with col_img:
    # TÙY CHỌN: Hiển thị logo nếu có file ảnh 'logo.png'
    # try:
    #     logo = Image.open("logo.png")
    #     st.image(logo, width=120)
    # except FileNotFoundError:
    st.markdown("<h1 style='font-size: 80px;'>💖</h1>", unsafe_allow_html=True)

with col_title:
    st.title("Chào mừng đến với Bạn Đồng Hành")
    st.markdown("#### Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")

st.markdown("---")
st.subheader("Hãy bắt đầu khám phá các tính năng của chúng mình nhé!")

# Hiển thị các tính năng với mô tả chi tiết
col1, col2 = st.columns(2, gap="large")

with col1:
    with st.container(border=True):
        st.page_link("pages/1_✨_Liệu_thuốc_tinh_thần.py", label="**Liệu thuốc tinh thần**", icon="✨")
        st.write("Nhận một thông điệp tích cực mỗi ngày để tiếp thêm động lực và niềm vui.")

    with st.container(border=True):
        st.page_link("pages/2_🍃_Góc_an_yên.py", label="**Góc an yên**", icon="🍃")
        st.write("Thư giãn với những bản nhạc êm dịu và các bài tập hít thở đơn giản.")

    with st.container(border=True):
        st.page_link("pages/3_💌_Lọ_biết_ơn.py", label="**Lọ biết ơn**", icon="💌")
        st.write("Ghi lại những điều bạn cảm thấy biết ơn để thấy cuộc sống ý nghĩa hơn.")
        
    with st.container(border=True):
        st.page_link("pages/8_💬_Trò_chuyện_cùng_Bot.py", label="**Trò chuyện cùng Bot**", icon="💬")
        st.write("Một người bạn AI luôn sẵn sàng lắng nghe và chia sẻ mọi tâm sự của bạn 24/7.")


with col2:
    with st.container(border=True):
        st.page_link("pages/4_🎨_Bảng_màu_cảm_xúc.py", label="**Bảng màu cảm xúc**", icon="🎨")
        st.write("Theo dõi và ghi nhận lại hành trình cảm xúc của bạn qua từng ngày.")

    with st.container(border=True):
        st.page_link("pages/5_🏃‍♀️_Nhanh_tay_lẹ_mắt.py", label="**Nhanh tay lẹ mắt**", icon="🏃‍♀️")
        st.write("Giải trí với một trò chơi đơn giản giúp rèn luyện sự tập trung và thư giãn đầu óc.")

    with st.container(border=True):
        st.page_link("pages/6_🏠_Góc_nhỏ.py", label="**Góc nhỏ**", icon="🏠")
        st.write("Không gian riêng tư để bạn viết nhật ký, đặt mục tiêu và lưu giữ suy nghĩ của riêng mình.")

st.markdown("---")
st.success("💖 **Bạn Đồng Hành** luôn ở đây để lắng nghe và hỗ trợ bạn trên hành trình chăm sóc bản thân!")
