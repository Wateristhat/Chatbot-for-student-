import streamlit as st
import sys
import os
import base64
import io
from datetime import datetime
import tempfile
from gtts import gTTS
from io import BytesIO
# Add parent directory to path to find database module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
import html
import time
import random

# --- DANH SÁCH GỢI Ý BIẾT ƠN LUÂN PHIÊN ---
GRATITUDE_SUGGESTIONS = [
    "Hôm nay bạn đã nụ cười với ai? Điều gì khiến bạn cảm thấy vui vẻ?",
    "Có món ăn nào ngon khiến bạn nhớ mãi không? Kể cho mình nghe nhé!",
    "Bạn đã học được điều gì mới mẻ hôm nay? Dù là điều nhỏ nhất!",
    "Ai là người đã giúp đỡ bạn gần đây? Bạn biết ơn họ điều gì?",
    "Thiên nhiên có gì đẹp khiến bạn thích thú? Trời xanh, cây lá, hay tiếng chim hót?",
    "Bạn đã làm được việc gì khiến bản thân tự hào? Dù nhỏ nhất cũng được!",
    "Có khoảnh khắc nào hôm nay khiến bạn cảm thấy bình yên và hạnh phúc?",
    "Điều gì trong ngôi nhà của bạn khiến bạn cảm thấy ấm áp và an toàn?"
]

# --- VIRTUAL ASSISTANT MESSAGES ---
ASSISTANT_MESSAGES = [
    "Chào bạn! Mình là Bee - bạn đồng hành nhỏ của bạn! 🐝✨",
    "Hôm nay bạn có muốn chia sẻ điều gì đặc biệt không? 💫",
    "Mỗi điều biết ơn nhỏ đều là kho báu quý giá lắm! 💎",
    "Bạn làm rất tốt khi ghi lại những khoảnh khắc đẹp! 🌟",
    "Cảm ơn bạn đã tin tương và chia sẻ với mình! 🤗"
]

# Thêm thông điệp đặc biệt khi người dùng gửi lời biết ơn
GRATITUDE_RESPONSES = [
    "Thật tuyệt vời! Lời biết ơn của bạn đã được thêm vào lọ! 🌟",
    "Cảm ơn bạn đã chia sẻ! Điều này sẽ làm sáng cả ngày của bạn! ✨", 
    "Tuyệt quá! Bạn vừa tạo ra một kỷ niệm đẹp! 💝",
    "Mình cảm thấy ấm lòng khi đọc lời biết ơn của bạn! 🤗",
    "Bạn đã làm cho thế giới này tích cực hơn một chút! 🦋"
]

# Danh sách avatar để người dùng lựa chọn
AVATAR_OPTIONS = ["🐝", "🦋", "🌟", "💫", "🌸", "🦄", "🧚‍♀️", "🌻"]
AVATAR_NAMES = ["Ong Bee", "Bướm xinh", "Sao sáng", "Ánh sáng", "Hoa đào", "Kỳ lân", "Tiên nhỏ", "Hoa hướng dương"]

ENCOURAGING_MESSAGES = [
    {
        "avatar": "🌸",
        "message": "Thật tuyệt vời khi bạn dành thời gian để cảm ơn! Mỗi lời biết ơn là một hạt giống hạnh phúc được gieo vào trái tim bạn."
    },
    {
        "avatar": "🌟", 
        "message": "Hãy nhớ rằng, những điều nhỏ bé nhất cũng có thể mang lại niềm vui lớn. Bạn đã làm rất tốt rồi!"
    },
    {
        "avatar": "💖",
        "message": "Mỗi khi bạn viết lời biết ơn, bạn đang nuôi dưỡng một tâm hồn tích cực. Điều này thật đáng quý!"
    },
    {
        "avatar": "🦋",
        "message": "Biết ơn giống như ánh nắng ấm áp, nó không chỉ sưởi ấm trái tim bạn mà còn lan tỏa đến những người xung quanh."
    },
    {
        "avatar": "🌈",
        "message": "Bạn có biết không? Khi chúng ta biết ơn, não bộ sẽ tiết ra những hormone hạnh phúc. Bạn đang chăm sóc bản thân thật tốt!"
    },
    {
        "avatar": "🌺",
        "message": "Mỗi lời cảm ơn bạn viết ra đều là một món quà bạn tặng cho chính mình. Hãy tiếp tục nuôi dưỡng lòng biết ơn nhé!"
    },
    {
        "avatar": "✨",
        "message": "Đôi khi những điều đơn giản nhất lại mang đến hạnh phúc lớn nhất. Bạn đã nhận ra điều này rồi đấy!"
    },
    {
        "avatar": "🍀",
        "message": "Lòng biết ơn là chìa khóa mở ra cánh cửa hạnh phúc. Bạn đang trên đúng con đường rồi!"
    }
]

