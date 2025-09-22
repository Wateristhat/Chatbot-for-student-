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

# ... Toàn bộ phần code UI phía dưới giữ nguyên như bạn đã gửi ...
# (Không cần sửa lại phần UI, chỉ cần thay thế các hàm xử lý phía trên)