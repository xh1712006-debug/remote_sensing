from django.contrib import admin
from .models import CropCategory, Crop, SoilProfile, FarmLocation

@admin.register(CropCategory)
class CropCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'growth_days', 'water_demand', 'nitrogen_fixing', 'root_depth', 'average_yield_ton_ha')
    list_filter = ('category', 'water_demand', 'nitrogen_fixing', 'root_depth')
    search_fields = ('name', 'scientific_name')

@admin.register(SoilProfile)
class SoilProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'texture', 'ph_min', 'ph_max', 'organic_matter_level', 'drainage')

@admin.register(FarmLocation)
class FarmLocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'latitude', 'longitude', 'soil_profile')
