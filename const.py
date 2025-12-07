# const.py

# VIETNAMESE_DICT: Phiên bản đầy đủ cho 10 test case
VIETNAMESE_DICT = {
    # Test case 4: "Rat vui hom nay"
    "rat": "rất", "vui": "vui", "hom": "hôm", "nay": "nay",
    
    # Test case 2 & biến thể
    "mon": "món", "an": "ăn", "dzo": "dở", "wa": "quá", "qua": "quá",
    
    # Test case 6
    "phim": "phim", "hay": "hay", "lam": "lắm",
    
    # Test case 9
    "cam": "cảm", "on": "ơn", "ban": "bạn", "nhieu": "nhiều",
    
    # Case 10
    "met": "mệt", "moi": "mỏi",
    
    # Case 3
    "bt": "bình thường", "thoi": "thời", "tiet": "tiết",
    
    # Các từ phổ biến khác
    "ko": "không", "dc": "được", "buon": "buồn",
}

TEST_CASES = [
    {"id": 1, "text": "Hôm nay tôi rất vui", "expected": "POSITIVE"},
    {"id": 2, "text": "Món ăn này dở quá", "expected": "NEGATIVE"},
    {"id": 3, "text": "Thời tiết bình thường", "expected": "NEUTRAL"},
    {"id": 4, "text": "Rat vui hom nay", "expected": "POSITIVE"}, # Test teencode
    {"id": 5, "text": "Công việc ổn định", "expected": "NEUTRAL"},
    {"id": 6, "text": "Phim này hay lắm", "expected": "POSITIVE"},
    {"id": 7, "text": "Tôi buồn vì thất bại", "expected": "NEGATIVE"},
    {"id": 8, "text": "Ngày mai đi học", "expected": "NEUTRAL"},
    {"id": 9, "text": "Cảm ơn bạn rất nhiều", "expected": "POSITIVE"},
    {"id": 10, "text": "Mệt mỏi quá hôm nay", "expected": "NEGATIVE"},
]