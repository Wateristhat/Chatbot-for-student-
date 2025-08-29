import streamlit as st

st.set_page_config(page_title="Chào mừng - Bạn Đồng Hành", page_icon="💖", layout="wide")

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
    .brand-title {
        font-size: 2.5rem;
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
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="brand-banner">
    <div class="brand-title">
        <span>💖</span>
        Chào mừng đến với <span style="font-weight:900">Bạn Đồng Hành!</span>
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
