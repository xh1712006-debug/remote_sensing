from django.test import TestCase, Client
from farm_advisor.models import CropCategory, Crop, SoilProfile, FarmLocation
from farm_advisor.services.rotation_engine import generate_crop_rotation_plan

class CropModelTestCase(TestCase):
    def setUp(self):
        self.category = CropCategory.objects.create(
            name="Cây họ Đậu",
            description="Cố định đạm tự nhiên"
        )
        self.crop = Crop.objects.create(
            name="Lạc Sen Thọ",
            scientific_name="Arachis hypogaea",
            category=self.category,
            growth_days=85,
            water_demand="LOW",
            nitrogen_fixing=True,
            root_depth="MEDIUM",
            ideal_temp_min=25.0,
            ideal_temp_max=38.0,
            max_tolerated_temp=42.0,
            soil_benefit="Cố định 50kg N/ha",
            best_season="Vụ Hè Thu",
            average_yield_ton_ha=3.8
        )

    def test_crop_creation(self):
        self.assertEqual(str(self.crop), "Lạc Sen Thọ")
        self.assertTrue(self.crop.nitrogen_fixing)
        self.assertEqual(self.crop.water_demand, "LOW")


class RotationEngineTestCase(TestCase):
    def setUp(self):
        self.extreme_climate = {
            "analysis": {
                "max_temp": 41.2,
                "extreme_heat_alert": True,
                "max_rain": 13.5,
                "flood_risk_alert": True
            }
        }

    def test_rotation_plan_schedule(self):
        plan = generate_crop_rotation_plan(self.extreme_climate, farmer_goal="soil_health")
        schedule = plan["schedule"]
        
        self.assertEqual(len(schedule), 3)
        # Vụ 1 là lúa vụ xuân
        self.assertIn("Lúa", schedule[0]["recommended_crop"])
        # Vụ 2 là cây họ đậu (lạc) để né nắng nóng gió Lào
        self.assertIn("Lạc", schedule[1]["recommended_crop"])
        self.assertIn("cố định đạm", schedule[1]["crop_type"])
        # Vụ 3 là khoai lang né đỉnh lũ
        self.assertIn("Khoai", schedule[2]["recommended_crop"])

        # Kiểm tra điểm số sức khỏe đất
        comparison = plan["comparison"]
        self.assertEqual(comparison["monoculture"]["soil_health_score"], 42)
        self.assertEqual(comparison["crop_rotation"]["soil_health_score"], 89)


class ApiEndpointTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_dashboard_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_api_analyze_farm_status(self):
        response = self.client.get('/api/analyze/?lat=18.9950&lon=105.4740&goal=soil_health')
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertTrue(json_data["success"])
        self.assertIn("nasa", json_data)
        self.assertIn("plan", json_data)
