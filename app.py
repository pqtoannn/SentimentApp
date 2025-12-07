import streamlit as st
import pandas as pd
import time

# --- 1. IMPORT CÁC MODULE TỰ VIẾT ---
try:
    from utils import preprocess_text
    from nlp_core import classify_sentiment
    from database import (
        init_db, save_sentiment, get_history, 
        get_sentiment_stats, clear_history
    )
except ImportError as e:
    st.error(f"❌ Lỗi Import: {e}. Hãy đảm bảo bạn có đủ 4 file: const.py, utils.py, nlp_core.py, database.py cùng thư mục.")
    st.stop()

# ==========================================
# 2. CẤU HÌNH TRANG & KHỞI TẠO
# ==========================================
st.set_page_config(
    page_title="Vietnamese Sentiment Analytics",
    page_icon="🧠",
    layout="wide"
)

# Khởi tạo Database ngay khi app chạy
init_db()

# CSS làm đẹp giao diện & Fix lỗi hiển thị Darkmode cho Metric
st.markdown("""
<style>
    .stButton>button {width: 100%; border-radius: 8px; font-weight: bold;}
    div[data-testid="metric-container"] {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        color: #31333F; /* Luôn dùng chữ màu tối cho metric */
    }
    /* Fix cho Darkmode: Đảm bảo metric vẫn sáng để dễ đọc */
    @media (prefers-color-scheme: dark) {
        div[data-testid="metric-container"] {
            background-color: #262730;
            color: #ffffff;
        }
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. SIDEBAR (MENU ĐÃ GỘP)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=80)
    st.title("NLP Dashboard")
    
    # Rút gọn menu chỉ còn 2 mục chính
    menu = st.radio(
        "Chọn chức năng:", 
        ["🏠 Trang chủ (Phân tích & Lịch sử)", "📂 Kiểm thử File CSV"]
    )
    
    st.divider()
    st.info("💡 **Ghi chú:**\n- Chế độ hiển thị đã được tối ưu cho cả Dark Mode và Light Mode.")

# ==========================================
# 4. HÀM TÔ MÀU (FIX LỖI DARK MODE)
# ==========================================
def style_sentiment_table(row, col_name_sentiment):
    """
    Hàm này trả về CSS gồm cả background-color VÀ color (màu chữ)
    để đảm bảo đọc được trên mọi nền tảng.
    """
    val = row[col_name_sentiment]
    
    # POSITIVE: Nền xanh nhạt - Chữ xanh đậm
    if val == 'POSITIVE':
        return ['background-color: #d1e7dd; color: #0f5132'] * len(row)
    
    # NEGATIVE: Nền đỏ nhạt - Chữ đỏ đậm
    elif val == 'NEGATIVE':
        return ['background-color: #f8d7da; color: #842029'] * len(row)
    
    # NEUTRAL: Nền vàng nhạt - Chữ nâu đậm
    elif val == 'NEUTRAL':
        return ['background-color: #fff3cd; color: #664d03'] * len(row)
        
    return [''] * len(row)

# ==========================================
# 5. CHỨC NĂNG 1: TRANG CHỦ (GỘP PHÂN TÍCH + LỊCH SỬ)
# ==========================================
if menu == "🏠 Trang chủ (Phân tích & Lịch sử)":
    
    # --- PHẦN A: FORM NHẬP LIỆU ---
    st.header("🔍 Phân tích cảm xúc")
    
    col_input, col_btn = st.columns([3, 1])
    with col_input:
        user_input = st.text_input("Nhập văn bản:", placeholder="Ví dụ: hàng tốt, giao nhanh...")
    with col_btn:
        st.write("") 
        st.write("") 
        btn_analyze = st.button("🚀 Chạy phân tích", type="primary")

    if btn_analyze and user_input.strip():
        with st.spinner("Đang xử lý..."):
            # 1. Xử lý & AI
            cleaned_text = preprocess_text(user_input)
            result = classify_sentiment(cleaned_text)
            label = result.get('label', 'NEUTRAL')
            score = result.get('score', 0.0)
            
            # 2. Lưu DB
            save_sentiment(user_input, cleaned_text, label, score)
            
            # 3. Hiển thị kết quả ngay lập tức
            st.success("Đã phân tích xong!")
            c1, c2 = st.columns([2, 1])
            with c1:
                if label == "POSITIVE":
                    st.markdown(f"### 😊 TÍCH CỰC")
                elif label == "NEGATIVE":
                    st.markdown(f"### 😡 TIÊU CỰC")
                else:
                    st.markdown(f"### 😐 TRUNG TÍNH")
                st.caption(f"Đã làm sạch: {cleaned_text}")
            with c2:
                st.metric("Độ tin cậy", f"{score:.2%}")
                st.progress(score)

    # --- PHẦN B: LỊCH SỬ (NẰM NGAY DƯỚI) ---
    st.divider()
    st.subheader("📜 Lịch sử phân tích gần đây")

    # Lấy dữ liệu
    history_data = get_history()
    
    if history_data:
        # Tạo DataFrame
        df = pd.DataFrame(
            history_data, 
            columns=['Thời gian', 'Câu gốc', 'Đã xử lý', 'Cảm xúc', 'Độ tin cậy']
        )
        
        # Thống kê nhanh
        stats = get_sentiment_stats()
        stats_dict = {item[0]: item[1] for item in stats}
        
        c_stat1, c_stat2, c_stat3, c_btn = st.columns(4)
        c_stat1.metric("Tổng số câu", len(df))
        c_stat2.metric("Tích cực", stats_dict.get('POSITIVE', 0))
        c_stat3.metric("Tiêu cực", stats_dict.get('NEGATIVE', 0))
        with c_btn:
            st.write("")
            if st.button("🗑️ Xóa lịch sử"):
                clear_history()
                st.rerun()

        # HIỂN THỊ BẢNG (Đã fix lỗi màu sắc)
        # Sắp xếp mới nhất lên đầu
        df_display = df.iloc[::-1] 
        
        # Áp dụng Style
        # Lưu ý: 'Cảm xúc' là tên cột chứa POSITIVE/NEGATIVE
        styled_df = df_display.style.apply(lambda row: style_sentiment_table(row, 'Cảm xúc'), axis=1)
        
        st.dataframe(styled_df, use_container_width=True, height=400)
        
    else:
        st.info("Chưa có dữ liệu. Hãy nhập một câu ở trên để bắt đầu!")

# ==========================================
# 6. CHỨC NĂNG 2: KIỂM THỬ FILE CSV (GIỮ NGUYÊN TAB 3 CŨ)
# ==========================================
elif menu == "📂 Kiểm thử File CSV":
    st.header("📂 Kiểm thử hàng loạt (Batch Processing)")
    st.write("Tải lên file CSV để phân tích nhiều dòng cùng lúc.")
    
    uploaded_file = st.file_uploader("Tải lên file CSV (UTF-8)", type=['csv'])
    
    if uploaded_file:
        try:
            df_upload = pd.read_csv(uploaded_file, encoding='utf-8', on_bad_lines='skip')
            
            # Tìm cột text
            text_col = next((c for c in df_upload.columns if c.lower() in ['text', 'content', 'câu', 'comment', 'review']), None)
            
            if text_col:
                st.success(f"Cột dữ liệu: **{text_col}**")
                
                if st.button("⚡ Bắt đầu phân tích"):
                    # ... (Logic xử lý giữ nguyên như cũ) ...
                    progress_bar = st.progress(0)
                    results_label = []
                    results_score = []
                    processed_texts = []
                    total = len(df_upload)
                    
                    for i, row in df_upload.iterrows():
                        text_origin = str(row[text_col])
                        clean = preprocess_text(text_origin)
                        res = classify_sentiment(clean)
                        
                        lbl = res.get('label', 'NEUTRAL')
                        scr = res.get('score', 0.0)
                        
                        processed_texts.append(clean)
                        results_label.append(lbl)
                        results_score.append(scr)
                        
                        # Có thể chọn lưu hoặc không lưu vào lịch sử chung ở đây
                        # save_sentiment(text_origin, clean, lbl, scr) 
                        
                        progress_bar.progress((i + 1) / total)
                    
                    df_upload['Processed'] = processed_texts
                    df_upload['AI_Label'] = results_label
                    df_upload['AI_Score'] = results_score
                    
                    st.success("✅ Hoàn tất!")
                    
                    # Áp dụng Style FIX LỖI MÀU SẮC cho bảng CSV
                    # Lưu ý: Cột chứa label ở đây là 'AI_Label'
                    styled_csv = df_upload.style.apply(lambda row: style_sentiment_table(row, 'AI_Label'), axis=1)
                    
                    st.dataframe(styled_csv, use_container_width=True)
                    
                    # Download
                    csv_res = df_upload.to_csv(index=False).encode('utf-8-sig')
                    st.download_button("📥 Tải kết quả", csv_res, "ketqua_batch.csv")
            else:
                st.error("Không tìm thấy cột chứa nội dung (text/content...).")
        except Exception as e:
            st.error(f"Lỗi: {e}")