import sqlite3

DATABASE_NAME = "app_data.db"

def connect_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    """Tạo bảng chat_history và gratitude_notes nếu chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bảng lịch sử trò chuyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # Bảng ghi chú biết ơn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def add_chat_message(sender, text):
    """Thêm một tin nhắn mới vào lịch sử trò chuyện."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (sender, text) VALUES (?, ?)", (sender, text))
    conn.commit()
    conn.close()

def get_chat_history(limit=None):
    """Lấy toàn bộ lịch sử trò chuyện, không phân biệt người dùng."""
    conn = connect_db()
    cursor = conn.cursor()
    if limit:
        cursor.execute("SELECT sender, text FROM chat_history ORDER BY timestamp DESC LIMIT ?", (limit,))
    else:
        cursor.execute("SELECT sender, text FROM chat_history ORDER BY timestamp ASC")
    history = [{"sender": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return history[::-1] if limit else history

# ====== BỔ SUNG CHO LỌ BIẾT ƠN ======
def add_gratitude_note(content):
    """Thêm một ghi chú biết ơn mới (không cần user_id)."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gratitude_notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()

def get_gratitude_notes():
    """Lấy toàn bộ ghi chú biết ơn."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM gratitude_notes ORDER BY timestamp ASC")
    notes = cursor.fetchall()
    conn.close()
    return notes

def delete_gratitude_note(note_id):
    """Xóa ghi chú biết ơn theo id."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gratitude_notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

# --- KHỞI TẠO BAN ĐẦU ---
create_tables()
