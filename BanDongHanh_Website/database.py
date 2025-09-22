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

# ====== BỔ SUNG CHO GÓC NHỎ - QUẢN LÝ KẾ HOẠCH CÁ NHÂN ======
def ensure_goc_nho_tables():
    """Tạo các bảng cần thiết cho chức năng Góc nhỏ."""
    conn = connect_db()
    cursor = conn.cursor()
    
    # Bảng lưu trữ người dùng đơn giản (chỉ cần username)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        created_date DATE DEFAULT (DATE('now'))
    )
    """)
    
    # Bảng lưu trữ kế hoạch hàng ngày của từng user
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        plan_date DATE NOT NULL,
        selected_actions TEXT NOT NULL,  -- JSON string of selected actions
        completed_actions TEXT DEFAULT '[]',  -- JSON string of completed actions
        created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id),
        UNIQUE(user_id, plan_date)
    )
    """)
    
    # Bảng lịch sử hành động (30 ngày)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS action_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        action_date DATE NOT NULL,
        action_name TEXT NOT NULL,
        completed_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    # Bảng thông báo/nhắc nhở
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_reminders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reminder_date DATE NOT NULL,
        reminder_type TEXT NOT NULL,  -- 'incomplete_plan', 'new_day', etc.
        message TEXT NOT NULL,
        is_shown BOOLEAN DEFAULT FALSE,
        created_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)
    
    conn.commit()
    conn.close()

def get_or_create_user(username):
    """Lấy hoặc tạo user mới, trả về user_id."""
    if not username or not username.strip():
        return None
        
    conn = connect_db()
    cursor = conn.cursor()
    
    # Tìm user hiện tại
    cursor.execute("SELECT id FROM users WHERE username = ?", (username.strip(),))
    user = cursor.fetchone()
    
    if user:
        user_id = user[0]
    else:
        # Tạo user mới
        cursor.execute("INSERT INTO users (username) VALUES (?)", (username.strip(),))
        user_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return user_id

def save_daily_plan(user_id, selected_actions, plan_date=None):
    """Lưu kế hoạch hàng ngày của user."""
    if plan_date is None:
        from datetime import date
        plan_date = date.today()
    
    import json
    conn = connect_db()
    cursor = conn.cursor()
    
    # Kiểm tra xem đã có plan cho ngày này chưa
    cursor.execute(
        "SELECT id, completed_actions FROM daily_plans WHERE user_id = ? AND plan_date = ?", 
        (user_id, plan_date)
    )
    existing = cursor.fetchone()
    
    if existing:
        # Cập nhật plan hiện tại (giữ lại completed_actions)
        cursor.execute(
            """UPDATE daily_plans 
               SET selected_actions = ?, updated_timestamp = CURRENT_TIMESTAMP 
               WHERE user_id = ? AND plan_date = ?""",
            (json.dumps(selected_actions, ensure_ascii=False), user_id, plan_date)
        )
    else:
        # Tạo plan mới
        cursor.execute(
            """INSERT INTO daily_plans (user_id, plan_date, selected_actions, completed_actions) 
               VALUES (?, ?, ?, '[]')""",
            (user_id, plan_date, json.dumps(selected_actions, ensure_ascii=False))
        )
    
    conn.commit()
    conn.close()

def get_daily_plan(user_id, plan_date=None):
    """Lấy kế hoạch hàng ngày của user."""
    if plan_date is None:
        from datetime import date
        plan_date = date.today()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT selected_actions, completed_actions FROM daily_plans WHERE user_id = ? AND plan_date = ?",
        (user_id, plan_date)
    )
    result = cursor.fetchone()
    conn.close()
    
    if result:
        import json
        return {
            'selected_actions': json.loads(result[0]) if result[0] else [],
            'completed_actions': json.loads(result[1]) if result[1] else []
        }
    return {'selected_actions': [], 'completed_actions': []}

