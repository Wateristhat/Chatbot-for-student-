# Trang_chủ.py
import streamlit as st
from datetime import datetime
import database as db # Đảm bảo file database.py của bạn đã đầy đủ
import time

# --- KHỞI TẠO DB VÀ CẤU HÌNH TRANG ---
# Hàm này nên được gọi để đảm bảo các bảng đã tồn tại
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- CSS HOÀN CHỈNH ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        a.feature-link { text-decoration: none; color: inherit; }
        html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
        .welcome-form { background-color: #f7f9fa; border-radius: 18px; padding: 2.5rem 2rem; margin-top: 1.5rem; }
        .stButton>button { background: linear-gradient(90deg, #f857a6 0%, #ff5858 100%); color: white; border-radius: 10px; padding: 0.6rem 1.5rem; font-weight: 600; }
        .features-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .feature-box { background: #fff; border-radius: 14px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(80,80,120,0.06); display: flex; align-items: flex-start; gap: 1rem; min-height: 120px; transition: all 0.2s; }
        .feature-box:hover { box-shadow: 0 6px 32px rgba(80,80,120,0.16); transform: translateY(-5px); }
        .feature-icon { font-size: 2.1rem; flex-shrink: 0; color: #f857a6; }
    </style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO SESSION STATE AN TOÀN ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- GIAO DIỆN CHÍNH ---
st.title("Chào mừng đến với Bạn Đồng Hành 💖")

# ===================================================================
# PHẦN 1: DÀNH CHO NGƯỜI DÙNG CHƯA ĐĂNG NHẬP
# ===================================================================
if not st.session_state.get('user_id'):
    st.markdown("Một không gian an toàn để bạn kết nối và chăm sóc sức khỏe tinh thần.")
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])

    # --- Tab Đăng nhập (An toàn và bảo mật) ---
    with tab1:
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        with st.form("login_form"):
            username = st.text_input("Tên đăng nhập", placeholder="Nhập tên của bạn...")
            password = st.text_input("Mật khẩu", type="password", placeholder="Nhập mật khẩu...")
            submitted = st.form_submit_button("Vào thôi!")

            if submitted:
                # Hàm check_user cần được viết trong database.py để xử lý
                user = db.check_user(username, password)
                if user:
                    st.session_state.user_id = user[0]
                    st.session_state.user_name = user[1]
                    st.rerun()
                else:
                    st.error("Tên đăng nhập hoặc mật khẩu không chính xác!")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- Tab Đăng ký (UX được cải thiện) ---
    with tab2:
        st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
        with st.form(key="signup_form"):
            name = st.text_input("📝 Bạn tên là gì?", placeholder="Tên bạn sẽ hiển thị trong ứng dụng")
            # password_reg = st.text_input("🔑 Mật khẩu của bạn", type="password", placeholder="Chọn một mật khẩu an toàn")
            
            if st.form_submit_button("💖 Tạo tài khoản và bắt đầu!"):
                if not name: #or not password_reg:
                    st.warning("⚠️ Tên và mật khẩu không được để trống bạn nhé!")
                else:
                    if db.add_user(name, "password_reg"): # Thay "password_reg" bằng biến mật khẩu thật
                        st.success(f"Tài khoản '{name}' đã được tạo! Đang chuyển hướng...")
                        time.sleep(2) # Chờ 2 giây để người dùng đọc thông báo
                        st.rerun()
                    else:
                        st.error("Tên này đã có người dùng. Vui lòng chọn tên khác.")
        st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# PHẦN 2: DÀNH CHO NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP
# =====================================================================
else:
    st.title(f"Hôm nay bạn thế nào, {st.session_state.user_name}? ✨")
    st.markdown("---")
    st.header("Khám phá các tính năng")
    
    # Danh sách tính năng, cần đảm bảo `url` khớp với tên file trong thư mục /pages
    features = [
         {"icon": "fa-solid fa-robot", "title": "Trò chuyện cùng Bot", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.", "url": "Trò_chuyện_cùng_Bot"},
         {"icon": "fa-solid fa-sun", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày.", "url": "Liều_Thuốc_Tinh_Thần"},
         {"icon": "fa-solid fa-spa", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở và chánh niệm.", "url": "Goc_an_yen"},
         {"icon": "fa-solid fa-jar", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.", "url": "Lo_biet_on"},
         {"icon": "fa-solid fa-paintbrush", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.", "url": "Bang_mau_cam_xuc"},
         {"icon": "fa-solid fa-dice", "title": "Nhanh Tay Lẹ Mắt", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.", "url": "Nhanh_tay_le_mat"},
         {"icon": "fa-solid fa-heart", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.", "url": "Goc_nho"},
         {"icon": "fa-solid fa-book-open", "title": "Người Kể Chuyện", "desc": "Lắng nghe những câu chuyện chữa lành ý nghĩa.", "url": "Nguoi_ke_chuyen"},
         {"icon": "fa-solid fa-phone", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các đường dây nóng đáng tin cậy.", "url": "Ho_tro_khan_cap"}
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

    # --- PHẦN ĐĂNG XUẤT (An toàn) ---
    st.markdown("---")
    if st.button("Đăng xuất"):
        # Xóa tất cả các khóa trong session state để đăng xuất an toàn
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

