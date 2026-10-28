# Kỹ Năng Chuẩn Bị Hồ Sơ Nộp Bài NASA Space Apps (NASA Submission Prep Skill)

Kỹ năng này hướng dẫn toàn bộ quy trình chuẩn bị hồ sơ dự thi **NASA Space Apps Challenge** theo chuẩn chấm điểm cao nhất của ban giám khảo quốc tế.

---

## 1. Dàn Ý Bộ Slide Thuyết Trình (7-Slide Pitch Deck Standard)

NASA Space Apps giới hạn bài thuyết trình trong **tối đa 7 trang slide** định dạng PDF.

| Trang (Slide) | Tiêu đề | Nội dung cốt lõi & Hình ảnh minh họa |
| :---: | :--- | :--- |
| **Slide 1** | **Trang Bìa (Title & Hook)** | • Tên dự án: **FieldShift**.<br>• Thông điệp: *"Adapting Farms with NASA Earth Observations for Resilient Soils"*.<br>• Tên nhóm & Thành phố tham dự. |
| **Slide 2** | **Vấn Đề (The Climate Crisis on Farms)** | • Nông dân đối mặt "khủng hoảng kép": Gió Lào nắng nóng >40°C và Mưa bão ngập lụt dồn dập.<br>• Thói quen độc canh 3 vụ lúa làm kiệt quệ đạm hữu cơ và chai cứng đất tầng mặt. |
| **Slide 3** | **Giải Pháp (The FieldShift Solution)** | • Hệ thống Hỗ trợ Ra Quyết định (DSS) biến dữ liệu vệ tinh NASA thành lịch luân canh vụ mùa thân thiện với nông dân.<br>• Sơ đồ kiến trúc Django MVT + PostgreSQL. |
| **Slide 4** | **Khai Thác Dữ Liệu NASA (How We Use NASA Data)** | • **NASA POWER Agroclimatology & MERRA-2**: `T2M_MAX` (phát hiện sốc nhiệt), `PRECTOTCORR` (lượng mưa bão), `GWETTOP` & `GWETROOT` (độ ẩm đất tầng mặt và tầng rễ).<br>• Dẫn chứng dữ liệu thực tế tại Nghệ An & ĐBSCL. |
| **Slide 5** | **Trình Diễn Sản Phẩm (Product Demo)** | • Ảnh chụp màn hình giao diện Dashboard: Bản đồ vệ tinh tương tác ESRI, biểu đồ khí hậu Chart.js và lộ trình 3 vụ luân canh thích ứng. |
| **Slide 6** | **Tác Động Xã Hội & Mục Tiêu Bền Vững (Impact & UN SDGs)** | • Giảm 50.3% lượng nước tưới mùa khô.<br>• Bổ sung +52 kg Đạm sinh học/ha nhờ cây họ đậu.<br>• Giảm 55% chi phí phân bón hóa học.<br>• Đóng góp vào UN SDG 2 (Xóa đói), SDG 13 (Khí hậu), SDG 15 (Bảo vệ đất). |
| **Slide 7** | **Tương Lai & Đội Ngũ (Roadmap & Team)** | • Kế hoạch mở rộng: Tích hợp ảnh vệ tinh Landsat NDVI và mở rộng toàn quốc.<br>• Giới thiệu thành viên nhóm & Lời cảm ơn. |

---

## 2. Kịch Bản Video Demo 90 Giây (90-Second Demo Video Script)

Video demo là tiêu chí bắt buộc (dưới 2 phút, khuyên dùng từ 60–90 giây):

* **00:00 – 00:15 (Phần Mở Đầu - Hook)**:  
  * *Lời thoại*: "Tại miền Trung Việt Nam, nắng nóng gió Lào vượt ngưỡng 40°C thiêu rụi các cánh đồng lúa hè thu, để rồi chỉ 2 tháng sau, bão lũ ngập úng lại quét sạch mùa màng. Đất đai đang kêu cứu vì độc canh cạn kiệt đạm."
  * *Hình ảnh*: Ảnh tư liệu cánh đồng nứt nẻ và giao diện vũ trụ của NASA.
* **00:15 – 00:45 (Trực Tiếp Thao Tác - Live Web Demo)**:  
  * *Lời thoại*: "FieldShift ra đời để giải quyết bài toán này. Nông dân chỉ cần nhấp chuột chọn vị trí thửa ruộng của mình trên bản đồ vệ tinh ESRI..."
  * *Hình ảnh*: Màn hình quay thao tác click chọn Nghệ An, hệ thống gọi API NASA trong 0.2 giây, các thẻ KPI nhiệt độ đỉnh 40.9°C và lượng mưa 12.4 mm/ngày bừng sáng.
* **00:45 – 01:15 (Đột Phá Luân Canh Thích Ứng)**:  
  * *Lời thoại*: "Dữ liệu vệ tinh lập tức cảnh báo nguy cơ sốc nhiệt và ngập lụt. Thay vì cố chấp trồng lúa vụ 2, FieldShift đề xuất chuyển sang Lạc Sen Thọ chịu nhiệt >40°C. Cây lạc né được cả khô hạn lẫn bão lũ, đồng thời tự nạp hơn 50kg đạm sinh học trả lại cho đất."
  * *Hình ảnh*: Lướt qua 3 thẻ vụ mùa và biểu đồ độ ẩm đất.
* **01:15 – 01:30 (Tác Động & Kêu Gọi)**:  
  * *Lời thoại*: "Điểm sức khỏe đất tăng từ 42 lên 89 điểm, tiết kiệm một nửa lượng nước tưới. FieldShift — Khi dữ liệu không gian của NASA bảo vệ từng tấc đất nông dân."
  * *Hình ảnh*: Logo FieldShift, logo NASA Space Apps Challenge và link GitHub.

---

## 3. Liên Kết Mục Tiêu Phát Triển Bền Vững Của Liên Hợp Quốc (UN SDGs)

Trong phần mô tả dự án trên trang chủ Space Apps, hãy tích chọn và lập luận 3 mục tiêu này:
1. **SDG 2: Zero Hunger (Xóa đói nghèo)**: Đảm bảo sản lượng lương thực ổn định, ngăn chặn nguy cơ mất trắng mùa vụ do thiên tai cực đoan.
2. **SDG 13: Climate Action (Hành động vì khí hậu)**: Giúp nông dân chủ động thích ứng với biến đổi khí hậu bằng dữ liệu vệ tinh khoa học thay vì phán đoán cảm tính.
3. **SDG 15: Life on Land (Bảo vệ hệ sinh thái trên cạn)**: Phục hồi sức khỏe đất, giảm xói mòn, giảm phát thải khí nhà kính từ phân bón hóa học nhờ vi khuẩn nốt sần cố định đạm.

---

## 4. Quy Chuẩn Trích Dẫn Dữ Liệu NASA (Data Citations)

Trong mục *"Data & Resources"* trên cổng nộp bài NASA Space Apps, copy đoạn trích dẫn chuẩn này:
```text
NASA Resources Used:
1. NASA POWER Agroclimatology API: Daily & Monthly Climatology Parameters (T2M, T2M_MAX, PRECTOTCORR, GWETTOP, GWETROOT, ALLSKY_SFC_SW_DWN) retrieved via NASA Langley Research Center.
2. Modern-Era Retrospective Analysis for Research and Applications, Version 2 (MERRA-2) meteorological datasets.
3. Earth Surface Soil Moisture & Root Zone Wetness models from NASA Land Data Assimilation Systems (LDAS).
```
