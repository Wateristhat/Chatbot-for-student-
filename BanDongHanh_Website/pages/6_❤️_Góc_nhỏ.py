import streamlit as st
from gtts import gTTS
from io import BytesIO

st.set_page_config(page_title="Góc nhỏ", page_icon="❤️", layout="centered")

# --- TTS ---
@st.cache_data
def text_to_speech(text):
    audio_bytes = BytesIO()
    tts = gTTS(text=text, lang='vi', slow=False)
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes.read()

def create_tts_button(text, key_suffix, button_text="🔊 Đọc to"):
    if st.button(button_text, key=f"tts_{key_suffix}"):
        st.audio(text_to_speech(text), format="audio/mp3")

# --- DATA ---
MICRO_ACTIONS = [
    {"text": "Uống một ly nước đầy", "icon": "💧"},
    {"text": "Vươn vai và duỗi người trong 1 phút", "icon": "🤸‍♀️"},
    {"text": "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp", "icon": "☁️"},
    {"text": "Nghe một bài hát bạn yêu thích", "icon": "🎵"},
    {"text": "Viết ra 1 điều bạn tự hào về bản thân", "icon": "✍️"},
    {"text": "Rửa mặt với nước mát", "icon": "🚿"},
    {"text": "Sắp xếp lại góc học tập/làm việc", "icon": "📚"},
    {"text": "Mỉm cười với chính mình trong gương", "icon": "😊"}
]

# --- STYLE ---
st.markdown("""
<style>
body, html, [class*="css"] {
    font-family: 'Quicksand', Arial, sans-serif;
}
h1, h2, h3 {
    font-family: 'Quicksand', Arial, sans-serif;
}
.goc-nho-header {
    font-size:2.2rem; color:#e53935; text-align:center; margin-bottom:1.2rem; font-weight:700;
}
.goc-nho-guide {
    background:#fffbe7;
    border-radius:14px;
    padding:1.1rem 1.3rem;
    font-size:1.1rem;
    color:#333;
    border-left:5px solid #ffd54f;
    margin:auto; margin-bottom:1.2rem; text-align:center;
}
.goc-nho-actions-title {
    font-size:1.4rem; font-weight:600; color:#6c63ff; margin-top:1rem; margin-bottom:0.5rem; text-align:center;
}
.goc-nho-action-btn {
    background:#fff;
    color:#222;
    font-size:1rem;
    font-weight:500;
    border-radius:13px;
    padding:0.7rem 1rem;
    margin:0.6rem 0;
    border:1.8px solid #ececec;
    box-shadow: 0 2px 8px rgba(100,100,100,0.04);
    transition:all 0.15s;
    width:100%;
    text-align:left;
}
.goc-nho-action-btn.selected {
    border:2px solid #6c63ff;
    background:#f3f2fd;
    color:#222;
}
.goc-nho-action-btn:hover {
    border:2px solid #81d4fa;
    background:#e3f2fd;
}
.goc-nho-checklist-title {
    font-size:1.18rem; font-weight:600; color:#333; margin-top:1.5rem; margin-bottom:0.5rem; text-align:center;
}
.goc-nho-check-item {
    background:#f9f9fb;
    border-radius:10px;
    padding:0.7rem 0.9rem;
    margin-bottom:0.5rem;
    display:flex;
    align-items:center;
    font-size:1rem;
    border:1.5px solid #ede7f6;
}
.goc-nho-check-icon {
    font-size:1.25rem; margin-right:0.7rem;
}
.goc-nho-check-status {
    margin-left:auto; font-size:1.2rem;
}
.goc-nho-congrats {
    background:#fffde7;
    border-radius:17px;
    padding:1.4rem 1.2rem;
    text-align:center;
    font-size:1.15rem;
    margin:1.5rem 0;
    color:#333;
    border:2px solid #ffd54f;
}
.goc-nho-footer {
    background:#f3e5f5;
    border-left:5px solid #ba68c8;
    border-radius:13px;
    padding:0.9rem 1.1rem;
    text-align:center;
    font-size:1rem;
    margin:0.5rem 0 1.2rem 0;
    color:#333;
}
@media (max-width:700px) {
    .goc-nho-header { font-size:1.4rem; }
    .goc-nho-actions-title { font-size:1.1rem;}
    .goc-nho-checklist-title { font-size:1.05rem;}
}
</style>
""", unsafe_allow_html=True)

# --- HEADER + NAV ---
st.markdown('<div class="goc-nho-header">❤️ Góc nhỏ của bạn</div>', unsafe_allow_html=True)
st.markdown('<a href="0_💖_Trang_chủ.py" style="text-decoration:none;color:#333;background:#e3f2fd;padding:0.5rem 1.3rem;border-radius:13px;border:2px solid #2196f3;font-weight:600;display:inline-block;margin-bottom:1.1rem;">⬅️ Quay về Trang chủ</a>', unsafe_allow_html=True)

