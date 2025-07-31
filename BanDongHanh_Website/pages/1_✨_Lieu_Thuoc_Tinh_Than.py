import streamlit as st
import random

st.set_page_config(page_title="Liều Thuốc Tinh Thần", page_icon="✨", layout="centered")

# --- Thư viện nội dung ---
LOI_KHANG_DINH = [
    "Hôm nay, tôi chọn bình yên.",
    "Tôi đủ mạnh mẽ để vượt qua mọi thử thách.",
    "Tôi xứng đáng được yêu thương và hạnh phúc.",
    "Mỗi hơi thở đều mang lại cho tôi sức mạnh.",
    "Tôi biết ơn vì con người của tôi ngay bây giờ."
]
GOC_VUI_VE = [
    "Sự thật thú vị: Rái cá biển thường nắm tay nhau khi ngủ để không bị trôi đi mất.",
    "Đố bạn: Cái gì luôn ở phía trước bạn, nhưng bạn không bao giờ thấy được? ... Đó là tương lai!",
    "Hãy mỉm cười nhé, vì nụ cười của bạn có thể thắp sáng một ngày của ai đó.",
    "Một bản nhạc vui vẻ có thể thay đổi tâm trạng của bạn ngay lập tức đấy."
]
KHOANH_KHAC_CHANH_NIEM = [
    "Hãy hít một hơi thật sâu... và thở ra thật chậm. Bạn đang ở đây, ngay bây giờ.",
    "Nhìn ra ngoài cửa sổ. Bạn thấy màu xanh nào không?",
    "Hãy chú ý đến cảm giác của đôi chân đang chạm đất.",
    "Bạn đang nghe thấy âm thanh gì xa nhất? Âm thanh gì gần nhất?"
]
ALL_MESSAGES = LOI_KHANG_DINH + GOC_VUI_VE + KHOANH_KHAC_CHANH_NIEM

# --- Giao diện trang ---
st.title("✨ Liều Thuốc Tinh Thần Cho Bạn")
st.markdown("Mỗi ngày đều cần một chút ánh nắng cho tâm hồn. Hãy xem hôm nay vũ trụ muốn nhắn nhủ gì với bạn nhé!")
st.write("---")

if 'current_message' not in st.session_state:
    st.session_state.current_message = random.choice(ALL_MESSAGES)

st.info(f"**{st.session_state.current_message}**", icon="💖")

if st.button("Nhận một thông điệp khác", type="primary"):
    st.session_state.current_message = random.choice(ALL_MESSAGES)
    st.rerun()

if random.random() < 0.2:
    st.balloons()
