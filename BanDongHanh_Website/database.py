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
    
    # Bảng người dùng chỉ có username và password
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)
    
    # Các bảng khác giữ nguyên
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        content TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

# --- CÁC HÀM XỬ LÝ MẬT KHẨU ---
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed)

# --- CÁC HÀM QUẢN LÝ NGƯỜI DÙNG ---
def add_user(username, password):
    """Thêm người dùng chỉ với username và password."""
    conn = connect_db()
    cursor = conn.cursor()
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
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

# --- CÁC HÀM KHÁC (Giữ nguyên) ---
# (Toàn bộ các hàm cho Lọ Biết Ơn và Lịch sử Chat được giữ nguyên)