# --- HƯỚNG DẪN ---
guide_txt = "Hãy chọn những việc nhỏ bạn muốn làm hôm nay để chăm sóc bản thân. Chỉ cần bấm một lần để chọn hoặc bỏ chọn!"
st.markdown(f'<div class="goc-nho-guide">💝 {guide_txt}</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns([1,1,1])
with col2:
    create_tts_button(guide_txt, "guide", "🔊 Đọc hướng dẫn")

# --- CHỌN HOẠT ĐỘNG ---
if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []

st.markdown('<div class="goc-nho-actions-title">🌈 Chọn từ ngân hàng hoạt động:</div>', unsafe_allow_html=True)
cols = st.columns(2)
for i, action in enumerate(MICRO_ACTIONS):
    col = cols[i % 2]
    with col:
        is_selected = action["text"] in st.session_state.selected_actions
        btn_key = f"action_btn_{i}"
        btn_label = f'{action["icon"]} {action["text"]}'
        btn_style = "goc-nho-action-btn selected" if is_selected else "goc-nho-action-btn"
        if st.button(
            btn_label,
            key=btn_key,
            help=f"Bấm để {'bỏ chọn' if is_selected else 'chọn'} hoạt động này",
            use_container_width=True
        ):
            if is_selected:
                st.session_state.selected_actions.remove(action["text"])
                st.toast(f"❌ Đã bỏ chọn: {action['text']}", icon="ℹ️")
            else:
                st.session_state.selected_actions.append(action["text"])
                st.toast(f"✅ Đã chọn: {action['text']}", icon="🎉")
            st.rerun()
        st.markdown(f'<div class="{btn_style}">{btn_label}</div>', unsafe_allow_html=True)

# --- CHECKLIST --- 
st.markdown("---")
if not st.session_state.selected_actions:
    st.markdown(
        '<div class="goc-nho-guide" style="background:#fffde7;border-left:5px solid #ffd54f;">🌟 Hãy chọn ít nhất một hành động để bắt đầu kế hoạch của bạn nhé! Mỗi bước nhỏ đều có ý nghĩa lớn.</div>',
        unsafe_allow_html=True
    )
else:
    st.markdown('<div class="goc-nho-checklist-title">📋 Danh sách việc cần làm của bạn hôm nay:</div>', unsafe_allow_html=True)
    checklist_tts = "Danh sách việc cần làm hôm nay của bạn gồm: " + ", ".join(st.session_state.selected_actions)
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        create_tts_button(checklist_tts, "checklist", "🔊 Đọc danh sách")
    all_done = True
    for i, action_text in enumerate(st.session_state.selected_actions):
        action_icon = next((a["icon"] for a in MICRO_ACTIONS if a["text"] == action_text), "💝")
        done_key = f"done_{action_text}"
        if done_key not in st.session_state:
            st.session_state[done_key] = False
        is_done = st.session_state[done_key]
        cols_done = st.columns([0.1, 0.8, 0.1])
        with cols_done[0]:
            new_state = st.checkbox("", value=is_done, key=f"cb_{action_text}_{i}")
        with cols_done[1]:
            st.markdown(
                f'<div class="goc-nho-check-item"><span class="goc-nho-check-icon">{action_icon}</span><span style="font-weight:600;">{action_text}</span></div>',
                unsafe_allow_html=True
            )
        with cols_done[2]:
            st.markdown(f"<span class='goc-nho-check-status'>{'✅' if is_done else '⬜'}</span>", unsafe_allow_html=True)
        if new_state != is_done:
            if new_state:
                st.toast(f"🎉 Tuyệt vời! Bạn đã hoàn thành: {action_text}", icon="🌟")
                st.balloons()
            else:
                st.toast(f"📝 Đã bỏ đánh dấu: {action_text}", icon="ℹ️")
            st.session_state[done_key] = new_state
        if not new_state:
            all_done = False

    if all_done and st.session_state.selected_actions:
        st.markdown(
            '<div class="goc-nho-congrats"><b>🎉 CHÚC MỪNG! 🎉</b><br>Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!<br>🌟 Bạn thật tuyệt vời! Hãy tự hào về bản thân nhé! 🌟</div>',
            unsafe_allow_html=True
        )
        st.balloons()
        congrats_tts = "Chúc mừng bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!"
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            create_tts_button(congrats_tts, "congrats", "🔊 Đọc lời chúc mừng")

# --- FOOTER ---
st.markdown('<div class="goc-nho-footer">💜 <strong>Nhớ nhé:</strong> Mỗi hành động nhỏ đều là một bước tiến lớn trong việc chăm sóc bản thân. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)
