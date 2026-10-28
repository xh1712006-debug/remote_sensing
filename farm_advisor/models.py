from django.db import models

class CropCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên nhóm")
    description = models.TextField(blank=True, verbose_name="Mô tả nhóm")

    class Meta:
        verbose_name = "Nhóm cây trồng"
        verbose_name_plural = "Các nhóm cây trồng"

    def __str__(self):
        return self.name


class Crop(models.Model):
    WATER_DEMAND_CHOICES = [
        ('LOW', 'Thấp (Chịu hạn tốt)'),
        ('MED', 'Trung bình'),
        ('HIGH', 'Cao (Cần ngập nước / tưới nhiều)'),
    ]

    ROOT_DEPTH_CHOICES = [
        ('SHALLOW', 'Rễ nông (< 30cm)'),
        ('MEDIUM', 'Rễ vừa (30 - 60cm)'),
        ('DEEP', 'Rễ cọc sâu (> 60cm - Phá nén dẽ đất)'),
    ]

    name = models.CharField(max_length=120, verbose_name="Tên cây trồng")
    scientific_name = models.CharField(max_length=150, blank=True, verbose_name="Tên khoa học")
    category = models.ForeignKey(CropCategory, on_delete=models.CASCADE, related_name='crops', verbose_name="Nhóm")
    
    growth_days = models.IntegerField(default=90, verbose_name="Thời gian sinh trưởng (ngày)")
    water_demand = models.CharField(max_length=10, choices=WATER_DEMAND_CHOICES, default='MED', verbose_name="Nhu cầu nước")
    nitrogen_fixing = models.BooleanField(default=False, verbose_name="Khả năng cố định đạm (Vi khuẩn nốt sần)")
    root_depth = models.CharField(max_length=10, choices=ROOT_DEPTH_CHOICES, default='MEDIUM', verbose_name="Độ sâu rễ")
    
    ideal_temp_min = models.FloatField(default=20.0, verbose_name="Nhiệt độ tối thiểu (°C)")
    ideal_temp_max = models.FloatField(default=35.0, verbose_name="Nhiệt độ tối đa (°C)")
    max_tolerated_temp = models.FloatField(default=40.0, verbose_name="Nhiệt độ chịu đựng tối đa (°C)")

    soil_benefit = models.CharField(max_length=255, verbose_name="Lợi ích cải tạo đất", help_text="VD: Bổ sung đạm hữu cơ, tăng mùn, chống xói mòn")
    best_season = models.CharField(max_length=100, default="Vụ Xuân, Vụ Hè Thu", verbose_name="Mùa vụ thích hợp")
    average_yield_ton_ha = models.FloatField(default=3.5, verbose_name="Năng suất trung bình (tấn/ha)")

    class Meta:
        verbose_name = "Cây trồng"
        verbose_name_plural = "Danh mục cây trồng"

    def __str__(self):
        return self.name


class SoilProfile(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên loại đất")
    texture = models.CharField(max_length=100, verbose_name="Thành phần cơ giới", help_text="VD: Cát pha, Phù sa ngọt, Feralit đỏ")
    ph_min = models.FloatField(default=5.5)
    ph_max = models.FloatField(default=6.8)
    organic_matter_level = models.CharField(max_length=50, default="Trung bình", verbose_name="Hàm lượng mùn hữu cơ")
    drainage = models.CharField(max_length=50, default="Tốt", verbose_name="Khả năng thoát nước")

    class Meta:
        verbose_name = "Hồ sơ thổ nhưỡng"
        verbose_name_plural = "Hồ sơ thổ nhưỡng"

    def __str__(self):
        return self.name


class FarmLocation(models.Model):
    name = models.CharField(max_length=150, verbose_name="Tên địa điểm")
    region = models.CharField(max_length=100, default="Nghệ An", verbose_name="Vùng / Tỉnh")
    latitude = models.FloatField(verbose_name="Vĩ độ (Lat)")
    longitude = models.FloatField(verbose_name="Kinh độ (Lng)")
    soil_profile = models.ForeignKey(SoilProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Loại đất chính")
    description = models.TextField(blank=True, verbose_name="Mô tả khí hậu nông nghiệp")

    class Meta:
        verbose_name = "Điểm nông trại mẫu"
        verbose_name_plural = "Danh sách điểm nông trại mẫu"

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
