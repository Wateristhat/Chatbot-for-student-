import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="✨ Liều Thuốc Tinh Thần",
    page_icon="✨",
    layout="centered"
)

# --- CSS CHUNG + NÚT BACK ---
st.markdown("""
<style>
    .back-btn {
        text-decoration: none;
        font-size: 0.95rem;
        color: #000;
        background: #f1f1f1;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
    }
    .back-btn:hover { background: #e5e5e5; }
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("[⬅ Về Trang chủ](0_💖_Trang_chủ.py)", unsafe_allow_html=True)

# --- CSS VÀ FONT RIÊNG CỦA TRANG ---
st.markdown("""
<link rel="stylesheet"
 href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; }
    .message-card {
        background: linear-gradient(100deg, #e1ffea 0%, #fff6eb 100%);
        border-radius: 15px; border: 1.5px solid #e3e7ea; padding: 2rem 1.3rem;
        margin: 1.5rem 0; font-size: 1.23rem; text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.07); animation: popIn 0.5s;
    }
    .category-icon {
        font-size: 2.3rem; margin-bottom: 0.25rem; display:block;
    }
    @keyframes popIn {
        0% { opacity:0; transform:scale(0.8);}
        100% { opacity:1; transform:scale(1);}
    }
    .journal-buttons {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
        flex-wrap: wrap;
    }
    .journal-btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    .journal-btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    .journal-btn-secondary {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    .journal-btn-secondary:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(240, 147, 251, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# --- THƯ VIỆN NỘI DUNG ---
MESSAGE_CATEGORIES = {
    "courage": {
        "label": "Cần Cổ Vũ",
        "icon": "<i class='fa-solid fa-bullhorn category-icon' style='color:#ff6a00'></i>",
        "messages": [
            "Hôm nay, tôi chọn bình yên.",
            "Tôi đủ mạnh mẽ để vượt qua mọi thử thách.",
            "Tôi xứng đáng được yêu thương và hạnh phúc.",
            "Mỗi hơi thở đều mang lại cho tôi sức mạnh.",
            "Tôi biết ơn vì con người của tôi ngay bây giờ."
        ]
    },
    "fun": {
        "label": "Muốn Vui Vẻ",
        "icon": "<i class='fa-solid fa-face-laugh-beam category-icon' style='color:#fbbf24'></i>",
        "messages": [
            "Sự thật thú vị: Rái cá biển thường nắm tay nhau khi ngủ để không bị trôi đi mất.",
            "Đố bạn: Cái gì luôn ở phía trước bạn, nhưng bạn không bao giờ thấy được? ... Đó là tương lai!",
            "Hãy mỉm cười nhé, vì nụ cười của bạn có thể thắp sáng một ngày của ai đó."
        ]
    },
    "peace": {
        "label": "Tìm Bình Yên",
        "icon": "<i class='fa-solid fa-spa category-icon' style='color:#49c5b6'></i>",
        "messages": [
            "Hãy hít một hơi thật sâu... và thở ra thật chậm. Bạn đang ở đây, ngay bây giờ.",
            "Nhìn ra ngoài cửa sổ. Bạn thấy màu xanh nào không?",
            "Hãy chú ý đến cảm giác của đôi chân đang chạm đất."
        ]
    }
}

# --- SESSION STATE ---
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = ""
if 'show_journal' not in st.session_state:
    st.session_state.show_journal = False

# --- HÀM XỬ LÝ ---
def select_category(category_key):
    st.session_state.message_category = category_key
    st.session_state.current_message = random.choice(
        MESSAGE_CATEGORIES[category_key]["messages"]
    )

def get_new_message():
    category_key = st.session_state.message_category
    if category_key:
        st.session_state.current_message = random.choice(
            MESSAGE_CATEGORIES[category_key]["messages"]
        )

# --- HÀM XỬ LÝ NHẬT KÝ CẢM XÚC ---
def get_csv_path():
    """Trả về đường dẫn đến file mood_journal.csv"""
    return os.path.join(os.path.dirname(__file__), "..", "mood_journal.csv")

def ensure_csv_exists():
    """Đảm bảo file CSV tồn tại với header phù hợp"""
    csv_path = get_csv_path()
    if not os.path.exists(csv_path):
        # Tạo DataFrame với header theo yêu cầu
        df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
        df.to_csv(csv_path, index=False, encoding='utf-8')
    else:
        # Kiểm tra và cập nhật header nếu cần
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            if list(df.columns) != ["Ngày giờ", "Loại", "Nội dung"]:
                # Backup dữ liệu cũ nếu có
                if not df.empty:
                    backup_path = csv_path.replace('.csv', '_backup.csv')
                    df.to_csv(backup_path, index=False, encoding='utf-8')
                # Tạo mới với header đúng
                df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
        except Exception:
            # Nếu có lỗi, tạo file mới
            df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
            df.to_csv(csv_path, index=False, encoding='utf-8')

def save_message_to_journal():
    """Lưu thông điệp hiện tại vào nhật ký cảm xúc"""
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        
        # Lấy thông tin hiện tại
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_type = "Liều thuốc tinh thần"
        content = st.session_state.current_message
        
        # Đọc file CSV hiện tại
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Thêm dòng mới
        new_row = pd.DataFrame({
            "Ngày giờ": [current_time],
            "Loại": [message_type], 
            "Nội dung": [content]
        })
        
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Lưu lại file
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        st.success("✅ Đã lưu thông điệp vào nhật ký cảm xúc!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Có lỗi khi lưu thông điệp: {str(e)}")

def show_journal_history():
    """Hiển thị lịch sử nhật ký liều thuốc tinh thần"""
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Lọc theo loại "Liều thuốc tinh thần"
        filtered_df = df[df["Loại"] == "Liều thuốc tinh thần"]
        
        if filtered_df.empty:
            st.info("📝 Chưa có thông điệp nào được lưu trong nhật ký.")
        else:
            st.subheader("📖 Nhật Ký Liều Thuốc Tinh Thần")
            
            # Sắp xếp theo thời gian mới nhất
            filtered_df = filtered_df.sort_values("Ngày giờ", ascending=False)
            
            # Hiển thị bảng
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày giờ": st.column_config.DatetimeColumn(
                        "Ngày giờ",
                        format="DD/MM/YYYY HH:mm:ss"
                    ),
                    "Loại": st.column_config.TextColumn(
                        "Loại",
                        width="medium"
                    ),
                    "Nội dung": st.column_config.TextColumn(
                        "Nội dung",
                        width="large"
                    )
                }
            )
            
            st.info(f"📊 Tổng cộng: {len(filtered_df)} thông điệp đã lưu")
            
    except Exception as e:
        st.error(f"❌ Có lỗi khi đọc nhật ký: {str(e)}")

