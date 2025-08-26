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

    /* Grid tính năng */
    .features {
        margin: 2rem 0 0 0;
    }
    .feature-card {
        background-color: #fff;
        border-radius: 14px;
        padding: 1.4rem 1.2rem;
        text-align: left;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        border: 1px solid #eee;
        transition: transform 0.18s ease, box-shadow 0.18s ease;
        cursor: pointer;
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

    /* Section nội dung */
    .section {
        scroll-margin-top: 90px; /* để cuộn dừng đẹp dưới hero */
        padding: 2rem 0;
        border-top: 1px solid #efefef;
    }
    .section h3 {
        font-size: 1.4rem;
        margin-bottom: 0.75rem;
        text-transform: none;
        letter-spacing: 0.3px;
    }
    .muted { color: var(--muted); }

    /* Thanh phân cách */
    .divider { height: 1px; background: #eee; margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ----------------- STATE -----------------
if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# ----------------- HERO -----------------
def hero(title: str, sub: str):
    st.markdown(f"""
    <section class="hero">
        <h1 class="hero-title">{title}</h1>
        <p class="hero-sub">{sub}</p>
    </section>
    """, unsafe_allow_html=True)

# ----------------- DANH SÁCH TÍNH NĂNG -----------------
features = [
    {"id": "lieu-thuoc", "icon": "✨", "title": "Liều Thuốc Tinh Thần", "desc": "Thông điệp tích cực mỗi ngày."},
    {"id": "goc-an-yen", "icon": "🧘", "title": "Góc An Yên", "desc": "Bài tập thở giúp thư giãn nhanh."},
    {"id": "lo-biet-on", "icon": "🍯", "title": "Lọ Biết Ơn", "desc": "Ghi lại điều nhỏ bé khiến bạn mỉm cười."},
    {"id": "vai-bo-vui-ve", "icon": "🎨", "title": "Vải Bố Vui Vẻ", "desc": "Vẽ và sáng tạo để giải tỏa cảm xúc."},
    {"id": "tro-choi-tri-tue", "icon": "🎲", "title": "Trò Chơi Trí Tuệ", "desc": "Thử thách nhẹ nhàng cho trí não."},
    {"id": "goc-tu-cham-soc", "icon": "❤️", "title": "Góc Tự Chăm Sóc", "desc": "Lập kế hoạch chăm sóc bản thân."},
    {"id": "tro-chuyen-bot", "icon": "💬", "title": "Trò chuyện cùng Bot", "desc": "Một người bạn AI luôn lắng nghe."},
    {"id": "ho-tro-khan-cap", "icon": "🆘", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Nguồn lực và đường dây nóng đáng tin cậy."},
]

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

    # --------- MỤC LỤC Ở SIDEBAR (tùy chọn) ----------
    with st.sidebar:
        st.markdown("#### Mục lục")
        # Cho phép chuyển phần bằng sidebar
        selected = st.radio(
            label="Đi tới",
            options=[f["icon"] + " " + f["title"] for f in features],
            label_visibility="collapsed",
            key="toc_radio"
        )
        # Lưu 'section' tương ứng vào state
        for f in features:
            if selected.endswith(f["title"]):
                st.session_state["section"] = f["id"]

    # --------- GRID CÁC THẺ TÍNH NĂNG ----------
    st.markdown('<div class="features">', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, f in enumerate(features):
        col = cols[i % 4]
        with col:
            st.markdown(
                f"""
                <div class="feature-card" onclick="document.getElementById('{f['id']}').scrollIntoView({{behavior:'smooth'}});">
                    <div class="feature-title">{f['icon']} {f['title']}</div>
                    <p class="feature-desc">{f['desc']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # --------- SECTION NỘI DUNG CHI TIẾT ----------
    # Tip: nếu bạn đã có các trang riêng trong thư mục pages/,
    # thay phần nội dung bên dưới bằng mô tả ngắn + nút chuyển trang.
    for f in features:
        st.markdown(f"<section id='{f['id']}' class='section'></section>", unsafe_allow_html=True)
        st.subheader(f"{f['icon']} {f['title']}")
        st.markdown(f"<p class='muted'>{f['desc']}</p>", unsafe_allow_html=True)

        # Nút chuyển hướng theo 2 cách:
        # 1) Cùng trang: đặt biến mục lục -> cuộn (fallback khi JS không chạy)
        if st.button(f"Đi tới {f['title']}", key=f"btn_{f['id']}"):
            st.session_state["section"] = f["id"]
            # Gợi ý cuộn mượt khi không dùng JS: hiển thị anchor mục tiêu đầu trang
            st.markdown(
                f"<script>document.getElementById('{f['id']}').scrollIntoView({{behavior:'smooth'}});</script>",
                unsafe_allow_html=True
            )

        # 2) Nếu bạn có page riêng: dùng st.page_link (Streamlit mới) hoặc st.sidebar radio chuyển trang
        # Ví dụ (bật khi có file phù hợp trong pages/):
        # st.page_link("pages/01_✨_Lieu_Thuoc_Tinh_Than.py", label="Mở trang tính năng")

        st.markdown("")  # spacing

    # Nếu có 'section' từ sidebar hoặc button: tự cuộn tới đó
    target = st.session_state.get("section", None)
    if target:
        st.markdown(
            f"<script>document.getElementById('{target}').scrollIntoView({{behavior:'smooth'}});</script>",
            unsafe_allow_html=True
        )
