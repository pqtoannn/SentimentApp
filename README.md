# 🧠 Vietnamese Sentiment Analysis App (Trợ Lý Phân Tích Cảm Xúc)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28-red)
![AI Model](https://img.shields.io/badge/Model-PhoBERT-green)
![Status](https://img.shields.io/badge/Status-Stable-success)

Ứng dụng phân tích cảm xúc văn bản tiếng Việt sử dụng mô hình học sâu **Transformer (PhoBERT)**. Ứng dụng hỗ trợ phân loại cảm xúc (Tích cực / Tiêu cực / Trung tính) theo thời gian thực và xử lý hàng loạt qua file CSV.

---

## 🔗 Liên kết nhanh (Quick Links)

- **🏠 Source Code (GitHub):** [https://github.com/pqtoannn/SentimentApp](https://github.com/pqtoannn/SentimentApp)
- **📥 Tải phần mềm (.exe) cho Windows:** [Tải xuống phiên bản mới nhất tại đây](https://github.com/pqtoannn/SentimentApp/releases/tag/latest)

---

## ✨ Tính năng chính

1.  **Phân tích thời gian thực (Real-time Analysis):**
    - Nhập câu tiếng Việt tự do.
    - Tự động nhận diện và xử lý Teencode, từ viết tắt, sai chính tả (ví dụ: "rat thich" -> "rất thích").
    - Trả về kết quả: Nhãn cảm xúc + Độ tin cậy (Confidence Score).

2.  **Phân tích hàng loạt (Batch Processing):**
    - Hỗ trợ tải lên file `.csv`.
    - Tự động quét cột nội dung và phân tích hàng nghìn dòng trong vài giây.
    - Xuất báo cáo kết quả ra file Excel/CSV.

3.  **Lịch sử & Thống kê:**
    - Lưu lại lịch sử các lần phân tích vào cơ sở dữ liệu nội bộ (SQLite).
    - Hiển thị bảng thống kê trực quan ngay trên giao diện.

4.  **Chế độ Offline (Sau lần chạy đầu):**
    - Mô hình AI được lưu cache cục bộ, không cần internet cho các lần sử dụng sau.

---

## 🚀 Hướng dẫn Cài đặt & Sử dụng

### 🅰️ Dành cho Người dùng phổ thông (Chạy file .exe)

Bạn không cần cài đặt Python hay biết về lập trình. Chỉ cần tải về và chạy.

1.  **Bước 1:** Truy cập [Link tải xuống](https://github.com/pqtoannn/SentimentApp/releases/tag/latest).
2.  **Bước 2:** Tải file `.zip` (ví dụ: `PhanTichCamXuc_Lite.zip`) về máy.
3.  **Bước 3:** Giải nén toàn bộ thư mục ra máy tính.
4.  **Bước 4:** Mở thư mục vừa giải nén, tìm và chạy file `PhanTichCamXuc_Lite.exe`.

> **⚠️ Lưu ý quan trọng cho lần chạy đầu tiên:**
> Vì đây là phiên bản Lite (giảm dung lượng), ở **lần mở đầu tiên**, máy tính của bạn cần **kết nối Internet**. Ứng dụng sẽ tự động tải mô hình AI (khoảng 300MB) về máy. Các lần sau bạn có thể dùng Offline hoàn toàn.

---

### 🅱️ Dành cho Lập trình viên (Chạy từ Source Code)

Nếu bạn muốn chỉnh sửa code hoặc chạy trên môi trường phát triển:

#### 1. Yêu cầu hệ thống
- Python 3.8 trở lên.
- Git.

#### 2. Cài đặt

```bash
# Clone dự án về máy
git clone [https://github.com/pqtoannn/SentimentApp.git](https://github.com/pqtoannn/SentimentApp.git)
cd SentimentApp

# Tạo môi trường ảo (Khuyến nghị)
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows:
.venv\Scripts\activate
# Trên Mac/Linux:
source .venv/bin/activate

# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

```
3. Chạy ứng dụng
```bash
streamlit run app.py
```
Sau khi chạy lệnh, trình duyệt sẽ tự động mở địa chỉ http://localhost:8501

## 📂 Cấu trúc dự án
```text
SentimentApp/
├── app.py              # Giao diện chính (Streamlit UI)
├── nlp_core.py         # Xử lý mô hình AI (Load Model, Prediction logic)
├── utils.py            # Các hàm phụ trợ (Clean text, xử lý Teencode)
├── const.py            # Chứa từ điển Teencode và các hằng số
├── database.py         # Quản lý kết nối SQLite (Lưu/Đọc lịch sử)
├── build_exe_lite.py   # Script đóng gói ra file .exe
├── requirements.txt    # Danh sách thư viện
└── README.md           # Tài liệu hướng dẫn
```
## 🛠 Công nghệ sử dụng
Ngôn ngữ: Python.

Giao diện: Streamlit.

Core AI: Hugging Face Transformers (PhoBERT Base).

Deep Learning Framework: PyTorch.

Database: SQLite.

Đóng gói: PyInstaller.

