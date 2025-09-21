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

# Optional: Gemini
try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except Exception:
    GENAI_AVAILABLE = False

# Fallback TTS
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False

# Preferred neural TTS (Microsoft Edge TTS)
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except Exception:
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
.chat-shell { max-width: 820px; margin: 0 auto; padding-top: 64px; padding-bottom: 120px; }

/* Header sticky giống app shopping */
.chat-header {
  position: fixed; top: 0; left: 0; right: 0; z-index: 999;
  background: #fff; border-bottom: 1px solid #efefef;
}
.chat-header-inner {
  max-width: 820px; margin: 0 auto; padding: 12px 16px;
  display: flex; align-items: center; gap: 12px;
}
.chat-title { font-weight: 700; font-size: 1.05rem; }

/* Bubbles */
.bubble-row { display:flex; margin: 8px 0; }
.bubble-user { justify-content: flex-end; }
.msg {
  border-radius: 18px; padding: 10px 14px; max-width: 70%;
  font-size: 1rem; line-height: 1.5; word-wrap: break-word;
}
.msg-user { background: #DCF8C6; color: #101010; border-top-right-radius: 6px; }
.msg-bot  { background: #F3F4F6; color: #111; border-top-left-radius: 6px; }

/* Typing indicator */
.typing { display:inline-block; }
.typing span {
  height: 8px; width: 8px; margin: 0 2px; background-color: #9E9E9E;
  display: inline-block; border-radius: 50%; opacity: 0.5; animation: bob 1s infinite;
}
@keyframes bob { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
.typing span:nth-child(1){animation-delay:-0.3s} .typing span:nth-child(2){animation-delay:-0.15s}

/* Quick actions (chips) */
.quick-actions { display:flex; gap:8px; flex-wrap: wrap; margin: 6px 0 12px; }
.quick-actions .chip {
  border: 1px solid #0084FF; color: #0084FF; background:#E7F3FF;
  border-radius: 16px; padding: 6px 10px; font-size: 0.9rem; cursor: pointer;
}
.quick-actions .chip:hover { background:#0084FF; color:#fff; }

/* Sticky input */
.input-bar {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 999;
  background: #fff; border-top: 1px solid #efefef;
}
.input-inner {
  max-width: 820px; margin: 0 auto; padding: 10px 12px;
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
    <div>🛍️</div>
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
            "input_placeholder": "Nhập tin nhắn…",
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
                "👋 Chào hỏi bạn bè": "Bạn có thể nói: “Chào bạn, hôm nay vui không?”",
                "🙋 Hỏi bài thầy cô": "Bạn thử hỏi: “Thầy/cô ơi, phần này em chưa rõ ạ?”"
            },
            "scenarios_extended": {
                "📚 Nhờ bạn giúp đỡ": "Bạn thử nói: “Cậu chỉ mình chỗ này với được không?”",
            },
        },
        "general": {
            "neutral_replies": [
                "Mình chưa rõ lắm, bạn nói cụ thể hơn được không?",
                "Mình đang nghe bạn nè, bạn muốn nói thêm điều gì không?"
            ],
            "follow_up_prompt": "Bạn muốn tiếp tục tâm sự hay luyện nói chuyện trong lớp nè?",
            "end_chat_replies": [
                "Cảm ơn bạn đã chia sẻ với mình hôm nay nha. Mình luôn sẵn sàng khi bạn cần 💖",
                "Bạn đã làm rất tốt khi bộc lộ cảm xúc. Khi nào cần, mình vẫn ở đây ✨"
            ],
        },
    }

CONFIG = get_config()

# Gemini optional
AI_ENABLED = False
if GENAI_AVAILABLE:
    try:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        AI_ENABLED = True
    except Exception as e:
        print(f"Lỗi cấu hình Gemini: {e}")


# ========== 3) SESSION STATE ==========

if "page_state" not in st.session_state:
    st.session_state.page_state = STATE_CHAT
    st.session_state.chat_state = CHAT_STATE_MAIN
    st.session_state.history = [
        {"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}
    ]
    st.session_state.turns = 0
    st.session_state.current_mood = None
    st.session_state.current_scenario = None
    st.session_state.user_input_buffer = ""  # dùng với chat_input

# Voice settings defaults
if "tts_enabled" not in st.session_state:
    st.session_state.tts_enabled = True
if "tts_voice" not in st.session_state:
    st.session_state.tts_voice = "vi-VN-HoaiMyNeural"  # nữ
if "tts_rate" not in st.session_state:
    st.session_state.tts_rate = 0  # %

# ========== 4) TTS (EDGE TTS NEURAL + FALLBACK GTTS) ==========

@st.cache_data(show_spinner=False)
def gtts_bytes(text: str):
    if not GTTS_AVAILABLE:
        return None
    try:
        bio = BytesIO()
        tts = gTTS(text=text, lang="vi")
        tts.write_to_fp(bio)
        bio.seek(0)
        return bio.read()
    except Exception as e:
        print("Lỗi gTTS:", e)
        return None

async def _edge_tts_bytes_async(text: str, voice: str, rate_pct: int):
    if not EDGE_TTS_AVAILABLE:
        return None
    try:
        # rate like "+0%", "-10%", "+10%"
        rate_str = f"{'+' if rate_pct>=0 else ''}{rate_pct}%"
        communicate = edge_tts.Communicate(text, voice=voice, rate=rate_str)
        audio = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio += chunk["data"]
        return audio
    except Exception as e:
        print("Lỗi Edge TTS:", e)
        return None

@st.cache_data(show_spinner=False)
def edge_tts_bytes(text: str, voice: str, rate_pct: int):
    try:
        return asyncio.run(_edge_tts_bytes_async(text, voice, rate_pct))
    except RuntimeError:
        # In case event loop is already running (Streamlit quirk)
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(_edge_tts_bytes_async(text, voice, rate_pct))
        finally:
            loop.close()
    except Exception as e:
        print("Lỗi chạy Edge TTS:", e)
        return None

def synthesize_tts(text: str, voice: str, rate_pct: int):
    # Prefer Edge TTS neural
    if EDGE_TTS_AVAILABLE:
        audio = edge_tts_bytes(text, voice, rate_pct)
        if audio:
            return audio
    # Fallback gTTS
    return gtts_bytes(text)

def autoplay_audio(audio_data: bytes):
    try:
        b64 = base64.b64encode(audio_data).decode()
        md = f"""
        <audio autoplay="true">
          <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.components.v1.html(md, height=0)
    except Exception as e:
        print("Lỗi phát âm thanh:", e)


# ========== 5) LOGIC CHAT & AI ==========

def add_message(sender, text):
    st.session_state.history.append({"sender": sender, "text": text})

def detect_mood_from_text(text):
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

def call_gemini(prompt: str) -> str:
    if not AI_ENABLED:
        return random.choice(CONFIG["general"]["neutral_replies"])
    try:
        contextual = (
            "Hãy trả lời như một người bạn đồng hành AI thân thiện, kiên nhẫn và thấu hiểu dành cho học sinh."
            " Trả lời bằng tiếng Việt, ngắn gọn và giàu đồng cảm.\n\n"
            f"Câu hỏi/Chia sẻ của người dùng: '{prompt}'"
        )
        resp = gemini_model.generate_content(contextual)
        return resp.text or random.choice(CONFIG["general"]["neutral_replies"])
    except Exception as e:
        return f"Xin lỗi, hệ thống đang bận. Bạn thử lại sau nhé. (Chi tiết: {e})"

def respond_bot(text: str):
    # Add bot message with typing effect
    with st.container():
        # Synthesize voice if enabled
        if st.session_state.tts_enabled:
            audio = synthesize_tts(text, st.session_state.tts_voice, st.session_state.tts_rate)
            if audio:
                autoplay_audio(audio)

    add_message("bot", text)

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

# Shell for chat
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

# Quick action chips (giống app mua sắm có gợi ý thao tác)
quick_actions_col = st.container()
with quick_actions_col:
    st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
    qa_cols = st.columns(4)
    with qa_cols[0]:
        if st.button("💖 Tâm sự", use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_TAM_SU_SELECTION
            respond_bot(CONFIG["tam_su"]["intro_message"])
    with qa_cols[1]:
        if st.button("🗣️ Luyện giao tiếp", use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_BASIC
            respond_bot(CONFIG["giao_tiep"]["intro_message"])
    with qa_cols[2]:
        if st.button("📓 Nhật ký", use_container_width=True):
            st.session_state.page_state = STATE_JOURNAL
    with qa_cols[3]:
        if st.button("😌 Thư giãn", use_container_width=True):
            st.session_state.page_state = STATE_RELAX
    st.markdown('</div>', unsafe_allow_html=True)

# Message history
for m in st.session_state.history:
    cls_row = "bubble-row bubble-user" if m["sender"] == "user" else "bubble-row"
    cls_msg = "msg msg-user" if m["sender"] == "user" else "msg msg-bot"
    st.markdown(
        f'<div class="{cls_row}"><div class="{cls_msg}">{html.escape(m["text"])}</div></div>',
        unsafe_allow_html=True
    )

# Suggested quick replies based on state (like shopping chat hints)
if st.session_state.chat_state == CHAT_STATE_TAM_SU_SELECTION:
    moods = list(CONFIG["tam_su"]["moods"].keys())
    st.caption("Gợi ý cảm xúc:")
    cols = st.columns(len(moods))
    for i, mood in enumerate(moods):
        if cols[i].button(mood):
            st.session_state.chat_state = CHAT_STATE_TAM_SU_CHAT
            st.session_state.current_mood = mood
            st.session_state.turns = 0
            respond_bot(CONFIG["tam_su"]["moods"][mood]["initial"])

elif st.session_state.chat_state == CHAT_STATE_TAM_SU_CHAT:
    col1, col2 = st.columns(2)
    if col1.button(CONFIG["tam_su"]["positive_affirmation_trigger"], use_container_width=True):
        affirm = random.choice(CONFIG["tam_su"]["positive_affirmations"])
        st.session_state.chat_state = CHAT_STATE_MAIN
        respond_bot(affirm)
    if col2.button("🏁 Kết thúc", use_container_width=True):
        st.session_state.chat_state = CHAT_STATE_MAIN
        respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))

elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_SELECTION_BASIC:
    st.caption("Tình huống cơ bản:")
    for scenario in CONFIG["giao_tiep"]["scenarios_basic"].keys():
        if st.button(scenario, use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_PRACTICE
            st.session_state.current_scenario = scenario
            respond_bot(CONFIG["giao_tiep"]["scenarios_basic"][scenario])

elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED:
    st.caption("Tình huống nâng cao:")
    for scenario in CONFIG["giao_tiep"]["scenarios_extended"].keys():
        if st.button(scenario, use_container_width=True):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_PRACTICE
            st.session_state.current_scenario = scenario
            respond_bot(CONFIG["giao_tiep"]["scenarios_extended"][scenario])

elif st.session_state.chat_state == CHAT_STATE_GIAO_TIEP_PRACTICE:
    b1, b2, b3 = st.columns(3)
    if b1.button(CONFIG["giao_tiep"]["confirm_buttons"]["understood"], use_container_width=True):
        st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_EXTENDED
        respond_bot("Tuyệt vời! Cùng xem các tình huống mở rộng nhé!")
    if b2.button(CONFIG["giao_tiep"]["confirm_buttons"]["not_understood"], use_container_width=True):
        sc = st.session_state.current_scenario
        text = CONFIG["giao_tiep"]["scenarios_basic"].get(sc) or CONFIG["giao_tiep"]["scenarios_extended"].get(sc, "")
        respond_bot(f"Không sao cả, mình nói lại nhé:\n\n{text}")
    if b3.button("⏹️ Dừng", use_container_width=True):
        st.session_state.chat_state = CHAT_STATE_MAIN
        respond_bot(random.choice(CONFIG["general"]["end_chat_replies"]))


# Chat input (modern, like shopping apps)
user_text = st.chat_input(CONFIG["ui"]["input_placeholder"])
if user_text:
    # Add user message
    add_message("user", user_text)
    st.session_state.turns += 1

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

# Close shell
st.markdown('</div>', unsafe_allow_html=True)

# Sticky input bar wrapper (purely visual; st.chat_input is already bottom-fixed by app flow)
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


# ========== 7) ROUTER NỘI BỘ: NHẬT KÝ & THƯ GIÃN ==========

def render_journal_ui():
    st.title("📓 Nhật Ký Cảm Xúc")
    MOOD_FILE = "mood_journal.csv"
    MOOD_OPTIONS = ["😄 Vui", "😔 Buồn", "😠 Tức giận", "😴 Mệt mỏi", "😐 Bình thường"]

    def load_mood_data():
        if os.path.exists(MOOD_FILE):
            try:
                return pd.read_csv(MOOD_FILE)
            except pd.errors.EmptyDataError:
                pass
        return pd.DataFrame(columns=["Ngày", "Cảm xúc", "Ghi chú"])

    journal_df = load_mood_data()
    st.header("Hôm nay bạn cảm thấy thế nào?")
    log_date = st.date_input("Chọn ngày", datetime.now())
    selected_mood = st.selectbox("Chọn cảm xúc", MOOD_OPTIONS)
    note = st.text_input("Ghi chú thêm?")
    if st.button("Lưu lại cảm xúc"):
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
                st.success("Đã lưu!")
                st.rerun()
        else:
            journal_df = new_entry
            journal_df.to_csv(MOOD_FILE, index=False)
            st.success("Đã lưu!")
            st.rerun()

    st.header("Lịch sử cảm xúc")
    if not journal_df.empty:
        st.dataframe(journal_df.sort_values(by="Ngày", ascending=False), use_container_width=True)
        st.header("Thống kê nhanh")
        st.bar_chart(journal_df["Cảm xúc"].value_counts())
    else:
        st.info("Nhật ký của bạn còn trống.")

    if st.button("⬅️ Quay lại trò chuyện"):
        st.session_state.page_state = STATE_CHAT
        st.rerun()

def render_relax_ui():
    st.title("😌 Góc Thư Giãn")
    st.write("Hít thở sâu, lắng nghe âm thanh nhẹ nhàng.")
    st.header("Bài tập hít thở hộp (4-4-4-4)")
    if st.button("Bắt đầu hít thở"):
        placeholder = st.empty()
        for i in range(3):
            placeholder.info("Chuẩn bị..."); time.sleep(1)
        steps = [("Hít vào bằng mũi", 4), ("Giữ hơi", 4), ("Thở ra bằng miệng", 4), ("Nghỉ", 4)]
        for title, sec in steps:
            placeholder.success(f"{title} ({sec}s)"); time.sleep(sec)
        placeholder.success("Hoàn thành! Bạn thấy tốt hơn chứ?")

    st.header("Âm thanh thiên nhiên")
    col1, col2, col3 = st.columns(3)
    with col1: st.video("https://www.youtube.com/watch?v=eKFTSSKCzWA")
    with col2: st.video("https://www.youtube.com/watch?v=gM_r4c6i25s")
    with col3: st.video("https://www.youtube.com/watch?v=aIIEI33EUqI")

    if st.button("⬅️ Quay lại trò chuyện"):
        st.session_state.page_state = STATE_CHAT
        st.rerun()

# Router nội bộ
if st.session_state.page_state == STATE_JOURNAL:
    render_journal_ui()
elif st.session_state.page_state == STATE_RELAX:
    render_relax_ui()
# STATE_CHAT hiển thị ở trên
