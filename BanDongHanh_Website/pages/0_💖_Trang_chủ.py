# FILE: 0_💖_Trang_chủ.py
# DÙNG PHIÊN BẢN HOÀN CHỈNH NÀY

import streamlit as st
from datetime import datetime

# Cấu hình trang
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS TÙY CHỈNH ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* ----- FONT CHUNG ----- */
    html, body, [class*="css"] { 
        font-family: 'Quicksand', Arial, sans-serif; 
    }
    .brand-minimal-box {
        background: linear-gradient(110deg, #ff82ac 3%, #fd5e7c 97%); border-radius: 38px;
        padding: 2.3rem 2.4rem 2.1rem 2.4rem; margin: 0 auto 2.5rem auto; max-width: 700px;
        box-shadow: 0 8px 32px rgba(255,88,88,0.08); display: flex; flex-direction: column; align-items: flex-start;
    }
    .brand-minimal-header {
        font-size: 2.3rem; font-weight: 800; letter-spacing: -1px; color: #fff;
        margin-bottom: 0.8rem; margin-left: 0.2rem; line-height: 1.22;
    }
    .brand-minimal-icon { font-size: 2.3rem; color: #f9c6d3; margin-right: 0.3rem; }
    .brand-minimal-desc {
        color: #fff; font-size: 1.17rem; font-weight: 500; margin-bottom: 1.3rem;
        margin-left: 0.2rem; line-height: 1.65;
    }
    .menu-list {
        display: flex; flex-direction: column; gap: 1.25rem;
        margin-top: 1.5rem; margin-bottom: 2.2rem;
    }
    .menu-card {
        background: #fff; border-radius: 18px; box-shadow: 0 2px 10px rgba(80,80,120,0.10);
        display: flex; align-items: center; gap: 1.3rem; min-height: 86px;
        transition: box-shadow 0.19s, transform 0.12s; border: 2.2px solid transparent;
        cursor: pointer; padding: 1.20rem 1.2rem 1.1rem 1.2rem; text-decoration: none !important;
    }
    .menu-card:hover {
        box-shadow: 0 8px 32px rgba(255,88,88,0.15); transform: translateY(-2px) scale(1.01);
        border: 2.2px solid #f857a6; background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
    }
    .menu-icon { font-size: 2.3rem; flex-shrink: 0; margin-right: 0.1rem; }
    .menu-title { font-weight:700; font-size:1.18rem; color: #222; }
    .menu-desc { color:#444; font-size:1.01rem; font-weight:500; }
</style>
""", unsafe_allow_html=True)

# --- QUẢN LÝ TRẠNG THÁI ĐĂNG NHẬP ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

# --- GIAO DIỆN CHÍNH ---

# 1. NẾU CHƯA ĐĂNG NHẬP
if not st.session_state.user_name:
    st.markdown("""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            Chào mừng bạn đến với Bạn Đồng Hành!
        </div>
        <div class="brand-minimal-desc">
            <b>“Bạn Đồng Hành”</b> – Người bạn thấu cảm, luôn bên cạnh trên hành trình chăm sóc sức khỏe tinh thần của bạn.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.title("👋 Chào bạn, mình là Bạn Đồng Hành 💖")
    st.header("Trước khi bắt đầu, chúng mình làm quen nhé?")
    with st.form(key="welcome_form", clear_on_submit=True):
        name = st.text_input("📝 Bạn tên là gì?")
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        if submitted:
            if not name:
                st.warning("⚠️ Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                # LƯU CẢ 2 KEY CẦN THIẾT
                st.session_state.user_name = name
                st.session_state.user_id = name
                st.success(f"✅ Lưu thông tin thành công! Chào mừng {name}!")
                st.rerun()

# 2. NẾU ĐÃ ĐĂNG NHẬP
else:
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            Chào mừng {st.session_state.user_name} quay trở lại!
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""<div style="font-size:1.7rem; font-weight:700; margin-bottom:0.3rem;">✨ Khám phá các tính năng</div>""", unsafe_allow_html=True)
    
    MENU_ITEMS = [
        {"icon": "fa-solid fa-sun", "color": "#FFB300", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày.", "page": "Liều_thuốc_tinh_thần"},
        {"icon": "fa-solid fa-spa", "color": "#4CAF50", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng.", "page": "Góc_An_Yên"},
        {"icon": "fa-solid fa-jar", "color": "#F48FB1", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.", "page": "Lọ_biết_ơn"},
        {"icon": "fa-solid fa-paintbrush", "color": "#2196F3", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.", "page": "Bảng_màu_cảm_xúc"},
        {"icon": "fa-solid fa-dice", "color": "#AB47BC", "title": "Nhanh Tay Lẹ Mắt", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.", "page": "Nhanh_tay_lẹ_mắt"},
        {"icon": "fa-solid fa-heart", "color": "#D50000", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.", "page": "Góc_nhỏ"},
        {"icon": "fa-solid fa-phone", "color": "#0288D1", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy.", "page": "Hỗ_Trợ_Khẩn_Cấp"},
        {"icon": "fa-solid fa-robot", "color": "#757575", "title": "Trò Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.", "page": "Trò_chuyện"},
        {"icon": "fa-solid fa-book", "color": "#F57C00", "title": "Người Kể Chuyện", "desc": "Lắng nghe những câu chuyện chữa lành tâm hồn.", "page": "Người_Kể_Chuyện"}
    ]
    
    st.markdown('<div class="menu-list">', unsafe_allow_html=True)
    for item in MENU_ITEMS:
        st.markdown(f"""
        <a href="{item['page']}" class="menu-card" target="_self">
            <span class="menu-icon" style="color:{item['color']};"><i class="{item['icon']}"></i></span>
            <span>
                <div class="menu-title">{item['title']}</div>
                <div class="menu-desc">{item['desc']}</div>
            </span>
        </a>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.info("👈 **Hãy chọn một tính năng từ mục lục bên trái để bắt đầu!**", icon="😊")
