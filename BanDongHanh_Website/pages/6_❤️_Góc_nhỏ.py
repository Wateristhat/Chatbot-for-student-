import streamlit as st
import random

RO_ACTIONS = [
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

# --- LOẠI TRÙNG LẶP GIỮ NGUYÊN THỨ TỰ ---
unique_ro_actions = []
seen = set()
for act in RO_ACTIONS:
    key = f"{act['icon']}|{act['text']}"
    if key not in seen:
        unique_ro_actions.append(act)
        seen.add(key)

# --- CHIA ĐỀU 2 CỘT ---
half = (len(unique_ro_actions)+1) // 2
left_col_actions = unique_ro_actions[:half]
right_col_actions = unique_ro_actions[half:]

# --- Assistant box giữ nguyên ---
st.markdown("""
<div style="background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 28px; box-shadow: 0 4px 24px rgba(124,77,255,.10); padding: 2.2rem 2.3rem 1.3rem 2.3rem; margin-bottom:2rem; margin-top:1rem; text-align: center; border: 3px solid #e1bee7;">
    <div style="font-size:2.4rem; margin-bottom:0.7rem;">🤖</div>
    <div style="font-size:1.25rem; font-weight:700; color:#6d28d9;">Bạn cần gợi ý hoặc trợ giúp? Trợ lý ảo luôn sẵn sàng hỗ trợ bạn!</div>
    <div style="display:flex; justify-content: center; gap: 32px; margin-top:1.05rem;">
        <form method="post">
            <button style="background: #fff; border: 2.5px solid #e1bee7; border-radius: 15px; font-size:1.13rem; font-weight:600; color:#6d28d9; padding: 0.8rem 1.3rem; cursor:pointer; box-shadow:0 2px 8px rgba(124,77,255,.10); transition:all 0.17s;" type="submit" name="ask_assist" formnovalidate>💬 Gợi ý hoạt động</button>
        </form>
        <form method="post">
            <button style="background: #fff; border: 2.5px solid #e1bee7; border-radius: 15px; font-size:1.13rem; font-weight:600; color:#6d28d9; padding: 0.8rem 1.3rem; cursor:pointer; box-shadow:0 2px 8px rgba(124,77,255,.10); transition:all 0.17s;" type="submit" name="ask_motivation" formnovalidate>🔊 Động viên tinh thần</button>
        </form>
    </div>
</div>
""", unsafe_allow_html=True)

if st.button("💡 Nhận gợi ý từ trợ lý ảo"):
    suggestion = random.choice([
        "Hãy thử viết ra một điều bạn tự hào về bản thân nhé!",
        "Bạn có thể nghe một bài hát bạn yêu thích để thư giãn.",
        "Vươn vai nhẹ nhàng giúp bạn tỉnh táo hơn đấy!",
        "Mỉm cười với chính mình trong gương - bạn rất đáng yêu!"
    ])
    st.session_state.assistant_message = f"🤖 Trợ lý ảo: {suggestion}"
    st.session_state.assistant_mode = "suggestion"
if st.button("🤖 Động viên tinh thần từ trợ lý ảo"):
    motivation = random.choice([
        "Bạn rất tuyệt vời! Mỗi nỗ lực dù nhỏ đều giúp bạn trưởng thành hơn và hạnh phúc hơn.",
        "Dù hôm nay có khó khăn, bạn vẫn xứng đáng được yêu thương và tự hào về bản thân.",
        "Hãy kiên nhẫn, mọi việc tốt đẹp đều cần thời gian. Bee tin bạn sẽ làm được!",
        "Bạn là người duy nhất trên thế giới, hãy tự tin và yêu thương bản thân mình nhé!"
    ])
    st.session_state.assistant_message = f"🤖 Trợ lý ảo: {motivation}"
    st.session_state.assistant_mode = "motivation"

if "assistant_message" in st.session_state and st.session_state.assistant_message:
    if st.session_state.assistant_mode == "suggestion":
        st.info(st.session_state.assistant_message)
    else:
        st.success(st.session_state.assistant_message)

# --- Title & grid ---
st.markdown('<div style="font-size:2rem;font-weight:700;color:#8e24aa;text-align:center;margin-bottom:1.1rem;">🌈 Chọn từ ngân hàng hoạt động:</div>', unsafe_allow_html=True)

if "selected_actions" not in st.session_state:
    st.session_state.selected_actions = []

cols = st.columns(2)
for idx, col_actions in enumerate([left_col_actions, right_col_actions]):
    with cols[idx]:
        for act in col_actions:
            is_selected = act["text"] in st.session_state.selected_actions
            btn_label = f'{act["icon"]} {act["text"]}'
            btn_key = f"action_{act['icon']}_{act['text']}"
            if st.button(btn_label, key=btn_key):
                if not is_selected:
                    st.session_state.selected_actions.append(act["text"])
                st.rerun()

# --- Checklist: các hoạt động đã chọn ---
if st.session_state.selected_actions:
    st.markdown('<div style="font-size:1.08rem;font-weight:600;color:#333;margin-top:1rem;margin-bottom:0.3rem;text-align:center;">📋 Danh sách việc đã chọn hôm nay:</div>', unsafe_allow_html=True)
    all_done = True
    for i, action_text in enumerate(st.session_state.selected_actions):
        action_icon = next((a["icon"] for a in unique_ro_actions if a["text"] == action_text), "💝")
        done_key = f"done_{action_text}"
        if done_key not in st.session_state:
            st.session_state[done_key] = False
        is_done = st.session_state[done_key]
        cols_done = st.columns([0.12, 0.8, 0.08])
        with cols_done[0]:
            new_state = st.checkbox("", value=is_done, key=f"cb_{action_text}_{i}")
        with cols_done[1]:
            st.markdown(
                f'<div style="background:#f9f9fb; border-radius:10px; padding:0.6rem 0.9rem; margin-bottom:0.6rem; display:flex; align-items:center; font-size:1.01rem; border:1.4px solid #ede7f6;"><span style="font-size:1.08rem;margin-right:0.6rem;">{action_icon}</span><span style="font-weight:600;">{action_text}</span></div>',
                unsafe_allow_html=True
            )
        with cols_done[2]:
            st.markdown(f"<span style='margin-left:auto;font-size:1.1rem;'>{'✅' if is_done else '⬜'}</span>", unsafe_allow_html=True)
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
            '<div style="background:#fffde7;border-radius:17px;padding:1.1rem 1rem;text-align:center;font-size:1.15rem;margin:1.2rem 0;color:#333;border:2px solid #ffd54f;"><b>🎉 CHÚC MỪNG! 🎉</b><br>Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!<br>🌟 Bạn thật tuyệt vời! Hãy tự hào về bản thân nhé! 🌟</div>',
            unsafe_allow_html=True
        )
        st.balloons()

# --- Footer động viên ---
st.markdown('<div style="background:#f3e5f5;border-left:5px solid #ba68c8;border-radius:10px;padding:0.7rem 1rem;text-align:center;font-size:0.98rem;margin:0.3rem 0 1.1rem 0;color:#333;">💜 <strong>Nhớ nhé:</strong> Mỗi hành động nhỏ đều là một bước tiến lớn trong việc chăm sóc bản thân. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)
