import streamlit as st
import random
import re
import time
import html
import pandas as pd
from datetime import datetime
import os
from gtts import gTTS
from io import BytesIO
import base64

# NEW: Thêm thư viện của Google Gemini
import google.generativeai as genai

# ... (Toàn bộ các hằng số STATE và hàm get_config() giữ nguyên như cũ) ...

# NEW: Cấu hình Gemini AI sử dụng Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    AI_ENABLED = True
except Exception as e:
    AI_ENABLED = False
    print(f"Lỗi cấu hình Gemini: {e}")

# ... (Toàn bộ phần thiết lập giao diện và CSS giữ nguyên) ...

# --- CÁC HÀM TIỆN ÍCH & LOGIC ---

# NEW: Hàm gọi AI Gemini
def call_gemini(prompt):
    """Gửi yêu cầu đến Gemini và trả về kết quả."""
    if not AI_ENABLED:
        return "Xin lỗi, tính năng AI hiện không khả dụng."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Xin lỗi, đã có lỗi xảy ra khi kết nối với AI: {e}"

# ... (Các hàm tiện ích khác như text_to_speech, add_message, set_state, detect_mood_from_text giữ nguyên) ...


# --- CÁC HÀM CALLBACK ---

# ... (Các hàm callback khác giữ nguyên) ...

# MODIFIED: Cập nhật hàm xử lý input của người dùng
def user_input_callback():
    """Xử lý khi người dùng nhập văn bản và nhấn Enter."""
    user_text = st.session_state.get("user_input", "")
    if not user_text: return
    
    add_message("user", user_text)
    st.session_state.turns += 1

    # Ưu tiên logic có sẵn trước
    detected_mood = detect_mood_from_text(user_text)

    if st.session_state.state == STATE_TAM_SU_CHAT:
        mood = st.session_state.current_mood
        response_text = random.choice(sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), []))
        if st.session_state.turns >= 2:
            set_state(STATE_AWAITING_FOLLOWUP)
            st.session_state.next_bot_response = f"{response_text} {CONFIG['general']['follow_up_prompt']}"
        else:
            st.session_state.next_bot_response = response_text
    elif detected_mood:
        set_state(STATE_TAM_SU_CHAT, current_mood=detected_mood, turns=0)
        st.session_state.next_bot_response = CONFIG["tam_su"]["moods"][detected_mood]["initial"]
    else:
        # MODIFIED: Nếu không khớp với logic nào, hãy gọi AI
        set_state(STATE_AWAITING_FOLLOWUP)
        # Hiển thị thông báo chờ trong khi gọi AI
        st.session_state.is_thinking = True 
        # Gọi Gemini AI
        ai_response = call_gemini(user_text)
        st.session_state.next_bot_response = ai_response
        st.session_state.is_thinking = False # Tắt trạng thái chờ
            
    st.session_state.user_input = ""

# ... (Toàn bộ phần vẽ giao diện và các hàm khác giữ nguyên) ...

# --- VẼ GIAO DIỆN CHÍNH ---

# ... (Phần vẽ tiêu đề và lịch sử chat giữ nguyên) ...

# Xử lý tin nhắn đang chờ của bot (bao gồm cả AI và tin nhắn thường)
if "next_bot_response" in st.session_state:
    bot_response_text = st.session_state.pop("next_bot_response")
    
    # Phát âm thanh trước
    audio_data = text_to_speech(bot_response_text)
    if audio_data:
        autoplay_audio(audio_data)

    # Hiển thị hiệu ứng gõ chữ
    with st.chat_message("bot"):
         st.write_stream(stream_response_generator(bot_response_text))
    
    add_message("bot", bot_response_text)

# Hiển thị chỉ báo "Bot đang suy nghĩ..." khi chờ AI
if st.session_state.get("is_thinking", False):
    with st.chat_message("bot"):
        st.markdown("<div class='typing-indicator'><span></span><span></span><span></span></div>", unsafe_allow_html=True)


# --- VẼ THANH FOOTER VÀ CÁC NÚT BẤM ---
# ... (Phần footer giữ nguyên) ...
