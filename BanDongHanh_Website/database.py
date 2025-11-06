# Sửa file: database.py
import sqlite3
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo # ### <<< SỬA ĐỔI 1: Thêm thư viện Múi giờ

DATABASE_NAME = "app_data.db"
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh") # ### <<< SỬA ĐỔI 2: Định nghĩa Múi giờ VN (UTC+7)

def connect_db():
    """Kết nối CSDL, bật chế độ check_same_thread=False cho Streamlit."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # Giúp trả về kết quả dạng dictionary
    return conn

def create_tables():
    """Tạo TẤT CẢ các bảng và THÊM CỘT user_id nếu chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # === Thêm cột user_id (Chạy 1 lần) ===
    try:
        cursor.execute("ALTER TABLE chat_history ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
        print("Đã thêm cột user_id vào chat_history.")
    except sqlite3.OperationalError: pass # Bỏ qua
    
    try:
        cursor.execute("ALTER TABLE gratitude_notes ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
        print("Đã thêm cột user_id vào gratitude_notes.")
    except sqlite3.OperationalError: pass # Bỏ qua
    
    try:
        cursor.execute("ALTER TABLE emotion_artworks ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
        print("Đã thêm cột user_id vào emotion_artworks.")
    except sqlite3.OperationalError: pass # Bỏ qua

    # === Tạo bảng (Đã xóa DEFAULT time) ===
    
    # Bảng Trò chuyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL, 
        sender TEXT NOT NULL, -- 'user' hoặc 'assistant'
        text TEXT NOT NULL,
        timestamp DATETIME
    )
    """)
    
    # Bảng Lọ Biết Ơn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp DATETIME
    )
    """)
    
    # Bảng Bảng Màu Cảm Xúc
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotion_artworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        emotion_emoji TEXT NOT NULL,
        canvas_data TEXT NOT NULL,
        title TEXT,
        timestamp DATETIME,
        date_only DATE
    )
    """)
    
    # Bảng Góc Nhỏ
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        content TEXT NOT NULL,
        is_done BOOLEAN DEFAULT 0,
        added_date DATE
    )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_activity_user_date ON activities (user_id, added_date)")
    
    conn.commit()
    conn.close()

# ====== TRÒ CHUYỆN ======

def add_chat_message(user_id, sender, text):
    """Thêm tin nhắn mới vào CSDL cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ) # ### <<< SỬA ĐỔI 3: Lấy giờ VN
    try:
        cursor.execute(
            "INSERT INTO chat_history (user_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, sender, text, vn_time) # ### <<< SỬA ĐỔI: Thêm vn_time
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm chat message: {e}")
    finally:
        conn.close()

def get_chat_history(user_id):
    """Lấy lịch sử chat của CHỈ user_id này (Format cho Gemini)."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT sender, text FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC",
            (user_id,)
        )
        history = []
        for row in cursor.fetchall():
            history.append({
                "role": "model" if row["sender"] == "assistant" else "user",
                "parts": [row["text"]]
            })
        return history
    except sqlite3.Error as e:
        print(f"Lỗi khi lấy chat history: {e}")
        return []
    finally:
        conn.close()

def clear_chat_history(user_id):
    """Xóa lịch sử chat của CHỈ user_id này."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM chat_history WHERE user_id = ?", (user_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi xóa chat history: {e}")
    finally:
        conn.close()

# ====== LỌ BIẾT ƠN ======

def add_gratitude_note(user_id, content):
    """Thêm ghi chú biết ơn cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ) # ### <<< SỬA ĐỔI: Lấy giờ VN
    cursor.execute("INSERT INTO gratitude_notes (user_id, content, timestamp) VALUES (?, ?, ?)", 
                   (user_id, content, vn_time)) # ### <<< SỬA ĐỔI: Thêm vn_time
    conn.commit()
    conn.close()

def get_gratitude_notes(user_id):
    """Lấy toàn bộ ghi chú của CHỈ user_id này."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, timestamp FROM gratitude_notes WHERE user_id = ? ORDER BY timestamp ASC", 
                   (user_id,))
    notes = cursor.fetchall() 
    conn.close()
    return notes

def delete_gratitude_note(user_id, note_id):
    """Xóa ghi chú của CHỈ user_id này."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gratitude_notes WHERE id = ? AND user_id = ?", 
                   (note_id, user_id))
    conn.commit()
    conn.close()

# ====== BẢNG MÀU CẢM XÚC ======

def add_artwork(user_id, emotion_emoji, canvas_data, title=None):
    """Thêm tác phẩm mới cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ) # ### <<< SỬA ĐỔI: Lấy giờ VN
    vn_date = vn_time.date()      # ### <<< SỬA ĐỔI: Lấy ngày VN
    cursor.execute(
        "INSERT INTO emotion_artworks (user_id, emotion_emoji, canvas_data, title, timestamp, date_only) VALUES (?, ?, ?, ?, ?, ?)", 
        (user_id, emotion_emoji, canvas_data, title, vn_time, vn_date) # ### <<< SỬA ĐỔI: Thêm vn_time, vn_date
    )
    conn.commit()
    conn.close()

