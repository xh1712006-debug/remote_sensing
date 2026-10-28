# Hướng Dẫn Phát Triển Dự Án FieldShift Cho Antigravity AI

## 1. Triết Lý & Nguyên Tắc Cốt Lõi
- **Bám sát yêu cầu đề bài NASA**: Luôn đối chiếu với [PROJECT_REQUIREMENTS.md](file:///d:/project/project-local/vientham/PROJECT_REQUIREMENTS.md) để giải quyết đúng bài toán: thích ứng biến đổi khí hậu, cải tạo sức khỏe đất và luân canh bằng dữ liệu vệ tinh NASA.
- **Kiến trúc thống nhất MVT**: Sử dụng Python Django MVT (Model - View - Template) kết hợp cơ sở dữ liệu PostgreSQL 18. Toàn bộ mã nguồn backend và frontend nằm trong cùng một repository duy nhất.
- **Quy chuẩn Code**: Tên biến, tên hàm, class bằng **Tiếng Anh**. Chú thích (comments) giải thích lý do bằng **Tiếng Việt** ngắn gọn, chuẩn xác theo [comment.md](file:///d:/project/project-local/vientham/.antigravity/rules/comment.md).

---

## 2. Hệ Thống Quy Tắc Bắt Buộc (Mandatory Rules)
Nằm trong thư mục `.antigravity/rules/`:
- **[business_rules.md](file:///d:/project/project-local/vientham/.antigravity/rules/business_rules.md)**: 4 nguyên tắc nghiệp vụ nông nghiệp (Cân bằng đạm sinh học, luân phiên rễ sâu/nông, cắt đứt sâu bệnh, quy tắc né hạn né bão).
- **[nasa_data_rules.md](file:///d:/project/project-local/vientham/.antigravity/rules/nasa_data_rules.md)**: Quy tắc khai thác và xử lý dữ liệu vệ tinh NASA POWER (chuẩn tọa độ WGS-84, làm tròn 4 số thập phân, timeout 12s, fallback cache an toàn).
- **[comment.md](file:///d:/project/project-local/vientham/.antigravity/rules/comment.md)**: Quy chuẩn viết chú thích bằng tiếng Việt và mã nguồn tiếng Anh.

---

## 3. Hệ Thống Kỹ Năng Chuyên Sâu (Advanced Project Skills)
Nằm trong thư mục `.antigravity/skills/`:

### A. Thiết kế Giao diện & Trực quan hóa
* **[ui_ux_agritech_design.md](file:///d:/project/project-local/vientham/.antigravity/skills/ui_ux_agritech_design.md)**: Cẩm nang thiết kế giao diện nông nghiệp công nghệ cao (phối màu vũ trụ - đất mẹ, Glassmorphism, Chart.js UX và bản đồ ESRI vệ tinh).

### B. Khoa học Dữ liệu & Nông nghiệp Thích ứng
* **[crop_rotation_planner.md](file:///d:/project/project-local/vientham/.antigravity/skills/crop_rotation_planner.md)**: Kỹ năng phân tích 5 bước và thuật toán lập kế hoạch luân canh 3 vụ thích ứng khí hậu.
* **[nasa_analysis.md](file:///d:/project/project-local/vientham/.antigravity/skills/nasa_analysis.md)**: Kỹ năng truy vấn và diễn giải các chỉ số vệ tinh Trái Đất (T2M_MAX, PRECTOTCORR, GWETTOP, GWETROOT).
* **[crop_dataset_manager.md](file:///d:/project/project-local/vientham/.antigravity/skills/crop_dataset_manager.md)**: Kỹ năng chuẩn hóa thuộc tính sinh học giống cây và nạp dữ liệu hàng loạt vào PostgreSQL.
* **[gis_satellite_indices.md](file:///d:/project/project-local/vientham/.antigravity/skills/gis_satellite_indices.md)**: Tích hợp chỉ số thực vật viễn thám mở rộng (NDVI, LST) và kết nối API thổ nhưỡng toàn cầu SoilGrids.
* **[cache_optimization.md](file:///d:/project/project-local/vientham/.antigravity/skills/cache_optimization.md)**: Tối ưu hóa bộ nhớ đệm Cache đưa thời gian phản hồi vệ tinh xuống dưới 30 mili-giây.

### C. Hồ sơ Dự thi & Quy trình Phát triển
* **[nasa_submission_prep.md](file:///d:/project/project-local/vientham/.antigravity/skills/nasa_submission_prep.md)**: Kỹ năng chuẩn bị hồ sơ nộp bài NASA Space Apps (7 Slide Pitch, Kịch bản Video Demo 90 giây, liên kết UN SDGs và trích dẫn khoa học).
* **[workflow.md](file:///d:/project/project-local/vientham/.antigravity/skills/workflow.md)**: Chu trình phát triển chuẩn 4 bước: **Generate ➔ Review ➔ Test ➔ Push**.

---

## 4. Bản Đồ 6 Luồng Công Việc Chi Tiết (Workflows Map)
Nằm trong thư mục `docs/workflows/` (kèm tệp tổng quan [docs/workflows/README.md](file:///d:/project/project-local/vientham/docs/workflows/README.md)):
- **[01-nasa-data-pipeline.md](file:///d:/project/project-local/vientham/docs/workflows/01-nasa-data-pipeline.md)**: Luồng 1 - Định vị nông trại & trích xuất dữ liệu vệ tinh NASA POWER.
- **[02-crop-rotation-decision-flow.md](file:///d:/project/project-local/vientham/docs/workflows/02-crop-rotation-decision-flow.md)**: Luồng 2 - Thuật toán quyết định luân canh 3 vụ thích ứng khí hậu.
- **[03-admin-data-management-flow.md](file:///d:/project/project-local/vientham/docs/workflows/03-admin-data-management-flow.md)**: Luồng 3 - Quản trị dữ liệu cây trồng PostgreSQL qua Admin & CLI.
- **[04-caching-performance-flow.md](file:///d:/project/project-local/vientham/docs/workflows/04-caching-performance-flow.md)**: Luồng 4 - Tối ưu hiệu năng & bộ nhớ đệm Cache dưới 30ms.
- **[05-testing-qa-flow.md](file:///d:/project/project-local/vientham/docs/workflows/05-testing-qa-flow.md)**: Luồng 5 - Kiểm thử tự động (Unit & Integration tests) & QA.
- **[06-nasa-submission-flow.md](file:///d:/project/project-local/vientham/docs/workflows/06-nasa-submission-flow.md)**: Luồng 6 - Chuẩn bị & đóng gói hồ sơ nộp bài NASA Space Apps.

---

## 5. Bản Đồ Tài Liệu Kỹ Thuật (Docs Cores)
Nằm trong thư mục `docs/cores/`:
- [01-database.md](file:///d:/project/project-local/vientham/docs/cores/01-database.md): Thiết kế ERD & Schema các bảng PostgreSQL (`CropCategory`, `Crop`, `SoilProfile`, `FarmLocation`).
- [02-backend.md](file:///d:/project/project-local/vientham/docs/cores/02-backend.md): Cấu trúc Django Backend, Services gọi NASA API (`nasa_service.py`) và Engine luân canh (`rotation_engine.py`).
- [03-frontend.md](file:///d:/project/project-local/vientham/docs/cores/03-frontend.md): Giao diện Django Templates + Bản đồ vệ tinh ESRI Leaflet.js + Biểu đồ Chart.js.
- [04-security.md](file:///d:/project/project-local/vientham/docs/cores/04-security.md): Cơ chế bảo mật Django CSRF, xác thực PostgreSQL, chống SQL Injection.
- [05-testing.md](file:///d:/project/project-local/vientham/docs/cores/05-testing.md): Quy chuẩn kiểm thử Django TestCase, mock dữ liệu NASA POWER.
- [06-deployment.md](file:///d:/project/project-local/vientham/docs/cores/06-deployment.md): Hướng dẫn khởi chạy cục bộ và đóng gói triển khai máy chủ.

---

## 6. Lệnh Thao Tác Nhanh (Quick Commands)
```powershell
# Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1

# Chạy server phát triển
python manage.py runserver 127.0.0.1:8000

# Tạo và chạy migrations PostgreSQL
python manage.py makemigrations
python manage.py migrate

# Nạp dữ liệu cây trồng mẫu
python manage.py seed_data

# Chạy kiểm thử tự động
python manage.py test farm_advisor
```
