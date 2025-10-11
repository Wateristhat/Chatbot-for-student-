import streamlit as st
import sys
import os
import html
import time
import random
from datetime import datetime
import tempfile
from gtts import gTTS
from io import BytesIO
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import database as db

st.markdown("""
<style>
.stButton > button {
    font-size: 1.25rem !important;         /* Tăng cỡ chữ lên 1/3 */
    padding: 1.2rem 2.5rem !important;     /* Tăng chiều cao & chiều ngang nút */
    border-radius: 16px !important;        /* Bo tròn nút */
    min-width: 170px;                      /* Đặt chiều rộng tối thiểu */
    min-height: 52px;                      /* Đặt chiều cao tối thiểu */
}
</style>
""", unsafe_allow_html=True)

# --- DANH SÁCH GỢI Ý BIẾT ƠN LUÂN PHIÊN ---
GRATITUDE_SUGGESTIONS = [
    "Hôm nay bạn đã nụ cười với ai? Điều gì khiến bạn cảm thấy vui vẻ?",
    "Có món ăn nào ngon khiến bạn nhớ mãi không? Kể cho mình nghe nhé!",
    "Bạn đã học được điều gì mới mẻ hôm nay? Dù là điều nhỏ nhất!",
    "Ai là người đã giúp đỡ bạn gần đây? Bạn biết ơn họ điều gì?",
    "Thiên nhiên có gì đẹp khiến bạn thích thú? Trời xanh, cây lá, hay tiếng chim hót?",
    "Bạn đã làm được việc gì khiến bản thân tự hào? Dù nhỏ nhất cũng được!",
    "Có khoảnh khắc nào hôm nay khiến bạn cảm thấy bình yên và hạnh phúc?",
    "Điều gì trong ngôi nhà của bạn khiến bạn cảm thấy ấm áp và an toàn?"
]

# --- VIRTUAL ASSISTANT MESSAGES ---
ASSISTANT_MESSAGES = [
    ("🤖", "Mỗi điều biết ơn nhỏ đều là kho báu quý giá!"),
    ("🤖", "Bạn làm rất tốt khi ghi lại những khoảnh khắc đẹp!"),
    ("🤖", "Cảm ơn bạn đã tin tưởng và chia sẻ với Bee!"),
    ("🤖", "Hôm nay bạn đã lan tỏa năng lượng tích cực!"),
    ("🤖", "Biết ơn là ánh nắng ấm áp cho trái tim!"),
    ("🤖", "Một lời biết ơn nhỏ - một niềm vui lớn!")
]
GRATITUDE_RESPONSES = [
    "Thật tuyệt vời! Lời biết ơn của bạn đã được thêm vào lọ! 🌟",
    "Cảm ơn bạn đã chia sẻ! Điều này sẽ làm sáng cả ngày của bạn! ✨", 
    "Tuyệt quá! Bạn vừa tạo ra một kỷ niệm đẹp! 💝",
    "Mình cảm thấy ấm lòng khi đọc lời biết ơn của bạn! 🤗",
    "Bạn đã làm cho thế giới này tích cực hơn một chút! 🦋"
]

AVATAR_OPTIONS = ["🐝", "🦋", "🌟", "💫", "🌸", "🦄", "🧚‍♀️", "🌻"]
AVATAR_NAMES = ["Ong Bee", "Bướm xinh", "Sao sáng", "Ánh sáng", "Hoa đào", "Kỳ lân", "Tiên nhỏ", "Hoa hướng dương"]

ENCOURAGING_MESSAGES = [
    {
        "avatar": "🌸",
        "message": "Thật tuyệt vời khi bạn dành thời gian để cảm ơn! Mỗi lời biết ơn là một hạt giống hạnh phúc được gieo vào trái tim bạn."
    },
    {
        "avatar": "🌟", 
        "message": "Hãy nhớ rằng, những điều nhỏ bé nhất cũng có thể mang lại niềm vui lớn. Bạn đã làm rất tốt rồi!"
    },
    {
        "avatar": "💖",
        "message": "Mỗi khi bạn viết lời biết ơn, bạn đang nuôi dưỡng một tâm hồn tích cực. Điều này thật đáng quý!"
    },
    {
        "avatar": "🦋",
        "message": "Biết ơn giống như ánh nắng ấm áp, nó không chỉ sưởi ấm trái tim bạn mà còn lan tỏa đến những người xung quanh."
    },
    {
        "avatar": "🌈",
        "message": "Bạn có biết không? Khi chúng ta biết ơn, não bộ sẽ tiết ra những hormone hạnh phúc. Bạn đang chăm sóc bản thân thật tốt!"
    },
    {
        "avatar": "🌺",
        "message": "Mỗi lời cảm ơn bạn viết ra đều là một món quà bạn tặng cho chính mình. Hãy tiếp tục nuôi dưỡng lòng biết ơn nhé!"
    },
    {
        "avatar": "✨",
        "message": "Đôi khi những điều đơn giản nhất lại mang đến hạnh phúc lớn nhất. Bạn đã nhận ra điều này rồi đấy!"
    },
    {
        "avatar": "🍀",
        "message": "Lòng biết ơn là chìa khóa mở ra cánh cửa hạnh phúc. Bạn đang trên đúng con đường rồi!"
    }
]

