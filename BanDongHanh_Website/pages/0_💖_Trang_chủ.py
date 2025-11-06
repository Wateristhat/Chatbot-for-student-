# THAY THẾ KHỐI ELSE: (Bắt đầu khoảng dòng 150)
else:
    # --- Giao diện đã đăng nhập ---
    # ... (Giữ nguyên phần hiển thị "Chào mừng...")
    
    # THAY THẾ TOÀN BỘ KHỐI MENU VÀ CSS BẰNG:
    st.markdown("---")
    st.info("🌟 Menu đã được chuyển sang thanh bên trái (Sidebar). Vui lòng sử dụng các liên kết ở đó để điều hướng mà không bị mất đăng nhập.")
    
    # Thêm nút Đăng xuất (chỉ để dự phòng)
    if st.button("❌ Đăng xuất", key="logout_btn_main"):
        st.session_state.user_name = None
        st.session_state.user_id = None
        st.rerun()
