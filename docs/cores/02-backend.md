# Thiết Kế Kiến Trúc Backend & API (Backend Architecture & API Design)

Tài liệu này đặc tả kiến trúc tầng xử lý dữ liệu (Backend), các dịch vụ tích hợp dữ liệu vệ tinh NASA và đặc tả REST API nội bộ của hệ thống **FieldShift**.

---

## 1. Công Nghệ Sử Dụng (Backend Stack)
- **Runtime**: Python 3.14 (kèm môi trường ảo `venv`).
- **Web Framework**: **Django 6.1.2** (kiến trúc MVT kết hợp API endpoints).
- **Cơ sở dữ liệu & Driver**: PostgreSQL 18 với thư viện driver **psycopg 3.3.6**.
- **HTTP Client**: `requests` / `urllib.request` phục vụ gọi dữ liệu NASA POWER.

---

## 2. Cấu Trúc Thư Mục Backend

```text
vientham/
├── core/                              # Cấu hình dự án Django
│   ├── settings.py                    # Cấu hình DATABASES, APPS, STATIC, TEMPLATES
│   ├── urls.py                        # Định tuyến gốc (admin và app routes)
│   └── wsgi.py                        # Cổng giao tiếp máy chủ WSGI
├── farm_advisor/                      # Ứng dụng chính (Core App)
│   ├── models.py                      # Models PostgreSQL (Crop, Category, Soil, Location)
│   ├── views.py                       # View controllers (dashboard_view, api_analyze_farm)
│   ├── urls.py                        # Định tuyến cho farm_advisor
│   ├── admin.py                       # Cấu hình quản trị Django Admin
│   ├── services/                      # Tầng nghiệp vụ xử lý logic chuyên sâu (Services Layer)
│   │   ├── nasa_service.py            # Kết nối & xử lý dữ liệu NASA POWER API
│   │   └── rotation_engine.py         # Thuật toán luân canh cây trồng thích ứng khí hậu
│   └── management/commands/
│       └── seed_data.py               # Lệnh quản trị nạp dữ liệu mẫu ban đầu
```

---

## 3. Các Dịch Vụ Cốt Lõi (Core Services)

### 3.1 Dịch vụ Vệ tinh NASA (`nasa_service.py`)
- **Chức năng**: Gọi trực tiếp REST API từ máy chủ NASA Langley Research Center theo tọa độ (Latitude, Longitude).
- **Endpoint**: `https://power.larc.nasa.gov/api/temporal/climatology/point`
- **Các thông số thu thập**:
  - `T2M_MAX`: Nhiệt độ tối đa trung bình tháng (°C).
  - `T2M`: Nhiệt độ trung bình tháng (°C).
  - `PRECTOTCORR`: Lượng mưa tích lũy hàng ngày (mm/ngày).
  - `GWETTOP`: Độ ẩm tầng đất mặt (0 - 5 cm).
  - `GWETROOT`: Độ ẩm vùng rễ cây (0 - 100 cm).
  - `ALLSKY_SFC_SW_DWN`: Bức xạ mặt trời bề mặt ($MJ/m^2/ngày$).
- **Phân tích rủi ro tự động**:
  - Cảnh báo sốc nhiệt gió Lào nếu $T_{max} \ge 39.0^\circ C$.
  - Cảnh báo nguy cơ lũ lụt nếu Lượng mưa tháng $\ge 11.0$ mm/ngày.
  - Cảnh báo hạn hán nứt nẻ đất nếu Độ ẩm đất tầng mặt $< 0.65$.

### 3.2 Thuật toán Luân canh Thích ứng (`rotation_engine.py`)
- **Quy tắc đạm (Nitrogen Dynamics)**: Cắt đứt chuỗi rút kiệt đạm của cây lúa bằng cách đưa cây họ Đậu (Lạc/Đậu nành) vào vụ hè thu để cố định từ 45 - 60 kg N/ha tự nhiên.
- **Quy tắc rễ & Chống nén dẽ (Root Architecture)**: Luân phiên giữa rễ chùm ăn nông (Lúa) và rễ cọc đâm sâu (Lạc, Khoai lang) giúp phục hồi cấu trúc tơi xốp của đất.
- **Quy tắc né thiên tai (Climate Avoidance)**: 
  - Tránh trồng lúa trong mùa gió Lào khô hạn (Tháng 5 - 7).
  - Thu hoạch cây vụ hè thu trước tháng 9 để tránh mùa mưa bão ngập lụt.
  - Gieo trồng cây vụ đông sau đỉnh lũ tháng 10.
