# Đặc Tả Yêu Cầu Phần Mềm (Software Requirements Specification - SRS)

**Dự án**: **FieldShift — Thích Ứng Nông Trại Với Dữ Liệu Vệ Tinh NASA**  
*(Field Shift: Adapting Farms with NASA Data — NASA Space Apps Challenge)*  
**Phiên bản**: 1.0.0  
**Tác giả**: Đội ngũ phát triển FieldShift  

---

## 1. Giới thiệu (Introduction)

### 1.1 Mục đích (Purpose)
Tài liệu này đặc tả toàn bộ các yêu cầu nghiệp vụ, chức năng và phi chức năng cho hệ thống **FieldShift**. Đây là một **Hệ thống Hỗ trợ Ra Quyết định (Decision Support System - DSS)** ứng dụng dữ liệu quan sát Trái Đất (Earth Observations) của NASA nhằm giải quyết bài toán suy thoái đất, thiếu hụt nguồn nước, nắng nóng cực đoan (gió Lào) và bão lũ thất thường trong canh tác nông nghiệp.

### 1.2 Phạm vi Sản phẩm (Product Scope)
* **Trong phạm vi (In-Scope)**:
  * Tích hợp dữ liệu khí hậu và viễn thám thực tế từ **NASA POWER API (Agroclimatology & MERRA-2)**: Nhiệt độ bề mặt (T2M, T2M_MAX), Lượng mưa tích lũy (PRECTOTCORR), Độ ẩm đất tầng mặt (GWETTOP) và Độ ẩm vùng rễ cây (GWETROOT).
  * Xây dựng bản đồ vệ tinh tương tác (Interactive Satellite Map với ESRI World Imagery) cho phép nông dân nhấp chọn vị trí thửa ruộng hoặc chọn nhanh vùng trọng điểm (Nghệ An, Bến Tre, Tây Nguyên).
  * Xây dựng công cụ phân tích rủi ro khí hậu mùa vụ và thuật toán đề xuất **Chiến lược Luân canh Cây trồng 3 Vụ Thích ứng (3-Season Adaptive Crop Rotation Engine)**.
  * Tính toán và so sánh **Chỉ số Sức khỏe Đất (Soil Health Score - SHS)** giữa phương thức Độc canh truyền thống (Monoculture 3 vụ lúa) và Phương thức Luân canh Thích ứng (Lúa ➔ Cây họ đậu cố định đạm ➔ Cây lấy củ/màu che phủ đất).
  * Cung cấp giao diện quản trị Django Admin cho phép chuyên gia nông nghiệp thêm mới, cập nhật hồ sơ các giống cây trồng và loại thổ nhưỡng.
* **Ngoài phạm vi (Out-of-Scope giai đoạn 1)**:
  * Chưa kết nối trực tiếp thiết bị cảm biến IoT tại ruộng (sử dụng 100% dữ liệu viễn thám vệ tinh NASA).
  * Chưa tích hợp cổng thương mại điện tử mua bán nông sản.

### 1.3 Thuật ngữ & Viết tắt (Definitions & Acronyms)
* **DSS (Decision Support System)**: Hệ thống hỗ trợ ra quyết định.
* **NASA POWER**: Prediction Of Worldwide Energy Resources (Bộ dữ liệu vệ tinh khí hậu nông nghiệp của NASA).
* **GWETTOP**: Surface Soil Wetness (Chỉ số độ ẩm đất tầng mặt 0–5 cm, thang đo 0–1).
* **GWETROOT**: Root Zone Soil Wetness (Chỉ số độ ẩm đất tầng rễ cây 0–100 cm, thang đo 0–1).
* **PRECTOTCORR**: Precipitation Corrected (Lượng mưa thực tế đo bằng vệ tinh mm/ngày).
* **SHS (Soil Health Score)**: Điểm đánh giá sức khỏe và độ phì nhiêu của đất (thang điểm 0–100).
* **Legumes**: Cây họ đậu có nốt sần chứa vi khuẩn Rhizobium có khả năng tự cố định đạm từ khí quyển.

---

## 2. Mô tả Tổng quan (Overall Description)

