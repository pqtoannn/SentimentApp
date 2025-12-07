# nlp_core.py
import streamlit as st
from transformers import pipeline
from const import VIETNAMESE_DICT

# @st.cache_resource: Giúp không phải load lại model mỗi lần reload web
@st.cache_resource
def load_model():
    print("Đang tải model sentiment...")
    model_pipeline = pipeline(
        "sentiment-analysis",
        model="wonrax/phobert-base-vietnamese-sentiment"
    )
    return model_pipeline

# Khởi tạo model 1 lần duy nhất
classifier = load_model()

def preprocess_text(text: str) -> str:
    """Chuẩn hóa text theo dictionary."""
    if not text: return ""
    text = text.lower()
    
    # Thay thế từ điển
    words = text.split()
    processed_words = [VIETNAMESE_DICT.get(word, word) for word in words]
    text = " ".join(processed_words)
    
    # Lưu ý: Model PhoBERT chịu được khoảng 256 token, 
    # cắt 50 ký tự là quá ngắn (mất ý nghĩa câu), nên để dài hơn hoặc bỏ cắt.
    # Ở đây tôi để 200 ký tự cho an toàn.
    if len(text) > 200:
        text = text[:200]
        
    return text

def classify_sentiment(text: str):
    """
    Phân loại cảm xúc.
    Trả về Dictionary: {'label': '...', 'score': 0.99}
    """
    try:
        # Gọi pipeline
        # truncation=True để tự cắt nếu câu quá dài so với model
        result = classifier(text, truncation=True, max_length=256)[0]
        
        raw_label = result['label'] 
        score = result['score']
        
        # Ánh xạ nhãn
        final_label = "NEUTRAL"
        if raw_label == "POS":
            final_label = "POSITIVE"
        elif raw_label == "NEG":
            final_label = "NEGATIVE"
        elif raw_label == "NEU":
            final_label = "NEUTRAL"
            
        return {
            "label": final_label,
            "score": score
        }
            
    except Exception as e:
        print(f"Lỗi khi phân loại: {e}")
        return {"label": "NEUTRAL", "score": 0.0}