# --- GIAO DIỆN CHÍNH ---
st.markdown("<div class='page-title'>✨ Liều Thuốc Tinh Thần Cho Bạn</div>", unsafe_allow_html=True)

st.markdown(
    "<div style='font-size:1.1rem;line-height:1.6;'>"
    "Đôi khi, chúng ta chỉ cần một lời nhắc nhở nhỏ để cảm thấy tốt hơn.<br>"
    "<b>Bạn đang cần điều gì lúc này?</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Nút chọn loại thông điệp
cols = st.columns(len(MESSAGE_CATEGORIES))
for idx, (key, value) in enumerate(MESSAGE_CATEGORIES.items()):
    with cols[idx]:
        st.button(
            label=value["label"],
            on_click=select_category,
            args=(key,),
            key=f"btn_{key}",
            use_container_width=True
        )

st.write("---")

# Hiển thị thông điệp
if st.session_state.current_message and st.session_state.message_category:
    category_key = st.session_state.message_category
    category_info = MESSAGE_CATEGORIES[category_key]
    
    st.markdown(f"""
    <div class="message-card">
        {category_info['icon']}
        <div>{st.session_state.current_message}</div>
    </div>
    """, unsafe_allow_html=True)

    st.button(
        "🔄 Nhận một thông điệp khác cùng loại",
        on_click=get_new_message,
        key="btn_next_message",
        use_container_width=True
    )
    
    # --- NÚT NHẬT KÝ CẢM XÚC ---
    st.write("")  # Khoảng cách
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "💾 Lưu thông điệp này vào nhật ký cảm xúc",
            key="btn_save_journal",
            use_container_width=True
        ):
            save_message_to_journal()
    
    with col2:
        if st.button(
            "📖 Xem nhật ký liều thuốc tinh thần", 
            key="btn_view_journal",
            use_container_width=True
        ):
            st.session_state.show_journal = not st.session_state.show_journal

    if random.random() < 0.2:
        st.balloons()

# --- HIỂN THỊ NHẬT KÝ NẾU ĐƯỢC YÊU CẦU ---
if st.session_state.show_journal:
    st.write("---")
    show_journal_history()
    
    # Nút đóng nhật ký
    if st.button("❌ Đóng nhật ký", key="btn_close_journal"):
        st.session_state.show_journal = False
        st.rerun()
