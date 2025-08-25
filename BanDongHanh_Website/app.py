import streamlit as st
from datetime import datetime
import database as db # Import file database của chúng ta

# Lần đầu tiên chạy, file database sẽ được tạo
db.init_db()

# --- CẤU HÌNH TRANG CHÍNH ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- GOOGLE FONTS VÀ CSS HIỆN ĐẠI (Giữ nguyên của bạn) ---
st.markdown("""
    <link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        html, body, [class*="css"]  {
            font-family: 'Quicksand', Arial, sans-serif;
        }
        .main-container {
            padding: 2rem;
        }
        .welcome-form {
            background-color: #f7f9fa;
            border-radius: 18px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
            padding: 2.5rem 2rem;
            margin-top: 2rem;
            transition: box-shadow 0.3s;
        }
        .welcome-form:hover {
            box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        }
        .stButton>button {
            background: linear-gradient(90deg, #f857a6 0%, #ff5858 100%);
            color: white;
            font-weight: 700;
            border-radius: 10px;
            transition: background 0.2s, transform 0.15s;
            padding: 0.6rem 1.5rem;
        }
        .stButton>button:hover {
            background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
            transform: scale(1.04);
        }
        .stTextInput>div>div>input, .stTextArea textarea, .stSelectbox>div>div {
            border-radius: 6px;
            border: 1px solid #e3e7ea;
        }
        .features-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        .feature-box {
            background: #fff;
            border-radius: 14px;
            padding: 1.2rem 1rem;
            box-shadow: 0 2px 8px rgba(80,80,120,0.06);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
            min-height: 120px;
            transition: box-shadow 0.2s, transform 0.18s;
        }
        .feature-box:hover {
            box-shadow: 0 4px 32px rgba(80,80,120,0.16);
            transform: translateY(-4px) scale(1.03);
        }
        .feature-icon {
            font-size: 2.1rem;
            flex-shrink: 0;
        }
        @media (max-width: 800px) {
            .features-list { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
            .feature-box { min-height: 80px; }
        }
    </style>
""", unsafe_allow_html=True)

# --- Khởi tạo session state để lưu trạng thái đăng nhập ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- GIAO DIỆN ---
st.title("Chào mừng đến với Bạn Đồng Hành 💖")

# Nếu người dùng chưa đăng nhập
if not st.session_state.user_id:
    tab1, tab2 = st.tabs(["👤 Người dùng cũ", "✨ Người dùng mới"])

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
                placeholder="Bạn có thể chia sẻ ở đây, mình luôn lắng nghe và giữ bí mật cho bạn..."
            )
            
            if st.form_submit_button("💖 Tạo tài khoản và bắt đầu!"):
                if not name:
                    st.warning("⚠️ Tên không được để trống bạn nhé!")
                else:
                    user_id = db.add_user(name, birth_year, school, issues)
                    if user_id:
                        st.session_state.user_id = user_id
                        st.session_state.user_name = name
                        st.success(f"Tài khoản '{name}' đã được tạo thành công! Đang tải lại...")
                        st.rerun()
                    else:
                        st.error("Tên này đã có người dùng. Vui lòng chọn tên khác hoặc đăng nhập ở tab bên cạnh.")
            st.markdown("</div>", unsafe_allow_html=True)

# Nếu người dùng đã đăng nhập thành công
else:
    st.title(f"💖 Chào mừng {st.session_state.user_name} đến với Bạn Đồng Hành!")
    
    st.markdown(
        """
        <div style='font-size:1.1rem;line-height:1.6;margin-bottom:1rem'>
        <b>“Bạn Đồng Hành”</b> được tạo ra với mong muốn trở thành một người bạn thấu cảm, 
        luôn ở bên cạnh để hỗ trợ bạn trên hành trình chăm sóc sức khỏe tinh thần.
        </div>
        """, unsafe_allow_html=True
    )

    st.markdown("---")
    st.header("✨ Khám phá các tính năng")
    
    features = [
        {"icon": "fa-solid fa-sun", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày."},
        {"icon": "fa-solid fa-spa", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng."},
        {"icon": "fa-solid fa-jar", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười."},
        {"icon": "fa-solid fa-paintbrush", "title": "Vải Bố Vui Vẻ", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc."},
        {"icon": "fa-solid fa-dice", "title": "Trò Chơi Trí Tuệ", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng."},
        {"icon": "fa-solid fa-heart", "title": "Góc Tự Chăm Sóc", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày."},
        {"icon": "fa-solid fa-robot", "title": "Trò chuyện cùng Bot", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn."},
        {"icon": "fa-solid fa-phone", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy."},
    ]

    st.markdown('<div class="features-list">', unsafe_allow_html=True)
    for fe in features:
        st.markdown(
            f"""
            <div class="feature-box">
                <span class="feature-icon"><i class="{fe['icon']}"></i></span>
                <span>
                    <b>{fe['title']}</b><br>
                    <span style="color:#666">{fe['desc']}</span>
                </span>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    if st.button("Đăng xuất"):
        st.session_state.user_id = None
        st.session_state.user_name = None
        st.rerun()
