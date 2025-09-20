import streamlit as st
from streamlit_drawable_canvas import st_canvas
import json
import random
from gtts import gTTS
from io import BytesIO
import base64
import sys
import os
from datetime import datetime

# Thêm đường dẫn để import database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import add_artwork, get_artworks_by_date, get_artwork_data

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Bảng màu cảm xúc", page_icon="🎨", layout="wide")

# --- KHỞI TẠO SESSION STATE ---
if 'selected_emotion' not in st.session_state:
    st.session_state.selected_emotion = ""
if 'emotion_description' not in st.session_state:
    st.session_state.emotion_description = ""

# --- CSS TÙY CHỈNH CHO GIAO DIỆN THÂN THIỆN ---
st.markdown("""
<style>
    .main-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 20px;
        margin: 10px;
    }
    
    .friendly-header {
        font-size: 2.5rem;
        color: #6a5acd;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    
    .assistant-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .emotion-selector {
        background: #fff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    .drawing-tools {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 2px solid #e9ecef;
    }
    
    .celebration {
        animation: bounce 2s infinite;
        text-align: center;
        font-size: 2rem;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
        40% { transform: translateY(-30px); }
        60% { transform: translateY(-15px); }
    }
    
    .timeline-item {
        background: white;
        padding: 15px;
        margin: 10px 0;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- DANH SÁCH CẢM XÚC VÀ LỜI KHUYẾN KHÍCH ---
EMOTIONS = {
    "😊": "Vui vẻ",
    "😢": "Buồn bã", 
    "😠": "Tức giận",
    "😰": "Lo lắng",
    "😍": "Yêu thương",
    "🤔": "Suy tư",
    "😴": "Mệt mỏi",
    "🥳": "Phấn khích",
    "😔": "Thất vọng",
    "🤗": "Ấm áp"
}

ENCOURAGEMENT_MESSAGES = [
    "Hãy để cảm xúc của bạn trở thành những nét cọ tuyệt đẹp! 🎨",
    "Mỗi màu sắc đều kể một câu chuyện riêng của bạn! 🌈",
    "Không có gì sai cả, chỉ có những sáng tạo độc đáo! ✨",
    "Hãy thể hiện bản thân một cách tự do nhất! 🦋",
    "Tranh của bạn là duy nhất trên thế giới này! 💫",
    "Cảm xúc là nguồn cảm hứng tuyệt vời nhất! 💝",
    "Hãy tô màu cho tâm hồn của bạn! 🎭",
    "Mỗi nét vẽ đều có giá trị đặc biệt! 🌟"
]

AVATAR_EMOJIS = ["🧚‍♀️", "🦄", "🌸", "⭐", "🎈", "🌙", "🦋", "🌻"]

# --- HÀM TEXT-TO-SPEECH ---
@st.cache_data
def text_to_speech(text):
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Lỗi tạo âm thanh: {e}")
        return None

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<h1 class="friendly-header">🎨 Bảng màu cảm xúc</h1>', unsafe_allow_html=True)

# Nút quay về trang chủ
st.markdown("⬅️ [🏠 Quay về Trang chủ](../0_💖_Trang_chủ.py)")

# --- TRỢ LÝ ẢO ĐỘNG VIÊN ---
if 'current_message' not in st.session_state:
    st.session_state.current_message = random.choice(ENCOURAGEMENT_MESSAGES)
    st.session_state.current_avatar = random.choice(AVATAR_EMOJIS)

# Thay đổi thông điệp mỗi 30 giây hoặc khi người dùng tương tác
if st.button("🔄 Lời khuyến khích mới", key="new_encouragement"):
    st.session_state.current_message = random.choice(ENCOURAGEMENT_MESSAGES)
    st.session_state.current_avatar = random.choice(AVATAR_EMOJIS)

st.markdown(f"""
<div class="assistant-box">
    <h3>{st.session_state.current_avatar} Trợ lý nhỏ của bạn nói:</h3>
    <p style="font-size: 1.2rem; font-style: italic;">"{st.session_state.current_message}"</p>
</div>
""", unsafe_allow_html=True)

# --- NÚT ĐỌC TO HƯỚNG DẪN ---
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("### 📝 Hướng dẫn sử dụng")
    instructions = """
    Đây là không gian để bạn tự do thể hiện cảm xúc qua màu sắc và hình vẽ. 
    Hãy chọn emoji cảm xúc phù hợp với tâm trạng hiện tại của bạn, 
    sau đó để tay bạn di chuyển một cách tự nhiên trên bảng vẽ. 
    Không cần phải vẽ đẹp hay có ý nghĩa gì cả - chỉ cần thể hiện cảm xúc thật của bạn.
    """
    st.write(instructions)

with col2:
    if st.button("🔊 Đọc to hướng dẫn", key="tts_instructions"):
        with st.spinner("Đang chuẩn bị âm thanh..."):
            audio_data = text_to_speech(instructions)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

st.write("---")

# --- CHỌN EMOJI CẢM XÚC ---
st.markdown('<div class="emotion-selector">', unsafe_allow_html=True)
st.markdown("### 💭 Cảm xúc của bạn hiện tại:")

# Tạo lưới emoji
emotion_cols = st.columns(5)
selected_emotion = None

for i, (emoji, description) in enumerate(EMOTIONS.items()):
    col_index = i % 5
    with emotion_cols[col_index]:
        if st.button(f"{emoji}\n{description}", key=f"emotion_{emoji}", use_container_width=True):
            st.session_state.selected_emotion = emoji
            st.session_state.emotion_description = description

# Hiển thị cảm xúc đã chọn
selected_emotion = st.session_state.get("selected_emotion", "")
emotion_description = st.session_state.get("emotion_description", "")

if selected_emotion:
    st.success(f"Cảm xúc đã chọn: {selected_emotion} {emotion_description}")
else:
    st.info("Hãy chọn một cảm xúc phù hợp với tâm trạng của bạn!")

st.markdown('</div>', unsafe_allow_html=True)

# --- KHU VỰC VẼ (CHỈ HIỆN KHI ĐÃ CHỌN CẢM XÚC) ---
if selected_emotion:
    st.write("---")
    st.markdown('<div class="drawing-tools">', unsafe_allow_html=True)
    st.markdown("### 🎨 Công cụ vẽ")
    
    # Công cụ vẽ với giao diện thân thiện hơn
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.markdown("#### 🖌️ Nét vẽ")
        stroke_width = st.slider("Độ dày nét bút:", min_value=1, max_value=50, value=15, 
                                help="Chọn độ dày phù hợp với cảm xúc của bạn")
        
        drawing_mode = st.selectbox(
            "Kiểu vẽ:",
            ("freedraw", "line", "rect", "circle"),
            help="Chọn 'freedraw' để vẽ tự do",
            format_func=lambda x: {
                "freedraw": "🖍️ Vẽ tự do", 
                "line": "📏 Đường thẳng",
                "rect": "⬛ Hình chữ nhật", 
                "circle": "⭕ Hình tròn"
            }[x]
        )
    
    with tool_col2:
        st.markdown("#### 🎨 Màu sắc")
        
        # Màu sắc đề xuất theo cảm xúc
        emotion_colors = {
            "😊": "#FFD700",  # Vàng vui vẻ
            "😢": "#4169E1",  # Xanh buồn
            "😠": "#DC143C",  # Đỏ tức giận
            "😰": "#808080",  # Xám lo lắng
            "😍": "#FF69B4",  # Hồng yêu thương
            "🤔": "#9370DB",  # Tím suy tư
            "😴": "#2F4F4F",  # Xanh đậm mệt mỏi
            "🥳": "#FF4500",  # Cam phấn khích
            "😔": "#8B4513",  # Nâu thất vọng
            "🤗": "#FFA500"   # Cam ấm áp
        }
        
        suggested_color = emotion_colors.get(selected_emotion, "#FF5733")
        emotion_desc = st.session_state.get("emotion_description", "")
        stroke_color = st.color_picker("Màu bút:", suggested_color, 
                                     help=f"Màu gợi ý cho cảm xúc {emotion_desc}")
        
        # Màu nền dịu mắt
        bg_colors = {
            "🌸 Hồng nhạt": "#FFF0F5",
            "☁️ Trắng mây": "#F8F8FF", 
            "🌿 Xanh nhạt": "#F0FFF0",
            "🌅 Cam nhạt": "#FFF8DC",
            "💜 Tím nhạt": "#F8F0FF"
        }
        
        bg_name = st.selectbox("Màu nền:", list(bg_colors.keys()))
        bg_color = bg_colors[bg_name]
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # --- KHUNG VẼ CANVAS ---
    st.markdown("### 🖼️ Bảng vẽ cảm xúc")
    st.write("Hãy để cảm xúc của bạn tự do bay bổng trên bảng vẽ này!")
    
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        height=600,  # Tăng chiều cao
        drawing_mode=drawing_mode,
        key="emotion_canvas",
        display_toolbar=True,
    )
    
    # --- NÚT LUU TÁC PHẨM ---
    save_col1, save_col2 = st.columns([2, 1])
    
    with save_col1:
        emotion_desc = st.session_state.get("emotion_description", "")
        artwork_title = st.text_input("Đặt tên cho tác phẩm của bạn (tùy chọn):", 
                                    placeholder=f"Tranh {emotion_desc} của tôi" if emotion_desc else "Tác phẩm của tôi")
    
    with save_col2:
        if st.button("💾 Lưu tác phẩm", type="primary", use_container_width=True):
            if canvas_result.json_data is not None:
                try:
                    # Lưu dữ liệu canvas dưới dạng JSON string
                    canvas_data = json.dumps(canvas_result.json_data)
                    emotion_desc = st.session_state.get("emotion_description", "")
                    title = artwork_title if artwork_title else f"Tranh {emotion_desc}" if emotion_desc else "Tác phẩm nghệ thuật"
                    
                    add_artwork(selected_emotion, canvas_data, title)
                    
                    # Hiệu ứng ăn mừng
                    st.markdown('<div class="celebration">🎉 🌟 ✨ Tuyệt vời! ✨ 🌟 🎉</div>', 
                              unsafe_allow_html=True)
                    st.success(f"Đã lưu tác phẩm '{title}' với cảm xúc {selected_emotion}!")
                    st.balloons()
                    
                    # Thông điệp khuyến khích
                    emotion_desc = st.session_state.get("emotion_description", "")
                    celebration_msg = f"Bạn đã hoàn thành một tác phẩm tuyệt vời"
                    if emotion_desc:
                        celebration_msg += f" thể hiện cảm xúc {emotion_desc}"
                    celebration_msg += "! Mỗi nét vẽ đều có ý nghĩa và giá trị riêng. Hãy tiếp tục sáng tạo nhé! 🎨✨"
                    
                    st.info(celebration_msg)
                    
                except Exception as e:
                    st.error(f"Lỗi khi lưu tác phẩm: {e}")
            else:
                st.warning("Hãy vẽ gì đó trước khi lưu nhé!")

# --- TIMELINE HIỂN THỊ CÁC TÁC PHẨM ĐÃ LƯU ---
st.write("---")
st.markdown("### 📚 Bộ sưu tập tranh cảm xúc của bạn")

# Tabs cho các chế độ xem khác nhau
tab1, tab2 = st.tabs(["📅 Theo ngày", "😊 Theo cảm xúc"])

with tab1:
    st.markdown("Xem lại hành trình cảm xúc qua tranh vẽ theo từng ngày:")
    artworks_by_date = get_artworks_by_date()
    
    if not artworks_by_date:
        st.info("Bạn chưa có tác phẩm nào. Hãy vẽ tác phẩm đầu tiên của bạn! 🎨")
    else:
        for date, artworks in artworks_by_date.items():
            with st.expander(f"📅 {date} ({len(artworks)} tác phẩm)"):
                for artwork in artworks:
                    st.markdown(f"""
                    <div class="timeline-item">
                        <strong>{artwork['emotion_emoji']} {artwork['title']}</strong><br>
                        <small>⏰ {artwork['timestamp']}</small>
                    </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown("Xem tác phẩm được nhóm theo cảm xúc:")
    
    # Hiển thị theo từng loại cảm xúc
    all_artworks = get_artworks_by_date()
    emotion_groups = {}
    
    for date, artworks in all_artworks.items():
        for artwork in artworks:
            emotion = artwork['emotion_emoji']
            if emotion not in emotion_groups:
                emotion_groups[emotion] = []
            emotion_groups[emotion].append(artwork)
    
    if not emotion_groups:
        st.info("Bạn chưa có tác phẩm nào. Hãy thể hiện cảm xúc qua tranh vẽ! 😊")
    else:
        for emotion, artworks in emotion_groups.items():
            emotion_name = EMOTIONS.get(emotion, "Cảm xúc khác")
            with st.expander(f"{emotion} {emotion_name} ({len(artworks)} tác phẩm)"):
                for artwork in artworks:
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.write(f"🎨 **{artwork['title']}**")
                        st.caption(f"📅 {artwork['timestamp']}")
                    with col2:
                        if st.button("👁️ Xem", key=f"view_{artwork['id']}"):
                            st.info("Tính năng xem lại tranh sẽ được cập nhật sớm!")

# Kết thúc container chính
st.markdown('</div>', unsafe_allow_html=True)

# --- THÔNG BÁO HƯỚNG DẪN CÀI ĐẶT (GIỮ NGUYÊN) ---
with st.expander("Gặp lỗi khi chạy trang này?"):
    st.info(
        """
        **Lưu ý:** Lần đầu sử dụng, bạn cần cài đặt thư viện cho tính năng này.
        Mở Terminal hoặc Command Prompt và chạy lệnh sau:
        ```bash
        pip install streamlit-drawable-canvas gtts
        ```
        Sau đó, hãy làm mới lại trang web.
        """
    )
