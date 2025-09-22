# Trong file app.py
import streamlit as st
import database as db

# Initialize database tables
db.create_tables()
db.ensure_goc_nho_tables()

# Check for incomplete plans and create reminders (run daily)
try:
    db.check_incomplete_plans()
except Exception as e:
    # Silent fail - don't break the app if reminder system has issues
    pass

st.switch_page("pages/0_💖_Trang_chủ.py")
