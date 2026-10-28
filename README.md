# 🌾 FieldShift: Thích Ứng Nông Trại Với Dữ Liệu Vệ Tinh NASA 🛰️

> **Dự án tham gia cuộc thi NASA Space Apps Challenge**  
> **Thử thách:** *Field Shift: Adapting Farms with NASA Data*  
> **Nền tảng:** Python Django MVT • PostgreSQL 18 • NASA POWER API • Leaflet.js • Chart.js  

---

## 📖 Giới Thiệu Dự Án

Biến đổi khí hậu đang tạo ra những cú sốc thời tiết cực đoan đối với người nông dân: nắng nóng gay gắt do gió Lào (>40°C), hạn hán làm khô nứt đồng ruộng, và mưa lũ dồn dập gây ngập úng. Thói quen độc canh thâm canh lúa 3 vụ/năm đang khiến đất đai kiệt quệ dinh dưỡng, mất dần hàm lượng mùn hữu cơ và phụ thuộc nặng nề vào phân bón hóa học.

**FieldShift** là một Hệ thống Hỗ trợ Ra Quyết định (Decision Support System - DSS) biến nguồn dữ liệu viễn thám mở của NASA thành công cụ trực quan hóa giúp người nông dân:
1. **Lắng nghe nhịp điệu khí hậu từ vũ trụ:** Truy xuất dữ liệu nhiệt độ cực đại, lượng mưa tích lũy và độ ẩm đất thực tế từ vệ tinh NASA POWER.
2. **Chẩn đoán rủi ro mùa vụ:** Phát hiện thời điểm nắng hạn khốc liệt và mùa bão lũ để chủ động ứng phó.
3. **Đề xuất chiến lược luân canh thích ứng:** Thay thế vụ lúa hè thu bằng cây họ đậu chịu hạn (Lạc Sen Thọ / L14, Mè đen) giúp tiết kiệm 50% nước tưới và nạp tự nhiên **+52 kg N/ha** vào đất nhờ vi khuẩn nốt sần.
4. **Mô phỏng sức khỏe đất:** Đo lường sự khác biệt rõ rệt giữa độc canh lúa (42/100 điểm) và luân canh thông minh (89/100 điểm).

---

## 🏛️ Kiến Trúc Hệ Thống (Django MVT)

Toàn bộ ứng dụng được xây dựng theo mô hình **MVT (Model - View - Template)** khép kín, gọn gàng, không phân mảnh:

```text
vientham/
├── core/                              # Cấu hình dự án Django (settings, urls, wsgi)
├── farm_advisor/                      # Phân hệ nghiệp vụ chính
│   ├── models.py                      # Models PostgreSQL (Crop, CropCategory, SoilProfile, FarmLocation)
│   ├── views.py                       # Controllers điều hướng & API endpoint (/api/analyze/)
│   ├── urls.py                        # Định tuyến URL
│   ├── admin.py                       # Đăng ký giao diện quản trị Django Admin
│   ├── services/
│   │   ├── nasa_service.py            # Kết nối & trích xuất NASA POWER Agroclimatology API
│   │   └── rotation_engine.py         # Thuật toán ma trận luân canh & tính điểm đất SHS
│   └── management/commands/
│       └── seed_data.py               # Nạp dữ liệu cây trồng và thổ nhưỡng mẫu
├── templates/                         # Giao diện người dùng HTML5
│   ├── base.html                      # Layout khung chuẩn, thanh điều hướng, CDN thư viện
│   └── dashboard.html                 # Màn hình Dashboard tương tác chính
├── static/                            # Tài nguyên tĩnh
│   └── css/style.css                  # Giao diện nông nghiệp hiện đại, Glassmorphism
├── AIgent/                            # Hệ thống tài liệu kỹ thuật & tiêu chuẩn dự án
└── requirements.txt                   # Danh sách thư viện Python
```

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Cục Bộ (Quickstart)

### 1. Yêu cầu hệ thống
* Python 3.12+ (đã kiểm thử mượt mà trên Python 3.14).
* Node.js 18+ (LTS v20+ khuyến nghị).
* PostgreSQL 18 (Cơ sở dữ liệu `remote_sensing` trên cổng 5432).

### 2. Khởi tạo môi trường & cài đặt thư viện
```powershell
# Di chuyển vào thư mục dự án
cd d:\project\project-local\vientham

# Kích hoạt môi trường ảo Python & cài đặt backend dependencies
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Cài đặt root dependencies (concurrently) & frontend dependencies
npm install
npm --prefix frontend install
```

### 3. Cấu hình Cơ sở dữ liệu & Chạy Migrations
Hệ thống kết nối trực tiếp cơ sở dữ liệu `remote_sensing` trên PostgreSQL:
```powershell
# Chạy migration
python manage.py migrate

# Nạp dữ liệu cây trồng mẫu
python manage.py seed_data
```

### 4. Khởi chạy toàn bộ hệ thống bằng 1 lệnh duy nhất
```powershell
npm run dev
```
*(Lệnh này tự động kích hoạt song song cả Django Backend API `127.0.0.1:8000` và Next.js Frontend `localhost:3000`)*.

Truy cập trình duyệt tại:
* 🌾 **Next.js Agritech Dashboard:** [http://localhost:3000/](http://localhost:3000/)
* 📡 **Django REST API:** [http://127.0.0.1:8000/api/analyze/](http://127.0.0.1:8000/api/analyze/)
* ⚙️ **Trang Quản trị Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)  
  *(Tài khoản: `admin` / Mật khẩu: `170106`)*

---

## 🛰️ Dữ Liệu Vệ Tinh NASA Sử Dụng

Dự án khai thác trực tiếp từ **NASA Langley Research Center** thông qua **NASA POWER API** (miễn phí, không cần API Key):
* **`T2M_MAX`**: Nhiệt độ tối đa ở độ cao 2m (°C) — Cảnh báo sốc nhiệt gió Lào.
* **`PRECTOTCORR`**: Lượng mưa tích lũy điều chỉnh (mm/ngày) — Cảnh báo khô hạn & lũ lụt.
* **`GWETTOP`**: Độ ẩm bề mặt đất (0 - 5 cm) — Đánh giá bốc thoát hơi nước tầng mặt.
* **`GWETROOT`**: Độ ẩm vùng rễ cây (0 - 100 cm) — Đánh giá khả năng cấp nước cho rễ.

---

## 📜 Giấy Phép & Ghi Nhận
* Dự án phát triển phục vụ cuộc thi **NASA Space Apps Challenge 2026**.
* Mã nguồn mở theo giấy phép MIT.
