from django.shortcuts import render
from django.http import JsonResponse
from .models import Crop, FarmLocation, SoilProfile
from .services.nasa_service import fetch_nasa_climate_data
from .services.rotation_engine import generate_crop_rotation_plan

def dashboard_view(request):
    locations = FarmLocation.objects.all()
    crops = Crop.objects.all().select_related('category')
    soils = SoilProfile.objects.all()

    # Mặc định ban đầu chọn Nghệ An
    default_location = locations.first()
    default_lat = default_location.latitude if default_location else 18.9950
    default_lon = default_location.longitude if default_location else 105.4740

    context = {
        'locations': locations,
        'crops': crops,
        'soils': soils,
        'default_lat': default_lat,
        'default_lon': default_lon,
    }
    return render(request, 'dashboard.html', context)


def api_analyze_farm(request):
    """
    API endpoint nhận tọa độ lat/lng và trả về dữ liệu vệ tinh NASA + Kế hoạch luân canh.
    """
    try:
        lat = float(request.GET.get('lat', 18.9950))
        lon = float(request.GET.get('lon', 105.4740))
        goal = request.GET.get('goal', 'soil_health')

        # 1. Gọi NASA POWER API
        nasa_data = fetch_nasa_climate_data(lat, lon)

        # 2. Sinh kế hoạch luân canh thích ứng
        rotation_plan = generate_crop_rotation_plan(nasa_data, farmer_goal=goal)

        return JsonResponse({
            'success': True,
            'nasa': nasa_data,
            'plan': rotation_plan,
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
