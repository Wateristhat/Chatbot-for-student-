# pages/8_💬_Trò_chuyện.py
import asyncio
import base64
import html
import os
import random
import re
import time
from datetime import datetime
from io import BytesIO

import pandas as pd
import streamlit as st

# Optional: Gemini - BỊ VÔ HIỆU HÓA ĐỂ TRÁNH LỖI KẾT NỐI
# Tôi giữ lại code nhưng sẽ không cố gắng kết nối ban đầu
GENAI_AVAILABLE = False
# try:
#     import google.generativeai as genai
#     GENAI_AVAILABLE = True
# except ImportError:
#     GENAI_AVAILABLE = False

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
            "simulated_ai_responses": [
                "Mình hiểu rồi. Cảm ơn bạn đã chia sẻ. Đôi khi mọi chuyện có vẻ khó khăn, nhưng bạn rất mạnh mẽ!",
                "Câu chuyện của bạn rất đáng suy nghĩ. Mình luôn ở đây để lắng nghe thêm nếu bạn muốn tâm sự.",
                "Mình cảm nhận được những gì bạn đang trải qua. Bạn có thể nói thêm về cảm xúc đó không?",
                "Đó là một câu hỏi hay. Mình tin rằng bạn sẽ tìm ra cách giải quyết vấn đề này. Mình có thể giúp bạn suy nghĩ thêm.",
            ]
        },
    }

CONFIG = get_config()

# Gemini optional - Vô hiệu hóa để tránh lỗi kết nối
AI_ENABLED = False
if GENAI_AVAILABLE:
    try:
        api_key = None
        try:
            api_key = st.secrets.get("GOOGLE_API_KEY")
        except:
            pass
            
        if not api_key:
            api_key = os.environ.get("GOOGLE_API_KEY")
            
        if api_key:
            import google.generativeai as genai # Import ở đây nếu cần
            genai.configure(api_key=api_key)
            # Dùng 'gemini-2.5-flash' hoặc 'gemini-1.5-flash'
            gemini_model = genai.GenerativeModel("gemini-1.5-flash")
            AI_ENABLED = True
        else:
            st.sidebar.warning("Chưa cấu hình API key cho Gemini. Đã chuyển sang chế độ dự phòng.", icon="⚠️")
    except Exception as e:
        st.sidebar.error(f"Lỗi cấu hình Gemini: {str(e)[:50]}... Đã chuyển sang chế độ dự phòng.", icon="🚨")


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
    
# Đã xóa 'user_input_buffer' vì không sử dụng
    
if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

# Voice settings defaults
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
    
if "tts_voice" not in st.session_state:
    st.session_state.tts_voice = "vi-VN-HoaiMyNeural"  # nữ
    
if "tts_rate" not in st.session_state:
    st.session_state.tts_rate = 0  # %

# Nhật ký (Sử dụng session state thay vì file cục bộ)
if "journal_data" not in st.session_state:
    st.session_state.journal_data = pd.DataFrame(columns=["Ngày", "Cảm xúc", "Ghi chú"])


# ========== 4) TTS (EDGE TTS NEURAL + FALLBACK GTTS) ==========

# @st.cache_data removed from gtts_bytes/edge_tts_bytes to ensure fresh run if args change slightly (optional but safer)
# Tuy nhiên, trong context này, tôi giữ lại @st.cache_data để tối ưu hóa performance như trong code gốc.

@st.cache_data(show_spinner=False)
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

@st.cache_data(show_spinner=False)
def edge_tts_bytes(text, voice, rate_pct):
    """Generate audio using Edge TTS (preferred method)"""
    if not EDGE_TTS_AVAILABLE:
        return None
    
    try:
        # Sử dụng threading.Thread hoặc multiprocessing để tránh block luồng chính
        # Tuy nhiên, để đơn giản và phù hợp với Streamlit, chúng ta dùng asyncio trong hàm cache
        # và giả định môi trường cho phép chạy asyncio.
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def _synthesize():
            # Đảm bảo rate_pct là số nguyên
            rate_pct_int = int(rate_pct)
            rate_str = f"{'+' if rate_pct_int>=0 else ''}{rate_pct_int}%"
            communicate = edge_tts.Communicate(text, voice=voice, rate=rate_str)
            audio = b""
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio += chunk["data"]
            return audio
            
        audio_data = loop.run_until_complete(_synthesize())
        loop.close()
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


# ========== 5) LOGIC CHAT & AI ==========

def add_message(sender, text):
    """Add a message to the chat history"""
    st.session_state.history.append({"sender": sender, "text": text})

