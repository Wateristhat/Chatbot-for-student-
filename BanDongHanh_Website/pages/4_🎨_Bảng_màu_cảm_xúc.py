# Sửa file: pages/4_🎨_Bảng_màu_cảm_xúc.py
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import random
from datetime import datetime
from gtts import gTTS
from io import BytesIO
import sys # ### <<< SỬA ĐỔI: Thêm import
import os  # ### <<< SỬA ĐỔI: Thêm import
import json # ### <<< SỬA ĐỔI: Thêm import

# ### <<< SỬA ĐỔI: Thêm import database >>>
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db 

# --- BẢO VỆ TRANG ---
### <<< SỬA ĐỔI: Thêm bảo vệ trang ở đầu file >>>
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.error("Bạn chưa đăng nhập! Vui lòng quay về Trang chủ.")
    st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    st.stop() # Dừng chạy code của trang này

# --- LẤY ID NGƯỜI DÙNG HIỆN TẠI ---
### <<< SỬA ĐỔI: Lấy user_id từ session_state >>>
current_user_id = st.session_state.user_id
    
st.set_page_config(page_title="🎨 Bảng Màu Cảm Xúc", page_icon="🎨", layout="wide")

# --- CSS (Giữ nguyên) ---
st.markdown("""
<style>
/* (Toàn bộ CSS của bạn được giữ nguyên) */
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
.bmcx-assist-btn-row {display:flex; justify-content: center; gap: 56px; margin-top:1.2rem;}
.bmcx-assist-action-btn {
    background: #fff; border: 2.5px solid #b39ddb; border-radius: 17px;
    font-size:1.25rem; font-weight:600; color:#6d28d9;
    padding: 1.1rem 2.5rem; cursor:pointer; box-shadow:0 2px 8px rgba(124,77,255,.14); transition:all 0.18s;
}
.bmcx-assist-action-btn:hover {background:#f3e8ff;}
.bmcx-palette-box {
    background: linear-gradient(120deg,#fffbe7 0%,#e0f7fa 100%);
    border-radius: 36px; box-shadow: 0 8px 36px rgba(124,77,255,.11);
    padding: 2.2rem 1.2rem 1.2rem 1.2rem; margin-bottom:2.2rem; margin-top:0.2rem;
    text-align: center; border: 3px solid #b39ddb; max-width:1200px; margin-left:auto; margin-right:auto;
}
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
.emotion-grid-container {
    display: flex;
    flex-wrap: nowrap;
    justify-content: space-around;
    padding: 1.5rem 0.5rem;
}
.emotion-grid-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-decoration: none !important; /* Bỏ gạch chân của link */
    color: #222;
}
.emotion-grid-item .bmcx-emotion-label {
    text-decoration: none !important;
}
@media (max-width: 768px) {
    .emotion-grid-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
        padding: 1rem;
    }
    
    .bmcx-emotion-circle {
        width: 100px;
        height: 100px;
        font-size: 2rem;
    }
}
.stButton > button {
    padding: 0.8rem 1.2rem;
    font-size: 1.15rem;
    font-weight: 600;
    width: 100%;
    margin-bottom: 0.7rem;
    border-radius: 12px;
    border: 2px solid #b39ddb;
    background-color: #f9f9fb;
    color: #6d28d9;
}
.stButton > button:hover {
    background-color: #f3e8ff;
    border-color: #5d3fd3;
    color: #5d3fd3;
}
@media (max-width:900px) {
    .bmcx-assist-bigbox, .bmcx-palette-box, .bmcx-history-box, .bmcx-note-box, .bmcx-footer {max-width:96vw;}
    .bmcx-title-feature { font-size:1.3rem; }
}
</style>
""", unsafe_allow_html=True)