def get_artworks_by_emotion(user_id, emotion_emoji=None):
    """Lấy tác phẩm của CHỈ user_id này."""
    conn = connect_db()
    cursor = conn.cursor()
    if emotion_emoji:
        cursor.execute(
            "SELECT * FROM emotion_artworks WHERE user_id = ? AND emotion_emoji = ? ORDER BY timestamp DESC", 
            (user_id, emotion_emoji)
        )
    else:
        cursor.execute(
            "SELECT * FROM emotion_artworks WHERE user_id = ? ORDER BY timestamp DESC",
            (user_id,)
        )
    artworks = cursor.fetchall()
    conn.close()
    return artworks

def get_artwork_data(user_id, artwork_id):
    """Lấy dữ liệu canvas của CHỈ user_id này."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT canvas_data FROM emotion_artworks WHERE id = ? AND user_id = ?", 
                   (artwork_id, user_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_artworks_by_date(user_id):
    """Lấy tác phẩm của CHỈ user_id này, nhóm theo ngày."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT date_only, emotion_emoji, title, id, timestamp 
           FROM emotion_artworks 
           WHERE user_id = ?
           ORDER BY date_only DESC, timestamp DESC""",
        (user_id,)
    )
    artworks = cursor.fetchall()
    conn.close()
    
    grouped = {}
    for artwork in artworks:
        date_only = artwork["date_only"]
        if date_only not in grouped:
            grouped[date_only] = []
        grouped[date_only].append({
            'id': artwork["id"],
            'emotion_emoji': artwork["emotion_emoji"],
            'title': artwork["title"],
            'timestamp': artwork["timestamp"]
        })
    return grouped

# ====== GÓC AN YÊN (CSV) ======

def add_mood_entry(user_id, exercise_type, content):
    """Thêm mục vào file CSV CÁ NHÂN của user_id."""
    user_journal_file = f"{user_id}_goc_an_yen_journal.csv"
    
    now = datetime.now(VN_TZ) # ### <<< SỬA ĐỔI: Lấy giờ VN
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    file_exists = os.path.exists(user_journal_file)
    is_empty = not file_exists or os.path.getsize(user_journal_file) == 0

    with open(user_journal_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if is_empty:
            writer.writerow(["Ngày giờ", "Loại bài tập", "Nội dung cảm nhận"])
        writer.writerow([timestamp, exercise_type, content])

def get_mood_entries(user_id, exercise_filter=None):
    """Lấy các mục từ file CSV CÁ NHÂN của user_id."""
    user_journal_file = f"{user_id}_goc_an_yen_journal.csv"
    entries = []
    
    if not os.path.exists(user_journal_file):
        return entries
    
    try:
        with open(user_journal_file, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                exercise_type = row.get("Loại bài tập", "")
                
                if exercise_filter is None or exercise_type.strip() == exercise_filter:
                    entries.append({
                        "timestamp": row.get("Ngày giờ", ""),
                        "exercise_type": exercise_type,
                        "content": row.get("Nội dung cảm nhận", "")
                    })
    except Exception as e:
        print(f"Lỗi đọc file nhật ký {user_journal_file}: {e}")
    
    return entries

# ====== GÓC NHỎ (ACTIVITIES) ======

def add_activity(user_id, content, added_date):
    """Thêm một hoạt động mới cho user_id vào ngày cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT 1 FROM activities WHERE user_id = ? AND content = ? AND added_date = ?",
            (user_id, content, added_date)
        )
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO activities (user_id, content, added_date, is_done) VALUES (?, ?, ?, 0)",
                (user_id, content, added_date)
            )
            conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi thêm activity: {e}")
    finally:
        conn.close()

def get_activities_by_date(user_id, added_date):
    """Lấy tất cả hoạt động của user_id trong ngày."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "SELECT id, content, is_done FROM activities WHERE user_id = ? AND added_date = ? ORDER BY id ASC",
            (user_id, added_date)
        )
        return cursor.fetchall() 
    except sqlite3.Error as e:
        print(f"Lỗi khi lấy activities: {e}")
        return []
    finally:
        conn.close()

def update_activity_status(user_id, activity_id, is_done):
    """Cập nhật trạng thái của một hoạt động."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE activities SET is_done = ? WHERE id = ? AND user_id = ?",
            (is_done, activity_id, user_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi cập nhật activity: {e}")
    finally:
        conn.close()

def delete_activity(user_id, activity_id):
    """Xóa một hoạt động."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM activities WHERE id = ? AND user_id = ?",
            (activity_id, user_id)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Lỗi khi xóa activity: {e}")
    finally:
        conn.close()

# --- KHỞI TẠO BAN ĐẦU ---
# (Chạy 1 lần khi ứng dụng khởi động)
create_tables()
print("Đã khởi tạo CSDL và kiểm tra các bảng (chat, gratitude, artwork).")
# --- Thêm vào phần KHỞI TẠO BAN ĐẦU ---
create_chat_history_table()
print("Đã khởi tạo bảng chat_history.")
# --- KẾT THÚC PHẦN DÁN THÊM ---
