import streamlit as st
import random

st.set_page_config(page_title="Trò Chơi Trí Tuệ", page_icon="🎲", layout="centered")

st.title("🎲 Trò Chơi Trí Tuệ")
st.markdown("Cùng thư giãn với những trò chơi nhẹ nhàng để rèn luyện sự tập trung và trí nhớ nhé!")
st.write("---")

st.header("🧠 Nối Hình Giống Nhau")

ICONS = "🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐸🐵".split()

def setup_game(rows, cols):
    if rows * cols % 2 != 0:
        st.error("Số ô phải là số chẵn!")
        return
    num_pairs = (rows * cols) // 2
    icons_for_game = random.sample(ICONS, num_pairs) * 2
    random.shuffle(icons_for_game)
    st.session_state.board = [[icons_for_game.pop() for _ in range(cols)] for _ in range(rows)]
    st.session_state.flipped = [[False for _ in range(cols)] for _ in range(rows)]
    st.session_state.matched = [[False for _ in range(cols)] for _ in range(rows)]
    st.session_state.first_pick = None
    st.session_state.second_pick = None
    st.session_state.moves = 0
    st.session_state.game_over = False

difficulty = st.selectbox("Chọn độ khó:", ["Dễ (2x4)", "Vừa (4x4)", "Khó (4x5)"])

rows, cols = 0, 0
if difficulty == "Dễ (2x4)":
    rows, cols = 2, 4
elif difficulty == "Vừa (4x4)":
    rows, cols = 4, 4
elif difficulty == "Khó (4x5)":
    rows, cols = 4, 5

if 'board' not in st.session_state or st.button("Chơi lại/Bắt đầu ván mới", type="primary"):
    setup_game(rows, cols)
    st.rerun()

if 'board' in st.session_state:
    if st.session_state.game_over:
        st.success(f"🎉 Chúc mừng! Bạn đã hoàn thành trò chơi sau {st.session_state.moves} lượt. 🎉")
        st.balloons()
    else:
        st.info(f"Số lượt đã đi: {st.session_state.moves}")
        grid = st.container()
        for r in range(rows):
            grid_cols = st.columns(cols)
            for c in range(cols):
                is_flipped = st.session_state.flipped[r][c]
                is_matched = st.session_state.matched[r][c]
                button_label = st.session_state.board[r][c] if is_flipped or is_matched else "❓"
                
                if grid_cols[c].button(button_label, key=f"btn_{r}_{c}", use_container_width=True, disabled=is_matched):
                    if st.session_state.second_pick:
                        r1, c1 = st.session_state.first_pick
                        r2, c2 = st.session_state.second_pick
                        if st.session_state.board[r1][c1] != st.session_state.board[r2][c2]:
                            st.session_state.flipped[r1][c1] = False
                            st.session_state.flipped[r2][c2] = False
                        st.session_state.first_pick, st.session_state.second_pick = None, None

                    if not st.session_state.flipped[r][c]:
                        st.session_state.flipped[r][c] = True
                        if not st.session_state.first_pick:
                            st.session_state.first_pick = (r, c)
                        else:
                            st.session_state.second_pick = (r, c)
                            st.session_state.moves += 1
                            r1, c1 = st.session_state.first_pick
                            r2, c2 = st.session_state.second_pick
                            if st.session_state.board[r1][c1] == st.session_state.board[r2][c2]:
                                st.session_state.matched[r1][c1] = True
                                st.session_state.matched[r2][c2] = True
                                st.session_state.first_pick, st.session_state.second_pick = None, None
                                if all(all(row) for row in st.session_state.matched):
                                    st.session_state.game_over = True
                    st.rerun()
