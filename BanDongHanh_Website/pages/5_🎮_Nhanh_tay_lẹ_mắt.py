import streamlit as st
from gtts import gTTS
from io import BytesIO
import os
import style # <-- 1. IMPORT STYLE

st.set_page_config(
    page_title="🐝 Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt", 
    page_icon="🎮", 
    layout="centered",
    initial_sidebar_state="collapsed" # <-- 2. ẨN SIDEBAR BAN ĐẦU
)

# --- 3. ÁP DỤNG CSS CHUNG ---
style.apply_global_style()


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
            st.audio(audio_data, format="audio/mp3", autoplay=True) # Thêm autoplay

# --- HƯỚNG DẪN & ĐỘNG VIÊN ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 class='game-title'>
            🐝 Bee Bay Cùng Bạn!
        </h1>
        <h2 class='game-subtitle'>🎮 Nhanh Tay Lẹ Mắt</h2>
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
# Logic của bạn: file game.html nằm ở thư mục gốc (cùng 0_Trang_chu.py)
game_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.html")
try:
    with open(game_file_path, "r", encoding="utf-8") as file:
        game_html_content = file.read()
    st.components.v1.html(game_html_content, height=1200, scrolling=False)
    st.info("👉 Nhấn phím SPACE (máy tính) hoặc chạm vào màn hình (điện thoại) để chơi game!")
except Exception as e:
    st.error(f"Không thể tải game. Kiểm tra file game.html trong thư mục BanDongHanh_Website. Chi tiết lỗi: {e}")

# --- ĐỘNG VIÊN KHI CHƠI GAME ---
st.write("---")
encouragement_text = """
Bee rất tự hào về sự cố gắng của bạn!
Dù điểm số thế nào, mỗi lần chơi là một lần bạn tiến bộ hơn.
Hãy thư giãn, tận hưởng trò chơi và luôn tự tin nhé!
"""
st.markdown(
    """
    <div class='encouragement-box'>
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

# --- 4. CẬP NHẬT NÚT QUAY VỀ TRANG CHỦ ---
st.write("---")
st.page_link("0_💖_Trang_chủ.py", label="⬅️ 🏠 Quay về Trang chủ", icon="🏠")


# --- 5. CSS RESPONSIVE & XÓA CSS BUTTON CỤC BỘ ---
st.markdown("""
    <style>
        /* CSS cho các hộp tùy chỉnh */
        .encouragement-box {
            background: linear-gradient(135deg, #FFE4B5, #F0E68C);
            border-radius: 18px;
            padding: 16px;
            margin: 18px 0;
            border: 2px solid #DAA520;
            text-align: center;
            font-size: 1.18rem;
        }
        .game-title {
            color: #2E8B57; 
            font-size: 2.7rem;
        }
        .game-subtitle {
            color: #4169E1; 
            font-size: 1.7rem;
        }
        
        /* CSS cho expander */
        .stExpander > div > div > div > div {
            background: linear-gradient(135deg, #F0F8FF, #E6E6FA);
            border-radius: 10px;
        }
        
        /* --- CSS CHO ĐIỆN THOẠI --- */
        @media (max-width: 900px) {
            .game-title {
                font-size: 2rem; /* Thu nhỏ tiêu đề */
            }
            .game-subtitle {
                font-size: 1.3rem; /* Thu nhỏ tiêu đề phụ */
            }
            .encouragement-box {
                font-size: 1rem; /* Thu nhỏ chữ */
                padding: 12px;
            }
        }
        
        /* --- KHỐI CSS BUTTON CỤC BỘ ĐÃ BỊ XÓA --- */
        /* (Phần .stButton > button { ... } đã bị xóa
           để file style.py chung quản lý) */
           
    </style>
""", unsafe_allow_html=True)
