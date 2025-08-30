import streamlit as st

# --- THÊM FONT & CSS CHO CARD MENU ---
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
.menu-list {
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
    margin-top: 1.5rem;
    margin-bottom: 2.2rem;
}
.menu-card {
    background: #fff;
    border-radius: 18px;
    box-shadow: 0 2px 10px rgba(80,80,120,0.10);
    display: flex;
    align-items: center;
    gap: 1.3rem;
    min-height: 86px;
    transition: box-shadow 0.19s, transform 0.12s;
    border: none;
    cursor: pointer;
    padding: 1.20rem 1.2rem 1.1rem 1.2rem;
    position: relative;
    text-decoration: none;
}
.menu-card:hover {
    box-shadow: 0 8px 32px rgba(255,88,88,0.15);
    transform: translateY(-2px) scale(1.03);
    border: 2.2px solid #f857a6;
    background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
}
.menu-icon {
    font-size: 2.3rem;
    flex-shrink: 0;
    margin-right: 0.1rem;
}
.menu-title {
    font-weight:700;
    font-size:1.18rem;
    margin-bottom:0.13rem;
    color: #222;
}
.menu-desc {
    color:#444;
    font-size:1.01rem;
    font-weight:500;
    margin-top:0.15rem;
}
@media (max-width: 700px) {
    .menu-card { min-height: 66px; padding:0.8rem 0.4rem;}
    .menu-icon { font-size: 1.5rem;}
    .menu-title { font-size:1.03rem;}
    .menu-desc { font-size:0.94rem;}
}
</style>
""", unsafe_allow_html=True)

MENU_ITEMS = [
    {
        "icon": "fa-solid fa-dice",
        "color": "#AB47BC",
        "title": "Trò Chơi Trí Tuệ",
        "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.",
        "page": "5_🎮_Nhanh_tay_le_mat.py"
    },
    {
        "icon": "fa-solid fa-heart",
        "color": "#D50000",
        "title": "Góc Nhỏ",
        "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.",
        "page": "6_❤️_Góc_nhỏ.py"
    },
    {
        "icon": "fa-solid fa-phone",
        "color": "#0288D1",
        "title": "Hỗ Trợ Khẩn Cấp",
        "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy.",
        "page": "7_📞_Ho_tro_khan_cap.py"
    },
    {
        "icon": "fa-solid fa-robot",
        "color": "#757575",
        "title": "Trò Chuyện",
        "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.",
        "page": "8_🤖_Tro_chuyen.py"
    },
    {
        "icon": "fa-solid fa-book",
        "color": "#F57C00",
        "title": "Người Kể Chuyện",
        "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.",
        "page": "9_📖_Nguoi_ke_chuyen.py"
    },
]

st.markdown('<div class="menu-list">', unsafe_allow_html=True)

for item in MENU_ITEMS:
    # Sử dụng markdown với thẻ <a> để chuyển trang, icon đẹp và bắt mắt
    st.markdown(
        f"""
        <a href="/{item['page']}" class="menu-card" target="_self">
            <span class="menu-icon" style="color:{item['color']}"><i class="{item['icon']}"></i></span>
            <span>
                <span class="menu-title">{item['title']}</span><br>
                <span class="menu-desc">{item['desc']}</span>
            </span>
        </a>
        """,
        unsafe_allow_html=True
    )

st.markdown('</div>', unsafe_allow_html=True)
