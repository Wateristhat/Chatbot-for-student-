import streamlit as st
import random
import pandas as pd
import os
from datetime import datetime
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="🎨 Bảng Màu Cảm Xúc", page_icon="🎨", layout="centered")

# --- CSS giao diện pastel trải ngang, đồng bộ Góc An Yên ---
st.markdown("""
<style>
.bmcx-title-feature {
    font-size:2.6rem; font-weight:700; color:#5d3fd3; text-align:center; margin-bottom:1.4rem; margin-top:0.7rem;
    letter-spacing:0.1px; display: flex; align-items: center; justify-content: center; gap: 1.1rem;
}
.bmcx-palette-box {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 36px; box-shadow: 0 8px 36px rgba(124,77,255,.11);
    padding: 3.2rem 2.2rem 2.1rem 2.2rem; margin-bottom:2.3rem; margin-top:0.2rem;
    text-align: center; border: 3.5px solid #b39ddb; max-width:1300px; margin-left:auto; margin-right:auto;
}
.bmcx-emotion-circle {
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    width: 120px; height: 120px; border-radius: 50%; color: #fff; font-size: 2.3rem; font-weight:700;
    margin: 0 18px 2rem 18px; box-shadow:0 3px 18px rgba(100,100,100,0.13); cursor: pointer;
    transition: all 0.22s; border:4px solid #fff;
}
.bmcx-emotion-circle.selected {
    border: 5px solid #5d3fd3; box-shadow: 0 6px 20px rgba(77,36,175,0.18); transform: scale(1.08);
}
.bmcx-emotion-label {font-size:1.15rem; font-weight:600; color:#222; margin-top:0.6rem;}
.bmcx-note-box {
    background: #f2fcfa; border-radius: 16px; padding: 1.3rem 1.5rem; font-size:1.1rem; color:#555;
    max-width:900px; margin-left:auto; margin-right:auto; margin-bottom:1.1rem; border-left:5px solid #80deea;
}
.bmcx-history-box {
    background: #e3f2fd; border-radius: 14px; padding: 1.05rem 1.2rem; font-size: 1.05rem; color: #333;
    border-left: 5px solid #2196f3; text-align:left; max-width:1200px; margin-left:auto; margin-right:auto; margin-bottom:1rem;
}
.bmcx-footer {
    background:#f3e5f5; border-left:5px solid #ba68c8; border-radius:15px; padding:1rem 1.3rem;
    text-align:center; font-size:1.12rem; margin:0.7rem 0 1rem 0; color:#333; max-width:1200px; margin-left:auto; margin-right:auto;
}
.bmcx-encourage-box {
    background: linear-gradient(120deg,#fffde7 0%,#e0f7fa 100%);
    border-radius: 16px; padding:1.2rem 1.5rem; font-size:1.18rem; color:#6d28d9;
    font-weight:600; margin-bottom:1.2rem; max-width:1200px; margin-left:auto; margin-right:auto;
    box-shadow:0 2px 10px rgba(100,100,100,0.05);
}
.bmcx-btn {
    background:#fff; color:#222; font-size:1.05rem; font-weight:500; border-radius:13px;
    padding:0.7rem 1rem; margin:0.6rem 0; border:2px solid #ececec;
    box-shadow: 0 2px 10px rgba(100,100,100,0.05); transition:all 0.18s; width:100%; text-align:center; outline:none;
}
.bmcx-btn.selected {border:2.5px solid #5d3fd3; background:#ede7f6; color:#222;}
.bmcx-btn:hover, .bmcx-btn:focus-visible {border:2.5px solid #4fc3f7; background:#e3f2fd;}
@media (max-width:900px) {
    .bmcx-palette-box, .bmcx-history-box, .bmcx-note-box, .bmcx-footer {max-width:96vw;}
    .bmcx-title-feature { font-size:1.6rem; }
    .bmcx-emotion-circle {width:90px;height:90px;font-size:1.4rem;}
}
</style>
""", unsafe_allow_html=True)

# --- Data cảm xúc & màu & động viên ---
EMOTIONS = [
    {
        "label": "Vui vẻ",
        "emoji": "😊",
        "color": "#FFD600",
        "encourage": "Hãy lan tỏa nụ cười của bạn tới mọi người xung quanh nhé!"
    },
    {
        "label": "Buồn",
        "emoji": "😢",
        "color": "#64B5F6",
        "encourage": "Bạn có thể chia sẻ với Bee hoặc bạn bè để cảm thấy nhẹ lòng hơn."
    },
    {
        "label": "Lo lắng",
        "emoji": "😰",
        "color": "#FF8A65",
        "encourage": "Thử hít thở thật sâu hoặc nhắm mắt lại một chút nhé!"
    },
    {
        "label": "Tức giận",
        "emoji": "😡",
        "color": "#FF1744",
        "encourage": "Hãy thử đếm đến 10 và thở thật đều, Bee luôn ở bên bạn!"
    },
    {
        "label": "Bình yên",
        "emoji": "😌",
        "color": "#81C784",
        "encourage": "Bạn đang làm rất tốt! Hãy giữ tâm trạng thư thái này nhé!"
    },
    {
        "label": "Hào hứng",
        "emoji": "🎉",
        "color": "#AB47BC",
        "encourage": "Hãy tận dụng năng lượng tích cực để sáng tạo và vui chơi!"
    },
    {
        "label": "Ngạc nhiên",
        "emoji": "😲",
        "color": "#FFB300",
        "encourage": "Cuộc sống luôn đầy bất ngờ, hãy tận hưởng nhé!"
    }
]

