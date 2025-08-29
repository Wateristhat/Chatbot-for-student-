# pages/1_✨_Liều_Thuốc_Tinh_Thần.py
import streamlit as st
import random

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="✨ Liều Thuốc Tinh Thần",
    page_icon="✨",
    layout="centered"
)

# --- Không cần đăng nhập nữa ---

# --- CSS CHUNG + NÚT BACK ---
st.markdown("""
<style>
    .back-btn {
        text-decoration: none;
        font-size: 0.95rem;
        color: #000;
        background: #f1f1f1;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
    }
    .back-btn:hover { background: #e5e5e5; }
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("[⬅ Về Trang chủ](0_💖_Trang_chủ.py)", unsafe_allow_html=True)

# --- CSS VÀ FONT RIÊNG CỦA TRANG ---
st.markdown("""
<link rel="stylesheet"
 href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; }
    .message-card {
        background: linear-gradient(100deg, #e1ffea 0%, #fff6eb 100%);
        border-radius: 15px; border: 1.5px solid #e3e7ea; padding: 2rem 1.3rem;
        margin: 1.5rem 0; font-size: 1.23rem; text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); animation: popIn 0.5s;
    }
    .category-icon {
        font-size: 2.3rem; margin-bottom: 0.25rem; display:block;
    }
    @keyframes popIn {
        0% { opacity:0; transform:scale(0.8);}
        100% { opacity:1; transform:scale(1);}
    }
</style>
""", unsafe_allow_html=True)

# --- THƯ VIỆN NỘI DUNG ---
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
            "Hãy mỉm cười nhé, vì nụ cười của bạn có thể thắp sáng một ngày của ai đó."
        ]
    },
    "peace": {
        "label": "Tìm Bình Yên",
        "icon": "<i class='fa-solid fa-spa category-icon' style='color:#49c5b6'></i>",
        "messages": [
            "Hãy hít một hơi thật sâu... và thở ra thật chậm. Bạn đang ở đây, ngay bây giờ.",
            "Nhìn ra ngoài cửa sổ. Bạn thấy màu xanh nào không?",
            "Hãy chú ý đến cảm giác của đôi chân đang chạm đất."
        ]
    }
}

# --- SESSION STATE ---
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""

# --- HÀM XỬ LÝ ---
def select_category(category_key):
    st.session_state.message_category = category_key
    st.session_state.current_message = random.choice(
        MESSAGE_CATEGORIES[category_key]["messages"]
    )

def get_new_message():
    category_key = st.session_state.message_category
    if category_key:
        st.session_state.current_message = random.choice(
            MESSAGE_CATEGORIES[category_key]["messages"]
        )

# --- GIAO DIỆN CHÍNH ---
st.markdown("<div class='page-title'>✨ Liều Thuốc Tinh Thần Cho Bạn</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='font-size:1.1rem;line-height:1.6;'>"
    "Đôi khi, chúng ta chỉ cần một lời nhắc nhở nhỏ để cảm thấy tốt hơn.<br>"
    "<b>Bạn đang cần điều gì lúc này?</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Nút chọn loại thông điệp
cols = st.columns(len(MESSAGE_CATEGORIES))
for idx, (key, value) in enumerate(MESSAGE_CATEGORIES.items()):
    with cols[idx]:
        st.button(
            label=value["label"],
            on_click=select_category,
            args=(key,),
            key=f"btn_{key}",
            use_container_width=True
        )

st.write("---")

# Hiển thị thông điệp
if st.session_state.current_message and st.session_state.message_category:
    category_key = st.session_state.message_category
    category_info = MESSAGE_CATEGORIES[category_key]
    
    st.markdown(f"""
    <div class="message-card">
        {category_info['icon']}
        <div>{st.session_state.current_message}</div>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "🔄 Nhận một thông điệp khác cùng loại",
        on_click=get_new_message,
        key="btn_next_message",
        use_container_width=True
    )

    if random.random() < 0.2:
        st.balloons()
