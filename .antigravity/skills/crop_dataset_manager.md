# Kỹ Năng Quản Trị & Mở Rộng Danh Mục Cây Trồng (Crop Dataset Manager Skill)

Kỹ năng này hướng dẫn cách thu thập, chuẩn hóa và nạp dữ liệu giống cây trồng mới từ các Viện nghiên cứu Nông nghiệp Việt Nam vào cơ sở dữ liệu PostgreSQL của **FieldShift**.

---

## 1. Khung Thuộc Tính Sinh Học Chuẩn Của Giống Cây (Crop Schema)

Mỗi giống cây trồng đưa vào hệ thống bắt buộc phải có đủ 10 chỉ số sau:

| Thuộc tính | Kiểu dữ liệu | Khoảng giá trị chuẩn | Ý nghĩa đối với thuật toán |
| :--- | :---: | :---: | :--- |
| `name` | Chuỗi | Tên phổ thông + Tên giống | Ví dụ: "Lạc L14", "Lúa ST25", "Đậu tương DT84" |
| `growth_days` | Số nguyên | 50 – 150 ngày | Xác định cây có kịp thu hoạch trước mùa bão hay không |
| `water_demand` | Lựa chọn | `LOW`, `MED`, `HIGH` | Hệ số tiêu thụ nước tưới theo mùa vụ |
| `nitrogen_fixing`| Boolean | `True` / `False` | Khả năng cộng sinh vi khuẩn nốt sần cố định đạm |
| `root_depth` | Lựa chọn | `SHALLOW`, `MEDIUM`, `DEEP` | Tầng rễ ăn nông (<30cm), vừa (30-60cm), sâu (>60cm) |
| `ideal_temp_min` | Số thực | 15.0 – 26.0 °C | Ngưỡng nhiệt dưới để hạt nảy mầm và phân cành |
| `ideal_temp_max` | Số thực | 28.0 – 38.0 °C | Ngưỡng nhiệt tối ưu cho quang hợp |
| `max_tolerated_temp`| Số thực | 35.0 – 45.0 °C | Nhiệt độ tối đa trước khi xảy ra hiện tượng lép hạt, cháy lá |
| `soil_benefit` | Chuỗi | Văn bản ngắn | Diễn giải lợi ích cho đất (tăng mùn, chống xói mòn) |
| `average_yield_ton_ha`| Số thực | 1.0 – 25.0 tấn/ha | Năng suất bình quân để tính toán hiệu quả kinh tế |

---

## 2. Quy Trình Nạp Dữ Liệu Hàng Loạt (Bulk Import Script)

Khi có danh sách giống cây mới từ file JSON hoặc CSV, tạo lệnh quản trị Django:

```python
# farm_advisor/management/commands/import_crops.py
import json
from django.core.management.base import BaseCommand
from farm_advisor.models import Crop, CropCategory

class Command(BaseCommand):
    help = 'Nạp hàng loạt giống cây trồng từ file JSON'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Đường dẫn tới file JSON')

    def handle(self, *args, **options):
        with open(options['file_path'], 'r', encoding='utf-8') as f:
            crops_list = json.load(f)

        created_count = 0
        for item in crops_list:
            category, _ = CropCategory.objects.get_or_create(name=item.pop('category_name'))
            crop, created = Crop.objects.update_or_create(
                name=item['name'],
                defaults={**item, 'category': category}
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Đã nạp thành công {created_count} giống cây mới!"))
```

---

## 3. Nguồn Dữ Liệu Khảo Cứu Uy Tín Tại Việt Nam
* **Viện Khoa học Nông nghiệp Việt Nam (VAAS)**: Dữ liệu về các giống lúa thuần, ngô lai và cây họ đậu thích ứng hạn.
* **Viện Cây lương thực và Cây thực phẩm (FCRI)**: Dữ liệu các giống đậu phộng (L14, L23), đậu tương chịu nhiệt.
* **Viện Lúa Đồng bằng Sông Cửu Long (CLRRI)**: Danh mục các giống lúa chịu mặn (OM5451, OM18, ST24, ST25).
