import streamlit as st

st.markdown("""
<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
.brand-minimal-box {
    background: linear-gradient(110deg, #ff82ac 3%, #fd5e7c 97%);
    border-radius: 38px;
    padding: 2.3rem 2.4rem 2.1rem 2.4rem;
    margin: 0 auto 2rem auto;
    max-width: 700px;
    box-shadow: 0 8px 32px rgba(255,88,88,0.08);
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.brand-minimal-header {
    font-family: 'Quicksand', Arial, sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: -1px;
    color: #fff;
    margin-bottom: 0.7rem;
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
    font-size: 2.2rem;
    font-weight: 800;
}
.brand-minimal-header .text-brand {
    color: #fff;
    font-size: 2.2rem;
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
    font-size: 1.13rem;
    font-weight: 500;
    margin-bottom: 1.4rem;
    margin-left: 0.2rem;
    line-height: 1.65;
}
.brand-minimal-desc .fa-heart {
    color: #ffb2be;
    font-size: 1.1rem;
    margin-right: 0.3rem;
}
.brand-minimal-highlight {
    background: rgba(255,255,255,0.78);
    border-radius: 22px;
    font-size: 1.12rem;
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
@media (max-width: 650px) {
    .brand-minimal-box { padding: 1.2rem 0.5rem 1.5rem 0.5rem; }
    .brand-minimal-header { font-size: 1.3rem; gap: 0.8rem 1.1rem;}
    .brand-minimal-header .text-main,
    .brand-minimal-header .text-brand { font-size: 1.3rem;}
    .brand-minimal-desc { font-size: 0.99rem;}
    .brand-minimal-highlight { font-size: 0.98rem; padding: 0.7rem 0.6rem;}
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="brand-minimal-box">
    <div class="brand-minimal-header">
        <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
        <span class="text-main">Chào mừng a đến với</span>
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
