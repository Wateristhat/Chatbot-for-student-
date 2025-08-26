# pages/Goc_nho.py
import streamlit as st

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Góc nhỏ", page_icon="❤️", layout="centered")

# --- KIỂM TRA ĐĂNG NHẬP ---
# Đảm bảo người dùng đã đăng nhập trước khi truy cập
if not st.session_state.get('user_id'):
    st.warning("Bạn ơi, hãy quay về Trang Chủ để đăng nhập hoặc tạo tài khoản mới nhé! ❤️")
    st.stop()

# --- GIAO DIỆỆN CHÍNH ---
st.title("❤️ Góc nhỏ của bạn")

# --- Liên kết quay về Trang chủ ---
st.page_link("Trang_chủ.py", label="⬅️ Quay về Trang chủ", icon="🏠")

st.markdown("Chăm sóc bản thân không phải là ích kỷ, đó là điều cần thiết. Hãy bắt đầu với những hành động nhỏ mỗi ngày nhé.")
st.write("---")

# Ngân hàng các hành động nhỏ để tự chăm sóc
MICRO_ACTIONS = [
    "Uống một ly nước đầy.",
    "Vươn vai và duỗi người trong 1 phút.",
    "Nhìn ra ngoài cửa sổ và tìm một đám mây đẹp.",
    "Nghe một bài hát bạn yêu thích.",
    "Viết ra 1 điều bạn tự hào về bản thân.",
    "Rửa mặt với nước mát.",
    "Sắp xếp lại góc học tập/làm việc.",
    "Mỉm cười với chính mình trong gương."
]

# --- PHẦN LÊN KẾ HOẠCH ---
st.header("Xây dựng kế hoạch cho hôm nay")
st.write("Chọn những việc nhỏ bạn muốn làm hôm nay để chăm sóc bản thân.")

# Khởi tạo state để lưu các lựa chọn
if 'selected_actions' not in st.session_state:
    st.session_state.selected_actions = []

# Cho phép người dùng chọn nhiều hành động
selected = st.multiselect(
    "Chọn từ ngân hàng gợi ý:",
    options=MICRO_ACTIONS,
    default=st.session_state.selected_actions,
    placeholder="Nhấn vào đây để chọn..."
)
st.session_state.selected_actions = selected

st.write("---")

# --- PHẦN HIỂN THỊ CHECKLIST ---
if not st.session_state.selected_actions:
    st.info("Hãy chọn ít nhất một hành động để bắt đầu kế hoạch của bạn nhé!")
else:
    st.subheader("Danh sách việc cần làm của bạn hôm nay:")
    all_done = True
    
    # Lặp qua các hành động đã chọn để tạo checklist
    for action in st.session_state.selected_actions:
        # Khởi tạo trạng thái hoàn thành cho mỗi hành động (nếu chưa có)
        if f"action_{action}" not in st.session_state:
            st.session_state[f"action_{action}"] = False
        
        # Tạo checkbox cho mỗi hành động
        is_done = st.checkbox(action, key=f"cb_{action}", value=st.session_state[f"action_{action}"])
        
        # Hiển thị thông báo khi người dùng vừa tick vào checkbox
        if is_done and not st.session_state[f"action_{action}"]:
            st.toast(f"Tuyệt vời! Bạn đã hoàn thành: {action}", icon="🎉")
        
        # Cập nhật lại trạng thái và kiểm tra xem tất cả đã hoàn thành chưa
        st.session_state[f"action_{action}"] = is_done
        if not is_done:
            all_done = False

    # Hiển thị thông báo chúc mừng khi hoàn thành tất cả
    if all_done:
        st.success("🎉 Chúc mừng! Bạn đã hoàn thành tất cả các mục tiêu tự chăm sóc cho hôm nay. Bạn thật tuyệt vời!")
        st.balloons()
