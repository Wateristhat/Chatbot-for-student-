import streamlit as st
import sys
import os
import base64
import io
from datetime import datetime
import tempfile
from gtts import gTTS
from io import BytesIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db
import html
import time
import random

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

ASSISTANT_MESSAGES = [
    "Chào bạn! Mình là Bee - bạn đồng hành nhỏ của bạn! 🐝✨",
    "Hôm nay bạn có muốn chia sẻ điều gì đặc biệt không? 💫",
    "Mỗi điều biết ơn nhỏ đều là kho báu quý giá lắm! 💎",
    "Bạn làm rất tốt khi ghi lại những khoảnh khắc đẹp! 🌟",
    "Cảm ơn bạn đã tin tương và chia sẻ với mình! 🤗"
]

GRATITUDE_RESPONSES = [
    "Thật tuyệt vời! Lời biết ơn của bạn đã được thêm vào lọ! 🌟",
    "Cảm ơn bạn đã chia sẻ! Điều này sẽ làm sáng cả ngày của bạn! ✨", 
    "Tuyệt quá! Bạn vừa tạo ra một kỷ niệm đẹp! 💝",
    "Mình cảm thấy ấm lòng khi đọc lời biết ơn của bạn! 🤗",
    "Bạn đã làm cho thế giới này tích cực hơn một chút! 🦋"
]

AVATAR_OPTIONS = ["🐝", "🦋", "🌟", "💫", "🌸", "🦄", "🧚‍♀️", "🌻"]
AVATAR_NAMES = ["Ong Bee", "Bướm xinh", "Sao sáng", "Ánh sáng", "Hoa đào", "Kỳ lân", "Tiên nhỏ", "Hoa hướng dương"]

ENCOURAGING_MESSAGES = [
    {"avatar": "🌸", "message": "Thật tuyệt vời khi bạn dành thời gian để cảm ơn! Mỗi lời biết ơn là một hạt giống hạnh phúc được gieo vào trái tim bạn."},
    {"avatar": "🌟", "message": "Hãy nhớ rằng, những điều nhỏ bé nhất cũng có thể mang lại niềm vui lớn. Bạn đã làm rất tốt rồi!"},
    {"avatar": "💖","message": "Mỗi khi bạn viết lời biết ơn, bạn đang nuôi dưỡng một tâm hồn tích cực. Điều này thật đáng quý!"},
    {"avatar": "🦋","message": "Biết ơn giống như ánh nắng ấm áp, nó không chỉ sưởi ấm trái tim bạn mà còn lan tỏa đến những người xung quanh."},
    {"avatar": "🌈","message": "Bạn có biết không? Khi chúng ta biết ơn, não bộ sẽ tiết ra những hormone hạnh phúc. Bạn đang chăm sóc bản thân thật tốt!"},
    {"avatar": "🌺","message": "Mỗi lời cảm ơn bạn viết ra đều là một món quà bạn tặng cho chính mình. Hãy tiếp tục nuôi dưỡng lòng biết ơn nhé!"},
    {"avatar": "✨","message": "Đôi khi những điều đơn giản nhất lại mang đến hạnh phúc lớn nhất. Bạn đã nhận ra điều này rồi đấy!"},
    {"avatar": "🍀","message": "Lòng biết ơn là chìa khóa mở ra cánh cửa hạnh phúc. Bạn đang trên đúng con đường rồi!"}
]

def get_random_encouragement():
    return random.choice(ENCOURAGING_MESSAGES)

def get_error_message(error_code):
    """Trả về thông báo lỗi thân thiện cho học sinh"""
    error_messages = {
        "empty_text": "💭 Chưa có nội dung để đọc. Hãy thử lại khi có văn bản!",
        "text_too_short": "💭 Nội dung quá ngắn để tạo âm thanh. Hãy thêm vài từ nữa nhé!",
        "network_error": "🌐 Không thể kết nối để tạo âm thanh. Hãy kiểm tra kết nối mạng và thử lại nhé! 💫",
        "timeout_error": "⏰ Kết nối hơi chậm. Hãy thử lại sau vài giây nữa nhé! ⭐",
        "access_blocked": "🚫 Tính năng âm thanh tạm thời không khả dụng. Hãy thử lại sau hoặc dùng trình duyệt khác! 🌟",
        "server_error": "🔧 Dịch vụ âm thanh đang bảo trì. Hãy thử lại sau 5-10 phút nhé! 🌈",
        "no_audio_generated": "🎵 Không thể tạo âm thanh lúc này. Hãy thử lại sau nhé!",
    }
    # Xử lý lỗi có prefix
    if error_code.startswith("unknown_error:"):
        return "🎵 Có lỗi nhỏ khi tạo âm thanh. Bạn có thể đọc nội dung ở trên hoặc thử lại sau nhé! ✨"
    return error_messages.get(error_code, "🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé! 💕")

