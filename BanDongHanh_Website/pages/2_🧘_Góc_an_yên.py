# pages/Goc_an_yen.py
import streamlit as st
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Góc An Yên", page_icon="🧘", layout="centered")

# --- GIAO DIỆN CHÍNH ---
st.title("🧘 Góc An Yên")

# *** ĐÃ THÊM: Liên kết quay về Trang chủ ***
st.page_link("Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown("Dành một vài phút để kết nối lại với bản thân và tìm thấy sự tĩnh lặng.")
st.write("---")

# --- CÁC TAB CHỨC NĂNG ---
tab1, tab2, tab3 = st.tabs(["🌬️ Hơi Thở Nhiệm Màu", "🖐️ Chạm Vào Hiện Tại", "🖼️ Ô Cửa Sổ Thần Kỳ"])

# --- TAB 1: BÀI TẬP HÍT THỞ ---
with tab1:
    st.header("🌬️ Hơi Thở Nhiệm Màu")
    st.write("Bài tập thở hộp (box breathing) giúp làm dịu hệ thần kinh và giảm căng thẳng. Hãy cùng nhau thực hành nhé.")

    duration = st.select_slider(
        "Chọn thời gian thực hành (giây):",
        options=[60, 120, 180],
        value=60
    )

    if st.button("Bắt đầu hít thở", type="primary"):
        placeholder = st.empty()
        progress_bar = st.progress(0, text="Bắt đầu thực hành...")
        start_time = time.time()
        end_time = start_time + duration

        # Vòng lặp chính điều khiển toàn bộ quá trình
        while time.time() < end_time:
            steps = ["Hít vào (4s)", "Giữ hơi (4s)", "Thở ra (4s)", "Nghỉ (4s)"]
            
            for step in steps:
                if time.time() >= end_time:
                    break
                
                # Cập nhật giao diện cho bước hiện tại
                with placeholder.container():
                    st.markdown(f"<h2 style='text-align: center; color: #2E8B57;'>{step}</h2>", unsafe_allow_html=True)
                    if "Hít vào" in step:
                        st.image("https://i.imgur.com/D4Jc0Vz.gif", use_column_width=True)
                    elif "Thở ra" in step:
                        st.image("https://i.imgur.com/O4g3eFz.gif", use_column_width=True)
                    else: # Ảnh tĩnh cho "Giữ hơi" và "Nghỉ"
                        st.image("https://i.imgur.com/y3yL4hA.png", use_column_width=True)
                
                # Vòng lặp con để chạy chính xác trong 4 giây và cập nhật thanh tiến trình
                step_start_time = time.time()
                while time.time() < step_start_time + 4:
                    if time.time() >= end_time:
                        break
                    
                    # Tính toán và cập nhật thanh tiến trình
                    progress_percent = (time.time() - start_time) / duration
                    progress_bar.progress(min(progress_percent, 1.0), text=f"Đang thực hành: {step}")
                    time.sleep(0.1) # Ngủ một chút để giao diện mượt mà

        # Hoàn thành
        placeholder.success("Hoàn thành! Bạn đã làm rất tốt. Hãy cảm nhận sự bình yên trong cơ thể nhé.")
        progress_bar.progress(100, text="Đã hoàn thành!")

# --- TAB 2: BÀI TẬP 5-4-3-2-1 ---
with tab2:
    st.header("🖐️ Chạm Vào Hiện Tại (5-4-3-2-1)")
    st.write("Khi cảm thấy choáng ngợp, bài tập này giúp bạn quay về với thực tại bằng cách sử dụng các giác quan.")
    st.info("**Bước 1: 5 thứ bạn có thể THẤY** 👀")
    st.write("Ví dụ: cái bàn, cây bút, bức tranh, cửa sổ, chiếc lá.")
    st.info("**Bước 2: 4 thứ bạn có thể CHẠM** 🖐️")
    st.write("Ví dụ: mặt bàn láng mịn, vải quần jean, làn gió mát, ly nước lạnh.")
    st.info("**Bước 3: 3 thứ bạn có thể NGHE** 👂")
    st.write("Ví dụ: tiếng chim hót, tiếng quạt máy, tiếng gõ phím.")
    st.info("**Bước 4: 2 thứ bạn có thể NGỬI** 👃")
    st.write("Ví dụ: mùi cà phê, mùi sách cũ, mùi cỏ cây sau mưa.")
    st.info("**Bước 5: 1 thứ bạn có thể NẾM** 👅")
    st.write("Ví dụ: vị ngọt của trà, vị thanh của nước lọc.")
    st.success("Tuyệt vời! Bạn đã kết nối thành công với hiện tại.")

# --- TAB 3: BÀI TẬP QUAN SÁT ---
with tab3:
    st.header("🖼️ Ô Cửa Sổ Thần Kỳ")
    st.write("Một bài tập đơn giản để thực hành quan sát không phán xét.")
    st.markdown("""
    **Hướng dẫn:**
    1.  Hãy dành một phút nhìn ra ngoài cửa sổ.
    2.  Đừng cố gắng đặt tên cho những gì bạn thấy. Chỉ cần chú ý đến **màu sắc**, **hình dạng** và **sự chuyển động**.
    3.  Hãy nhìn mọi thứ như thể bạn đang thấy chúng lần đầu tiên.
    """)
    if st.button("Bắt đầu 1 phút quan sát", type="primary", key="quan_sat"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Vòng lặp 60 giây, mỗi giây cập nhật một lần
        for i in range(61):
            progress_value = i / 60.0
            progress_bar.progress(min(progress_value, 1.0))
            status_text.text(f"Thời gian còn lại: {60-i} giây")
            time.sleep(1)
            
        status_text.success("Đã hết một phút. Cảm ơn bạn đã dành thời gian cho chính mình. ❤️")
