# pages/7_🆘_Hỗ_trợ_khẩn_cấp.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="centered")

# --- CSS TÙY CHỈNH ĐỂ TĂNG CỠ CHỮ VÀ TẠO SỰ CHÚ Ý ---
st.markdown("""
<style>
.hotline-container {
    background-color: #FFF0F0; /* Nền màu đỏ nhạt */
    border-radius: 15px;
    padding: 25px;
    margin: 25px 0;
    border: 2px solid #D9534F; /* Viền đỏ đậm */
    text-align: center;
}
.hotline-title {
    font-size: 1.5rem; /* Cỡ chữ lớn cho tên tổ chức */
    font-weight: 700; /* In đậm */
    color: #333;
    margin-bottom: 10px;
}
.hotline-number {
    font-size: 3.5rem; /* Cỡ chữ RẤT LỚN cho số điện thoại */
    font-weight: 900; /* In rất đậm */
    color: #D9534F; /* Màu đỏ cảnh báo */
    letter-spacing: 3px;
    line-height: 1.2;
}
.hotline-description {
    font-size: 1.1rem;
    margin-top: 5px;
    color: #555;
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
st.error(
    """
    **ỨNG DỤNG NÀY KHÔNG PHẢI LÀ DỊCH VỤ CẤP CỨU.**

    Nếu bạn hoặc người thân đang ở trong tình huống nguy hiểm đến tính mạng, vui lòng gọi **115** (Cấp cứu y tế) hoặc đến cơ sở y tế gần nhất.
    """
)

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
