import streamlit as st
from views.gioi_thieu import GioiThieuPage
from views.tro_chuyen import TroChuyenPage
from views.nhat_ky import NhatKyPage
from views.thu_gian import ThuGianPage
# ... import các trang khác nếu bạn muốn thêm vào menu chính

st.set_page_config(
    page_title="Bạn Đồng Hành",
    page_icon="❤️",
    layout="wide"
)

# Điều hướng dựa trên lựa chọn của người dùng
menu = {
    "Giới Thiệu": GioiThieuPage(),
    "Trò Chuyện Cùng Bot": TroChuyenPage(),
    "Nhật Ký Cảm Xúc": NhatKyPage(),
    "Góc An Yên": ThuGianPage(),
}

st.sidebar.title("Menu Chính")
selection = st.sidebar.radio("Chọn một tính năng:", list(menu.keys()))

page = menu[selection]
page.render()
