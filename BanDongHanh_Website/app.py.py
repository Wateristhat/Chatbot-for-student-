import streamlit as st

st.set_page_config(
    page_title="Trang chủ - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

st.title("Chào mừng đến với Bạn Đồng Hành 💖")
st.sidebar.success("Hãy chọn một tính năng ở trên nhé!")

st.markdown(
    """
    **Bạn Đồng Hành** là một không gian an toàn được xây dựng để hỗ trợ các bạn học sinh hòa nhập
    trong môi trường học đường. Ứng dụng này được thiết kế với giao diện đơn giản, thân thiện
    và tập trung vào việc hỗ trợ tinh thần cũng như rèn luyện kỹ năng xã hội.

    ### Các tính năng chính:

    - **💬 Trò chuyện cùng Bot**: Một người bạn AI luôn sẵn sàng lắng nghe những tâm sự, chia sẻ cảm xúc của bạn mà không phán xét.
    - **📔 Nhật ký cảm xúc**: Ghi lại cảm xúc mỗi ngày và xem lại lịch sử để hiểu rõ hơn về bản thân.
    - **🧘 Góc thư giãn**: Nơi bạn có thể tìm thấy các bài tập hít thở và âm thanh thiên nhiên giúp xoa dịu căng thẳng.

    👈 **Hãy bắt đầu bằng cách chọn một tính năng từ thanh điều hướng bên trái!**
    """
)