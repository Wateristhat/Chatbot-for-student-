import streamlit as st

from datetime import datetime



st.set_page_config(

    page_title="Chào mừng - Bạn Đồng Hành",

    page_icon="💖",

    layout="wide"

)



# --- GOOGLE FONTS + CSS TỐI GIẢN SANG TRỌNG + CARD MENU ---

st.markdown("""

<link href="https://fonts.googleapis.com/css?family=Quicksand:700,400&display=swap" rel="stylesheet">

<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

<style>

    html, body, [class*="css"]  { font-family: 'Quicksand', Arial, sans-serif; }

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

        margin-bottom: 0.3rem;

    }

    .menu-card:hover {

        box-shadow: 0 8px 32px rgba(255,88,88,0.15);

        transform: translateY(-2px) scale(1.03);

        border: 2.2px solid #f857a6;

        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);

    }

    .menu-card, .menu-card * {

        text-decoration: none !important;

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

        text-decoration: none !important;

    }

    .menu-desc {

        color:#444;

        font-size:1.01rem;

        font-weight:500;

        margin-top:0.15rem;

        text-decoration: none !important;

    }

    @media (max-width: 700px) {

        .menu-card { min-height: 66px; padding:0.8rem 0.4rem;}

        .menu-icon { font-size: 1.5rem;}

        .menu-title { font-size:1.03rem;}

        .menu-desc { font-size:0.94rem;}

    }

</style>

""", unsafe_allow_html=True)



if 'user_name' not in st.session_state:

    st.session_state.user_name = None



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

    

    # ----------- MENU ICON CHUYỂN TRANG NHƯ HÌNH -----------

    MENU_ITEMS = [

        {

            "icon": "fa-solid fa-sun",

            "color": "#FFB300",

            "title": "Liều Thuốc Tinh Thần",

            "desc": "Nhận những thông điệp tích cực mỗi ngày.",

            "page": "1_✨_Liều_Thuốc_Tinh_Thần.py"

        },

        {

            "icon": "fa-solid fa-spa",

            "color": "#4CAF50",

            "title": "Góc An Yên",

            "desc": "Thực hành các bài tập hít thở để giảm căng thẳng.",

            "page": "2_🧘_Góc_An_Yên.py"

        },

        {

            "icon": "fa-solid fa-jar",

            "color": "#F48FB1",

            "title": "Lọ Biết Ơn",

            "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.",

            "page": "3_🍯_Lọ_biết_ơn.py"

        },

        {

            "icon": "fa-solid fa-paintbrush",

            "color": "#2196F3",

            "title": "Bảng Màu Cảm Xúc",

            "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.",

            "page": "4_🎨_Bảng_màu_cảm_xúc.py"

        },

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

        {

            "icon": "fa-solid fa-heart",

            "color": "#9C27B0",

            "title": "Góc An Yên - Hòa Nhập",

            "desc": "Trợ lý ảo và hướng dẫn âm thanh cho học sinh hòa nhập.",

            "page": "3_🫧_Góc_An_Yên.py"

        },

    ]

    st.markdown('<div class="menu-list">', unsafe_allow_html=True)

    for item in MENU_ITEMS:

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

    # ----------- END MENU -----------



    st.markdown("---")

    st.info("👈 <b>Hãy chọn một tính năng từ mục lục để bắt đầu!</b>", icon="😊")



    # Banner mini động chào mừng cuối trang

    st.markdown(

        """

        <div style="margin-top:2rem;text-align:center;">

            <img src="https://cdn.pixabay.com/photo/2017/01/31/20/13/emoji-2027186_1280.png" width="80" style="opacity:0.85;">

            <div style="font-size:1.08rem;color:#888;margin-top:0.3rem">Chúc bạn một ngày tuyệt vời! 💖</div>

        </div>

        """, unsafe_allow_html=True

    )
