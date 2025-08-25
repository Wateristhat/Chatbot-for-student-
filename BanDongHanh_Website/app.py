import streamlit as st
from datetime import datetime
import database as db

# --- KHỞI TẠO DB VÀ CẤU HÌNH TRANG ---
db.init_db()
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS ĐÃ NÂNG CẤP ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CSS cho thẻ link bao quanh khối tính năng */
        a.feature-link {
            text-decoration: none; /* Bỏ gạch chân của link */
            color: inherit; /* Dùng màu chữ mặc định */
        }
        
        /* (Toàn bộ CSS cũ của bạn giữ nguyên) */
        html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
        .welcome-form { background-color: #f7f9fa; border-radius: 18px; padding: 2.5rem 2rem; margin-top: 2rem; }
        .stButton>button { background: linear-gradient(90deg, #f857a6 0%, #ff5858 100%); color: white; border-radius: 10px; padding: 0.6rem 1.5rem; }
        .features-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .feature-box { background: #fff; border-radius: 14px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(80,80,120,0.06); display: flex; align-items: flex-start; gap: 1rem; min-height: 120px; transition: all 0.2s; }
        .feature-box:hover { box-shadow: 0 6px 32px rgba(80,80,120,0.16); transform: translateY(-5px); }
        .feature-icon { font-size: 2.1rem; flex-shrink: 0; }
    </style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO SESSION STATE ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- GIAO DIỆN ---
st.title("Chào mừng đến với Bạn Đồng Hành 💖")

# --- PHẦN ĐĂNG NHẬP/ĐĂNG KÝ ---
if not st.session_state.user_id:
    tab1, tab2 = st.tabs(["👤 Người dùng cũ", "✨ Người dùng mới"])
    with tab1:
        # (code đăng nhập)
    with tab2:
        # (code đăng ký)

# --- PHẦN DÀNH CHO NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP ---
else:
    st.title(f"💖 Chào mừng {st.session_state.user_name} đến với Bạn Đồng Hành!")
    
    st.markdown("---")
    st.header("✨ Khám phá các tính năng")
    
    # [QUAN TRỌNG] DANH SÁCH TÍNH NĂNG VỚI ĐÚNG URL
    features = [
        {"icon": "fa-solid fa-sun", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày.", "url": "Liều_Thuốc_Tinh_Thần"},
        {"icon": "fa-solid fa-spa", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng.", "url": "Góc_An_Yên"},
        {"icon": "fa-solid fa-jar", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.", "url": "Lọ_Biết_Ơn"},
        {"icon": "fa-solid fa-paintbrush", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.", "url": "Bảng_Màu_Cảm_Xúc"},
        {"icon": "fa-solid fa-dice", "title": "Sân Chơi Trí Tuệ", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.", "url": "Sân_Chơi_Trí_Tuệ"},
        {"icon": "fa-solid fa-heart", "title": "Kế Hoạch Yêu Thương", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.", "url": "Kế_Hoạch_Yêu_Thương"},
        {"icon": "fa-solid fa-robot", "title": "Trò chuyện cùng Bot", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.", "url": "Trò_chuyện"},
        {"icon": "fa-solid fa-phone", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy.", "url": "Hỗ_Trợ_Khẩn_Cấp"},
        {"icon": "fa-solid fa-book-open", "title": "Người Kể Chuyện AI", "desc": "Lắng nghe những câu chuyện chữa lành do AI sáng tác.", "url": "Người_Kể_Chuyện_AI"}
    ]

    st.markdown('<div class="features-list">', unsafe_allow_html=True)
    for fe in features:
        st.markdown(
            f"""
            <a href="{fe['url']}" target="_self" class="feature-link">
                <div class="feature-box">
                    <span class="feature-icon"><i class="{fe['icon']}"></i></span>
                    <span>
                        <b>{fe['title']}</b><br>
                        <span style="color:#666">{fe['desc']}</span>
                    </span>
                </div>
            </a>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PHẦN ĐĂNG XUẤT ---
    st.markdown("---")
    if st.button("Đăng xuất"):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
