# const.py (Phiên bản đã sửa lỗi ngữ cảnh & thêm từ vựng)

VIETNAMESE_DICT = {
    # --- 1. SỬA LỖI NGỮ CẢNH (Quan trọng: Xóa các từ 'lam', 'ban', 'on' gây lỗi) ---
    # Chỉ giữ lại những từ chắc chắn đúng 100%
    "rat": "rất", 
    "wa": "quá", "qua": "quá",
    "dzo": "dở", 
    "bt": "bình thường",
    "ko": "không", "k": "không", "kh": "không", "hok": "không",
    "dc": "được", "đc": "được",
    "mn": "mọi người",
    "nt": "nhắn tin",
    "sp": "sản phẩm",
    
    # --- 2. BỔ SUNG TỪ TIÊU CỰC (Fix lỗi Case 20, 21, 24) ---
    "te": "tệ", 
    "xau": "xấu",
    "hong": "hỏng", 
    "loi": "lỗi",
    "lom": "lõm", # Để xử lý từ 'lồi lõm'
    "chan": "chán",
    "buon": "buồn",
    "vong": "vọng", # thất vọng
    "rach": "rách",
    
    # --- 3. BỔ SUNG TỪ TÍCH CỰC ---
    "thich": "thích",
    "iu": "yêu",
    "ung": "ưng",
    "tuyet": "tuyệt",
    "dep": "đẹp",
    "ok": "tốt", "oke": "tốt", "gud": "tốt",
    
    # --- 4. HACK NÃO AI (Xử lý các cụm đặc biệt) ---
    # Thay thế cả cụm từ để AI không hiểu nhầm
    "k che": "xuất sắc", # Fix Case 29: biến 'không chê' thành từ tích cực mạnh
    "k dl": "không du lịch", # Ví dụ khác
}

# (Phần TEST_CASES bên dưới giữ nguyên hoặc xóa đi cũng được vì không dùng trong app)