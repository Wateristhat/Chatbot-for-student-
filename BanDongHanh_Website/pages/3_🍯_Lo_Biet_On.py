import streamlit as st
import random
import html

st.set_page_config(page_title="Lọ Biết Ơn", page_icon="🍯", layout="centered")

st.title("🍯 Lọ Biết Ơn")
st.markdown("Mỗi ngày, hãy gieo một hạt mầm biết ơn vào chiếc lọ này. Dần dần, bạn sẽ có cả một khu vườn an vui trong tâm hồn.")
st.write("---")

if 'gratitude_notes' not in st.session_state:
    st.session_state.gratitude_notes = []

prompts = [
    "Hôm nay, ai đã làm bạn mỉm cười?",
    "Điều gì nhỏ bé trong ngày hôm nay khiến bạn cảm thấy vui?",
    "Bạn biết ơn món ăn nào hôm nay?",
    "Hãy nghĩ về một người bạn và điều bạn trân trọng ở họ.",
    "Kể tên một bài hát khiến bạn cảm thấy yêu đời."
]

st.info(random.choice(prompts))

note = st.text_area("Viết điều bạn biết ơn vào đây...", height=100, placeholder="Ví dụ: Mình biết ơn vì hôm nay trời nắng đẹp...")

if st.button("Thêm vào lọ biết ơn", type="primary"):
    if note:
        st.session_state.gratitude_notes.append(note)
        st.success("Đã thêm một hạt mầm biết ơn vào lọ! 🌱")
        st.balloons()
        time.sleep(1)
        st.rerun()
    else:
        st.warning("Bạn ơi, hãy viết gì đó vào ô bên trên nhé!")

st.write("---")

if st.session_state.gratitude_notes:
    st.subheader("Những điều bạn biết ơn:")
    for n in reversed(st.session_state.gratitude_notes):
        st.markdown(
            f"""
            <div style="background-color: #FFF8DC; border-left: 5px solid #FFD700; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <p style="color: #333;">{html.escape(n)}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
else:
    st.write("Chiếc lọ của bạn đang chờ những điều biết ơn đầu tiên. ❤️")
