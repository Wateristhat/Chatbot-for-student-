# File: 0_💖_Trang_chủ.py (FIX CUỐI CÙNG: Chuyển Menu thành Mô tả Tĩnh và Thêm Đăng Xuất)
import streamlit as st
from datetime import datetime
import sys, os
import importlib

# Import database helpers
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
# Đảm bảo nạp lại module nếu Streamlit đã cache lần trước
try:
    db = importlib.reload(db)
except Exception:
    pass


st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)
# --- 🚀 KÍCH HOẠT PWA (THÊM ĐOẠN NÀY) ---
st.markdown("""
<link rel="manifest" href="static/manifest.json">
<script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('static/sw.js');
        });
    }
</script>
""", unsafe_allow_html=True)

# --- CSS (Bổ sung class feature-card mới) ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    html, body, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; }
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
    
    /* CSS cho khối Mô tả Tính năng TĨNH */
    .feature-card {
        background: #fff;
        border-radius: 18px;
        box-shadow: 0 2px 10px rgba(80,80,120,0.10);
        display: flex;
        align-items: center;
        gap: 1.3rem;
        min-height: 86px;
        border: 2.2px solid transparent;
        padding: 1.20rem 1.2rem 1.1rem 1.2rem;
        margin-bottom: 1.25rem;
        pointer-events: none; /* QUAN TRỌNG: Loại bỏ khả năng nhấp */
    }
    .feature-icon { font-size: 2.3rem; flex-shrink: 0; margin-right: 0.1rem; }
    .feature-title { font-weight:700; font-size:1.18rem; margin-bottom:0.13rem; color: #222; }
    .feature-desc { color:#444; font-size:1.01rem; font-weight:500; margin-top:0.15rem; }
</style>
""", unsafe_allow_html=True)

# --- LOGIC ĐĂNG NHẬP (Giữ nguyên) ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_name:
    # --- Giới thiệu ngắn ---
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
            <span class="highlight-action">Hãy bắt đầu bằng việc đăng nhập hoặc tạo tài khoản nhé!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_login, tab_register = st.tabs(["💖 Đăng nhập", "📝 Đăng ký"])

    with tab_login:
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập")
            password = st.text_input("Mật khẩu", type="password")
            submit_login = st.form_submit_button("Đăng nhập")
            if submit_login:
                if not username or not password:
                    st.warning("Vui lòng nhập đầy đủ tên đăng nhập và mật khẩu.")
                else:
                    if db.verify_user(username, password):
                        st.session_state.user_name = username
                        st.session_state['user_id'] = username
                        st.success("Đăng nhập thành công!")
                        st.rerun()
                    else:
                        st.error("Sai tên đăng nhập hoặc mật khẩu.")

    with tab_register:
        with st.form("register_form"):
            new_username = st.text_input("Tên đăng nhập mới")
            new_password = st.text_input("Mật khẩu", type="password")
            new_password2 = st.text_input("Nhập lại mật khẩu", type="password")
            submit_reg = st.form_submit_button("Tạo tài khoản")
            if submit_reg:
                if not new_username or not new_password or not new_password2:
                    st.warning("Vui lòng nhập đầy đủ thông tin.")
                elif len(new_username.strip()) < 3:
                    st.warning("Tên đăng nhập phải có ít nhất 3 ký tự.")
                elif len(new_password) < 6:
                    st.warning("Mật khẩu phải có ít nhất 6 ký tự.")
                elif new_password != new_password2:
                    st.warning("Mật khẩu nhập lại không khớp.")
                else:
                    ok = db.create_user(new_username, new_password)
                    if ok:
                        st.success("Tạo tài khoản thành công! Bạn có thể đăng nhập ngay.")
                    else:
                        st.error("Tên đăng nhập đã tồn tại hoặc dữ liệu không hợp lệ.")
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

    col_welcome, col_logout = st.columns([4,1])
    with col_welcome:
        st.markdown("---")
    st.markdown("## ✨ Khám phá các tính năng")
    with col_logout:
        if st.button("🚪 Đăng xuất"):
            for key in ["user_name", "user_id", "user_info"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_set_query_params()
            st.rerun()
    
    st.info("Vui lòng sử dụng **Menu ở thanh bên trái** để truy cập các tính năng.")
    
    # --- DỮ LIỆU CÁC TÍNH NĂNG (FEATURE LIST) ---
    FEATURE_ITEMS = [
        {"icon": "fa-solid fa-sun", "color": "#FFB300", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày."},
        {"icon": "fa-solid fa-spa", "color": "#4CAF50", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng."},
        {"icon": "fa-solid fa-jar", "color": "#F48FB1", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười."},
        {"icon": "fa-solid fa-paintbrush", "color": "#2196F3", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc."},
        {"icon": "fa-solid fa-dice", "color": "#AB47BC", "title": "Nhanh Tay Lẹ Mắt", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng."},
        {"icon": "fa-solid fa-heart", "color": "#D50000", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày."},
        {"icon": "fa-solid fa-phone", "color": "#0288D1", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy."},
        {"icon": "fa-solid fa-robot", "color": "#757575", "title": "Trò Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn."},
        {"icon": "fa-solid fa-book", "color": "#F57C00", "title": "Người Kể Chuyện", "desc": "Lắng nghe những câu chuyện chữa lành tâm hồn."}
    ]

    # --- TẠO CÁC KHỐI MÔ TẢ TĨNH ---
    for item in FEATURE_ITEMS:
        st.markdown(
            f"""
            <div class="feature-card">
                <span class="feature-icon" style="color:{item['color']}"><i class="{item['icon']}"></i></span>
                <span>
                    <span class="feature-title">{item['title']}</span><br>
                    <span class="feature-desc">{item['desc']}</span>
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- TRUY CẬP NHANH: LIÊN KẾT TỚI CÁC TRANG ---
    st.markdown("---")
    st.markdown("## 🚀 Truy cập nhanh")
    st.caption("Bạn có thể bấm nhanh vào các liên kết dưới đây để chuyển đến từng tính năng.")

    quick_links = [
        {"path": "pages/1_✨_Liều_thuốc_tinh_thần.py", "label": "✨ Liều Thuốc Tinh Thần", "icon": "✨"},
        {"path": "pages/2_🫧_Góc_An_Yên.py", "label": "🫧 Góc An Yên", "icon": "🫧"},
        {"path": "pages/3_🍯_Lọ_biết_ơn.py", "label": "🍯 Lọ Biết Ơn", "icon": "🍯"},
        {"path": "pages/4_🎨_Bảng_màu_cảm_xúc.py", "label": "🎨 Bảng Màu Cảm Xúc", "icon": "🎨"},
        {"path": "pages/5_🎮_Nhanh_tay_lẹ_mắt.py", "label": "🎮 Nhanh Tay Lẹ Mắt", "icon": "🎮"},
        {"path": "pages/6_❤️_Góc_nhỏ.py", "label": "❤️ Góc Nhỏ", "icon": "❤️"},
        {"path": "pages/7_🆘_Hỗ_Trợ_Khẩn_Cấp.py", "label": "🆘 Hỗ Trợ Khẩn Cấp", "icon": "🆘"},
        {"path": "pages/8_💬_Trò_chuyện.py", "label": "💬 Trò Chuyện", "icon": "💬"},
        {"path": "pages/9_📖_Người_Kể_Chuyện.py", "label": "📖 Người Kể Chuyện", "icon": "📖"},
    ]

    # Hiển thị theo 3 cột trên desktop, tự động xếp dọc trên mobile
    cols = st.columns(3)
    for idx, link in enumerate(quick_links):
        with cols[idx % 3]:
            st.page_link(link["path"], label=link["label"])  # icon đã nằm trong label
        


