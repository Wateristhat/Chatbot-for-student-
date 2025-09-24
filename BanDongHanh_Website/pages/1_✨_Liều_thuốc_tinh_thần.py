import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="✨ Liều Thuốc Tinh Thần", page_icon="✨", layout="centered")

# --- CSS cho trợ lý ảo ở đầu trang ---
st.markdown("""
<style>
.lttt-title-feature {
    font-size:2.2rem; font-weight:700; color:#e53935; text-align:center; margin-bottom:1.3rem; margin-top:0.5rem;
    letter-spacing:0.2px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}
.lttt-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom:2.3rem; margin-top:0.1rem;
    text-align: center; border: 3.5px solid #e1bee7; max-width:950px; margin-left:auto; margin-right:auto;
}
.lttt-assist-icon {font-size:3.1rem; margin-bottom:0.7rem;}
.lttt-assist-text {font-size:1.45rem; font-weight:700; color:#6d28d9; margin-bottom:1.2rem;}
.lttt-assist-btn-row {display:flex; justify-content: center; gap: 50px; margin-top:1.25rem;}
.lttt-assist-action-btn {
    background: #fff; border: 2.5px solid #e1bee7; border-radius: 18px;
    font-size:1.19rem; font-weight:600; color:#6d28d9;
    padding: 1rem 2.1rem; cursor:pointer; box-shadow:0 2px 8px rgba(124,77,255,.14); transition:all 0.17s;
}
.lttt-assist-action-btn:hover {background:#f3e8ff;}
.page-title {display:none;}
</style>
""", unsafe_allow_html=True)

# --- Trợ lý ảo đầu trang ---
ASSISTANT_MESSAGES = [
    ("🤖", "🌟 Bạn đang làm rất tốt! Hãy tiếp tục nhé!"),
    ("🤖", "✨ Mỗi người đều cần được động viên. Bee luôn bên bạn!"),
    ("🤖", "🌈 Khó khăn chỉ là thử thách nhỏ, bạn sẽ vượt qua được!"),
    ("🤖", "💙 Mỗi hơi thở đều là một món quà cho bản thân."),
    ("🤖", "🦋 Từng bước nhỏ đều đưa bạn đến gần hơn với sự bình an."),
    ("🤖", "🌺 Bạn xứng đáng được yêu thương và quan tâm.")
]

if "current_assistant_message" not in st.session_state:
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)

# --- Tiêu đề tính năng ---
st.markdown(
    '<div class="lttt-title-feature">'
    ' <span style="font-size:2.2rem;">✨</span> Liều Thuốc Tinh Thần'
    '</div>',
    unsafe_allow_html=True
)

