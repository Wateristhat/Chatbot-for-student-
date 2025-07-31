import streamlit as st

st.set_page_config(page_title="Hỗ Trợ Khẩn Cấp", page_icon="🆘", layout="centered")

st.title("🆘 Hỗ Trợ Khẩn Cấp")
st.markdown("Khi bạn cần sự giúp đỡ ngay lập tức, hãy tìm đến những nguồn lực này.")
st.write("---")

st.error(
    """
    **Ứng dụng này không phải là một dịch vụ cấp cứu.**

    Nếu bạn hoặc người thân đang ở trong tình huống nguy hiểm đến tính mạng hoặc cần hỗ trợ y tế khẩn cấp, 
    vui lòng gọi **115** (Cấp cứu y tế) hoặc đến bệnh viện/cơ sở y tế gần nhất.
    """
)

st.header("Các đường dây nóng hỗ trợ sức khỏe tinh thần tại Việt Nam")
st.markdown("- **Tổng đài Quốc gia Bảo vệ Trẻ em:** `111` (Miễn phí, 24/7)")
st.markdown("- **Đường dây nóng Ngày Mai:** `096.357.9488` (Hỗ trợ người trầm cảm)")

st.write("---")
st.info(
    """
    **Hãy nhớ rằng:** Việc tìm kiếm sự giúp đỡ là một hành động dũng cảm. Bạn không đơn độc.
    """
)
