# Quy Tắc Khai Thác & Xử Lý Dữ Liệu Vệ Tinh NASA (NASA Data Rules)

Tài liệu này quy định các tiêu chuẩn kỹ thuật khi làm việc với API viễn thám và dữ liệu quan sát Trái Đất của NASA trong dự án **FieldShift**.

---

## 1. Chuẩn Hóa Endpoint & Nguồn Dữ Liệu
- **Nguồn dữ liệu chính thức**: Sử dụng **NASA POWER Agroclimatology API** do NASA Langley Research Center vận hành.
- **Endpoint chuẩn**: `https://power.larc.nasa.gov/api/temporal/climatology/point`
- **Tham số bắt buộc**:
  - `community=AG`: Bắt buộc chỉ định phân hệ nông nghiệp khí hậu học.
  - `format=JSON`: Đảm bảo dữ liệu trả về theo chuẩn JSON máy đọc.
  - `parameters`: Phải bao gồm đủ các chỉ số:
    - `T2M`: Nhiệt độ trung bình ở độ cao 2m (°C).
    - `T2M_MAX`: Nhiệt độ tối đa trung bình tháng (°C).
    - `PRECTOTCORR`: Lượng mưa tích lũy hiệu chỉnh (mm/ngày).
    - `GWETTOP`: Độ ẩm tầng mặt đất (0 - 5 cm, tỷ lệ 0 - 1).
    - `GWETROOT`: Độ ẩm vùng rễ cây (0 - 100 cm, tỷ lệ 0 - 1).
    - `ALLSKY_SFC_SW_DWN`: Bức xạ mặt trời ($MJ/m^2/ngày$).

---

## 2. Quy Chuẩn Xử Lý Tọa Độ (Geographical Coordinates)
- **Định dạng**: Hệ tọa độ trắc địa quốc tế **WGS-84** (EPSG:4326), biểu diễn dưới dạng số thực thập phân (Decimal Degrees).
- **Độ chính xác**: Khi gửi yêu cầu lên API của NASA, tọa độ vĩ độ (`lat`) và kinh độ (`lon`) phải được làm tròn tối đa **4 chữ số thập phân** (đảm bảo độ phân giải thực tế khoảng 11 mét trên thực địa):
  ```python
  url = f"{BASE_URL}?longitude={longitude:.4f}&latitude={latitude:.4f}&..."
  ```
- **Phạm vi hợp lệ**:
  - Vĩ độ (`latitude`): Nằm trong khoảng `[-90.0, 90.0]`. Với Việt Nam: `[8.0, 24.0]`.
  - Kinh độ (`longitude`): Nằm trong khoảng `[-180.0, 180.0]`. Với Việt Nam: `[102.0, 110.0]`.

---

## 3. Quản Lý Thời Gian Chờ & Cơ Chế Dự Phòng (Timeout & Fallback Rules)
- **Thời gian chờ mạng (Network Timeout)**: Mọi kết nối mạng tới máy chủ NASA phải cài đặt `timeout = 12` giây để tránh tình trạng worker bị treo vĩnh viễn khi mạng quốc tế nghẽn.
- **Cơ chế Fallback bắt buộc**:
  - Nếu kết nối tới NASA bị lỗi mạng (DNS, Timeout, 502/503), hàm xử lý không bao giờ được trả về Exception làm sập giao diện web.
  - Hệ thống phải bắt ngoại lệ `try...except`, ghi log lỗi và tự động trả về bộ dữ liệu mẫu dự phòng đã được kiểm chứng (chuẩn dữ liệu vùng Nghệ An hoặc ĐBSCL) kèm cờ cảnh báo `"fallback": true`.

---

## 4. Quy Chuẩn Tính Toán Chỉ Số Nông Nghiệp Dẫn Xuất
- **Quy đổi lượng mưa**: Lượng mưa tháng được tính bằng:
  $$\text{Lượng mưa tháng (mm)} = \text{PRECTOTCORR} \times \text{Số ngày trong tháng}$$
- **Đánh giá thiếu hụt nước (Water Deficit)**: Khi bốc thoát hơi nước tiềm năng (PET) ước tính từ bức xạ và nhiệt độ lớn hơn lượng mưa rơi xuống kết hợp `GWETROOT < 0.65`, hệ thống phải tự động gán nhãn `drought_alert = True`.
