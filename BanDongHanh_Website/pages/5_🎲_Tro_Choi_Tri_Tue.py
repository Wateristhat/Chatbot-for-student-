import streamlit as st
import random
import time

st.set_page_config(page_title="Trò Chơi Trí Tuệ Nâng Cấp", page_icon="🎮", layout="centered")

# CSS tùy chỉnh
st.markdown(
    """
    <style>
    .stButton button {
        font-size: 1rem;
        font-weight: bold;
        padding: 0.6rem 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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

# Khởi tạo trạng thái
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'answered' not in st.session_state:
    st.session_state.answered = False
if 'highscore' not in st.session_state:
    st.session_state.highscore = 0
if 'timer' not in st.session_state:
    st.session_state.timer = 30

# Khởi tạo câu hỏi mới
def new_question():
    st.session_state.question = random.choice(COLOR_LIST)
    st.session_state.options = random.sample(COLOR_LIST, k=4)
    if st.session_state.question not in st.session_state.options:
        st.session_state.options[random.randint(0, 3)] = st.session_state.question
    st.session_state.answered = False
    st.session_state.timer = 30

if 'question' not in st.session_state:
    new_question()

# Hiển thị tiêu đề
st.title("🎮 Trò Chơi Nhận Biết Màu Sắc - Nâng Cấp")
st.markdown(
    "<div style='font-size:1.15rem'>"
    "Chọn đúng màu theo yêu cầu trong thời gian quy định. Chế độ khó sẽ tăng thử thách bằng cách pha trộn các màu sắc.<br>"
    "<b>Chúc bạn vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Bộ đếm thời gian
col1, col2 = st.columns([1, 3])
with col1:
    st.metric(label="⏳ Thời gian", value=f"{st.session_state.timer} giây")
with col2:
    st.metric(label="🌟 Điểm cao nhất", value=st.session_state.highscore)

# Đếm ngược thời gian
if not st.session_state.answered:
    if st.session_state.timer > 0:
        time.sleep(1)
        st.session_state.timer -= 1
        st.experimental_rerun()
    else:
        st.error("⏰ Hết giờ! Bạn đã không trả lời kịp thời.", icon="❌")
        st.session_state.answered = True

# Hiển thị câu hỏi
st.header(f"🟢 Vòng {st.session_state.round}")
st.subheader("Chọn đúng màu:")
st.markdown(
    f"<div style='font-size:2.4rem;font-weight:bold;color:#222;margin:16px 0 24px'>{st.session_state.question['name']}</div>",
    unsafe_allow_html=True
)

# Hiển thị các nút màu
cols = st.columns(2)
selected = None
for idx, color in enumerate(st.session_state.options):
    btn = cols[idx % 2].button(
        label=" ",
        key=f"color_btn_{idx}_{st.session_state.round}",
        help=f"Đây là màu {color['name']}",
        use_container_width=True
    )
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
    if btn and not st.session_state.answered:
        selected = color

# Xử lý câu trả lời
if selected:
    st.session_state.answered = True
    if selected == st.session_state.question:
        st.success("🎉 Chính xác! Bạn đã chọn đúng màu.", icon="✅")
        st.session_state.score += 1
        st.session_state.highscore = max(st.session_state.score, st.session_state.highscore)
        st.balloons()
    else:
        st.error(f"❌ Sai rồi! Đây là màu {selected['name']}.", icon="❌")
    st.experimental_rerun()

# Nút tiếp theo
if st.session_state.answered:
    if st.button("Câu tiếp theo ➡️", type="primary"):
        st.session_state.round += 1
        new_question()
        st.experimental_rerun()

# Hiển thị điểm số
st.write("---")
st.info(f"🌟 Số câu trả lời đúng: {st.session_state.score}", icon="💡")

st.caption("Trò chơi thú vị và thử thách, hãy cố gắng đạt điểm cao nhất!")
