# Trong file app.py
import streamlit as st
import database as db

db.create_tables() # <-- Đặt ở đây

st.switch_page("pages/0_💖_Trang_chủ.py")
