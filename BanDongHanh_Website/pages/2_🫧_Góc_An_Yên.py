import streamlit as st  # <-- 1. SỬA LỖI TYPO 'streaimport'
import time
import random
import pandas as pd
import sys
import os
import tempfile
import subprocess
import requests
from gtts import gTTS
from io import BytesIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import add_mood_entry, get_mood_entries

# --- 2. GIỮ NGUYÊN CSS BUTTON CỤC BỘ (VÌ KHÔNG DÙNG style.py) ---
st.markdown("""
<style>
.stButton > button {
    font-size: 1.5rem !important;      /* Tăng cỡ chữ lên 1.5 lần */
    padding: 1.8rem 3.6rem !important;  /* Tăng chiều cao & chiều ngang nút */
    border-radius: 18px !important;      /* Bo tròn nút */
    min-width: 220px;                   /* Đặt chiều rộng tối thiểu lớn hơn */
    min-height: 68px;                   /* Đặt chiều cao tối thiểu lớn hơn */
}
</style>
""", unsafe_allow_html=True)

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

# --- 3. SỬA LỖI CẤU HÌNH TRANG (THÊM DẤU PHẨY VÀ COLLAPSED) ---
st.set_page_config(
    page_title="Góc An Yên", 
    page_icon="🫧", 
    layout="wide", 
    initial_sidebar_state="collapsed" # <-- SỬA LỖI Ở ĐÂY
)

# --- 4. XÓA CSS SIDEBAR CỤC BỘ GÂY LỖI ---
# (Khối st.markdown(""" <style> [data-testid="stSidebar"] { ... } </style> """) đã bị xóa)

# --- CÁC THÔNG ĐIỆP ĐỘNG VIÊN NGẪU NHIÊN ---
ENCOURAGEMENT_MESSAGES = [
    "🌟 Bạn đang làm rất tốt! Hãy tiếp tục nhé!",
    "💙 Mỗi hơi thở đều là một món quà cho bản thân.",
    # ... (các tin nhắn khác) ...
]
ASSISTANT_AVATARS = ["🤖", "😊", "🌟", "💙", "🌸", "✨"]

# --- HÀM TEXT-TO-SPEECH CẢI TIẾN ---

def validate_text_input(text):
    if text is None: return False, "", "text_is_none"
    if not isinstance(text, str): return False, "", "text_not_string"
    try:
        cleaned_text = text.strip()
        if not cleaned_text: return False, "", "text_empty_after_strip"
        if len(cleaned_text) < 2: return False, "", "text_too_short"
        return True, cleaned_text, "valid"
    except Exception as e: return False, "", "text_validation_error"

def check_network_connectivity():
    try:
        response = requests.get("https://translate.google.com", timeout=3)
        return response.status_code == 200
    except: return False

# --- 5. SỬA LỖI ÂM THANH: DÙNG TEMPFILE THAY VÌ BYTESIO ---
def gtts_with_diagnostics(text):
    """Tạo âm thanh bằng gTTS (SỬA LẠI DÙNG TEMPFILE cho điện thoại)"""
    if not GTTS_AVAILABLE:
        return None, "gTTS không có sẵn trong hệ thống"
    
    is_valid, cleaned_text, validation_error = validate_text_input(text)
    if not is_valid:
        print(f"[gTTS] Input validation failed: {validation_error}")
        return None, validation_error
    
    if not check_network_connectivity():
        return None, "network_error"
    
    temp_path = "" # Khởi tạo
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            temp_path = tmp_file.name
        tts = gTTS(text=cleaned_text, lang='vi', slow=False)
        tts.save(temp_path)
        
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            try: os.unlink(temp_path)
            except: pass
            return audio_data, "success"
        else:
            try: os.unlink(temp_path)
            except: pass
            return None, "no_audio_generated"
            
    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            try: os.unlink(temp_path)
            except: pass
        error_str = str(e).lower()
        if "connection" in error_str: return None, "network_error"
        else: return None, f"unknown_error: {str(e)}"

