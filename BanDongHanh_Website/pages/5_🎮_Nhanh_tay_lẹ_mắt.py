import streamlit as st
import os
import sys
from gtts import gTTS
from io import BytesIO

# Add path for database import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from database import add_mood_entry
except ImportError:
    pass

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="🐝 Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt", page_icon="🎮", layout="centered")

# --- HÀM TEXT-TO-SPEECH ---
@st.cache_data
def text_to_speech(text):
    """Chuyển văn bản thành giọng nói."""
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        st.error(f"Lỗi tạo âm thanh: {e}")
        return None

# --- HÀM TẠO NÚT ĐỌC TO ---
def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    """Tạo nút đọc to cho văn bản."""
    if st.button(button_text, key=f"tts_{key_suffix}", help="Nhấn để nghe hướng dẫn"):
        # Kiểm tra text đầu vào
        if not text or not text.strip():
            st.info("💭 Chưa có nội dung để đọc. Hãy thử lại khi có văn bản!")
            return
        
        with st.spinner("Đang chuẩn bị âm thanh..."):
            audio_data = text_to_speech(text)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
            else:
                st.info("🎵 Hiện tại không thể tạo âm thanh. Bạn có thể đọc nội dung ở trên nhé!")

# --- GIAO DIỆN CHÍNH ---
st.markdown(
    """
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='color: #2E8B57; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);'>
            🐝 Bee Bay Cùng Bạn!
        </h1>
        <h2 style='color: #4169E1; font-size: 2rem;'>🎮 Nhanh Tay Lẹ Mắt</h2>
    </div>
    """, unsafe_allow_html=True
)

# Nút quay về trang chủ với style đẹp hơn
st.markdown(
    """
    <div style='text-align: center; margin: 20px 0;'>
        <a href='0_💖_Trang_chủ.py' style='
            display: inline-block;
            background: linear-gradient(135deg, #FF6B6B, #4ECDC4);
            color: white;
            text-decoration: none;
            padding: 12px 24px;
            border-radius: 25px;
            font-size: 1.2rem;
            font-weight: bold;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s ease;
        '>⬅️ 🏠 Quay về Trang chủ</a>
    </div>
    """, unsafe_allow_html=True
)