- **Mô hình tính điểm Soil Health Score (SHS)**: Đánh giá sự chuyển dịch từ độc canh (42 điểm) lên luân canh bền vững (89 điểm).

---

## 4. Đặc Tả REST API Nội Bộ (Internal API Specification)

### Endpoint: Phân Tích Nông Trại & Lập Kế Hoạch Luân Canh
* **URL**: `/api/analyze/`
* **Method**: `GET`
* **Query Parameters**:
  * `lat` (float, required): Vĩ độ nông trại (ví dụ: `18.9950`).
  * `lon` (float, required): Kinh độ nông trại (ví dụ: `105.4740`).
  * `goal` (string, optional): Mục tiêu chiến lược (`soil_health`, `water_saving`, `economic_balance`).

#### Cấu trúc Phản hồi Thành công (200 OK):
```json
{
  "success": true,
  "nasa": {
    "coordinates": { "lat": 18.995, "lon": 105.474 },
    "months_vn": ["Th.1", "Th.2", "Th.3", "Th.4", "Th.5", "Th.6", "Th.7", "Th.8", "Th.9", "Th.10", "Th.11", "Th.12"],
    "data": {
      "t2m_max": [31.4, 34.5, 35.1, 39.2, 40.1, 38.4, 40.9, 36.0, 34.6, 32.4, 32.3, 29.4],
      "precipitation": [1.0, 0.7, 1.4, 1.9, 4.8, 4.1, 7.0, 9.4, 12.4, 9.1, 2.6, 1.3],
      "gwet_top": [0.76, 0.73, 0.69, 0.65, 0.65, 0.66, 0.68, 0.75, 0.83, 0.85, 0.83, 0.79],
      "gwet_root": [0.74, 0.71, 0.68, 0.64, 0.63, 0.64, 0.66, 0.73, 0.82, 0.85, 0.83, 0.78]
    },
    "analysis": {
      "max_temp": 40.9,
      "max_temp_month": "JUL",
      "extreme_heat_alert": true,
      "max_rain": 12.4,
      "max_rain_month": "SEP",
      "flood_risk_alert": true,
      "min_soil_moist": 0.63,
      "drought_alert": true
    }
  },
  "plan": {
    "schedule": [
      {
        "season_name": "Vụ 1: Vụ Đông Xuân (Tháng 1 – Tháng 5)",
        "recommended_crop": "Lúa thuần chất lượng cao (Jasmine / ST24)",
        "growth_days": "105 - 115 ngày",
        "why": "Tận dụng nguồn nước đầu năm và thời tiết mát mẻ.",
        "soil_action": "Bón lót phân chuồng ủ hoai và vôi bột.",
        "icon": "🌾"
      },
      {
        "season_name": "Vụ 2: Vụ Hè Thu (Tháng 5 – Tháng 8)",
        "recommended_crop": "Lạc (Đậu phộng) Sen Thọ / L14",
        "growth_days": "80 - 90 ngày",
        "why": "Chịu nắng nóng >40°C, tiêu thụ ít nước, tự cố định 40 - 60 kg N/ha.",
        "soil_action": "Cày vùi thân lá lạc làm phân xanh tăng mùn hữu cơ.",
        "icon": "🥜"
      },
      {
        "season_name": "Vụ 3: Vụ Thu Đông (Tháng 9 – Tháng 12)",
        "recommended_crop": "Khoai lang Hoàng Long / Ngô nếp",
        "growth_days": "85 - 95 ngày",
        "why": "Gieo sau 15/10 né đỉnh lũ, chống xói mòn rửa trôi đất tầng mặt.",
        "soil_action": "Lên luống cao thoát nước.",
        "icon": "🍠"
      }
    ],
    "comparison": {
      "monoculture": { "soil_health_score": 42 },
      "crop_rotation": { "soil_health_score": 89, "water_saved_percent": "50.3%" }
    }
  }
}
```
