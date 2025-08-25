# file: database.py
import sqlite3
from datetime import datetime

DATABASE_FILE = "ban_dong_hanh_data.db"

def init_db():
    """Khởi tạo cơ sở dữ liệu và tất cả các bảng cần thiết."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    
    # Bảng 1: Lưu thông tin người dùng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        birth_year INTEGER,
        school TEXT,
        issues TEXT,
        created_at TEXT NOT NULL
    )
    """)
    
    # Bảng 2: Lưu các ghi chú biết ơn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        note TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # Bảng 3: Lưu lịch sử trò chuyện với bot
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        sender TEXT NOT NULL, -- 'user' or 'bot'
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

# --- Các hàm liên quan đến Người dùng ---
def get_all_users():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM users ORDER BY name")
    users = cursor.fetchall()
    conn.close()
    return users

def add_user(name, birth_year, school, issues):
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO users (name, birth_year, school, issues, created_at) VALUES (?, ?, ?, ?, ?)",
            (name, birth_year, school, issues, created_at)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        return None # Tên đã tồn tại

# --- Các hàm liên quan đến Lọ Biết Ơn ---
def add_gratitude_note(user_id, note):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO gratitude_notes (user_id, note, created_at) VALUES (?, ?, ?)",
        (user_id, note, created_at)
    )
    conn.commit()
    conn.close()

def get_gratitude_notes(user_id):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT note FROM gratitude_notes WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    notes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return notes

# --- Các hàm liên quan đến Chatbot ---
def add_chat_message(user_id, sender, message):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO chat_history (user_id, sender, message, created_at) VALUES (?, ?, ?, ?)",
        (user_id, sender, message, created_at)
    )
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=20):
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sender, message FROM chat_history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit)
    )
    # Sắp xếp lại theo thứ tự cũ -> mới
    history = [{"sender": row[0], "text": row[1]} for row in reversed(cursor.fetchall())]
    conn.close()
    return history
