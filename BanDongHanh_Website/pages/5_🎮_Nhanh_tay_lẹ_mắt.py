import streamlit as st
import streamlit.components.v1 as components
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

# Hướng dẫn chi tiết với HTML được chuẩn hóa - Header
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
        box-shadow: 0 4px 15px rgba(147, 112, 219, 0.3);
    '>
        <div style='text-align: center; margin-bottom: 20px;'>
            <span style='font-size: 2rem;'>🐝✨</span>
            <h3 style='color: #4169E1; font-size: 1.5rem; margin: 10px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);'> 📖 Hướng dẫn chơi game chi tiết </h3>
            <span style='font-size: 2rem;'>✨🎈</span>
        </div>
    """, unsafe_allow_html=True
)

# Game objectives section
st.markdown(
    """
        <div style='color: #2E8B57; text-align: left; max-width: 600px; margin: 0 auto;'>
            <div style='background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #FF6347;'>
                <h4 style='color: #FF6347; margin: 0 0 10px 0;'>🎯 Mục tiêu game:</h4>
                <p style='margin: 5px 0;'>• Điều khiển chú ong Bee bay qua các quả bóng bay màu sắc</p>
                <p style='margin: 5px 0;'>• Tránh va chạm với chướng ngại vật để duy trì cuộc chơi</p>
                <p style='margin: 5px 0;'>• Thu thập điểm số cao nhất có thể</p>
            </div>
    """, unsafe_allow_html=True
)

# Controls section  
st.markdown(
    """
            <div style='background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #4169E1;'>
                <h4 style='color: #4169E1; margin: 0 0 10px 0;'>🎮 Cách điều khiển:</h4>
                <p style='margin: 5px 0;'>• <strong>Máy tính:</strong> Nhấn phím <span style='background: #4169E1; color: white; padding: 3px 8px; border-radius: 5px; font-weight: bold;'>SPACE</span> để Bee nhảy lên cao</p>
                <p style='margin: 5px 0;'>• <strong>Điện thoại/Tablet:</strong> Chạm vào màn hình game để Bee nhảy</p>
                <p style='margin: 5px 0;'>• <strong>Lưu ý:</strong> Bee sẽ rơi xuống do trọng lực, hãy tính toán thời điểm nhảy</p>
            </div>
    """, unsafe_allow_html=True
)

# Game modes section
st.markdown(
    """
            <div style='background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #32CD32;'>
                <h4 style='color: #32CD32; margin: 0 0 10px 0;'>🌟 Chế độ chơi:</h4>
                <p style='margin: 5px 0;'><strong>🌟 Siêu Dễ:</strong></p>
                <ul style='margin: 5px 0 10px 20px;'>
                    <li>Tốc độ chậm, dễ điều khiển</li>
                    <li>Khoảng cách chướng ngại vật rộng hơn</li>
                    <li>Phù hợp cho người mới bắt đầu</li>
                </ul>
                <p style='margin: 5px 0;'><strong>⭐ Bình Thường:</strong></p>
                <ul style='margin: 5px 0 10px 20px;'>
                    <li>Tốc độ nhanh hơn, thử thách hơn</li>
                    <li>Chướng ngại vật xuất hiện dày đặc hơn</li>
                    <li>Dành cho người đã quen thuộc</li>
                </ul>
            </div>
    """, unsafe_allow_html=True
)

# Features section
st.markdown(
    """
            <div style='background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #9370DB;'>
                <h4 style='color: #9370DB; margin: 0 0 10px 0;'>🔧 Tính năng hỗ trợ:</h4>
                <p style='margin: 5px 0;'>• <strong>Điều khiển âm thanh:</strong> Bật/tắt hiệu ứng âm thanh và nhạc nền</p>
                <p style='margin: 5px 0;'>• <strong>Điểm số:</strong> Theo dõi điểm hiện tại và kỷ lục cá nhân</p>
                <p style='margin: 5px 0;'>• <strong>Lời động viên:</strong> Tin nhắn khích lệ khi kết thúc game</p>
                <p style='margin: 5px 0;'>• <strong>Debug mode:</strong> Nhấn Ctrl + D để xem thông tin kỹ thuật (dành cho giáo viên)</p>
            </div>
    """, unsafe_allow_html=True
)

# Bee tips section and close the container
st.markdown(
    """
            <div style='background: linear-gradient(135deg, #FFE4E1, #FFF8DC); padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center; border: 2px solid #FF69B4;'>
                <h4 style='color: #FF1493; margin: 0 0 10px 0;'>💖 Lời khuyên từ Bee:</h4>
                <p style='margin: 5px 0; font-style: italic;'>"Đừng nản lòng nếu không đạt điểm cao ngay lần đầu!"</p>
                <p style='margin: 5px 0; font-style: italic;'>"Mỗi lần chơi là một cơ hội học hỏi và cải thiện!"</p>
                <p style='margin: 5px 0; font-weight: bold; color: #FF6347;'>🎈 Hãy thư giãn và tận hưởng trò chơi nhé! 🌈</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True
)

# Nút TTS cho hướng dẫn với nội dung cập nhật
instructions_text = """
Chào các bạn! Đây là trò chơi Bee Bay Cùng Bạn - Nhanh Tay Lẹ Mắt. 

Mục tiêu của bạn là điều khiển chú ong Bee bay qua các quả bóng bay màu sắc bằng cách nhấn phím SPACE để nhảy lên cao, hoặc chạm vào màn hình nếu bạn chơi trên điện thoại.

Game có hai chế độ: Siêu Dễ với tốc độ chậm phù hợp cho người mới bắt đầu, và Bình Thường thử thách hơn khi bạn đã quen.

Bạn có thể điều chỉnh âm thanh và nhạc nền theo ý muốn. Hãy thư giãn và tận hưởng trò chơi nhé! Bee luôn ủng hộ và tin tưởng vào bạn!

Nhớ rằng, mỗi lần chơi là một cơ hội học hỏi và vui chơi. Chúc bạn có những phút giây thật vui vẻ!
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
    
    # Hiển thị game với kích thước lớn hơn để đảm bảo hiển thị đầy đủ
    st.components.v1.html(game_html_content, height=720, scrolling=False)
    
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
    </style>
    """, unsafe_allow_html=True
)
