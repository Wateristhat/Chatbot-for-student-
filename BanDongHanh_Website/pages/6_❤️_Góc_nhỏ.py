import streamlit as st
import sys
import os
from datetime import date, datetime, timedelta
import json
from gtts import gTTS
from io import BytesIO

# Add parent directory to path for database import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import (
    get_or_create_user, save_daily_plan, get_daily_plan, 
    update_completed_actions, get_action_history, 
    get_pending_reminders, mark_reminder_shown,
    check_incomplete_plans
)

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Góc nhỏ của bạn", page_icon="❤️", layout="centered")

# --- CSS CHO GIAO DIỆN HÒA NHẬP ---
st.markdown("""
<style>
    /* Giao diện chính thân thiện */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .description-card {
        background: linear-gradient(135deg, #E8F5E8 0%, #F0F8F0 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 6px solid #32CD32;
        font-size: 1.3rem;
        line-height: 1.8;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .action-card {
        background: #FFF8DC;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 3px solid #FFD700;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .action-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        border-color: #FFA500;
    }
    
    .action-icon {
        font-size: 2rem;
        margin-right: 1rem;
        vertical-align: middle;
    }
    
    .completed-action {
        background: linear-gradient(135deg, #98FB98 0%, #90EE90 100%) !important;
        border-color: #32CD32 !important;
        animation: completePulse 0.6s ease-in-out;
    }
    
    @keyframes completePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .reminder-card {
        background: linear-gradient(135deg, #FFE4E6 0%, #FFF0F0 100%);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid #FF69B4;
        font-size: 1.2rem;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(255,105,180,0.2);
        animation: gentleBounce 2s ease-in-out infinite;
    }
    
    @keyframes gentleBounce {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-3px); }
    }
    
    .history-card {
        background: #F0F8FF;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #4169E1;
        font-size: 1.1rem;
    }
    
    .tts-button {
        background: linear-gradient(135deg, #87CEEB 0%, #4682B4 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.7rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(70,130,180,0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .tts-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(70,130,180,0.4) !important;
    }
    
    .celebration {
        animation: celebrate 0.8s ease-in-out;
        background: linear-gradient(45deg, #FFD700, #FF69B4, #32CD32, #FF6347) !important;
        background-size: 400% 400% !important;
        animation: celebration-gradient 2s ease infinite !important;
    }
    
    @keyframes celebration-gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .large-text {
        font-size: 1.2rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #32CD32, #FFD700, #FF69B4);
        margin: 2rem 0;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- HÀM TEXT-TO-SPEECH ---
@st.cache_data
def text_to_speech(text):
    """Chuyển văn bản thành giọng nói."""
    if not text or not text.strip():
        return None
    
    try:
        audio_bytes = BytesIO()
        tts = gTTS(text=text.strip(), lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        return audio_bytes.read()
    except Exception as e:
        return None

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    """Tạo nút đọc to cho văn bản."""
    if st.button(button_text, key=f"tts_{key_suffix}", help="Nhấn để nghe hướng dẫn", 
                 use_container_width=False):
        if not text or not text.strip():
            st.info("💭 Chưa có nội dung để đọc. Hãy thử lại khi có văn bản!")
            return
        
        with st.spinner("🎵 Đang chuẩn bị âm thanh..."):
            audio_data = text_to_speech(text)
            if audio_data:
                st.audio(audio_data, format="audio/mp3")
            else:
                st.info("🎵 Hiện tại không thể tạo âm thanh. Bạn có thể đọc nội dung ở trên nhé!")

# --- GIAO DIỆN CHÍNH ---
st.markdown('<div class="main-header">❤️ Góc nhỏ của bạn</div>', unsafe_allow_html=True)

# Nút quay về trang chủ (hiển thị trong ứng dụng chính)
if hasattr(st, '_get_query_params'):
    try:
        st.page_link("pages/0_💖_Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")
    except:
        st.markdown("🏠 **[⬅️ Quay về Trang chủ](../0_💖_Trang_chủ.py)**")

# Mô tả chính với TTS
main_description = "Chăm sóc bản thân không phải là ích kỷ, đó là điều cần thiết. Hãy bắt đầu với những hành động nhỏ mỗi ngày nhé. Bee sẽ giúp bạn tạo thói quen tốt và nhắc nhở bạn mỗi ngày!"

st.markdown(f'<div class="description-card">{main_description}</div>', unsafe_allow_html=True)

# Nút đọc to cho mô tả chính
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    create_tts_button(main_description, "main_desc")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- QUẢN LÝ NGƯỜI DÙNG ---
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
    st.session_state.user_id = None

# Input tên người dùng
if not st.session_state.current_user:
    st.subheader("👋 Xin chào! Bạn tên gì?")
    col1, col2 = st.columns([3, 1])
    with col1:
        username_input = st.text_input(
            "Nhập tên của bạn để Bee có thể nhắc nhở bạn cá nhân:",
            placeholder="Ví dụ: Hoa, Minh, Lan...",
            key="username_input"
        )
    with col2:
        if st.button("✨ Bắt đầu", use_container_width=True):
            if username_input and username_input.strip():
                st.session_state.current_user = username_input.strip()
                st.session_state.user_id = get_or_create_user(username_input.strip())
                st.rerun()
            else:
                st.warning("Hãy nhập tên của bạn nhé!")
    
    st.info("💡 Bee cần biết tên bạn để có thể lưu kế hoạch và nhắc nhở bạn mỗi ngày!")
    st.stop()

# Hiển thị thông tin người dùng
st.success(f"🌟 Chào bạn {st.session_state.current_user}! Hãy cùng lập kế hoạch chăm sóc bản thân nhé!")

# Kiểm tra nhắc nhở chưa hiển thị
if st.session_state.user_id:
    check_incomplete_plans()  # Kiểm tra và tạo nhắc nhở nếu cần
    pending_reminders = get_pending_reminders(st.session_state.user_id)
    
    for reminder in pending_reminders:
        st.markdown(f'<div class="reminder-card">🐝 {reminder["message"]}</div>', 
                   unsafe_allow_html=True)
        mark_reminder_shown(reminder['id'])

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- NGÂN HÀNG HÀNH ĐỘNG ---
# Ngân hàng các hành động nhỏ để tự chăm sóc với emoji minh họa
MICRO_ACTIONS = [
    {"text": "Uống một ly nước đầy", "emoji": "💧", "encouragement": "Tuyệt vời! Cơ thể bạn đang được hydrat hóa!"},
    {"text": "Vươn vai và duỗi người trong 1 phút", "emoji": "🤸‍♀️", "encouragement": "Tuyệt! Cơ thể bạn đang thư giãn!"},
    {"text": "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp", "emoji": "☁️", "encouragement": "Thật tuyệt! Bạn đã dành thời gian cho thiên nhiên!"},
    {"text": "Nghe một bài hát bạn yêu thích", "emoji": "🎵", "encouragement": "Tuyệt vời! Âm nhạc nuôi dưỡng tâm hồn bạn!"},
    {"text": "Viết ra 1 điều bạn tự hào về bản thân", "emoji": "📝", "encouragement": "Thật tuyệt! Bạn đáng được tự hào về mình!"},
    {"text": "Rửa mặt với nước mát", "emoji": "😊", "encouragement": "Tuyệt! Bạn đã làm mới bản thân!"},
    {"text": "Sắp xếp lại góc học tập/làm việc", "emoji": "📚", "encouragement": "Tuyệt vời! Không gian gọn gàng giúp tâm trí thư thái!"},
    {"text": "Mỉm cười với chính mình trong gương", "emoji": "😄", "encouragement": "Tuyệt vời! Nụ cười của bạn rạng rỡ lắm!"}
]

# --- PHẦN LÊN KẾ HOẠCH ---
st.header("🎯 Xây dựng kế hoạch chăm sóc bản thân hôm nay")

plan_instruction = "Hãy chọn những việc nhỏ bạn muốn làm hôm nay để chăm sóc bản thân. Mỗi việc nhỏ đều có ý nghĩa lớn!"
st.markdown(f'<div class="large-text">{plan_instruction}</div>', unsafe_allow_html=True)

# TTS cho hướng dẫn
create_tts_button(plan_instruction, "plan_instruction")

# Lấy kế hoạch hiện tại từ database
current_plan = get_daily_plan(st.session_state.user_id) if st.session_state.user_id else {'selected_actions': [], 'completed_actions': []}

# Khởi tạo session state từ database
if 'selected_actions' not in st.session_state:
    st.session_state.selected_actions = current_plan['selected_actions']

if 'completed_actions' not in st.session_state:
    st.session_state.completed_actions = current_plan['completed_actions']

# Tạo checkboxes cho từng hành động với emoji
st.subheader("🌈 Ngân hàng hành động chăm sóc bản thân:")

actions_display = []
for action_data in MICRO_ACTIONS:
    actions_display.append(f"{action_data['emoji']} {action_data['text']}")

selected = st.multiselect(
    "Chọn các hành động bạn muốn làm:",
    options=actions_display,
    default=st.session_state.selected_actions,
    placeholder="💫 Nhấn vào đây để chọn những việc nhỏ...",
    help="Bạn có thể chọn nhiều hành động để tạo thành kế hoạch của riêng mình!"
)

# Cập nhật selected_actions và lưu vào database
if selected != st.session_state.selected_actions:
    st.session_state.selected_actions = selected
    if st.session_state.user_id:
        save_daily_plan(st.session_state.user_id, selected)
    st.rerun()

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- PHẦN HIỂN THỊ CHECKLIST ---
if not st.session_state.selected_actions:
    st.info("💡 Hãy chọn ít nhất một hành động để bắt đầu kế hoạch chăm sóc bản thân của bạn nhé!")
else:
    st.subheader("📋 Danh sách việc cần làm của bạn hôm nay:")
    
    # Tạo mapping từ display text về action data
    action_mapping = {}
    for action_data in MICRO_ACTIONS:
        display_text = f"{action_data['emoji']} {action_data['text']}"
        action_mapping[display_text] = action_data
    
    all_done = True
    completed_count = 0
    
    for action_display in st.session_state.selected_actions:
        action_data = action_mapping.get(action_display, {"text": action_display, "emoji": "✨", "encouragement": "Tuyệt vời!"})
        
        # Khởi tạo trạng thái checkbox
        if f"action_{action_display}" not in st.session_state:
            st.session_state[f"action_{action_display}"] = action_display in st.session_state.completed_actions
        
        col1, col2 = st.columns([4, 1])
        with col1:
            is_done = st.checkbox(
                action_display,
                key=f"cb_{action_display}",
                value=st.session_state[f"action_{action_display}"]
            )
        
        with col2:
            # TTS cho từng hành động
            create_tts_button(action_data["text"], f"action_{hash(action_display)}")
        
        # Kiểm tra thay đổi trạng thái và hiển thị popup động viên
        if is_done and not st.session_state[f"action_{action_display}"]:
            # Vừa hoàn thành
            st.balloons()
            st.success(f"🎉 {action_data['encouragement']}")
            
            # Cập nhật completed_actions
            if action_display not in st.session_state.completed_actions:
                st.session_state.completed_actions.append(action_display)
                if st.session_state.user_id:
                    update_completed_actions(st.session_state.user_id, st.session_state.completed_actions)
        
        elif not is_done and st.session_state[f"action_{action_display}"]:
            # Vừa bỏ tick
            if action_display in st.session_state.completed_actions:
                st.session_state.completed_actions.remove(action_display)
                if st.session_state.user_id:
                    update_completed_actions(st.session_state.user_id, st.session_state.completed_actions)
        
        st.session_state[f"action_{action_display}"] = is_done
        
        if is_done:
            completed_count += 1
        else:
            all_done = False

    # Hiển thị tiến độ
    progress = completed_count / len(st.session_state.selected_actions) if st.session_state.selected_actions else 0
    st.progress(progress)
    st.write(f"✅ Đã hoàn thành: {completed_count}/{len(st.session_state.selected_actions)} việc")
    
    # Celebration khi hoàn thành tất cả
    if all_done and len(st.session_state.selected_actions) > 0:
        st.markdown('<div class="celebration">', unsafe_allow_html=True)
        st.success("🎊 CHÚC MỪNG! Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!")
        st.markdown("🌟 **Bạn thật tuyệt vời! Hãy tự thưởng cho bản thân nhé!** 🌟")
        st.markdown('</div>', unsafe_allow_html=True)
        st.balloons()
        
        # TTS cho lời chúc mừng
        celebration_text = "Chúc mừng! Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay! Bạn thật tuyệt vời!"
        create_tts_button(celebration_text, "celebration")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- PHẦN LỊCH SỬ HÀNH ĐỘNG ---
if st.session_state.user_id:
    st.header("📚 Lịch sử hành động của bạn (30 ngày gần nhất)")
    
    if st.button("📖 Xem lịch sử của tôi", use_container_width=True):
        st.session_state.show_history = not st.session_state.get("show_history", False)
    
    if st.session_state.get("show_history", False):
        history = get_action_history(st.session_state.user_id, 30)
        
        if history:
            st.subheader("🌟 Những hành động tuyệt vời bạn đã thực hiện:")
            
            # Nhóm theo ngày
            from collections import defaultdict
            history_by_date = defaultdict(list)
            
            for item in history:
                history_by_date[item['date']].append(item)
            
            # Hiển thị từ ngày gần nhất
            for date_str in sorted(history_by_date.keys(), reverse=True):
                st.markdown(f"**📅 {date_str}:**")
                actions_on_date = history_by_date[date_str]
                
                for item in actions_on_date:
                    # Tìm emoji tương ứng
                    action_emoji = "✅"
                    for action_data in MICRO_ACTIONS:
                        if action_data['text'] in item['action']:
                            action_emoji = action_data['emoji']
                            break
                    
                    st.markdown(f'<div class="history-card">{action_emoji} {item["action"]}</div>', 
                               unsafe_allow_html=True)
                
                st.write("---")
        else:
            st.info("🌱 Chưa có lịch sử hành động. Hãy bắt đầu hoàn thành những hành động nhỏ từ hôm nay!")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- PHẦN HƯỚNG DẪN ---
st.header("💡 Hướng dẫn sử dụng")

guide_text = """
🔵 **Bước 1:** Nhập tên của bạn để Bee có thể nhắc nhở cá nhân
🔵 **Bước 2:** Chọn những việc nhỏ bạn muốn làm từ ngân hàng hành động
🔵 **Bước 3:** Đánh dấu ✅ khi hoàn thành mỗi việc
🔵 **Bước 4:** Nhận lời động viên từ Bee khi hoàn thành
🔵 **Bước 5:** Xem lại lịch sử để thấy sự tiến bộ của bản thân

💡 **Mẹo:** Nhấn nút 🔊 "Đọc to" bất cứ lúc nào để nghe hướng dẫn!
"""

st.markdown(f'<div class="description-card">{guide_text}</div>', unsafe_allow_html=True)

# TTS cho hướng dẫn
create_tts_button(guide_text.replace('🔵', '').replace('💡', ''), "guide")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666; font-size: 1.1rem;">
💚 <b>Nhớ rằng:</b> Những bước nhỏ cũng là những bước tiến lớn! 💚<br>
🐝 Bee luôn ở đây để đồng hành cùng bạn! 🐝
</div>
""", unsafe_allow_html=True)
