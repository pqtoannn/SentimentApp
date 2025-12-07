# database.py
import sqlite3
from datetime import datetime

DB_NAME = "history.db"

def init_db():
    """Khởi tạo CSDL và bảng sentiments."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sentiments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        sentiment TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def save_sentiment(text: str, sentiment: str):
    """Lưu kết quả phân loại."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        "INSERT INTO sentiments (text, sentiment, timestamp) VALUES (?, ?, ?)",
        (text, sentiment, now)
    )
    conn.commit()
    conn.close()

def get_history():
    """Lấy 50 bản ghi mới nhất."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, text, sentiment FROM sentiments ORDER BY timestamp DESC LIMIT 50"
    )
    history = cursor.fetchall()
    conn.close()
    return history

# Thêm vào cuối file database.py

def get_sentiment_stats():
    """Thống kê số lượng từng loại cảm xúc để vẽ biểu đồ."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT sentiment, COUNT(*) 
        FROM sentiments 
        GROUP BY sentiment
    """)
    stats = cursor.fetchall() # Trả về list dạng [('POSITIVE', 5), ('NEGATIVE', 2)...]
    conn.close()
    return stats