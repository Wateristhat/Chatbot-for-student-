import sqlite3

# Tên file cơ sở dữ liệu
DATABASE_NAME = "app_data.db"

def connect_db():
    """Tạo và trả về đối tượng kết nối CSDL."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    """Tạo bảng chat_history nếu chưa tồn tại.
    Bỏ hoàn toàn bảng users và các bảng liên quan đến người dùng."""
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
    
    conn.commit()
    conn.close()

def add_chat_message(sender, text):
    """Thêm một tin nhắn mới vào lịch sử trò chuyện.
    Không có user_id nữa."""
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

# --- KHỞI TẠO BAN ĐẦU ---
create_tables()
