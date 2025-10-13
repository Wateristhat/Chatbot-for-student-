import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS HOÀN CHỈNH (ĐÃ THÊM STYLE CHO NÚT BẤM ĐỂ GIỐNG CARD) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
    /* --- Các style cũ của bạn giữ nguyên --- */
    .brand-minimal-box, .brand-minimal-header, .menu-list {
        /* ... (toàn bộ các style này giữ nguyên) ... */
    }

    /* --- STYLE MỚI ĐỂ BIẾN ST.BUTTON THÀNH MENU-CARD --- */
    .stButton > button {
        background: #fff;
        border-radius: 18px !important;
        box-shadow: 0 2px 10px rgba(80,80,120,0.10) !important;
        display: flex !important;
        align-items: center !important;
        gap: 1.3rem !important;
        min-height: 86px !important;
        transition: box-shadow 0.19s, transform 0.12s !important;
        border: 2.2px solid transparent !important; /* Thêm viền trong suốt để không bị giật khi hover */
        cursor: pointer;
        padding: 1.20rem 1.2rem 1.1rem 1.2rem !important;
        position: relative;
        text-decoration: none;
        margin-bottom: 0.3rem !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        box-shadow: 0 8px 32px rgba(255,88,88,0.15) !important;
        transform: translateY(-2px) scale(1.03) !important;
        border: 2.2px solid #f857a6 !important;
        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%) !important;
    }
    .stButton > button p { /* Nhắm vào text bên trong nút */
        text-align: left;
        margin: 0;
        padding: 0;
        line-height: 1.4;
    }
    .menu-icon {
        font-size: 2.3rem;
        flex-shrink: 0;
        margin-right: 0.1rem;
    }
    .menu-title {
        font-weight: 700;
        font-size: 1.18rem;
        color: #222;
    }
    .menu-desc {
        color: #444;
        font-size: 1.01rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ĐĂNG NHẬP (Giữ nguyên) ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_name:
    # ... (Giao diện đăng nhập giữ nguyên) ...
    with st.form(key="welcome_form", clear_on_submit=True):
        name = st.text_input("📝 Bạn tên là gì?")
        # ...
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        if submitted:
            if not name:
                st.warning("⚠️ Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state['user_id'] = name
                # ...
                st.success("✅ Lưu thông tin thành công! Chào mừng bạn đến với Bạn Đồng Hành!")
                st.rerun()
else:
    # --- GIAO DIỆN ĐÃ ĐĂNG NHẬP ---
    # ... (Phần chào mừng giữ nguyên) ...
    st.markdown("---")
    st.markdown("""<div class="brand-title" style="font-size:1.7rem; margin-bottom:0.3rem; text-align:left;">
    <span>✨</span> Khám phá các tính năng
    </div>""", unsafe_allow_html=True)
    
    # ----------- MENU ĐÃ SỬA LỖI VÀ GIỮ GIAO DIỆN -----------
    MENU_ITEMS = [
        {"icon": "fa-solid fa-sun", "color": "#FFB300", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày.", "page": "pages/1_✨_Liều_thuốc_tinh_thần.py"},
        {"icon": "fa-solid fa-spa", "color": "#4CAF50", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng.", "page": "pages/2_🫧_Góc_An_Yên.py"},
        {"icon": "fa-solid fa-jar", "color": "#F48FB1", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.", "page": "pages/3_🍯_Lọ_biết_ơn.py"},
        {"icon": "fa-solid fa-paintbrush", "color": "#2196F3", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.", "page": "pages/4_🎨_Bảng_màu_cảm_xúc.py"},
        {"icon": "fa-solid fa-dice", "color": "#AB47BC", "title": "Nhanh Tay Lẹ Mắt", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.", "page": "pages/5_🎮_Nhanh_tay_lẹ_mắt.py"},
        {"icon": "fa-solid fa-heart", "color": "#D50000", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.", "page": "pages/6_❤️_Góc_nhỏ.py"},
        {"icon": "fa-solid fa-phone", "color": "#0288D1", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy.", "page": "pages/7_🆘_Hỗ_Trợ_Khẩn_Cấp.py"},
        {"icon": "fa-solid fa-robot", "color": "#757575", "title": "Trò Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.", "page": "pages/8_💬_Trò_chuyện.py"},
        {"icon": "fa-solid fa-book", "color": "#F57C00", "title": "Người Kể Chuyện", "desc": "Lắng nghe những câu chuyện chữa lành tâm hồn.", "page": "pages/9_📖_Người_Kể_Chuyện.py"}
    ]
    
    st.markdown('<div class="menu-list">', unsafe_allow_html=True)
    for item in MENU_ITEMS:
        # Tạo nội dung HTML cho nút bấm
        button_html = f"""
            <span class="menu-icon" style="color:{item['color']}"><i class="{item['icon']}"></i></span>
            <span>
                <p class="menu-title">{item['title']}</p>
                <p class="menu-desc">{item['desc']}</p>
            </span>
        """
        if st.button(label=button_html, key=item['page'], use_container_width=True):
             st.switch_page(item['page'])

    st.markdown('</div>', unsafe_allow_html=True)
    # ----------- KẾT THÚC MENU ĐÃ SỬA LỖI -----------

    st.markdown("---")
    st.info("👈 <b>Hãy chọn một tính năng từ mục lục để bắt đầu!</b>", icon="😊")