# Hướng dẫn chi tiết với TTS
st.markdown(
    """
    <div style='
        background: linear-gradient(135deg, #E6E6FA, #F0F8FF);
        border-radius: 20px;
        padding: 25px;
        margin: 20px 0;
        border: 3px solid #9370DB;
        font-size: 1.3rem;
        line-height: 1.8;
    '>
        <div style='text-align: center; margin-bottom: 20px;'>
            <span style='font-size: 2rem;'>🐝✨</span>
            <strong style='color: #4169E1; font-size: 1.5rem;'> Hướng dẫn chơi game </strong>
            <span style='font-size: 2rem;'>✨🎈</span>
        </div>
        
        <div style='color: #2E8B57;'>
            <p><strong>🎯 Mục tiêu:</strong> Giúp Bee bay qua các quả bóng bay màu sắc!</p>
            
            <p><strong>🎮 Cách chơi:</strong></p>
            <ul>
                <li>Nhấn phím <span style='background: #4169E1; color: white; padding: 5px 10px; border-radius: 8px; font-weight: bold;'>SPACE</span> để Bee nhảy lên cao</li>
                <li>Tránh chạm vào các quả bóng bay đáng yêu 🎈</li>
                <li>Thu thập điểm số mỗi khi vượt qua chướng ngại vật</li>
            </ul>
            
            <p><strong>🌟 Chế độ chơi:</strong></p>
            <ul>
                <li><strong>Siêu Dễ:</strong> Tốc độ chậm, ít chướng ngại vật - phù hợp với bạn mới bắt đầu</li>
                <li><strong>Bình Thường:</strong> Thử thách hơn một chút khi bạn đã quen</li>
            </ul>
            
            <p style='text-align: center; font-size: 1.4rem; color: #FF1493;'>
                <strong>💖 Hãy thư giãn và tận hưởng nhé! Bee luôn ủng hộ bạn! 🌈</strong>
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# Nút TTS cho hướng dẫn
instructions_text = """
Chào bạn! Đây là trò chơi Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt. 
Mục tiêu của bạn là giúp chú ong Bee bay qua các quả bóng bay màu sắc bằng cách nhấn phím SPACE để nhảy lên cao.
Có hai chế độ chơi: Siêu Dễ với tốc độ chậm phù hợp cho người mới, và Bình Thường thử thách hơn.
Hãy thư giãn và tận hưởng trò chơi nhé! Bee luôn ủng hộ bạn!
"""

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    create_tts_button(instructions_text, "game_instructions", "🔊 Nghe hướng dẫn")

st.write("---")

# --- NHÚNG GAME HTML5 CẢI TIẾN ---
# Đường dẫn đến file game.html
game_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game.html")

try:
    # Đọc nội dung file game.html và nhúng trực tiếp
    with open(game_file_path, "r", encoding="utf-8") as file:
        game_html_content = file.read()
    
    # Hiển thị game với kích thước lớn hơn
    st.components.v1.html(game_html_content, height=650, scrolling=False)
    
except FileNotFoundError:
    st.error("Không tìm thấy file game.html. Vui lòng kiểm tra lại đường dẫn file.")
    st.info("File game.html cần được đặt trong thư mục BanDongHanh_Website.")
except Exception as e:
    st.error(f"Có lỗi xảy ra khi tải game: {str(e)}")
    
    # Fallback: Hiển thị iframe với GitHub Pages URL (nếu được bật)
    st.info("Đang thử tải game từ GitHub Pages...")
    game_url = "https://wateristhat.github.io/Chatbot-for-student-/BanDongHanh_Website/game.html"
    game_html = f"""
    <iframe src="{game_url}" width="100%" height="600" frameborder="0" scrolling="no" style="border-radius: 15px;"></iframe>
    """
    st.components.v1.html(game_html, height=620)

# --- PHẦN ĐỘNG VIÊN VÀ HỖ TRỢ ---
st.markdown("---")

st.markdown(
    """
    <div style='
        background: linear-gradient(135deg, #FFE4B5, #F0E68C);
        border-radius: 20px;
        padding: 20px;
        margin: 20px 0;
        border: 3px solid #DAA520;
        text-align: center;
    '>
        <h3 style='color: #8B4513; margin-bottom: 15px;'>💝 Lời nhắn từ Bee</h3>
        <p style='font-size: 1.2rem; color: #2F4F4F; line-height: 1.6;'>
            Chơi game không chỉ để giành chiến thắng, mà còn để học hỏi và vui vẻ! 🌟<br>
            Mỗi lần thử là một bước tiến, mỗi điểm số là một thành tựu nhỏ.<br>
            Bee rất tự hào về sự cố gắng của bạn! 🐝💕
        </p>
    </div>
    """, unsafe_allow_html=True
)

# Nút TTS cho lời động viên
encouragement_text = """
Chơi game không chỉ để giành chiến thắng, mà còn để học hỏi và vui vẻ! 
Mỗi lần thử là một bước tiến, mỗi điểm số là một thành tựu nhỏ.
Bee rất tự hào về sự cố gắng của bạn!
"""

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    create_tts_button(encouragement_text, "encouragement", "🔊 Nghe lời động viên")

# --- MẸO CHƠI GAME ---
with st.expander("🎯 Mẹo chơi game hiệu quả", expanded=False):
    st.markdown(
        """
        <div style='font-size: 1.1rem; line-height: 1.7;'>
            <ul>
                <li><strong>🧘 Thư giãn:</strong> Đừng căng thẳng, hãy thở sâu và thư giãn</li>
                <li><strong>⏱️ Thời điểm nhảy:</strong> Nhấn SPACE khi thấy chướng ngại vật đến gần</li>
                <li><strong>👁️ Quan sát:</strong> Chú ý đến khoảng cách và tốc độ của bóng bay</li>
                <li><strong>🎯 Luyện tập:</strong> Bắt đầu với chế độ "Siêu Dễ" để làm quen</li>
                <li><strong>💪 Kiên trì:</strong> Đừng nản lòng nếu không đạt điểm cao ngay lần đầu</li>
                <li><strong>🎵 Âm thanh:</strong> Bật âm thanh để nghe hiệu ứng vui nhộn</li>
            </ul>
        </div>
        """, unsafe_allow_html=True
    )

# CSS để làm đẹp thêm
st.markdown(
    """
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
    """, unsafe_allow_html=True
)
