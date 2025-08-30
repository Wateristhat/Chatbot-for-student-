import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- GOOGLE FONTS + CSS TỐI GIẢN SANG TRỌNG ---
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
    .brand-minimal-header .text-main {
        color: #fff;
        background: none;
        font-size: 2.3rem;
        font-weight: 800;
    }
    .brand-minimal-header .text-brand {
        color: #fff;
        font-size: 2.3rem;
        font-weight: 800;
        background: none;
    }
    .brand-minimal-icon {
        font-size: 2.3rem;
        color: #f9c6d3;
        margin-right: 0.3rem;
    }
    .brand-minimal-desc {
        color: #fff;
        font-size: 1.17rem;
        font-weight: 500;
        margin-bottom: 1.3rem;
        margin-left: 0.2rem;
        line-height: 1.65;
        text-align: left;
        width: 100%;
    }
    .brand-minimal-desc .fa-heart {
        color: #ffb2be;
        font-size: 1.1rem;
        margin-right: 0.3rem;
    }
    .brand-minimal-highlight {
        background: rgba(255,255,255,0.87);
        border-radius: 22px;
        font-size: 1.14rem;
        color: #444;
        max-width: 580px;
        padding: 1.1rem 1.3rem 0.9rem 1.3rem;
        font-weight: 500;
        line-height: 1.65;
        margin-left: 0.1rem;
        margin-top: 0.1rem;
        box-shadow: 0 2px 16px rgba(255,88,88,0.07);
        text-align: left;
    }
    .brand-minimal-highlight .highlight-action {
        color: #fd5e7c;
        font-weight: 700;
        font-size: 1.09rem;
    }
    @media (max-width: 700px) {
        .brand-minimal-box { padding: 1.2rem 0.5rem 1.2rem 0.5rem;}
        .brand-minimal-header { font-size: 1.3rem; gap: 0.8rem 1.1rem;}
        .brand-minimal-header .text-main,
        .brand-minimal-header .text-brand { font-size: 1.3rem;}
        .brand-minimal-desc { font-size: 0.99rem;}
        .brand-minimal-highlight { font-size: 0.98rem; padding: 0.7rem 0.6rem;}
    }
    /* Các phần còn lại giữ nguyên */
    .features-list {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 2.4rem;
        animation: fadeIn 1.2s;
    }
    .feature-box {
        background: #fff;
        border-radius: 16px;
        padding: 1.5rem 1rem 1.1rem 1rem;
        box-shadow: 0 2px 10px rgba(80,80,120,0.09);
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        min-height: 120px;
        transition: box-shadow 0.22s, transform 0.17s, border 0.18s;
        border: 2.2px solid #f7f8fa;
        cursor: pointer;
        position: relative;
    }
    .feature-box:hover {
        box-shadow: 0 8px 32px rgba(255,88,88,0.16);
        transform: translateY(-4px) scale(1.04);
        border: 2.2px solid #f857a6;
        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
    }
    .feature-icon {
        font-size: 2.35rem;
        flex-shrink: 0;
        margin-top: 0.2rem;
        margin-right: 0.2rem;
        transition: color 0.18s;
    }
    .feature-title {
        font-weight:700;
        font-size:1.12rem;
        margin-bottom:0.15rem;
    }
    .feature-desc {
        color:#666;
        font-size:1rem;
        font-weight:500;
    }
    .welcome-form {
        background-color: #f7f9fa;
        border-radius: 18px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.07);
        padding: 2.5rem 2rem;
        margin-top: 2rem;
        transition: box-shadow 0.3s;
        max-width: 500px;
        margin-left: auto;
        margin-right: auto;
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
    @media (max-width: 800px) {
        .features-list { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
        .feature-box { min-height: 90px; }
        .welcome-form { padding: 1.2rem 0.5rem;}
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC HIỂN THỊ ---

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

# ---- FORM LÀM QUEN ----
if not st.session_state.user_name:
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng bạn đến với</span>
            <span class="text-brand">Bạn Đồng Hành!</span>
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
        
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        
        if submitted:
            if not name:
                st.warning("⚠️ Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state.user_info = {
                    "year": birth_year,
                    "school": school,
                    "issues": issues
                }
                st.success("✅ Lưu thông tin thành công! Chào mừng bạn đến với Bạn Đồng Hành!")
                st.rerun()
                
        st.markdown("</div>", unsafe_allow_html=True)

# ---- GIAO DIỆN SAU KHI ĐÃ CÓ THÔNG TIN ----
else:
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng {st.session_state.user_name} đến với</span>
            <span class="text-brand">Bạn Đồng Hành!</span>
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

    st.markdown("---")
    st.markdown("""<div class="brand-title" style="font-size:1.7rem; margin-bottom:0.3rem; text-align:left;">
    <span>✨</span> Khám phá các tính năng
    </div>""", unsafe_allow_html=True)
    
    # Danh sách tính năng với icon FontAwesome và màu nổi bật cho từng tính năng
    features = [
        {"icon": "fa-solid fa-sun", "color": "#FFB300", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày."},
        {"icon": "fa-solid fa-spa", "color": "#4CAF50", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng."},
        {"icon": "fa-solid fa-jar", "color": "#F48FB1", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười."},
        {"icon": "fa-solid fa-paintbrush", "color": "#2196F3", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc."},
        {"icon": "fa-solid fa-dice", "color": "#AB47BC", "title": "Trò Chơi Trí Tuệ", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng."},
        {"icon": "fa-solid fa-heart", "color": "#D50000", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày."},
        {"icon": "fa-solid fa-phone", "color": "#0288D1", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy."},
        {"icon": "fa-solid fa-robot", "color": "#757575", "title": "Trò Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn."},
        {"icon": "fa-solid fa-book", "color": "#F57C00", "title": "Người Kể Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn."},
    ]
    st.markdown('<div class="features-list">', unsafe_allow_html=True)
    for fe in features:
        st.markdown(
            f"""
            <div class="feature-box">
                <span class="feature-icon" style="color:{fe['color']}"><i class="{fe['icon']}"></i></span>
                <span>
                    <span class="feature-title">{fe['title']}</span><br>
                    <span class="feature-desc">{fe['desc']}</span>
                </span>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 <b>Hãy chọn một tính năng từ thanh điều hướng bên trái để bắt đầu!</b>", icon="😊")

    # Banner mini động chào mừng cuối trang
    st.markdown(
        """
        <div style="margin-top:2rem;text-align:center;">
            <img src="https://cdn.pixabay.com/photo/2017/01/31/20/13/emoji-2027186_1280.png" width="80" style="opacity:0.85;">
            <div style="font-size:1.08rem;color:#888;margin-top:0.3rem">Chúc bạn một ngày tuyệt vời! 💖</div>
        </div>
        """, unsafe_allow_html=True
    )
