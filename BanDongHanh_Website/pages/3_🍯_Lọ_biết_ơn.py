import streamlit as st
import database as db
import html
import time
import random
from gtts import gTTS
from io import BytesIO

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Lọ Biết Ơn", page_icon="🍯", layout="centered")

# --- TTS FUNCTIONALITY ---
@st.cache_data
def text_to_speech(text):
    """Tạo file âm thanh từ văn bản"""
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        # More user-friendly error handling
        if "Failed to connect" in str(e) or "Unknown" in str(e):
            st.info("🌐 Hiện tại không thể kết nối để tạo âm thanh. Vui lòng kiểm tra kết nối mạng và thử lại sau nhé!")
        else:
            st.warning(f"Không thể tạo âm thanh: {e}")
        return None

# --- VIRTUAL ASSISTANT MESSAGES ---
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

# --- CSS STYLING ---
st.markdown("""
<style>
    .virtual-assistant {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
        color: white;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .virtual-assistant:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
    }
    
    .assistant-avatar {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        display: block;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    .assistant-message {
        font-size: 1.1rem;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .gratitude-note {
        background: linear-gradient(135deg, #FFF8DC 0%, #F0E68C 100%);
        border-left: 5px solid #FFD700;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(255, 215, 0, 0.2);
        min-height: 60px;
        display: flex;
        align-items: center;
        transition: all 0.3s ease;
    }
    
    .gratitude-note:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(255, 215, 0, 0.3);
    }
    
    .gratitude-text {
        color: #333;
        margin: 0;
        font-size: 1.05rem;
        line-height: 1.5;
        flex-grow: 1;
    }
    
    .tts-button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        margin-top: 1rem;
        transition: all 0.3s ease;
    }
    
    .tts-button:hover {
        transform: scale(1.05);
    }
    
    .guidance-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #ff6b6b;
        box-shadow: 0 3px 12px rgba(168, 237, 234, 0.3);
    }
    
    .guidance-section h4 {
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .guidance-section p {
        color: #34495e;
        margin: 0.5rem 0;
        font-size: 1rem;
        line-height: 1.5;
    }
    
    /* Accessibility improvements */
    button:focus {
        outline: 2px solid #4facfe;
        outline-offset: 2px;
    }
    
    .gratitude-note:focus-within {
        outline: 2px solid #FFD700;
        outline-offset: 2px;
    }
</style>
""", unsafe_allow_html=True)

# --- GIAO DIỆN CHÍNH ---
st.title("🍯 Lọ Biết Ơn")

# *** SỬA LẠI ĐÚNG ĐƯỜNG DẪN ***
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

# --- VIRTUAL ASSISTANT SECTION ---
if 'current_encouragement' not in st.session_state:
    st.session_state.current_encouragement = get_random_encouragement()

encouragement = st.session_state.current_encouragement

st.markdown(f"""
<div class="virtual-assistant">
    <div class="assistant-avatar">{encouragement['avatar']}</div>
    <div class="assistant-message">{encouragement['message']}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🎲 Nhận lời động viên mới", help="Nhận một thông điệp động viên khác"):
        st.session_state.current_encouragement = get_random_encouragement()
        st.rerun()

with col2:
    if st.button("🔊 Đọc to", help="Nghe lời động viên"):
        with st.spinner("Đang tạo âm thanh..."):
            audio_data = text_to_speech(encouragement['message'])
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

# --- GUIDANCE SECTION ---
st.markdown("""
<div class="guidance-section">
    <h4>💡 Hướng dẫn sử dụng Lọ Biết Ơn</h4>
    <p>🌟 Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay</p>
    <p>💝 Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương</p>
    <p>🌈 Không cần hoàn hảo, chỉ cần chân thành từ trái tim</p>
</div>
""", unsafe_allow_html=True)

# TTS for guidance
col_guide1, col_guide2 = st.columns([3, 1])
with col_guide2:
    if st.button("🔊 Đọc hướng dẫn", help="Nghe hướng dẫn sử dụng", key="guidance_tts"):
        guidance_text = ("Hướng dẫn sử dụng Lọ Biết Ơn. "
                        "Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay. "
                        "Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương. "
                        "Không cần hoàn hảo, chỉ cần chân thành từ trái tim.")
        with st.spinner("Đang tạo âm thanh..."):
            audio_data = text_to_speech(guidance_text)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")

st.markdown("Hôm nay có điều gì khiến bạn mỉm cười không?")

# Khu vực nhập liệu
note_text = st.text_area(
    "Viết điều bạn biết ơn vào đây...", 
    height=100, 
    key="gratitude_input",
    placeholder="Ví dụ: Hôm nay trời đẹp, mình được ăn món ngon..."
)

if st.button("Thêm vào lọ biết ơn", type="primary", use_container_width=True):
    if note_text:
        db.add_gratitude_note(note_text)  # Không dùng user_id nữa
        st.success("Đã thêm một hạt mầm biết ơn vào lọ! 🌱")
        st.balloons()
        time.sleep(1)
        st.rerun()
    else:
        st.warning("Bạn hãy viết gì đó nhé!")

st.write("---")

# --- HIỂN THỊ CÁC GHI CHÚ ĐÃ CÓ ---
gratitude_notes = db.get_gratitude_notes()  # Không truyền user_id

if gratitude_notes:
    st.subheader("Những điều bạn biết ơn:")
    
    # Đảo ngược danh sách để hiển thị ghi chú mới nhất lên đầu
    gratitude_notes.reverse()
    
    for note_id, note_content in gratitude_notes:
        col1, col2 = st.columns([10, 1])
        
        with col1:
            safe_content = html.escape(note_content)
            st.markdown(
                f'<div class="gratitude-note">'
                f'<p class="gratitude-text">{safe_content}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            
            # TTS button for each note positioned below the content
            col_tts, col_spacer = st.columns([1, 3])
            with col_tts:
                if st.button(f"🔊 Đọc to", key=f"tts_{note_id}", help="Nghe ghi chú này"):
                    with st.spinner("Đang tạo âm thanh..."):
                        audio_data = text_to_speech(note_content)
                        if audio_data:
                            st.audio(audio_data, format="audio/mp3")
        
        with col2:
            if st.button("🗑️", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                db.delete_gratitude_note(note_id)
                st.toast("Đã xóa ghi chú!")
                time.sleep(1)
                st.rerun()

else:
    st.info("Chiếc lọ của bạn đang chờ những điều biết ơn đầu tiên. ❤️")
