import streamlit as st
import random

st.set_page_config(
    page_title="Liều Thuốc Tinh Thần",
    page_icon="✨",
    layout="centered"
)

# Thêm FontAwesome qua CDN (không cần pip)
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    html, body, [class*="css"] {
        font-family: 'Quicksand', Arial, sans-serif;
    }
    .category-btn {
        background: #fff;
        border-radius: 18px;
        border: 2px solid #f0f2f5;
        padding: 1.5rem 0.5rem;
        margin: 0.6rem 0;
        text-align: center;
        transition: all 0.22s;
        color: #1c1731;
        font-weight: 600;
        font-size: 1.13rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        width: 100%;
        cursor: pointer;
        outline: none;
    }
    .category-btn:hover {
        border: 2px solid #0084ff;
        background: #e6f1ff;
        color: #0084ff;
        transform: translateY(-2px) scale(1.03);
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }
    .category-icon {
        font-size: 2.3rem;
        margin-bottom: 0.25rem;
        display:block;
    }
    .message-card {
        background: linear-gradient(100deg, #e1ffea 0%, #fff6eb 100%);
        border-radius: 15px;
        border: 1.5px solid #e3e7ea;
        padding: 2rem 1.3rem;
        margin: 1.5rem 0;
        font-size: 1.23rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07);
        animation: popIn 0.5s;
    }
    @keyframes popIn {
        0% { opacity:0; transform:scale(0.8);}
        100% { opacity:1; transform:scale(1);}
    }
    @media (max-width: 600px) {
        .message-card { font-size: 1.09rem; padding: 1.2rem 0.5rem;}
        .category-btn { font-size: 1rem; }
    }
</style>
""", unsafe_allow_html=True)

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

# --- Giao diện trang ---
st.title("✨ Liều Thuốc Tinh Thần Cho Bạn")
st.markdown(
    "<div style='font-size:1.1rem;line-height:1.6;'>"
    "Đôi khi, chúng ta chỉ cần một lời nhắc nhở nhỏ để cảm thấy tốt hơn.<br>"
    "<b>Bạn đang cần điều gì lúc này?</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Khởi tạo session_state
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

# Hiển thị nút chọn danh mục với icon đẹp hơn
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📣 Cần Cổ Vũ", key="btn_courage"):
        st.session_state.message_category = "courage"
        st.session_state.current_message = random.choice(LOI_KHANG_DINH)
with col2:
    if st.button("😄 Muốn Vui Vẻ", key="btn_fun"):
        st.session_state.message_category = "fun"
        st.session_state.current_message = random.choice(GOC_VUI_VE)
with col3:
    if st.button("🧘 Tìm Bình Yên", key="btn_peace"):
        st.session_state.message_category = "peace"
        st.session_state.current_message = random.choice(KHOANH_KHAC_CHANH_NIEM)

st.write("---")

# Hiển thị thông điệp sau khi chọn
if st.session_state.current_message:
    # Dùng icon FontAwesome sinh động hơn
    icon_html = {
        "courage": "<i class='fa-solid fa-bullhorn category-icon' style='color:#ff6a00'></i>",
        "fun": "<i class='fa-solid fa-face-laugh-beam category-icon' style='color:#fbbf24'></i>",
        "peace": "<i class='fa-solid fa-spa category-icon' style='color:#49c5b6'></i>",
    }
    icon = icon_html.get(st.session_state.message_category, "💖")
    st.markdown(f"""
    <div class="message-card">
        {icon}
        <div>{st.session_state.current_message}</div>
    </div>
    """, unsafe_allow_html=True)

    # Nút đổi thông điệp mới
    if st.button("🔄 Nhận một thông điệp khác cùng loại", key="btn_next_message"):
        if st.session_state.message_category == "courage":
            st.session_state.current_message = random.choice(LOI_KHANG_DINH)
        elif st.session_state.message_category == "fun":
            st.session_state.current_message = random.choice(GOC_VUI_VE)
        elif st.session_state.message_category == "peace":
            st.session_state.current_message = random.choice(KHOANH_KHAC_CHANH_NIEM)
        st.rerun()

    # Hiệu ứng động, chỉ thỉnh thoảng
    if random.random() < 0.25:
        st.balloons()
