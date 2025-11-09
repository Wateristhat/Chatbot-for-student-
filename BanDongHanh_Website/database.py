# Sửa file: database.py
import sqlite3
import csv
import os
from datetime import datetime
from zoneinfo import ZoneInfo 
import bcrypt

DATABASE_NAME = "app_data.db"
VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh") 

def connect_db():
    """Kết nối CSDL, bật chế độ check_same_thread=False cho Streamlit."""
    conn = sqlite3.connect(DATABASE_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row 
    return conn

# ====== 1. CÁC HÀM TẠO BẢNG CHÍNH ======

def create_tables():
    """Tạo TẤT CẢ các bảng và THÊM CỘT user_id nếu chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # === Thêm cột user_id (Chạy 1 lần) ===
    try:
        cursor.execute("ALTER TABLE chat_history ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
    except sqlite3.OperationalError: pass
    
    try:
        cursor.execute("ALTER TABLE gratitude_notes ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
    except sqlite3.OperationalError: pass
    
    try:
        cursor.execute("ALTER TABLE emotion_artworks ADD COLUMN user_id TEXT NOT NULL DEFAULT 'global'")
    except sqlite3.OperationalError: pass

    # === Tạo bảng (Đã xóa DEFAULT time) ===
    # Bảng Users
    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash BLOB NOT NULL,
        created_at DATETIME
    )
    """
    )
    
    # Bảng Trò chuyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL, 
        sender TEXT NOT NULL,
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
    
    conn.commit()
    conn.close()

def create_activity_tables():
    """Tạo bảng cho Góc Nhỏ (activities)"""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bảng lưu các hoạt động tự chăm sóc của người dùng
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

# ====== 2. CÁC HÀM TRÒ CHUYỆN ======

def add_chat_message(user_id, sender, text):
    """Thêm tin nhắn mới vào CSDL cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ)
    try:
        cursor.execute(
            "INSERT INTO chat_history (user_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
            (user_id, sender, text, vn_time)
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

# ====== 3. CÁC HÀM LỌ BIẾT ƠN ======

def add_gratitude_note(user_id, content):
    """Thêm ghi chú biết ơn cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ) 
    cursor.execute("INSERT INTO gratitude_notes (user_id, content, timestamp) VALUES (?, ?, ?)", 
                   (user_id, content, vn_time)) 
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

# ====== 4. CÁC HÀM BẢNG MÀU CẢM XÚC ======

def add_artwork(user_id, emotion_emoji, canvas_data, title=None):
    """Thêm tác phẩm mới cho user_id cụ thể."""
    conn = connect_db()
    cursor = conn.cursor()
    vn_time = datetime.now(VN_TZ) 
    vn_date = vn_time.date()      
    cursor.execute(
        "INSERT INTO emotion_artworks (user_id, emotion_emoji, canvas_data, title, timestamp, date_only) VALUES (?, ?, ?, ?, ?, ?)", 
        (user_id, emotion_emoji, canvas_data, title, vn_time, vn_date)
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

# ====== 5. CÁC HÀM GÓC AN YÊN (CSV) ======

def add_mood_entry(user_id, exercise_type, content):
    """Thêm mục vào file CSV CÁ NHÂN của user_id."""
    user_journal_file = f"{user_id}_goc_an_yen_journal.csv"
    
    now = datetime.now(VN_TZ) 
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

# ====== 6. CÁC HÀM GÓC NHỎ (ACTIVITIES) ======

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

# --- KHỞI TẠO TẤT CẢ CÁC BẢNG (CHỈ CHẠY 1 LẦN) ---
create_tables()
create_activity_tables()
print("CSDL đã khởi tạo hoàn tất.")

# ====== 7. HÀM NGƯỜI DÙNG (AUTH) ======

def create_user(username: str, password: str) -> bool:
    """Tạo người dùng mới với mật khẩu băm bằng bcrypt. Trả về True nếu thành công."""
    if not username or not password:
        return False
    username = username.strip()
    if len(username) < 3 or len(password) < 6:
        return False
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    conn = connect_db()
    cursor = conn.cursor()
    try:
        vn_time = datetime.now(VN_TZ)
        cursor.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, pw_hash, vn_time),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # username đã tồn tại
        return False
    finally:
        conn.close()

def get_user_by_username(username: str):
    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, username, password_hash FROM users WHERE username = ?", (username.strip(),))
        row = cursor.fetchone()
        return row
    finally:
        conn.close()

def verify_user(username: str, password: str) -> bool:
    """Kiểm tra username/password. Trả True nếu hợp lệ."""
    row = get_user_by_username(username)
    if not row:
        return False
    pw_hash = row["password_hash"]
    try:
        return bcrypt.checkpw(password.encode("utf-8"), pw_hash)
    except Exception:
        return False
