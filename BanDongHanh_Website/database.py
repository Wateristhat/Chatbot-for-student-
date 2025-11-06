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
    
    # Bảng lưu trữ tranh vẽ cảm xúc
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emotion_artworks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emotion_emoji TEXT NOT NULL,
        canvas_data TEXT NOT NULL,
        title TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        date_only DATE DEFAULT (DATE('now'))
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
    """Lấy toàn bộ ghi chú biết ơn kèm thời gian."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, content, timestamp FROM gratitude_notes ORDER BY timestamp ASC")
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

# ====== BỔ SUNG CHO BẢNG MÀU CẢM XÚC ======
def add_artwork(emotion_emoji, canvas_data, title=None):
    """Thêm một tác phẩm nghệ thuật mới với cảm xúc."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO emotion_artworks (emotion_emoji, canvas_data, title) VALUES (?, ?, ?)", 
        (emotion_emoji, canvas_data, title)
    )
    conn.commit()
    conn.close()

def get_artworks_by_emotion(emotion_emoji=None):
    """Lấy tác phẩm theo cảm xúc, hoặc tất cả nếu không chỉ định."""
    conn = connect_db()
    cursor = conn.cursor()
    
    if emotion_emoji:
        cursor.execute(
            "SELECT id, emotion_emoji, title, timestamp, date_only FROM emotion_artworks WHERE emotion_emoji = ? ORDER BY timestamp DESC", 
            (emotion_emoji,)
        )
    else:
        cursor.execute(
            "SELECT id, emotion_emoji, title, timestamp, date_only FROM emotion_artworks ORDER BY timestamp DESC"
        )
    
    artworks = cursor.fetchall()
    conn.close()
    return artworks

def get_artwork_data(artwork_id):
    """Lấy dữ liệu canvas của một tác phẩm."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT canvas_data FROM emotion_artworks WHERE id = ?", (artwork_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def get_artworks_by_date():
    """Lấy tác phẩm được nhóm theo ngày."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT date_only, emotion_emoji, title, id, timestamp 
           FROM emotion_artworks 
           ORDER BY date_only DESC, timestamp DESC"""
    )
    
    artworks = cursor.fetchall()
    conn.close()
    
    # Nhóm theo ngày
    grouped = {}
    for artwork in artworks:
        date_only = artwork[0]
        if date_only not in grouped:
            grouped[date_only] = []
        grouped[date_only].append({
            'id': artwork[3],
            'emotion_emoji': artwork[1],
            'title': artwork[2],
            'timestamp': artwork[4]
        })
    
    return grouped

# ====== BỔ SUNG CHO NHẬT KÝ CẢM XÚC (MOOD JOURNAL) ======
import csv
from datetime import datetime
import os

MOOD_JOURNAL_FILE = "goc_an_yen_journal.csv"

def add_mood_entry(exercise_type, content):
    """Thêm một mục vào nhật ký cảm xúc của Góc An Yên."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Check if file exists
    file_exists = os.path.exists(MOOD_JOURNAL_FILE)
    
    with open(MOOD_JOURNAL_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write headers if file is new or empty
        if not file_exists or os.path.getsize(MOOD_JOURNAL_FILE) == 0:
            writer.writerow(["Ngày giờ", "Loại bài tập", "Nội dung cảm nhận"])
        
        writer.writerow([timestamp, exercise_type, content])

def get_mood_entries(exercise_filter=None):
    """Lấy các mục từ nhật ký cảm xúc của Góc An Yên, có thể lọc theo loại bài tập."""
    entries = []
    
    if not os.path.exists(MOOD_JOURNAL_FILE):
        return entries
    
    try:
        with open(MOOD_JOURNAL_FILE, 'r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                timestamp = row.get("Ngày giờ", "")
                exercise_type = row.get("Loại bài tập", "")
                content = row.get("Nội dung cảm nhận", "")
                
                if exercise_filter is None or exercise_type.strip() == exercise_filter:
                    entries.append({
                        "timestamp": timestamp,
                        "exercise_type": exercise_type,
                        "content": content
                    })
    except Exception as e:
        print(f"Error reading mood journal: {e}")
    
    return entries

# --- KHỞI TẠO BAN ĐẦU ---
create_tables()

