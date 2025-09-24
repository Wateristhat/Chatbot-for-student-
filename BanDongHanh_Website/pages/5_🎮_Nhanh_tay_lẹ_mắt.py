import streamlit as st
from gtts import gTTS
from io import BytesIO

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
            st.audio(audio_data, format="audio/mp3")

# --- GIAO DIỆN ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='color: #2E8B57; font-size: 2.7rem;'>
            🐝 Bee Bay Cùng Bạn!
        </h1>
        <h2 style='color: #4169E1; font-size: 1.7rem;'>🎮 Vượt Chướng Ngại Vật</h2>
        <div style='margin-top:8px; color:#444; font-size:1.1rem;'>Điều khiển bằng phím <b>SPACE</b> hoặc chạm màn hình điện thoại</div>
    </div>
""", unsafe_allow_html=True)

# --- Nút TTS hướng dẫn ---
instructions_text = """
Chào bạn! Đây là trò chơi Bee Bay Cùng Bạn - Vượt Chướng Ngại Vật.
Mục tiêu là giúp ong Bee bay qua các quả bóng mà không va chạm.
Bạn hãy dùng phím SPACE để ong nhảy lên cao, hoặc chạm vào màn hình nếu dùng điện thoại.
Chúc bạn chơi vui và luôn tự tin!
"""
col1, col2, col3 = st.columns([1,1,1])
with col2:
    create_tts_button(instructions_text, "game_instructions", "🔊 Nghe hướng dẫn")

st.write("---")

# --- NHÚNG GAME HTML5 ---
game_url = "https://wateristhat.github.io/Chatbot-for-student-/BanDongHanh_Website/game.html"  # Đường dẫn game của bạn

st.components.v1.html(
    f"""
    <iframe src="{game_url}" width="100%" height="600" frameborder="0" scrolling="no" style="border-radius: 15px; background: #F9F9FF;"></iframe>
    """,
    height=620
)

st.info("👉 Nhấn phím SPACE (trên máy tính) hoặc chạm vào màn hình (điện thoại) để ong Bee bay qua chướng ngại vật!")

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
with st.expander("🎯 Mẹo chơi game cho học sinh hòa nhập", expanded=False):
    tips = """
    1. **Thở sâu, thư giãn trước khi chơi.**
    2. **Dùng SPACE hoặc chạm màn hình để điều khiển ong Bee nhảy qua bóng.**
    3. **Đừng lo nếu chưa đạt điểm cao, mỗi lần chơi là một cơ hội học hỏi.**
    4. **Nếu thấy mệt, hãy nghỉ ngơi rồi chơi lại sau nhé.**
    5. **Hãy chia sẻ niềm vui và thành tích của mình với bạn bè, thầy cô!**
    """
    st.markdown(tips)

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

# --- CSS làm đẹp thêm (không ảnh hưởng game) ---
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