# --- Data cảm xúc & màu (Giữ nguyên) ---
EMOTIONS = [
    {"label": "Vui vẻ", "emoji": "😊", "color": "#FFD600", "encourage": "Hãy lan tỏa nụ cười của bạn tới mọi người xung quanh nhé!"},
    {"label": "Buồn", "emoji": "😢", "color": "#64B5F6", "encourage": "Bạn có thể chia sẻ với Bee hoặc bạn bè để cảm thấy nhẹ lòng hơn."},
    {"label": "Lo lắng", "emoji": "😰", "color": "#FF8A65", "encourage": "Thử hít thở thật sâu hoặc nhắm mắt lại một chút nhé!"},
    {"label": "Tức giận", "emoji": "😡", "color": "#FF1744", "encourage": "Hãy thử đếm đến 10 và thở thật đều, Bee luôn ở bên bạn!"},
    {"label": "Bình yên", "emoji": "😌", "color": "#81C784", "encourage": "Bạn đang làm rất tốt! Hãy giữ tâm trạng thư thái này nhé!"},
    {"label": "Hào hứng", "emoji": "🎉", "color": "#AB47BC", "encourage": "Hãy tận dụng năng lượng tích cực để sáng tạo và vui chơi!"},
    {"label": "Ngạc nhiên", "emoji": "😲", "color": "#FFB300", "encourage": "Cuộc sống luôn đầy bất ngờ, hãy tận hưởng nhé!"}
]
### <<< SỬA ĐỔI: Thêm từ điển tra cứu ngược >>>
EMOJI_TO_LABEL = {emo["emoji"]: emo["label"] for emo in EMOTIONS}

# --- Session state (Giữ nguyên) ---
if "selected_emotion_idx" not in st.session_state:
    st.session_state.selected_emotion_idx = None
if "emotion_note" not in st.session_state:
    st.session_state.emotion_note = ""
# if "emotion_history" not in st.session_state:  ### <<< SỬA ĐỔI: Không cần nữa, dùng CSDL
#     st.session_state.emotion_history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# --- Trợ lý ảo & tên tính năng (Giữ nguyên) ---
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
    if st.button("💬 Thông điệp mới", key="new_msg_top"):
        st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe trợ lý ảo", key="tts_msg_top"):
        audio_bytes = BytesIO()
        tts = gTTS(text=msg, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format="audio/mpeg")

### <<< SỬA ĐỔI: Đảm bảo đường dẫn page_link chính xác >>>
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

# --- KHUNG VẼ CANVAS (Giữ nguyên) ---
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
    if st.session_state.selected_emotion_idx is not None:
        default_color = EMOTIONS[st.session_state.selected_emotion_idx]["color"]
    else:
        default_color = "#FF5733"
    stroke_color = st.color_picker("Màu bút:", default_color)
    bg_color = st.color_picker("Màu nền:", "#FFFFFF")

# --- BẢNG CHỌN CẢM XÚC (Giữ nguyên) ---
def select_emotion(idx):
    st.session_state.selected_emotion_idx = idx
    st.session_state.emotion_note = ""

st.markdown('<div class="bmcx-palette-box">', unsafe_allow_html=True)
st.markdown("#### Hãy chọn cảm xúc của bạn hôm nay:")

cols = st.columns(len(EMOTIONS))
for idx, (col, emo) in enumerate(zip(cols, EMOTIONS)):
    with col:
        with st.container(border=False):
            selected = st.session_state.selected_emotion_idx == idx
            selected_class = ' selected' if selected else ''
            
            st.markdown(f"""
            <div class="emotion-grid-item">
                <div class="bmcx-emotion-circle{selected_class}" style="background:{emo['color']};">
                    {emo['emoji']}
                </div>
                <div class="bmcx-emotion-label">{emo['label']}</div>
            </div>
            """, unsafe_allow_html=True)

            st.button(
                label=emo['label'], # <<< SỬA ĐỔI: Dùng tên cảm xúc (Vui vẻ, Buồn...)
                on_click=select_emotion,
                args=[idx],
                key=f"btn_emo_{idx}",
                use_container_width=True
            )

