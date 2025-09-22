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
    }
    
    # Xử lý lỗi có prefix
    if error_code.startswith("unknown_error:"):
        return "🎵 Có lỗi nhỏ khi tạo âm thanh. Bạn có thể đọc nội dung ở trên hoặc thử lại sau nhé! ✨"
    
    return error_messages.get(error_code, "🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé! 💕")

def create_audio_file(text):
    """Tạo file âm thanh với xử lý lỗi chi tiết"""
    # Kiểm tra text đầu vào
    if not text or not text.strip():
        return None, "empty_text"
    
    text = text.strip()
    if len(text) < 2:
        return None, "text_too_short"
    
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name, "success"
    except Exception as e:
        # Phân loại lỗi để đưa ra thông báo phù hợp
        error_str = str(e).lower()
        if "connection" in error_str or "network" in error_str or "failed to connect" in error_str:
            return None, "network_error"
        elif "timeout" in error_str:
            return None, "timeout_error"  
        elif "forbidden" in error_str or "403" in error_str:
            return None, "access_blocked"
        elif "503" in error_str or "502" in error_str or "500" in error_str:
            return None, "server_error"
        else:
            # Log chi tiết cho developer
            print(f"TTS Error: {e}")
            return None, f"unknown_error: {str(e)}"

if 'selected_emotion' not in st.session_state:
    st.session_state.selected_emotion = None
