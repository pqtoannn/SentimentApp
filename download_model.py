# File: download_model.py
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Tên model trên Hugging Face
model_name = "wonrax/phobert-base-vietnamese-sentiment"

# Thư mục sẽ lưu model (nằm cùng cấp với các file code khác)
save_directory = "./local_model"

# Tạo thư mục nếu chưa có
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

print(f"⏳ Đang tải model '{model_name}' về máy...")

# Tải tokenizer và model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Lưu vào thư mục local
tokenizer.save_pretrained(save_directory)
model.save_pretrained(save_directory)

print(f"✅ Đã tải xong! Model được lưu tại: {save_directory}")