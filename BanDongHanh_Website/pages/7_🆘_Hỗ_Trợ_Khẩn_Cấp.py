# pages/7_🆘_Hỗ_trợ_khẩn_cấp.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="wide")

# --- CSS TÙY CHỈNH ĐỂ TĂNG CỠ CHỮ VÀ TẠO SỰ CHÚ Ý ---
st.markdown("""
<style>
/* --- CSS MỚI - CHỮ CỰC LỚN VÀ HÀI HÒA --- */
.hotline-container {
    background-color: #FFF0F0;
    border-radius: 20px;
    padding: 50px 30px; /* << TĂNG PADDING ĐỂ KHUNG CAO HƠN */
    margin: 30px 0;
    border: 3px solid #D9534F;
    text-align: center;
}
.hotline-title {
    font-size: 3rem;   /* << TĂNG CỠ CHỮ */
    font-weight: 700;
    color: #333;
    margin-bottom: 20px;
}
.hotline-number {
    font-size: 8rem;   /* << TĂNG CỠ CHỮ SỐ ĐIỆN THOẠI CỰC LỚN */
    font-weight: 900;
    color: #D9534F;
    letter-spacing: 4px;
    line-height: 1.1;
}
.hotline-description {
    font-size: 2rem;   /* << TĂNG CỠ CHỮ */
    margin-top: 15px;
    color: #555;
}
/* --- CSS CHO KHUNG CẢNH BÁO LỚN HƠN --- */
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
/* --- Class mới để đổi màu số 115 --- */
.emergency-number {
    color: #D9534F; /* Màu đỏ đậm */
    font-size: 1.8rem; /* Cho số to và nổi bật hơn */
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.title("🆘 HỖ TRỢ KHẨN CẤP")

# --- Liên kết quay về Trang chủ ---
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

# --- HIỂN THỊ CÁC ĐƯỜNG DÂY NÓNG VỚI GIAO DIỆN MỚI ---
st.markdown("""
<div class="hotline-container">
    <p class="hotline-title">Tổng đài Quốc gia Bảo vệ Trẻ em</p>
    <p class="hotline-number">111</p>
    <p class="hotline-description">Miễn phí, hoạt động 24/7</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hotline-container">
    <p class="hotline-title">Đường dây nóng Ngày Mai</p>
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