if 'suggestion_index' not in st.session_state:
    st.session_state.suggestion_index = random.randint(0, 4)
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = "🐝"
if 'current_assistant_message' not in st.session_state:
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
if 'show_gratitude_response' not in st.session_state:
    st.session_state.show_gratitude_response = False

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
.emotion-selection,
.timeline-count,
.guidance-section h4,
.guidance-section p {
    font-family: 'Comic Neue', Arial, sans-serif !important;
}
.main-title {
    font-size: 3rem;
    text-align: center;
    background: linear-gradient(45deg, #FFD700, #FFA500, #FF69B4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    font-weight: 700;
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
    font-size: 1.4rem;
    font-weight: 700;
    text-align: center;
    color: #4169E1;
    line-height: 1.5;
}
.suggestion-box {
    font-size: 1.2rem;
    color: #4B0082;
    background: linear-gradient(135deg, #E6E6FA, #F5F5DC);
    border: 2px solid #9370DB;
    border-radius: 15px;
    padding: 1.5rem;
    margin: 1rem 0;
    text-align: center;
    box-shadow: 0 3px 10px rgba(147, 112, 219, 0.2);
    line-height: 1.6;
}
.gratitude-input {
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
    font-size: 1.2rem;
    color: #8B4513;
    margin-bottom: 0.8rem;
    line-height: 1.6;
}
.timeline-date {
    font-size: 1.1rem;
    font-weight: 700;
    color: #CD853F;
    display: flex;
    align-items: center;
    gap: 0.5rem;
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
.stButton > button {
    font-size: 1.2rem;
    font-weight: 700;
    border-radius: 25px;
    border: 3px solid #32CD32;
    background: linear-gradient(45deg, #98FB98, #90EE90);
    color: #006400;
    padding: 0.8rem 2rem;
    transition: all 0.3s ease;
    font-family: 'Comic Neue', Arial, sans-serif !important;
}
.stButton > button:hover {
    background: linear-gradient(45deg, #90EE90, #7FFFD4);
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(50, 205, 50, 0.3);
}
button:focus {
    outline: 2px solid #4facfe;
    outline-offset: 2px;
}
.timeline-item:focus-within {
    outline: 2px solid #FFD700;
    outline-offset: 2px;
}
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
    color: #4B0082;
    line-height: 1.6;
    margin-bottom: 0.8rem;
}
.footer-message {
    font-size: 1.2rem;
    font-weight: 700;
    color: #8B4513;
    line-height: 1.6;
}
.empty-state-message {
    font-size: 1.4rem;
    font-weight: 700;
    color: #9370DB;
    line-height: 1.6;
}
.empty-state-subtitle {
    font-size: 1.1rem;
    font-weight: 600;
    color: #DDA0DD;
    line-height: 1.5;
}
.emotion-selection {
    font-size: 1.4rem;
    font-weight: 700;
    color: #FF69B4;
    line-height: 1.5;
}
.timeline-count {
    font-size: 1.2rem;
    font-weight: 700;
    color: #8B4513;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-title">🍯 Lọ Biết Ơn Của Bạn</h1>', unsafe_allow_html=True)
st.markdown("⬅️ [Quay về Trang chủ](../0_💖_Trang_chủ.py)")

current_message = random.choice(ASSISTANT_MESSAGES)
st.markdown(f"""<div class="assistant-box"><div class="assistant-avatar">🐝</div><div class="assistant-message">{current_message}</div></div>""", unsafe_allow_html=True)

st.markdown("### 💝 Hôm nay bạn cảm thấy thế nào?")
emotion_cols = st.columns(5)
emotions = ["😊", "😃", "🥰", "😌", "🤗"]
emotion_names = ["Vui vẻ", "Hạnh phúc", "Yêu thương", "Bình yên", "Ấm áp"]

for i, (col, emotion, name) in enumerate(zip(emotion_cols, emotions, emotion_names)):
    with col:
        if st.button(emotion, key=f"emotion_{i}", help=name):
            st.session_state.selected_emotion = emotion
            st.rerun()

if st.session_state.selected_emotion:
    st.markdown(f"<div class='emotion-selection' style='text-align: center; margin: 1rem 0;'>Bạn đang cảm thấy {st.session_state.selected_emotion} - Thật tuyệt vời!</div>", unsafe_allow_html=True)

st.write("---")

if 'current_encouragement' not in st.session_state:
    st.session_state.current_encouragement = get_random_encouragement()
encouragement = st.session_state.current_encouragement
st.markdown(f"""<div class="assistant-box"><div class="assistant-avatar">{encouragement['avatar']}</div><div class="assistant-message">{encouragement['message']}</div></div>""", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🎲 Nhận lời động viên mới", help="Nhận một thông điệp động viên khác"):
        st.session_state.current_encouragement = get_random_encouragement()
        st.rerun()
with col2:
    if st.button("🔊 Đọc to", help="Nghe lời động viên"):
        with st.spinner("Đang tạo âm thanh..."):
            audio_file, result_code = create_audio_file(encouragement['message'])
            if audio_file and result_code == "success":
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)
                except Exception as e:
                    print(f"Audio playback error: {e}")  # Log cho developer
                    st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
            else:
                # Hiển thị thông báo lỗi thân thiện
                error_msg = get_error_message(result_code)
                st.info(error_msg)

st.markdown("""
<div class="suggestion-box">
    <strong>💡 Gợi ý cho bạn:</strong><br>
    Hôm nay có điều gì khiến bạn mỉm cười không?
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="guidance-section">
    <h4>💡 Hướng dẫn sử dụng Lọ Biết Ơn</h4>
    <p>🌟 Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay</p>
    <p>💝 Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương</p>
    <p>🌈 Không cần hoàn hảo, chỉ cần chân thành từ trái tim</p>
</div>
""", unsafe_allow_html=True)

col_guide1, col_guide2 = st.columns([3, 1])
with col_guide2:
    if st.button("🔊 Đọc hướng dẫn", help="Nghe hướng dẫn sử dụng", key="guidance_tts"):
        guidance_text = ("Hướng dẫn sử dụng Lọ Biết Ơn. "
                        "Hãy viết về những điều nhỏ bé mà bạn biết ơn hôm nay. "
                        "Có thể là nụ cười của bạn bè, bữa ăn ngon, hay cảm giác được yêu thương. "
                        "Không cần hoàn hảo, chỉ cần chân thành từ trái tim.")
        with st.spinner("Đang tạo âm thanh..."):
            audio_file, result_code = create_audio_file(guidance_text)
            if audio_file and result_code == "success":
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)
                except Exception as e:
                    print(f"Audio playback error: {e}")  # Log cho developer
                    st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
            else:
                # Hiển thị thông báo lỗi thân thiện
                error_msg = get_error_message(result_code)
                st.info(error_msg)

current_suggestion = GRATITUDE_SUGGESTIONS[st.session_state.suggestion_index]
st.markdown(f"""<div class="suggestion-box"><strong>💡 Gợi ý cho bạn:</strong><br>{current_suggestion}</div>""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🔄 Gợi ý khác", use_container_width=True):
        st.session_state.suggestion_index = (st.session_state.suggestion_index + 1) % len(GRATITUDE_SUGGESTIONS)
        st.rerun()

st.markdown("### ✍️ Viết điều bạn biết ơn:")
note_text = st.text_area(
    "",
    height=120,
    key="gratitude_input",
    placeholder="Hãy viết về điều làm bạn cảm thấy biết ơn... Mỗi từ đều có ý nghĩa! 💕",
    label_visibility="collapsed"
)

if st.button("🌟 Thêm vào lọ biết ơn", type="primary", use_container_width=True):
    if note_text:
        db.add_gratitude_note(note_text)
        success_stickers = ["🎉", "⭐", "🌟", "✨", "💫", "🎊", "🦋", "🌈", "🎁", "💝"]
        selected_stickers = random.sample(success_stickers, 3)
        st.markdown(f"""<div style="text-align: center; font-size: 3rem; margin: 1rem 0; animation: bounce 1s ease-in-out;">{''.join(selected_stickers)}</div>""", unsafe_allow_html=True)
        st.success("🌱 Đã thêm một hạt mầm biết ơn vào lọ! Cảm ơn bạn đã chia sẻ!")
        st.balloons()
        time.sleep(2)
        st.rerun()
    else:
        st.warning("💛 Bạn hãy viết gì đó để chia sẻ nhé! Mình đang chờ đây!")

st.write("---")

st.markdown("### 📖 Timeline - Những Kỷ Niệm Biết Ơn")
gratitude_notes = db.get_gratitude_notes()

if gratitude_notes:
    st.markdown(f"<div class='timeline-count' style='text-align: center; margin-bottom: 1.5rem;'>Bạn đã có <strong>{len(gratitude_notes)}</strong> kỷ niệm đẹp! 💎</div>", unsafe_allow_html=True)
    for note_id, note_content, timestamp in gratitude_notes:
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%d/%m/%Y lúc %H:%M")
            day_name = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][dt.weekday()]
            full_date = f"{day_name}, {formatted_date}"
        except:
            full_date = timestamp
        with st.container():
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-content">{html.escape(note_content)}</div>
                <div class="timeline-date">📅 {full_date}</div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button("🔊 Đọc to", key=f"tts_{note_id}", help="Nghe ghi chú này"):
                    audio_file, result_code = create_audio_file(note_content)
                    if audio_file and result_code == "success":
                        try:
                            with open(audio_file, 'rb') as f:
                                audio_bytes = f.read()
                            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                            os.unlink(audio_file)
                        except Exception as e:
                            print(f"Audio playback error: {e}")  # Log cho developer
                            st.info("🎵 Hiện tại không thể phát âm thanh. Bạn có thể đọc nội dung ở trên nhé!")
                    else:
                        # Hiển thị thông báo lỗi thân thiện
                        error_msg = get_error_message(result_code)
                        st.info(error_msg)
            with col2:
                if st.button("💝 Thích", key=f"like_{note_id}", help="Tôi thích ghi chú này!"):
                    st.markdown("💕 Cảm ơn bạn đã thích kỷ niệm này!")
            with col3:
                if st.button("🗑️", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                    db.delete_gratitude_note(note_id)
                    st.success("🌸 Đã xóa ghi chú!")
                    time.sleep(1)
                    st.rerun()
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🍯</div>
        <div class="empty-state-message">Chiếc lọ biết ơn của bạn đang chờ những điều tuyệt vời đầu tiên!</div>
        <div class="empty-state-subtitle" style="margin-top: 1rem;">Hãy bắt đầu bằng việc chia sẻ một điều nhỏ nhất mà bạn biết ơn hôm nay ❤️</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
<div class="footer-message" style="text-align: center; padding: 1rem;">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi ngày là một món quà, mỗi khoảnh khắc biết ơn là một viên ngọc quý. 
    Cảm ơn bạn đã chia sẻ những điều tuyệt vời trong cuộc sống! 🌟"
</div>
""", unsafe_allow_html=True)