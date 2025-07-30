import streamlit as st
import time

st.set_page_config(page_title="Góc Thư Giãn", layout="wide")
st.title("🧘 Góc Thư Giãn")
st.write("Hãy dành một chút thời gian để hít thở sâu và lắng nghe những âm thanh nhẹ nhàng nhé.")

# --- Bài tập hít thở ---
st.header("Bài tập hít thở hộp (4-4-4-4)")
if st.button("Bắt đầu hít thở"):
    placeholder = st.empty()
    for i in range(3): # Lặp lại 3 lần
        placeholder.info("Chuẩn bị...")
        time.sleep(2)
        placeholder.success("Hít vào bằng mũi... (4 giây)")
        time.sleep(4)
        placeholder.warning("Giữ hơi... (4 giây)")
        time.sleep(4)
        placeholder.success("Thở ra từ từ bằng miệng... (4 giây)")
        time.sleep(4)
        placeholder.warning("Nghỉ... (4 giây)")
        time.sleep(4)
    placeholder.success("Hoàn thành! Bạn cảm thấy tốt hơn rồi chứ?")

# --- Âm thanh thiên nhiên ---
st.header("Lắng nghe âm thanh thiên nhiên")
tab1, tab2, tab3 = st.tabs(["Tiếng mưa 🌧️", "Suối chảy 🏞️", "Nhạc thiền 🕉️"])

with tab1:
    st.video("https://www.youtube.com/watch?v=eKFTSSKCzWA")

with tab2:
    st.video("https://www.youtube.com/watch?v=gM_r4c6i25s")

with tab3:
    st.video("https://www.youtube.com/watch?v=aIIEI33EUqI")