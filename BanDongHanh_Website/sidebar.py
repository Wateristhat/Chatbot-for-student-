import streamlit as st

def render_sidebar(active_index=None):
    menu = [
        ("❤️ Trang chủ", "0_💖_Trang_chủ.py"),
        ("✨ Liều thuốc tinh thần", "1_✨_Liều_thuốc_tinh_thần.py"),
        ("🧘‍♂️ Góc An Yên", "2_🧘‍♂️_Góc_An_Yên.py"),
        ("🪴 Lọ biết ơn", "3_🪴_Lọ_biết_ơn.py"),
        ("🎨 Bảng màu cảm xúc", "4_🎨_Bảng_màu_cảm_xúc.py"),
        ("🎮 Nhanh tay lẹ mắt", "5_🎮_Nhanh_tay_lẹ_mắt.py"),
        ("💝 Góc nhỏ", "6_💝_Góc_nhỏ.py"),
        ("🆘 Hỗ Trợ Khẩn Cấp", "7_🆘_Hỗ_Trợ_Khẩn_Cấp.py"),
        ("💬 Trò chuyện", "8_💬_Trò_chuyện.py"),
        ("📖 Người Kể Chuyện", "9_📖_Người_Kể_Chuyện.py")
    ]
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&display=swap');
        .custom-sidebar {
            width: 240px;
            min-height: 100vh;
            background: #F3F5FC;
            padding: 36px 0 0 0;
            font-family: 'Quicksand', Arial, sans-serif;
            border-right: 0px solid #e6e6e6;
        }
        .custom-sidebar ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .custom-sidebar li {
            margin-bottom: 10px;
        }
        .custom-sidebar .active {
            background: #e2e6ef;
            font-weight: 700;
            border-radius: 13px;
            color: #444 !important;
            box-shadow: 0 0 0 1.5px #e2e6ef;
        }
        .custom-sidebar a {
            color: #444;
            font-size: 17px;
            font-weight: 600;
            text-decoration: none;
            display: flex;
            align-items: center;
            padding: 11px 20px;
            border-radius: 13px;
            transition: background 0.18s, font-weight 0.18s;
            margin: 0;
        }
        .custom-sidebar a:hover {
            background: #dde2ee;
            font-weight: 700;
        }
        .custom-sidebar li:first-child {
            margin-bottom: 20px;
        }
        .custom-sidebar span.menu-title {
            color: #888;
            font-size: 15px;
            font-weight: 600;
            margin-left: 18px;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
            display: block;
        }
    </style>
    """, unsafe_allow_html=True)

    menu_html = "<div class='custom-sidebar'><ul>"
    menu_html += "<li><span class='menu-title'>app</span></li>"
    for idx, (title, link) in enumerate(menu):
        class_active = "active" if idx == active_index else ""
        menu_html += f"<li><a class='{class_active}' href='{link}'>{title}</a></li>"
    menu_html += "</ul></div>"
    st.sidebar.markdown(menu_html, unsafe_allow_html=True)