# CSS cho nút bấm ma (Giữ nguyên)
st.markdown("""
<style>
    div[data-testid="stButton"] button[key*="btn_emo_"] {
        position: absolute; 
        top: 0; left: 0; width: 100%; height: 100%;
        background: transparent !important;
        border: none !important;
        color: transparent !important; 
        box-shadow: none !important; 
    }
    div[data-testid*="stVerticalBlock"] div[data-testid="stButton"][key*="btn_emo_"]:hover + div .bmcx-emotion-circle {
        transform: scale(1.08);
        box-shadow: 0 6px 20px rgba(77,36,175,0.18);
    }
    div[data-testid*="stVerticalBlock"] div[data-testid="stButton"][key*="btn_emo_"] > div {
        position: relative;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- KHUNG VẼ (Giữ nguyên) ---
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=stroke_width,
    stroke_color=stroke_color,
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

# --- Động viên theo cảm xúc (Giữ nguyên) ---
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
            audio_bytes = BytesIO()
            tts = gTTS(text=emo['encourage'], lang='vi', slow=False)
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes.read(), format="audio/mpeg")

# --- Nhập ghi chú cảm xúc ---
if st.session_state.selected_emotion_idx is not None:
    emo = EMOTIONS[st.session_state.selected_emotion_idx] # Lấy lại emo
    
    st.markdown('<div class="bmcx-note-box">', unsafe_allow_html=True)
    st.markdown("#### 📝 Bạn muốn chia sẻ thêm về cảm xúc của mình không?")
    st.session_state.emotion_note = st.text_area(
        "",
        value=st.session_state.emotion_note,
        height=80,
        placeholder="Bạn có thể mô tả lý do, hoàn cảnh hoặc ai ở bên bạn lúc này..."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    ### <<< SỬA ĐỔI: Logic nút "Lưu" để lưu vào CSDL >>>
    if st.button("💾 Lưu cảm xúc hôm nay", type="primary", use_container_width=True):
        
        # Lấy dữ liệu từ canvas
        canvas_data = canvas_result.json_data
        
        # Kiểm tra xem người dùng đã vẽ gì chưa
        if canvas_data is None or not canvas_data.get("objects"):
            st.warning("🎨 Bạn chưa vẽ gì cả! Hãy vẽ gì đó lên khung để lưu lại tác phẩm nhé.")
        else:
            # Lưu vào CSDL
            db.add_artwork(
                user_id=current_user_id,
                emotion_emoji=emo["emoji"],
                canvas_data=json.dumps(canvas_data), # Chuyển dict thành chuỗi JSON
                title=st.session_state.emotion_note # Lưu ghi chú làm tiêu đề
            )
            
            st.success("✅ Đã lưu tác phẩm và cảm xúc vào lịch sử của bạn!")
            st.balloons()
            
            # Reset trạng thái
            st.session_state.selected_emotion_idx = None
            st.session_state.emotion_note = ""
            st.rerun()

st.write("---")

# --- Lịch sử cảm xúc ---
st.markdown("### 📖 Lịch sử cảm xúc của bạn")
if st.button("📖 Xem lịch sử", key="show_history_btn"):
    st.session_state.show_history = not st.session_state.show_history

### <<< SỬA ĐỔI: Đọc lịch sử từ CSDL >>>
if st.session_state.show_history:
    
    # Lấy TẤT CẢ tác phẩm của CHỈ người dùng này
    all_artworks = db.get_artworks_by_emotion(current_user_id) 
    
    if not all_artworks:
        st.info("Bạn chưa lưu cảm xúc nào. Hãy chọn cảm xúc, vẽ và lưu lại nhé!")
    else:
        # Lặp qua các dòng (Row) từ CSDL
        for item in all_artworks:
            # Tra cứu lại Tên cảm xúc từ Emoji
            emotion_label = EMOJI_TO_LABEL.get(item['emotion_emoji'], "Cảm xúc")
            
            st.markdown(
                f"""
                <div class="bmcx-history-box">
                    <div style='font-size:2rem;display:inline-block;'>{item['emotion_emoji']}</div>
                    <span style='font-size:1.13rem;font-weight:700;margin-left:8px;color:#5d3fd3;'>{emotion_label}</span>
                    <span style='font-size:1rem;color:#888;margin-left:12px;'>{item['timestamp']}</span>
                    <div style='margin-top:0.6rem;'>{item['title'] if item['title'] else "<i>(Không có ghi chú)</i>"}</div>
                    
                    </div>
                """,
                unsafe_allow_html=True
            )

# --- Footer (Giữ nguyên) ---
st.markdown("""
<div class="bmcx-footer">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi cảm xúc đều đáng trân trọng. Bạn hãy tự tin chia sẻ và chăm sóc cảm xúc của mình nhé! 🎨"
</div>
""", unsafe_allow_html=True)
