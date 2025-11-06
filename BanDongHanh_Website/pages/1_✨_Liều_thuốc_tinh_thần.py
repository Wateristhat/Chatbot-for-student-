# Sửa file: pages/1_✨_Liều_thuốc_tinh_thần.py
import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import sys # ### <<< SỬA ĐỔI: Thêm import
from gtts import gTTS
from io import BytesIO

# ### <<< SỬA ĐỔI: Thêm đường dẫn để import database (nếu cần, dù file này dùng CSV) >>>
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# (File này không dùng database.py, nhưng giữ lại cũng không sao)

# --- BẢO VỆ TRANG ---
### <<< SỬA ĐỔI: Thêm bảo vệ trang ở đầu file >>>
# Kiểm tra xem người dùng đã đăng nhập chưa (ở Trang chủ)
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    # Dùng đường dẫn chính xác (tính từ app.py)
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() # Dừng chạy code của trang này

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI ---
### <<< SỬA ĐỔI: Lấy user_id từ session_state >>>
current_user_id = st.session_state.user_id

st.set_page_config(page_title="✨ Liều Thuốc Tinh Thần", page_icon="✨", layout="wide")

# --- CSS (Giữ nguyên) ---
st.markdown("""
<style>
/* (Toàn bộ CSS của bạn được giữ nguyên) */
.lttt-title-feature {
    font-size:2.6rem; font-weight:700; color:#e53935; text-align:center; margin-bottom:1.7rem; margin-top:0.7rem;
    letter-spacing:0.2px; display: flex; align-items: center; justify-content: center; gap: 1.1rem;
}
.lttt-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.6rem 2.8rem 2.4rem 2.8rem; margin-bottom:2.3rem; margin-top:0.2rem;
    text-align: center; border: 3.5px solid #e1bee7; max-width:1700px; width:100%; margin-left:auto; margin-right:auto;
}
.lttt-assist-icon {font-size:3.2rem; margin-bottom:0.7rem;}
.lttt-assist-text {font-size:1.8rem; font-weight:700; color:#6d28d9; margin-bottom:1.2rem;}
.lttt-box, .lttt-card, .lttt-footer {
    background: #fffbe7;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    font-size: 1.12rem;
    color: #333;
    border-left: 5px solid #ffd54f;
    text-align:center;
    max-width:1200px;
    margin-left:auto; margin-right:auto; margin-bottom:1.2rem;
    box-shadow:0 2px 10px rgba(255, 223, 186, 0.09);
}
.lttt-card {
    background:#fffde7;
    border-radius:17px;
    padding:1.6rem 1.1rem;
    text-align:center;
    font-size:1.21rem;
    margin:1.2rem 0;
    color:#333;
    border:2px solid #ffd54f;
    box-shadow:0 2px 10px rgba(255, 223, 186, 0.08);
    max-width:1200px;
    margin-left:auto; margin-right:auto;
}
.lttt-footer {
    background:#f3e5f5;
    border-left:5px solid #ba68c8;
    border-radius:15px;
    padding:1rem 1.3rem;
    text-align:center;
    font-size:1.12rem;
    margin:0.7rem 0 1rem 0;
    color:#333;
    max-width:1200px;
    margin-left:auto; margin-right:auto;
}
.lttt-avatar {
    font-size:2.6rem; margin-bottom:0.7rem; animation:bounce 2s infinite; display:inline-block;
}
@keyframes bounce { 0%,100%{transform:translateY(0);} 50%{transform:translateY(-7px);} }
.lttt-history-box {
    background: #e3f2fd;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    font-size: 1.09rem;
    color: #333;
    border-left: 5px solid #2196f3;
    text-align:left;
    max-width:1200px;
    margin-left:auto; margin-right:auto; margin-bottom:1rem;
}
::-webkit-scrollbar {width: 9px; background: #e3f2fd;}
::-webkit-scrollbar-thumb {background: #b3e5fc; border-radius: 8px;}
/* --- CSS ĐỂ LÀM CÁC NÚT BẤM TO HƠN --- */
.stButton > button {
    padding: 0.8rem 1.2rem;     /* Tăng khoảng đệm bên trong nút */
    font-size: 1.15rem;         /* Tăng kích thước chữ */
    font-weight: 600;           /* Làm chữ đậm hơn */
    border-radius: 12px;        /* Bo tròn góc nút cho mềm mại */
    border: 2px solid #e1bee7;  /* Thêm viền hồng nhạt đồng bộ */
    background-color: #f9f9fb;  /* Màu nền nút */
}
.stButton > button:hover {
    background-color: #f3e8ff;  /* Đổi màu khi di chuột vào */
    border-color: #ba68c8;
}
</style>
""", unsafe_allow_html=True)

