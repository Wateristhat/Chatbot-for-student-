# Dán toàn bộ code này vào file 0_💖_Trang_chủ.py
import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)


# --- CSS (Giữ nguyên, không thay đổi) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
    .brand-minimal-box {
        background: linear-gradient(110deg, #ff82ac 3%, #fd5e7c 97%);
        border-radius: 38px;
        padding: 2.3rem 2.4rem 2.1rem 2.4rem;
        margin: 0 auto 2.5rem auto;
        max-width: 700px;
        box-shadow: 0 8px 32px rgba(255,88,88,0.08);
        display: flex;
        flex-direction: column;
        align-items: flex-start;
    }
    .brand-minimal-header {
        font-family: 'Quicksand', Arial, sans-serif;
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -1px;
        color: #fff;
        margin-bottom: 0.8rem;
        margin-left: 0.2rem;
        line-height: 1.22;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: 1.1rem 1.5rem;
    }
    .brand-minimal-header .text-main, .brand-minimal-header .text-brand {
        color: #fff; background: none; font-size: 2.3rem; font-weight: 800;
    }
    .brand-minimal-icon { font-size: 2.3rem; color: #f9c6d3; margin-right: 0.3rem; }
    .brand-minimal-desc {
        color: #fff; font-size: 1.17rem; font-weight: 500; margin-bottom: 1.3rem;
        margin-left: 0.2rem; line-height: 1.65; text-align: left; width: 100%;
    }
    .brand-minimal-desc .fa-heart { color: #ffb2be; font-size: 1.1rem; margin-right: 0.3rem; }
    .brand-minimal-highlight {
        background: rgba(255,255,255,0.87); border-radius: 22px; font-size: 1.14rem;
        color: #444; max-width: 580px; padding: 1.1rem 1.3rem 0.9rem 1.3rem;
        font-weight: 500; line-height: 1.65; margin-left: 0.1rem; margin-top: 0.1rem;
        box-shadow: 0 2px 16px rgba(255,88,88,0.07); text-align: left;
    }
    .brand-minimal-highlight .highlight-action { color: #fd5e7c; font-weight: 700; font-size: 1.09rem; }
    .menu-list {
        display: flex;
        flex-direction: column;
        gap: 1.25rem;
        margin-top: 1.5rem;
        margin-bottom: 2.2rem;
    }
    .menu-card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 10px rgba(80,80,120,0.10);
        display: flex;
        align-items: center;
        gap: 1.3rem;
        min-height: 86px;
        transition: box-shadow 0.19s, transform 0.12s;
        border: 2.2px solid transparent;
        cursor: pointer;
        padding: 1.20rem 1.2rem 1.1rem 1.2rem;
        position: relative;
        text-decoration: none;
        margin-bottom: 0.3rem;
    }
    .menu-card:hover {
        box-shadow: 0 8px 32px rgba(255,88,88,0.15);
        transform: translateY(-2px) scale(1.01);
        border: 2.2px solid #f857a6;
        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
    }
    .menu-card, .menu-card * { text-decoration: none !important; }
    .menu-icon { font-size: 2.3rem; flex-shrink: 0; margin-right: 0.1rem; }
    .menu-title { font-weight:700; font-size:1.18rem; margin-bottom:0.13rem; color: #222; }
    .menu-desc { color:#444; font-size:1.01rem; font-weight:500; margin-top:0.15rem; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ĐĂNG NHẬP (Giữ nguyên) ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_name:
    # --- Giao diện chưa đăng nhập ---
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng bạn đến với</span> <span class="text-brand">Bạn Đồng Hành!</span>
        </div>
        <div class="brand-minimal-desc">
            <i class="fa-solid fa-heart"></i>
            <span><b>“Bạn Đồng Hành”</b> – Người bạn thấu cảm, luôn bên cạnh trên hành trình chăm sóc sức khỏe tinh thần.</span>
        </div>
        <div class="brand-minimal-highlight">
            Cùng truyền cảm hứng và lan tỏa yêu thương mỗi ngày. Được thiết kế để giúp bạn vượt qua thử thách trong học tập, cuộc sống, và nuôi dưỡng sự cân bằng cảm xúc.<br>
            <span class="highlight-action">Hãy bắt đầu khám phá nhé!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.title("👋 Chào bạn, mình là Bạn Đồng Hành 💖")
    st.header("Trước khi bắt đầu, chúng mình làm quen nhé?")

    with st.form(key="welcome_form", clear_on_submit=True):
        name = st.text_input("📝 Bạn tên là gì?")
        # ... (các input khác như năm sinh, trường học) ...
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        if submitted:
            if not name:
                st.warning("⚠️ Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state['user_id'] = name
                st.session_state.user_info = {
                    # "year": birth_year, "school": school, "issues": issues
                }
                st.success("✅ Lưu thông tin thành công! Chào mừng bạn đến với Bạn Đồng Hành!")
                st.rerun()
else:
    # --- Giao diện đã đăng nhập ---
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng {st.session_state.user_name} đến với</span> <span class="text-brand">Bạn Đồng Hành!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""<div style="font-size:1.7rem; font-weight:700; margin-bottom:0.3rem;">✨ Khám phá các tính năng</div>""", unsafe_allow_html=True)
    
    # ----------- MENU ĐÃ SỬA LỖI LINK VÀ GIỮ GIAO DIỆN GỐC -----------
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
        # THAY ĐỔI QUAN TRỌNG: href="{item['page']}" thay vì href="/{item['page']}"
        # Streamlit sẽ tự động hiểu đây là link nội bộ và không tải lại trang
        st.markdown(
            f"""
            <a href="{item['page']}" class="menu-card" target="_self">
                <span class="menu-icon" style="color:{item['color']}"><i class="{item['icon']}"></i></span>
                <span>
                    <span class="menu-title">{item['title']}</span><br>
                    <span class="menu-desc">{item['desc']}</span>
                </span>
            </a>
            """,
            unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    # ----------- KẾT THÚC MENU ĐÃ SỬA LỖI -----------

