import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random
from datetime import datetime
from gtts import gTTS
from io import BytesIO
import sys 
import os
import tempfile # <-- 1. THÊM TEMPFILE ĐỂ SỬA LỖI ÂM THANH
import style # <-- 2. IMPORT STYLE

# --- 3. THÊM ĐƯỜNG DẪN VÀ IMPORT DATABASE ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db

# --- 4. SỬA LỖI PAGE CONFIG ---
st.set_page_config(
    page_title="🎨 Bảng Màu Cảm Xúc", 
    page_icon="🎨", 
    layout="wide",
    initial_sidebar_state="collapsed" # <-- SỬA LỖI Ở ĐÂY
)

# --- 5. ÁP DỤNG CSS CHUNG ---
style.apply_global_style()

# --- CSS giao diện (ĐÃ XÓA CSS BUTTON VÀ @MEDIA CỤC BỘ) ---
st.markdown("""
<style>
/* --- 6. XÓA CSS BUTTON CỤC BỘ (GÂY LỖI) --- */
/* (Khối .stButton > button đã bị xóa) */

/* (Giữ lại CSS tùy chỉnh của trang) */
.bmcx-title-feature {
    font-size:2.6rem; font-weight:700; color:#5d3fd3; text-align:center; margin-bottom:1.4rem; margin-top:0.7rem;
    letter-spacing:0.1px; display: flex; align-items: center; justify-content: center; gap: 1.1rem;
}
.bmcx-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom:2.3rem; margin-top:0.2rem;
    text-align: center; border: 3.5px solid #b39ddb; max-width:1700px; margin-left:auto; margin-right:auto;
}
.bmcx-assist-icon {font-size:3.2rem; margin-bottom:0.7rem;}
.bmcx-assist-text {font-size:1.7rem; font-weight:700; color:#6d28d9; margin-bottom:1.1rem;}
.bmcx-palette-box {
    background: linear-gradient(120deg,#fffbe7 0%,#e0f7fa 100%);
    border-radius: 36px; box-shadow: 0 8px 36px rgba(124,77,255,.11);
    padding: 2.2rem 1.2rem 1.2rem 1.2rem; margin-bottom:2.2rem; margin-top:0.2rem;
    text-align: center; border: 3px solid #b39ddb; max-width:1200px; margin-left:auto; margin-right:auto;
}

/* --- 10. (SỬA) CSS ĐỂ SỬA LỖI GIAO DIỆN BỊ VỠ --- */

/* Đây là CSS cho vòng tròn (nhưng nó sẽ bị CSS "small" bên dưới ghi đè) */
.bmcx-emotion-circle {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    width: 120px; height: 120px; border-radius: 50%; color: #fff; font-size: 2.3rem; font-weight:700;
    margin: 0 18px 2rem 18px; box-shadow:0 3px 18px rgba(100,100,100,0.13); cursor: pointer;
    transition: all 0.22s; border:4px solid #fff;
}
.bmcx-emotion-circle.selected {
    border: 5px solid #5d3fd3; box-shadow: 0 6px 20px rgba(77,36,175,0.18); transform: scale(1.08);
}
.bmcx-emotion-label {font-size:1.15rem; font-weight:600; color:#222; margin-top:0.6rem;}

/* (CSS tùy chỉnh của trang) */
.bmcx-note-box {
    background: #f2fcfa; border-radius: 16px; padding: 1.3rem 1.5rem; font-size:1.13rem; color:#555;
    max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:1.1rem; border-left:5px solid #80deea;
}
.bmcx-history-box {
    background: #e3f2fd; border-radius: 14px; padding: 1.05rem 1.2rem; font-size: 1.08rem; color: #333;
    border-left: 5px solid #2196f3; text-align:left; max-width:1200px; margin-left:auto; margin-right:auto; margin-bottom:1rem;
}
.bmcx-footer {
    background:#f3e5f5; border-left:5px solid #ba68c8; border-radius:15px; padding:1rem 1.3rem;
    text-align:center; font-size:1.13rem; margin:0.7rem 0 1rem 0; color:#333; max-width:1200px; margin-left:auto; margin-right:auto;
}

/* --- 10. (MỚI) CSS ĐỂ SỬA LỖI GIAO DIỆN BỊ VỠ --- */
.emotion-flex-container {
    display: flex;
    flex-wrap: wrap; /* Tự động ngắt dòng */
    justify-content: center; /* Căn giữa các emoji */
    gap: 10px; /* Khoảng cách giữa các emoji */
}
.emotion-item-wrapper {
    /* Đặt kích thước cho 1 item (đủ cho 2 item/hàng trên đt) */
    width: 140px; 
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    cursor: pointer; /* Biến cả cục thành con trỏ */
}
/* Thu nhỏ nút bấm emoji (nút thật) */
.emotion-item-wrapper .stButton > button {
     width: 100px !important; /* Phải đủ to để bấm vào vòng tròn */
     height: 100px !important;
     min-width: 100px !important;
     min-height: 100px !important;
     font-size: 2rem !important;
     padding: 0 !important;
     margin-bottom: 10px !important;
     /* Ẩn nút bấm đi */
     border: none !important;
     background: transparent !important;
     box-shadow: none !important;
     color: transparent !important; /* Ẩn emoji của nút */
}
/* Làm cho vòng tròn nằm "dưới" nút bấm + THU NHỎ */
.bmcx-emotion-circle-small {
     margin-top: -110px; /* Kéo vòng tròn lên trên (100px + 10px margin) */
     z-index: -1; /* Đưa vòng tròn ra sau nút bấm */
     /* Thu nhỏ vòng tròn (theo yêu cầu của bạn) */
     width: 100px !important;
     height: 100px !important;
     font-size: 2rem !important;
     margin-bottom: 1rem !important;
     margin-left: auto; /* Căn giữa */
     margin-right: auto; /* Căn giữa */
}
.bmcx-emotion-label-small {
    font-size: 1rem !important;
    margin-top: -10px !important; /* Kéo chữ lên */
    font-weight: 600; color:#222;
}

/* --- 6. XÓA KHỐI @media (ĐÃ GỘP VÀO STYLE.PY) --- */
/* (Khối @media (max-width:900px) đã bị xóa khỏi đây) */
</style>
""", unsafe_allow_html=True)

