# Thiết Kế Kiến Trúc Frontend & UI/UX (Frontend Architecture & UI/UX Design)

Tài liệu này đặc tả thiết kế giao diện (UI/UX) và kiến trúc ứng dụng phía Client của hệ thống **FieldShift**.

---

## 1. Công Nghệ Sử Dụng (Frontend Stack)
- **Engine giao diện**: **Django Templates (HTML5)** theo chuẩn MVT, kế thừa qua `base.html` và `dashboard.html`.
- **Styling**: **Vanilla CSS3** hiện đại, sử dụng hệ thống biến CSS (CSS Custom Properties), hiệu ứng **Glassmorphism**, và bố cục Flexbox/CSS Grid.
- **Bản đồ vệ tinh**: **Leaflet.js 1.9.4** kết hợp lớp bản đồ vệ tinh độ phân giải cao **ESRI World Imagery** và lớp nhãn địa danh đường bộ trong suốt.
- **Trực quan hóa dữ liệu**: **Chart.js 4.x** (vẽ biểu đồ đa trục kết hợp Cột/Đường và biểu đồ diện tích độ ẩm đất).
- **Phông chữ & Biểu tượng**: Google Fonts (*Plus Jakarta Sans* & *Space Grotesk*), FontAwesome 6.5.

---

## 2. Hệ Thống Thiết Kế (Design System & Theme)

### Bảng màu chủ đạo (Color Palette):
```css
:root {
    --bg-main: #0b1120;             /* Nền không gian tối sâu */
    --bg-card: rgba(30, 41, 59, 0.7);/* Thẻ kính mờ Glassmorphism */
    --primary: #10b981;             /* Xanh ngọc lục bảo (Emerald Green - Nông nghiệp) */
    --primary-light: #34d399;       /* Xanh ngọc sáng */
    --accent-blue: #38bdf8;         /* Xanh dương vệ tinh & lượng mưa */
    --accent-amber: #f59e0b;        /* Vàng hổ phách cảnh báo khô hạn */
    --accent-rose: #f43f5e;         /* Đỏ hồng nhiệt độ cực đoan & rủi ro */
    --text-primary: #f8fafc;        /* Chữ trắng sáng */
    --text-secondary: #94a3b8;      /* Chữ xám bạc */
}
```

---

## 3. Bố Cục Giao Diện Người Dùng (UI Layout)

```text
┌────────────────────────────────────────────────────────────────────────┐
│  🛰️ FieldShift | NASA Space Apps          ● NASA API: Connected   [Admin]│
├────────────────────────────────────────────────────────────────────────┤
│  🌾 Hero Banner: Tóm tắt đề tài & Tác động của Dữ liệu Vệ tinh         │
├──────────────────────────────────┬─────────────────────────────────────┤
│  [CỘT ĐIỀU KHIỂN & BẢN ĐỒ]       │  [CỘT PHÂN TÍCH & KẾ HOẠCH VỤ MÙA] │
│                                  │                                     │
│  - Chọn nhanh: [Nghệ An] [Bến Tre]│  - 4 Thẻ KPI: Tmax | Mưa | Ẩm đất | Đạm│
│  - Bản đồ vệ tinh ESRI Leaflet    │  - Chart 1: Nhiệt độ & Lượng mưa 12T│
│  - Tọa độ Lat / Lng              │  - Chart 2: Độ ẩm tầng mặt & tầng rễ│
│  - Mục tiêu: Cải tạo đất / Hạn... │  - Timeline 3 Vụ Luân Canh Thích Ứng│
│  - [Nút: Phân Tích NASA]          │  - Bảng So Sánh: Độc Canh vs Luân Canh│
└──────────────────────────────────┴─────────────────────────────────────┘
```

---

## 4. Tương Tác Bản Đồ & Vẽ Biểu Đồ Động (Client-Side Logic)

### Tương tác Bản đồ (Leaflet.js):
- Khi người dùng click chuột vào bất kỳ vị trí nào trên bản đồ hoặc kéo thả Marker:
  1. Tự động cập nhật 2 ô nhập liệu `input-lat` và `input-lon`.
  2. Bấm nút hoặc chọn Preset sẽ tự động gửi yêu cầu ngầm AJAX `fetch('/api/analyze/?lat=...&lon=...')`.
  3. Hiển thị hiệu ứng tải dữ liệu (Loading Spinner).

### Trực quan hóa Biểu đồ (Chart.js):
1. **Biểu đồ Thời tiết (Weather Chart)**:
   - Trục trái: Đường cong nhiệt độ tối đa `T2M_MAX` (°C) màu đỏ hồng.
   - Trục phải: Cột lượng mưa tích lũy `PRECTOTCORR` (mm/ngày) màu xanh dương.
2. **Biểu đồ Độ ẩm Đất (Soil Moisture Chart)**:
   - Vùng phủ màu xanh lá: Độ ẩm đất tầng mặt `GWETTOP` (0 - 5cm).
   - Đường nét đứt màu vàng: Độ ẩm đất tầng rễ cây `GWETROOT` (0 - 100cm).
