# nlp_core.py
import streamlit as st
from transformers import pipeline
from const import VIETNAMESE_DICT

@st.cache_resource
def load_model():
    """
    Tải model đã được Fine-tune cho tác vụ Sentiment Tiếng Việt.
    Model: wonrax/phobert-base-vietnamese-sentiment
    (Dựa trên kiến trúc PhoBERT chuẩn của VinAI)
    """
    print("Đang tải model sentiment...")
    model_pipeline = pipeline(
        "sentiment-analysis",
        model="wonrax/phobert-base-vietnamese-sentiment"
    )
    return model_pipeline

# Khởi tạo model
classifier = load_model()

def preprocess_text(text: str) -> str:
    """Chuẩn hóa text theo dictionary."""
    text = text.lower()
    words = text.split()
    processed_words = [VIETNAMESE_DICT.get(word, word) for word in words]
    text = " ".join(processed_words)
    
    if len(text) > 50:
        text = text[:50]
    return text

def classify_sentiment(text: str) -> str:
    """Phân loại cảm xúc."""
    try:
        # 1. Gọi pipeline
        result = classifier(text)[0]
        label = result['label'] 
        
        # Model wonrax trả về nhãn: 'POS', 'NEG', 'NEU'
        
        # 2. Ánh xạ nhãn sang format yêu cầu
        if label == "POS":
            return "POSITIVE"
        elif label == "NEG":
            return "NEGATIVE"
        elif label == "NEU":
            return "NEUTRAL"
        else:
            return "NEUTRAL"
            
    except Exception as e:
        print(f"Lỗi khi phân loại: {e}")
        return "NEUTRAL"