def get_random_encouragement():
    return random.choice(ENCOURAGING_MESSAGES)

def create_audio_file(text):
    try:
        tts = gTTS(text=text, lang='vi', slow=False)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
            tts.save(tmp_file.name)
            return tmp_file.name
    except Exception as e:
        st.error(f"Lỗi tạo file âm thanh: {e}")
        return None

# --- SESSION STATE ---
if 'selected_emotion' not in st.session_state:
    st.session_state.selected_emotion = None
if 'suggestion_index' not in st.session_state:
    st.session_state.suggestion_index = random.randint(0, 4)
if 'selected_avatar' not in st.session_state:
    st.session_state.selected_avatar = "🐝"
if 'current_assistant_message' not in st.session_state or not isinstance(st.session_state.current_assistant_message, tuple):
    st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
if 'show_gratitude_response' not in st.session_state:
    st.session_state.show_gratitude_response = False

# --- CSS GIAO DIỆN ĐỒNG BỘ GÓC AN YÊN ---
st.markdown("""
<style>
.lo-title-feature {
    font-size:2.3rem; font-weight:700; color:#d81b60; text-align:center; margin-bottom:1.5rem; margin-top:0.7rem;
    letter-spacing:0.2px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
}
.lo-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom:2.3rem; margin-top:0.2rem;
    text-align: center; border: 3.5px solid #e1bee7; max-width:1400px; margin-left:auto; margin-right:auto;
}
.lo-assist-icon {font-size:3.1rem; margin-bottom:0.7rem;}
.lo-assist-text {font-size:1.45rem; font-weight:700; color:#6d28d9; margin-bottom:1.2rem;}
.lo-assist-btn-row {display:flex; justify-content: center; gap: 55px; margin-top:1.25rem;}
.lo-assist-action-btn {
    background: #fff; border: 2.5px solid #e1bee7; border-radius: 18px;
    font-size:1.19rem; font-weight:600; color:#6d28d9;
    padding: 1rem 2.1rem; cursor:pointer; box-shadow:0 2px 8px rgba(124,77,255,.14); transition:all 0.17s;
}
.lo-assist-action-btn:hover {background:#f3e8ff;}
.lo-box, .timeline-item, .lo-footer {
    background: #fffbe7;
    border-radius: 13px;
    padding: 1rem 1.2rem;
    font-size: 1.07rem;
    color: #333;
    border-left: 5px solid #ffd54f;
    text-align:center;
    max-width:1200px;
    margin-left:auto; margin-right:auto; margin-bottom:1.2rem;
    box-shadow:0 2px 10px rgba(255, 223, 186, 0.09);
}
.timeline-item {
    background:linear-gradient(135deg,#FFF8DC,#FFFACD);border-radius:15px;padding:1.3rem;max-width:1200px;margin:auto;margin-bottom:1.2rem;box-shadow:0 4px 12px rgba(255,215,0,0.2);border-left:6px solid #FFD700;
}
.timeline-content {font-size:1.17rem;color:#8B4513;margin-bottom:0.5rem;line-height:1.4;}
.timeline-date {font-size:0.99rem;color:#CD853F;font-weight:700;}
.lo-footer {background:#f3e5f5;border-left:5px solid #ba68c8;border-radius:10px;padding:0.9rem 1.2rem;text-align:center;font-size:1.09rem;margin:0.7rem 0 1.2rem 0;color:#333;}
@media (max-width: 1100px) {.lo-assist-bigbox{padding:2rem 1rem 1rem 1rem; max-width:100vw;}}
</style>
""", unsafe_allow_html=True)