# --- Data cảm xúc & màu (Giữ nguyên) ---
EMOTIONS = [
    {
        "label": "Vui vẻ",
        "emoji": "😊",
        "color": "#FFD600",
        "encourage": "Hãy lan tỏa nụ cười của bạn tới mọi người xung quanh nhé!"
    },
    { "label": "Buồn", "emoji": "😢", "color": "#64B5F6", "encourage": "Bạn có thể chia sẻ với Bee hoặc bạn bè."},
    { "label": "Lo lắng", "emoji": "😰", "color": "#FF8A65", "encourage": "Thử hít thở thật sâu hoặc nhắm mắt lại."},
    { "label": "Tức giận", "emoji": "😡", "color": "#FF1744", "encourage": "Hãy thử đếm đến 10 và thở thật đều."},
    { "label": "Bình yên", "emoji": "😌", "color": "#81C784", "encourage": "Bạn đang làm rất tốt! Hãy giữ tâm trạng này."},
    { "label": "Hào hứng", "emoji": "🎉", "color": "#AB47BC", "encourage": "Hãy tận dụng năng lượng tích cực này!"},
    { "label": "Ngạc nhiên", "emoji": "😲", "color": "#FFB300", "encourage": "Cuộc sống luôn đầy bất ngờ, hãy tận hưởng!"}
]

# --- 7. SỬA LỖI ÂM THANH: DÙNG TEMPFILE ---
@st.cache_data
def generate_audio_data(text):
    """Tạo file âm thanh (dùng tempfile) và trả về data."""
    if not text or not text.strip():
        return None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            temp_path = tmp_file.name
        
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.save(temp_path)
        
        with open(temp_path, 'rb') as f:
            audio_data = f.read()
        
        os.unlink(temp_path) # Xóa file tạm
        return audio_data
    except Exception as e:
        st.error(f"Lỗi tạo file âm thanh: {e}")
        return None

def set_new_assistant_message():
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)

def set_emotion(idx, color):
    """Callback khi chọn cảm xúc."""
    st.session_state.selected_emotion_idx = idx
    st.session_state.emotion_note = ""
    st.session_state.stroke_color = color # Cập nhật màu bút vẽ

# --- Session state ---
if "selected_emotion_idx" not in st.session_state:
    st.session_state.selected_emotion_idx = None
if "emotion_note" not in st.session_state:
    st.session_state.emotion_note = ""
if "show_history" not in st.session_state:
    st.session_state.show_history = False
if "stroke_color" not in st.session_state:
    st.session_state.stroke_color = "#FF5733" # Màu mặc định ban đầu


