import streamlit as st
from gtts import gTTS
from io import BytesIO
import os
import style # <-- 1. IMPORT STYLE
import tempfile # <-- 2. THÊM TEMPFILE ĐỂ SỬA LỖI ÂM THANH

# --- 3. SỬA LỖI CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="🐝 Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt", 
    page_icon="🎮", 
    layout="centered",
    initial_sidebar_state="collapsed" # <-- Thêm dòng này
)

# --- 4. ÁP DỤNG CSS CHUNG ---
style.apply_global_style()

# --- 5. SỬA LỖI ÂM THANH (DÙNG TEMPFILE) ---
@st.cache_data
def generate_audio_data(text):
    """Tạo file âm thanh (dùng tempfile) và trả về data."""
    if not text or not text.strip():
        return None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            temp_path = tmp_file.name
        
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.save(temp_path)
        
        with open(temp_path, 'rb') as f:
            audio_data = f.read()
        
        os.unlink(temp_path) # Xóa file tạm
        return audio_data
    except Exception as e:
        st.error(f"Lỗi tạo file âm thanh: {e}")
        return None

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    if st.button(button_text, key=f"tts_{key_suffix}"):
        audio_data = generate_audio_data(text) # Dùng hàm mới
        if audio_data:
            st.audio(audio_data, format="audio/mp3") # <-- Xóa autoplay

# --- HƯỚNG DẪN & ĐỘNG VIÊN ---
st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 class='game-title'>
            🐝 Bee Bay Cùng Bạn!
        </h1>
        <h2 class'game-subtitle'>🎮 Nhanh Tay Lẹ Mắt</h2>
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

    # --- 7. SỬA LỖI GAME BỊ CẮT (ÉP GAME CO LẠI) ---
    # Tiêm CSS vào file HTML để ép game co lại vừa màn hình
    game_responsive_css = """
    <style>
        body, html {
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden; /* Ẩn thanh cuộn của game */
        }
        /* Nhắm vào thẻ canvas của game */
        canvas {
            width: 100% !important;
            max-width: 100vw !important; /* Vừa 100% màn hình */
            height: auto !important;     /* Tự động chỉnh chiều cao */
            object-fit: contain; 
        }
    </style>
    """
    # Thêm CSS vào đầu file game
    game_html_content = game_responsive_css + game_html_content
    
    # Giảm chiều cao (height) để vừa màn hình điện thoại
    st.components.v1.html(game_html_content, height=600, scrolling=False)
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
    <div class='encouragement-box' style='
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
    tips_tts = "Mẹo chơi game dành cho bạn..." # (Rút gọn)
    create_tts_button(tips_tts, "tips", "🔊 Nghe mẹo chơi game")

# --- 8. SỬA LỖI LINK QUAY VỀ TRANG CHỦ ---
st.write("---")
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ 🏠 Quay về Trang chủ", icon="🏠")

# --- 9. XÓA CSS CỤC BỘ GÂY XUNG ĐỘT ---
# (Toàn bộ khối st.markdown(""" <style> .stButton > button { ... } ... </style> """)
#  ở cuối file đã bị xóa để dùng style.py chung)
