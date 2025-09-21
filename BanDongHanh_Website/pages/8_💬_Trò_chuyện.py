# pages/8_💬_Trò_chuyện.py
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


# ========== 0) HẰNG SỐ VÀ TRẠNG THÁI ==========

STATE_CHAT = "chat"
STATE_JOURNAL = "journal"
STATE_RELAX = "relax"

CHAT_STATE_MAIN = "main"
CHAT_STATE_TAM_SU_SELECTION = "tam_su_selection"
CHAT_STATE_TAM_SU_CHAT = "tam_su_chat"
CHAT_STATE_GIAO_TIEP_SELECTION_BASIC = "giao_tiep_selection_basic"
CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED = "giao_tiep_selection_extended"
CHAT_STATE_GIAO_TIEP_PRACTICE = "giao_tiep_practice"
CHAT_STATE_AWAITING_FOLLOWUP = "awaiting_followup"

# ========== 1) CẤU HÌNH UI & CSS ==========

st.set_page_config(page_title="💬 Trò chuyện", page_icon="💬", layout="wide")

st.markdown(
    """
<style>
/* Reset chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Layout */
.stApp { background-color: #FFFFFF; }
.chat-shell { 
    max-width: 820px; 
    margin: 0 auto; 
    padding-top: 64px; 
    padding-bottom: 150px; /* Increased to avoid overlap with input bar */
}

/* Header sticky giống app shopping */
.chat-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 999;
  background: #fff; border-bottom: 1px solid #efefef;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.chat-header-inner {
  max-width: 820px; margin: 0 auto; padding: 12px 16px;
  display: flex; align-items: center; gap: 12px;
}
.chat-title { font-weight: 700; font-size: 1.05rem; }

/* Bubbles */
.bubble-row { display:flex; margin: 12px 0; }
.bubble-user { justify-content: flex-end; }
.msg {
  border-radius: 18px; padding: 12px 16px; max-width: 75%;
  font-size: 1rem; line-height: 1.5; word-wrap: break-word;
}
.msg-user { 
  background: linear-gradient(135deg, #25D366, #128C7E); 
  color: white; 
  border-top-right-radius: 6px; 
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}
.msg-bot { 
  background: #F3F4F6; color: #111; border-top-left-radius: 6px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}

/* Typing indicator */
.typing { display:inline-block; padding: 8px 14px; border-radius: 18px; background: #F3F4F6; }
.typing span {
  height: 8px; width: 8px; margin: 0 2px; background-color: #9E9E9E;
  display: inline-block; border-radius: 50%; opacity: 0.5; animation: bob 1s infinite;
}
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
.typing span:nth-child(1){animation-delay:-0.3s} .typing span:nth-child(2){animation-delay:-0.15s}

/* Quick actions (chips) */
.quick-actions { display:flex; gap:10px; flex-wrap: wrap; margin: 10px 0 16px; }
.chip {
  border: none; color: white; background: linear-gradient(135deg, #0084FF, #0069cc);
  border-radius: 20px; padding: 8px 14px; font-size: 0.9rem; cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.chip:hover { transform: translateY(-2px); box-shadow: 0 3px 6px rgba(0,0,0,0.15); }

/* Sticky input */
.input-bar {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 999;
  background: #fff; border-top: 1px solid #efefef;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
}
.input-inner {
  max-width: 820px; margin: 0 auto; padding: 15px 16px;
}

/* Buttons */
button {
  transition: all 0.2s ease;
}
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 3px 6px rgba(0,0,0,0.1);
}

/* Option pills */
.option-pill {
  background: #f0f2f5;
  border-radius: 18px;
  padding: 10px 14px;
  margin: 5px 0;
  cursor: pointer;
  transition: all 0.2s;
  border: 1px solid #e4e6eb;
}

.option-pill:hover {
  background: #e4e6eb;
}

/* Scrollbar customization */
::-webkit-scrollbar {
  width: 8px;
}
::-webkit-scrollbar-track {
  background: #f1f1f1;
}
::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}

</style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
<div class="chat-header">
  <div class="chat-header-inner">
    <div>💬</div>
    <div class="chat-title">Trò chuyện - Bạn Đồng Hành</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ========== 2) CONFIG DỮ LIỆU NỘI DUNG ==========

@st.cache_data
def get_config():
    return {
        "ui": {
            "title": "Bạn đồng hành 💖",
            "input_placeholder": "Nhập tin nhắn của bạn...",
        },
        "tam_su": {
            "intro_message": "Hôm nay bạn cảm thấy như thế nào nè? Mình luôn sẵn lòng lắng nghe bạn nha 🌟",
            "positive_affirmation_trigger": "🌼 Nghe một lời tích cực",
            "positive_affirmations": [
                "Bạn mạnh mẽ hơn bạn nghĩ rất nhiều.",
                "Mỗi bước nhỏ bạn đi đều là một thành công lớn.",
                "Cảm xúc của bạn là thật và đáng được tôn trọng.",
                "Bạn xứng đáng được yêu thương và hạnh phúc.",
                "Hôm nay có thể khó khăn, nhưng ngày mai sẽ tốt hơn."
            ],
            "moods": {
                "😄 Vui": {
                    "keywords": ["vui", "hạnh phúc", "tuyệt vời", "giỏi", "đi chơi", "🎉", "😄"],
                    "initial": "Tuyệt vời quá! Có chuyện gì vui không, kể mình nghe với nè!",
                    "styles": {
                        "Khuyến khích": [
                            "Nghe là thấy vui giùm bạn luôn á! Kể thêm chút nữa đi!",
                            "Hôm nay chắc là một ngày đặc biệt rồi! Chia sẻ thêm nhé!"
                        ]
                    }
                },
                "😔 Buồn": {
                    "keywords": ["buồn", "chán", "stress", "cô đơn", "tệ", "😔"],
                    "initial": "Ôi, mình nghe rồi nè. Có chuyện gì làm bạn buồn vậy?",
                    "styles": {
                        "Lắng nghe": [
                            "Không sao đâu, bạn buồn cũng được mà. Kể mình nghe thêm nhé.",
                            "Bạn không cần phải gồng đâu, mình ở đây nè."
                        ]
                    }
                }
            }
        },
        "giao_tiep": {
            "intro_message": "Hãy chọn một tình huống bên dưới để mình cùng luyện tập nhé!",
            "confirm_buttons": {"understood": "✅ Đã hiểu!", "not_understood": "❓ Chưa rõ lắm!"},
            "scenarios_basic": {
                "👋 Chào hỏi bạn bè": "Bạn có thể nói: \"Chào bạn, hôm nay vui không?\"",
                "🙋 Hỏi bài thầy cô": "Bạn thử hỏi: \"Thầy/cô ơi, phần này em chưa rõ ạ?\""
            },
            "scenarios_extended": {
                "📚 Nhờ bạn giúp đỡ": "Bạn thử nói: \"Cậu chỉ mình chỗ này với được không?\"",
                "🙏 Xin lỗi khi đến muộn": "Bạn có thể nói: \"Em xin lỗi vì đã đến muộn, em có thể vào lớp không ạ?\"",
                "🤔 Hỏi khi không hiểu bài": "Thử nói: \"Em chưa hiểu phần này, thầy/cô có thể giải thích lại được không ạ?\"",
            },
        },
        "general": {
            "neutral_replies": [
                "Mình chưa rõ lắm, bạn nói cụ thể hơn được không?",
                "Mình đang nghe bạn nè, bạn muốn nói thêm điều gì không?",
                "Bạn có thể chia sẻ thêm về điều đó không?",
                "Mình muốn hiểu bạn hơn. Bạn có thể kể chi tiết hơn được không?"
            ],
            "follow_up_prompt": "Bạn muốn tiếp tục tâm sự hay luyện nói chuyện trong lớp nè?",
            "end_chat_replies": [
                "Cảm ơn bạn đã chia sẻ với mình hôm nay nha. Mình luôn sẵn sàng khi bạn cần 💖",
                "Bạn đã làm rất tốt khi bộc lộ cảm xúc. Khi nào cần, mình vẫn ở đây ✨"
            ],
        },
    }

CONFIG = get_config()

# ========== 3) SESSION STATE ==========

# Initialize session state
if "page_state" not in st.session_state:
    st.session_state.page_state = STATE_CHAT
    
if "chat_state" not in st.session_state:
    st.session_state.chat_state = CHAT_STATE_MAIN
    
if "history" not in st.session_state:
    st.session_state.history = [
        {"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}
    ]
    
if "turns" not in st.session_state:
    st.session_state.turns = 0
    
if "current_mood" not in st.session_state:
    st.session_state.current_mood = None
    
if "current_scenario" not in st.session_state:
    st.session_state.current_scenario = None
    
if "user_input_buffer" not in st.session_state:
    st.session_state.user_input_buffer = ""
    
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Lưu trữ context (thêm tính năng mới)
if "chat_context" not in st.session_state:
    st.session_state.chat_context = {
        "user_name": None,
        "chat_history": []
    }

# Voice settings defaults
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
    
if "tts_voice" not in st.session_state:
    st.session_state.tts_voice = "vi-VN-HoaiMyNeural"  # nữ
    
if "tts_rate" not in st.session_state:
    st.session_state.tts_rate = 0  # %

# ========== 4) GEMINI AI ==========

# Gemini optional
AI_ENABLED = False
if GENAI_AVAILABLE:
    try:
        # First try to get from secrets
        api_key = None
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY")
        except:
            pass
            
        # Then try environment variable
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY")
            
        if api_key:
            genai.configure(api_key=api_key)
            # Sử dụng gemini-1.0-pro thay vì flash để có context dài hơn
            gemini_model = genai.GenerativeModel("gemini-1.0-pro")
            
            # Tạo chat session để lưu context
            if "gemini_chat" not in st.session_state:
                st.session_state.gemini_chat = gemini_model.start_chat(history=[])
                
            AI_ENABLED = True
        else:
            st.sidebar.warning("Chưa cấu hình API key cho Gemini", icon="⚠️")
    except Exception as e:
        st.sidebar.error(f"Lỗi cấu hình Gemini: {str(e)}", icon="🚨")


def call_gemini(prompt):
    """Call Gemini AI for text generation with context awareness"""
    if not AI_ENABLED:
        return random.choice(CONFIG["general"]["neutral_replies"])
    try:
        # Lưu đoạn chat hiện tại vào context
        st.session_state.chat_context["chat_history"].append({"role": "user", "content": prompt})
        
        # Tạo nội dung system prompt
        system_prompt = (
            "Hãy trả lời như một người bạn đồng hành AI thân thiện, kiên nhẫn và thấu hiểu dành cho học sinh Việt Nam. "
            "Trả lời bằng tiếng Việt, ngắn gọn (dưới 100 từ) và giàu đồng cảm. "
            "Hạn chế trả lời giáo điều và sử dụng ngôn ngữ tự nhiên, thân thiện.\n\n"
            "Hãy nhớ thông tin cá nhân của người dùng nếu họ chia sẻ (như tên, tuổi, sở thích...)."
        )
        
        # Tạo prompt với context
        user_name = st.session_state.chat_context.get("user_name", "")
        if user_name:
            contextual_prompt = f"[Tên người dùng: {user_name}]\n{prompt}"
        else:
            contextual_prompt = prompt
            
            # Phát hiện tên người dùng
            name_match = re.search(r"tên (tôi|mình|của mình|tui|của tui) là (\w+)", prompt.lower())
            if name_match:
                detected_name = name_match.group(2)
                detected_name = detected_name.capitalize()
                st.session_state.chat_context["user_name"] = detected_name
        
        # Gửi đến Gemini với system prompt
        try:
            response = st.session_state.gemini_chat.send_message(
                contextual_prompt,
                system_instruction=system_prompt
            )
        except Exception as e:
            # Fallback: nếu gặp lỗi với system_instruction, thử lại không dùng
            response = st.session_state.gemini_chat.send_message(contextual_prompt)
        
        # Lưu phản hồi vào context
        st.session_state.chat_context["chat_history"].append({"role": "assistant", "content": response.text})
        
        return response.text
    except Exception as e:
        error_msg = f"Xin lỗi, hệ thống đang bận. Bạn thử lại sau nhé. (Lỗi: {str(e)[:50]}...)"
        print(f"Gemini Error: {e}")
        return error_msg

# ========== 5) TTS (EDGE TTS NEURAL + FALLBACK GTTS) ==========

def gtts_bytes(text):
    """Generate audio using gTTS as fallback"""
    if not GTTS_AVAILABLE:
        return None
    try:
        bio = BytesIO()
        tts = gTTS(text=text, lang="vi")
        tts.write_to_fp(bio)
        bio.seek(0)
        return bio.read()
    except Exception as e:
        print(f"Lỗi gTTS: {e}")
        return None

def edge_tts_bytes(text, voice, rate_pct):
    """Generate audio using Edge TTS synchronously (avoid asyncio issues)"""
    if not EDGE_TTS_AVAILABLE:
        return None
    
    try:
        # Use a synchronous approach to simplify the code and avoid asyncio issues
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        # Build command arguments
        rate_str = f"{'+' if rate_pct>=0 else ''}{rate_pct}%"
        
        # Run the communicate command synchronously
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate_str,
            "--text", text,
            "--write-media", temp_path
        ]
        
        # Execute the command
        subprocess.run(cmd, check=True, capture_output=True)
        
        # Read the audio data
        with open(temp_path, 'rb') as f:
            audio_data = f.read()
            
        # Clean up
        os.unlink(temp_path)
        
        return audio_data
    except Exception as e:
        print(f"Lỗi Edge TTS: {e}")
        return None

def synthesize_tts(text, voice, rate_pct):
    """Generate text-to-speech audio using available methods"""
    # Prefer Edge TTS neural
    if EDGE_TTS_AVAILABLE:
        audio = edge_tts_bytes(text, voice, rate_pct)
        if audio:
            return audio
            
    # Fallback gTTS
    return gtts_bytes(text)

def autoplay_audio(audio_data):
    """Play audio data automatically in the streamlit app"""
    if audio_data is None:
        return
        
    try:
        b64 = base64.b64encode(audio_data).decode()
        md = f"""
        <audio autoplay="true">
          <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.components.v1.html(md, height=0)
    except Exception as e:
        print(f"Lỗi phát âm thanh: {e}")


# ========== 6) LOGIC CHAT & AI ==========

def add_message(sender, text):
    """Add a message to the chat history"""
    st.session_state.history.append({"sender": sender, "text": text})

def detect_mood_from_text(text):
    """Detect mood from user input text"""
    cfg = CONFIG["tam_su"]["moods"]
    lowered = text.lower()
    tokens = set(re.findall(r"\b\w+\b", lowered))
    emojis = {"😄", "😔"}
    tokens.update(ch for ch in text if ch in emojis)
    best, score = None, 0
    for mood, m_cfg in cfg.items():
        kws = set(m_cfg["keywords"])
        matches = len(tokens.intersection(kws))
        if matches > score:
            best, score = mood, matches
    return best

def respond_bot(text):
    """Generate bot response with optional text-to-speech"""
    add_message("bot", text)
    
    # Synthesize voice if enabled
    if st.session_state.tts_enabled:
        with st.spinner("Đang tạo giọng nói..."):
            audio = synthesize_tts(text, st.session_state.tts_voice, st.session_state.tts_rate)
            if audio:
                autoplay_audio(audio)

# ========== 7) GIAO DIỆN CHÍNH (SHOPPING CHAT STYLE) ==========

with st.sidebar:
    st.markdown("### Cài đặt giọng nói")
    st.session_state.tts_enabled = st.toggle("Đọc to phản hồi", value=st.session_state.tts_enabled)
    
    voice = st.selectbox(
        "Giọng đọc",
        options=[
            "vi-VN-HoaiMyNeural (Nữ)",
            "vi-VN-NamMinhNeural (Nam)"
        ],
        index=0 if st.session_state.tts_voice.endswith("HoaiMyNeural") else 1
    )
    st.session_state.tts_voice = "vi-VN-HoaiMyNeural" if "HoaiMy" in voice else "vi-VN-NamMinhNeural"
    
    rate = st.slider("Tốc độ nói (%)", -50, 50, st.session_state.tts_rate, step=5)
    st.session_state.tts_rate = rate
    
    if AI_ENABLED:
        st.success("✅ AI đã được kết nối")
    else:
        st.warning("⚠️ Chức năng AI chưa sẵn sàng")
    
    st.divider()
    
    # Thêm nút xóa lịch sử
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.history = [
            {"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}
        ]
        st.session_state.chat_context = {"user_name": None, "chat_history": []}
        if "gemini_chat" in st.session_state:
            if AI_ENABLED:
                st.session_state.gemini_chat = gemini_model.start_chat(history=[])
            else:
                st.session_state.gemini_chat = None
        st.success("Đã xóa lịch sử trò chuyện!")
        st.rerun()
    
    # About section
    st.markdown("### Giới thiệu")
    st.markdown("""
    **Bạn Đồng Hành** là chatbot hỗ trợ tâm lý và kỹ năng giao tiếp cho học sinh.
    
    Chatbot có thể:
    - Lắng nghe và đồng cảm với cảm xúc
    - Hỗ trợ luyện tập giao tiếp
    - Ghi nhật ký cảm xúc
    - Hướng dẫn bài tập thư giãn
    """)
    
    st.markdown("Phiên bản: 1.3.0")

# Shell for chat
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

# Quick action chips
quick_actions_col = st.container()
with quick_actions_col:
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    qa_cols = st.columns(4)
    with qa_cols[0]:
        if st.button("💖 Tâm sự", use_container_width=True, key="btn_tam_su", help="Trò chuyện và chia sẻ cảm xúc"):
            st.session_state.chat_state = CHAT_STATE_TAM_SU_SELECTION
            respond_bot(CONFIG["tam_su"]["intro_message"])
            st.rerun()
    with qa_cols[1]:
        if st.button("🗣️ Luyện giao tiếp", use_container_width=True, key="btn_giao_tiep", help="Thực hành kỹ năng giao tiếp"):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_BASIC
            respond_bot(CONFIG["giao_tiep"]["intro_message"])
            st.rerun()
    with qa_cols[2]:
        if st.button("📓 Nhật ký", use_container_width=True, key="btn_journal", help="Lưu lại cảm xúc hàng ngày"):
            st.session_state.page_state = STATE_JOURNAL
            st.rerun()
    with qa_cols[3]:
        if st.button("😌 Thư giãn", use_container_width=True, key="btn_relax", help="Các hoạt động giúp thư giãn"):
            st.session_state.page_state = STATE_RELAX
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Message history
message_container = st.container()
with message_container:
    for m in st.session_state.history:
        cls_row = "bubble-row bubble-user" if m["sender"] == "user" else "bubble-row"
        cls_msg = "msg msg-user" if m["sender"] == "user" else "msg msg-bot"
        st.markdown(
            f'<div class="{cls_row}"><div class="{cls_msg}">{html.escape(m["text"])}</div></div>',
            unsafe_allow_html=True
        )

    # Show typing indicator while processing
    if st.session_state.is_processing:
        st.markdown(
            '<div class="bubble-row"><div class="typing"><span></span><span></span><span></span></div></div>',
            unsafe_allow_html=True
        )

# Suggested quick replies based on state
options_container = st.container()

with options_container:
    if st.session_state.chat_state == CHAT_STATE_TAM_SU_SELECTION:
        moods = list(CONFIG["tam_su"]["moods"].keys())
        st.markdown("#### Gợi ý cảm xúc")
        cols = st.columns(len(moods))
        for i, mood in enumerate(moods):
            if cols[i].button(mood, key=f"mood_{i}"):
                st.session_state.chat_state = CHAT_STATE_TAM_SU_CHAT
                st.session_state.current_mood = mood
                st.session_state.turns = 0
                respond_bot(CONFIG["tam_su"]["moods"][mood]["initial"])
                st.rerun()

    elif st.session_state.chat_state == CHAT_STATE_TAM_SU_CHAT:
        st.markdown("#### Tùy chọn")
        col1, col2 = st.columns(2)
        if col1.button(CONFIG["tam_su"]["positive_affirmation_trigger"], use_container_width=True):
            affirm = random.choice(CONFIG["tam_su"]["positive_affirmations"])
            st.session_state.chat_state = CHAT_STATE_MAIN
            respond_bot(affirm)
            st.rerun()
        if col2.button("🏁 Kết thúc", use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_MAIN
            respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))
            st.rerun()

    elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_SELECTION_BASIC:
        st.markdown("#### Tình huống cơ bản")
        for scenario in CONFIG["giao_tiep"]["scenarios_basic"].keys():
            if st.button(scenario, use_container_width=True, key=f"scenario_basic_{scenario}"):
                st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_PRACTICE
                st.session_state.current_scenario = scenario
                respond_bot(CONFIG["giao_tiep"]["scenarios_basic"][scenario])
                st.rerun()

    elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED:
        st.markdown("#### Tình huống nâng cao")
        for scenario in CONFIG["giao_tiep"]["scenarios_extended"].keys():
            if st.button(scenario, use_container_width=True, key=f"scenario_extended_{scenario}"):
                st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_PRACTICE
                st.session_state.current_scenario = scenario
                respond_bot(CONFIG["giao_tiep"]["scenarios_extended"][scenario])
                st.rerun()

    elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_PRACTICE:
        st.markdown("#### Bạn đã hiểu chưa?")
        b1, b2, b3 = st.columns(3)
        if b1.button(CONFIG["giao_tiep"]["confirm_buttons"]["understood"], use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED
            respond_bot("Tuyệt vời! Cùng xem các tình huống mở rộng nhé!")
            st.rerun()
        if b2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"], use_container_width=True):
            sc = st.session_state.current_scenario
            text = CONFIG["giao_tiep"]["scenarios_basic"].get(sc) or CONFIG["giao_tiep"]["scenarios_extended"].get(sc, "")
            respond_bot(f"Không sao cả, mình nói lại nhé:\n\n{text}")
            st.rerun()
        if b3.button("⏹️ Dừng", use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_MAIN
            respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))
            st.rerun()


# Chat input
user_text = st.chat_input(CONFIG["ui"]["input_placeholder"])

if user_text and not st.session_state.is_processing:
    # Set flag to indicate processing
    st.session_state.is_processing = True
    
    # Add user message
    add_message("user", user_text)
    st.session_state.turns += 1

    # Rerun to display the user message immediately
    st.rerun()

# Process the input after rerun if the processing flag is set
if st.session_state.is_processing:
    try:
        # Get the last user message
        last_msg = [m for m in st.session_state.history if m["sender"] == "user"][-1]
        user_text = last_msg["text"]
        
        # Process the user message based on the current state
        if st.session_state.chat_state == CHAT_STATE_TAM_SU_CHAT:
            mood = st.session_state.current_mood
            styles_all = sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), [])
            response_text = random.choice(styles_all)
            if st.session_state.turns >= 2:
                st.session_state.chat_state = CHAT_STATE_AWAITING_FOLLOWUP
                respond_bot(f"{response_text} {CONFIG['general']['follow_up_prompt']}")
            else:
                respond_bot(response_text)
        else:
            detected = detect_mood_from_text(user_text)
            if detected:
                st.session_state.chat_state = CHAT_STATE_TAM_SU_CHAT
                st.session_state.current_mood = detected
                st.session_state.turns = 0
                respond_bot(CONFIG["tam_su"]["moods"][detected]["initial"])
            else:
                # Call AI for open-ended stuff
                reply = call_gemini(user_text)
                st.session_state.chat_state = CHAT_STATE_AWAITING_FOLLOWUP
                respond_bot(reply)
    except Exception as e:
        print(f"Error processing message: {e}")
        respond_bot("Xin lỗi, có lỗi xảy ra. Bạn có thể thử lại sau.")
    finally:
        # Reset the processing flag
        st.session_state.is_processing = False
    
    st.rerun()

