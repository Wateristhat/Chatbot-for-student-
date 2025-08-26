# database.py
import sqlite3
import bcrypt

def connect_db():
    """Kết nối tới cơ sở dữ liệu SQLite."""
    return sqlite3.connect("ban_dong_hanh.db")

def create_tables():
    """Tạo các bảng cần thiết nếu chúng chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bảng người dùng với mật khẩu
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    # Bảng Lọ Biết Ơn
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # Bảng lịch sử chat
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

# --- CÁC HÀM XỬ LÝ MẬT KHẨU AN TOÀN ---
def hash_password(password):
    """Mã hóa mật khẩu."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    """Kiểm tra mật khẩu đã mã hóa."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# --- CÁC HÀM QUẢN LÝ NGƯỜI DÙNG ---
def add_user(username, password):
    """Thêm người dùng mới vào database."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError: # Lỗi nếu tên người dùng đã tồn tại
        return False
    finally:
        conn.close()

def check_user(username, password):
    """Kiểm tra thông tin đăng nhập."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password(password, user[2]):
        return user[0], user[1] # Trả về id và username
    return None

# --- CÁC HÀM CHO LỌ BIẾT ƠN ---
def get_gratitude_notes(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content FROM gratitude_notes WHERE user_id = ?", (user_id,))
    notes = cursor.fetchall()
    conn.close()
    return notes

def add_gratitude_note(user_id, content):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO gratitude_notes (user_id, content) VALUES (?, ?)", (user_id, content))
    conn.commit()
    conn.close()

def delete_gratitude_note(note_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM gratitude_notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()

# --- CÁC HÀM CHO LỊCH SỬ CHAT ---
def get_chat_history(user_id, limit=50):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT sender, text FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    history = [{"sender": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    return list(reversed(history))

def add_chat_message(user_id, sender, text):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, sender, text) VALUES (?, ?, ?)", (user_id, sender, text))
    conn.commit()
    conn.close()