def create_audio_file(text):
    """Tạo file âm thanh từ text với xử lý lỗi chi tiết và log developer"""
    if not text:
        print("🔍 TTS Debug: Text is None")
        return None, "empty_text"
    if not text.strip():
        print("🔍 TTS Debug: Text is empty after stripping")
        return None, "empty_text"
    cleaned_text = text.strip()
    if len(cleaned_text) < 3:
        print(f"🔍 TTS Debug: Text too short ({len(cleaned_text)} chars)")
        return None, "text_too_short"
    try:
        print(f"🔍 TTS Debug: Attempting to create TTS for text length {len(cleaned_text)}")
        tts = gTTS(text=cleaned_text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            print(f"🔍 TTS Debug: Saving to temporary file {tmp_file.name}")
            tts.save(tmp_file.name)
            if os.path.exists(tmp_file.name) and os.path.getsize(tmp_file.name) > 0:
                print(f"🔍 TTS Debug: Success! File size: {os.path.getsize(tmp_file.name)} bytes")
                return tmp_file.name, "success"
            else:
                print("🔍 TTS Debug: File created but empty or missing")
                return None, "no_audio_generated"
    except Exception as e:
        error_str = str(e).lower()
        print(f"🔍 TTS Debug: Exception - {type(e).__name__}: {e}")
        if "connection" in error_str or "network" in error_str or "failed to connect" in error_str:
            return None, "network_error"
        elif "timeout" in error_str:
            return None, "timeout_error"
        elif "forbidden" in error_str or "403" in error_str:
            return None, "access_blocked"
        elif "503" in error_str or "502" in error_str or "500" in error_str:
            return None, "server_error"
        else:
            return None, f"unknown_error: {str(e)}"

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🍯 Lọ Biết Ơn",
    page_icon="🍯",
    layout="centered"
)

# Khởi tạo session state
if 'suggestion_index' not in st.session_state:
    st.session_state.suggestion_index = random.randint(0, len(GRATITUDE_SUGGESTIONS) - 1)
if 'current_encouragement' not in st.session_state:
    st.session_state.current_encouragement = get_random_encouragement()

# --- CSS STYLES ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');

.main-title,
.assistant-message,
.suggestion-box,
.gratitude-input,
.timeline-content,
.timeline-date,
.footer-message,
.empty-state-message,
.empty-state-subtitle,
.timeline-count,
.guidance-section h4,
.guidance-section p {
    font-family: 'Comic Neue', Arial, sans-serif !important;
}

/* Tiêu đề chính */
.main-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #FF6B6B;
    text-align: center;
    margin: 2rem 0;
    text-shadow: 2px 2px 4px rgba(255,107,107,0.3);
    background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: pulse 2s ease-in-out infinite;
}

/* Hộp tin nhắn từ trợ lý */
.assistant-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 20px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    color: white;
    display: flex;
    align-items: center;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    position: relative;
    overflow: hidden;
}

.assistant-box::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { left: -100%; }
    100% { left: 100%; }
}

.assistant-avatar {
    font-size: 3rem;
    margin-right: 1rem;
    animation: avatar-bounce 2s ease-in-out infinite;
}

@keyframes avatar-bounce {
    0%, 100% { transform: translateY(0px) rotate(0deg); }
    50% { transform: translateY(-8px) rotate(5deg); }
}

.assistant-message {
    font-size: 1.4rem;
    font-weight: 600;
    line-height: 1.6;
    flex: 1;
}

/* Hộp gợi ý */
.suggestion-box {
    background: linear-gradient(135deg, #FFF6E1, #FFE4B5);
    border: 2px solid #FFD700;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1.5rem 0;
    font-size: 1.3rem;
    font-weight: 600;
    color: #B8860B;
    text-align: center;
    box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3);
    animation: soft-glow 2s ease-in-out infinite alternate;
}

@keyframes soft-glow {
    from { box-shadow: 0 5px 20px rgba(255, 215, 0, 0.3); }
    to { box-shadow: 0 8px 25px rgba(255, 215, 0, 0.5); }
}

/* Timeline items */
.timeline-item {
    background: linear-gradient(135deg, #E8F4FD, #C3E9FF);
    border: 2px solid #4facfe;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(79, 172, 254, 0.2);
    transition: all 0.3s ease;
    position: relative;
}

.timeline-item:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(79, 172, 254, 0.4);
    border-color: #FFD700;
}

.timeline-content {
    font-size: 1.3rem;
    font-weight: 600;
    color: #2c3e50;
    line-height: 1.6;
    margin-bottom: 1rem;
}

