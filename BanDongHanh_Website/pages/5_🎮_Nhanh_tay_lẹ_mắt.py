import streamlit as st
from gtts import gTTS
from io import BytesIO
import os

st.set_page_config(page_title="🐝 Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt", page_icon="🎮", layout="centered")

# --- TTS FUNCTION ---
@st.cache_data
def text_to_speech(text):
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Lỗi tạo âm thanh: {e}")
        return None

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    if st.button(button_text, key=f"tts_{key_suffix}"):
        audio_data = text_to_speech(text)
        if audio_data:
            st.audio(audio_data, format="audio/mpeg")

# --- HƯỚNG DẪN & ĐỘNG VIÊN ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='color: #2E8B57; font-size: 2.7rem;'>
            🐝 Bee Bay Cùng Bạn!
        </h1>
        <h2 style='color: #4169E1; font-size: 1.7rem;'>🎮 Nhanh Tay Lẹ Mắt</h2>
        <div style='margin-top:8px; color:#444; font-size:1.1rem;'>Điều khiển bằng phím <b>SPACE</b> hoặc chạm màn hình điện thoại</div>
    </div>
""", unsafe_allow_html=True)

instructions_text = """
Chào bạn! Đây là trò chơi Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt.
Mục tiêu là giúp ong Bee bay qua các quả bóng mà không va chạm.
Bạn hãy dùng phím SPACE để ong nhảy lên cao, hoặc chạm vào màn hình nếu dùng điện thoại.
Chúc bạn chơi vui và luôn tự tin!
"""
col1, col2, col3 = st.columns([1,1,1])
with col2:
    create_tts_button(instructions_text, "game_instructions", "🔊 Nghe hướng dẫn")

st.write("---")

# --- GAME HTML NHÚNG TRỰC TIẾP ---
game_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.html")
try:
    with open(game_file_path, "r", encoding="utf-8") as file:
        game_html_content = file.read()
    
    # --- 1. ĐOẠN CODE SỬA LỖI MÀN HÌNH BỊ CẮT ---
    # Tiêm CSS vào file HTML để ép game co lại vừa màn hình
    game_responsive_css = """
    <style>
        body, html {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden; /* Ẩn thanh cuộn của game */
        }
        /* Nhắm vào thẻ canvas của game (thẻ vẽ game) */
        canvas {
            width: 100% !important;     /* Ép canvas vừa 100% màn hình */
            max-width: 100vw !important;
            height: auto !important;     /* Tự động chỉnh chiều cao */
            object-fit: contain; 
        }
    </style>
    """
    # Thêm CSS vào đầu file game
    game_html_content_fixed = game_responsive_css + game_html_content
    # --- KẾT THÚC ĐOẠN CODE SỬA LỖI ---

    # --- 2. SỬA LỖI CHIỀU CAO GAME ---
    # Giảm chiều cao (height) từ 1200 xuống 600 để vừa màn hình điện thoại
    st.components.v1.html(game_html_content_fixed, height=1200, scrolling=False) 
    st.info("👉 Nhấn phím SPACE (máy tính) hoặc chạm vào màn hình (điện thoại) để chơi game!")
except Exception as e:
    st.error(f"Không thể tải game. Kiểm tra file game.html. Chi tiết lỗi: {e}")

# --- ĐỘNG VIÊN KHI CHƠI GAME ---
st.write("---")
encouragement_text = """
Bee rất tự hào về sự cố gắng của bạn!
Dù điểm số thế nào, mỗi lần chơi là một lần bạn tiến bộ hơn.
Hãy thư giãn, tận hưởng trò chơi và luôn tự tin nhé!
"""
st.markdown(
    """
    <div style='
        background: linear-gradient(135deg, #FFE4B5, #F0E68C);
        border-radius: 18px;
        padding: 16px;
        margin: 18px 0;
        border: 2px solid #DAA520;
        text-align: center;
        font-size: 1.18rem;
    '>
        💝 Bee: Chơi game không chỉ để giành chiến thắng, mà còn để học hỏi và vui vẻ! <br>
        Mỗi lần thử là một bước tiến, mỗi điểm số là một thành tựu nhỏ.<br>
        Bee rất tự hào về sự cố gắng của bạn! 🐝💕
    </div>
    """, unsafe_allow_html=True
)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    create_tts_button(encouragement_text, "encouragement", "🔊 Nghe lời động viên")

# --- MẸO CHƠI GAME ---
with st.expander("🎯 Mẹo chơi game dành cho bạn", expanded=False):
    tips = """
    1. Thở sâu, thư giãn trước khi chơi.
    2. Dùng SPACE hoặc chạm màn hình để điều khiển ong Bee nhảy qua bóng.
    3. Đừng lo nếu chưa đạt điểm cao, mỗi lần chơi là một cơ hội học hỏi.
    4. Nếu thấy mệt, hãy nghỉ ngơi rồi chơi lại sau nhé.
    5. Hãy chia sẻ niềm vui và thành tích của mình với bạn bè, thầy cô!
    """
    st.markdown(tips)
    tips_tts = "Mẹo chơi game dành cho bạn. Một, thở sâu và thư giãn trước khi chơi. Hai, dùng phím SPACE hoặc chạm màn hình để điều khiển ong Bee nhảy qua bóng. Ba, đừng lo nếu chưa đạt điểm cao, mỗi lần chơi là một cơ hội học hỏi. Bốn, nếu thấy mệt hãy nghỉ ngơi rồi chơi lại sau nhé. Năm, hãy chia sẻ niềm vui và thành tích của mình với bạn bè, thầy cô!"
    create_tts_button(tips_tts, "tips", "🔊 Nghe mẹo chơi game")

# --- Nút quay về trang chủ ---
st.markdown(
    """
    <div style='text-align: center; margin-top: 24px;'>
        <a href='0_💖_Trang_chủ.py' style='
            display: inline-block;
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 18px;
            font-size: 1.15rem;
            font-weight: bold;
            margin-top: 20px;
        '>⬅️ 🏠 Quay về Trang chủ</a>
    </div>
    """, unsafe_allow_html=True
)

# --- CSS làm đẹp thêm ---
st.markdown("""
    <style>
        .stButton > button {
            background: linear-gradient(135deg, #9370DB, #8A2BE2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            font-weight: bold;
            transition: transform 0.2s ease;
        }
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }
        .stExpander > div > div > div > div {
            background: linear-gradient(135deg, #F0F8FF, #E6E6FA);
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)
