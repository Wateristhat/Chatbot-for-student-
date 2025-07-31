import streamlit as st

# Cấu hình trang chính
st.set_page_config(
    page_title="Trang chủ - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- Giao diện trang chủ ---

st.title("Chào mừng đến với Bạn Đồng Hành 💖")
st.header("Một không gian an toàn cho sức khỏe tinh thần của bạn")
st.markdown("---")

st.markdown(
    """
    **Bạn Đồng Hành** được tạo ra với mong muốn trở thành một người bạn thấu cảm, 
    luôn ở bên cạnh để hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần.

    Ứng dụng này được thiết kế với giao diện đơn giản, nhẹ nhàng và tích cực, đặc biệt 
    phù hợp cho các bạn học sinh cần một nơi để giải tỏa căng thẳng và rèn luyện kỹ năng.

    ### Các tính năng chính:
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

st.write("---")
st.info("👈 **Hãy bắt đầu bằng cách chọn một tính năng từ thanh điều hướng bên trái nhé!**", icon="😊")