# --- Khung trợ lý ảo (đồng bộ Góc An Yên) ---
avatar, msg = st.session_state.current_assistant_message
st.markdown(f"""
<div class="lttt-assist-bigbox">
    <div class="lttt-assist-icon">{avatar}</div>
    <div class="lttt-assist-text">{msg}</div>
    <div class="lttt-assist-btn-row">
        <form method="post">
            <button class="lttt-assist-action-btn" type="submit" name="new_message" formnovalidate>🔄 Thông điệp mới</button>
        </form>
        <form method="post">
            <button class="lttt-assist-action-btn" type="submit" name="tts_message" formnovalidate>🔊 Nghe động viên</button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,2])
with col1:
    if st.button("🔄 Thông điệp mới", key="new_msg_top"):
        st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe động viên", key="tts_msg_top"):
        audio_bytes = BytesIO()
        tts = gTTS(text=msg, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format="audio/mp3")

# --- Giao diện chính ---
st.markdown('<div class="lttt-box">🐝 Chọn điều bạn cần nhất, Bee sẽ gửi động viên phù hợp! Bạn có thể nghe hoặc lưu lại nhé! 🌈</div>', unsafe_allow_html=True)

# --- DATA ---
LTTT_CATEGORIES = {
    "courage": {
        "label": "🐝 Cần Cổ Vũ",
        "icon": "🐝",
        "messages": [
            {"avatar": "🐝", "text": "Bee tin rằng bạn có thể làm được! Mỗi bước nhỏ đều rất quan trọng, cứ từ từ thôi nhé!", "name": "Ong Bee"},
            {"avatar": "🌟", "text": "Bạn là ngôi sao sáng nhất! Hãy tự tin tỏa sáng như chính mình nhé!", "name": "Sao sáng"},
            {"avatar": "🌈", "text": "Sau cơn mưa sẽ có cầu vồng! Khó khăn hôm nay sẽ là niềm vui ngày mai.", "name": "Cầu vồng"},
            {"avatar": "🦄", "text": "Bạn đặc biệt như kỳ lân! Không ai có thể thay thế được vị trí của bạn đâu!", "name": "Kỳ lân"}
        ]
    },
    "fun": {
        "label": "😊 Muốn Vui Vẻ", 
        "icon": "😊",
        "messages": [
            {"avatar": "🐧", "text": "Chim cánh cụt đi bộ lắc lư để không bị ngã. Bạn cũng cứ vui vẻ đi thôi!", "name": "Chim cánh cụt"},
            {"avatar": "🌻", "text": "Hoa hướng dương luôn quay về phía mặt trời! Hãy tìm điều tích cực nhé!", "name": "Hoa hướng dương"},
            {"avatar": "🎈", "text": "Khinh khí cầu bay cao vì chở đầy không khí vui! Bạn cũng bay cao thôi!", "name": "Khinh khí cầu"},
            {"avatar": "🐨", "text": "Gấu koala ngủ 20 tiếng/ngày mà vẫn hạnh phúc! Đôi khi chậm lại cũng tốt mà.", "name": "Gấu koala"}
        ]
    },
    "peace": {
        "label": "🫧 Tìm Bình Yên",
        "icon": "🫧", 
        "messages": [
            {"avatar": "🫧", "text": "Hãy thở sâu như những bong bóng bay... từ từ thôi, bạn đang làm rất tốt.", "name": "Bong bóng"},
            {"avatar": "🍃", "text": "Lá cây nhảy múa trong gió mà không gãy. Bạn cũng mềm mại và mạnh mẽ như vậy.", "name": "Lá cây"},
            {"avatar": "🌙", "text": "Trăng tròn hay trăng khuyết đều đẹp. Bạn lúc vui hay buồn cũng đều đáng yêu.", "name": "Trăng xinh"},
            {"avatar": "🕯️", "text": "Như ngọn nến nhỏ trong đêm tối, bạn có sức mạnh thầm lặng nhưng rất ấm áp.", "name": "Ngọn nến"}
        ]
    }
}
LTTT_CATEGORY_ORDER = ["courage", "fun", "peace"]

# --- SESSION STATE ---
if 'message_category' not in st.session_state:
    st.session_state.message_category = None
if 'current_message' not in st.session_state:
    st.session_state.current_message = None
if 'saved_encouragements' not in st.session_state:
    st.session_state.saved_encouragements = []
if 'show_journal' not in st.session_state:
    st.session_state.show_journal = False

# --- TTS động viên dưới ---
@st.cache_data
def create_audio_with_tts(text):
    if not text or not text.strip():
        return None
    audio_bytes = BytesIO()
    tts = gTTS(text=text.strip(), lang='vi', slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def play_encouragement_audio(message_data):
    full_text = f"{message_data['name']} nói: {message_data['text']}"
    with st.spinner("🎵 Đang chuẩn bị âm thanh cho bạn..."):
        audio_data = create_audio_with_tts(full_text)
        if audio_data:
            st.audio(audio_data, format="audio/mp3")
            st.balloons()
        else:
            st.info("🔊 Không thể tạo âm thanh. Bạn có thể đọc nội dung ở trên nhé!")

# --- CSV Nhật ký ---
def get_csv_path():
    return os.path.join(os.path.dirname(__file__), "..", "mood_journal.csv")

def ensure_csv_exists():
    csv_path = get_csv_path()
    if not os.path.exists(csv_path):
        df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
        df.to_csv(csv_path, index=False, encoding='utf-8')
    else:
        try:
            df = pd.read_csv(csv_path, encoding='utf-8')
            if list(df.columns) != ["Ngày giờ", "Loại", "Nội dung"]:
                backup_path = csv_path.replace('.csv', '_backup.csv')
                df.to_csv(backup_path, index=False, encoding='utf-8')
                df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
                df.to_csv(csv_path, index=False, encoding='utf-8')
        except Exception:
            df = pd.DataFrame(columns=["Ngày giờ", "Loại", "Nội dung"])
            df.to_csv(csv_path, index=False, encoding='utf-8')

def save_message_to_journal():
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_type = "Liều thuốc tinh thần"
        if st.session_state.current_message:
            content = f"{st.session_state.current_message['name']}: {st.session_state.current_message['text']}"
        else:
            content = "Không có nội dung"
        df = pd.read_csv(csv_path, encoding='utf-8')
        new_row = pd.DataFrame({
            "Ngày giờ": [current_time],
            "Loại": [message_type], 
            "Nội dung": [content]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(csv_path, index=False, encoding='utf-8')
        st.success("✅ Đã lưu thông điệp vào nhật ký cảm xúc!")
        st.balloons()
    except Exception as e:
        st.error(f"❌ Có lỗi khi lưu thông điệp: {str(e)}")

def show_journal_history():
    try:
        ensure_csv_exists()
        csv_path = get_csv_path()
        df = pd.read_csv(csv_path, encoding='utf-8')
        filtered_df = df[df["Loại"] == "Liều thuốc tinh thần"]
        if filtered_df.empty:
            st.info("📝 Chưa có thông điệp nào được lưu trong nhật ký.")
        else:
            st.markdown('<div class="lttt-history-box"><b>📖 Nhật Ký Liều Thuốc Tinh Thần</b></div>', unsafe_allow_html=True)
            filtered_df = filtered_df.sort_values("Ngày giờ", ascending=False)
            st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"❌ Có lỗi khi đọc nhật ký: {str(e)}")

# --- Chọn loại thông điệp ---
st.markdown("### 🌟 Bạn đang cần điều gì lúc này?")
cols = st.columns(len(LTTT_CATEGORY_ORDER))
for idx, cat in enumerate(LTTT_CATEGORY_ORDER):
    with cols[idx]:
        label = LTTT_CATEGORIES[cat]["label"]
        icon = LTTT_CATEGORIES[cat]["icon"]
        if st.button(f"{icon} {label}", key=f"btn_{cat}", use_container_width=True):
            st.session_state.message_category = cat
            st.session_state.current_message = random.choice(LTTT_CATEGORIES[cat]["messages"])
            st.rerun()

st.write("---")

# --- Hiển thị thông điệp ---
if st.session_state.current_message and st.session_state.message_category:
    msg = st.session_state.current_message
    st.markdown(
        f'<div class="lttt-card"><div class="lttt-avatar">{msg["avatar"]}</div>'
        f'<div style="font-size:1.11rem;font-weight:600;margin-bottom:0.3rem;">{msg["text"]}</div>'
        f'<div style="font-size:1rem;color:#7f8c8d;margin-top:0.4rem;">💝 Từ {msg["name"]} gửi bạn</div></div>',
        unsafe_allow_html=True
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Nhận lời khác", key="next_msg", use_container_width=True):
            st.session_state.current_message = random.choice(
                LTTT_CATEGORIES[st.session_state.message_category]["messages"]
            )
            st.rerun()
    with col2:
        if st.button("🔊 Đọc to", key="tts_msg", use_container_width=True):
            play_encouragement_audio(msg)
    with col3:
        if st.button("💝 Lưu vào lọ động viên", key="save_enc", use_container_width=True):
            enc = {
                "avatar": msg["avatar"], "text": msg["text"],
                "name": msg["name"], "category": st.session_state.message_category,
                "saved_time": datetime.now().strftime("%d/%m/%Y %H:%M")
            }
            if enc not in st.session_state.saved_encouragements:
                st.session_state.saved_encouragements.append(enc)
                st.success("✨ Đã lưu lời động viên vào lọ!")
                st.balloons()
            else:
                st.info("💫 Lời động viên này đã có trong lọ rồi nhé!")

    col_journal1, col_journal2 = st.columns(2)
    with col_journal1:
        if st.button("📓 Lưu vào nhật ký cảm xúc", key="save_journal", use_container_width=True):
            save_message_to_journal()
    with col_journal2:
        if st.button("📖 Xem nhật ký đã lưu", key="view_journal", use_container_width=True):
            st.session_state.show_journal = not st.session_state.show_journal

# --- Lọ động viên cá nhân ---
if st.session_state.saved_encouragements:
    st.write("---")
    st.markdown(f'<div class="lttt-box" style="background:#fffde7;border-left:5px solid #ffd54f;"><b>🍯 Lọ Động Viên Của Bạn ({len(st.session_state.saved_encouragements)} lời động viên)</b></div>', unsafe_allow_html=True)
    for idx, encouragement in enumerate(reversed(st.session_state.saved_encouragements)):
        with st.container():
            col1, col2, col3 = st.columns([1,6,2])
            with col1:
                st.markdown(f"<div style='font-size:2.1rem;text-align:center;'>{encouragement['avatar']}</div>", unsafe_allow_html=True)
            with col2:
                st.markdown(
                    f"<div style='background:#f8f9fa;padding:1rem;border-radius:10px;margin:0.5rem 0;'>"
                    f"<strong>{encouragement['name']}:</strong><br>{encouragement['text']}<br>"
                    f"<small style='color:#6c757d;'>💾 {encouragement['saved_time']}</small></div>", unsafe_allow_html=True)
            with col3:
                if st.button("🔊", key=f"jar_tts_{idx}", help="Nghe lại lời động viên này"):
                    play_encouragement_audio(encouragement)
                if st.button("🗑️", key=f"jar_remove_{idx}", help="Xóa khỏi lọ động viên"):
                    st.session_state.saved_encouragements.remove(encouragement)
                    st.success("✅ Đã xóa khỏi lọ động viên!")
                    st.rerun()

# --- Nhật ký động viên ---
if st.session_state.show_journal:
    st.write("---")
    show_journal_history()
    if st.button("❌ Đóng nhật ký", key="close_journal"):
        st.session_state.show_journal = False
        st.rerun()

# --- Footer động viên ---
st.markdown('<div class="lttt-footer">💜 <strong>Nhớ nhé:</strong> Mỗi động viên nhỏ đều là một bước tiến lớn. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)
