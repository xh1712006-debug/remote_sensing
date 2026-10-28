from django.core.management.base import BaseCommand
from farm_advisor.models import CropCategory, Crop, SoilProfile, FarmLocation

class Command(BaseCommand):
    help = 'Nạp dữ liệu mẫu ban đầu về cây trồng, đất đai và nông trại mẫu'

    def handle(self, *args, **options):
        self.stdout.write("Loading seed data into database...")

        # 1. Nhóm cây trồng
        cat_cereal, _ = CropCategory.objects.get_or_create(
            name="Ngũ cốc",
            defaults={"description": "Các loại cây ngũ cốc chủ lực: lúa, ngô, cao lương"}
        )
        cat_legume, _ = CropCategory.objects.get_or_create(
            name="Cây họ Đậu (Legumes)",
            defaults={"description": "Cây có vi khuẩn nốt sần Rhizobium cố định đạm tự nhiên, cải tạo đất"}
        )
        cat_root, _ = CropCategory.objects.get_or_create(
            name="Cây lấy củ & Rau màu",
            defaults={"description": "Khoai lang, củ cải, rau các loại"}
        )
        cat_oil, _ = CropCategory.objects.get_or_create(
            name="Cây có dầu",
            defaults={"description": "Vừng/mè, hướng dương, đậu tương"}
        )

        # 2. Hồ sơ đất
        soil_catpha, _ = SoilProfile.objects.get_or_create(
            name="Đất cát pha ven biển Nghệ An",
            defaults={
                "texture": "Cát pha",
                "ph_min": 5.2,
                "ph_max": 6.2,
                "organic_matter_level": "Nghèo mùn (dễ bị khô nẻ)",
                "drainage": "Thoát nước nhanh, giữ ẩm kém"
            }
        )

        soil_phusa, _ = SoilProfile.objects.get_or_create(
            name="Đất phù sa sông Lam / Sông Tiền",
            defaults={
                "texture": "Phù sa ngọt",
                "ph_min": 6.0,
                "ph_max": 7.0,
                "organic_matter_level": "Giàu mùn hữu cơ",
                "drainage": "Trung bình"
            }
        )

        # 3. Cây trồng
        crops_data = [
            {
                "name": "Lúa nước (Jasmine / ST24)",
                "scientific_name": "Oryza sativa",
                "category": cat_cereal,
                "growth_days": 110,
                "water_demand": "HIGH",
                "nitrogen_fixing": False,
                "root_depth": "SHALLOW",
                "ideal_temp_min": 22.0,
                "ideal_temp_max": 32.0,
                "max_tolerated_temp": 36.0,
                "soil_benefit": "Cung cấp an ninh lương thực chính, tuy nhiên hút nhiều đạm và kali",
                "best_season": "Vụ Xuân",
                "average_yield_ton_ha": 6.2
            },
            {
                "name": "Lạc (Đậu phộng) Sen Thọ / L14",
                "scientific_name": "Arachis hypogaea",
                "category": cat_legume,
                "growth_days": 85,
                "water_demand": "LOW",
                "nitrogen_fixing": True,
                "root_depth": "MEDIUM",
                "ideal_temp_min": 25.0,
                "ideal_temp_max": 38.0,
                "max_tolerated_temp": 42.0,
                "soil_benefit": "Cố định 45-60kg N/ha tự nhiên nhờ nốt sần rễ, xới xốp đất, cắt đứt sâu bệnh lúa",
                "best_season": "Vụ Hè Thu (Né gió Lào và mưa bão)",
                "average_yield_ton_ha": 3.8
            },
            {
                "name": "Đậu xanh ngắn ngày (DX044)",
                "scientific_name": "Vigna radiata",
                "category": cat_legume,
                "growth_days": 65,
                "water_demand": "LOW",
                "nitrogen_fixing": True,
                "root_depth": "SHALLOW",
                "ideal_temp_min": 24.0,
                "ideal_temp_max": 37.0,
                "max_tolerated_temp": 41.0,
                "soil_benefit": "Sinh trưởng thần tốc 60-65 ngày, cố định đạm, chịu hạn rất tốt",
                "best_season": "Vụ Hè Thu / Gối vụ",
                "average_yield_ton_ha": 2.2
            },
            {
                "name": "Mè (Vừng đen Nghệ An)",
                "scientific_name": "Sesamum indicum",
                "category": cat_oil,
                "growth_days": 75,
                "water_demand": "LOW",
                "nitrogen_fixing": False,
                "root_depth": "MEDIUM",
                "ideal_temp_min": 26.0,
                "ideal_temp_max": 38.0,
                "max_tolerated_temp": 43.0,
                "soil_benefit": "Chịu nắng nóng cực hạn, phù hợp tuyệt đối với đất cát pha mùa gió Lào",
                "best_season": "Vụ Hè Thu",
                "average_yield_ton_ha": 1.2
            },
            {
                "name": "Khoai lang Hoàng Long",
                "scientific_name": "Ipomoea batatas",
                "category": cat_root,
                "growth_days": 90,
                "water_demand": "MED",
                "nitrogen_fixing": False,
                "root_depth": "DEEP",
                "ideal_temp_min": 18.0,
                "ideal_temp_max": 30.0,
                "max_tolerated_temp": 35.0,
                "soil_benefit": "Bộ rễ và thảm lá dày che phủ đất, giữ ẩm và chống rửa trôi sau mùa bão lũ",
                "best_season": "Vụ Đông (Sau lũ tháng 10)",
                "average_yield_ton_ha": 15.0
            },
            {
                "name": "Ngô lai sinh khối (NK7328)",
                "scientific_name": "Zea mays",
                "category": cat_cereal,
                "growth_days": 100,
                "water_demand": "MED",
                "nitrogen_fixing": False,
                "root_depth": "MEDIUM",
                "ideal_temp_min": 20.0,
                "ideal_temp_max": 34.0,
                "max_tolerated_temp": 38.0,
                "soil_benefit": "Thân lá lớn bổ sung sinh khối mùn hữu cơ dồi dào cho đất",
                "best_season": "Vụ Đông / Vụ Xuân",
                "average_yield_ton_ha": 7.5
            }
        ]

        for c_data in crops_data:
            Crop.objects.get_or_create(name=c_data["name"], defaults=c_data)

        # 4. Điểm nông trại mẫu
        FarmLocation.objects.get_or_create(
            name="Cánh đồng Diễn Châu - Yên Thành",
            region="Nghệ An",
            defaults={
                "latitude": 18.9950,
                "longitude": 105.4740,
                "soil_profile": soil_catpha,
                "description": "Vùng trọng điểm nông nghiệp Nghệ An chịu tác động kép: Gió Lào khô hạn tháng 5-7 và Mưa bão lũ tháng 9-10."
            }
        )
        FarmLocation.objects.get_or_create(
            name="Nông trại Bến Tre (Châu Thành - Ba Tri)",
            region="Bến Tre (ĐBSCL)",
            defaults={
                "latitude": 10.2433,
                "longitude": 106.3753,
                "soil_profile": soil_phusa,
                "description": "Vùng hạ lưu ĐBSCL đối mặt xâm nhập mặn và cạn kiệt nước ngọt tháng 1-4."
            }
        )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
