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

# --- CSS HOÀN CHỈNH ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CSS cho thẻ link bao quanh khối tính năng */
        a.feature-link {
            text-decoration: none; /* Bỏ gạch chân của link */
            color: inherit; /* Dùng màu chữ mặc định */
        }
        
        /* Toàn bộ CSS giao diện của bạn */
        html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
        .welcome-form { background-color: #f7f9fa; border-radius: 18px; padding: 2.5rem 2rem; margin-top: 2rem; }
        .stButton>button { background: linear-gradient(90deg, #f857a6 0%, #ff5858 100%); color: white; border-radius: 10px; padding: 0.6rem 1.5rem; }
        .features-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-top: 1.5rem; }
        .feature-box { background: #fff; border-radius: 14px; padding: 1.5rem; box-shadow: 0 2px 8px rgba(80,80,120,0.06); display: flex; align-items: flex-start; gap: 1rem; min-height: 120px; transition: all 0.2s; }
        .feature-box:hover { box-shadow: 0 6px 32px rgba(80,80,120,0.16); transform: translateY(-5px); }
        .feature-icon { font-size: 2.1rem; flex-shrink: 0; }
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
    tab1, tab2 = st.tabs(["👤 Người dùng cũ", "✨ Người dùng mới"])

    # --- Tab Đăng nhập (Hoàn chỉnh) ---
    with tab1:
        st.header("Bạn đã quay trở lại!")
        all_users = db.get_all_users()
        if not all_users:
            st.info("Chưa có ai đăng ký cả. Hãy là người đầu tiên ở tab 'Người dùng mới' nhé!")
        else:
            user_dict = {user[0]: user[1] for user in all_users}
            selected_user_id = st.selectbox(
                "Hãy chọn tên của bạn:",
                options=user_dict.keys(),
                format_func=lambda user_id: user_dict.get(user_id, "Lỗi")
            )
            if st.button("Vào thôi!", key="login_btn", type="primary"):
                st.session_state.user_id = selected_user_id
                st.session_state.user_name = user_dict[selected_user_id]
                st.rerun()

    # --- Tab Đăng ký (Hoàn chỉnh) ---
    with tab2:
        st.header("Chúng mình làm quen nhé?")
        with st.form(key="signup_form"):
            st.markdown("<div class='welcome-form'>", unsafe_allow_html=True)
            name = st.text_input("📝 Bạn tên là gì?")
            current_year = datetime.now().year
            birth_year = st.selectbox(
                "🎂 Bạn sinh năm bao nhiêu?",
                options=range(current_year - 5, current_year - 25, -1)
            )
            school = st.text_input("🏫 Bạn đang học ở trường nào?")
            issues = st.text_area(
                "😥 Gần đây, có điều gì khiến bạn cảm thấy khó khăn không?",
                placeholder="Bạn có thể chia sẻ ở đây, mình luôn lắng nghe..."
            )
            
            if st.form_submit_button("💖 Tạo tài khoản và bắt đầu!"):
                if not name:
                    st.warning("⚠️ Tên không được để trống bạn nhé!")
                else:
                    user_id = db.add_user(name, birth_year, school, issues)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.user_name = name
                        st.success(f"Tài khoản '{name}' đã được tạo! Đang tải lại...")
                        st.rerun()
                    else:
                        st.error("Tên này đã có người dùng. Vui lòng chọn tên khác.")
            st.markdown("</div>", unsafe_allow_html=True)

# =====================================================================
# PHẦN 2: DÀNH CHO NGƯỜI DÙNG ĐÃ ĐĂNG NHẬP
# =====================================================================
else:
    st.title(f"💖 Chào mừng {st.session_state.user_name}!")
    st.markdown("---")
    st.header("✨ Khám phá các tính năng")
    
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
        # Thêm query parameters để duy trì session state
        user_params = f"?user_id={st.session_state.user_id}&user_name={st.session_state.user_name}"
        feature_url = f"{fe['url']}{user_params}"
        st.markdown(
            f"""
            <a href="{feature_url}" target="_self" class="feature-link">
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

    # --- PHẦN ĐĂNG XUẤT (Hoàn chỉnh) ---
    st.markdown("---")
    if st.button("Đăng xuất"):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