def edge_tts_with_diagnostics(text, voice="vi-VN-HoaiMyNeural", rate=0):
    if not EDGE_TTS_AVAILABLE:
        return None, "edge_tts_not_available"
    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
            temp_path = temp_file.name
        rate_str = f"{'+' if rate >= 0 else ''}{rate}%"
        cmd = ["edge-tts", "--voice", voice, "--rate", rate_str, "--text", text, "--write-media", temp_path]
        subprocess.run(cmd, check=True, capture_output=True, timeout=10)
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
            with open(temp_path, 'rb') as f: audio_data = f.read()
            try: os.unlink(temp_path)
            except: pass
            return audio_data, "success"
        else:
            try: os.unlink(temp_path)
            except: pass
            return None, "no_audio_file_generated"
    except Exception as e:
        if temp_path and os.path.exists(temp_path):
            try: os.unlink(temp_path)
            except: pass
        return None, f"edge_tts_error: {str(e)}"

@st.cache_data
def text_to_speech_enhanced(text):
    is_valid, cleaned_text, validation_error = validate_text_input(text)
    if not is_valid: return None, validation_error
    if EDGE_TTS_AVAILABLE:
        audio_data, error_code = edge_tts_with_diagnostics(cleaned_text)
        if audio_data: return audio_data, "success_edge_tts"
    if GTTS_AVAILABLE:
        audio_data, error_code = gtts_with_diagnostics(cleaned_text)
        if audio_data: return audio_data, "success_gtts"
        else: return None, error_code
    return None, "no_tts_available"
    
def get_error_message(error_code):
    error_messages = { "text_is_none": "💭 Chưa có nội dung để đọc.", "network_error": "🌐 Không thể kết nối internet.", }
    if error_code.startswith("unknown_error:"): return "🔍 Có lỗi không xác định."
    return error_messages.get(error_code, f"🔊 Lỗi âm thanh ({error_code}).")

def create_tts_button_enhanced(text, key_suffix, button_text="🔊 Đọc to"):
    is_valid, cleaned_text, validation_error = validate_text_input(text)
    if not is_valid: return
    
    if st.button(button_text, key=f"tts_enhanced_{key_suffix}", help="Nhấn để nghe nội dung"):
        with st.spinner("🎵 Đang tạo âm thanh..."):
            audio_data, result_code = text_to_speech_enhanced(text)
            
            if audio_data and result_code.startswith("success"):
                if "edge_tts" in result_code: st.success("🎵 Đã tạo âm thanh bằng Edge TTS")
                else: st.success("🎵 Đã tạo âm thanh bằng Google TTS")
                
                # --- 6. SỬA LỖI ÂM THANH: XÓA AUTOPLAY=TRUE ---
                st.audio(audio_data, format="audio/mpeg") 
            else:
                error_msg = get_error_message(result_code)
                if "network" in result_code.lower(): st.error(error_msg)
                else: st.info(error_msg)

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    create_tts_button_enhanced(text, key_suffix, button_text)
@st.cache_data  
def text_to_speech(text):
    audio_data, result_code = text_to_speech_enhanced(text)
    return audio_data if audio_data else None