### 2.1 Bối cảnh Hệ thống (Product Perspective)
FieldShift hoạt động theo mô hình Web Application khép kín **Django MVT** kết nối cơ sở dữ liệu **PostgreSQL 18**:
* Phía Client giao tiếp qua REST API nội bộ `/api/analyze/`.
* Phía Backend kết nối trực tiếp tới máy chủ dữ liệu của **NASA Langley Research Center** qua NASA POWER REST API để lấy số liệu khí hậu theo tọa độ thực tế.
* Hệ thống lưu trữ danh mục cây trồng, thổ nhưỡng và lịch sử nông trại trong cơ sở dữ liệu PostgreSQL.

### 2.2 Tác nhân & Đối tượng Sử dụng (User Classes)
* **Nông dân & Hợp tác xã (Farmers & Cooperatives)**: Người dùng trực tiếp, cần giao diện trực quan, dễ hiểu, xem được ngay rủi ro thời tiết và lịch luân canh cụ thể từng tháng để gieo trồng đúng thời vụ.
* **Cán bộ Khuyến nông & Chuyên gia Nông nghiệp (Agronomists)**: Sử dụng trang Admin để bổ sung đặc tính giống cây mới, cập nhật ngưỡng chịu nhiệt, nhu cầu nước và hiệu quả cố định đạm.
* **Ban giám khảo & Cộng đồng NASA Space Apps (Judges & Researchers)**: Đánh giá tính khoa học, độ tin cậy của dữ liệu viễn thám NASA và tác động thực tiễn đến việc chống biến đổi khí hậu.

### 2.3 Ràng buộc & Phụ thuộc (Constraints & Dependencies)
* **Ràng buộc**: Ngôn ngữ backend Python 3.14+, Django 6.x, cơ sở dữ liệu PostgreSQL 18.
* **Phụ thuộc**: Tính sẵn sàng của NASA POWER API Server (`power.larc.nasa.gov`). Trong trường hợp mạng chập chờn, hệ thống có cơ chế Fallback sử dụng bộ dữ liệu viễn thám mẫu đã được kiểm chứng cho vùng Nghệ An.

---

## 3. Yêu cầu Giao diện Ngoại vi (External Interface Requirements)

### 3.1 Giao diện Người dùng (User Interface)
* Giao diện phong cách **Modern Agricultural Tech & Glassmorphism**: Tone màu chủ đạo Emerald Green (`#10b981`), Midnight Blue (`#0b1120`), Dark Slate (`#1e293b`).
* Font chữ chuẩn quốc tế: *Plus Jakarta Sans* & *Space Grotesk*.
* Bản đồ số vệ tinh Leaflet.js sử dụng lớp ảnh **ESRI World Imagery** độ phân giải cao kết hợp nhãn địa danh đường bộ.
* Biểu đồ trực quan hóa dữ liệu bằng **Chart.js**: Biểu đồ kết hợp cột lượng mưa và đường nhiệt độ; biểu đồ miền độ ẩm tầng mặt và độ ẩm tầng rễ 12 tháng.

### 3.2 Giao diện Phần mềm & API (Software & API Interfaces)
* **NASA POWER Agroclimatology API**:
  * Endpoint: `https://power.larc.nasa.gov/api/temporal/climatology/point`
  * Tham số: `T2M,T2M_MAX,PRECTOTCORR,GWETTOP,GWETROOT,ALLSKY_SFC_SW_DWN`.
* **ESRI ArcGIS World Imagery Tile Service**:
  * Cung cấp bản đồ ảnh vệ tinh bề mặt Trái Đất theo chuẩn XYZ Tiles.

---

## 4. Yêu cầu Chức năng (Functional Requirements)

### 4.1 Phân hệ Bản đồ & Định vị Nông trại (Farm Location & Mapping)
* `[US-MAP-01]`: Người dùng có thể bấm chọn nhanh các vùng thí điểm trọng điểm (Nghệ An, Bến Tre, Đắk Lắk).
* `[US-MAP-02]`: Người dùng có thể nhấp chuột vào bất kỳ vị trí nào trên bản đồ ảnh vệ tinh để ghim tọa độ thửa ruộng của mình.
* `[US-MAP-03]`: Người dùng có thể tự nhập trực tiếp tọa độ Vĩ độ (Latitude) và Kinh độ (Longitude) dạng số thập phân.

