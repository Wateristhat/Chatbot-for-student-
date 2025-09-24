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
        .custom-sidebar {
            width: 230px;
            min-height: 100vh;
            background: #F3F5FC;
            padding: 40px 0 0 0;
        }
        .custom-sidebar ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
        }
        .custom-sidebar li {
            margin-bottom: 16px;
        }
        .custom-sidebar .active {
            background: #e2e6ef;
            font-weight: bold;
            border-radius: 15px;
        }
        .custom-sidebar a {
            color: #444;
            font-size: 17px;
            font-weight: 600;
            text-decoration: none;
            display: block;
            padding: 10px 18px;
            border-radius: 15px;
            transition: all 0.2s;
        }
        .custom-sidebar a:hover {
            background: #dde2ee;
        }
    </style>
    """, unsafe_allow_html=True)

    menu_html = "<div class='custom-sidebar'><ul>"
    menu_html += "<li style='margin-bottom:18px;'><span style='color:#444; font-size:15px;'>app</span></li>"
    for idx, (title, link) in enumerate(menu):
        class_active = "active" if idx == active_index else ""
        menu_html += f"<li><a class='{class_active}' href='{link}'>{title}</a></li>"
    menu_html += "</ul></div>"
    st.markdown(menu_html, unsafe_allow_html=True)
