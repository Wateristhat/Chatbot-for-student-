import streamlit as st
import random
import style # <-- 1. IMPORT STYLE

# --- 2. THIẾT LẬP CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="Ngân Hàng Hoạt Động", 
    page_icon="🌈", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 3. ÁP DỤNG CSS CHUNG ---
style.apply_global_style()

st.markdown("""
<style>
.gn-assist-bigbox {
    background: linear-gradient(120deg,#e0e7ff 0%,#f3e8ff 100%);
    border-radius: 38px; box-shadow: 0 8px 36px rgba(124,77,255,.13);
    padding: 3.2rem 2.8rem 2.1rem 2.8rem; margin-bottom:2.3rem; margin-top:0.2rem;
    text-align: center; border: 3.5px solid #b39ddb; max-width:1700px; margin-left:auto; margin-right:auto;
}
.gn-assist-icon {font-size:3.2rem; margin-bottom:0.7rem;}
.gn-assist-text {font-size:1.7rem; font-weight:700; color:#6d28d9; margin-bottom:1.1rem;}

/* --- 4. XÓA CSS BUTTON CỤC BỘ --- */
/* (Khối .stButton > button đã bị xóa
   để file style.py chung quản lý, giúp tương thích ĐT) */

/* --- 5. CHUYỂN STYLE INLINE THÀNH CLASS ĐỂ QUẢN LÝ --- */
.gn-assist-response {
    background: #e9f3fd;
    border-radius: 16px;
    padding: 2.2rem 2.8rem;
    font-size: 1.23rem;
    color: #1565c0;
    max-width: 1700px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 1.1rem;
    margin-bottom: 1.1rem;
    box-shadow: 0 2px 18px rgba(21,101,192,0.06);
}
.gn-title {
    font-size:2rem;
    font-weight:700;
    color:#8e24aa;
    text-align:center;
    margin-bottom:1.1rem;
}
.gn-checklist-item {
    background:#f9f9fb; 
    border-radius:10px; 
    padding:0.6rem 0.9rem; 
    margin-bottom:0.6rem; 
    display:flex; 
    align-items:center; 
    font-size:1.01rem; 
    border:1.4px solid #ede7f6;
}
.gn-congrats {
    background:#fffde7;
    border-radius:17px;
    padding:1.1rem 1rem;
    text-align:center;
    font-size:1.15rem;
    margin:1.2rem 0;
    color:#333;
    border:2px solid #ffd54f;
}
.gn-footer {
    background:#f3e5f5;
    border-left:5px solid #ba68c8;
    border-radius:10px;
    padding:0.7rem 1rem;
    text-align:center;
    font-size:0.98rem;
    margin:0.3rem 0 1.1rem 0;
    color:#333;
}
.gn-checklist-title {
    font-size:1.08rem;
    font-weight:600;
    color:#333;
    margin-top:1rem;
    margin-bottom:0.3rem;
    text-align:center;
}

/* --- 6. CSS TƯƠNG THÍCH ĐIỆN THOẠI --- */
@media (max-width: 900px) {
    .gn-assist-bigbox {
        padding: 2rem 1rem 1rem 1rem; 
        max-width: 96vw;
    }
    .gn-assist-text, .gn-assist-response {
        font-size: 1.1rem;
        padding: 1.5rem 1rem;
    }
    .gn-title {
        font-size: 1.5rem;
    }
    .gn-checklist-item {
        font-size: 0.9rem;
        padding: 0.5rem 0.7rem;
    }
    .gn-congrats {
        font-size: 1rem;
    }
    .gn-footer {
        font-size: 0.85rem;
    }
}
</style>
""", unsafe_allow_html=True)
st.markdown(f"""
<div class="gn-assist-bigbox">
    <div class="gn-assist-icon">🤖</div>
    <div class="gn-assist-text">Bạn cần gợi ý hoặc trợ giúp? Trợ lý ảo luôn sẵn sàng hỗ trợ bạn!</div>
</div>
""", unsafe_allow_html=True)

# --- 7. THÊM LINK QUAY VỀ ---
st.page_link("0_💖_Trang_chủ.py", label="⬅️ 🏠 Quay về Trang chủ", icon="🏠")
st.write("---")


col1, col2 = st.columns([2,2])
with col1:
    if st.button("💬 Gợi ý hoạt động", key="suggest_activity"):
        suggestion = random.choice([
            "Hãy thử viết ra một điều bạn tự hào về bản thân nhé!",
            "Bạn có thể nghe một bài hát bạn yêu thích để thư giãn.",
            "Vươn vai nhẹ nhàng giúp bạn tỉnh táo hơn đấy!",
            "Mỉm cười với chính mình trong gương - bạn rất đáng yêu!"
        ])
        st.session_state.assistant_message = f"🤖 Trợ lý ảo: {suggestion}"
        st.session_state.assistant_mode = "suggestion"
with col2:
    if st.button("💜 Động viên tinh thần", key="motivation"):
        motivation = random.choice([
            "Bạn rất tuyệt vời! Mỗi nỗ lực dù nhỏ đều giúp bạn trưởng thành hơn và hạnh phúc hơn.",
            "Dù hôm nay có khó khăn, bạn vẫn xứng đáng được yêu thương và tự hào về bản thân.",
            "Hãy kiên nhẫn, mọi việc tốt đẹp đều cần thời gian. Bee tin bạn sẽ làm được!",
            "Bạn là người duy nhất trên thế giới, hãy tự tin và yêu thương bản thân mình nhé!"
        ])
        st.session_state.assistant_message = f"🤖 Trợ lý ảo: {motivation}"
        st.session_state.assistant_mode = "motivation"
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

if "assistant_message" in st.session_state and st.session_state.assistant_message:
    # --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
    st.markdown(f"""
    <div class="gn-assist-response">
        {st.session_state.assistant_message}
    </div>
    """, unsafe_allow_html=True)

# --- Title & grid ---
# --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
st.markdown('<div class="gn-title">🌈 Chọn từ ngân hàng hoạt động:</div>', unsafe_allow_html=True)

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
    # --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
    st.markdown('<div class="gn-checklist-title">📋 Danh sách việc đã chọn hôm nay:</div>', unsafe_allow_html=True)
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
            # --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
            st.markdown(
                f'<div class="gn-checklist-item"><span style="font-size:1.08rem;margin-right:0.6rem;">{action_icon}</span><span style="font-weight:600;">{action_text}</span></div>',
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
        # --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
        st.markdown(
            '<div class="gn-congrats"><b>🎉 CHÚC MỪNG! 🎉</b><br>Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay!<br>🌟 Bạn thật tuyệt vời! Hãy tự hào về bản thân nhé! 🌟</div>',
            unsafe_allow_html=True
        )
        st.balloons()

# --- Footer động viên ---
# --- 8. SỬ DỤNG CLASS THAY VÌ STYLE INLINE ---
st.markdown('<div class="gn-footer">💜 <strong>Nhớ nhé:</strong> Mỗi hành động nhỏ đều là một bước tiến lớn trong việc chăm sóc bản thân. Hãy kiên nhẫn và yêu thương chính mình! 💜</div>', unsafe_allow_html=True)
