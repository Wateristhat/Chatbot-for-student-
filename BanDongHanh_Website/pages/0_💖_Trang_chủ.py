# File: 0_💖_Trang_chủ.py
import streamlit as st
from datetime import datetime


st.set_page_config(
    page_title="Chào mừng - Bạn Đồng Hành",
    page_icon="💖",
    layout="wide"
)


# --- CSS (Giữ nguyên) ---
# ... (Phần trước) ...

# --- SỬA ĐỔI CSS ĐỂ NÚT ẨN HOẠT ĐỘNG ---
st.markdown("""
<style>
    /* ẨN label st.page_link mặc định */
    div[data-testid="stPageLink"] label { visibility: hidden; height: 0; }
    
    /* Làm cho st.page_link (nút bấm) trong suốt và đè lên trên */
    div[data-testid="stPageLink"] button {
        position: absolute; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%;
        
        /* LÀM CHO NÚT TRONG SUỐT VÀ KHÔNG GÂY ẢNH HƯỞNG */
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        
        z-index: 10; /* Đảm bảo nút này nằm trên div menu-card */
        cursor: pointer;
    }
    
    /* [CẢNH BÁO: DÒNG NÀY ĐÃ ĐƯỢC XÓA]
    div[data-testid="stVerticalBlock"] > div:nth-child(2) > div:nth-child(2) {
        position: relative;
    }
    */
    
    /* Thiết lập lại bối cảnh vị trí tương đối cho mỗi mục menu */
    div[data-testid="stVerticalBlock"] > div:has(> button[key*="link_to_"]) {
        position: relative; 
    }
    
    .menu-card {
        position: relative;
        z-index: 5;
    }
    
    /* Áp dụng hiệu ứng hover khi nút ẩn bị hover */
    div[data-testid="stPageLink"] button:hover { /* Sửa target hover */
        transform: translateY(-2px) scale(1.01);
        border: 2.2px solid #f857a6;
        box-shadow: 0 8px 32px rgba(255,88,88,0.15);
        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
    }

</style>
""", unsafe_allow_html=True)

# --- LOGIC ĐĂNG NHẬP ---
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if not st.session_state.user_name:
    # --- Giao diện chưa đăng nhập ---
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng bạn đến với</span> <span class="text-brand">Bạn Đồng Hành!</span>
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
        name = st.text_input("📝 Bạn tên là gì?")
        submitted = st.form_submit_button("💖 Lưu thông tin và bắt đầu!")
        if submitted:
            if not name:
                st.warning("⚠️ Bạn ơi, hãy cho mình biết tên của bạn nhé!")
            else:
                st.session_state.user_name = name
                st.session_state['user_id'] = name
                st.session_state.user_info = {}
                st.success("✅ Lưu thông tin thành công! Chào mừng bạn đến với Bạn Đồng Hành!")
                st.rerun()