# Close shell
st.markdown('</div>', unsafe_allow_html=True)

# Sticky input bar wrapper
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
    st.title("📓 Nhật Ký Cảm Xúc")
    MOOD_FILE = "mood_journal.csv"
    MOOD_OPTIONS = ["😄 Vui", "😔 Buồn", "😠 Tức giận", "😴 Mệt mỏi", "😐 Bình thường"]

    def load_mood_data():
        try:
            if os.path.exists(MOOD_FILE):
                try:
                    return pd.read_csv(MOOD_FILE)
                except pd.errors.EmptyDataError:
                    pass
        except Exception as e:
            st.error(f"Lỗi khi đọc dữ liệu nhật ký: {e}")
        return pd.DataFrame(columns=["Ngày", "Cảm xúc", "Ghi chú"])

    journal_df = load_mood_data()
    
    # Use two columns for the form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Hôm nay bạn cảm thấy thế nào?")
        with st.form("mood_form"):
            log_date = st.date_input("Chọn ngày", datetime.now())
            selected_mood = st.selectbox("Chọn cảm xúc", MOOD_OPTIONS)
            note = st.text_area("Ghi chú thêm (không bắt buộc)", height=100)
            submitted = st.form_submit_button("Lưu lại cảm xúc", use_container_width=True)
            
            if submitted:
                try:
                    new_entry = pd.DataFrame(
                        [{"Ngày": log_date.strftime("%Y-%m-%d"), "Cảm xúc": selected_mood, "Ghi chú": note}]
                    )
                    if not journal_df.empty:
                        journal_df["Ngày"] = journal_df["Ngày"].astype(str)
                        if log_date.strftime("%Y-%m-%d") in journal_df["Ngày"].values:
                            st.warning("Bạn đã ghi lại cảm xúc cho ngày này rồi.")
                        else:
                            journal_df = pd.concat([journal_df, new_entry], ignore_index=True)
                            journal_df.to_csv(MOOD_FILE, index=False)
                            st.success("Đã lưu nhật ký cảm xúc thành công!")
                            st.rerun()
                    else:
                        journal_df = new_entry
                        journal_df.to_csv(MOOD_FILE, index=False)
                        st.success("Đã lưu nhật ký cảm xúc đầu tiên!")
                        st.rerun()
                except Exception as e:
                    st.error(f"Lỗi khi lưu nhật ký: {e}")
    
    with col2:
        if not journal_df.empty:
            st.markdown("### Thống kê cảm xúc")
            try:
                mood_counts = journal_df["Cảm xúc"].value_counts()
                st.bar_chart(mood_counts)
            except Exception:
                st.info("Chưa có đủ dữ liệu để hiển thị thống kê.")

    st.markdown("### Lịch sử cảm xúc")
    if not journal_df.empty:
        # Format dataframe for display
        display_df = journal_df.sort_values(by="Ngày", ascending=False).copy()
        display_df.rename(columns={
            "Ngày": "📅 Ngày", 
            "Cảm xúc": "😊 Cảm xúc", 
            "Ghi chú": "📝 Ghi chú"
        }, inplace=True)
        
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "📝 Ghi chú": st.column_config.TextColumn(
                    "📝 Ghi chú",
                    width="large",
                    help="Những điều bạn ghi lại"
                )
            },
            hide_index=True
        )
    else:
        st.info("Nhật ký của bạn còn trống. Hãy thêm một mục nhật ký đầu tiên nhé!")

    if st.button("⬅️ Quay lại trò chuyện", use_container_width=False, key="back_from_journal"):
        st.session_state.page_state = STATE_CHAT
        st.rerun()