# --- Trợ lý ảo & tên tính năng ---
ASSISTANT_MESSAGES = [
    ("🤖", "Chào mừng tới Bảng Màu Cảm Xúc! Hãy chọn cảm xúc và vẽ màu lên khung nhé!"),
    ("🤖", "Mỗi cảm xúc đều là một màu sắc tuyệt vời. Hãy tự do thể hiện!"),
    ("🤖", "Đừng ngại chia sẻ cảm xúc của mình, Bee luôn bên bạn!"),
]
if "current_assistant_message" not in st.session_state or not isinstance(st.session_state.current_assistant_message, tuple):
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
avatar, msg = st.session_state.current_assistant_message

st.markdown(
    '<div class="bmcx-title-feature">'
    ' <span style="font-size:2.3rem;">🎨</span> Bảng Màu Cảm Xúc'
    '</div>',
    unsafe_allow_html=True
)
st.markdown(f"""
<div class="bmcx-assist-bigbox">
    <div class="bmcx-assist-icon">{avatar}</div>
    <div class="bmcx-assist-text">{msg}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,2])
with col1:
    st.button("💬 Thông điệp mới", key="new_msg_top", on_click=set_new_assistant_message)
with col2:
    if st.button("🔊 Nghe trợ lý ảo", key="tts_msg_top"):
        with st.spinner("Đang tạo âm thanh..."):
            audio_data = generate_audio_data(msg)
            if audio_data:
                st.audio(audio_data, format="audio/mp3") # <-- 7. XÓA AUTOPLAY

# --- 8. SỬA LỖI ĐƯỜNG DẪN LINK ---
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")


# --- KHUNG VẼ CANVAS (trắng, vẽ tự do) ---
st.markdown("""
Đây là không gian để bạn tự do thể hiện. Không cần phải vẽ đẹp, không cần phải có ý nghĩa.  
Hãy chọn một **màu sắc** thể hiện cảm xúc của bạn lúc này và để tay bạn di chuyển một cách tự nhiên.
""")
st.write("---")

col1, col2 = st.columns(2)
with col1:
    stroke_width = st.slider("Độ dày nét bút:", min_value=1, max_value=50, value=10)
    drawing_mode = st.selectbox(
        "Công cụ:",
        ("freedraw", "line", "rect", "circle", "transform"),
        help="Chọn 'freedraw' để vẽ tự do, các công cụ khác để vẽ hình học."
    )
with col2:
    st.session_state.stroke_color = st.color_picker(
        "Màu bút:", 
        st.session_state.stroke_color
    )
    bg_color = st.color_picker("Màu nền:", "#FFFFFF")

st.markdown('<div class="bmcx-palette-box">', unsafe_allow_html=True)
st.markdown("#### Hãy chọn cảm xúc của bạn hôm nay:")

# --- 10. SỬA LỖI GIAO DIỆN BỊ VỠ (XÓA st.columns) ---
st.markdown('<div class="emotion-flex-container">', unsafe_allow_html=True) # Bắt đầu flex container

# (XÓA DÒNG emotion_cols = st.columns(len(EMOTIONS)))
for idx, emo in enumerate(EMOTIONS):
    # (XÓA DÒNG with emotion_cols[idx]:)
    
    st.markdown('<div class="emotion-item-wrapper">', unsafe_allow_html=True) # Thêm wrapper cho từng item
    
    selected = st.session_state.selected_emotion_idx == idx
    
    # NÚT BẤM (đã được CSS ẩn đi, nhưng vẫn bấm được)
    if st.button(f"{emo['emoji']}", key=f"emo_{idx}", help=emo["label"]):
        set_emotion(idx, emo["color"]) # Dùng callback
        st.rerun()

    # VÒNG TRÒN MÀU (nằm bên dưới nút)
    st.markdown(
        f"""
        <div class="bmcx-emotion-circle bmcx-emotion-circle-small {' selected' if selected else ''}" style="background:{emo['color']};">
            {emo['emoji']}
        </div>
        <div class="bmcx-emotion-label bmcx-emotion-label-small">{emo['label']}</div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True) # Đóng wrapper

st.markdown('</div>', unsafe_allow_html=True) # Đóng flex-container
st.markdown('</div>', unsafe_allow_html=True) # Đóng palette-box


canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=st.session_state.stroke_color, 
    background_color=bg_color,
    height=500,
    drawing_mode=drawing_mode,
    key="canvas",
    display_toolbar=True,
)

