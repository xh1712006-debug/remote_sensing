# Đặc Tả Kiểm Thử Phần Mềm (Testing Specification)

Tài liệu này quy định chiến lược kiểm thử tự động, cấu trúc test suite và quy chuẩn viết test cho dự án **FieldShift**.

---

## 1. Chiến Lược Kiểm Thử (Testing Strategy)

Hệ thống được kiểm thử tự động thông qua 3 tầng cốt lõi:

1. **Kiểm thử Đơn vị Dịch vụ (Unit Tests for Services)**:
   * Kiểm thử tính đúng đắn của module trích xuất dữ liệu NASA [nasa_service.py](file:///d:/project/project-local/vientham/farm_advisor/services/nasa_service.py).
   * Kiểm thử logic thuật toán luân canh và tính điểm sức khỏe đất [rotation_engine.py](file:///d:/project/project-local/vientham/farm_advisor/services/rotation_engine.py) trong các kịch bản thời tiết khác nhau (nắng nóng cực đoan >40°C, mưa lũ bão dồn dập, đất khô cằn).
2. **Kiểm thử Tích hợp API & Views (Integration Tests)**:
   * Giả lập gửi HTTP GET tới `/api/analyze/?lat=18.9950&lon=105.4740` để kiểm tra định dạng phản hồi JSON và mã trạng thái HTTP 200.
   * Kiểm tra giao diện Dashboard `/` render đầy đủ các thành phần HTML và context dữ liệu.
3. **Kiểm thử Cơ sở dữ liệu (Model Tests)**:
   * Xác thực các ràng buộc toàn vẹn dữ liệu trong PostgreSQL (Foreign Key giữa `Crop` và `CropCategory`, các giá trị mặc định).

---

## 2. Công Cụ & Thư Viện Kiểm Thử (Testing Stack)
- **Framework kiểm thử**: **Django Test Framework** kế thừa từ `unittest.TestCase`.
- **HTTP Test Client**: `django.test.Client` (cho phép gửi request giả lập nội bộ tốc độ cao mà không cần khởi động web server).
- **Mocking**: `unittest.mock` dùng để giả lập phản hồi của máy chủ NASA POWER khi chạy kiểm thử offline.

---

## 3. Mã Nguồn Kiểm Thử Mẫu (Sample Test Code)

Ví dụ kiểm thử thuật toán luân canh trong `farm_advisor/tests.py`:

```python
from django.test import TestCase, Client
from farm_advisor.services.rotation_engine import generate_crop_rotation_plan

class CropRotationEngineTestCase(TestCase):
    def setUp(self):
        # Dữ liệu giả lập thời tiết khắc nghiệt Nghệ An
        self.mock_nasa_data = {
            "analysis": {
                "max_temp": 41.2,
                "extreme_heat_alert": True,
                "max_rain": 13.5,
                "flood_risk_alert": True
            }
        }

    def test_extreme_heat_recommends_legumes(self):
        """Kiểm tra: Khi nắng nóng cực đoan >40°C, hệ thống phải đề xuất cây họ Đậu (Lạc) để thay thế lúa"""
        plan = generate_crop_rotation_plan(self.mock_nasa_data, farmer_goal="soil_health")
        summer_season = plan["schedule"][1]
        
        self.assertIn("Lạc", summer_season["recommended_crop"])
        self.assertEqual(summer_season["crop_type"], "Cây họ Đậu cố định đạm (Legume)")
        self.assertGreater(plan["comparison"]["crop_rotation"]["soil_health_score"], 80)

class ApiEndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_api_analyze_returns_success(self):
        """Kiểm tra: Endpoint /api/analyze/ trả về JSON hợp lệ với status 200"""
        response = self.client.get('/api/analyze/?lat=18.9950&lon=105.4740&goal=soil_health')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertIn("nasa", json_data)
        self.assertIn("plan", json_data)
```

---

## 4. Lệnh Thực Thi Kiểm Thử (Test Execution)

```powershell
# Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1

# Chạy toàn bộ bộ kiểm thử của dự án
python manage.py test farm_advisor

# Chạy kiểm thử chi tiết kèm thông số thời gian
python manage.py test farm_advisor -v 2
```
