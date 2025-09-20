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