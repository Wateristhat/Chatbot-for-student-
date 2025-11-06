# --- File: header_utils.py ---
import streamlit as st
import time

def inject_global_components():
    """
    Chèn Nút Loa Cố Định, Logic Nhắc Nhở, và Thẻ Audio Nhạc Nền. 
    Hàm này được gọi ở đầu MỌI file trang.
    """
    
    # Đảm bảo các biến session state cần thiết tồn tại 
    if 'show_music_prompt' not in st.session_state:
        st.session_state.show_music_prompt = False
    if 'music_playing' not in st.session_state:
        st.session_state.music_playing = False
    if 'music_url' not in st.session_state:
        # Giá trị mặc định (Sẽ được ghi đè bởi app.py)
        st.session_state.music_url = "" 
        
    # --- KHỐI 1: NÚT LOA CỐ ĐỊNH & LOGIC PROMPT ---
    show_prompt = st.session_state.get('show_music_prompt', False)
    music_on = st.session_state.get('music_playing', False)
    icon = "🔊" if music_on else "🔇"

    # Nút Bật/Tắt nhạc nền
    if st.button(icon, key=f"global_music_toggle_button_{hash(st.current_page_name)}"): 
        st.session_state.music_playing = not st.session_state.music_playing
        st.session_state.show_music_prompt = False # Ẩn nhắc nhở khi tương tác
        st.rerun()

    st.markdown(
        """
        <style>
        /* CSS Cố định nút ở góc trên bên phải */
        div[data-testid="stButton"] > button[key*="global_music_toggle_button"] {
            position: fixed; top: 1rem; right: 1rem; z-index: 1000;
            width: 3rem; height: 3rem; border-radius: 50%; 
            font-size: 1.5rem; background-color: #ffffff;
            border: 2px solid #e0e0e0; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

    # Hiển thị thông báo nhắc nhở (CSS cố định)
    if show_prompt:
        st.markdown(
            """
            <div style="position: fixed; top: 70px; right: 20px; z-index: 999; 
                        background-color: #fff3cd; color: #856404; padding: 10px; 
                        border-radius: 8px; border: 1px solid #ffeeba; box-shadow: 0 2px 5px rgba(0,0,0,0.1);">
                🎵 <b>Nhạc nền đã tạm dừng.</b> <br> Bạn muốn bật lại không?
            </div>
            """, unsafe_allow_html=True)
    
    # --- KHỐI 2: NHÚNG AUDIO VÀ JS ĐIỀU KHIỂN (Đặt ở cuối HTML) ---
    is_playing = st.session_state.get('music_playing', False)
    music_url = st.session_state.get('music_url', "")

    st.markdown(f"""
    <audio id="bgMusic" src="{music_url}" loop></audio>
    <script>
        var music = document.getElementById("bgMusic");
        var isPlaying_from_python = {str(is_playing).lower()};
        
        if (music) {{
            music.volume = 0.1; // Chỉnh âm lượng nhỏ (10%)
            if (isPlaying_from_python) {{
                music.play().catch(e => console.log("Lỗi: Người dùng cần tương tác để bật nhạc"));
            }} else {{
                music.pause();
            }}
        }}
    </script>
    """, unsafe_allow_html=True)

def pause_music_for_tts():
    """Tạo lệnh JS để tạm dừng nhạc nền. Dùng trước st.audio."""
    js_pause = "<script>var music = document.getElementById('bgMusic'); if (music) { music.pause(); }</script>"
    st.markdown(js_pause, unsafe_allow_html=True)
