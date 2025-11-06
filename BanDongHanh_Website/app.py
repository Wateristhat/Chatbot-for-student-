# Tên file: app.py
# (PHIÊN BẢN ĐÃ SỬA LỖI KÝ TỰ LẠ)

import streamlit as st
import database  # <--- TÔI ĐÃ SỬA DÒNG NÀY
import time

# --- CẤU HÌNH BAN ĐẦU ---
st.set_page_config(
    page_title="Trang chủ - Bạn Đồng Hành",
    page_icon="❤️",
    layout="wide"
)

# KHỞI TẠO DATABASE (chỉ chạy 1 lần)
database.init_db()

# ===================================================================
# HÀM ĐĂNG XUẤT (Phải được định nghĩa ở app.py)
# ===================================================================
def logout():
    """Xóa thông tin user khỏi phiên và tải lại trang"""
    if "user_id" in st.session_state:
        del st.session_state.user_id
    if "username" in st.session_state:
        del st.session_state.username
    st.rerun() # Tải lại, sẽ quay về trang đăng nhập

# ===================================================================
# TRANG ĐĂNG NHẬP (Hiển thị nếu chưa đăng nhập)
# ===================================================================
def show_login_page():
    """Hiển thị form đăng nhập"""
    
    # st.image("image_c067ff.png") # Bỏ tạm dòng này để test

    with st.form("login_form"):
        st.write("👋 **Chào bạn, mình là Bạn Đồng Hành ❤️**")
        st.write("Trước khi bắt đầu, chúng mình làm quen nhé?")
        
        username = st.text_input("Bạn tên là gì?")
        secret_color = st.text_input("Màu sắc yêu thích của bạn là gì?", type="password")
        
        submitted = st.form_submit_button("Lưu thông tin và bắt đầu!")

    if submitted:
        if not username or not secret_color:
            st.error("Bạn ơi, nhập cả tên và màu sắc yêu thích nhé!")
        else:
            with st.spinner("Đang kiểm tra..."):
                user_id = database.get_or_create_user(username, secret_color)
                
            if user_id:
                st.success(f"Chào mừng trở lại, {username.capitalize()}!")
                st.session_state.user_id = user_id
                st.session_state.username = username.capitalize()
                time.sleep(1) 
                st.rerun() 
            else:
                st.error("Có lỗi xảy ra. Vui lòng thử lại.")

# ===================================================================
# TRANG CHỦ (Hiển thị nếu ĐÃ đăng nhập)
# ===================================================================
def show_main_page():
    """Hiển thị nội dung Trang chủ"""
    
    st.sidebar.title(f"Xin chào, {st.session_state.username}! 👋")
    st.sidebar.button("Đăng xuất (Đổi tên)", on_click=logout)
    
    # --- Nội dung trang chủ của bạn ---
    st.title(f"❤️ Chào mừng bạn đến với Bạn Đồng Hành!")
    st.write("Hãy chọn một tính năng bên trái để khám phá nhé.")
    st.write("Đây là nội dung của Trang chủ.")


# ===================================================================
# HÀM LOGIC CHÍNH (CỔNG BẢO VỆ)
# =================================S==================================
def main():
    if 'user_id' not in st.session_state:
        show_login_page()
    else:
        show_main_page()

# --- CHẠY ỨNG DỤNG ---
if __name__ == "__main__":
    main()