# --- TIÊU ĐỀ + TRỢ LÝ ẢO ĐẦU TRANG ---
st.markdown(
    '<div class="lo-title-feature">'
    ' <span style="font-size:2.5rem;">🍯</span> Lọ Biết Ơn'
    '</div>',
    unsafe_allow_html=True
)
avatar, msg = st.session_state.current_assistant_message
st.markdown(f"""
<div class="lo-assist-bigbox">
    <div class="lo-assist-icon">{avatar}</div>
    <div class="lo-assist-text">{msg}</div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2,2])
with col1:
    if st.button("💬 Thông điệp mới", key="new_msg_top"):
        st.session_state.current_assistant_message = random.choice(ASSISTANT_MESSAGES)
        st.rerun()
with col2:
    if st.button("🔊 Nghe động viên", key="tts_msg_top"):
        audio_bytes = BytesIO()
        tts = gTTS(text=msg, lang='vi', slow=False)
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes.read(), format="audio/mp3")

# --- NAVIGATION LINK ---
st.markdown("⬅️ [Quay về Trang chủ](../0_💖_Trang_chủ.py)")

# --- Hiển thị avatar trợ lý ảo khi gửi biết ơn ---
if st.session_state.show_gratitude_response:
    avatar, msg = st.session_state.current_assistant_message
    message_to_show = random.choice(GRATITUDE_RESPONSES)
    st.markdown(f"""
    <div class="lo-assist-bigbox">
        <div class="lo-assist-icon">{st.session_state.selected_avatar}</div>
        <div class="lo-assist-text">{message_to_show}</div>
    </div>
    """, unsafe_allow_html=True)

# --- CẢM XÚC BẰNG EMOJI ---
st.markdown("### 💝 Hôm nay bạn cảm thấy thế nào?")
emotion_cols = st.columns(5)
emotions = ["😊", "😃", "🥰", "😌", "🤗"]
emotion_names = ["Vui vẻ", "Hạnh phúc", "Yêu thương", "Bình yên", "Ấm áp"]
for i, (col, emotion, name) in enumerate(zip(emotion_cols, emotions, emotion_names)):
    with col:
        if st.button(emotion, key=f"emotion_{i}", help=name):
            st.session_state.selected_emotion = emotion
            st.rerun()

if st.session_state.selected_emotion:
    st.markdown(f"<div style='text-align: center; font-size: 1.2rem; color: #FF69B4; margin: 1rem 0;'>Bạn đang cảm thấy {st.session_state.selected_emotion} - Thật tuyệt vời!</div>", unsafe_allow_html=True)
st.write("---")

# --- ĐỘNG VIÊN BEE ---
if 'current_encouragement' not in st.session_state:
    st.session_state.current_encouragement = get_random_encouragement()
encouragement = st.session_state.current_encouragement
st.markdown(f"""
<div class="lo-assist-bigbox" style="padding:2rem 1.8rem 1.2rem 1.8rem;">
    <div class="lo-assist-icon">{encouragement['avatar']}</div>
    <div class="lo-assist-text">{encouragement['message']}</div>
</div>
""", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])
with col1:
    if st.button("🎲 Nhận lời động viên mới", help="Nhận một thông điệp động viên khác"):
        st.session_state.current_encouragement = get_random_encouragement()
        st.rerun()
with col2:
    if st.button("🔊 Đọc to", help="Nghe lời động viên"):
        with st.spinner("Đang tạo âm thanh..."):
            audio_file = create_audio_file(encouragement['message'])
            if audio_file:
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)
                except Exception as e:
                    st.error(f"Không thể phát âm thanh: {e}")

# --- HỘP GỢI Ý BIẾT ƠN LUÂN PHIÊN ---
current_suggestion = GRATITUDE_SUGGESTIONS[st.session_state.suggestion_index]
st.markdown(f"""
<div class="lo-box">
    <strong>💡 Gợi ý cho bạn:</strong><br>
    {current_suggestion}
</div>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("🔊 Đọc to", key="read_suggestion", help="Đọc to gợi ý này"):
        with st.spinner("Đang chuẩn bị âm thanh..."):
            audio_file = create_audio_file(f"Gợi ý cho bạn: {current_suggestion}")
            if audio_file:
                try:
                    with open(audio_file, 'rb') as f:
                        audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                    os.unlink(audio_file)  # Xóa file tạm
                except Exception as e:
                    st.error(f"Không thể phát âm thanh: {e}")
with col2:
    if st.button("🔄 Gợi ý khác", use_container_width=True):
        st.session_state.suggestion_index = (st.session_state.suggestion_index + 1) % len(GRATITUDE_SUGGESTIONS)
        st.rerun()

# --- KHU VỰC NHẬP LIỆU ---
st.markdown("### ✍️ Viết điều bạn biết ơn hôm nay:")
note_text = st.text_area(
    "",
    height=120,
    key="gratitude_input",
    placeholder="Hãy viết về điều làm bạn cảm thấy biết ơn... Mỗi từ đều có ý nghĩa! 💕",
    label_visibility="collapsed"
)
if st.button("🌟 Thêm vào lọ biết ơn", type="primary", use_container_width=True):
    if note_text:
        db.add_gratitude_note(note_text)
        st.session_state.show_gratitude_response = True
        success_stickers = ["🎉", "⭐", "🌟", "✨", "💫", "🎊", "🦋", "🌈", "🎁", "💝"]
        selected_stickers = random.sample(success_stickers, 3)
        st.markdown(f"""
        <div style="text-align: center; font-size: 3rem; margin: 1rem 0; animation: bounce 1s ease-in-out;">
            {''.join(selected_stickers)}
        </div>
        """, unsafe_allow_html=True)
        st.success("🌱 Đã thêm một hạt mầm biết ơn vào lọ! Cảm ơn bạn đã chia sẻ!")
        st.balloons()
        time.sleep(2)
        st.rerun()
    else:
        st.warning("💛 Bạn hãy viết gì đó để chia sẻ nhé! Mình đang chờ đây!")

st.write("---")

# --- TIMELINE HIỂN THỊ GHI CHÚ ---
st.markdown("### 📖 Timeline - Những Kỷ Niệm Biết Ơn")
gratitude_notes = db.get_gratitude_notes()
if gratitude_notes:
    st.markdown(f"<div style='text-align: center; font-size: 1.1rem; color: #8B4513; margin-bottom: 1.5rem;'>Bạn đã có <strong>{len(gratitude_notes)}</strong> kỷ niệm đẹp! 💎</div>", unsafe_allow_html=True)
    for note_id, note_content, timestamp in gratitude_notes:
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            formatted_date = dt.strftime("%d/%m/%Y lúc %H:%M")
            day_name = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"][dt.weekday()]
            full_date = f"{day_name}, {formatted_date}"
        except:
            full_date = timestamp
        with st.container():
            st.markdown(f"""
            <div class="timeline-item">
                <div class="timeline-content">{html.escape(note_content)}</div>
                <div class="timeline-date">📅 {full_date}</div>
            </div>
            """, unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                if st.button("🔊 Đọc to", key=f"tts_{note_id}", help="Nghe ghi chú này"):
                    audio_file = create_audio_file(note_content)
                    if audio_file:
                        try:
                            with open(audio_file, 'rb') as f:
                                audio_bytes = f.read()
                            st.audio(audio_bytes, format='audio/mp3', autoplay=True)
                            os.unlink(audio_file)
                        except Exception as e:
                            st.error(f"Không thể phát âm thanh: {e}")
            with col2:
                if st.button("💝 Thích", key=f"like_{note_id}", help="Tôi thích ghi chú này!"):
                    st.markdown("💕 Cảm ơn bạn đã thích kỷ niệm này!")
            with col3:
                if st.button("🗑️", key=f"delete_{note_id}", help="Xóa ghi chú này"):
                    db.delete_gratitude_note(note_id)
                    st.success("🌸 Đã xóa ghi chú!")
                    time.sleep(1)
                    st.rerun()
else:
    st.markdown("""
    <div style="text-align: center; padding: 3rem; font-size: 1.3rem; color: #9370DB;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🍯</div>
        <div>Chiếc lọ biết ơn của bạn đang chờ những điều tuyệt vời đầu tiên!</div>
        <div style="font-size: 1rem; margin-top: 1rem; color: #DDA0DD;">Hãy bắt đầu bằng việc chia sẻ một điều nhỏ nhất mà bạn biết ơn hôm nay ❤️</div>
    </div>
    """, unsafe_allow_html=True)

# --- FOOTER KHUYẾN KHÍCH ---
st.markdown("---")
st.markdown("""
<div class="lo-footer">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi ngày là một món quà, mỗi khoảnh khắc biết ơn là một viên ngọc quý. 
    Cảm ơn bạn đã chia sẻ những điều tuyệt vời trong cuộc sống! 🌟"
</div>
""", unsafe_allow_html=True)




