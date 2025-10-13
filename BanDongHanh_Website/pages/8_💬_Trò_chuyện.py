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

# --- KIỂM TRA ĐĂNG NHẬP ---
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập nhé! ❤️")
    st.stop()
    
# ========== CẤU HÌNH UI & CSS ==========
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
.quick-actions { display:flex; gap:10px; flex-wrap: wrap; margin: 10px 0 16px; }
.input-bar { position: fixed; left: 0; right: 0; bottom: 0; z-index: 999; background: #fff; border-top: 1px solid #efefef; box-shadow: 0 -2px 10px rgba(0,0,0,0.05);}
.input-inner { max-width: 820px; margin: 0 auto; padding: 15px 16px;}
</style>
""",
    unsafe_allow_html=True,
)
st.markdown("""<div class="chat-header"> <div class="chat-header-inner"> <div>💬</div> <div class="chat-title">Trò chuyện - Bạn Đồng Hành</div> </div> </div>""", unsafe_allow_html=True)

# ========== CONFIG DỮ LIỆU NỘI DUNG ==========
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

# ========== SESSION STATE ==========
if "page_state" not in st.session_state: st.session_state.page_state = "chat"
if "chat_state" not in st.session_state: st.session_state.chat_state = "main"
if "history" not in st.session_state: st.session_state.history = [{"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}]
if "turns" not in st.session_state: st.session_state.turns = 0

# ========== GEMINI AI (PHIÊN BẢN ĐÃ SỬA LỖI VÀ TỐI ƯU) ==========
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
        model = genai.GenerativeModel("gemini-pro")
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
        return random.choice(CONFIG["general"]["neutral_replies"])
    
    system_prompt = "Bạn là 'Bạn Đồng Hành', một chatbot AI thân thiện, thấu cảm và kiên nhẫn, được tạo ra để trò chuyện và hỗ trợ tinh thần cho học sinh. Hãy trả lời một cách nhẹ nhàng, tích cực và đơn giản."
    full_prompt = f"{system_prompt}\n\nNgười dùng nói: {prompt}"
    
    try:
        response = st.session_state.gemini_chat.send_message(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"Lỗi khi gọi Gemini: {e}")
        return "Xin lỗi, AI tạm thời không khả dụng."

# --- CÁC HÀM KHÁC VÀ GIAO DIỆN CHÍNH ---
# ... (Phần code còn lại của bạn giữ nguyên, không cần thay đổi) ...

# ========== 5) TTS (EDGE TTS NEURAL + FALLBACK GTTS) ==========

def synthesize_tts(text, voice, rate_pct):
    if EDGE_TTS_AVAILABLE:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            rate_str = f"{'+' if rate_pct>=0 else ''}{rate_pct}%"
            cmd = [
                "edge-tts", "--voice", voice, "--rate", rate_str, 
                "--text", text, "--write-media", temp_path
            ]
            subprocess.run(cmd, check=True, capture_output=True, text=True)
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            os.unlink(temp_path)
            return audio_data
        except Exception as e:
            print(f"Lỗi Edge TTS: {e}. Chuyển sang gTTS.")

    if GTTS_AVAILABLE:
        try:
            bio = BytesIO()
            tts = gTTS(text=text, lang="vi")
            tts.write_to_fp(bio)
            bio.seek(0)
            return bio.read()
        except Exception as e:
            print(f"Lỗi gTTS: {e}")
    
    return None

def autoplay_audio(audio_data):
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

def respond_bot(text):
    add_message("bot", text)
    if st.session_state.tts_enabled:
        # Không cần spinner ở đây vì nó có thể làm gián đoạn luồng UI
        audio = synthesize_tts(text, st.session_state.tts_voice, st.session_state.tts_rate)
        if audio:
            autoplay_audio(audio)

# ========== 7) GIAO DIỆN CHÍNH ==========

with st.sidebar:
    st.markdown("### Cài đặt giọng nói")
    st.session_state.tts_enabled = st.toggle("Đọc to phản hồi", value=st.session_state.tts_enabled)
    voice = st.selectbox(
        "Giọng đọc",
        options=["vi-VN-HoaiMyNeural (Nữ)", "vi-VN-NamMinhNeural (Nam)"],
        index=0 if "HoaiMy" in st.session_state.tts_voice else 1
    )
    st.session_state.tts_voice = "vi-VN-HoaiMyNeural" if "HoaiMy" in voice else "vi-VN-NamMinhNeural"
    rate = st.slider("Tốc độ nói (%)", -50, 50, st.session_state.tts_rate, step=5)
    st.session_state.tts_rate = rate
    
    st.divider()
    
    if st.button("🗑️ Xóa lịch sử trò chuyện"):
        st.session_state.history = [
            {"sender": "bot", "text": "Chào bạn, mình là Bạn đồng hành đây! Mình có thể giúp gì cho bạn hôm nay?"}
        ]
        if AI_ENABLED:
            st.session_state.gemini_chat = gemini_model.start_chat(history=[])
        st.success("Đã xóa lịch sử trò chuyện!")
        st.rerun()

    st.markdown("### Giới thiệu")
    st.markdown("""
    **Bạn Đồng Hành** là chatbot hỗ trợ tâm lý và kỹ năng giao tiếp cho học sinh.
    - Lắng nghe và đồng cảm
    - Hỗ trợ luyện tập giao tiếp
    - Ghi nhật ký cảm xúc
    - Hướng dẫn bài tập thư giãn
    """)
    st.markdown("Phiên bản: 1.5.0 (Đã tối ưu)")

# Main chat UI
st.markdown('<div class="chat-shell">', unsafe_allow_html=True)

# Hiển thị các tin nhắn cũ
for m in st.session_state.history:
    cls_row = "bubble-row bubble-user" if m["sender"] == "user" else "bubble-row"
    cls_msg = "msg msg-user" if m["sender"] == "user" else "msg msg-bot"
    st.markdown(
        f'<div class="{cls_row}"><div class="{cls_msg}">{html.escape(m["text"])}</div></div>',
        unsafe_allow_html=True
    )

# Quick actions và options
if st.session_state.chat_state == CHAT_STATE_MAIN:
    quick_actions_col = st.container()
    with quick_actions_col:
        st.markdown('<div class="quick-actions">', unsafe_allow_html=True)
        qa_cols = st.columns(4)
        if qa_cols[0].button("💖 Tâm sự", use_container_width=True, key="btn_tam_su"):
            st.session_state.chat_state = CHAT_STATE_TAM_SU_SELECTION
            respond_bot(CONFIG["tam_su"]["intro_message"])
            st.rerun()
        if qa_cols[1].button("🗣️ Luyện giao tiếp", use_container_width=True, key="btn_giao_tiep"):
            st.session_state.chat_state = CHAT_STATE_GIAO_TIEP_SELECTION_BASIC
            respond_bot(CONFIG["giao_tiep"]["intro_message"])
            st.rerun()
        if qa_cols[2].button("📓 Nhật ký", use_container_width=True, key="btn_journal"):
            st.session_state.page_state = STATE_JOURNAL
            st.rerun()
        if qa_cols[3].button("😌 Thư giãn", use_container_width=True, key="btn_relax"):
            st.session_state.page_state = STATE_RELAX
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ... Các options khác ...
options_container = st.container()
with options_container:
    if st.session_state.chat_state == CHAT_STATE_TAM_SU_SELECTION:
        moods = list(CONFIG["tam_su"]["moods"].keys())
        cols = st.columns(len(moods))
        for i, mood in enumerate(moods):
            if cols[i].button(mood, key=f"mood_{i}"):
                st.session_state.chat_state = CHAT_STATE_TAM_SU_CHAT
                st.session_state.current_mood = mood
                st.session_state.turns = 0
                respond_bot(CONFIG["tam_su"]["moods"][mood]["initial"])
                st.rerun()
    # ... Các elif khác cho các chat_state ... (giữ nguyên như code cũ)
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
    # ... và các states còn lại ...

# Input bar và xử lý logic
if prompt := st.chat_input(CONFIG["ui"]["input_placeholder"]):
    # 1. Thêm và hiển thị tin nhắn của người dùng ngay lập tức
    add_message("user", prompt)
    st.session_state.turns += 1
    
    # 2. Tạo ô chờ trong khi bot xử lý
    with st.chat_message("assistant"):
        st.markdown(
            '<div class="bubble-row"><div class="typing"><span></span><span></span><span></span></div></div>',
            unsafe_allow_html=True
        )
        
        # 3. Quyết định câu trả lời của bot
        response_text = ""
        if st.session_state.chat_state == CHAT_STATE_TAM_SU_CHAT:
            mood = st.session_state.current_mood
            styles_all = sum(CONFIG["tam_su"]["moods"][mood]["styles"].values(), [])
            response_text = random.choice(styles_all)
            if st.session_state.turns >= 2:
                st.session_state.chat_state = CHAT_STATE_AWAITING_FOLLOWUP
                response_text += f" {CONFIG['general']['follow_up_prompt']}"
        else:
            detected_mood = detect_mood_from_text(prompt)
            if detected_mood:
                st.session_state.chat_state = CHAT_STATE_TAM_SU_CHAT
                st.session_state.current_mood = detected_mood
                st.session_state.turns = 0
                response_text = CONFIG["tam_su"]["moods"][detected_mood]["initial"]
            else:
                # Đây là lúc gọi AI
                response_text = call_gemini(prompt)
                st.session_state.chat_state = CHAT_STATE_AWAITING_FOLLOWUP

        # 4. Gửi câu trả lời của bot
        respond_bot(response_text)
        
    # 5. Chạy lại script để hiển thị tin nhắn mới của bot
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
# ... (Giữ nguyên toàn bộ code cho render_journal_ui và render_relax_ui) ...
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

if st.session_state.page_state == STATE_JOURNAL:
    render_journal_ui()
elif st.session_state.page_state == STATE_RELAX:
    render_relax_ui()



