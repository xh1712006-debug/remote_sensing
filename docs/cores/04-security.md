# Thiết Kế Xác Thực & An Toàn Bảo Mật (Security & Authentication Design)

Tài liệu này đặc tả các cơ chế bảo mật, phân quyền và bảo vệ dữ liệu trong hệ thống **FieldShift** nhằm đáp ứng các tiêu chuẩn bảo mật theo khuyến nghị OWASP.

---

## 1. Cơ Chế Xác Thực & Phân Quyền (Authentication & RBAC)

Hệ thống sử dụng cơ chế bảo mật tích hợp sẵn của **Django Authentication Framework**:
- **Băm mật khẩu (Password Hashing)**: Sử dụng thuật toán chuẩn `PBKDF2` kết hợp `SHA-256` với muối (salt) ngẫu nhiên, tự động nâng cấp độ phức tạp theo chuẩn quốc tế.
- **Phân quyền Quản trị (Admin Access)**:
  - Chỉ tài khoản có cờ `is_staff = True` và `is_superuser = True` mới có quyền truy cập vào cổng quản trị cơ sở dữ liệu cây trồng `/admin/`.
  - Phân quyền theo mô hình nhóm người dùng (Groups) và quyền chi tiết (Permissions: `add_crop`, `change_crop`, `delete_crop`).

---

## 2. Phòng Chống Các Lỗ Hổng Web Cốt Lõi (OWASP Top 10)

### 2.1 Phòng chống SQL Injection
- Toàn bộ các thao tác đọc và ghi dữ liệu vào PostgreSQL 18 đều thông qua **Django ORM** (`Crop.objects.all()`, `FarmLocation.objects.get()`).
- Django ORM tự động tham số hóa (Parameterized queries) mọi tham số đầu vào từ người dùng, triệt tiêu hoàn toàn nguy cơ chèn mã độc SQL.

### 2.2 Phòng chống Tấn công CSRF (Cross-Site Request Forgery)
- Hệ thống kích hoạt middleware `django.middleware.csrf.CsrfViewMiddleware`.
- Mọi form gửi dữ liệu hoặc yêu cầu POST đều bắt buộc phải đính kèm thẻ `{% csrf_token %}` hoặc Header `X-CSRFToken`.

### 2.3 Phòng chống Tấn công XSS (Cross-Site Scripting)
- Công cụ hiển thị giao diện **Django Template Engine** mặc định tự động mã hóa ký tự HTML (Auto-escaping: biến `<` thành `&lt;`, `>` thành `&gt;`).
- Mọi dữ liệu JSON trả về từ API đều được định kiểu `application/json` và lọc sạch dữ liệu độc hại trước khi đưa vào DOM.

### 2.4 An toàn Kết nối Dữ liệu Ngoại vi (NASA API Security)
- Kết nối tới máy chủ NASA POWER bắt buộc chạy trên giao thức **HTTPS mã hóa (TLS 1.3)**: `https://power.larc.nasa.gov/`.
- Thiết lập giới hạn thời gian chờ (`timeout=12s`) trong lời gọi mạng để ngăn chặn hiện tượng treo worker / Denial of Service khi đường truyền quốc tế gặp sự cố.

---

## 3. Quản Lý Thông Tin Nhạy Cảm (Secrets Management)
- Thông tin nhạy cảm (Secret Key, Mật khẩu PostgreSQL) khi đưa lên môi trường Production bắt buộc phải đọc từ biến môi trường của hệ thống (`os.environ.get(...)`) hoặc file `.env`.
- Tệp `.env` đã được cấu hình trong `.gitignore` để không bao giờ bị lộ lên kho lưu trữ mã nguồn GitHub.
