import streamlit as st
from datetime import datetime

# --- CẤU HÌNH TRANG CHÍNH ---
st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)

# --- GOOGLE FONTS + ANIMATION + CSS THƯƠNG HIỆU ---
st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }
    .brand-banner {
        background: linear-gradient(120deg, #f857a6 0%, #ff5858 100%);
        border-radius: 22px;
        padding: 2.2rem 3vw 2.8rem 3vw;
        margin: 0 auto 2.4rem auto;
        box-shadow: 0 8px 32px rgba(255,88,88,0.09);
        position: relative;
        animation: fadeIn 1.2s;
    }
    .brand-sparkle {
        position: absolute;
        top: 18px; left: 38px;
        font-size: 2.9rem;
        animation: sparkleMove 2.2s infinite alternate;
        opacity: 0.8;
        pointer-events: none;
    }
    @keyframes sparkleMove {
        0% { transform: scale(1) rotate(-6deg);}
        100% { transform: scale(1.18) rotate(7deg);}
    }
    @keyframes fadeIn {
        0% { opacity:0; transform: translateY(30px);}
        100% { opacity:1; transform: translateY(0);}
    }
    .brand-title {
        font-size: 2.7rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.3rem;
        background: linear-gradient(90deg,#ffb6b9 13%,#f5f7fa 79%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        -webkit-text-fill-color: transparent;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
    }
    .brand-subtext {
        font-size: 1.22rem;
        color: #fff;
        text-align: center;
        padding: 0.5rem 0 0.2rem 0;
        font-weight: 500;
        text-shadow: 0 2px 16px rgba(80,80,120,0.13);
        margin-bottom: 0.8rem;
    }
    .brand-desc {
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        font-size: 1.13rem;
        color: #333;
        max-width: 570px;
        margin: 0.4rem auto 0 auto;
        padding: 1rem 2vw;
        box-shadow: 0 2px 16px rgba(255,88,88,0.07);
        font-weight: 500;
        text-align: center;
    }
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
        transition: box-shadow 0.22s, transform 0.17s;
        border: 2.2px solid #f7f8fa;
        cursor: pointer;
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
    @media (max-width: 800px) {
        .brand-banner { padding:1.2rem 1vw 1.5rem 1vw;}
        .brand-title { font-size:2rem;}
        .brand-desc { font-size:1.01rem;}
        .features-list { grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); }
        .feature-box { min-height: 90px; }
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC HIỂN THỊ ---

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

if st.session_state.user_name:
    # Banner thương hiệu nổi bật
    st.markdown(f"""
    <div class="brand-banner">
        <span class="brand-sparkle">✨</span>
        <div class="brand-title">
            <span>💖</span>
            Chào mừng {st.session_state.user_name} đến với <span style="font-weight:900">Bạn Đồng Hành!</span>
        </div>
        <div class="brand-subtext">
            <i class="fa-solid fa-heart" style="color:#ff6a00;margin-right:7px;"></i>
            <b>“Bạn Đồng Hành”</b> – Người bạn thấu cảm, luôn bên cạnh trên hành trình chăm sóc sức khỏe tinh thần.
        </div>
        <div class="brand-desc">
            Cùng truyền cảm hứng và lan tỏa yêu thương mỗi ngày. Được thiết kế để giúp bạn vượt qua thử thách trong học tập, cuộc sống, và nuôi dưỡng sự cân bằng cảm xúc.<br>
            <span style="color:#ff5858;font-weight:700;">Hãy bắt đầu khám phá nhé!</span>
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
