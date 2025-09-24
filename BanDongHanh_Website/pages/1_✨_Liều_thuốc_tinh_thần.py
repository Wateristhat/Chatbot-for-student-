import streamlit as st
import random
import pandas as pd
from datetime import datetime
import os
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="✨ Liều Thuốc Tinh Thần", page_icon="✨", layout="centered")

# --- CSS nhẹ, đồng bộ với Góc An Yên ---
st.markdown("""
<style>
body, html, [class*="css"] { font-family: 'Quicksand', Arial, sans-serif; font-size: 1.15rem; }
.page-title {
    font-size:2.1rem; font-weight:700; color:#e53935; text-align:center; margin-bottom:1.2rem; margin-top:1rem;
}
.lttt-box {
    background: #fffbe7;
    border-radius: 13px;
    padding: 1rem 1.2rem;
    font-size: 1.06rem;
    color: #333;
    border-left: 5px solid #ffd54f;
    text-align:center;
    max-width:650px;
    margin: auto;
    margin-bottom:1.2rem;
}
.lttt-btn {
    background:#fff;
    color:#222;
    font-size:1rem;
    font-weight:500;
    border-radius:12px;
    padding:0.6rem 0.9rem;
    margin:0.5rem 0;
    border:1.5px solid #ececec;
    box-shadow: 0 2px 8px rgba(100,100,100,0.04);
    transition:all 0.13s;
    width:100%;
    text-align:left;
}
.lttt-btn.selected {
    border:2px solid #6c63ff;
    background:#f3f2fd;
    color:#222;
}
.lttt-btn:hover {
    border:2px solid #81d4fa;
    background:#e3f2fd;
}
.lttt-card {
    background:#fffde7;
    border-radius:15px;
    padding:1.3rem 1.1rem;
    text-align:center;
    font-size:1.09rem;
    margin:1.2rem 0;
    color:#333;
    border:2px solid #ffd54f;
}
.lttt-footer {
    background:#f3e5f5;
    border-left:5px solid #ba68c8;
    border-radius:12px;
    padding:0.8rem 1rem;
    text-align:center;
    font-size:1rem;
    margin:0.5rem 0 1rem 0;
    color:#333;
}
.lttt-avatar {
    font-size:2.15rem; margin-bottom:0.6rem;
}
.lttt-history-box {
    background: #e3f2fd;
    border-radius: 12px;
    padding: 0.8rem 1rem;
    font-size: 1rem;
    color: #333;
    border-left: 5px solid #2196f3;
    text-align:left;
    max-width:650px;
    margin: auto;
    margin-bottom:1rem;
}
@media (max-width:700px) {
    .page-title { font-size:1.3rem; }
}
</style>
""", unsafe_allow_html=True)

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

# --- TTS ---
@st.cache_data
def create_audio_with_tts(text):
    if not text or not text.strip():
        return None
    audio_bytes = BytesIO()
    tts = gTTS(text=text.strip(), lang='vi', slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    if st.button(button_text, key=f"tts_{key_suffix}"):
        st.audio(create_audio_with_tts(text), format="audio/mp3")

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

# --- Giao diện chính ---
st.markdown('<div class="page-title">✨ Liều Thuốc Tinh Thần Cho Bạn ✨</div>', unsafe_allow_html=True)
st.markdown('<a href="0_💖_Trang_chủ.py" style="text-decoration:none;color:#333;background:#e3f2fd;padding:0.5rem 1.3rem;border-radius:13px;border:2px solid #2196f3;font-weight:600;display:inline-block;margin-bottom:1.1rem;">⬅️ Quay về Trang chủ</a>', unsafe_allow_html=True)
st.markdown('<div class="lttt-box">🐝 Chọn điều bạn cần nhất, Bee sẽ gửi động viên phù hợp! Bạn có thể nghe hoặc lưu lại nhé! 🌈</div>', unsafe_allow_html=True)

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
        f'<div style="font-size:1.09rem;font-weight:600;margin-bottom:0.3rem;">{msg["text"]}</div>'
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