with st.expander("Gặp lỗi khi chạy trang này?"):
    st.info(
        """
        **Lưu ý:** Lần đầu sử dụng, bạn cần cài đặt thư viện cho tính năng này.
        Mở Terminal hoặc Command Prompt và chạy lệnh sau:
        ```bash
        pip install streamlit-drawable-canvas
        ```
        Sau đó, hãy làm mới lại trang web.
        """
    )

# --- Động viên theo cảm xúc đã chọn ---
if st.session_state.selected_emotion_idx is not None:
    emo = EMOTIONS[st.session_state.selected_emotion_idx]
    st.markdown(f"""
    <div class="bmcx-assist-bigbox" style="max-width:1200px;padding:2.1rem 1.5rem;">
        <span style="font-size:2.1rem;">{emo['emoji']}</span> <strong>{emo['encourage']}</strong>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([2,2])
    with col1:
        if st.button("🔊 Nghe động viên", key="tts_encourage"):
            with st.spinner("Đang tạo âm thanh..."):
                audio_data = generate_audio_data(emo['encourage'])
                if audio_data:
                    st.audio(audio_data, format="audio/mp3") # <-- 7. XÓA AUTOPLAY

# --- 9. CẬP NHẬT LƯU VÀO DATABASE ---
if st.session_state.selected_emotion_idx is not None:
    emo = EMOTIONS[st.session_state.selected_emotion_idx] 
    st.markdown('<div class="bmcx-note-box">', unsafe_allow_html=True)
    st.markdown("#### 📝 Bạn muốn chia sẻ thêm về cảm xúc của mình không?")
    st.session_state.emotion_note = st.text_area(
        "",
        value=st.session_state.emotion_note,
        height=80,
        placeholder="Bạn có thể mô tả lý do, hoàn cảnh hoặc ai ở bên bạn lúc này...",
        key="emotion_note_input"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("💾 Lưu cảm xúc hôm nay", type="primary", use_container_width=True):
        try:
            db.add_emotion_note(emo["label"], st.session_state.emotion_note) # <-- 9. SỬA LỖI LƯU TRỮ
            st.success("✅ Đã lưu cảm xúc vào lịch sử của bạn!")
            st.balloons()
            st.session_state.selected_emotion_idx = None
            st.session_state.emotion_note = ""
            st.rerun()
        except Exception as e:
            st.error(f"Lỗi khi lưu vào database: {e}")
            st.warning("Hãy đảm bảo bạn đã cập nhật file database.py để có bảng `emotion_notes` nhé!")

st.write("---")

# --- 9. CẬP NHẬT LẤY LỊCH SỬ TỪ DATABASE ---
st.markdown("### 📖 Lịch sử cảm xúc của bạn")
if st.button("📖 Xem/Ẩn lịch sử", key="show_history_btn"):
    st.session_state.show_history = not st.session_state.show_history

if st.session_state.show_history:
    try:
        emotion_history = db.get_emotion_notes() # <-- 9. SỬA LỖI LƯU TRỮ
        if emotion_history:
            st.write(f"Bạn có **{len(emotion_history)}** ghi chú cảm xúc đã lưu.")
            for entry_id, emotion, note, timestamp in emotion_history:
                emoji = "💖" 
                for emo_dict in EMOTIONS:
                    if emo_dict["label"] == emotion:
                        emoji = emo_dict["emoji"]
                        break
                try:
                    dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    formatted_date = dt.strftime("%d/%m/%Y lúc %H:%M")
                except:
                    formatted_date = timestamp

                st.markdown(
                    f"""
                    <div class="bmcx-history-box">
                        <div style='font-size:2rem;display:inline-block;'>{emoji}</div>
                        <span style='font-size:1.13rem;font-weight:700;margin-left:8px;color:#5d3fd3;'>{emotion}</span>
                        <span style='font-size:1rem;color:#888;margin-left:12px;'>{formatted_date}</span>
                        <div style='margin-top:0.6rem;'>{note if note else "<i>(Không có ghi chú)</i>"}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("Bạn chưa lưu cảm xúc nào. Hãy chọn và lưu cảm xúc nhé!")
    except Exception as e:
        st.error(f"Lỗi khi tải lịch sử từ database: {e}")
        st.warning("Hãy đảm bảo file database.py của bạn đã có hàm `get_emotion_notes()`.")


# --- Footer ---
st.markdown("""
<div class="bmcx-footer">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi cảm xúc đều đáng trân trọng. Bạn hãy tự tin chia sẻ và chăm sóc cảm xúc của mình nhé! 🎨"
</div>
""", unsafe_allow_html=True)
