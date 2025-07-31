import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Nhật ký Cảm xúc", layout="wide")
st.title("📔 Nhật Ký Cảm Xúc")

MOOD_FILE = "mood_journal.csv"
MOOD_OPTIONS = ["😄 Vui", "😔 Buồn", "😡 Tức giận", "😢 Tủi thân", "😴 Mệt mỏi", "😐 Bình thường"]

# Hàm để tải dữ liệu từ file CSV
def load_mood_data():
    if os.path.exists(MOOD_FILE):
        try:
            return pd.read_csv(MOOD_FILE)
        except pd.errors.EmptyDataError: # Xử lý trường hợp file trống
            return pd.DataFrame(columns=["Ngày", "Cảm xúc", "Ghi chú"])
    else:
        # Nếu file không tồn tại, tạo DataFrame rỗng
        return pd.DataFrame(columns=["Ngày", "Cảm xúc", "Ghi chú"])

# Tải dữ liệu
journal_df = load_mood_data()

# --- Phần nhập liệu ---
st.header("Hôm nay bạn cảm thấy thế nào?")
log_date = st.date_input("Chọn ngày", datetime.now())
selected_mood = st.selectbox("Chọn cảm xúc của bạn", MOOD_OPTIONS)
note = st.text_input("Bạn có muốn ghi chú thêm điều gì không?")

if st.button("Lưu lại cảm xúc"):
    new_entry = pd.DataFrame([{
        "Ngày": log_date.strftime("%Y-%m-%d"),
        "Cảm xúc": selected_mood,
        "Ghi chú": note
    }])
    
    if not journal_df.empty:
        journal_df['Ngày'] = journal_df['Ngày'].astype(str)
    
    # Kiểm tra xem ngày này đã có mục nhập chưa
    if log_date.strftime("%Y-%m-%d") in journal_df["Ngày"].values:
        st.warning(f"Bạn đã ghi lại cảm xúc cho ngày {log_date.strftime('%d-%m-%Y')} rồi.")
    else:
        journal_df = pd.concat([journal_df, new_entry], ignore_index=True)
        journal_df.to_csv(MOOD_FILE, index=False)
        st.success(f"Đã lưu lại cảm xúc '{selected_mood}' cho ngày {log_date.strftime('%d-%m-%Y')}!")
        st.rerun()

# --- Phần hiển thị ---
st.header("Lịch sử cảm xúc của bạn")
if not journal_df.empty:
    journal_df_display = journal_df.sort_values(by="Ngày", ascending=False)
    st.dataframe(journal_df_display, use_container_width=True)

    # --- Phần biểu đồ ---
    st.header("Thống kê cảm xúc")
    mood_counts = journal_df["Cảm xúc"].value_counts()
    st.bar_chart(mood_counts)
else:
    st.info("Nhật ký của bạn còn trống. Hãy ghi lại cảm xúc đầu tiên nhé!")