# --- CSS CHO GIAO DIỆN THÂN THIỆN ---
st.markdown("""
<style>
    /* (CSS .stButton > button đã bị xóa khỏi đây) */

    .assistant-card {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        border-radius: 20px; padding: 2rem; margin: 1.5rem 0;
        border: 3px solid #e1bee7;
        box-shadow: 0 6px 20px rgba(156,39,176,0.3);
        animation: gentleGlow 3s ease-in-out infinite alternate;
        position: relative; overflow: hidden;
    }
    .assistant-card::before {
        content: ''; position: absolute;
        top: -2px; left: -2px; right: -2px; bottom: -2px;
        background: linear-gradient(45deg, #9c27b0, #e91e63, #2196f3, #4caf50);
        border-radius: 22px; z-index: -1;
        animation: borderGlow 4s linear infinite;
    }
    @keyframes borderGlow { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    @keyframes gentleGlow { from { box-shadow: 0 4px 15px rgba(0,0,0,0.1); } to { box-shadow: 0 6px 20px rgba(156,39,176,0.2); } }
    .assistant-avatar {
        font-size: 4rem; display: block; text-align: center;
        margin-bottom: 1rem; animation: bounce 2s infinite;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.3));
    }
    @keyframes bounce { 0%, 20%, 50%, 80%, 100% { transform: translateY(0); } 40% { transform: translateY(-10px); } 60% { transform: translateY(-5px); } }
    .assistant-message {
        text-align: center; font-size: 1.3rem; font-weight: 700;
        color: #4a148c; margin-bottom: 1.5rem; line-height: 1.8;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .exercise-card {
        background: linear-gradient(145deg, #fff3e0 0%, #e8f5e8 100%);
        border-radius: 15px; padding: 1.5rem; margin: 1rem 0;
        border-left: 5px solid #4caf50;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .big-friendly-button {
        background: linear-gradient(135deg, #4caf50 0%, #8bc34a 100%);
        color: white; border: none; border-radius: 25px; padding: 1rem 2rem;
        font-size: 1.2rem; font-weight: 600; cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(76,175,80,0.3);
        width: 100%; margin: 0.5rem 0;
    }
    .big-friendly-button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(76,175,80,0.4); }
    .progress-container { background: #f5f5f5; border-radius: 10px; padding: 1rem; margin: 1rem 0; text-align: center; }
    .inclusive-instruction {
        background: #e1f5fe; border-radius: 10px; padding: 1rem;
        margin: 0.5rem 0; border-left: 4px solid #03a9f4;
        font-size: 1.1rem; line-height: 1.8;
    }
    
    /* --- 7. THÊM CSS TƯƠNG THÍCH ĐIỆN THOẠI --- */
    @media (max-width: 900px) {
        .assistant-card {
            padding: 1.5rem 1rem;
            max-width: 96vw;
        }
        .assistant-avatar {
            font-size: 3rem;
        }
        .assistant-message {
            font-size: 1.1rem;
        }
        .exercise-card, .inclusive-instruction, .progress-container, .assistant-card {
            padding: 1rem 0.8rem;
            font-size: 1rem;
            max-width: 96vw;
        }
        .inclusive-instruction h4 {
            font-size: 1.1rem;
        }
        /* Làm cho nút to ban đầu nhỏ lại trên điện thoại */
        .stButton > button {
            font-size: 1.1rem !important;
            padding: 1rem 1.5rem !important;
            min-height: 50px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# --- TRỢ LÝ ẢO ĐỘNG VIÊN ---
def show_virtual_assistant():
    if 'current_avatar' not in st.session_state:
        st.session_state.current_avatar = random.choice(ASSISTANT_AVATARS)
    if 'current_message' not in st.session_state:
        st.session_state.current_message = random.choice(ENCOURAGEMENT_MESSAGES)
    
    st.markdown(f"""
    <div class="assistant-card">
        <div class="assistant-avatar">{st.session_state.current_avatar}</div>
        <div class="assistant-message">{st.session_state.current_message}</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Thông điệp mới", help="Nhận thông điệp động viên mới"):
            st.session_state.current_avatar = random.choice(ASSISTANT_AVATARS)
            st.session_state.current_message = random.choice(ENCOURAGEMENT_MESSAGES)
            st.rerun()
    with col2:
        create_tts_button(st.session_state.current_message, "assistant_msg", "🔊 Nghe động viên")

# --- GIAO DIỆN CHÍNH ---
st.title("🫧 Góc An Yên")

# --- 8. SỬA LỖI ĐƯỜNG DẪN LINK ---
st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

show_virtual_assistant()
st.write("---")

description_text = """
Chào mừng đến với Góc An Yên đặc biệt dành cho các bạn học sinh! 
Đây là không gian an toàn để bạn thư giãn, tìm lại sự bình yên và chăm sóc cảm xúc của mình.
Chúng mình sẽ cùng nhau thực hành những bài tập đơn giản và hiệu quả nhé!
"""
st.markdown(f'<div class="inclusive-instruction">{description_text}</div>', unsafe_allow_html=True)
create_tts_button(description_text, "main_desc", "🔊 Nghe mô tả")

st.write("---")

# --- CÁC TAB CHỨC NĂNG ---
tab1, tab2, tab3 = st.tabs(["🌬️ Hơi Thở Nhiệm Màu", "🖐️ Chạm Vào Hiện Tại", "🖼️ Ô Cửa Sổ Thần Kỳ"])

# --- TAB 1: BÀI TẬP HÍT THỞ (Giữ nguyên logic) ---
with tab1:
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.header("🌬️ Hơi Thở Nhiệm Màu")
    
    instruction_text = """
    Bài tập thở hộp sẽ giúp bạn cảm thấy bình tĩnh và thư giãn hơn. 
    Đây là cách thực hành rất đơn giản và hiệu quả. 
    Hãy tìm một chỗ ngồi thoải mái và cùng thực hành nhé!
    """
    st.markdown(f'<div class="inclusive-instruction">{instruction_text}</div>', unsafe_allow_html=True)
    create_tts_button(instruction_text, "breathing_instruction")
    st.markdown('</div>', unsafe_allow_html=True)

    steps_text = """
    Các bước thực hành:
    1. Hít vào trong 4 giây - tưởng tượng hơi thở như ánh sáng dịu nhẹ
    2. Giữ hơi trong 4 giây - cảm nhận sự bình yên trong cơ thể
    3. Thở ra trong 4 giây - thả bỏ mọi căng thẳng và lo lắng  
    4. Nghỉ 4 giây - tận hưởng khoảnh khắc tĩnh lặng
    """
    st.markdown(f'<div class="inclusive-instruction">{steps_text}</div>', unsafe_allow_html=True)
    create_tts_button(steps_text, "breathing_steps")

    duration = st.select_slider(
        "Chọn thời gian thực hành (giây):",
        options=[60, 120, 180], value=60,
        help="Thời gian càng dài, hiệu quả càng tốt. Bạn hãy chọn theo khả năng của mình nhé!"
    )

    if st.button("🌟 Bắt đầu hít thở", type="primary", use_container_width=True):
        placeholder = st.empty()
        progress_bar = st.progress(0, text="Chuẩn bị bắt đầu...")
        start_time = time.time()
        end_time = start_time + duration
        while time.time() < end_time:
            steps = [
                ("Hít vào nhẹ nhàng (4s)", "💨", "#e3f2fd"), 
                ("Giữ hơi thở (4s)", "⏸️", "#f3e5f5"), 
                ("Thở ra từ từ (4s)", "🌊", "#e8f5e8"), 
                ("Nghỉ và cảm nhận (4s)", "✨", "#fff3e0")
            ]
            for step_text, emoji, bg_color in steps:
                if time.time() >= end_time: break
                with placeholder.container():
                    st.markdown(f"""
                    <div style="background: {bg_color}; padding: 2rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
                        <div style="font-size: 4rem; margin-bottom: 1rem;">{emoji}</div>
                        <h2 style="color: #4a148c; margin-bottom: 1rem;">{step_text}</h2>
                        <p style="font-size: 1.1rem; color: #666;">Hãy theo dõi hơi thở và cảm nhận sự thư giãn</p>
                    </div>
                    """, unsafe_allow_html=True)
                step_start_time = time.time()
                while time.time() < step_start_time + 4:
                    if time.time() >= end_time: break
                    progress_percent = (time.time() - start_time) / duration
                    progress_bar.progress(min(progress_percent, 1.0), text=f"Đang thực hành: {step_text}")
                    time.sleep(0.1)
        with placeholder.container():
            st.markdown("""
            <div style="background: linear-gradient(135deg, #c8e6c9 0%, #dcedc8 100%); padding: 2rem; border-radius: 15px; text-align: center;">
                <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
                <h2 style="color: #2e7d32;">Tuyệt vời! Bạn đã hoàn thành!</h2>
                <p style="font-size: 1.2rem; color: #388e3c;">Hãy cảm nhận sự bình yên và thư giãn trong cơ thể nhé. Bạn đã làm rất tốt!</p>
            </div>
            """, unsafe_allow_html=True)
        progress_bar.progress(100, text="Hoàn thành rồi! 🎉")
        completion_text = "Tuyệt vời! Bạn đã hoàn thành bài tập hít thở. Hãy cảm nhận sự bình yên và thư giãn trong cơ thể nhé."
        create_tts_button(completion_text, "completion_breathing")
        st.write("---")
        if st.button("💬 Chia sẻ cảm nhận", key="share_breathing", use_container_width=True):
            st.session_state.show_breathing_sharing = True
            st.rerun()

    if st.session_state.get("show_breathing_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn:")
        feeling_content = st.text_area("Cảm nhận của bạn:", placeholder="Ví dụ: Sau khi thực hành, tôi cảm thấy bình tĩnh hơn...", key="breathing_feeling")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký", key="save_breathing", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Hơi Thở Nhiệm Màu", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký!")
                    st.session_state.show_breathing_sharing = False
                    time.sleep(1); st.rerun()
                else: st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        with col2:
            if st.button("❌ Hủy", key="cancel_breathing", use_container_width=True):
                st.session_state.show_breathing_sharing = False
                st.rerun()

# --- TAB 2: BÀI TẬP 5-4-3-2-1 (Giữ nguyên logic) ---
with tab2:
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.header("🖐️ Chạm Vào Hiện Tại (5-4-3-2-1)")
    instruction_541 = """
    Bài tập 5-4-3-2-1 giúp bạn tập trung vào thời điểm hiện tại bằng cách sử dụng các giác quan.
    Đây là cách tuyệt vời để làm dịu tâm trí khi bạn cảm thấy lo lắng hoặc căng thẳng.
    Hãy cùng thực hành từng bước một cách nhẹ nhàng nhé!
    """
    st.markdown(f'<div class="inclusive-instruction">{instruction_541}</div>', unsafe_allow_html=True)
    create_tts_button(instruction_541, "541_instruction")
    st.markdown('</div>', unsafe_allow_html=True)
    steps_541 = [
        ("👀 5 thứ bạn có thể THẤY", "Ví dụ: cái bàn, cây bút, bức tranh, cửa sổ, chiếc lá."),
        ("🖐️ 4 thứ bạn có thể CHẠM", "Ví dụ: mặt bàn láng mịn, vải quần jean, làn gió mát, ly nước lạnh."),
        ("👂 3 thứ bạn có thể NGHE", "Ví dụ: tiếng chim hót, tiếng quạt máy, tiếng gõ phím."),
        ("👃 2 thứ bạn có thể NGỬI", "Ví dụ: mùi cà phê, mùi sách cũ, mùi cỏ cây sau mưa."),
        ("👅 1 thứ bạn có thể NẾM", "Ví dụ: vị ngọt của trà, vị thanh của nước lọc.")
    ]
    for i, (step_title, step_example) in enumerate(steps_541, 1):
        with st.container():
            st.markdown(f"""
            <div class="inclusive-instruction" style="background: linear-gradient(135deg, #e1f5fe 0%, #f3e5f5 100%);">
                <h4>{step_title}</h4>
                <p>{step_example}</p>
            </div>
            """, unsafe_allow_html=True)
            step_text = f"Bước {i}: {step_title}. {step_example}"
            create_tts_button(step_text, f"step_541_{i}")
    completion_541 = "Tuyệt vời! Bạn đã kết nối thành công với hiện tại. Cảm nhận sự bình yên trong thời khắc này!"
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #c8e6c9 0%, #dcedc8 100%); padding: 1.5rem; border-radius: 15px; text-align: center; margin: 1rem 0;">
        <h3 style="color: #2e7d32;">🎉 {completion_541}</h3>
    </div>
    """, unsafe_allow_html=True)
    create_tts_button(completion_541, "completion_541")
    if st.button("💬 Chia sẻ cảm nhận", key="share_543", use_container_width=True):
        st.session_state.show_543_sharing = True
        st.rerun()
    if st.session_state.get("show_543_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn:")
        feeling_content = st.text_area("Cảm nhận của bạn:", placeholder="Ví dụ: Bài tập giúp tôi tập trung vào hiện tại...", key="543_feeling")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký", key="save_543", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Chạm Vào Hiện Tại (5-4-3-2-1) - Hòa Nhập", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký!")
                    st.session_state.show_543_sharing = False
                    time.sleep(1); st.rerun()
                else: st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        with col2:
            if st.button("❌ Hủy", key="cancel_observation", use_container_width=True): # Sửa key
                st.session_state.show_543_sharing = False
                st.rerun()

# --- TAB 3: BÀI TẬP QUAN SÁT (Giữ nguyên logic) ---
with tab3:
    st.markdown('<div class="exercise-card">', unsafe_allow_html=True)
    st.header("🖼️ Ô Cửa Sổ Thần Kỳ")
    instruction_window = """
    Bài tập quan sát này rất đơn giản và thú vị! Bạn sẽ dành một phút để nhìn ra ngoài 
    và thực hành quan sát không phán xét. Đây là cách tuyệt vời để thư giãn tâm trí 
    và kết nối với thế giới xung quanh.
    """
    st.markdown(f'<div class="inclusive-instruction">{instruction_window}</div>', unsafe_allow_html=True)
    create_tts_button(instruction_window, "window_instruction")
    st.markdown('</div>', unsafe_allow_html=True)
    detailed_guide = """
    Hướng dẫn chi tiết:
    1. Hãy dành một phút nhìn ra ngoài cửa sổ hoặc xung quanh bạn
    2. Đừng cố gắng đặt tên cho những gì bạn thấy
    3. Chỉ cần chú ý đến màu sắc, hình dạng và sự chuyển động
    4. Hãy nhìn mọi thứ như thể bạn đang thấy chúng lần đầu tiên
    5. Cảm nhận sự kỳ diệu trong những điều đơn giản
    """
    st.markdown(f'<div class="inclusive-instruction">{detailed_guide}</div>', unsafe_allow_html=True)
    create_tts_button(detailed_guide, "window_guide")
    if st.button("🌟 Bắt đầu 1 phút quan sát", type="primary", key="quan_sat", use_container_width=True):
        progress_bar = st.progress(0)
        status_placeholder = st.empty()
        for i in range(61):
            progress_value = i / 60.0
            progress_bar.progress(min(progress_value, 1.0))
            encouragements = [
                "Hãy để mắt bạn khám phá tự nhiên...",
                "Chú ý đến những màu sắc xung quanh...",
                "Quan sát không cần phán xét...",
                "Cảm nhận sự bình yên trong quan sát...",
                "Để tâm trí thư giãn và thoải mái..."
            ]
            current_encouragement = encouragements[i // 12] if i // 12 < len(encouragements) else encouragements[-1]
            status_placeholder.markdown(f"""
            <div style="text-align: center; padding: 1rem; background: #e3f2fd; border-radius: 10px;">
                <h4 style="color: #1976d2;">⏰ Thời gian còn lại: {60-i} giây</h4>
                <p style="color: #1565c0; font-style: italic;">{current_encouragement}</p>
            </div>
            """, unsafe_allow_html=True)
            time.sleep(1)
        status_placeholder.markdown("""
        <div style="background: linear-gradient(135deg, #c8e6c9 0%, #dcedc8 100%); padding: 2rem; border-radius: 15px; text-align: center;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎊</div>
            <h2 style="color: #2e7d32;">Đã hết một phút!</h2>
            <p style="font-size: 1.2rem; color: #388e3c;">Cảm ơn bạn đã dành thời gian cho chính mình. Hy vọng bạn cảm thấy thư giãn và bình yên! ❤️</p>
        </div>
        """, unsafe_allow_html=True)
        completion_window = "Đã hết một phút quan sát! Cảm ơn bạn đã dành thời gian cho chính mình. Hy vọng bạn cảm thấy thư giãn và bình yên!"
        create_tts_button(completion_window, "completion_window")
        st.write("---")
        if st.button("💬 Chia sẻ cảm nhận", key="share_observation", use_container_width=True):
            st.session_state.show_observation_sharing = True
            st.rerun()
    if st.session_state.get("show_observation_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn:")
        feeling_content = st.text_area("Cảm nhận của bạn:", placeholder="Ví dụ: Khi quan sát không phán xét, tôi cảm thấy thư giãn...", key="observation_feeling")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký", key="save_observation", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Ô Cửa Sổ Thần Kỳ - Hòa Nhập", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký!")
                    st.session_state.show_observation_sharing = False
                    time.sleep(1); st.rerun()
                else: st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        with col2:
            if st.button("❌ Hủy", key="cancel_observation", use_container_width=True):
                st.session_state.show_observation_sharing = False
                st.rerun()

# --- PHẦN XEM LỊCH SỬ (Giữ nguyên logic) ---
st.write("---")
st.header("📖 Lịch Sử Góc An Yên")
history_description = "Xem lại những cảm nhận và trải nghiệm của bạn từ các bài tập trong Góc An Yên dành cho học sinh hòa nhập."
st.markdown(f'<div class="inclusive-instruction">{history_description}</div>', unsafe_allow_html=True)
create_tts_button(history_description, "history_desc")

if st.button("📖 Xem lịch sử của tôi", use_container_width=True):
    st.session_state.show_history = not st.session_state.get("show_history", False)

if st.session_state.get("show_history", False):
    st.markdown("### 💭 Các cảm nhận đã lưu:")
    all_entries = get_mood_entries()
    inclusive_exercises = [
        "Hơi Thở Nhiệm Màu", 
        "Chạm Vào Hiện Tại (5-4-3-2-1) - Hòa Nhập", 
        "Ô Cửa Sổ Thần Kỳ - Hòa Nhập"
    ]
    inclusive_entries = [entry for entry in all_entries if entry["exercise_type"] in inclusive_exercises]
    if inclusive_entries:
        inclusive_entries.sort(key=lambda x: x["timestamp"], reverse=True)
        for entry in inclusive_entries:
            with st.container():
                if "Hơi Thở" in entry["exercise_type"]: icon, bg_color = "🌬️", "#e3f2fd"
                elif "Chạm Vào Hiện Tại" in entry["exercise_type"]: icon, bg_color = "🖐️", "#f3e5f5"
                else: icon, bg_color = "🖼️", "#e8f5e8"
                st.markdown(f"""
                <div style="background-color: {bg_color}; border-left: 4px solid #9c27b0; 
                            padding: 1.5rem; border-radius: 12px; margin-bottom: 15px;
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <div style="font-size: 1rem; color: #666; margin-bottom: 8px; font-weight: 600;">
                        {icon} <strong>{entry["exercise_type"]}</strong> • {entry["timestamp"]}
                    </div>
                    <div style="color: #333; line-height: 1.6; font-size: 1.1rem;">
                        {entry["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                create_tts_button(f"Cảm nhận từ {entry['exercise_type']}: {entry['content']}", f"entry_{entry['timestamp']}")
            st.write("")
    else:
        st.markdown("""
        <div style="background: #fff3e0; padding: 2rem; border-radius: 15px; text-align: center; border: 2px dashed #ff9800;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🌱</div>
            <h3 style="color: #f57c00;">Chưa có cảm nhận nào!</h3>
            <p style="color: #ef6c00; font-size: 1.1rem;">Hãy thực hành một bài tập và chia sẻ cảm nhận của bạn nhé!</p>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 Làm mới lịch sử", key="refresh_history"):
        st.rerun()
