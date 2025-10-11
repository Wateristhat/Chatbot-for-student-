# pages/7_🆘_Hỗ_trợ_khẩn_cấp.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="wide")

# --- CSS HOÀN CHỈNH VÀ SẠCH SẼ ---
st.markdown("""
<style>
/* --- CSS CHO KHUNG HOTLINE (ĐỒNG BỘ VỚI KHUNG 115) --- */
.hotline-container {
    background-color: #FFF0F0;
    border: 2px solid #D9534F;
    border-radius: 15px;
    padding: 40px;
    margin: 25px 0;
    text-align: center;
}
.hotline-title {
    font-size: 1.5rem !important;
    font-weight: 700;
    display: block;
    margin-bottom: 1rem;
    color: #333;
}
.hotline-number {
    font-size: 1.8rem !important;
    font-weight: 900;
    color: #D9534F;
}
.hotline-description {
    font-size: 1.3rem !important;
    margin-top: 1rem;
    color: #555;
}

/* --- CSS CHO KHUNG CẢNH BÁO 115 --- */
.emergency-warning-box {
    background-color: #FFF0F0;
    border: 2px solid #D9534F;
    border-radius: 15px;
    padding: 40px;
    margin: 25px 0;
}
.emergency-warning-box p {
    font-size: 1.3rem;
    text-align: center;
    margin-bottom: 1rem;
}
.emergency-warning-box strong {
    font-size: 1.5rem;
    display: block;
    margin-bottom: 1rem;
}
/* --- Class mới để đổi màu và font chữ số 115 --- */
.emergency-number {
    color: #D9534F;
    font-size: 1.8rem;
    font-weight: 900;
    font-family: 'Courier New', Courier, monospace; /* Thêm font chữ khối */
    letter-spacing: 3px; /* Thêm khoảng cách giống số 111 */
}
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.title("🆘 HỖ TRỢ KHẨN CẤP")
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
st.markdown("Khi bạn hoặc ai đó bạn biết đang gặp khủng hoảng, hãy tìm đến sự giúp đỡ ngay lập tức.")
st.write("---")

# --- CẢNH BÁO QUAN TRỌNG ---
st.markdown("""
<div class="emergency-warning-box">
    <p><strong>ỨNG DỤNG NÀY KHÔNG PHẢI LÀ DỊCH VỤ CẤP CỨU.</strong></p>
    <p>Nếu bạn hoặc người thân đang ở trong tình huống nguy hiểm đến tính mạng, vui lòng gọi <strong class="emergency-number">115</strong> (Cấp cứu y tế) hoặc đến cơ sở y tế gần nhất.</p>
</div>
""", unsafe_allow_html=True)

st.header("Các đường dây nóng hỗ trợ sức khỏe tinh thần tại Việt Nam")

# --- HIỂN THỊ CÁC ĐƯỜNG DÂY NÓNG ---
st.markdown("""
<div class="hotline-container">
    <p class="hotline-title"><strong>Tổng đài Quốc gia Bảo vệ Trẻ em</strong></p>
    <p class="hotline-number">111</p>
    <p class="hotline-description">Miễn phí, hoạt động 24/7</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hotline-container">
    <p class="hotline-title"><strong>Đường dây nóng Ngày Mai</strong></p>
    <p class="hotline-number">096 357 94 88</p>
    <p class="hotline-description">Hỗ trợ người trầm cảm và các vấn đề sức khỏe tinh thần</p>
</div>
""", unsafe_allow_html=True)

st.write("---")

# --- THÔNG ĐIỆP ĐỘNG VIÊN ---
st.info(
    """
    **Hãy nhớ rằng:** Việc tìm kiếm sự giúp đỡ là một hành động dũng cảm và mạnh mẽ. Bạn không hề đơn độc.
    """
)