# --- Session state ---
if "selected_emotion_idx" not in st.session_state:
    st.session_state.selected_emotion_idx = None
if "emotion_note" not in st.session_state:
    st.session_state.emotion_note = ""
if "emotion_history" not in st.session_state:
    st.session_state.emotion_history = []
if "show_history" not in st.session_state:
    st.session_state.show_history = False

# --- Tiêu đề ---
st.markdown(
    '<div class="bmcx-title-feature">'
    ' <span style="font-size:2.3rem;">🎨</span> Bảng Màu Cảm Xúc'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("⬅️ [Quay về Trang chủ](../0_💖_Trang_chủ.py)")

# --- Khung chọn cảm xúc (palette) ---
st.markdown('<div class="bmcx-palette-box">', unsafe_allow_html=True)
st.markdown("#### Hãy chọn cảm xúc của bạn hôm nay:")

emotion_cols = st.columns(len(EMOTIONS))
for idx, emo in enumerate(EMOTIONS):
    with emotion_cols[idx]:
        selected = st.session_state.selected_emotion_idx == idx
        if st.button(f"{emo['emoji']}", key=f"emo_{idx}", help=emo["label"]):
            st.session_state.selected_emotion_idx = idx
            st.session_state.emotion_note = ""
            st.rerun()
        st.markdown(
            f"""
            <div class="bmcx-emotion-circle{' selected' if selected else ''}" style="background:{emo['color']};">
                {emo['emoji']}
            </div>
            <div class="bmcx-emotion-label">{emo['label']}</div>
            """,
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# --- Động viên theo cảm xúc đã chọn ---
if st.session_state.selected_emotion_idx is not None:
    emo = EMOTIONS[st.session_state.selected_emotion_idx]
    st.markdown(f"""
    <div class="bmcx-encourage-box">
        <span style="font-size:2.1rem;">{emo['emoji']}</span> <strong>{emo['encourage']}</strong>
    </div>
    """, unsafe_allow_html=True)
    col1, col2 = st.columns([2,2])
    with col1:
        if st.button("🔊 Nghe động viên", key="tts_encourage"):
            audio_bytes = BytesIO()
            tts = gTTS(text=emo['encourage'], lang='vi', slow=False)
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes.read(), format="audio/mp3")

# --- Nhập ghi chú cảm xúc ---
if st.session_state.selected_emotion_idx is not None:
    st.markdown('<div class="bmcx-note-box">', unsafe_allow_html=True)
    st.markdown("#### 📝 Bạn muốn chia sẻ thêm về cảm xúc của mình không?")
    st.session_state.emotion_note = st.text_area(
        "",
        value=st.session_state.emotion_note,
        height=80,
        placeholder="Bạn có thể mô tả lý do, hoàn cảnh hoặc ai ở bên bạn lúc này..."
    )
    st.markdown('</div>', unsafe_allow_html=True)
    if st.button("💾 Lưu cảm xúc hôm nay", type="primary", use_container_width=True):
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        st.session_state.emotion_history.append({
            "emoji": emo["emoji"], "emotion": emo["label"], "note": st.session_state.emotion_note, "time": now
        })
        st.success("✅ Đã lưu cảm xúc vào lịch sử của bạn!")
        st.balloons()
        st.session_state.selected_emotion_idx = None
        st.session_state.emotion_note = ""
        st.rerun()

st.write("---")

# --- Lịch sử cảm xúc ---
st.markdown("### 📖 Lịch sử cảm xúc của bạn")
if st.button("📖 Xem lịch sử", key="show_history_btn"):
    st.session_state.show_history = not st.session_state.show_history
if st.session_state.show_history:
    if st.session_state.emotion_history:
        for item in reversed(st.session_state.emotion_history):
            st.markdown(
                f"""
                <div class="bmcx-history-box">
                    <div style='font-size:2rem;display:inline-block;'>{item['emoji']}</div>
                    <span style='font-size:1.13rem;font-weight:700;margin-left:8px;color:#5d3fd3;'>{item['emotion']}</span>
                    <span style='font-size:1rem;color:#888;margin-left:12px;'>{item['time']}</span>
                    <div style='margin-top:0.6rem;'>{item['note'] if item['note'] else "<i>(Không có ghi chú)</i>"}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("Bạn chưa lưu cảm xúc nào hôm nay. Hãy chọn và lưu cảm xúc nhé!")

# --- Footer ---
st.markdown("""
<div class="bmcx-footer">
    <strong>💫 Lời nhắn từ Bee:</strong><br>
    "Mỗi cảm xúc đều đáng trân trọng. Bạn hãy tự tin chia sẻ và chăm sóc cảm xúc của mình nhé! 🎨"
</div>
""", unsafe_allow_html=True)