def detect_mood_from_text(text):
    """Detect mood from user input text"""
    cfg = CONFIG["tam_su"]["moods"]
    lowered = text.lower()
    # Tìm từ khóa
    tokens = set(re.findall(r"\b\w+\b", lowered))
    # Tìm emoji
    emojis = set(re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+', text))
    # Gộp cả từ khóa và emoji (chỉ lấy các emoji có trong cấu hình)
    all_tokens = tokens.union(ch for mood_cfg in cfg.values() for ch in mood_cfg["keywords"] if ch in text)
    
    best, score = None, 0
    for mood, m_cfg in cfg.items():
        kws = set(m_cfg["keywords"])
        # Chỉ xét từ khóa hoặc emoji có trong cấu hình
        matches = len(all_tokens.intersection(kws))
        if matches > score:
            best, score = mood, matches
    return best

def get_ai_response(prompt):
    """
    Call Gemini AI for text generation hoặc dùng Fallback Logic.
    Phần này sẽ bị block nếu AI_ENABLED = True.
    """
    if AI_ENABLED:
        try:
            contextual = (
                "Hãy trả lời như một người bạn đồng hành AI thân thiện, kiên nhẫn và thấu hiểu dành cho học sinh."
                " Trả lời bằng tiếng Việt, ngắn gọn (dưới 100 từ) và giàu đồng cảm. "
                " Hạn chế trả lời giáo điều và sử dụng ngôn ngữ tự nhiên, thân thiện.\n\n"
                f"Câu hỏi/Chia sẻ của người dùng: '{prompt}'"
            )
            # Dùng st.spinner ở giao diện để hiển thị trạng thái chờ
            # LƯU Ý: Hàm này BLOCK luồng, nên cần xử lý hiển thị hiệu ứng "Đang gõ" ở phía gọi.
            resp = gemini_model.generate_content(contextual)
            return resp.text or random.choice(CONFIG["general"]["neutral_replies"])
        except Exception as e:
            # Nếu có lỗi khi gọi AI (ví dụ: timeout, API key hết hạn)
            return f"Xin lỗi, có lỗi khi kết nối AI: {str(e)[:50]}.... Đã chuyển sang phản hồi dự phòng: {random.choice(CONFIG['general']['simulated_ai_responses'])}"
            
    # Fallback Logic (Dự phòng)
    # Mô phỏng thời gian chờ để người dùng cảm nhận ứng dụng đang "nghĩ"
    time.sleep(random.uniform(1.0, 2.5)) 
    return random.choice(CONFIG["general"]["simulated_ai_responses"])


def respond_bot(text):
    """Generate bot response with optional text-to-speech"""
    # Không cần dùng st.spinner trong hàm này nữa, dùng bên ngoài khi gọi hàm AI
    add_message("bot", text)
    
    # Synthesize voice if enabled
    if st.session_state.tts_enabled:
        audio = synthesize_tts(text, st.session_state.tts_voice, st.session_state.tts_rate)
        if audio:
            autoplay_audio(audio)
            

# ========== 6) GIAO DIỆN CHÍNH (SHOPPING CHAT STYLE) ==========

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
    
    st.divider()
    
    # About section
    st.markdown("### Giới thiệu")
    if not AI_ENABLED:
         st.warning("⚠️ **Chế độ Dự phòng:** Chức năng AI bị vô hiệu hóa do lỗi kết nối/cấu hình API. Phản hồi chung được mô phỏng.", icon="🚫")
    st.markdown("""
    **Bạn Đồng Hành** là chatbot hỗ trợ tâm lý và kỹ năng giao tiếp cho học sinh.
    
    Chatbot có thể:
    - Lắng nghe và đồng cảm với cảm xúc
    - Hỗ trợ luyện tập giao tiếp
    - Ghi nhật ký cảm xúc
    - Hướng dẫn bài tập thư giãn
    """)
    
    st.markdown("Phiên bản: 1.2.1 (Sửa lỗi)")

# Shell for chat
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

# Quick action chips
quick_actions_col = st.container()
with quick_actions_col:
    # Logic chỉ hiển thị quick actions khi ở trạng thái MAIN hoặc AWAITING_FOLLOWUP
    if st.session_state.chat_state in (CHAT_STATE_MAIN, CHAT_STATE_AWAITING_FOLLOWUP):
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        qa_cols = st.columns(4)
        with qa_cols[0]:
            if st.button("💖 Tâm sự", use_container_width=True, key="btn_tam_su"):
                st.session_state.chat_state = CHAT_STATE_TAM_SU_SELECTION
                respond_bot(CONFIG["tam_su"]["intro_message"])
                st.rerun()
        with qa_cols[1]:
            if st.button("🗣️ Luyện giao tiếp", use_container_width=True, key="btn_giao_tiep"):
                st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_BASIC
                respond_bot(CONFIG["giao_tiep"]["intro_message"])
                st.rerun()
        with qa_cols[2]:
            if st.button("📓 Nhật ký", use_container_width=True, key="btn_journal"):
                st.session_state.page_state = STATE_JOURNAL
                st.rerun()
        with qa_cols[3]:
            if st.button("😌 Thư giãn", use_container_width=True, key="btn_relax"):
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

    # Hiển thị Typing Indicator TẠM THỜI (để giữ vị trí)
    # LƯU Ý: Hiệu ứng này chỉ thực sự hoạt động nếu có 2 lần rerun, rất khó trong Streamlit
    # Tôi sẽ cố gắng giữ nguyên logic để bạn tùy chỉnh sau.
    # if st.session_state.is_processing:
    #     st.markdown(
    #         '<div class="bubble-row"><div class="typing"><span></span><span></span><span></span></div></div>',
    #         unsafe_allow_html=True
    #     )
    
# Suggested quick replies based on state
options_container = st.container()

with options_container:
    if st.session_state.chat_state == CHAT_STATE_TAM_SU_SELECTION:
        st.markdown("#### Gợi ý cảm xúc")
        moods = list(CONFIG["tam_su"]["moods"].keys())
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
        # Thêm nút chuyển sang Tình huống nâng cao
        if st.button("Xem tình huống nâng cao ➡️", key="btn_ext_scenarios"):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED
            st.rerun()

        for scenario in CONFIG["giao_tiep"]["scenarios_basic"].keys():
            if st.button(scenario, use_container_width=True, key=f"scenario_basic_{scenario}"):
                st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_PRACTICE
                st.session_state.current_scenario = scenario
                respond_bot(CONFIG["giao_tiep"]["scenarios_basic"][scenario])
                st.rerun()

    elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED:
        st.markdown("#### Tình huống nâng cao")
        # Thêm nút quay lại Tình huống cơ bản
        if st.button("⬅️ Quay lại tình huống cơ bản", key="btn_basic_scenarios"):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_BASIC
            st.rerun()
            
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
            # Sau khi hiểu, chuyển sang chế độ mở rộng
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED
            respond_bot("Tuyệt vời! Cùng xem các tình huống mở rộng nhé!")
            st.rerun()
        if b2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"], use_container_width=True):
            sc = st.session_state.current_scenario
            # Lấy lại text kịch bản
            text = CONFIG["giao_tiep"]["scenarios_basic"].get(sc) or CONFIG["giao_tiep"]["scenarios_extended"].get(sc, "Mình chưa rõ kịch bản này.")
            respond_bot(f"Không sao cả, mình nói lại nhé:\n\n{text}")
            st.rerun()
        if b3.button("⏹️ Dừng", use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_MAIN
            respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))
            st.rerun()


