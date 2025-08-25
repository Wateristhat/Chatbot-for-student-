import streamlit as st

st.set_page_config(page_title="Góc nhỏ", page_icon="❤️", layout="centered")

st.title("❤️ Góc nhỏ")
st.markdown("Chăm sóc bản thân không phải là ích kỷ, đó là điều cần thiết. Hãy bắt đầu với những hành động nhỏ mỗi ngày nhé.")
st.write("---")

MICRO_ACTIONS = [
    "Uống một ly nước đầy.",
    "Vươn vai và duỗi người trong 1 phút.",
    "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp.",
    "Nghe một bài hát bạn yêu thích.",
    "Viết ra 1 điều bạn tự hào về bản thân.",
    "Rửa mặt với nước mát.",
    "Sắp xếp lại góc học tập/làm việc.",
    "Mỉm cười với chính mình trong gương."
]

st.header("Xây dựng kế hoạch cho hôm nay")
st.write("Chọn những việc nhỏ bạn muốn làm hôm nay để chăm sóc bản thân.")

if 'selected_actions' not in st.session_state:
    st.session_state.selected_actions = []

selected = st.multiselect(
    "Chọn từ ngân hàng gợi ý:",
    options=MICRO_ACTIONS,
    default=st.session_state.selected_actions
)
st.session_state.selected_actions = selected

st.write("---")

if not st.session_state.selected_actions:
    st.info("Hãy chọn ít nhất một hành động để bắt đầu kế hoạch của bạn nhé!")
else:
    st.subheader("Danh sách việc cần làm của bạn hôm nay:")
    all_done = True
    for action in st.session_state.selected_actions:
        if f"action_{action}" not in st.session_state:
            st.session_state[f"action_{action}"] = False
        
        is_done = st.checkbox(action, key=f"cb_{action}", value=st.session_state[f"action_{action}"])
        
        if is_done and not st.session_state[f"action_{action}"]:
            st.toast(f"Tuyệt vời! Bạn đã hoàn thành: {action}", icon="🎉")
        
        st.session_state[f"action_{action}"] = is_done
        if not is_done:
            all_done = False

    if all_done:
        st.success("🎉 Chúc mừng! Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay. Bạn thật tuyệt vời!")
        st.balloons()