def render_relax_ui():
    st.title("😌 Góc Thư Giãn")
    
    tabs = st.tabs(["🧘 Hít thở", "🎵 Âm thanh", "📋 Hướng dẫn"])
    
    with tabs[0]:
        st.markdown("### Bài tập hít thở hộp (4-4-4-4)")
        st.info("Kỹ thuật này giúp giảm lo âu và căng thẳng bằng cách kiểm soát nhịp thở.")
        
        col1, col2 = st.columns([3,1])
        
        with col1:
            if st.button("Bắt đầu bài tập hít thở", key="start_breathing", use_container_width=True):
                placeholder = st.empty()
                for i in range(3):
                    placeholder.warning(f"Chuẩn bị... {3-i}")
                    time.sleep(1)
                
                steps = [
                    ("Hít vào từ từ qua mũi", 4),
                    ("Giữ hơi thở", 4),
                    ("Thở ra từ từ qua miệng", 4),
                    ("Tiếp tục giữ nhịp trước khi hít vào", 4)
                ]
                
                # Repeat the cycle 3 times
                for cycle in range(3):
                    placeholder.markdown(f"### Chu kỳ {cycle+1}/3")
                    for title, sec in steps:
                        for i in range(sec, 0, -1):
                            placeholder.success(f"{title} ({i}s)")
                            time.sleep(1)
                
                placeholder.success("✅ Hoàn thành! Bạn cảm thấy thư giãn hơn chưa?")
        
        with col2:
            st.markdown("**Lợi ích:**")
            st.markdown("""
            - Giảm căng thẳng
            - Tập trung tốt hơn
            - Kiểm soát lo âu
            - Cải thiện giấc ngủ
            """)
            
    with tabs[1]:
        st.markdown("### Âm thanh thiên nhiên giúp thư giãn")
        st.write("Hãy nhấn play và thưởng thức âm thanh trong lúc học tập hoặc nghỉ ngơi.")
        
        col1, col2, col3 = st.columns(3)
        with col1: 
            st.markdown("#### Mưa rơi nhẹ nhàng")
            st.video("https://www.youtube.com/watch?v=eKFTSSKCzWA")
        with col2: 
            st.markdown("#### Sóng biển êm đềm")
            st.video("https://www.youtube.com/watch?v=gM_r4c6i25s")
        with col3: 
            st.markdown("#### Rừng nhiệt đới")
            st.video("https://www.youtube.com/watch?v=aIIEI33EUqI")
    
    with tabs[2]:
        st.markdown("### Hướng dẫn thư giãn nhanh")
        st.markdown("""
        #### 1. Thư giãn cơ bắp tiến bộ
        1. Ngồi hoặc nằm thoải mái
        2. Siết chặt bàn tay thành nắm đấm trong 5 giây
        3. Thả lỏng trong 10 giây
        4. Lặp lại với các nhóm cơ khác: cánh tay, vai, mặt, bụng, chân
        
        #### 2. Kỹ thuật 5-4-3-2-1
        Khi cảm thấy căng thẳng, hãy liệt kê:
        - 5 thứ bạn NHÌN thấy
        - 4 thứ bạn CÓ THỂ CHẠM vào
        - 3 thứ bạn NGHE thấy
        - 2 thứ bạn NGỬI thấy
        - 1 thứ bạn NẾM thấy
        
        Kỹ thuật này giúp kéo bạn về hiện tại và giảm lo âu.
        """)
    
    if st.button("⬅️ Quay lại trò chuyện", use_container_width=False, key="back_from_relax"):
        st.session_state.page_state = STATE_CHAT
        st.rerun()

# Router nội bộ
if st.session_state.page_state == STATE_JOURNAL:
    render_journal_ui()
elif st.session_state.page_state == STATE_RELAX:
    render_relax_ui()
# STATE_CHAT hiển thị ở trên