.timeline-date {
    font-size: 1rem;
    color: #7f8c8d;
    font-weight: 500;
    text-align: right;
}

.timeline-count {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e74c3c;
    background: linear-gradient(135deg, #FFE8E8, #FFD1DC);
    border: 2px solid #FF69B4;
    border-radius: 25px;
    padding: 1rem 2rem;
    display: inline-block;
}

/* Empty state */
.empty-state-message {
    font-size: 1.5rem;
    font-weight: 600;
    color: #34495e;
    margin-bottom: 0.5rem;
}

.empty-state-subtitle {
    font-size: 1.2rem;
    color: #7f8c8d;
    font-weight: 500;
}

/* Footer message */
.footer-message {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px;
    padding: 2rem;
    font-size: 1.2rem;
    font-weight: 600;
    line-height: 1.6;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    margin: 2rem 0;
}

/* Guidance section */
.guidance-section {
    background: linear-gradient(135deg, #F0F8FF, #E6E6FA);
    border: 2px solid #9370DB;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 3px 10px rgba(147, 112, 219, 0.2);
}

.guidance-section h4 {
    font-size: 1.4rem;
    font-weight: 700;
    color: #4B0082;
    margin-bottom: 1rem;
    text-align: center;
}

.guidance-section p {
    font-size: 1.2rem;
    font-weight: 600;
    color: #5D4E75;
    margin: 0.5rem 0;
    line-height: 1.6;
}

/* Animations */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.8; }
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

/* Focus accessibility */
.timeline-item:focus {
    outline: 2px solid #4facfe;
    outline-offset: 2px;
}
.timeline-item:focus-within {
    outline: 2px solid #FFD700;
    outline-offset: 2px;
}

/* Responsive design */
@media (max-width: 768px) {
    .main-title {
        font-size: 2.2rem;
    }
    .assistant-message {
        font-size: 1.2rem;
    }
    .suggestion-box {
        font-size: 1.1rem;
        padding: 1rem;
    }
    .timeline-content {
        font-size: 1.1rem;
    }
}
</style>
""", unsafe_allow_html=True)

# --- MAIN UI ---
st.markdown('<h1 class="main-title">🍯 Lọ Biết Ơn</h1>', unsafe_allow_html=True)

# Hiển thị thông điệp động viên
encouragement = st.session_state.current_encouragement
st.markdown(f"""<div class="assistant-box"><div class="assistant-avatar">{encouragement['avatar']}</div><div class="assistant-message">{encouragement['message']}</div></div>""", unsafe_allow_html=True)

# Nút động viên và TTS
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🎲 Nhận lời động viên mới", help="Nhận một thông điệp động viên khác"):
        st.session_state.current_encouragement = get_random_encouragement()
        st.rerun()
with col2:
    if st.button("🔊 Đọc to", help="Nghe lời động viên"):
        with st.spinner("Đang tạo âm thanh..."):
            audio_file, error_code = create_audio_file(encouragement['message'])
            if audio_file:
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)
                except Exception:
                    st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
            else:
                error_msg = get_error_message(error_code)
                st.info(error_msg)

# Hướng dẫn sử dụng
st.markdown("""
<div class="guidance-section">
    <h4>💡 Hướng dẫn sử dụng Lọ Biết Ơn</h4>
    <p>🌟 Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay</p>
    <p>💝 Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương</p>
    <p>🌈 Không cần hoàn hảo, chỉ cần chân thành từ trái tim</p>
</div>
""", unsafe_allow_html=True)

# Nút đọc hướng dẫn
col_guide1, col_guide2 = st.columns([3, 1])
with col_guide2:
    if st.button("🔊 Đọc hướng dẫn", help="Nghe hướng dẫn sử dụng", key="guidance_tts"):
        guidance_text = ("Hướng dẫn sử dụng Lọ Biết Ơn. "
                        "Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay. "
                        "Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương. "
                        "Không cần hoàn hảo, chỉ cần chân thành từ trái tim.")
        with st.spinner("Đang tạo âm thanh..."):
            audio_file, error_code = create_audio_file(guidance_text)
            if audio_file:
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)
                except Exception:
                    st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
            else:
                error_msg = get_error_message(error_code)
                st.info(error_msg)

# Hiển thị gợi ý
current_suggestion = GRATITUDE_SUGGESTIONS[st.session_state.suggestion_index]
st.markdown(f"""<div class="suggestion-box"><strong>💡 Gợi ý cho bạn:</strong><br>{current_suggestion}</div>""", unsafe_allow_html=True)

# Nút thay đổi gợi ý
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Gợi ý khác", use_container_width=True):
        st.session_state.suggestion_index = (st.session_state.suggestion_index + 1) % len(GRATITUDE_SUGGESTIONS)
        st.rerun()

# Form nhập ghi chú biết ơn
st.markdown("### ✍️ Viết điều bạn biết ơn:")
note_text = st.text_area(
    "",
    height=120,
    key="gratitude_input",
    placeholder="Hãy viết về điều làm bạn cảm thấy biết ơn... Mỗi từ đều có ý nghĩa! 💕",
    label_visibility="collapsed"
)

# Nút thêm vào lọ
if st.button("🌟 Thêm vào lọ biết ơn", type="primary", use_container_width=True):
    if note_text.strip():
        try:
            db.add_gratitude_note(note_text.strip())
            # Hiệu ứng thành công
            success_stickers = ["🎉", "⭐", "🌟", "✨", "💫", "🎊", "🦋", "🌈", "🎁", "💝"]
            selected_stickers = random.sample(success_stickers, 3)
            st.markdown(f"""<div style="text-align: center; font-size: 3rem; margin: 1rem 0; animation: bounce 1s ease-in-out;">{''.join(selected_stickers)}</div>""", unsafe_allow_html=True)
            st.success("🌱 Đã thêm một hạt mầm biết ơn vào lọ! Cảm ơn bạn đã chia sẻ!")
            st.balloons()
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error("🙈 Có lỗi xảy ra khi lưu ghi chú. Vui lòng thử lại!")
    else:
        st.warning("💛 Bạn hãy viết gì đó để chia sẻ nhé! Mình đang chờ đây!")

st.write("---")

# Hiển thị Timeline
st.markdown("### 📖 Timeline - Những Kỷ Niệm Biết Ơn")

try:
    gratitude_notes = db.get_gratitude_notes()
    
    if gratitude_notes:
        st.markdown(f"<div class='timeline-count' style='text-align: center; margin-bottom: 1.5rem;'>Bạn đã có <strong>{len(gratitude_notes)}</strong> kỷ niệm đẹp! 💎</div>", unsafe_allow_html=True)
        
        # Hiển thị các ghi chú theo thứ tự mới nhất trước
        for note_id, note_content, timestamp in reversed(gratitude_notes):
            try:
                # Parse timestamp
                dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                formatted_date = dt.strftime("%d/%m/%Y lúc %H:%M")
                day_names = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
                day_name = day_names[dt.weekday()]
                full_date = f"{day_name}, {formatted_date}"
            except:
                full_date = timestamp
            
            # Container cho mỗi ghi chú
            with st.container():
                st.markdown(f"""
                <div class="timeline-item">
                    <div class="timeline-content">{html.escape(note_content)}</div>
                    <div class="timeline-date">📅 {full_date}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Các nút hành động
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    if st.button("🔊 Đọc to", key=f"tts_{note_id}", help="Nghe ghi chú này"):
                        with st.spinner("Đang tạo âm thanh..."):
                            audio_file, error_code = create_audio_file(note_content)
                            if audio_file:
                                try:
                                    with open(audio_file, 'rb') as f:
                                        audio_bytes = f.read()
                                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                                    os.unlink(audio_file)
                                except Exception:
                                    st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
                            else:
                                error_msg = get_error_message(error_code)
                                st.info(error_msg)
                with col2:
                    if st.button("💝 Thích", key=f"like_{note_id}", help="Tôi thích ghi chú này!"):
                        st.markdown("💕 Cảm ơn bạn đã thích kỷ niệm này!")
                with col3:
                    if st.button("🗑️", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                        try:
                            db.delete_gratitude_note(note_id)
                            st.success("🌸 Đã xóa ghi chú!")
                            time.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error("🙈 Có lỗi xảy ra khi xóa ghi chú. Vui lòng thử lại!")
    else:
        # Trạng thái rỗng - thân thiện và khuyến khích
        st.markdown("""
        <div style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🍯</div>
            <div class="empty-state-message">Chiếc lọ biết ơn của bạn đang chờ những điều tuyệt vời đầu tiên!</div>
            <div class="empty-state-subtitle" style="margin-top: 1rem;">Hãy bắt đầu bằng việc chia sẻ một điều nhỏ nhất mà bạn biết ơn hôm nay ❤️</div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error("🙈 Có lỗi khi tải dữ liệu. Hãy thử làm mới trang!")
    st.info("💡 **Gợi ý khắc phục**: Làm mới trang (F5) hoặc thông báo cho giáo viên nếu vấn đề tiếp tục.")

# Footer message
st.markdown("---")
st.markdown("""
<div class="footer-message" style="text-align: center; padding: 1rem;">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi ngày là một món quà, mỗi khoảnh khắc biết ơn là một viên ngọc quý. 
    Cảm ơn bạn đã chia sẻ những điều tuyệt vời trong cuộc sống! 🌟"
</div>
""", unsafe_allow_html=True)