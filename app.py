import streamlit as st
import pandas as pd
import time
import random

# ==========================================
# 1. CẤU HÌNH TRANG & CSS
# ==========================================
st.set_page_config(
    page_title="Vietnamese Sentiment Analysis",
    page_icon="🤖",
    layout="wide"
)

# CSS tùy chỉnh để giao diện đẹp hơn
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stButton>button {width: 100%; border-radius: 5px; height: 3em;}
    .stMetric {background-color: #262730; padding: 15px; border-radius: 5px; border: 1px solid #41444e;}
    .css-1v0mbdj {display: flex; justify-content: center;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. KHỐI XỬ LÝ AI (MODEL)
# ==========================================
@st.cache_resource
def load_ai_model():
    """
    Hàm này chỉ chạy 1 lần để load model nặng vào bộ nhớ.
    Bạn hãy đặt code load model (PhoBERT/ViBERT) thật của bạn vào đây.
    """
    # Ví dụ:
    # tokenizer = AutoTokenizer.from_pretrained("path_to_model")
    # model = AutoModelForSequenceClassification.from_pretrained("path_to_model")
    # return tokenizer, model
    print("Model loaded!")
    return None

# Load model (giả lập)
model = load_ai_model()

def predict_sentiment(text):
    """
    Hàm dự đoán cảm xúc.
    Thay thế logic bên dưới bằng logic model thật của bạn.
    Input: Chuỗi văn bản
    Output: Dictionary {label, score}
    """
    # --- BẮT ĐẦU: KHU VỰC GIẢ LẬP (Xóa đi khi dùng model thật) ---
    time.sleep(0.5) # Giả lập độ trễ xử lý
    
    # Logic random để demo giao diện
    keywords_pos = ['vui', 'tốt', 'thích', 'tuyệt', 'ngon', 'yêu']
    keywords_neg = ['buồn', 'chán', 'tệ', 'đau', 'ghét', 'xấu']
    
    text_lower = text.lower()
    if any(k in text_lower for k in keywords_pos):
        label = "POSITIVE"
        score = random.uniform(0.85, 0.99)
    elif any(k in text_lower for k in keywords_neg):
        label = "NEGATIVE"
        score = random.uniform(0.70, 0.95)
    else:
        label = "NEUTRAL"
        score = random.uniform(0.50, 0.70)
    # --- KẾT THÚC: KHU VỰC GIẢ LẬP ---

    return {"label": label, "score": score}

# ==========================================
# 3. GIAO DIỆN CHÍNH (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100)
    st.title("Menu Điều Khiển")
    
    menu = st.radio("Chọn chức năng:", ["Trang chủ (Kiểm tra nhanh)", "Kiểm thử theo Lô (File CSV)"])
    
    st.info("💡 **Mẹo:** \n- Chức năng CSV hỗ trợ file có cột tên là 'text' hoặc 'content'.")
    st.caption("Phiên bản: 2.0.1 (Update Batch Test)")

# ==========================================
# 4. CHỨC NĂNG 1: TRANG CHỦ (SINGLE TEST)
# ==========================================
if menu == "Trang chủ (Kiểm tra nhanh)":
    st.header("📝 Nhập liệu & Phân tích thời gian thực")
    st.markdown("Hệ thống ghi nhận và phân tích phản hồi tiếng Việt.")

    # Khởi tạo session_state để lưu kết quả không bị mất khi reload
    if 'single_result' not in st.session_state:
        st.session_state.single_result = None

    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_input = st.text_area("Nhập câu văn bản:", height=150, placeholder="Ví dụ: Hôm nay tôi cảm thấy rất vui vì trời đẹp.")
        
        if st.button("🚀 Phân tích ngay", type="primary"):
            if user_input.strip():
                with st.spinner('Đang phân tích...'):
                    # Gọi hàm xử lý
                    result = predict_sentiment(user_input)
                    # Lưu vào session_state
                    st.session_state.single_result = result
            else:
                st.warning("Vui lòng nhập nội dung!")

    # Hiển thị kết quả (Kiểm tra trong session_state)
    with col2:
        if st.session_state.single_result:
            res = st.session_state.single_result
            lbl = res['label']
            scr = res['score']
            
            st.subheader("Kết quả phân tích")
            
            # Logic màu sắc và icon
            if lbl == "POSITIVE":
                st.success(f"TÍCH CỰC (Positive)")
                st.balloons()
            elif lbl == "NEGATIVE":
                st.error(f"TIÊU CỰC (Negative)")
            else:
                st.warning(f"TRUNG TÍNH (Neutral)")
            
            # Hiển thị Score chi tiết
            st.metric(label="Độ tin cậy (Confidence Score)", value=f"{scr:.2%}", delta="AI Model")
            st.progress(scr)
            st.caption(f"AI chắc chắn {scr*100:.1f}% về kết quả này.")

# ==========================================
# 5. CHỨC NĂNG 2: KIỂM THỬ CSV (BATCH TEST)
# ==========================================
elif menu == "Kiểm thử theo Lô (File CSV)":
    st.header("📂 Kiểm thử tự động qua file CSV")
    
    uploaded_file = st.file_uploader("Tải lên file CSV (UTF-8)", type=["csv"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file, encoding='utf-8')
            
            # Kiểm tra xem file có cột chứa text không
            text_column = None
            possible_names = ['text', 'content', 'câu', 'comment', 'review']
            
            # Tự động tìm cột phù hợp
            for col in df.columns:
                if col.lower() in possible_names:
                    text_column = col
                    break
            
            if text_column:
                st.write(f"Đã tìm thấy cột dữ liệu: **{text_column}**. Đang hiển thị 5 dòng đầu:")
                st.dataframe(df.head())
                
                if st.button("⚡ Chạy phân tích hàng loạt"):
                    # Thanh tiến trình
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    results = []
                    scores = []
                    
                    total_rows = len(df)
                    
                    for i, row in df.iterrows():
                        # Lấy text
                        text = str(row[text_column])
                        
                        # Dự đoán
                        prediction = predict_sentiment(text)
                        
                        # Lưu kết quả
                        results.append(prediction['label'])
                        scores.append(prediction['score'])
                        
                        # Cập nhật thanh tiến trình
                        progress = (i + 1) / total_rows
                        progress_bar.progress(progress)
                        status_text.text(f"Đang xử lý dòng {i+1}/{total_rows}...")
                    
                    # Thêm kết quả vào DataFrame
                    df['AI_Label'] = results
                    df['AI_Score'] = scores
                    
                    st.success("✅ Đã xử lý xong!")
                    status_text.empty()
                    
                    # Hiển thị bảng kết quả
                    st.subheader("Kết quả chi tiết:")
                    
                    # Tô màu cho bảng kết quả (Pandas Styler)
                    def color_sentiment(val):
                        if val == 'POSITIVE': return 'background-color: #d4edda; color: green'
                        elif val == 'NEGATIVE': return 'background-color: #f8d7da; color: red'
                        return 'background-color: #fff3cd; color: orange'

                    st.dataframe(df.style.applymap(color_sentiment, subset=['AI_Label']))
                    
                    # Chức năng Download
                    csv_data = df.to_csv(index=False).encode('utf-8-sig') # utf-8-sig để Excel đọc được tiếng Việt
                    st.download_button(
                        label="📥 Tải xuống kết quả (CSV)",
                        data=csv_data,
                        file_name="ket_qua_phan_tich.csv",
                        mime="text/csv",
                    )
                    
                    # Thống kê nhanh
                    st.write("---")
                    col_stat1, col_stat2 = st.columns(2)
                    with col_stat1:
                        st.write("Biểu đồ phân bố nhãn:")
                        st.bar_chart(df['AI_Label'].value_counts())
                        
            else:
                st.error(f"Không tìm thấy cột chứa văn bản. File CSV cần có một trong các cột: {', '.join(possible_names)}")
                st.write("Các cột hiện có:", list(df.columns))
                
        except Exception as e:
            st.error(f"Lỗi khi đọc file: {e}")