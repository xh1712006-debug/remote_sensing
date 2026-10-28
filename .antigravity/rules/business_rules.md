# Quy Tắc Nghiệp Vụ Nông Nghiệp & Luân Canh Đất Đai (Agricultural Business Rules)

Tài liệu này định nghĩa toàn bộ các quy tắc nghiệp vụ cốt lõi mà mọi thuật toán, API hoặc logic gợi ý trong dự án **FieldShift** bắt buộc phải tuân thủ nghiêm ngặt.

---

## 1. Nguyên Tắc Cân Bằng Dinh Dưỡng & Cố Định Đạm (Nitrogen Balance Rule)
- **Quy tắc cấm độc canh**: Nghiêm cấm đề xuất trồng 3 vụ lúa nước liên tiếp trong năm trên cùng một thửa ruộng vì sẽ gây cạn kiệt tầng đạm hữu cơ, chua hóa đất và nén dẽ tầng đế cày.
- **Quy tắc bắt buộc cây họ Đậu (Legumes Mandatory)**:
  - Bắt buộc phải có ít nhất **1 vụ trong năm** sử dụng cây thuộc họ Đậu (`nitrogen_fixing = True`, ví dụ: Lạc/Đậu phộng, Đậu xanh, Đậu nành).
  - Vi khuẩn nốt sần *Rhizobium* cộng sinh ở rễ phải đảm bảo bổ sung tối thiểu từ **40 – 60 kg N/ha tự nhiên** cho đất.
  - Phải hướng dẫn nông dân cày vùi tàn dư thân lá sau thu hoạch để tăng hàm lượng mùn hữu cơ (SOC - Soil Organic Carbon).

---

## 2. Nguyên Tắc Đa Dạng Hóa Tầng Rễ (Root Architecture Rule)
- Đất canh tác phải được luân phiên giữa các kiểu rễ:
  - **Rễ chùm ăn nông (`root_depth = 'SHALLOW'`)**: Lúa nước, rau màu (hút dinh dưỡng tầng mặt 0–25 cm).
  - **Rễ cọc đâm sâu (`root_depth = 'DEEP'`)**: Cây lấy củ (Khoai lang, Cà rốt), Cây họ đậu rễ sâu (hút dinh dưỡng tầng 30–70 cm, phá vỡ lớp nén dẽ do máy móc và nước đọng, tạo mao dẫn thông khí cho vi sinh vật).
- Không gieo trồng liên tục 2 vụ các loại cây có cùng tầng rễ nông.

---

## 3. Nguyên Tắc Cắt Đứt Vòng Đời Sâu Bệnh (Pest & Pathogen Break Rule)
- **Cấm trồng liên tiếp cùng họ thực vật**:
  - Không luân canh cây cùng họ Cà (*Solanaceae*: Cà chua ➔ Cà tím ➔ Khoai tây) do tích tụ nấm bệnh *Phytophthora* và tuyến trùng nốt sần.
  - Sau một vụ ngũ cốc (*Poaceae*: Lúa/Ngô) có nguy cơ sâu đục thân và rầy nâu, vụ tiếp theo bắt buộc phải chuyển sang cây trồng cạn không phải ký chủ (Lạc hoặc Mè).
- Chuyển đổi môi trường đất giữa **ngập nước (yếm khí)** và **đất cạn (hiếu khí)** để tiêu diệt mầm mống cỏ dại và sâu bệnh trong đất một cách tự nhiên mà không cần phun hóa chất.

---

## 4. Nguyên Tắc Thích Ứng Khí Hậu Cực Đoan Dựa Trên Dữ Liệu NASA (Climate Adaptation Rules)

### 4.1 Ứng phó Nắng Nóng & Gió Lào (Extreme Heat & Foehn Wind):
- **Điều kiện kích hoạt**: Khi dữ liệu NASA chỉ ra nhiệt độ cực đại $T_{max} \ge 38.0^\circ C$ trong các tháng mùa hè (Tháng 5 – Tháng 7):
  - **CẤM**: Khuyến nghị gieo trồng lúa hè thu tại các vùng thiếu chủ động nước tưới (như Nghệ An, Hà Tĩnh).
  - **BẮT BUỘC**: Chuyển đổi sang cây chịu hạn cao (`water_demand = 'LOW'`), có ngưỡng chịu nhiệt tối đa $\ge 40.0^\circ C$ (Lạc Sen Thọ / L14, Mè đen, Đậu xanh ngắn ngày).
  - Chu kỳ sinh trưởng của vụ 2 không được vượt quá **90 ngày** để đảm bảo thu hoạch trước ngày 01 tháng 9.

### 4.2 Ứng phó Mưa Bão & Ngập Lụt (Flood & Storm Avoidance):
- **Điều kiện kích hoạt**: Khi dữ liệu vệ tinh NASA ghi nhận lượng mưa tích lũy tháng đạt đỉnh $\ge 11.0$ mm/ngày (Tháng 9 – Tháng 10):
  - **CẤM**: Để cây trồng trong giai đoạn trổ bông hoặc thu hoạch trong tháng 9 vì nguy cơ mất trắng do ngập lụt là trên 85%.
  - **BẮT BUỘC**: Vụ 3 (Thu Đông) chỉ được phép xuống giống sau ngày **15 tháng 10** khi đỉnh lũ đã rút.
  - Ưu tiên cây có thảm phủ xanh dày (Khoai lang, Ngô sinh khối) để chống rửa trôi lớp đất mặt màu mỡ do mưa lớn.

### 4.3 Ứng phó Hạn Hán & Thiếu Nước Tầng Rễ (Root Moisture Deficit):
- Khi chỉ số độ ẩm tầng rễ `GWETROOT < 0.65`:
  - Hệ thống phải đưa ra khuyến cáo tưới tiết kiệm nước (tưới nhỏ giọt/phun mưa cục bộ) và chỉ gợi ý các cây trồng tiết kiệm nước (giảm $\ge 40\%$ lượng nước tưới so với lúa).
