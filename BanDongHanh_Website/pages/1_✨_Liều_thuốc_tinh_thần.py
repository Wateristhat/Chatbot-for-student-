import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
import tempfile
import subprocess
import requests
from gtts import gTTS
from io import BytesIO
import time

# Check TTS availability
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="✨ Liều Thuốc Tinh Thần",
    page_icon="✨",
    layout="wide"
)
st.markdown("""
<style>
[data-testid="stSidebar"] {
    min-width: 320px !important;
    max-width: 320px !important;
    width: 320px !important;
}
/* Chỉnh font và kích thước chữ sidebar */
[data-testid="stSidebar"] .css-1v0mbdj, 
[data-testid="stSidebar"] .css-1wv5c7b, 
[data-testid="stSidebar"] .css-1v8zqwd, 
[data-testid="stSidebar"] .css-1xcwr2u, 
[data-testid="stSidebar"] .css-15zrgzn {
    font-size: 1.18rem !important;
    font-family: 'Comic Neue', Arial, sans-serif !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .back-btn {
        text-decoration: none;
        font-size: 0.95rem;
        color: #000;
        background: #f1f1f1;
        padding: 0.4rem 0.8rem;
        border-radius: 8px;
    }
    .back-btn:hover { background: #e5e5e5; }
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("[⬅ Về Trang chủ](0_💖_Trang_chủ.py)", unsafe_allow_html=True)

# --- CSS VÀ FONT RIÊNG CỦA TRANG ---
st.markdown("""
<link rel="stylesheet"
 href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;500;600;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Quicksand', Arial, sans-serif; 
        font-size: 1.1rem;
    }
    
    /* Giao diện thân thiện với màu sắc tươi sáng */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b, #4ecdc4, #45b7d1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        animation: gentle-bounce 2s ease-in-out infinite;
    }
    
    @keyframes gentle-bounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Nút lớn và thân thiện */
    .big-friendly-button {
        font-size: 1.4rem !important;
        padding: 1rem 1.5rem !important;
        border-radius: 20px !important;
        margin: 0.5rem 0 !important;
        font-weight: 600 !important;
        border: none !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        text-align: center !important;
        display: block !important;
        width: 100% !important;
    }
    
    .btn-courage {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%) !important;
        color: #333 !important;
        box-shadow: 0 6px 20px rgba(255, 154, 158, 0.4) !important;
    }
    
    .btn-fun {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%) !important;
        color: #333 !important;
        box-shadow: 0 6px 20px rgba(252, 182, 159, 0.4) !important;
    }
    
    .btn-peace {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%) !important;
        color: #333 !important;
        box-shadow: 0 6px 20px rgba(168, 237, 234, 0.4) !important;
    }
    
    .big-friendly-button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
    }
    
    /* Card động viên với avatar */
    .encouragement-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 30%, #ee9ca7 100%);
        border-radius: 25px;
        padding: 2.5rem 2rem;
        margin: 2rem 0;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        animation: card-appear 0.6s ease-out;
        border: 3px solid #fff;
    }
    
    @keyframes card-appear {
        0% { opacity: 0; transform: scale(0.8) translateY(20px); }
        100% { opacity: 1; transform: scale(1) translateY(0); }
    }
    
    .encouragement-avatar {
        font-size: 4rem;
        margin-bottom: 1rem;
        animation: avatar-bounce 2s ease-in-out infinite;
    }
    
    @keyframes avatar-bounce {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-8px) rotate(5deg); }
    }
    
    .encouragement-message {
        font-size: 1.4rem;
        font-weight: 600;
        color: #2c3e50;
        line-height: 1.8;
        margin: 1rem 0;
        text-shadow: 0 1px 3px rgba(255,255,255,0.7);
    }
    
    /* Hộp hướng dẫn nhỏ */
    .guidance-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1.5rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: 500;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.3);
        animation: gentle-pulse 3s ease-in-out infinite;
    }
    
    @keyframes gentle-pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    /* Hiệu ứng bong bóng bay */
    @keyframes bubble-float {
        0% { transform: translateY(0px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    .bubble {
        position: fixed;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.8);
        animation: bubble-float 4s linear infinite;
        z-index: 1000;
    }
    
    /* Nút TTS thân thiện */
    .tts-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.8rem 1.5rem !important;
        border-radius: 15px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        margin: 0.5rem !important;
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4) !important;
    }
    
    .tts-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6) !important;
    }
    
    /* Lọ động viên */
    .encouragement-jar {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6px 20px rgba(255, 234, 167, 0.4);
    }
    
    /* Hiệu ứng sao rơi */
    @keyframes star-fall {
        0% { transform: translateY(-10px) rotate(0deg); opacity: 1; }
        100% { transform: translateY(100px) rotate(180deg); opacity: 0; }
    }
    
    .falling-star {
        position: fixed;
        color: #ffd700;
        font-size: 2rem;
        animation: star-fall 3s linear infinite;
        z-index: 1000;
    }
    
    /* Responsive cho học sinh */
    @media (max-width: 700px) {
        .main-title { font-size: 2rem; }
        .encouragement-message { font-size: 1.2rem; }
        .encouragement-avatar { font-size: 3rem; }
        .big-friendly-button { font-size: 1.2rem !important; padding: 0.8rem 1.2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- THƯ VIỆN NỘI DUNG CẢI TIẾN ---
MESSAGE_CATEGORIES = {
    "courage": {
        "label": "🐝 Cần Cổ Vũ",
        "icon": "🐝",
        "color_class": "btn-courage", 
        "messages": [
            {
                "avatar": "🐝",
                "text": "Bee tin rằng bạn có thể làm được! Mỗi bước nhỏ đều rất quan trọng, cứ từ từ thôi nhé!",
                "name": "Ong Bee"
            },
            {
                "avatar": "🦋", 
                "text": "Giống như bướm vượt qua kén để bay lên, bạn cũng đang trở nên mạnh mẽ hơn mỗi ngày!",
                "name": "Bướm xinh"
            },
            {
                "avatar": "🌟",
                "text": "Bạn là ngôi sao sáng nhất trong bầu trời! Hãy tự tin tỏa sáng như chính mình nhé!",
                "name": "Sao sáng"
            },
            {
                "avatar": "🌈",
                "text": "Sau cơn mưa sẽ có cầu vồng! Những khó khăn hôm nay sẽ là niềm vui ngày mai đấy!",
                "name": "Cầu vồng"
            },
            {
                "avatar": "🦄",
                "text": "Bạn đặc biệt như kỳ lân vậy! Không ai có thể thay thế được vị trí của bạn đâu!",
                "name": "Kỳ lân"
            }
        ]
    },
    "fun": {
        "label": "😊 Muốn Vui Vẻ", 
        "icon": "😊",
        "color_class": "btn-fun",
        "messages": [
            {
                "avatar": "🐝",
                "text": "Bee kể cho bạn nghe nhé: Tại sao ong luôn vui? Vì ong biết cách 'bay' khỏi buồn phiền! Hihi!",
                "name": "Ong Bee"
            },
            {
                "avatar": "🐧",
                "text": "Bạn có biết chim cánh cụt đi bộ lắc lư để không bị ngã không? Cũng giống bạn vậy, cứ vui vẻ đi thôi!",
                "name": "Chim cánh cụt"
            },
            {
                "avatar": "🐨",
                "text": "Gấu koala ngủ 20 tiếng/ngày mà vẫn hạnh phúc! Đôi khi chậm lại cũng tốt mà, bạn nhỉ?",
                "name": "Gấu koala"
            },
            {
                "avatar": "🌻",
                "text": "Hoa hướng dương luôn quay mặt về phía mặt trời! Hãy tìm những điều tích cực nào!",
                "name": "Hoa hướng dương"
            },
            {
                "avatar": "🎈",
                "text": "Khinh khí cầu bay cao vì chở đầy không khí nóng... tức là niềm vui! Bạn cũng bay cao thôi!",
                "name": "Khinh khí cầu"
            }
        ]
    },
    "peace": {
        "label": "🫧 Tìm Bình Yên",
        "icon": "🫧", 
        "color_class": "btn-peace",
        "messages": [
            {
                "avatar": "🫧",
                "text": "Hãy thở sâu như những bong bóng bay... từ từ thôi, không vội được đâu. Bạn đang làm rất tốt.",
                "name": "Bong bóng"
            },
            {
                "avatar": "🌊",
                "text": "Như sóng biển nhẹ nhàng vỗ bờ, hãy để tâm hồn bạn được nghỉ ngơi nhé.",
                "name": "Sóng biển"
            },
            {
                "avatar": "🍃",
                "text": "Lá cây nhảy múa trong gió mà không gãy. Bạn cũng mềm mại và mạnh mẽ như vậy.",
                "name": "Lá cây"
            },
            {
                "avatar": "🌙",
                "text": "Trăng tròn hay trăng khuyết đều đẹp. Bạn lúc vui hay buồn cũng đều đáng yêu.",
                "name": "Trăng xinh"
            },
            {
                "avatar": "🕯️",
                "text": "Như ngọn nến nhỏ trong đêm tối, bạn có sức mạnh thầm lặng nhưng rất ấm áp.",
                "name": "Ngọn nến"
            }
        ]
    }
}

# --- SESSION STATE ---
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = {}
if 'show_journal' not in st.session_state:
    st.session_state.show_journal = False
if 'saved_encouragements' not in st.session_state:
    st.session_state.saved_encouragements = []
if 'show_effects' not in st.session_state:
    st.session_state.show_effects = False

# --- ENHANCED TTS FUNCTIONS ---

def check_network_connectivity():
    """Kiểm tra kết nối mạng để sử dụng TTS online"""
    try:
        response = requests.get("https://translate.google.com", timeout=3)
        return response.status_code == 200
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
        return False
    except Exception:
        return False

def check_file_permissions():
    """Kiểm tra quyền ghi file tạm thời"""
    try:
        # Thử tạo file tạm trong thư mục temp
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            tmp_file.write(b"test")
            return True
    except Exception:
        return False

def gtts_with_diagnostics(text):
    """Tạo âm thanh bằng gTTS với chẩn đoán lỗi chi tiết và logging"""
    if not GTTS_AVAILABLE:
        print(f"[DEBUG - TTS] gTTS không có sẵn trong hệ thống")  # Log cho dev/admin
        return None, "gtts_not_available"
    
    # Kiểm tra kết nối mạng trước
    if not check_network_connectivity():
        print(f"[DEBUG - TTS] Không thể kết nối internet")  # Log cho dev/admin
        return None, "network_error"
    
    # Kiểm tra quyền ghi file
    if not check_file_permissions():
        print(f"[DEBUG - TTS] Không có quyền ghi file tạm thời")  # Log cho dev/admin
        return None, "file_permission_error"
    
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text.strip(), lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        audio_data = audio_bytes.read()
        
        if audio_data and len(audio_data) > 0:
            print(f"[DEBUG - TTS] Tạo âm thanh thành công với gTTS, kích thước: {len(audio_data)} bytes")  # Log cho dev/admin
            return audio_data, "success"
        else:
            print(f"[DEBUG - TTS] gTTS không tạo được dữ liệu âm thanh")  # Log cho dev/admin
            return None, "no_audio_generated"
            
    except Exception as e:
        error_str = str(e).lower()
        print(f"[DEBUG - TTS] Lỗi gTTS: {str(e)}")  # Log chi tiết cho dev/admin
        
        if "connection" in error_str or "network" in error_str:
            return None, "network_error"
        elif "timeout" in error_str:
            return None, "timeout_error"
        elif "forbidden" in error_str or "403" in error_str:
            return None, "access_blocked"
        elif "503" in error_str or "502" in error_str or "500" in error_str:
            return None, "server_error"
        else:
            return None, f"unknown_error: {str(e)}"

def edge_tts_with_diagnostics(text, voice="vi-VN-HoaiMyNeural", rate=0):
    """Tạo âm thanh bằng Edge TTS với chẩn đoán lỗi chi tiết"""
    if not EDGE_TTS_AVAILABLE:
        print(f"[DEBUG - TTS] Edge TTS không có sẵn trong hệ thống")  # Log cho dev/admin
        return None, "edge_tts_not_available"
    
    try:
        # Tạo file tạm thời
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        
        # Tạo lệnh Edge TTS
        rate_str = f"{'+' if rate >= 0 else ''}{rate}%"
        cmd = [
            "edge-tts",
            "--voice", voice,
            "--rate", rate_str,
            "--text", text,
            "--write-media", temp_path
        ]
        
        print(f"[DEBUG - TTS] Chạy lệnh Edge TTS: {' '.join(cmd)}")  # Log cho dev/admin
        
        # Chạy lệnh
        result = subprocess.run(cmd, check=True, capture_output=True, timeout=10)
        
        # Đọc dữ liệu âm thanh
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Xóa file tạm thời
            try:
                os.unlink(temp_path)
            except:
                pass
            
            print(f"[DEBUG - TTS] Tạo âm thanh thành công với Edge TTS, kích thước: {len(audio_data)} bytes")  # Log cho dev/admin
            return audio_data, "success"
        else:
            print(f"[DEBUG - TTS] Edge TTS không tạo được file âm thanh")  # Log cho dev/admin
            return None, "no_audio_file_generated"
            
    except subprocess.TimeoutExpired:
        print(f"[DEBUG - TTS] Edge TTS timeout")  # Log cho dev/admin
        return None, "edge_tts_timeout"
    except subprocess.CalledProcessError as e:
        print(f"[DEBUG - TTS] Edge TTS command error: {e.returncode}")  # Log cho dev/admin
        return None, f"edge_tts_command_error: {e.returncode}"
    except FileNotFoundError:
        print(f"[DEBUG - TTS] Edge TTS chưa được cài đặt")  # Log cho dev/admin
        return None, "edge_tts_not_installed"
    except Exception as e:
        print(f"[DEBUG - TTS] Lỗi Edge TTS: {str(e)}")  # Log cho dev/admin
        return None, f"edge_tts_error: {str(e)}"

@st.cache_data
def create_audio_with_tts_enhanced(text):
    """Chuyển văn bản thành giọng nói với hệ thống chẩn đoán và fallback"""
    # Kiểm tra text đầu vào
    if not text or not text.strip():
        print(f"[DEBUG - TTS] Text rỗng hoặc chỉ có khoảng trắng")  # Log cho dev/admin
        return None, "empty_text"
    
    text = text.strip()
    if len(text) < 3:  # Tăng độ dài tối thiểu lên 3 cho tiếng Việt
        print(f"[DEBUG - TTS] Text quá ngắn: '{text}' (độ dài: {len(text)})")  # Log cho dev/admin
        return None, "text_too_short"
    
    print(f"[DEBUG - TTS] Bắt đầu tạo âm thanh cho text: '{text[:50]}{'...' if len(text) > 50 else ''}'")  # Log cho dev/admin
    
    # Thử Edge TTS trước (không cần internet)
    if EDGE_TTS_AVAILABLE:
        print(f"[DEBUG - TTS] Thử Edge TTS trước...")  # Log cho dev/admin
        audio_data, error_code = edge_tts_with_diagnostics(text)
        if audio_data:
            return audio_data, "success_edge_tts"
    
    # Fallback sang gTTS (cần internet)
    if GTTS_AVAILABLE:
        print(f"[DEBUG - TTS] Fallback sang gTTS...")  # Log cho dev/admin
        audio_data, error_code = gtts_with_diagnostics(text)
        if audio_data:
            return audio_data, "success_gtts"
        else:
            return None, error_code
    
    print(f"[DEBUG - TTS] Không có TTS engine nào khả dụng")  # Log cho dev/admin
    return None, "no_tts_available"

def get_error_message(error_code):
    """Trả về thông báo lỗi thân thiện cho học sinh"""
    error_messages = {
        "empty_text": "💭 Chưa có nội dung để đọc. Hãy thử lại khi có văn bản!",
        "text_too_short": "💭 Nội dung quá ngắn để tạo âm thanh. Hãy thêm vài từ nữa nhé!",
        "network_error": "🌐 Không thể kết nối internet để tạo âm thanh. Hãy kiểm tra kết nối mạng và thử lại sau nhé!",
        "timeout_error": "⏰ Kết nối quá chậm. Hãy thử lại sau vài giây hoặc kiểm tra tốc độ mạng!",
        "access_blocked": "🚫 Dịch vụ tạo âm thanh tạm thời bị chặn. Hãy thử lại sau hoặc dùng trình duyệt khác!",
        "server_error": "🔧 Máy chủ tạo âm thanh đang bảo trì. Hãy thử lại sau 5-10 phút nhé!",
        "file_permission_error": "📁 Không thể tạo file âm thanh tạm thời. Hãy thử lại hoặc liên hệ hỗ trợ!",
        "no_tts_available": "🔊 Tính năng đọc to hiện không khả dụng. Bạn có thể đọc nội dung ở trên nhé!",
        "gtts_not_available": "🎵 Dịch vụ tạo âm thanh Google không khả dụng.",
        "edge_tts_not_available": "🎵 Edge TTS không có sẵn",
        "edge_tts_timeout": "⏰ Tạo âm thanh mất quá nhiều thời gian. Hãy thử lại!",
        "edge_tts_not_installed": "🔧 Chưa cài đặt công cụ tạo giọng nói. Hãy liên hệ quản trị viên!",
        "no_audio_generated": "❌ Không thể tạo âm thanh. Hãy thử lại với nội dung khác!",
        "no_audio_file_generated": "❌ Không thể tạo file âm thanh. Hãy thử lại!",
    }
    
    # Xử lý lỗi có prefix
    if error_code.startswith("unknown_error:"):
        return "🔍 Có lỗi không xác định xảy ra. Hãy thử lại sau hoặc liên hệ hỗ trợ!"
    elif error_code.startswith("edge_tts_error:"):
        return "🎵 Có lỗi khi tạo giọng nói. Hãy thử lại sau!"
    elif error_code.startswith("edge_tts_command_error:"):
        return "🔧 Lệnh tạo giọng nói gặp lỗi. Hãy thử lại hoặc khởi động lại ứng dụng!"
    
    return error_messages.get(error_code, f"🔊 Hiện tại không thể tạo âm thanh. Bạn có thể đọc nội dung ở trên nhé!")

# Giữ lại hàm cũ để tương thích ngược
@st.cache_data
def create_audio_with_tts(text):
    """Hàm TTS cũ - chuyển sang phiên bản cải tiến"""
    audio_data, result_code = create_audio_with_tts_enhanced(text)
    return audio_data if audio_data else None

# Hàm debug đơn giản cho server admin
def tts_debug_test():
    """Hàm test đơn giản để debug TTS cho server admin"""
    test_text = "Xin chào, đây là bài test âm thanh tiếng Việt."
    
    st.markdown("### 🔧 TTS Debug Test (Dành cho Admin)")
    st.info("Công cụ này giúp admin kiểm tra tình trạng TTS system")
    
    if st.button("🧪 Chạy test TTS"):
        st.markdown("#### Thông tin hệ thống:")
        st.write(f"- gTTS khả dụng: {GTTS_AVAILABLE}")
        st.write(f"- Edge TTS khả dụng: {EDGE_TTS_AVAILABLE}")
        st.write(f"- Kết nối mạng: {check_network_connectivity()}")
        st.write(f"- Quyền ghi file: {check_file_permissions()}")
        
        st.markdown("#### Test tạo âm thanh:")
        with st.spinner("Đang test..."):
            audio_data, result_code = create_audio_with_tts_enhanced(test_text)
            
            if audio_data:
                st.success(f"✅ Tạo âm thanh thành công! ({result_code})")
                st.audio(audio_data, format="audio/mp3")
            else:
                st.error(f"❌ Lỗi: {result_code}")
                st.info(get_error_message(result_code))

def play_encouragement_audio(message_data):
    """Phát âm thanh cho lời động viên với xử lý lỗi chi tiết"""
    full_text = f"{message_data['name']} nói: {message_data['text']}"
    
    with st.spinner("🎵 Bee đang chuẩn bị âm thanh cho bạn..."):
        audio_data, result_code = create_audio_with_tts_enhanced(full_text)
        
        if audio_data and result_code.startswith("success"):
            # Hiển thị thông tin thành công nhẹ nhàng
            if "edge_tts" in result_code:
                st.success("🎵 Đã tạo âm thanh bằng giọng nói tự nhiên!")
            else:
                st.success("🎵 Đã tạo âm thanh cho bạn!")
            
            # Phát âm thanh
            st.audio(audio_data, format="audio/mp3")
            
            # Thêm hiệu ứng vui vẻ
            st.session_state.show_effects = True
            time.sleep(0.5)
            if random.random() < 0.7:  # 70% khả năng có hiệu ứng
                st.balloons()
        else:
            # Hiển thị lỗi thân thiện với hướng dẫn khắc phục
            error_msg = get_error_message(result_code)
            
            # Sử dụng st.info hoặc st.warning thay vì st.error để không làm học sinh sợ hãi
            if "network" in result_code.lower():
                st.warning(error_msg)
                st.info("💡 **Gợi ý**: Kiểm tra kết nối WiFi/4G → Tải lại trang → Thử lại")
            elif "timeout" in result_code.lower():
                st.info(error_msg)  
                st.info("💡 **Gợi ý**: Đợi 5 giây → Thử lại → Hoặc sử dụng mạng khác")
            elif "blocked" in result_code.lower() or "403" in result_code:
                st.info(error_msg)
                st.info("💡 **Gợi ý**: Thử trình duyệt khác (Chrome/Firefox) → Tắt VPN → Thử lại")
            elif "server" in result_code.lower():
                st.info(error_msg)
                st.info("💡 **Gợi ý**: Đợi 10 phút → Thử lại → Lỗi từ nhà cung cấp dịch vụ")
            else:
                st.info(error_msg)
            
            # Thêm thông điệp động viên khi gặp lỗi
            st.info("🤗 Âm thanh đang bận, nhưng Bee vẫn yêu bạn! Bạn có thể đọc nội dung ở trên nhé!")

# --- HIỆU ỨNG ANIMATIONS ---
def show_floating_effects():
    """Hiển thị hiệu ứng bong bóng bay và sao rơi"""
    if st.session_state.show_effects:
        # JavaScript cho hiệu ứng động
        effects_html = f"""
        <script>
        function createBubbles() {{
            for(let i = 0; i < 6; i++) {{
                setTimeout(() => {{
                    const bubble = document.createElement('div');
                    bubble.innerHTML = '{random.choice(["🫧", "💫", "✨", "🌟", "🎈", "💎"])}';
                    bubble.style.position = 'fixed';
                    bubble.style.left = Math.random() * 100 + '%';
                    bubble.style.fontSize = (Math.random() * 1.5 + 1) + 'rem';
                    bubble.style.zIndex = '9999';
                    bubble.style.pointerEvents = 'none';
                    bubble.style.animation = 'bubble-float 4s ease-out forwards';
                    document.body.appendChild(bubble);
                    setTimeout(() => bubble.remove(), 4000);
                }}, i * 300);
            }}
        }}
        
        function createFallingStars() {{
            for(let i = 0; i < 4; i++) {{
                setTimeout(() => {{
                    const star = document.createElement('div');
                    star.innerHTML = '{random.choice(["⭐", "🌟", "✨", "💫"])}';
                    star.style.position = 'fixed';
                    star.style.left = Math.random() * 100 + '%';
                    star.style.fontSize = '1.8rem';
                    star.style.zIndex = '9999';
                    star.style.pointerEvents = 'none';
                    star.style.animation = 'star-fall 3s ease-in forwards';
                    document.body.appendChild(star);
                    setTimeout(() => star.remove(), 3000);
                }}, i * 600);
            }}
        }}
        
        function createFlyingBee() {{
            const bee = document.createElement('div');
            bee.innerHTML = '🐝';
            bee.style.position = 'fixed';
            bee.style.fontSize = '2rem';
            bee.style.zIndex = '9999';
            bee.style.pointerEvents = 'none';
            bee.style.left = '-50px';
            bee.style.top = Math.random() * 50 + 30 + '%';
            bee.style.animation = 'bee-fly 8s linear forwards';
            document.body.appendChild(bee);
            setTimeout(() => bee.remove(), 8000);
        }}
        
        // Thêm CSS animations nếu chưa có
        if (!document.getElementById('magic-animations')) {{
            const style = document.createElement('style');
            style.id = 'magic-animations';
            style.textContent = `
                @keyframes bubble-float {{
                    0% {{ transform: translateY(0) rotate(0deg) scale(1); opacity: 0.8; }}
                    50% {{ transform: translateY(-50vh) rotate(180deg) scale(1.2); opacity: 1; }}
                    100% {{ transform: translateY(-100vh) rotate(360deg) scale(0.8); opacity: 0; }}
                }}
                @keyframes star-fall {{
                    0% {{ transform: translateY(-10px) translateX(0) rotate(0deg); opacity: 1; }}
                    100% {{ transform: translateY(100vh) translateX(50px) rotate(360deg); opacity: 0; }}
                }}
                @keyframes bee-fly {{
                    0% {{ transform: translateX(0) translateY(0) rotate(0deg); }}
                    25% {{ transform: translateX(25vw) translateY(-20px) rotate(10deg); }}
                    50% {{ transform: translateX(50vw) translateY(10px) rotate(-5deg); }}
                    75% {{ transform: translateX(75vw) translateY(-15px) rotate(8deg); }}
                    100% {{ transform: translateX(100vw) translateY(0) rotate(0deg); }}
                }}
            `;
            document.head.appendChild(style);
        }}
        
        // Chạy hiệu ứng
        setTimeout(createBubbles, 500);
        setTimeout(createFallingStars, 1000);
        setTimeout(createFlyingBee, 1500);
        </script>
        """
        st.markdown(effects_html, unsafe_allow_html=True)

# --- HÀM XỬ LÝ ---
def select_category(category_key):
    st.session_state.message_category = category_key
    st.session_state.current_message = random.choice(
        MESSAGE_CATEGORIES[category_key]["messages"]
    )

def get_new_message():
    category_key = st.session_state.message_category
    if category_key:
        st.session_state.current_message = random.choice(
            MESSAGE_CATEGORIES[category_key]["messages"]
        )

def save_to_encouragement_jar():
    """Lưu động viên vào lọ động viên cá nhân"""
    if st.session_state.current_message:
        encouragement = {
            "avatar": st.session_state.current_message["avatar"],
            "text": st.session_state.current_message["text"], 
            "name": st.session_state.current_message["name"],
            "category": st.session_state.message_category,
            "saved_time": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        # Kiểm tra không trùng lặp
        if encouragement not in st.session_state.saved_encouragements:
            st.session_state.saved_encouragements.append(encouragement)
            st.success(f"✨ Đã lưu lời động viên từ {encouragement['name']} vào lọ động viên!")
            if random.random() < 0.8:
                st.balloons()
        else:
            st.info("💫 Lời động viên này đã có trong lọ rồi nhé!")

# --- HÀM XỬ LÝ NHẬT KÝ CẢM XÚC ---
def get_csv_path():
    """Trả về đường dẫn đến file mood_journal.csv"""
    return os.path.join(os.path.dirname(__file__), "..", "mood_journal.csv")

def ensure_csv_exists():
    """Đảm bảo file CSV tồn tại với header phù hợp"""
    csv_path = get_csv_path()
    if not os.path.exists(csv_path):
        # Tạo DataFrame với header theo yêu cầu
        df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
        df.to_csv(csv_path, index=False, encoding='utf-8')
    else:
        # Kiểm tra và cập nhật header nếu cần
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            if list(df.columns) != ["Ngày giờ", "Loại", "Nội dung"]:
                # Backup dữ liệu cũ nếu có
                if not df.empty:
                    backup_path = csv_path.replace('.csv', '_backup.csv')
                    df.to_csv(backup_path, index=False, encoding='utf-8')
                # Tạo mới với header đúng
                df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
        except Exception:
            # Nếu có lỗi, tạo file mới
            df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
            df.to_csv(csv_path, index=False, encoding='utf-8')

def save_message_to_journal():
    """Lưu thông điệp hiện tại vào nhật ký cảm xúc"""
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        
        # Lấy thông tin hiện tại
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_type = "Liều thuốc tinh thần"
        
        if st.session_state.current_message:
            content = f"{st.session_state.current_message['name']}: {st.session_state.current_message['text']}"
        else:
            content = "Không có nội dung"
        
        # Đọc file CSV hiện tại
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Thêm dòng mới
        new_row = pd.DataFrame({
            "Ngày giờ": [current_time],
            "Loại": [message_type], 
            "Nội dung": [content]
        })
        
        df = pd.concat([df, new_row], ignore_index=True)
        
        # Lưu lại file
        df.to_csv(csv_path, index=False, encoding='utf-8')
        
        st.success("✅ Đã lưu thông điệp vào nhật ký cảm xúc!")
        st.balloons()
        
    except Exception as e:
        st.error(f"❌ Có lỗi khi lưu thông điệp: {str(e)}")

def show_journal_history():
    """Hiển thị lịch sử nhật ký liều thuốc tinh thần với thống kê cho giáo viên"""
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        
        df = pd.read_csv(csv_path, encoding='utf-8')
        
        # Lọc theo loại "Liều thuốc tinh thần"
        filtered_df = df[df["Loại"] == "Liều thuốc tinh thần"]
        
        if filtered_df.empty:
            st.info("📝 Chưa có thông điệp nào được lưu trong nhật ký.")
        else:
            st.markdown("### 📖 Nhật Ký Liều Thuốc Tinh Thần")
            
            # Thống kê cho giáo viên
            st.markdown("#### 📊 Thống Kê Sử Dụng (Dành cho Giáo viên)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("📈 Tổng lượt sử dụng", len(filtered_df))
            
            with col2:
                # Phân tích loại động viên được dùng nhiều nhất
                categories_used = []
                for content in filtered_df["Nội dung"]:
                    if "Ong Bee" in content or "Bướm xinh" in content or "Sao sáng" in content or "Cầu vồng" in content or "Kỳ lân" in content:
                        categories_used.append("Cổ vũ")
                    elif "Chim cánh cụt" in content or "Gấu koala" in content or "Hoa hướng dương" in content or "Khinh khí cầu" in content:
                        categories_used.append("Vui vẻ") 
                    elif "Bong bóng" in content or "Sóng biển" in content or "Lá cây" in content or "Trăng xinh" in content or "Ngọn nến" in content:
                        categories_used.append("Bình yên")
                        
                most_used = max(set(categories_used), key=categories_used.count) if categories_used else "Chưa có"
                st.metric("💫 Loại được ưa thích", most_used)
            
            with col3:
                # Ngày sử dụng gần nhất
                latest_date = filtered_df["Ngày giờ"].max() if not filtered_df.empty else "Chưa có"
                st.metric("📅 Sử dụng gần nhất", latest_date[:10] if latest_date != "Chưa có" else "Chưa có")
            
            st.write("---")
            
            # Sắp xếp theo thời gian mới nhất
            filtered_df = filtered_df.sort_values("Ngày giờ", ascending=False)
            
            # Hiển thị bảng chi tiết
            st.markdown("#### 📋 Chi Tiết Sử Dụng")
            st.dataframe(
                filtered_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Ngày giờ": st.column_config.DatetimeColumn(
                        "Ngày giờ",
                        format="DD/MM/YYYY HH:mm:ss"
                    ),
                    "Loại": st.column_config.TextColumn(
                        "Loại",
                        width="medium"
                    ),
                    "Nội dung": st.column_config.TextColumn(
                        "Nội dung",
                        width="large"
                    )
                }
            )
            
            # Hướng dẫn cho giáo viên
            st.markdown("""
            ---
            ### 👩‍🏫 Hướng Dẫn Cho Giáo Viên
            - **Tần suất sử dụng cao**: Học sinh có thể đang cần nhiều hỗ trợ tinh thần
            - **Loại "Cổ vũ"**: Học sinh cần động viên và khích lệ
            - **Loại "Vui vẻ"**: Học sinh muốn giải tỏa căng thẳng
            - **Loại "Bình yên"**: Học sinh cần hỗ trợ quản lý cảm xúc và stress
            
            💡 *Gợi ý: Nếu học sinh sử dụng nhiều một loại động viên, hãy trò chuyện riêng để hiểu thêm về tình hình của em.*
            """)
            
    except Exception as e:
        st.error(f"❌ Có lỗi khi đọc nhật ký: {str(e)}")

# --- GIAO DIỆN CHÍNH ---
st.markdown("<div class='main-title'>✨ Liều Thuốc Tinh Thần Cho Bạn ✨</div>", unsafe_allow_html=True)

# Hộp hướng dẫn thân thiện
st.markdown("""
<div class="guidance-box">
    🐝 Chọn điều bạn cần nhất, Bee sẽ gửi động viên phù hợp! Bạn có thể nghe hoặc lưu lại nhé! 🌈
</div>
""", unsafe_allow_html=True)

# Nút chọn loại thông điệp với giao diện cải thiện
st.markdown("### 🌟 Bạn đang cần điều gì lúc này?")

cols = st.columns(len(MESSAGE_CATEGORIES))
for idx, (key, value) in enumerate(MESSAGE_CATEGORIES.items()):
    with cols[idx]:
        if st.button(
            f"{value['icon']} {value['label']}", 
            key=f"btn_{key}",
            help=f"Nhận động viên về {value['label'].lower()}",
            use_container_width=True
        ):
            select_category(key)
            st.rerun()

st.write("---")

# Hiển thị thông điệp với avatar và hiệu ứng
if st.session_state.current_message and st.session_state.message_category:
    message_data = st.session_state.current_message
    
    # Card động viên với avatar và hiệu ứng
    st.markdown(f"""
    <div class="encouragement-card">
        <div class="encouragement-avatar">{message_data['avatar']}</div>
        <div class="encouragement-message">{message_data['text']}</div>
        <div style="font-size: 1.1rem; color: #7f8c8d; margin-top: 1rem;">
            💝 Từ {message_data['name']} gửi bạn
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Hiệu ứng động khi hiển thị
    show_floating_effects()
    
    # Các nút tương tác
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(
            "🔄 Nhận lời khác cùng loại",
            key="btn_next_message",
            help="Nhận một thông điệp động viên khác cùng loại",
            use_container_width=True
        ):
            get_new_message()
            st.rerun()
    
    with col2:
        if st.button(
            "🔊 Đọc to",
            key="btn_tts",
            help="Nghe lời động viên bằng tiếng Việt",
            use_container_width=True
        ):
            play_encouragement_audio(message_data)
    
    with col3:
        if st.button(
            "💝 Lưu vào lọ động viên",
            key="btn_save_jar",
            help="Lưu lời động viên này để xem lại sau",
            use_container_width=True
        ):
            save_to_encouragement_jar()

    st.write("")  # Khoảng cách

    # Nút nhật ký cảm xúc
    col_journal1, col_journal2 = st.columns(2)
    
    with col_journal1:
        if st.button(
            "📓 Lưu vào nhật ký cảm xúc",
            key="btn_save_journal",
            help="Lưu vào nhật ký để giáo viên có thể xem",
            use_container_width=True
        ):
            save_message_to_journal()
    
    with col_journal2:
        if st.button(
            "📖 Xem nhật ký đã lưu", 
            key="btn_view_journal",
            help="Xem lịch sử các lời động viên đã lưu",
            use_container_width=True
        ):
            st.session_state.show_journal = not st.session_state.show_journal

# --- HIỂN THỊ LỌ ĐỘNG VIÊN ---
if st.session_state.saved_encouragements:
    st.write("---")
    st.markdown("### 🍯 Lọ Động Viên Của Bạn")
    
    st.markdown(f"""
    <div class="encouragement-jar">
        <h4 style="text-align: center; margin-bottom: 1rem;">
            🍯 Bạn đã thu thập {len(st.session_state.saved_encouragements)} lời động viên!
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Hiển thị các lời động viên đã lưu
    for idx, encouragement in enumerate(reversed(st.session_state.saved_encouragements)):
        with st.container():
            col1, col2, col3 = st.columns([1, 6, 2])
            
            with col1:
                st.markdown(f"<div style='font-size: 2.5rem; text-align: center;'>{encouragement['avatar']}</div>", 
                           unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background: #f8f9fa; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;'>
                    <strong>{encouragement['name']}:</strong><br>
                    {encouragement['text']}<br>
                    <small style='color: #6c757d;'>💾 {encouragement['saved_time']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                if st.button("🔊", key=f"jar_tts_{idx}", help="Nghe lại lời động viên này"):
                    play_encouragement_audio(encouragement)
                
                if st.button("🗑️", key=f"jar_remove_{idx}", help="Xóa khỏi lọ động viên"):
                    st.session_state.saved_encouragements.remove(encouragement)
                    st.success("✅ Đã xóa khỏi lọ động viên!")
                    st.rerun()

# --- HIỂN THỊ NHẬT KÝ NẾU ĐƯỢC YÊU CẦU ---
if st.session_state.show_journal:
    st.write("---")
    show_journal_history()
    
    # Nút đóng nhật ký
    if st.button("❌ Đóng nhật ký", key="btn_close_journal"):
        st.session_state.show_journal = False
        st.rerun()

# Reset hiệu ứng sau khi hiển thị
if st.session_state.show_effects:
    st.session_state.show_effects = False

# --- ADMIN DEBUG SECTION (Ẩn cho học sinh) ---
if 'show_debug' not in st.session_state:
    st.session_state.show_debug = False

# Chỉ hiển thị debug khi admin muốn
st.write("---")
with st.expander("🔧 Khu vực Admin/Debug (Chỉ dành cho quản trị viên)", expanded=False):
    st.markdown("""
    **Lưu ý**: Khu vực này dành cho giáo viên và quản trị viên hệ thống để kiểm tra tình trạng TTS.
    Học sinh có thể bỏ qua phần này.
    """)
    
    if st.button("🧪 Hiển thị Debug Console", key="show_debug_btn"):
        st.session_state.show_debug = not st.session_state.show_debug

    if st.session_state.show_debug:
        tts_debug_test()