def get_random_encouragement():
    """Lấy một thông điệp động viên ngẫu nhiên"""
    return random.choice(ENCOURAGING_MESSAGES)

# --- TEXT-TO-SPEECH FUNCTION ---
def create_audio_file(text):
    """Tạo file audio từ text sử dụng gTTS"""
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Lỗi tạo file âm thanh: {e}")
        return None

# --- KHỞI TẠO SESSION STATE ---
if 'selected_emotion' not in st.session_state:
    st.session_state.selected_emotion = None
if 'suggestion_index' not in st.session_state:
    st.session_state.suggestion_index = random.randint(0, 4)
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = "🐝"  # Avatar mặc định
if 'current_assistant_message' not in st.session_state:
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
if 'show_gratitude_response' not in st.session_state:
    st.session_state.show_gratitude_response = False

# --- CSS STYLING CHO GIAO DIỆN DỄ NHÌN ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');

/* Global font setting */
html, body, [class*="css"], div, span, input, textarea, button {
    font-family: 'Comic Neue', Arial, sans-serif !important;
}

.main-title {
    font-family: 'Comic Neue', Arial, sans-serif;
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(45deg, #FFD700, #FFA500, #FF69B4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
}
.assistant-box {
    background: linear-gradient(135deg, #FFE4E1, #F0F8FF);
    border: 3px solid #FFB6C1;
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(255, 182, 193, 0.3);
    animation: gentle-pulse 3s ease-in-out infinite;
}
@keyframes gentle-pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.02); }
}
.assistant-avatar {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 0.5rem;
    animation: bounce 2s ease-in-out infinite;
}
@keyframes bounce {
    0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-10px); }
    60% { transform: translateY(-5px); }
}
.assistant-message {
    font-family: 'Comic Neue', Arial, sans-serif;
    font-size: 1.3rem;
    text-align: center;
    color: #4169E1;
    font-weight: 700;
    line-height: 1.4;
}
.emotion-button {
    font-size: 3rem !important;
    background: linear-gradient(45deg, #FFE4E1, #F0F8FF) !important;
    border: 3px solid #DDA0DD !important;
    border-radius: 50% !important;
    width: 80px !important;
    height: 80px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0.5rem !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}
.emotion-button:hover {
    transform: scale(1.1) !important;
    box-shadow: 0 4px 20px rgba(221, 160, 221, 0.4) !important;
}
.emotion-selected {
    border: 4px solid #FF1493 !important;
    background: linear-gradient(45deg, #FFB6C1, #FFC0CB) !important;
    transform: scale(1.1) !important;
    box-shadow: 0 4px 20px rgba(255, 20, 147, 0.5) !important;
}
.suggestion-box {
    background: linear-gradient(135deg, #E6E6FA, #F5F5DC);
    border: 2px solid #9370DB;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    font-family: 'Comic Neue', Arial, sans-serif;
    font-size: 1.2rem;
    color: #4B0082;
    text-align: center;
    box-shadow: 0 3px 10px rgba(147, 112, 219, 0.2);
}
.gratitude-input {
    font-family: 'Comic Neue', Arial, sans-serif;
    font-size: 1.1rem;
    border: 3px solid #DDA0DD;
    border-radius: 15px;
    padding: 1rem;
}
.timeline-item {
    background: linear-gradient(135deg, #FFF8DC, #FFFACD);
    border-left: 6px solid #FFD700;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
    transition: all 0.3s ease;
}
.timeline-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
}
.timeline-content {
    font-family: 'Comic Neue', Arial, sans-serif;
    font-size: 1.2rem;
    color: #8B4513;
    margin-bottom: 0.8rem;
    line-height: 1.5;
}
.timeline-date {
    font-size: 1rem;
    color: #CD853F;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Comic Neue', Arial, sans-serif;
}
.success-animation {
    animation: rainbow 2s ease-in-out;
}
@keyframes rainbow {
    0% { background: #ff0000; }
    16.66% { background: #ff8000; }
    33.33% { background: #ffff00; }
    50% { background: #80ff00; }
    66.66% { background: #00ffff; }
    83.33% { background: #8000ff; }
    100% { background: #ff0080; }
}

.note-card {
    background: linear-gradient(135deg, #FFF8DC, #FFFACD);
    border-left: 6px solid #FFD700;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(255, 215, 0, 0.2);
    font-family: 'Comic Neue', Arial, sans-serif;
    transition: all 0.3s ease;
}

.note-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255, 215, 0, 0.3);
}

.note-actions {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
    justify-content: flex-end;
    flex-wrap: wrap;
}

.sticker-success {
    font-size: 2rem;
    text-align: center;
    animation: bounce 1s ease-in-out;
}
</style>
""", unsafe_allow_html=True)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🍯 Lọ Biết Ơn",
    page_icon="🍯",
    layout="centered"
)

# --- HIỂN THỊ TIÊU ĐỀ CHÍNH ---
st.markdown('<h1 class="main-title">🍯 Lọ Biết Ơn Của Bạn</h1>', unsafe_allow_html=True)

# --- NÚT QUAY VỀ TRANG CHỦ ---
st.markdown("[⬅️ Về trang chủ](../0_💖_Trang_chủ.py)", unsafe_allow_html=True)

# --- TRỢ LÝ ẢO ĐỘNG VIÊN ---
def show_virtual_assistant():
    """Hiển thị trợ lý ảo với thông điệp động viên."""
    encouragement = get_random_encouragement()
    
    st.markdown(f"""
    <div class="assistant-box">
        <div class="assistant-avatar">{encouragement['avatar']}</div>
        <div class="assistant-message">{encouragement['message']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Nút đổi thông điệp và TTS
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Thông điệp mới", key="new_encouragement"):
            st.rerun()
    with col2:
        create_tts_button(encouragement['message'], "encouragement")

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    """Tạo nút text-to-speech cho văn bản."""
    if st.button(button_text, key=f"tts_{key_suffix}", help="Nhấn để nghe"):
        try:
            with st.spinner("Đang tạo âm thanh..."):
                tts = gTTS(text=text, lang='vi', slow=False)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes.read(), format="audio/mp3")
                st.success("🎵 Âm thanh đã sẵn sàng!")
        except Exception as e:
            st.info("🔇 Chức năng đọc to tạm thời không khả dụng. Nội dung: " + text[:100] + "...")

# Hiển thị trợ lý ảo
show_virtual_assistant()

# --- FORM THÊM GHI CHÚ BIẾT ƠN MỚI ---
st.markdown("### ✨ Chia sẻ điều bạn biết ơn hôm nay")

# Hiển thị gợi ý ngẫu nhiên
current_suggestion = GRATITUDE_SUGGESTIONS[st.session_state.suggestion_index]
st.markdown(f'''
<div class="suggestion-box">
    💡 <strong>Gợi ý:</strong> {current_suggestion}
</div>
''', unsafe_allow_html=True)

# Nút đổi gợi ý
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("🔄 Gợi ý khác", key="new_suggestion"):
        st.session_state.suggestion_index = random.randint(0, len(GRATITUDE_SUGGESTIONS)-1)
        st.rerun()

# Chọn cảm xúc
st.markdown("**🌈 Bạn cảm thấy thế nào?**")
emotion_options = ["😊", "😍", "🥰", "😌", "🤗", "😇", "✨", "💫"]
emotion_names = ["Vui vẻ", "Yêu thích", "Hạnh phúc", "Bình yên", "Ấm áp", "Thuần khiết", "Rạng ngời", "Kỳ diệu"]

# Hiển thị các nút cảm xúc
cols = st.columns(4)
for i, (emoji, name) in enumerate(zip(emotion_options, emotion_names)):
    with cols[i % 4]:
        button_style = "emotion-selected" if st.session_state.selected_emotion == emoji else "emotion-button"
        if st.button(emoji, key=f"emotion_{i}", help=name):
            st.session_state.selected_emotion = emoji

# Form nhập ghi chú
with st.form("gratitude_form", clear_on_submit=True):
    gratitude_text = st.text_area(
        "💝 Viết lời biết ơn của bạn:",
        placeholder="Hãy chia sẻ những điều khiến bạn cảm thấy biết ơn...",
        height=150,
        help="Hãy thật lòng và cụ thể về những gì bạn cảm thấy biết ơn."
    )
    
    col1, col2 = st.columns([2, 1])
    with col1:
        submit = st.form_submit_button("🌟 Thêm vào lọ biết ơn", use_container_width=True)
    with col2:
        clear_emotion = st.form_submit_button("🧹 Xóa cảm xúc")
    
    if clear_emotion:
        st.session_state.selected_emotion = None
        st.rerun()
    
    if submit and gratitude_text.strip():
        # Thêm vào database
        full_note = f"{st.session_state.selected_emotion or '💝'} {gratitude_text.strip()}"
        db.add_gratitude_note(full_note)
        
        # Hiển thị phản hồi thành công
        st.session_state.show_gratitude_response = True
        success_response = random.choice(GRATITUDE_RESPONSES)
        
        st.markdown(f"""
        <div class="sticker-success">
            {success_response}
        </div>
        """, unsafe_allow_html=True)
        
        # Hiển thị sticker thành công
        st.balloons()
        time.sleep(2)
        st.rerun()
    elif submit:
        st.warning("💡 Hãy viết gì đó trước khi thêm vào lọ biết ơn nhé!")

# --- HIỂN THỊ TIMELINE CÁC GHI CHÚ ---
st.markdown("---")
st.markdown("### 📖 Timeline Lọ Biết Ơn")

# Lấy tất cả ghi chú từ database
notes = db.get_gratitude_notes()

if notes:
    st.markdown(f"*Tổng cộng: {len(notes)} ghi chú biết ơn* ✨")
    
    # Hiển thị từng ghi chú
    for note_id, content, timestamp in reversed(notes):  # Hiển thị mới nhất trước
        # Parse timestamp
        try:
            dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
            time_str = dt.strftime('%d/%m/%Y lúc %H:%M')
        except:
            time_str = timestamp
        
        st.markdown(f"""
        <div class="note-card">
            <div class="timeline-content">{content}</div>
            <div class="timeline-date">
                📅 {time_str}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Nút hành động cho mỗi ghi chú
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("❤️ Thích", key=f"like_{note_id}", help="Thích ghi chú này"):
                st.toast("💖 Bạn đã thích ghi chú này!")
        
        with col2:
            create_tts_button(content, f"note_{note_id}", "🔊 Đọc to")
        
        with col3:
            if st.button("📋 Sao chép", key=f"copy_{note_id}", help="Sao chép nội dung"):
                st.toast("📋 Đã sao chép vào clipboard!")
        
        with col4:
            if st.button("🗑️ Xóa", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                if st.session_state.get(f"confirm_delete_{note_id}", False):
                    db.delete_gratitude_note(note_id)
                    st.toast("🗑️ Đã xóa ghi chú!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.session_state[f"confirm_delete_{note_id}"] = True
                    st.toast("⚠️ Nhấn lại để xác nhận xóa!")
        
        st.markdown("---")
        
else:
    # Hiển thị khi chưa có ghi chú
    st.markdown("""
    <div class="suggestion-box">
        🍯 Lọ biết ơn của bạn còn trống! Hãy thêm điều đầu tiên bạn cảm thấy biết ơn hôm nay nhé.
        <br><br>
        💡 <em>Mẹo nhỏ: Những điều đơn giản nhất thường mang lại hạnh phúc lớn nhất!</em>
    </div>
    """, unsafe_allow_html=True)

# --- THỐNG KÊ VUI ---
if notes:
    st.markdown("---")
    st.markdown("### 📊 Thống kê vui")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🗒️ Tổng ghi chú", len(notes))
    with col2:
        # Đếm số ghi chú có emoji
        emoji_notes = sum(1 for _, content, _ in notes if any(c in content for c in "😊😍🥰😌🤗😇✨💫💝"))
        st.metric("😊 Ghi chú có cảm xúc", emoji_notes)
    with col3:
        # Tính số từ trung bình
        if notes:
            total_words = sum(len(content.split()) for _, content, _ in notes)
            avg_words = total_words / len(notes)
            st.metric("📝 Từ TB/ghi chú", f"{avg_words:.1f}")

# --- FOOTER ĐỘNG VIÊN ---
st.markdown("---")
footer_message = random.choice([
    "🌟 Mỗi ngày là một cơ hội mới để biết ơn!",
    "💝 Lòng biết ơn làm cho cuộc sống thêm ý nghĩa!",
    "🌈 Hạnh phúc bắt đầu từ việc trân trọng những gì ta đang có!",
    "✨ Cảm ơn bạn đã dành thời gian nuôi dưỡng lòng biết ơn!"
])

st.markdown(f"""
<div class="assistant-message" style="text-align: center; margin-top: 2rem;">
    {footer_message}
</div>
""", unsafe_allow_html=True)