# Chat input
# Sử dụng placeholder để hiển thị Typing Indicator khi logic đang chạy
user_text = st.chat_input(CONFIG["ui"]["input_placeholder"], disabled=st.session_state.is_processing)

if user_text and not st.session_state.is_processing:
    # BẮT ĐẦU XỬ LÝ
    
    # 1. Thêm tin nhắn người dùng
    add_message("user", user_text)
    st.session_state.turns += 1

    # 2. Hiển thị Typing Indicator TẠI ĐÂY (trước khi gọi hàm block)
    # Tuy nhiên, do Streamlit hoạt động, cách tốt nhất là dùng st.spinner()
    with message_container:
         # Thêm placeholder cho hiệu ứng đang gõ
         typing_placeholder = st.empty()
         typing_placeholder.markdown(
            '<div class="bubble-row"><div class="typing"><span></span><span></span><span></span></div></div>',
            unsafe_allow_html=True
         )
         
    # 3. Lấy phản hồi BOT
    if st.session_state.chat_state == CHAT_STATE_TAM_SU_CHAT:
        mood = st.session_state.current_mood
        styles_all = sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), [])
        response_text = random.choice(styles_all)
        if st.session_state.turns >= 2:
            st.session_state.chat_state = CHAT_STATE_AWAITING_FOLLOWUP
            final_response = f"{response_text} {CONFIG['general']['follow_up_prompt']}"
        else:
            final_response = response_text
        
        # Mô phỏng thời gian chờ
        time.sleep(random.uniform(0.5, 1.5))

    elif st.session_state.chat_state in (CHAT_STATE_MAIN, CHAT_STATE_AWAITING_FOLLOWUP):
        detected = detect_mood_from_text(user_text)
        if detected:
            st.session_state.