# --- Trợ lý ảo đầu trang (Giữ nguyên) ---
ASSISTANT_MESSAGES = [
    ("🤖", "🌸 Bạn xứng đáng được yêu thương và quan tâm."),
    ("🤖", "✨ Mỗi người đều cần được động viên. Bee luôn bên bạn!"),
    ("🤖", "🌟 Bạn đang làm rất tốt! Hãy tiếp tục nhé!"),
    ("🤖", "🌈 Khó khăn chỉ là thử thách nhỏ, bạn sẽ vượt qua được!"),
    ("🤖", "💙 Mỗi hơi thở đều là một món quà cho bản thân."),
    ("🤖", "🦋 Từng bước nhỏ đều đưa bạn đến gần hơn với sự bình an.")
]
if "current_assistant_message" not in st.session_state or not isinstance(st.session_state.current_assistant_message, tuple):
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)

# --- Tiêu đề tính năng (Giữ nguyên) ---
st.markdown(
    '<div class="lttt-title-feature">'
    ' <span style="font-size:2.4rem;">✨</span> Liều Thuốc Tinh Thần'
    '</div>',
    unsafe_allow_html=True
)

# --- Khung trợ lý ảo (Giữ nguyên) ---
avatar, msg = st.session_state.current_assistant_message
st.markdown(f"""
<div class="lttt-assist-bigbox">
    <div class="lttt-assist-icon">{avatar}</div>
    <div class="lttt-assist-text">{msg}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,2])
with col1:
    if st.button("💬 Thông điệp mới", key="new_msg_top"):
        st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe động viên", key="tts_msg_top"):
        audio_bytes = BytesIO()
        tts = gTTS(text=msg, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format="audio/mpeg")

# --- Hộp chọn động viên (Giữ nguyên) ---
st.markdown('<div class="lttt-box">🐝 Chọn điều bạn cần nhất, Bee sẽ gửi động viên phù hợp! Bạn có thể nghe hoặc lưu lại nhé! 🌈</div>', unsafe_allow_html=True)

# --- DATA (Giữ nguyên) ---
LTTT_CATEGORIES = {
    "courage": {
        "label": "🐝 Cần Cổ Vũ",
        "icon": "🐝",
        "messages": [
            {"avatar": "🐝", "text": "Bee tin rằng bạn có thể làm được! Mỗi bước nhỏ đều rất quan trọng, cứ từ từ thôi nhé!", "name": "Ong Bee"},
            {"avatar": "🌟", "text": "Bạn là ngôi sao sáng nhất! Hãy tự tin tỏa sáng như chính mình nhé!", "name": "Sao sáng"},
            {"avatar": "🌈", "text": "Sau cơn mưa sẽ có cầu vồng! Khó khăn hôm nay sẽ là niềm vui ngày mai.", "name": "Cầu vồng"},
            {"avatar": "🦄", "text": "Bạn đặc biệt như kỳ lân! Không ai có thể thay thế được vị trí của bạn đâu!", "name": "Kỳ lân"}
        ]
    },
    "fun": {
        "label": "😊 Muốn Vui Vẻ", 
        "icon": "😊",
        "messages": [
            {"avatar": "🐧", "text": "Chim cánh cụt đi bộ lắc lư để không bị ngã. Bạn cũng cứ vui vẻ đi thôi!", "name": "Chim cánh cụt"},
            {"avatar": "🌻", "text": "Hoa hướng dương luôn quay về phía mặt trời! Hãy tìm điều tích cực nhé!", "name": "Hoa hướng dương"},
            {"avatar": "🎈", "text": "Khinh khí cầu bay cao vì chở đầy không khí vui! Bạn cũng bay cao thôi!", "name": "Khinh khí cầu"},
            {"avatar": "🐨", "text": "Gấu koala ngủ 20 tiếng/ngày mà vẫn hạnh phúc! Đôi khi chậm lại cũng tốt mà.", "name": "Gấu koala"}
        ]
    },
    "peace": {
        "label": "🫧 Tìm Bình Yên",
        "icon": "🫧", 
        "messages": [
            {"avatar": "🫧", "text": "Hãy thở sâu như những bong bóng bay... từ từ thôi, bạn đang làm rất tốt.", "name": "Bong bóng"},
            {"avatar": "🍃", "text": "Lá cây nhảy múa trong gió mà không gãy. Bạn cũng mềm mại và mạnh mẽ như vậy.", "name": "Lá cây"},
            {"avatar": "🌙", "text": "Trăng tròn hay trăng khuyết đều đẹp. Bạn lúc vui hay buồn cũng đều đáng yêu.", "name": "Trăng xinh"},
            {"avatar": "🕯️", "text": "Như ngọn nến nhỏ trong đêm tối, bạn có sức mạnh thầm lặng nhưng rất ấm áp.", "name": "Ngọn nến"}
        ]
    }
}
LTTT_CATEGORY_ORDER = ["courage", "fun", "peace"]

# --- SESSION STATE (Giữ nguyên) ---
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = None
if 'saved_encouragements' not in st.session_state:
    st.session_state.saved_encouragements = []
if 'show_journal' not in st.session_state:
    st.session_state.show_journal = False

# --- TTS động viên dưới (Giữ nguyên) ---
@st.cache_data
def create_audio_with_tts(text):
    if not text or not text.strip():
        return None
    audio_bytes = BytesIO()
    tts = gTTS(text=text.strip(), lang='vi', slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def play_encouragement_audio(message_data):
    full_text = f"{message_data['name']} nói: {message_data['text']}"
    with st.spinner("🎵 Đang chuẩn bị âm thanh cho bạn..."):
        audio_data = create_audio_with_tts(full_text)
        if audio_data:
            st.audio(audio_data, format="audio/mpeg")
            st.balloons()
        else:
            st.info("🔊 Không thể tạo âm thanh. Bạn có thể đọc nội dung ở trên nhé!")

# --- CSV Nhật ký ---
### <<< SỬA ĐỔI: Thêm `user_id` vào các hàm CSV >>>

def get_csv_path(user_id):
    """Tạo đường dẫn file CSV cá nhân hóa theo user_id."""
    # Đảm bảo user_id là tên file an toàn
    safe_user_id = "".join(c for c in user_id if c.isalnum() or c in ('_', '-')).rstrip()
    if not safe_user_id: safe_user_id = "default_user" # Dự phòng
    
    # Tên file mới: "thu_mood_journal.csv"
    filename = f"{safe_user_id}_mood_journal.csv"
    
    # Lưu file ở thư mục cha (cùng cấp với app.py)
    return os.path.join(os.path.dirname(__file__), "..", filename)

def ensure_csv_exists(user_id):
    """Đảm bảo file CSV của user_id tồn tại và có đúng cột."""
    csv_path = get_csv_path(user_id)
    
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
        df.to_csv(csv_path, index=False, encoding='utf-8')
    else:
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            if list(df.columns) != ["Ngày giờ", "Loại", "Nội dung"]:
                # Nếu file cũ sai cấu trúc, tạo file mới
                df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
        except Exception:
            # Nếu file bị lỗi không đọc được, tạo file mới
            df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
            df.to_csv(csv_path, index=False, encoding='utf-8')

def save_message_to_journal(user_id):
    """Lưu thông điệp vào file CSV CÁ NHÂN của user_id."""
    try:
        ensure_csv_exists(user_id)
        csv_path = get_csv_path(user_id)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_type = "Liều thuốc tinh thần"
        if st.session_state.current_message:
            content = f"{st.session_state.current_message['name']}: {st.session_state.current_message['text']}"
        else:
            content = "Không có nội dung"
            
        df = pd.read_csv(csv_path, encoding='utf-8')
        new_row = pd.DataFrame({
            "Ngày giờ": [current_time],
            "Loại": [message_type], 
            "Nội dung": [content]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        st.success("✅ Đã lưu thông điệp vào nhật ký cảm xúc!")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Có lỗi khi lưu thông điệp: {str(e)}")

def show_journal_history(user_id):
    """Hiển thị lịch sử từ file CSV CÁ NHÂN của user_id."""
    try:
        ensure_csv_exists(user_id)
        csv_path = get_csv_path(user_id)
        
        df = pd.read_csv(csv_path, encoding='utf-8')
        filtered_df = df[df["Loại"] == "Liều thuốc tinh thần"]
        
        if filtered_df.empty:
            st.info("📝 Chưa có thông điệp nào được lưu trong nhật ký.")
        else:
            st.markdown('<div class="lttt-history-box"><b>📖 Nhật Ký Liều Thuốc Tinh Thần</b></div>', unsafe_allow_html=True)
            filtered_df = filtered_df.sort_values("Ngày giờ", ascending=False)
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Có lỗi khi đọc nhật ký: {str(e)}")

# --- Chọn loại thông điệp (Giữ nguyên) ---
st.markdown("### 🌟 Bạn đang cần điều gì lúc này?")
cols = st.columns(len(LTTT_CATEGORY_ORDER))
for idx, cat in enumerate(LTTT_CATEGORY_ORDER):
    with cols[idx]:
        label = LTTT_CATEGORIES[cat]["label"]
        icon = LTTT_CATEGORIES[cat]["icon"]
        if st.button(f"{icon} {label}", key=f"btn_{cat}", use_container_width=True):
            st.session_state.message_category = cat
            st.session_state.current_message = random.choice(LTTT_CATEGORIES[cat]["messages"])
            st.rerun()

st.write("---")

# --- Hiển thị thông điệp (Giữ nguyên) ---
if st.session_state.current_message and st.session_state.message_category:
    msg = st.session_state.current_message
    st.markdown(
        f'<div class="lttt-card"><div class="lttt-avatar">{msg["avatar"]}</div>'
        f'<div style="font-size:1.35rem;font-weight:700;margin-bottom:0.3rem;color:#6d28d9;">{msg["text"]}</div>'
        f'<div style="font-size:1.07rem;color:#7f8c8d;margin-top:0.4rem;">💝 Từ {msg["name"]} gửi bạn</div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Nhận lời khác", key="next_msg", use_container_width=True):
            st.session_state.current_message = random.choice(
                LTTT_CATEGORIES[st.session_state.message_category]["messages"]
            )
            st.rerun()
    with col2:
        if st.button("🔊 Đọc to", key="tts_msg", use_container_width=True):
            play_encouragement_audio(msg)
    with col3:
        # Nút "Lưu vào lọ động viên" này lưu vào session_state (tạm thời, không phải lỗi bảo mật)
        # Chúng ta giữ nguyên logic này
        if st.button("💝 Lưu vào lọ động viên", key="save_enc", use_container_width=True):
            enc = {
                "avatar": msg["avatar"], "text": msg["text"],
                "name": msg["name"], "category": st.session_state.message_category,
                "saved_time": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            if enc not in st.session_state.saved_encouragements:
                st.session_state.saved_encouragements.append(enc)
                st.success("✨ Đã lưu lời động viên vào lọ!")
                st.balloons()
            else:
                st.info("💫 Lời động viên này đã có trong lọ rồi nhé!")

    col_journal1, col_journal2 = st.columns(2)
    with col_journal1:
        ### <<< SỬA ĐỔI: Truyền `current_user_id` vào hàm save >>>
        if st.button("📓 Lưu vào nhật ký cảm xúc", key="save_journal", use_container_width=True):
            save_message_to_journal(current_user_id)
            
    with col_journal2:
        if st.button("📖 Xem nhật ký đã lưu", key="view_journal", use_container_width=True):
            st.session_state.show_journal = not st.session_state.show_journal

# --- Lọ động viên cá nhân (Giữ nguyên) ---
# Logic này dùng st.session_state nên đã an toàn và riêng tư cho mỗi user
if st.session_state.saved_encouragements:
    st.write("---")
    st.markdown(f'<div class="lttt-box" style="background:#fffde7;border-left:5px solid #ffd54f;"><b>🍯 Lọ Động Viên Của Bạn ({len(st.session_state.saved_encouragements)} lời động viên)</b></div>', unsafe_allow_html=True)
    for idx, encouragement in enumerate(reversed(st.session_state.saved_encouragements)):
        with st.container():
            col1, col2, col3 = st.columns([1,6,2])
            with col1:
                st.markdown(f"<div style='font-size:2.3rem;text-align:center;'>{encouragement['avatar']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f"<div style='background:#f8f9fa;padding:1.2rem;border-radius:12px;margin:0.65rem 0;'>"
                    f"<strong>{encouragement['name']}:</strong><br>{encouragement['text']}<br>"
                    f"<small style='color:#6c757d;'>💾 {encouragement['saved_time']}</small></div>", unsafe_allow_html=True)
            with col3:
                if st.button("🔊", key=f"jar_tts_{idx}", help="Nghe lại lời động viên này"):
                    play_encouragement_audio(encouragement)
                if st.button("🗑️", key=f"jar_remove_{idx}", help="Xóa khỏi lọ động viên"):
                    st.session_state.saved_encouragements.remove(encouragement)
                    st.success("✅ Đã xóa khỏi lọ động viên!")
                    st.rerun()

# --- Nhật ký động viên ---
if st.session_state.show_journal:
    st.write("---")
    ### <<< SỬA ĐỔI: Truyền `current_user_id` vào hàm show >>>
    show_journal_history(current_user_id)
    
    if st.button("❌ Đóng nhật ký", key="close_journal"):
        st.session_state.show_journal = False
        st.rerun()

# --- Footer động viên (Giữ nguyên) ---
st.markdown('<div class="lttt-footer">💜 <strong>Nhớ nhé:</strong> Mỗi động viên nhỏ đều là một bước tiến lớn. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)

