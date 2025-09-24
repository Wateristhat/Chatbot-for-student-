import streamlit as st
import random

MICRO_ACTIONS = [
    {"text": "Uống một ly nước đầy", "icon": "💧"},
    {"text": "Uống một ly nước đầy", "icon": "💧"},
    {"text": "Vươn vai và duỗi người trong 1 phút", "icon": "🤸‍♀️"},
    {"text": "Vươn vai và duỗi người trong 1 phút", "icon": "🤸‍♀️"},
    {"text": "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp", "icon": "☁️"},
    {"text": "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp", "icon": "☁️"},
    {"text": "Nghe một bài hát bạn yêu thích", "icon": "🎵"},
    {"text": "Nghe một bài hát bạn yêu thích", "icon": "🎵"},
    {"text": "Viết ra 1 điều bạn tự hào về bản thân", "icon": "✍️"},
    {"text": "Viết ra 1 điều bạn tự hào về bản thân", "icon": "✍️"},
    {"text": "Rửa mặt với nước mát", "icon": "🚿"},
    {"text": "Rửa mặt với nước mát", "icon": "🚿"},
    {"text": "Sắp xếp lại góc học tập/làm việc", "icon": "📚"},
    {"text": "Sắp xếp lại góc học tập/làm việc", "icon": "📚"},
    {"text": "Mỉm cười với chính mình trong gương", "icon": "😊"},
    {"text": "Mỉm cười với chính mình trong gương", "icon": "😊"},
]

# --- LOẠI BỎ TRÙNG LẶP hoạt động (icon+text) ---
unique_micro_actions = []
seen = set()
for act in MICRO_ACTIONS:
    key = f"{act['icon']}_{act['text']}"
    if key not in seen:
        unique_micro_actions.append(act)
        seen.add(key)

# --- Custom CSS for assistant and compact 2-column grid ---
st.markdown("""
<style>
/* ...CSS giữ nguyên... */
</style>
""", unsafe_allow_html=True)

# --- Assistant box on top (like Góc An Yên), các phần giữ nguyên ---

# --- Title & grid ---
st.markdown('<div class="goc-nho-title">🌈 Chọn từ ngân hàng hoạt động:</div>', unsafe_allow_html=True)

if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []

# --- Chỉ 1 nút cho mỗi hoạt động, 2 columns, click chọn xác nhận ---
cols = st.columns(2)
for i, action in enumerate(unique_micro_actions):   # DÙNG unique_micro_actions THAY VÌ MICRO_ACTIONS
    col = cols[i % 2]
    with col:
        is_selected = action["text"] in st.session_state.selected_actions
        btn_label = f'{action["icon"]} {action["text"]}'
        btn_style = "goc-nho-btn selected" if is_selected else "goc-nho-btn"
        btn_key = f"action_{i}"
        if st.button(btn_label, key=btn_key):
            # Chỉ cần nhấp là xác nhận, không cho bỏ chọn
            if not is_selected:
                st.session_state.selected_actions.append(action["text"])
            st.rerun()
        st.markdown(f'<div class="{btn_style}">{btn_label}</div>', unsafe_allow_html=True)

# --- Checklist: các hoạt động đã chọn ---
if st.session_state.selected_actions:
    st.markdown('<div class="goc-nho-checklist-title">📋 Danh sách việc đã chọn hôm nay:</div>', unsafe_allow_html=True)
    all_done = True
    for i, action_text in enumerate(st.session_state.selected_actions):
        action_icon = next((a["icon"] for a in unique_micro_actions if a["text"] == action_text), "💝")
        done_key = f"done_{action_text}"
        if done_key not in st.session_state:
            st.session_state[done_key] = False
        is_done = st.session_state[done_key]
        cols_done = st.columns([0.12, 0.8, 0.08])
        with cols_done[0]:
            new_state = st.checkbox("", value=is_done, key=f"cb_{action_text}_{i}")
        with cols_done[1]:
            st.markdown(
                f'<div class="goc-nho-checklist-item"><span class="goc-nho-check-icon">{action_icon}</span><span style="font-weight:600;">{action_text}</span></div>',
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

# --- Footer động viên ---
st.markdown('<div class="goc-nho-footer">💜 <strong>Nhớ nhé:</strong> Mỗi hành động nhỏ đều là một bước tiến lớn trong việc chăm sóc bản thân. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)
