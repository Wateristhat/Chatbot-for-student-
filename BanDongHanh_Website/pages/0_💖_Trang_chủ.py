import streamlit as st
from datetime import datetime

# ----------------- CẤU HÌNH TRANG -----------------
st.set_page_config(
    page_title="Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# ----------------- CSS PHONG CÁCH THỜI TRANG -----------------
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
        letter-spacing: 0.2px;
    }
    /* Hero */
    .hero {
        width: 100%;
        padding: 6rem 0 3rem 0;
        text-align: center;
        background: linear-gradient(180deg, #ffffff 0%, #fafafa 100%);
    }
    .hero-title {
        font-size: clamp(32px, 6vw, 64px);
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 0;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1.05rem;
        max-width: 820px;
        margin: 1rem auto 0 auto;
        line-height: 1.6;
    }
    /* Form khởi tạo */
    .form-container {
        background-color: var(--card);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        max-width: 720px;
        margin: 2rem auto;
        box-shadow: 0 6px 24px rgba(0,0,0,0.06);
        border: 1px solid #eee;
    }
    .stButton>button {
        background-color: var(--accent);
        color: white;
        font-size: 1rem;
        border-radius: 999px;
        padding: 0.65rem 1.6rem;
        letter-spacing: 0.5px;
        border: none;
        transition: transform 0.2s ease, opacity 0.2s ease;
    }
    .stButton>button:hover { transform: translateY(-1px); opacity: 0.92; }
    /* Card tính năng */
    .feature-card {
        background-color: #fff;
        border-radius: 14px;
        padding: 1.4rem 1.2rem;
        text-align: left;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #eee;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        min-height: 140px;
    }
    .feature-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(0,0,0,0.1);
    }
    .feature-title {
        margin: 0 0 0.35rem 0;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .feature-desc {
        color: var(--muted);
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0;
    }
</style>
""", unsafe_allow_html=True)


def hero(title: str, sub: str):
    st.markdown(f"""
    <section class="hero">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-sub">{sub}</p>
    </section>
    """, unsafe_allow_html=True)


# ----------------- STATE -----------------
if 'user_name' not in st.session_state:
    st.session_state.user_name = None


# ----------------- GIAO DIỆN -----------------
if not st.session_state.user_name:
    hero("Bạn Đồng Hành", "Một trải nghiệm chăm sóc tinh thần tối giản, tinh tế — như một lookbook thời trang dành riêng cho bạn.")
    with st.form(key="welcome_form", clear_on_submit=True):
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        name = st.text_input("👤 Tên của bạn")
        current_year = datetime.now().year
        birth_year = st.selectbox("📅 Năm sinh", options=range(current_year - 5, current_year - 25, -1))
        school = st.text_input("🏫 Trường học")
        issues = st.text_area("💬 Gần đây điều gì khiến bạn bận tâm?", placeholder="Bạn có thể chia sẻ ở đây, mình luôn lắng nghe…")
        submitted = st.form_submit_button("Bắt đầu hành trình")
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if not name:
                st.warning("Vui lòng cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state.user_info = {"year": birth_year, "school": school, "issues": issues}
                st.rerun()

else:
    hero(f"Xin chào, {st.session_state.user_name}", "Chọn một tính năng bên dưới — mình sẽ đưa bạn tới đúng nơi.")

    # ---- DANH SÁCH TÍNH NĂNG ----
    features = [
        {
            "icon": "✨",
            "title": "Liều Thuốc Tinh Thần",
            "desc": "Nhận thông điệp tích cực mỗi ngày.",
            "page": "pages/1_✨_Liều_thuốc_tinh_thần.py"
        },
        {
            "icon": "🧘",
            "title": "Góc An Yên",
            "desc": "Bài tập thở giúp thư giãn.",
            "page": "pages/2_🧘_Góc_An_Yên.py"
        },
        {
            "icon": "🍯",
            "title": "Lọ Biết Ơn",
            "desc": "Ghi lại điều khiến bạn mỉm cười.",
            "page": "pages/3_🍯_Lọ_Biết_Ơn.py"
        },
        {
            "icon": "🎨",
            "title": "Vải Bố Vui Vẻ",
            "desc": "Vẽ và sáng tạo để giải tỏa cảm xúc.",
            "page": "pages/4_🎨_Vải_Bố_Vui_Vẻ.py"
        },
        {
            "icon": "🎲",
            "title": "Trò Chơi Trí Tuệ",
            "desc": "Thử thách trí não nhẹ nhàng.",
            "page": "pages/5_🎲_Trò_Chơi_Trí_Tuệ.py"
        },
        {
            "icon": "❤️",
            "title": "Góc Tự Chăm Sóc",
            "desc": "Lập kế hoạch chăm sóc bản thân.",
            "page": "pages/6_❤️_Góc_Tự_Chăm_Sóc.py"
        },
        {
            "icon": "💬",
            "title": "Trò chuyện cùng Bot",
            "desc": "Một người bạn AI luôn lắng nghe.",
            "page": "pages/7_💬_Trò_Chuyện_Cùng_Bot.py"
        },
        {
            "icon": "🆘",
            "title": "Hỗ Trợ Khẩn Cấp",
            "desc": "Nguồn lực và đường dây nóng đáng tin cậy.",
            "page": "pages/8_🆘_Hỗ_Trợ_Khẩn_Cấp.py"
        }
    ]

    # ---- HIỂN THỊ CARD ----
    cols = st.columns(4)
    for col, feature in zip(cols * (len(features) // len(cols) + 1), features):
        with col:
            st.page_link(
                feature["page"],
                label=f"""
                <div class="feature-card">
                    <div class="feature-title">{feature['icon']} {feature['title']}</div>
                    <p class="feature-desc">{feature['desc']}</p>
                </div>
                """,
                use_container_width=True
            )
