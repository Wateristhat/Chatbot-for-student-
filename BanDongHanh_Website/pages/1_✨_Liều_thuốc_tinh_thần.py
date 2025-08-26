# pages/Lieu_thuoc_tinh_than.py
import streamlit as st
import random

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Liều Thuốc Tinh Thần",
    page_icon="✨",
    layout="centered"
)

# --- THÊM CSS VÀ FONT ---
# Sử dụng CSS để có giao diện đẹp và tùy chỉnh font chữ
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Thêm Google Font Quicksand */
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', Arial, sans-serif; /* Áp dụng font chữ cho toàn bộ trang */
    }
    /* Các style khác của bạn được giữ nguyên và tối ưu */
    .category-btn {
        background: #fff; border-radius: 18px; border: 2px solid #f0f2f5;
        padding: 1.5rem 0.5rem; margin: 0.6rem 0; text-align: center;
        transition: all 0.22s; color: #1c1731; font-weight: 600;
        font-size: 1.13rem; box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        width: 100%; cursor: pointer; outline: none;
    }
    .category-btn:hover {
        border: 2px solid #0084ff; background: #e6f1ff; color: #0084ff;
        transform: translateY(-2px) scale(1.03); box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    }
    .category-icon {
        font-size: 2.3rem; margin-bottom: 0.25rem; display:block;
    }
    .message-card {
        background: linear-gradient(100deg, #e1ffea 0%, #fff6eb 100%);
        border-radius: 15px; border: 1.5px solid #e3e7ea; padding: 2rem 1.3rem;
        margin: 1.5rem 0; font-size: 1.23rem; text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); animation: popIn 0.5s;
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


# --- THƯ VIỆN NỘI DUNG ---
# GOM TẤT CẢ VÀO MỘT CHỖ ĐỂ DỄ QUẢN LÝ
MESSAGE_CATEGORIES = {
    "courage": {
        "label": "Cần Cổ Vũ",
        "icon": "<i class='fa-solid fa-bullhorn category-icon' style='color:#ff6a00'></i>",
        "messages": [
            "Hôm nay, tôi chọn bình yên.",
            "Tôi đủ mạnh mẽ để vượt qua mọi thử thách.",
            "Tôi xứng đáng được yêu thương và hạnh phúc.",
            "Mỗi hơi thở đều mang lại cho tôi sức mạnh.",
            "Tôi biết ơn vì con người của tôi ngay bây giờ."
        ]
    },
    "fun": {
        "label": "Muốn Vui Vẻ",
        "icon": "<i class='fa-solid fa-face-laugh-beam category-icon' style='color:#fbbf24'></i>",
        "messages": [
            "Sự thật thú vị: Rái cá biển thường nắm tay nhau khi ngủ để không bị trôi đi mất.",
            "Đố bạn: Cái gì luôn ở phía trước bạn, nhưng bạn không bao giờ thấy được? ... Đó là tương lai!",
            "Hãy mỉm cười nhé, vì nụ cười của bạn có thể thắp sáng một ngày của ai đó.",
            "Một bản nhạc vui vẻ có thể thay đổi tâm trạng của bạn ngay lập tức đấy."
        ]
    },
    "peace": {
        "label": "Tìm Bình Yên",
        "icon": "<i class='fa-solid fa-spa category-icon' style='color:#49c5b6'></i>",
        "messages": [
            "Hãy hít một hơi thật sâu... và thở ra thật chậm. Bạn đang ở đây, ngay bây giờ.",
            "Nhìn ra ngoài cửa sổ. Bạn thấy màu xanh nào không?",
            "Hãy chú ý đến cảm giác của đôi chân đang chạm đất.",
            "Bạn đang nghe thấy âm thanh gì xa nhất? Âm thanh gì gần nhất?"
        ]
    }
}

# --- KHỞI TẠO STATE ---
# Đảm bảo các biến trạng thái được khởi tạo an toàn
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

# --- HÀM XỬ LÝ ---
def select_category(category_key):
    """Hàm được gọi khi người dùng chọn một danh mục."""
    st.session_state.message_category = category_key
    st.session_state.current_message = random.choice(MESSAGE_CATEGORIES[category_key]["messages"])

def get_new_message():
    """Hàm lấy một thông điệp mới từ danh mục hiện tại."""
    category_key = st.session_state.message_category
    if category_key:
        st.session_state.current_message = random.choice(MESSAGE_CATEGORIES[category_key]["messages"])

# --- GIAO DIỆN CHÍNH ---
st.title("✨ Liều Thuốc Tinh Thần Cho Bạn")

# *** ĐÃ THÊM: Liên kết quay về Trang chủ ***
st.page_link("Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown(
    "<div style='font-size:1.1rem;line-height:1.6;'>"
    "Đôi khi, chúng ta chỉ cần một lời nhắc nhở nhỏ để cảm thấy tốt hơn.<br>"
    "<b>Bạn đang cần điều gì lúc này?</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# --- HIỂN THỊ CÁC NÚT CHỌN DANH MỤC ---
cols = st.columns(len(MESSAGE_CATEGORIES))
for idx, (key, value) in enumerate(MESSAGE_CATEGORIES.items()):
    with cols[idx]:
        # Dùng st.button trực tiếp với on_click để code sạch hơn
        st.button(
            label=value["label"],
            on_click=select_category,
            args=(key,),
            key=f"btn_{key}",
            use_container_width=True
        )

st.write("---")

# --- HIỂN THỊ THÔNG ĐIỆP SAU KHI CHỌN ---
if st.session_state.current_message and st.session_state.message_category:
    category_key = st.session_state.message_category
    category_info = MESSAGE_CATEGORIES[category_key]
    
    # Hiển thị thẻ thông điệp
    st.markdown(f"""
    <div class="message-card">
        {category_info['icon']}
        <div>{st.session_state.current_message}</div>
    </div>
    """, unsafe_allow_html=True)

    # Nút đổi thông điệp mới
    st.button(
        "🔄 Nhận một thông điệp khác cùng loại",
        on_click=get_new_message,
        key="btn_next_message",
        use_container_width=True
    )

    # Hiệu ứng động, chỉ thỉnh thoảng để tạo bất ngờ
    if random.random() < 0.2:
        st.balloons()
