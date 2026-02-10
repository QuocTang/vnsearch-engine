# Hướng dẫn sử dụng VnSearch Engine

Dưới đây là các bước đơn giản để khởi động hệ thống:

### Bước 1: Chuẩn bị môi trường

- Đảm bảo đã cài đặt **Docker** và **Docker Compose**.
- Cài đặt **Python 3.10+** và công cụ **uv** (khuyên dùng để chạy Crawler).

### Bước 2: Chạy hệ thống Core (Database & n8n)

1. Mở terminal và tạo Docker network (bắt buộc):
   ```bash
   docker network create main-network
   ```
2. Chạy container:
   ```bash
   cd setup
   bash start.sh
   ```
3. Truy cập giao diện **n8n** tại: [http://localhost:5678](http://localhost:5678)

### Bước 3: Chạy VnExpress Crawler

1. Mở terminal mới và di chuyển vào thư mục crawler:
   ```bash
   cd microservices/vnexpress_crawler
   ```
2. Khởi tạo môi trường và chạy ứng dụng:
   ```bash
   cp .env.example .env  # Nếu cần chỉnh sửa cấu hình
   uv sync
   uv run main.py
   ```
3. Xem tài liệu API tại: [http://localhost:8000/docs](http://localhost:8000/docs)

### Bước 4: Nhập Workflow vào n8n

1. Mở n8n trên trình duyệt.
2. Chọn **Import from File** và chọn tệp: `microservices/n8n/vnepress_crawler_workflow.json`.
3. Kích hoạt workflow để bắt đầu thu thập dữ liệu.
