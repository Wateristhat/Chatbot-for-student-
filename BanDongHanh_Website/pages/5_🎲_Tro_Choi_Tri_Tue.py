import streamlit as st
import random

st.set_page_config(page_title="Trò Chơi Trí Tuệ Đơn Giản", page_icon="🎲", layout="centered")

st.title("🎲 Trò Chơi Nhận Biết Màu Sắc")
st.markdown(
    "<div style='font-size:1.15rem'>"
    "Bạn hãy chọn đúng màu theo yêu cầu. Trò chơi này rất đơn giản, phù hợp cho mọi đối tượng, kể cả người khiếm khuyết về trí tuệ.<br>"
    "<b>Chúc bạn vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Danh sách các màu cơ bản
COLOR_LIST = [
    {"name": "Đỏ", "code": "#FF3333"},
    {"name": "Vàng", "code": "#FFD600"},
    {"name": "Xanh Lá", "code": "#4CAF50"},
    {"name": "Xanh Dương", "code": "#2196F3"},
    {"name": "Tím", "code": "#9C27B0"},
    {"name": "Cam", "code": "#FF9800"},
    {"name": "Hồng", "code": "#FF69B4"},
    {"name": "Nâu", "code": "#795548"},
]

if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'question' not in st.session_state or st.button("Chơi lại/Bắt đầu mới", type="primary"):
    st.session_state.question = random.choice(COLOR_LIST)
    st.session_state.options = random.sample(COLOR_LIST, k=4)
    if st.session_state.question not in st.session_state.options:
        # Đảm bảo đáp án luôn nằm trong options
        st.session_state.options[random.randint(0, 3)] = st.session_state.question
    st.session_state.answered = False
    st.session_state.round = 1
    st.session_state.score = 0

st.header(f"🟢 Vòng {st.session_state.round}")
st.subheader("Chọn đúng màu:")

# Hiển thị tên màu cần chọn với màu chữ đen rõ ràng
st.markdown(
    f"<div style='font-size:2.4rem;font-weight:bold;color:#222;margin:16px 0 24px'>{st.session_state.question['name']}</div>",
    unsafe_allow_html=True
)

cols = st.columns(2)
selected = None

for idx, color in enumerate(st.session_state.options):
    btn = cols[idx % 2].button(
        label=" ",
        key=f"color_btn_{idx}_{st.session_state.round}",
        help=f"Đây là màu {color['name']}",
        use_container_width=True
    )
    # CSS cho nút màu lớn
    st.markdown(
        f"""
        <style>
        div[data-testid="column"]:nth-of-type({idx%2+1}) button[kind="secondary"] {{
            height: 85px !important;
            background: {color['code']} !important;
            border-radius: 20px;
            border: 3px solid #ddd;
            margin: 12px 0 24px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    if btn and not st.session_state.get('answered', False):
        selected = color

if selected:
    st.session_state.answered = True
    if selected == st.session_state.question:
        st.success("🎉 Chính xác! Bạn đã chọn đúng màu.", icon="✅")
        st.session_state.score += 1
        st.balloons()
    else:
        st.error(f"❌ Sai rồi! Đây là màu {selected['name']}.", icon="❌")
    # Sau khi trả lời, tự chuyển sang câu tiếp theo sau 1.5s
    st.experimental_rerun()

if st.session_state.get('answered', False):
    if st.button("Câu tiếp theo ➡️", type="primary"):
        st.session_state.round += 1
        st.session_state.question = random.choice(COLOR_LIST)
        st.session_state.options = random.sample(COLOR_LIST, k=4)
        if st.session_state.question not in st.session_state.options:
            st.session_state.options[random.randint(0, 3)] = st.session_state.question
        st.session_state.answered = False
        st.experimental_rerun()

# Hiển thị điểm số
st.write("---")
st.info(f"🌟 Số câu trả lời đúng: {st.session_state.score}", icon="💡")

st.write("<br>", unsafe_allow_html=True)
st.caption("Trò chơi dành cho mọi người, kể cả các bạn nhỏ hoặc người khiếm khuyết về trí tuệ. Chỉ cần bấm đúng màu là được nhé!")
