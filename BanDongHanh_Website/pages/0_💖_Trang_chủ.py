import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- GIAO DIỆN CHÍNH ---
st.title("Chào mừng đến với Bạn Đồng Hành 💖")
st.markdown("Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")
st.markdown("Bạn có thể bắt đầu khám phá các tính năng của chúng mình ngay bây giờ nhé!")

# Hiển thị các nút điều hướng đến các trang khác
st.markdown("---")
st.subheader("Các tính năng chính của ứng dụng:")

col1, col2 = st.columns(2)

with col1:
    st.page_link("pages/1_✨_Liệu_thuốc_tinh_thần.py", label="Liệu thuốc tinh thần", icon="✨")
    st.page_link("pages/2_🍃_Góc_an_yên.py", label="Góc an yên", icon="🍃")
    st.page_link("pages/3_💌_Lọ_biết_ơn.py", label="Lọ biết ơn", icon="💌")

with col2:
    st.page_link("pages/4_🎨_Bảng_màu_cảm_xúc.py", label="Bảng màu cảm xúc", icon="🎨")
    st.page_link("pages/5_🏃‍♀️_Nhanh_tay_lẹ_mắt.py", label="Nhanh tay lẹ mắt", icon="🏃‍♀️")
    st.page_link("pages/6_🏠_Góc_nhỏ.py", label="Góc nhỏ", icon="🏠")
    st.page_link("pages/8_💬_Trò_chuyện_cùng_Bot.py", label="Trò chuyện cùng Bot", icon="💬")
