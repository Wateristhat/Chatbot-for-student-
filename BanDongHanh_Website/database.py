import sqlite3
import bcrypt

DATABASE_NAME = "app_data.db"

def connect_db():
    """Tạo và trả về đối tượng kết nối CSDL."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables():
    """Tạo các bảng cần thiết nếu chúng chưa tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bảng người dùng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)
    
    # Bảng lịch sử trò chuyện
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Mã hóa mật khẩu bằng bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(password, hashed_password):
    """Kiểm tra mật khẩu đã nhập với mật khẩu đã mã hóa."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def add_user(username, password):
    """Thêm người dùng mới vào CSDL, xử lý trường hợp tên người dùng đã tồn tại."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        hashed_password = hash_password(password)
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True # Thêm thành công
    except sqlite3.IntegrityError:
        return False # Tên người dùng đã tồn tại
    finally:
        conn.close()

def check_user(username, password):
    """Kiểm tra thông tin đăng nhập và trả về thông tin người dùng."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password(password, user[2]):
        return (user[0], user[1]) # Trả về user_id và username
    return None

def add_chat_message(user_id, sender, text):
    """Thêm một tin nhắn mới vào lịch sử trò chuyện."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (user_id, sender, text) VALUES (?, ?, ?)", (user_id, sender, text))
    conn.commit()
    conn.close()

def get_chat_history(user_id, limit=None):
    """Lấy lịch sử trò chuyện của một người dùng, có thể giới hạn số lượng tin nhắn."""
    conn = connect_db()
    cursor = conn.cursor()
    
    if limit:
        cursor.execute("SELECT sender, text FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, limit))
    else:
        cursor.execute("SELECT sender, text FROM chat_history WHERE user_id = ? ORDER BY timestamp ASC", (user_id,))
        
    history = [{"sender": row[0], "text": row[1]} for row in cursor.fetchall()]
    conn.close()
    
    return history[::-1] if limit else history # Đảo ngược nếu có limit để hiển thị mới nhất trước

# --- KHỞI TẠO BAN ĐẦU ---
create_tables()

if __name__ == '__main__':
    # Đoạn code này chỉ chạy khi file được chạy trực tiếp,
    # giúp kiểm tra các hàm CSDL một cách độc lập.
    print("Initializing database...")
    create_tables()
    print("Database initialization complete.")
