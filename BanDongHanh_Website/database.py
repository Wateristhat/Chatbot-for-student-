# Tên file: database.py
# PHIÊN BẢN ĐÃ NÂNG CẤP ĐỂ CÁ NHÂN HÓA
import sqlite3
import streamlit as st
from datetime import datetime

# Tên file database
DB_NAME = "bandonghanh.db" 

# Dùng @st.singleton để đảm bảo chỉ có 1 kết nối được tạo
@st.singleton
def get_db_connection():
    """Tạo và trả về một kết nối đến database SQLite."""
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Khởi tạo các bảng trong database nếu chúng chưa tồn tại.
    TẤT CẢ CÁC BẢNG (trừ users) ĐỀU CÓ user_id.
    """
    conn = get_db_connection()
    c = conn.cursor()
    
    # --- Bảng 1: USERS (QUAN TRỌNG NHẤT) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        secret_color TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(username, secret_color)
    )
    """)
    
    # --- Bảng 2: CHAT_HISTORY (TRÒ CHUYỆN) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        sender TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    # --- Bảng 3: GRATITUDE_JAR (LỌ BIẾT ƠN) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS gratitude_jar (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    # --- Bảng 4: EMOTION_ARTWORKS (BÓNG MÀU CẢM XÚC) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS emotion_artworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        emotion_emoji TEXT NOT NULL,
        canvas_data TEXT NOT NULL,
        title TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        date_only DATE DEFAULT (DATE('now')),
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)

    # --- Bảng 5: MOOD_JOURNAL (GÓC AN YÊN - THAY THẾ CHO FILE .CSV) ---
    c.execute("""
    CREATE TABLE IF NOT EXISTS mood_journal (
        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        exercise_type TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    """)
    
    conn.commit()
    print("Database (Personalized) initialized successfully.")

# ===================================================================
# HÀM QUẢN LÝ NGƯỜI DÙNG (USER)
# ===================================================================

def get_or_create_user(username, secret_color):
    """Hàm Đăng nhập / Đăng ký"""
    conn = get_db_connection()
    c = conn.cursor()
    
    norm_username = username.lower().strip()
    norm_color = secret_color.lower().strip()
    
    if not norm_username or not norm_color:
        return None 

    try:
        c.execute(
            "SELECT user_id FROM users WHERE username = ? AND secret_color = ?",
            (norm_username, norm_color)
        )
        user = c.fetchone()
        
        if user:
            return user["user_id"] # Trả về ID nếu đã tồn tại
        else:
            c.execute(
                "INSERT INTO users (username, secret_color) VALUES (?, ?)",
                (norm_username, norm_color)
            )
            conn.commit()
            return c.lastrowid # Trả về ID của user MỚI
            
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

# ===================================================================
# HÀM TÍNH NĂNG "LỌ BIẾT ƠN" (ĐÃ CÁ NHÂN HÓA)
# ===================================================================

def add_gratitude_note(user_id, content):
    """Thêm ghi chú biết ơn cho 1 user cụ thể."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO gratitude_jar (user_id, content) VALUES (?, ?)", 
        (user_id, content)
    )
    conn.commit()

def get_gratitude_notes(user_id):
    """Lấy ghi chú biết ơn CỦA CHỈ 1 user."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "SELECT entry_id, content, timestamp FROM gratitude_jar WHERE user_id = ? ORDER BY timestamp ASC",
        (user_id,)
    )
    return [dict(row) for row in c.fetchall()]

def delete_gratitude_note(note_id, user_id):
    """Xóa ghi chú (và kiểm tra xem nó có đúng là của user đó không)."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "DELETE FROM gratitude_jar WHERE entry_id = ? AND user_id = ?", 
        (note_id, user_id)
    )
    conn.commit()

# ===================================================================
# HÀM TÍNH NĂNG "BÓNG MÀU CẢM XÚC" (ĐÃ CÁ NHÂN HÓA)
# ===================================================================

def add_artwork(user_id, emotion_emoji, canvas_data, title=None):
    """Thêm tác phẩm cho 1 user."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO emotion_artworks (user_id, emotion_emoji, canvas_data, title) VALUES (?, ?, ?, ?)",
        (user_id, emotion_emoji, canvas_data, title)
    )
    conn.commit()

def get_artworks_by_date(user_id):
    """Lấy tác phẩm CỦA CHỈ 1 user, nhóm theo ngày."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        """SELECT date_only, emotion_emoji, title, id, timestamp 
           FROM emotion_artworks 
           WHERE user_id = ? 
           ORDER BY date_only DESC, timestamp DESC""",
        (user_id,)
    )
    
    artworks = c.fetchall()
    grouped = {}
    for artwork in artworks:
        date_only = artwork["date_only"]
        if date_only not in grouped:
            grouped[date_only] = []
        grouped[date_only].append(dict(artwork))
    return grouped

# (Thêm các hàm get_artwork_data, get_artworks_by_emotion... tương tự,
#  luôn thêm `user_id` và mệnh đề `WHERE user_id = ?`)

# ===================================================================
# HÀM TÍNH NĂNG "GÓC AN YÊN" (ĐÃ CÁ NHÂN HÓA)
# ===================================================================

def add_mood_entry(user_id, exercise_type, content):
    """Thêm một mục nhật ký cảm xúc CỦA 1 user."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO mood_journal (user_id, exercise_type, content) VALUES (?, ?, ?)",
        (user_id, exercise_type, content)
    )
    conn.commit()

def get_mood_entries(user_id, exercise_filter=None):
    """Lấy các mục nhật ký CỦA CHỈ 1 user."""
    conn = get_db_connection()
    c = conn.cursor()
    
    query = "SELECT timestamp, exercise_type, content FROM mood_journal WHERE user_id = ?"
    params = [user_id]
    
    if exercise_filter:
        query += " AND exercise_type = ?"
        params.append(exercise_filter)
        
    query += " ORDER BY timestamp DESC"
    
    c.execute(query, tuple(params))
    return [dict(row) for row in c.fetchall()]

# (Lặp lại logic này cho TRÒ CHUYỆN và các tính năng khác)
