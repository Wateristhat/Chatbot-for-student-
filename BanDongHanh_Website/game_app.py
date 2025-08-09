import streamlit as st

st.set_page_config(page_title="Trò chơi tránh vật cản", page_icon="🎮")

st.title("🎮 Trò chơi Tránh Vật Cản")
st.markdown(
    "<div style='font-size:1.15rem'>"
    "Hãy nhấn phím SPACE để chơi trò chơi! Tránh các vật cản để ghi điểm.<br>"
    "<b>Chúc bạn chơi vui vẻ!</b>"
    "</div>", unsafe_allow_html=True
)
st.write("---")

# Nhúng trò chơi HTML5
game_html = """
<iframe src="game.html" width="480" height="400" frameborder="0"></iframe>
"""
st.components.v1.html(game_html, height=400)