### 4.2 Phân hệ Khai thác Dữ liệu Vệ tinh NASA (NASA Data Fetching)
* `[US-NASA-01]`: Hệ thống tự động gửi yêu cầu API lên máy chủ NASA POWER theo tọa độ người dùng đã chọn.
* `[US-NASA-02]`: Hệ thống trích xuất và hiển thị 4 thẻ chỉ số thời tiết trọng yếu: Nhiệt độ đỉnh ($T_{max}$), Lượng mưa cực đại tháng lũ, Độ ẩm đất thấp nhất tháng hạn, Lượng đạm sinh học tự sinh.
* `[US-NASA-03]`: Hệ thống vẽ biểu đồ diễn biến 12 tháng về nhiệt độ, lượng mưa và độ ẩm đất tầng mặt/tầng rễ.

### 4.3 Phân hệ Thuật toán Luân canh Thích ứng (Decision Support Engine)
* `[US-DSS-01]`: Hệ thống nhận diện các cú sốc khí hậu (ví dụ: Gió Lào nắng nóng >40°C tháng 5–7, bão lũ ngập úng tháng 9–10 tại Nghệ An).
* `[US-DSS-02]`: Hệ thống tự động lập lịch trình luân canh 3 vụ/năm:
  * Vụ 1 (Đông Xuân): Lúa chất lượng cao (nhiệt độ mát, đủ nước).
  * Vụ 2 (Hè Thu): Thay thế lúa bằng cây họ đậu chịu hạn (Lạc Sen Thọ / Mè đen) để né gió Lào và tích lũy đạm tự nhiên.
  * Vụ 3 (Thu Đông): Cây lấy củ/màu (Khoai lang, Ngô) trồng sau lũ để chống rửa trôi đất tầng mặt.
* `[US-DSS-03]`: Cho phép nông dân lựa chọn mục tiêu chiến lược: *Cải tạo đất & Bổ sung đạm* / *Tiết kiệm nước & Chống hạn* / *Cân bằng kinh tế*.

### 4.4 Phân hệ Đánh giá & Mô phỏng Sức khỏe Đất (Soil Health Impact)
* `[US-SOIL-01]`: Tính toán điểm số sức khỏe đất (Soil Health Score: 0 - 100) cho phương án Độc canh và Luân canh.
* `[US-SOIL-02]`: Ước tính lượng nước tưới tiết kiệm được (%) khi chuyển đổi cơ cấu cây trồng mùa khô.
* `[US-SOIL-03]`: Ước tính hàm lượng phân đạm sinh học bổ sung tự nhiên vào đất (+52 kg N/ha) và chi phí phân bón tiết kiệm được.

### 4.5 Phân hệ Quản trị Dữ liệu Nông nghiệp (Admin CMS)
* `[US-ADM-01]`: Quản trị viên có thể truy cập `/admin` để quản lý các nhóm cây trồng (Ngũ cốc, Cây họ đậu, Cây có dầu, Cây lấy củ).
* `[US-ADM-02]`: Quản trị viên có thể thêm giống cây mới với các chỉ số sinh học: thời gian sinh trưởng, độ sâu rễ, ngưỡng nhiệt độ tối đa, nhu cầu nước.

---

## 5. Yêu cầu Phi chức năng (Non-functional Requirements)

### 5.1 Hiệu năng (Performance)
* Thời gian phản hồi API phân tích nông trại và tải dữ liệu NASA trung bình dưới **3.5 giây**.
* Bản đồ và biểu đồ hiển thị mượt mà trên trình duyệt với tần số quét 60 FPS.

### 5.2 Độ tin cậy (Reliability & Availability)
* Tích hợp cơ chế Fallback tự động khi đường truyền quốc tế đến máy chủ NASA bị gián đoạn, đảm bảo ứng dụng không bị crash.
* Dữ liệu cây trồng và cấu hình nông trại được lưu trữ bền vững trong cơ sở dữ liệu PostgreSQL 18.

### 5.3 Bảo mật (Security)
* Sử dụng Django CSRF Protection cho các form và API POST.
* Phân quyền quản trị thông qua Django Authentication & Permissions.
* Mọi tham số truy vấn cơ sở dữ liệu đều thông qua Django ORM để triệt tiêu lỗ hổng SQL Injection.
