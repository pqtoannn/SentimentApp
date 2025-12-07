import re
from const import VIETNAMESE_DICT 

def preprocess_text(text):
    """
    Hàm chuẩn hóa văn bản sử dụng từ điển trong const.py
    """
    if not isinstance(text, str):
        return ""
        
    text = text.lower()
    
    # Sử dụng VIETNAMESE_DICT được import từ const.py
    for word, replacement in VIETNAMESE_DICT.items():
        # Dùng regex để thay thế chính xác từ (tránh thay nhầm)
        pattern = r'\b' + re.escape(word) + r'\b'
        text = re.sub(pattern, replacement, text)
        
    return text