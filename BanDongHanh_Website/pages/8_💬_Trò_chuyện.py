# Dán toàn bộ code này vào file pages/8_💬_Trò_chuyện.py
import base64
import html
import os
import random
import re
import time
import subprocess
import tempfile
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

# Optional: Gemini
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False

# Fallback TTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Preferred neural TTS (Microsoft Edge TTS)
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé! ❤️")
    st.stop()
    
# ========== 0) HẰNG SỐ VÀ TRẠNG THÁI ==========
STATE_CHAT = "chat"
STATE_JOURNAL = "journal"
STATE_RELAX = "relax"
CHAT_STATE_MAIN = "main"
CHAT_STATE_TAM_SU_SELECTION = "tam_su_selection"
CHAT_STATE_TAM_SU_CHAT = "tam_su_chat"
CHAT_STATE_GIAO_TIEP_SELECTION_BASIC = "giao_tiep_selection_basic"
CHAT_STATE_AWAITING_FOLLOWUP = "awaiting_followup"

# ========== 1) CẤU HÌNH UI & CSS ==========
st.set_page_config(page_title="💬 Trò chuyện", page_icon="💬", layout="wide")
st.markdown(
    """
<style>
/* Reset chrome */
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #FFFFFF; }
.chat-shell { max-width: 820px; margin: 0 auto; padding-top: 64px; padding-bottom: 150px;}
.chat-header { position: fixed; top: 0; left: 0; right: 0; z-index: 999; background: #fff; border-bottom: 1px solid #efefef; box-shadow: 0 2px 10px rgba(0,0,0,0.05);}
.chat-header-inner { max-width: 820px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; gap: 12px;}
.chat-title { font-weight: 700; font-size: 1.05rem; }
.bubble-row { display:flex; margin: 12px 0; }
.bubble-user { justify-content: flex-end; }
.msg { border-radius: 18px; padding: 12px 16px; max-width: 75%; font-size: 1rem; line-height: 1.5; word-wrap: break-word;}
.msg-user { background: linear-gradient(135deg, #25D366, #128C7E); color: white; border-top-right-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.1);}
.msg-bot { background: #F3F4F6; color: #111; border-top-left-radius: 6px; box-shadow: 0 1px 2px rgba(0,0,0,0.05);}
.typing { display:inline-block; padding: 8px 14px; border-radius: 18px; background: #F3F4F6; }
.typing span { height: 8px; width: 8px; margin: 0 2px; background-color: #9E9E9E; display: inline-block; border-radius: 50%; opacity: 0.5; animation: bob 1s infinite;}
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
.typing span:nth-child(1){animation-delay:-0.3s} .typing span:nth-child(2){animation-delay:-0.15s}
.quick-actions { display:flex; gap:10px; flex-wrap: wrap; margin: 10px 0 16px; }
.input-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 999; background: #fff; border-top: 1px solid #efefef; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);}
.input-inner { max-width: 820px; margin: 0 auto; padding: 15px 16px;}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown("""<div class="chat-header"> <div class="chat-header-inner"> <div>💬</div> <div class="chat-title">Trò chuyện - Bạn Đồng Hành</div> </div> </div>""", unsafe_allow_html=True)

# ========== 2) CONFIG DỮ LIỆU NỘI DUNG ==========
@st.cache_data
def get_config():
    return {
        "ui": { "title": "Bạn đồng hành 💖", "input_placeholder": "Nhập tin nhắn của bạn...", },
        "tam_su": {
            "intro_message": "Hôm nay bạn cảm thấy như thế nào nè? Mình luôn sẵn lòng lắng nghe bạn nha 🌟",
            "positive_affirmation_trigger": "🌼 Nghe một lời tích cực",
            "positive_affirmations": [
                "Bạn mạnh mẽ hơn bạn nghĩ rất nhiều.", "Mỗi bước nhỏ bạn đi đều là một thành công lớn.",
                "Cảm xúc của bạn là thật và đáng được tôn trọng.", "Bạn xứng đáng được yêu thương và hạnh phúc.",
                "Hôm nay có thể khó khăn, nhưng ngày mai sẽ tốt hơn."
            ],
            "moods": {
                "😄 Vui": { "keywords": ["vui", "hạnh phúc", "tuyệt vời"], "initial": "Tuyệt vời quá! Có chuyện gì vui không, kể mình nghe với nè!", "styles": {"Khuyến khích": ["Nghe là thấy vui giùm bạn luôn á! Kể thêm chút nữa đi!"]} },
                "😔 Buồn": { "keywords": ["buồn", "chán", "stress", "cô đơn"], "initial": "Ôi, mình nghe rồi nè. Có chuyện gì làm bạn buồn vậy?", "styles": {"Lắng nghe": ["Không sao đâu, bạn buồn cũng được mà. Kể mình nghe thêm nhé."]} }
            }
        },
        "giao_tiep": { "intro_message": "Hãy chọn một tình huống bên dưới để mình cùng luyện tập nhé!", "scenarios_basic": { "👋 Chào hỏi bạn bè": "Bạn có thể nói: \"Chào bạn, hôm nay vui không?\"", "🙋 Hỏi bài thầy cô": "Bạn thử hỏi: \"Thầy/cô ơi, phần này em chưa rõ ạ?\"" } },
        "general": { "neutral_replies": ["Mình chưa rõ lắm, bạn nói cụ thể hơn được không?"], "follow_up_prompt": "Bạn muốn tiếp tục tâm sự hay luyện nói chuyện trong lớp nè?", "end_chat_replies": ["Cảm ơn bạn đã chia sẻ với mình hôm nay nha."] },
    }
CONFIG = get_config()

# ========== 3) SESSION STATE ==========
if "page_state" not in st.session_state: st.session_state.page_state = "chat"
if "chat_state" not in st.session_state: st.session_state.chat_state = "main"
if "history" not in st.session_state: st.session_state.history = [{"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}]
if "turns" not in st.session_state: st.session_state.turns = 0

# ========== 4) GEMINI AI (PHIÊN BẢN ĐÃ SỬA LỖI) ==========
@st.cache_resource
def initialize_gemini():
    if not GENAI_AVAILABLE:
        st.sidebar.warning("Thư viện google.generativeai chưa được cài đặt.", icon="⚠️")
        return None

    api_key = st.secrets.get("GOOGLE_API_KEY")
    if not api_key:
        st.sidebar.error("Chưa cấu hình `GOOGLE_API_KEY` trong Streamlit Secrets.", icon="🚨")
        return None
    
    try:
        genai.configure(api_key=api_key)
        # TẬP TRUNG VÀO MODEL ỔN ĐỊNH NHẤT LÀ "gemini-pro"
        model = genai.GenerativeModel("gemini-pro") 
        # Ping model để kiểm tra kết nối
        model.generate_content("ping", generation_config={"max_output_tokens": 1}) 
        st.sidebar.success("✅ AI đã kết nối thành công!")
        return model
    except Exception as e:
        st.sidebar.error(f"Lỗi kết nối Gemini: {e}", icon="🚨")
        return None

gemini_model = initialize_gemini()
AI_ENABLED = gemini_model is not None

if AI_ENABLED and "gemini_chat" not in st.session_state:
    st.session_state.gemini_chat = gemini_model.start_chat(history=[])

def call_gemini(prompt):
    if not AI_ENABLED or not hasattr(st.session_state, 'gemini_chat'):
        return "Xin lỗi, mình chưa sẵn sàng để trò chuyện. Bạn thử lại sau nhé."
    
    try:
        response = st.session_state.gemini_chat.send_message(prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi khi gọi Gemini: {e}")
        return "Xin lỗi, AI tạm thời không khả dụng."

# ========== 5) CÁC HÀM KHÁC ==========
def add_message(sender, text):
    st.session_state.history.append({"sender": sender, "text": text})

def respond_bot(text):
    add_message("bot", text)
    # TTS logic can be added here if needed

# ========== 6) GIAO DIỆN CHÍNH ==========

with st.sidebar:
    st.markdown("### Cài đặt")
    # SỬA LỖI ATTRIBUTEERROR
    st.session_state.tts_enabled = st.toggle("Đọc to phản hồi", value=st.session_state.get("tts_enabled", True))
    
    st.divider()
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.history = [{"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}]
        if AI_ENABLED:
            st.session_state.gemini_chat = gemini_model.start_chat(history=[])
        st.success("Đã xóa lịch sử trò chuyện!")
        st.rerun()

# Main chat UI
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

for m in st.session_state.history:
    st.markdown(f"**{m['sender']}**: {m['text']}")

if st.session_state.chat_state == "main":
    qa_cols = st.columns(2)
    if qa_cols[0].button("💖 Tâm sự", use_container_width=True):
        st.session_state.chat_state = "tam_su_selection"
        respond_bot(CONFIG["tam_su"]["intro_message"])
        st.rerun()
    if qa_cols[1].button("🗣️ Luyện giao tiếp", use_container_width=True):
        st.session_state.chat_state = "giao_tiep_selection_basic"
        respond_bot(CONFIG["giao_tiep"]["intro_message"])
        st.rerun()

if prompt := st.chat_input(CONFIG["ui"]["input_placeholder"]):
    add_message("user", prompt)
    
    with st.spinner("Bot đang suy nghĩ..."):
        response_text = call_gemini(prompt)
        respond_bot(response_text)
    
    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.chat_state == "main":
    quick_actions_col = st.container()
    with quick_actions_col:
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        qa_cols = st.columns(4)
        if qa_cols[0].button("💖 Tâm sự", use_container_width=True, key="btn_tam_su"):
            st.session_state.chat_state = "tam_su_selection"
            respond_bot(CONFIG["tam_su"]["intro_message"])
            st.rerun()
        if qa_cols[1].button("🗣️ Luyện giao tiếp", use_container_width=True, key="btn_giao_tiep"):
            st.session_state.chat_state = "giao_tiep_selection_basic"
            respond_bot(CONFIG["giao_tiep"]["intro_message"])
            st.rerun()
        if qa_cols[2].button("📓 Nhật ký", use_container_width=True, key="btn_journal"):
            st.session_state.page_state = "journal"
            st.rerun()
        if qa_cols[3].button("😌 Thư giãn", use_container_width=True, key="btn_relax"):
            st.session_state.page_state = "relax"
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

options_container = st.container()
with options_container:
    if st.session_state.chat_state == "tam_su_selection":
        moods = list(CONFIG["tam_su"]["moods"].keys())
        cols = st.columns(len(moods))
        for i, mood in enumerate(moods):
            if cols[i].button(mood, key=f"mood_{i}"):
                st.session_state.chat_state = "tam_su_chat"
                st.session_state.current_mood = mood
                st.session_state.turns = 0
                respond_bot(CONFIG["tam_su"]["moods"][mood]["initial"])
                st.rerun()
    elif st.session_state.chat_state == "tam_su_chat":
        st.markdown("#### Tùy chọn")
        col1, col2 = st.columns(2)
        if col1.button(CONFIG["tam_su"]["positive_affirmation_trigger"], use_container_width=True):
            affirm = random.choice(CONFIG["tam_su"]["positive_affirmations"])
            st.session_state.chat_state = "main"
            respond_bot(affirm)
            st.rerun()
        if col2.button("🏁 Kết thúc", use_container_width=True):
            st.session_state.chat_state = "main"
            respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))
            st.rerun()
    elif st.session_state.chat_state == "giao_tiep_selection_basic":
        st.markdown("#### Tình huống cơ bản")
        for scenario in CONFIG["giao_tiep"]["scenarios_basic"].keys():
            if st.button(scenario, use_container_width=True, key=f"scenario_basic_{scenario}"):
                st.session_state.chat_state = "giao_tiep_practice"
                st.session_state.current_scenario = scenario
                respond_bot(CONFIG["giao_tiep"]["scenarios_basic"][scenario])
                st.rerun()
    # ... (và các states còn lại như giao_tiep_selection_extended, giao_tiep_practice) ...

# Input bar và xử lý logic
if prompt := st.chat_input(CONFIG["ui"]["input_placeholder"]):
    add_message("user", prompt)
    st.session_state.turns += 1

    with st.chat_message("assistant"):
        st.markdown('<div class="bubble-row"><div class="typing"><span></span><span></span><span></span></div></div>', unsafe_allow_html=True)

        response_text = ""
        if st.session_state.chat_state == "tam_su_chat":
            mood = st.session_state.current_mood
            styles_all = sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), [])
            response_text = random.choice(styles_all)
            if st.session_state.turns >= 2:
                st.session_state.chat_state = "awaiting_followup"
                response_text += f" {CONFIG['general']['follow_up_prompt']}"
        else:
            detected_mood = detect_mood_from_text(prompt)
            if detected_mood:
                st.session_state.chat_state = "tam_su_chat"
                st.session_state.current_mood = detected_mood
                st.session_state.turns = 0
                response_text = CONFIG["tam_su"]["moods"][detected_mood]["initial"]
            else:
                response_text = call_gemini(prompt)
                st.session_state.chat_state = "awaiting_followup"

        respond_bot(response_text)

    st.rerun()

st.markdown('</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="input-bar">
  <div class="input-inner">
    <small style="color:#999">Mẹo: Bạn có thể bấm các gợi ý nhanh phía trên để thao tác nhanh hơn.</small>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ========== 8) ROUTER NỘI BỘ: NHẬT KÝ & THƯ GIÃN ==========
def render_journal_ui():
    # ... (Toàn bộ code của render_journal_ui) ...
    pass
def render_relax_ui():
    # ... (Toàn bộ code của render_relax_ui) ...
    pass

if st.session_state.page_state == "journal":
    render_journal_ui()
elif st.session_state.page_state == "relax":
    render_relax_ui()

