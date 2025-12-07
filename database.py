import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    """Khởi tạo CSDL và bảng sentiments."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Cập nhật thêm cột processed_text và score
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,           -- Câu gốc người dùng nhập
        processed_text TEXT,          -- Câu đã qua xử lý (Teencode/Dấu)
        sentiment TEXT NOT NULL,      -- Kết quả (POSITIVE/NEGATIVE)
        score REAL,                   -- Độ tin cậy (0.0 - 1.0)
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_sentiment(text: str, processed_text: str, sentiment: str, score: float):
    """Lưu kết quả phân loại đầy đủ."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    cursor.execute(
        """INSERT INTO sentiments (text, processed_text, sentiment, score, timestamp) 
           VALUES (?, ?, ?, ?, ?)""",
        (text, processed_text, sentiment, score, now)
    )
    conn.commit()
    conn.close()

def get_history():
    """Lấy 50 bản ghi mới nhất trả về dạng List of Tuples."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Lấy đầy đủ các cột để hiển thị lên bảng
    cursor.execute(
        """SELECT timestamp, text, processed_text, sentiment, score 
           FROM sentiments 
           ORDER BY id DESC LIMIT 50"""
    )
    history = cursor.fetchall()
    conn.close()
    return history

def get_sentiment_stats():
    """Thống kê số lượng từng loại cảm xúc."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sentiment, COUNT(*) 
        FROM sentiments 
        GROUP BY sentiment
    """)
    stats = cursor.fetchall() 
    conn.close()
    return stats

def clear_history():
    """Xóa toàn bộ dữ liệu (Dùng cho nút Reset)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sentiments")
    conn.commit()
    conn.close()