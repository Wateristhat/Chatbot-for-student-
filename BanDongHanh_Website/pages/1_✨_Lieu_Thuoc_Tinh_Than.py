import streamlit as st
import random
import html

st.set_page_config(page_title="Liều Thuốc Tinh Thần", page_icon="✨", layout="centered")

# --- Thư viện nội dung được phân loại ---
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

# --- CSS Tùy chỉnh ---
st.markdown("""
<style>
    .category-button {
        background-color: #F0F2F5;
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: center;
        transition: all 0.3s;
        border: 2px solid transparent;
        color: #050505;
        width: 100%;
    }
    .category-button:hover {
        border: 2px solid #0084FF;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .category-icon {
        font-size: 3rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 50px;
    }
</style>
""", unsafe_allow_html=True)


# --- Giao diện trang ---
st.title("✨ Liều Thuốc Tinh Thần Cho Bạn")
st.markdown("Đôi khi, chúng ta chỉ cần một lời nhắc nhở nhỏ để cảm thấy tốt hơn. Bạn đang cần điều gì lúc này?")
st.write("---")

# Khởi tạo session_state
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

# Lựa chọn danh mục
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📣 Cần Cổ Vũ", use_container_width=True):
        st.session_state.message_category = "courage"
        st.session_state.current_message = random.choice(LOI_KHANG_DINH)
with col2:
    if st.button("😄 Muốn Vui Vẻ", use_container_width=True):
        st.session_state.message_category = "fun"
        st.session_state.current_message = random.choice(GOC_VUI_VE)
with col3:
    if st.button("🧘 Tìm Bình Yên", use_container_width=True):
        st.session_state.message_category = "peace"
        st.session_state.current_message = random.choice(KHOANH_KHAC_CHANH_NIEM)

st.write("---")

# Hiển thị thông điệp sau khi chọn
if st.session_state.current_message:
    st.subheader("Thông điệp dành cho bạn:")
    
    # Dùng icon phù hợp với danh mục
    icon = "💖"
    if st.session_state.message_category == "courage":
        icon = "📣"
    elif st.session_state.message_category == "fun":
        icon = "😄"
    elif st.session_state.message_category == "peace":
        icon = "🧘"
        
    st.info(f"**{st.session_state.current_message}**", icon=icon)

    if st.button("Nhận một thông điệp khác cùng loại", type="primary"):
        if st.session_state.message_category == "courage":
            st.session_state.current_message = random.choice(LOI_KHANG_DINH)
        elif st.session_state.message_category == "fun":
            st.session_state.current_message = random.choice(GOC_VUI_VE)
        elif st.session_state.message_category == "peace":
            st.session_state.current_message = random.choice(KHOANH_KHAC_CHANH_NIEM)
        st.rerun()

    if random.random() < 0.2:
        st.balloons()
