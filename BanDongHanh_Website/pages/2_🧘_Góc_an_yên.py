import streamlit as st
import time
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import add_mood_entry, get_mood_entries

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Góc An Yên", page_icon="🧘", layout="centered")

# --- GIAO DIỆN CHÍNH ---
st.title("🧘 Góc An Yên")

# *** NAVIGATION LINK ***
st.markdown("⬅️ [Quay về Trang chủ](../0_💖_Trang_chủ.py)")

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

    if st.button("Bắt đầu hít thở", type="primary", use_container_width=True):
        placeholder = st.empty()
        progress_bar = st.progress(0, text="Bắt đầu thực hành...")
        start_time = time.time()
        end_time = start_time + duration

        while time.time() < end_time:
            steps = ["Hít vào (4s)", "Giữ hơi (4s)", "Thở ra (4s)", "Nghỉ (4s)"]
            
            for step in steps:
                if time.time() >= end_time:
                    break
                
                with placeholder.container():
                    st.markdown(f"<h2 style='text-align: center; color: #2E8B57;'>{step}</h2>", unsafe_allow_html=True)
                    if "Hít vào" in step:
                        st.image("https://i.imgur.com/D4Jc0Vz.gif", use_column_width=True)
                    elif "Thở ra" in step:
                        st.image("https://i.imgur.com/O4g3eFz.gif", use_column_width=True)
                    else:
                        st.image("https://i.imgur.com/y3yL4hA.png", use_column_width=True)
                
                step_start_time = time.time()
                while time.time() < step_start_time + 4:
                    if time.time() >= end_time:
                        break
                    
                    progress_percent = (time.time() - start_time) / duration
                    progress_bar.progress(min(progress_percent, 1.0), text=f"Đang thực hành: {step}")
                    time.sleep(0.1)

        placeholder.success("Hoàn thành! Bạn đã làm rất tốt. Hãy cảm nhận sự bình yên trong cơ thể nhé.")
        progress_bar.progress(100, text="Đã hoàn thành!")
        
        # Thêm nút chia sẻ cảm nhận sau khi hoàn thành
        st.write("---")
        if st.button("💬 Chia sẻ cảm nhận", key="share_breathing", use_container_width=True):
            st.session_state.show_breathing_sharing = True
            st.rerun()

    # Hiển thị form chia sẻ cảm nhận nếu được kích hoạt
    if st.session_state.get("show_breathing_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn về bài tập hít thở:")
        feeling_content = st.text_area(
            "Cảm nhận của bạn:",
            placeholder="Ví dụ: Sau khi thực hành, tôi cảm thấy bình tĩnh hơn và dễ tập trung hơn...",
            key="breathing_feeling",
            help="Hãy mô tả những gì bạn cảm nhận được sau khi thực hành bài tập hít thở"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký cảm xúc", key="save_breathing", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Hơi Thở Nhiệm Màu", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký cảm xúc!")
                    st.session_state.show_breathing_sharing = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        
        with col2:
            if st.button("❌ Hủy", key="cancel_breathing", use_container_width=True):
                st.session_state.show_breathing_sharing = False
                st.rerun()

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
    
    # Thêm nút chia sẻ cảm nhận cho bài tập 5-4-3-2-1
    if st.button("💬 Chia sẻ cảm nhận", key="share_543", use_container_width=True):
        st.session_state.show_543_sharing = True
        st.rerun()

    # Hiển thị form chia sẻ cảm nhận nếu được kích hoạt
    if st.session_state.get("show_543_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn về bài tập 5-4-3-2-1:")
        feeling_content = st.text_area(
            "Cảm nhận của bạn:",
            placeholder="Ví dụ: Bài tập giúp tôi tập trung vào hiện tại và quên đi những lo lắng...",
            key="543_feeling",
            help="Hãy mô tả những gì bạn cảm nhận được khi thực hành bài tập 5-4-3-2-1"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký cảm xúc", key="save_543", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Chạm Vào Hiện Tại (5-4-3-2-1)", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký cảm xúc!")
                    st.session_state.show_543_sharing = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        
        with col2:
            if st.button("❌ Hủy", key="cancel_543", use_container_width=True):
                st.session_state.show_543_sharing = False
                st.rerun()

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
    if st.button("Bắt đầu 1 phút quan sát", type="primary", key="quan_sat", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(61):
            progress_value = i / 60.0
            progress_bar.progress(min(progress_value, 1.0))
            status_text.text(f"Thời gian còn lại: {60-i} giây")
            time.sleep(1)
            
        status_text.success("Đã hết một phút. Cảm ơn bạn đã dành thời gian cho chính mình. ❤️")
        
        # Thêm nút chia sẻ cảm nhận sau khi hoàn thành quan sát
        st.write("---")
        if st.button("💬 Chia sẻ cảm nhận", key="share_observation", use_container_width=True):
            st.session_state.show_observation_sharing = True
            st.rerun()

    # Hiển thị form chia sẻ cảm nhận nếu được kích hoạt
    if st.session_state.get("show_observation_sharing", False):
        st.markdown("#### 💭 Hãy chia sẻ cảm nhận của bạn về bài tập quan sát:")
        feeling_content = st.text_area(
            "Cảm nhận của bạn:",
            placeholder="Ví dụ: Khi quan sát không phán xét, tôi cảm thấy thư giãn và nhận ra nhiều điều mới...",
            key="observation_feeling",
            help="Hãy mô tả những gì bạn cảm nhận được khi thực hành bài tập quan sát"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💾 Lưu vào nhật ký cảm xúc", key="save_observation", use_container_width=True):
                if feeling_content.strip():
                    add_mood_entry("Ô Cửa Sổ Thần Kỳ", feeling_content.strip())
                    st.success("✅ Đã lưu cảm nhận vào nhật ký cảm xúc!")
                    st.session_state.show_observation_sharing = False
                    time.sleep(1)
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập cảm nhận của bạn trước khi lưu!")
        
        with col2:
            if st.button("❌ Hủy", key="cancel_observation", use_container_width=True):
                st.session_state.show_observation_sharing = False
                st.rerun()

# --- PHẦN XEM LỊCH SỬ GÓCA AN YÊN ---
st.write("---")
st.header("📖 Lịch Sử Góc An Yên")

if st.button("📖 Xem lịch sử Góc An Yên", use_container_width=True):
    st.session_state.show_history = not st.session_state.get("show_history", False)

if st.session_state.get("show_history", False):
    st.markdown("### 💭 Các cảm nhận đã lưu từ Góc An Yên:")
    
    # Lấy tất cả entries từ Góc An Yên (tất cả 3 loại bài tập)
    all_entries = get_mood_entries()
    goc_an_yen_exercises = ["Hơi Thở Nhiệm Màu", "Chạm Vào Hiện Tại (5-4-3-2-1)", "Ô Cửa Sổ Thần Kỳ"]
    
    # Lọc entries từ Góc An Yên
    goc_an_yen_entries = [entry for entry in all_entries if entry["exercise_type"] in goc_an_yen_exercises]
    
    if goc_an_yen_entries:
        # Sắp xếp theo thời gian mới nhất trước
        goc_an_yen_entries.sort(key=lambda x: x["timestamp"], reverse=True)
        
        for entry in goc_an_yen_entries:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Chọn emoji theo loại bài tập
                    if entry["exercise_type"] == "Hơi Thở Nhiệm Màu":
                        icon = "🌬️"
                    elif entry["exercise_type"] == "Chạm Vào Hiện Tại (5-4-3-2-1)":
                        icon = "🖐️"
                    else:
                        icon = "🖼️"
                    
                    st.markdown(f"""
                    <div style="background-color: #f0f8ff; border-left: 4px solid #4682b4; 
                                padding: 1rem; border-radius: 8px; margin-bottom: 10px;">
                        <div style="font-size: 0.9em; color: #666; margin-bottom: 5px;">
                            {icon} <strong>{entry["exercise_type"]}</strong> • {entry["timestamp"]}
                        </div>
                        <div style="color: #333; line-height: 1.4;">
                            {entry["content"]}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.write("")  # Add spacing between entries
    else:
        st.info("💡 Chưa có cảm nhận nào được lưu từ Góc An Yên. Hãy thực hành một bài tập và chia sẻ cảm nhận của bạn!")

    if st.button("🔄 Làm mới lịch sử", key="refresh_history"):
        st.rerun()
