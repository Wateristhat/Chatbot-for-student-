import streamlit as st
import time
import random

# Cấu hình trang
st.set_page_config(page_title="🏎️ Đua Xe Ảo", page_icon="🏎️", layout="centered")

# Khởi tạo trạng thái
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'highscore' not in st.session_state:
    st.session_state.highscore = 0
if 'obstacle_position' not in st.session_state:
    st.session_state.obstacle_position = random.randint(0, 4)
if 'player_position' not in st.session_state:
    st.session_state.player_position = 2
if 'game_active' not in st.session_state:
    st.session_state.game_active = True

# Tiêu đề trò chơi
st.title("🏎️ Đua Xe Ảo")
st.markdown(
    "<div style='font-size:1.15rem'>"
    "Điều khiển xe của bạn để tránh các chướng ngại vật! Mỗi lần tránh thành công, bạn sẽ nhận được điểm.<br>"
    "<b>Chúc bạn vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Hiển thị điểm số
col1, col2 = st.columns(2)
col1.metric(label="🌟 Điểm hiện tại", value=st.session_state.score)
col2.metric(label="🏆 Điểm cao nhất", value=st.session_state.highscore)

# Hiển thị đường đua
def render_race():
    road = ["🛣️"] * 5
    player_icon = "🚗"
    obstacle_icon = "🚧"

    # Vẽ xe của người chơi
    road[st.session_state.player_position] = player_icon

    # Vẽ chướng ngại vật
    road[st.session_state.obstacle_position] = obstacle_icon

    # Hiển thị đường đua
    st.markdown(
        f"<div style='font-size:2rem;text-align:center'>{''.join(road)}</div>",
        unsafe_allow_html=True
    )

# Điều khiển xe
def move_left():
    if st.session_state.player_position > 0:
        st.session_state.player_position -= 1

def move_right():
    if st.session_state.player_position < 4:
        st.session_state.player_position += 1

# Nút điều khiển
col1, col2 = st.columns(2)
col1.button("⬅️ Sang Trái", on_click=move_left)
col2.button("➡️ Sang Phải", on_click=move_right)

# Xử lý logic trò chơi
if st.session_state.game_active:
    render_race()

    # Kiểm tra va chạm
    if st.session_state.player_position == st.session_state.obstacle_position:
        st.error("💥 Bạn đã va chạm với chướng ngại vật! Trò chơi kết thúc.", icon="❌")
        st.session_state.game_active = False
    else:
        st.session_state.score += 1
        st.session_state.highscore = max(st.session_state.highscore, st.session_state.score)
        st.session_state.obstacle_position = random.randint(0, 4)
        time.sleep(0.5)  # Tăng tốc độ chướng ngại vật

# Nút chơi lại
if not st.session_state.game_active and st.button("🔄 Chơi lại"):
    st.session_state.score = 0
    st.session_state.player_position = 2
    st.session_state.obstacle_position = random.randint(0, 4)
    st.session_state.game_active = True
    st.experimental_rerun()
