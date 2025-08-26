# 0_💖_Trang_chủ.py
import streamlit as st
from datetime import datetime

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="💖 Trang chủ",
    page_icon="💖",
    layout="wide"
)

# --- CSS CHUNG ---
st.markdown("""
<style>
    :root {
        --text: #1f1f1f;
        --muted: #6b6b6b;
        --bg: #ffffff;
        --card: #f8f8f8;
        --accent: #000000;
    }
    html, body, .block-container {
        background: var(--bg) !important;
        color: var(--text);
        font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
    }
    .hero {padding: 5rem 0 3rem 0; text-align: center;}
    .hero-title {font-size: clamp(32px, 6vw, 64px); font-weight: 700; text-transform: uppercase;}
    .hero-sub {color: var(--muted); font-size: 1.05rem; max-width: 820px; margin: 1rem auto 0;}
    .form-container {background: var(--card); border-radius: 16px; padding: 2rem 2.5rem; max-width: 720px; margin: 2rem auto; box-shadow: 0 6px 24px rgba(0,0,0,0.06); border: 1px solid #eee;}
    .stButton>button {background-color: var(--accent); color: white; font-size: 1rem; border-radius: 999px; padding: 0.65rem 1.6rem; border: none;}
    .feature-card {background-color: #fff; border-radius: 14px; padding: 1.4rem 1.2rem; box-shadow: 0 4px 16px rgba(0,0,0,0.06); border: 1px solid #eee; min-height: 140px;}
    .feature-card:hover {transform: translateY(-4px); box-shadow: 0 10px 24px rgba(0,0,0,0.1);}
    .feature-title {margin: 0 0 0.35rem 0; font-size: 1.05rem; font-weight: 700;}
    .feature-desc {color: var(--muted); font-size: 0.95rem; line-height: 1.5; margin: 0;}
</style>
""", unsafe_allow_html=True)

# --- HÀM HERO ---
def hero(title, sub):
    st.markdown(f"<section class='hero'><h1 class='hero-title'>{title}</h1><p class='hero-sub'>{sub}</p></section>", unsafe_allow_html=True)

# --- SESSION ---
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# --- GIAO DIỆN ---
if not st.session_state.user_id:
    hero("Bạn Đồng Hành", "Trải nghiệm chăm sóc tinh thần tối giản & tinh tế.")
    with st.form(key="welcome_form", clear_on_submit=True):
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        name = st.text_input("👤 Tên của bạn")
        current_year = datetime.now().year
        birth_year = st.selectbox("📅 Năm sinh", options=range(current_year - 5, current_year - 25, -1))
        school = st.text_input("🏫 Trường học")
        issues = st.text_area("💬 Điều khiến bạn bận tâm?", placeholder="Mình luôn sẵn sàng lắng nghe…")
        submitted = st.form_submit_button("Bắt đầu hành trình")
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not name:
                st.warning("Vui lòng cho mình biết tên nhé!")
            else:
                st.session_state.user_id = name.lower().replace(" ", "_")
                st.session_state.user_name = name
                st.session_state.user_info = {
                    "year": birth_year,
                    "school": school,
                    "issues": issues
                }
                st.rerun()
else:
    hero(f"Xin chào, {st.session_state.user_name}", "Chọn tính năng bên dưới để bắt đầu")

    features = [
        {"icon": "💖", "title": "Trang chủ", "desc": "Về màn hình chính", "page": "0_💖_Trang_chủ.py"},
        {"icon": "✨", "title": "Liều thuốc tinh thần", "desc": "Thông điệp tích cực mỗi ngày", "page": "1_✨_Liều_Thuốc_Tinh_Thần.py"},
        {"icon": "🛋️", "title": "Góc an yên", "desc": "Nơi thư giãn tâm trí", "page": "2_🛋️_Góc_an_yên.py"},
        {"icon": "🏺", "title": "Lọ biết ơn", "desc": "Ghi lại điều khiến bạn mỉm cười", "page": "3_🏺_Lọ_biết_ơn.py"},
        {"icon": "🎨", "title": "Bảng màu cảm xúc", "desc": "Tô màu cảm xúc của bạn", "page": "4_🎨_Bảng_màu_cảm_xúc.py"},
        {"icon": "🕹️", "title": "Nhanh tay lẹ mắt", "desc": "Trò chơi phản xạ vui nhộn", "page": "5_🕹️_Nhanh_tay_lẹ_mắt.py"},
        {"icon": "💓", "title": "Góc nhỏ", "desc": "Chăm chút bản thân", "page": "6_💓_Góc_nhỏ.py"},
        {"icon": "🆘", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Nguồn lực và liên hệ khẩn", "page": "7_🆘_Hỗ_Trợ_Khẩn_Cấp.py"},
        {"icon": "💬", "title": "Trò chuyện", "desc": "Nói chuyện với AI", "page": "8_💬_Trò_chuyện.py"},
        {"icon": "📖", "title": "Người Kể Chuyện", "desc": "Câu chuyện & trải nghiệm", "page": "9_📖_Người_Kể_Chuyện.py"}
    ]

    cols = st.columns(4)
    for col, f in zip(cols * ((len(features) // len(cols)) + 1), features):
        with col:
            st.page_link(
                f["page"],
                label=f"""
                <div class="feature-card">
                    <div class="feature-title">{f['icon']} {f['title']}</div>
                    <p class="feature-desc">{f['desc']}</p>
                </div>
                """,
                use_container_width=True
            )