else:
    # --- Giao diện đã đăng nhập ---
    st.markdown(f"""
    <div class="brand-minimal-box">
        <div class="brand-minimal-header">
            <span class="brand-minimal-icon"><i class="fa-solid fa-heart"></i></span>
            <span class="text-main">Chào mừng {st.session_state.user_name} đến với</span> <span class="text-brand">Bạn Đồng Hành!</span>
        </div>
        <div style="text-align: right; margin-top: -1.5rem; margin-right: 1.5rem;">
            <form action="." method="get" target="_self">
                <input type="hidden" name="logout" value="true">
                <button type="submit" style="
                    background: none; border: none; color: #ffb2be; 
                    font-size: 1rem; font-weight: 600; cursor: pointer;
                    text-decoration: underline; padding: 0;
                ">❌ Đăng xuất</button>
            </form>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Thêm logic Đăng xuất
    if st.query_params.get("logout") == "true":
        st.session_state.user_name = None
        st.session_state.user_id = None
        st.query_params.clear()
        st.rerun()

    st.markdown("---")
    st.markdown("""<div style="font-size:1.7rem; font-weight:700; margin-bottom:0.3rem;">✨ Khám phá các tính năng</div>""", unsafe_allow_html=True)
    
    # ----------- MENU MỚI SỬ DỤNG st.page_link ẨN (FIX LỖI MẤT ĐĂNG NHẬP) -----------
    
    MENU_ITEMS = [
        {"icon": "fa-solid fa-sun", "color": "#FFB300", "title": "Liều Thuốc Tinh Thần", "desc": "Nhận những thông điệp tích cực mỗi ngày.", "file": "1_✨_Liều_thuốc_tinh_thần.py"},
        {"icon": "fa-solid fa-spa", "color": "#4CAF50", "title": "Góc An Yên", "desc": "Thực hành các bài tập hít thở để giảm căng thẳng.", "file": "2_🫧_Góc_An_Yên.py"},
        {"icon": "fa-solid fa-jar", "color": "#F48FB1", "title": "Lọ Biết Ơn", "desc": "Ghi lại những điều nhỏ bé khiến bạn mỉm cười.", "file": "3_🍯_Lọ_biết_ơn.py"},
        {"icon": "fa-solid fa-paintbrush", "color": "#2196F3", "title": "Bảng Màu Cảm Xúc", "desc": "Thỏa sức sáng tạo, vẽ để giải tỏa cảm xúc.", "file": "4_🎨_Bảng_màu_cảm_xúc.py"},
        {"icon": "fa-solid fa-dice", "color": "#AB47BC", "title": "Nhanh Tay Lẹ Mắt", "desc": "Thử thách bản thân với các trò chơi nhẹ nhàng.", "file": "5_🎮_Nhanh_tay_lẹ_mắt.py"},
        {"icon": "fa-solid fa-heart", "color": "#D50000", "title": "Góc Nhỏ", "desc": "Xây dựng kế hoạch chăm sóc bản thân mỗi ngày.", "file": "6_💖_Góc_nhỏ.py"},
        {"icon": "fa-solid fa-phone", "color": "#0288D1", "title": "Hỗ Trợ Khẩn Cấp", "desc": "Danh sách các nguồn lực và đường dây nóng đáng tin cậy.", "file": "7_🆘_Hỗ_Trợ_Khẩn_Cấp.py"},
        {"icon": "fa-solid fa-robot", "color": "#757575", "title": "Trò Chuyện", "desc": "Một người bạn AI luôn sẵn sàng lắng nghe bạn.", "file": "8_💬_Trò_chuyện.py"},
        {"icon": "fa-solid fa-book", "color": "#F57C00", "title": "Người Kể Chuyện", "desc": "Lắng nghe những câu chuyện chữa lành tâm hồn.", "file": "9_📖_Người_Kể_Chuyện.py"}
    ]
    
    st.markdown('<div class="menu-list">', unsafe_allow_html=True)

    for item in MENU_ITEMS:
        # Sử dụng st.container để bọc nội dung và nút bấm lại
        with st.container(border=False):
            
            # 1. Hiển thị giao diện đẹp bằng CSS (sử dụng lại class menu-card)
            st.markdown(
                f"""
                <div class="menu-card menu-card-style-only">
                    <span class="menu-icon" style="color:{item['color']}"><i class="{item['icon']}"></i></span>
                    <span>
                        <span class="menu-title">{item['title']}</span><br>
                        <span class="menu-desc">{item['desc']}</span>
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )

            # 2. Tạo nút bấm/link ẩn (st.page_link) ĐÈ LÊN trên khối HTML
            st.page_link(
                f"pages/{item['file']}", 
                label=f"Link to {item['title']}", # Label ẩn
                key=f"link_to_{item['file']}",
                use_container_width=True
            )
            
    st.markdown('</div>', unsafe_allow_html=True)
    # ----------- KẾT THÚC MENU MỚI -----------

# --- SỬA ĐỔI CSS ĐỂ NÚT ẨN HOẠT ĐỘNG (Dán lại phần này) ---
st.markdown("""
<style>
    /* ẨN label st.page_link mặc định */
    div[data-testid="stPageLink"] label { visibility: hidden; height: 0; }
    
    /* Làm cho st.page_link (nút bấm) trong suốt và đè lên trên */
    div[data-testid="stPageLink"] button {
        position: absolute; 
        top: 0; 
        left: 0; 
        width: 100%; 
        height: 100%;
        
        /* LÀM CHO NÚT TRONG SUỐT VÀ KHÔNG GÂY ẢNH HƯỞNG */
        background: transparent !important;
        color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        
        z-index: 10; /* Đảm bảo nút này nằm trên div menu-card */
        cursor: pointer;
    }
    
    /* Điều chỉnh các phần tử bọc để vị trí absolute hoạt động */
    div[data-testid="stVerticalBlock"] > div:nth-child(2) > div:nth-child(2) {
        position: relative;
    }
    .menu-card {
        position: relative;
        z-index: 5;
    }
    /* Loại bỏ hiệu ứng hover gốc của thẻ menu-card khi nó được bao bởi container */
    .menu-list .menu-card-style-only:hover {
        /* Bỏ các thuộc tính hover cũ của thẻ <a> */
        box-shadow: 0 2px 10px rgba(80,80,120,0.10); /* Giữ nguyên khi không hover */
        transform: none;
        border: 2.2px solid transparent;
        background: #fff;
    }
    
    /* Áp dụng hiệu ứng hover khi nút ẩn bị hover (tức là người dùng rê chuột) */
    div[data-testid="stPageLink"] button:hover ~ div .menu-card-style-only {
        box-shadow: 0 8px 32px rgba(255,88,88,0.15);
        transform: translateY(-2px) scale(1.01);
        border: 2.2px solid #f857a6;
        background: linear-gradient(90deg,#fff6f6 60%,#f7f8fa 100%);
    }

</style>
""", unsafe_allow_html=True)