def update_completed_actions(user_id, completed_actions, plan_date=None):
    """Cập nhật danh sách hành động đã hoàn thành."""
    if plan_date is None:
        from datetime import date
        plan_date = date.today()
    
    import json
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(
        """UPDATE daily_plans 
           SET completed_actions = ?, updated_timestamp = CURRENT_TIMESTAMP 
           WHERE user_id = ? AND plan_date = ?""",
        (json.dumps(completed_actions, ensure_ascii=False), user_id, plan_date)
    )
    
    # Thêm vào lịch sử hành động
    for action in completed_actions:
        cursor.execute(
            "INSERT OR IGNORE INTO action_history (user_id, action_date, action_name) VALUES (?, ?, ?)",
            (user_id, plan_date, action)
        )
    
    conn.commit()
    conn.close()

def get_action_history(user_id, days=30):
    """Lấy lịch sử hành động của user trong N ngày gần nhất."""
    from datetime import date, timedelta
    
    conn = connect_db()
    cursor = conn.cursor()
    
    start_date = date.today() - timedelta(days=days)
    cursor.execute(
        """SELECT action_date, action_name, completed_timestamp 
           FROM action_history 
           WHERE user_id = ? AND action_date >= ? 
           ORDER BY action_date DESC, completed_timestamp DESC""",
        (user_id, start_date)
    )
    
    history = cursor.fetchall()
    conn.close()
    
    return [{'date': row[0], 'action': row[1], 'timestamp': row[2]} for row in history]

def create_reminder(user_id, reminder_type, message, reminder_date=None):
    """Tạo nhắc nhở cho user."""
    if reminder_date is None:
        from datetime import date
        reminder_date = date.today()
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO user_reminders (user_id, reminder_date, reminder_type, message) VALUES (?, ?, ?, ?)",
        (user_id, reminder_date, reminder_type, message)
    )
    conn.commit()
    conn.close()

def get_pending_reminders(user_id):
    """Lấy các nhắc nhở chưa hiển thị của user."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, reminder_type, message, reminder_date, created_timestamp 
           FROM user_reminders 
           WHERE user_id = ? AND is_shown = FALSE 
           ORDER BY created_timestamp ASC""",
        (user_id,)
    )
    
    reminders = cursor.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'type': row[1], 
        'message': row[2],
        'date': row[3],
        'timestamp': row[4]
    } for row in reminders]

def mark_reminder_shown(reminder_id):
    """Đánh dấu nhắc nhở đã được hiển thị."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE user_reminders SET is_shown = TRUE WHERE id = ?", (reminder_id,))
    conn.commit()
    conn.close()

def check_incomplete_plans():
    """Kiểm tra các kế hoạch chưa hoàn thành và tạo nhắc nhở."""
    from datetime import date, timedelta
    import json
    
    conn = connect_db()
    cursor = conn.cursor()
    
    yesterday = date.today() - timedelta(days=1)
    cursor.execute(
        """SELECT dp.user_id, u.username, dp.selected_actions, dp.completed_actions 
           FROM daily_plans dp
           JOIN users u ON dp.user_id = u.id
           WHERE dp.plan_date = ?""",
        (yesterday,)
    )
    
    incomplete_users = []
    for row in cursor.fetchall():
        user_id, username, selected_str, completed_str = row
        selected = json.loads(selected_str) if selected_str else []
        completed = json.loads(completed_str) if completed_str else []
        
        if len(selected) > len(completed):  # Có kế hoạch chưa hoàn thành
            incomplete_users.append((user_id, username, len(selected) - len(completed)))
    
    # Tạo nhắc nhở cho ngày hôm nay
    today = date.today()
    for user_id, username, incomplete_count in incomplete_users:
        message = f"🐝 Bee nhắc {username} lên kế hoạch chăm sóc bản thân hôm nay nhé! Hôm qua bạn còn {incomplete_count} việc chưa hoàn thành."
        create_reminder(user_id, 'incomplete_plan', message, today)
    
    conn.close()

# --- KHỞI TẠO BAN ĐẦU ---
create_tables()
ensure_goc_nho_tables()
