# Kỹ Năng Thiết Kế Giao Diện Nông Nghiệp Công Nghệ Cao (Agritech UI/UX Design Skill)

Tài liệu này là cẩm nang thiết kế giao diện (Design System & UX Guidelines) chuyên sâu cho dự án **FieldShift**, kết hợp giữa tính thẩm mỹ không gian hiện đại của **NASA** và tính thân thiện, dễ sử dụng cho **Nông dân & Chuyên gia nông nghiệp**.

---

## 1. Triết Lý Thiết Kế: "Space-Tech Meets Soil" (Vũ Trụ Gặp Đất Mẹ)
- **Không dùng giao diện màu sắc cơ bản/đơn điệu** (xanh lá cậy thô, đỏ tươi, trắng chói).
- **Phối màu tinh tế (Tailored Palette)**: Lấy cảm hứng từ góc nhìn Trái Đất từ vệ tinh: nền không gian tối sâu (Midnight Space), điểm nhấn xanh ngọc lục bảo (Emerald Green của thảm thực vật) và xanh khí quyển (Atmospheric Blue).
- **Độ tương phản cao & Dễ đọc ngoài trời**: Nông dân thường xem web trên điện thoại ngoài trời nắng, do đó phông chữ phải to rõ, độ tương phản văn bản đạt chuẩn **WCAG AAA**.

---

## 2. Hệ Thống Màu Sắc Chuẩn (Color Tokens)

```css
:root {
    /* Nền & Thẻ Kính Mờ (Glassmorphism) */
    --bg-main: #0b1120;                /* Xanh đen không gian sâu */
    --bg-card: rgba(30, 41, 59, 0.7);   /* Kính mờ phủ nền */
    --bg-card-hover: rgba(51, 65, 85, 0.85);
    --border-subtle: rgba(255, 255, 255, 0.08);
    --border-focus: rgba(16, 185, 129, 0.4);

    /* Màu Nhận Diện Nông Nghiệp Thông Minh */
    --primary-emerald: #10b981;        /* Xanh lục bảo chủ đạo (Sinh trưởng, Phục hồi đất) */
    --primary-light: #34d399;          /* Xanh ngọc phát sáng cho Badge & Highlights */
    --primary-dark: #059669;           /* Xanh đậm cho nút bấm */

    /* Màu Dữ Liệu Thời Tiết & Cảnh Báo */
    --accent-sky: #38bdf8;             /* Lượng mưa, nước tưới, vệ tinh */
    --accent-amber: #f59e0b;           /* Cảnh báo khô hạn, độ ẩm thấp */
    --accent-rose: #f43f5e;            /* Cảnh báo nắng nóng cực đoan >40°C, rủi ro ngập lũ */

    /* Kiểu Chữ (Typography) */
    --text-pure: #ffffff;              /* Tiêu đề & Chỉ số KPI */
    --text-muted: #94a3b8;             /* Nhãn & Mô tả phụ */
}
```

---

## 3. Quy Chuẩn Thành Phần Giao Diện (Component Guidelines)

### 3.1 Thẻ Chỉ Số KPI Thời Tiết (Metric Cards)
* **Cấu trúc**: Icon nổi bật bên góc $\rightarrow$ Nhãn danh mục (chữ hoa nhỏ 11px) $\rightarrow$ Con số đo lường cỡ lớn (28–32px, font Space Grotesk) $\rightarrow$ Đơn vị đo $\rightarrow$ Dòng trạng thái đánh giá nhanh (ví dụ: *"Báo động gió Lào"*).
* **Đường viền trạng thái (Status Accent Border)**: Thẻ cảnh báo nắng nóng có dải viền trái màu đỏ hồng (`--accent-rose`), thẻ phục hồi đạm có dải viền xanh (`--primary-emerald`).

### 3.2 Bản Đồ Vệ Tinh Trực Quan (Leaflet GIS Map)
* **Lớp bản đồ**: Sử dụng **ESRI World Imagery** để người dùng nhìn thấy từng thửa ruộng thật từ ảnh vệ tinh, phủ thêm lớp ranh giới địa danh và đường giao thông trong suốt.
* **Marker tương tác**: Con trỏ vị trí có hiệu ứng đập mạch nhẹ (Pulse Animation) giúp người dùng định vị chính xác vị trí đang phân tích.
* **Tích hợp nút thao tác nhanh**: Cung cấp danh sách nút bấm Preset (Nghệ An, Bến Tre, Tây Nguyên) để người dùng có thể chuyển vùng chỉ với 1 click.

### 3.3 Trực Quan Hóa Biểu Đồ (Chart.js UX)
* **Biểu đồ thời tiết**: Kết hợp đồng bộ giữa **Cột (Bar)** cho lượng mưa và **Đường cong mượt (Smooth Line tension 0.35)** cho nhiệt độ cực đại.
* **Biểu đồ độ ẩm đất**: Sử dụng dải diện tích có màu chuyển sắc (Gradient Fill) thể hiện trực quan mức độ khô nẻ của đất tầng mặt từ tháng 1 đến tháng 12.
* **Tooltip**: Hiển thị đầy đủ tiếng Việt kèm ngữ cảnh (ví dụ: *"Tháng 7: 40.88°C - Gió Lào cực đoan"*).

### 3.4 Thẻ Lịch Luân Canh 3 Vụ (Timeline Season Cards)
* Mỗi vụ mùa được đóng gói trong một thẻ riêng biệt có Icon đại diện (🌾 Lúa, 🥜 Lạc, 🍠 Khoai).
* **Vụ trọng tâm thích ứng khí hậu (Vụ 2)** phải có khung phát sáng nhẹ (`box-shadow: 0 0 15px rgba(16,185,129,0.2)`) để thu hút mắt người nhìn đầu tiên.
* Phân tách rõ ràng: **Tên giống cây** ➔ **Thời gian ngày** ➔ **Lý do khoa học** ➔ **Hành động cải tạo đất**.

---

## 4. Thiết Kế Đáp Ứng Thiết Bị (Responsive & Mobile-First)
* **Màn hình máy tính (Desktop $\ge$ 1024px)**: Chia cột tỷ lệ vàng `380px` (bộ điều khiển & bản đồ) : `1fr` (dashboard kết quả).
* **Màn hình di động & Máy tính bảng (Mobile / Tablet < 1024px)**:
  * Tự động xếp chồng thành 1 cột duy nhất.
  * Bản đồ thu gọn độ cao xuống `240px` để tiết kiệm không gian lướt tay.
  * Các thẻ KPI tự động co giãn từ 4 cột sang lưới 2x2.
  * Nút bấm hành động có chiều cao tối thiểu `48px` để ngón tay dễ bấm khi ở ngoài đồng ruộng.
