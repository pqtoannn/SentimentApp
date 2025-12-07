import streamlit as st
import pandas as pd
import time
import datetime
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# --- 1. IMPORT HÀM XỬ LÝ TỪ UTILS ---
# Đoạn này sẽ lấy hàm chuẩn hóa từ file utils.py
try:
    from utils import preprocess_text
except ImportError:
    st.error("⚠️ Lỗi: Không tìm thấy file 'utils.py'. Hãy tạo file này và 'const.py' cùng thư mục!")
    st.stop()

# ==========================================
# 2. CẤU HÌNH TRANG & CSS
# ==========================================
st.set_page_config(
    page_title="Vietnamese Sentiment Analysis (Final)",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stButton>button {width: 100%; border-radius: 5px; height: 3em; font-weight: bold;}
    .metric-card {background-color: #262730; padding: 15px; border-radius: 8px; border: 1px solid #41444e;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. KHỐI XỬ LÝ AI (MODEL THẬT)
# ==========================================
@st.cache_resource
def load_ai_model():
    """
    Load model PhoBERT từ HuggingFace.
    """
    model_name = "wonrax/phobert-base-vietnamese-sentiment"
    
    # st.write(f"Đang tải model: {model_name} ...") # Bật dòng này nếu muốn xem log trên web
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    
    return tokenizer, model

# Load model ngay khi app khởi động
try:
    # with st.spinner("Đang khởi động AI Model..."): # Tắt spinner để giao diện lên nhanh hơn nếu đã cache
    tokenizer, model = load_ai_model()
except Exception as e:
    st.error(f"Lỗi tải model: {e}")
    st.stop()

def predict_sentiment(text):
    """
    Dự đoán cảm xúc sử dụng model PhoBERT thật + Tiền xử lý (Preprocessing).
    """
    if not text:
        return None

    # --- BƯỚC QUAN TRỌNG: CHUẨN HÓA VĂN BẢN TRƯỚC ---
    # Ví dụ: "hang k tot" -> "hàng không tốt"
    clean_text = preprocess_text(text)
    # -----------------------------------------------

    # 1. Tokenize văn bản ĐÃ LÀM SẠCH
    inputs = tokenizer(clean_text, return_tensors="pt", truncation=True, padding=True, max_length=256)
    
    # 2. Đưa qua Model
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1)
    
    # 3. Lấy kết quả
    labels_map = {0: "NEGATIVE", 1: "POSITIVE", 2: "NEUTRAL"}
    
    score_list = probs[0].tolist()
    max_score = max(score_list)
    max_index = score_list.index(max_score)
    
    label = labels_map[max_index]
    
    # Trả về cả clean_text để hiển thị cho người dùng xem AI đã sửa gì
    return {"label": label, "score": max_score, "clean_text": clean_text}

# ==========================================
# 4. QUẢN LÝ SESSION STATE (LƯU LỊCH SỬ)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []

def add_to_history(original, cleaned, label, score):
    st.session_state.history.insert(0, {
        "Thời gian": datetime.datetime.now().strftime("%H:%M:%S"),
        "Câu gốc": original,
        "AI đã hiểu là": cleaned, # Thêm cột này để so sánh
        "Kết quả": label,
        "Độ tin cậy": f"{score:.2%}"
    })

# ==========================================
# 5. GIAO DIỆN CHÍNH
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("AI Control Panel")
    menu = st.radio("Chế độ:", ["Trang chủ (Single Test)", "Kiểm thử file (CSV Batch)"])
    st.success("✅ Model Status: Online")
    st.info("💡 Đã bật tính năng tự động sửa lỗi (Auto-Correction).")

# ==========================================
# CHỨC NĂNG 1: TRANG CHỦ
# ==========================================
if menu == "Trang chủ (Single Test)":
    st.title("🧠 Phân tích cảm xúc (Real AI)")
    
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        user_input = st.text_input("Nhập câu cần phân tích:", placeholder="VD: mon an nay dzo qua (thử viết không dấu)...")
    with col_btn:
        st.write("") 
        st.write("")
        btn_analyze = st.button("🔍 Phân tích", type="primary")

    if btn_analyze and user_input.strip():
        # Gọi hàm AI thật
        result = predict_sentiment(user_input)
        
        # Lưu kết quả
        add_to_history(user_input, result['clean_text'], result['label'], result['score'])
        st.session_state.current_result = result

    # Hiển thị kết quả
    if 'current_result' in st.session_state and st.session_state.current_result:
        res = st.session_state.current_result
        lbl = res['label']
        scr = res['score']
        clean = res['clean_text']
        
        st.markdown("---")
        c1, c2 = st.columns([2, 1])
        
        with c1:
            if lbl == "POSITIVE":
                st.success(f"### 😃 TÍCH CỰC (POSITIVE)")
            elif lbl == "NEGATIVE":
                st.error(f"### 😡 TIÊU CỰC (NEGATIVE)")
            else:
                st.warning(f"### 😐 TRUNG TÍNH (NEUTRAL)")
            
            st.write(f"Câu gốc: *'{user_input}'*")
            # Hiển thị câu đã được chuẩn hóa để người dùng biết tại sao AI đoán vậy
            st.caption(f"ℹ️ AI đã tự động sửa thành: **'{clean}'**")

        with c2:
            st.metric("Độ tin cậy AI", f"{scr:.2%}")
            st.progress(scr)

    # Dashboard
    if len(st.session_state.history) > 0:
        st.markdown("---")
        st.subheader("📊 Lịch sử phân tích")
        
        # Nút xóa lịch sử
        if st.button("Xóa lịch sử"):
            st.session_state.history = []
            st.rerun()
            
        st.dataframe(pd.DataFrame(st.session_state.history), use_container_width=True)

# ==========================================
# CHỨC NĂNG 2: KIỂM THỬ CSV (BATCH TEST)
# ==========================================
elif menu == "Kiểm thử file (CSV Batch)":
    st.title("📂 Kiểm thử hàng loạt (CSV)")
    
    uploaded_file = st.file_uploader("Upload file CSV (UTF-8)", type=["csv"])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            
            # Tìm cột text
            text_col = next((c for c in df.columns if c.lower() in ['text', 'content', 'câu']), None)
            
            if text_col:
                st.write(f"Đang xem trước 3 dòng (Tổng: {len(df)} dòng):")
                st.dataframe(df.head(3))
                
                if st.button("⚡ Chạy AI Phân tích"):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results, scores, cleaned_texts = [], [], []
                    total = len(df)
                    
                    start_time = time.time()
                    
                    for i, row in df.iterrows():
                        # Gọi AI
                        pred = predict_sentiment(str(row[text_col]))
                        results.append(pred['label'])
                        scores.append(pred['score'])
                        cleaned_texts.append(pred['clean_text']) # Lưu cả text đã xử lý
                        
                        # Cập nhật tiến trình
                        prog = (i + 1) / total
                        progress_bar.progress(prog)
                        status_text.text(f"Đang xử lý: {i+1}/{total} câu...")
                    
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    # Thêm kết quả vào DataFrame
                    df['Processed_Text'] = cleaned_texts # Cột mới: Text đã qua xử lý
                    df['AI_Label'] = results
                    df['AI_Score'] = scores
                    
                    st.success(f"✅ Hoàn thành trong {duration:.2f} giây!")
                    
                    # Tô màu kết quả
                    def color_df(val):
                        color = 'green' if val == 'POSITIVE' else ('red' if val == 'NEGATIVE' else 'orange')
                        return f'color: {color}; font-weight: bold'
                        
                    st.dataframe(df.style.applymap(color_df, subset=['AI_Label']))
                    
                    # Download
                    csv = df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📥 Tải kết quả về", csv, "ket_qua_ai_complete.csv", "text/csv")
            else:
                st.error("Không tìm thấy cột 'text' hoặc 'content' trong file CSV.")
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")