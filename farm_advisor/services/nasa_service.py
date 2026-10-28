import urllib.request
import json
import logging

logger = logging.getLogger(__name__)

NASA_POWER_API_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

def fetch_nasa_climate_data(latitude: float, longitude: float):
    """
    Gọi NASA POWER API để lấy dữ liệu khí hậu và độ ẩm đất cho tọa độ (latitude, longitude).
    Trả về dữ liệu trung bình các tháng trong năm (12 tháng).
    """
    params = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,GWETTOP,GWETROOT,ALLSKY_SFC_SW_DWN"
    url = f"{NASA_POWER_API_URL}?parameters={params}&community=AG&longitude={longitude:.4f}&latitude={latitude:.4f}&format=JSON"

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'NASA-SpaceApps-FieldShift/1.0'})
        with urllib.request.urlopen(req, timeout=12) as response:
            raw_data = json.loads(response.read().decode('utf-8'))
            properties = raw_data.get('properties', {})
            parameters = properties.get('parameter', {})

            months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
            
            # Trích xuất các chuỗi dữ liệu theo tháng
            t2m_max = [parameters.get('T2M_MAX', {}).get(m, 0) for m in months]
            t2m_avg = [parameters.get('T2M', {}).get(m, 0) for m in months]
            t2m_min = [parameters.get('T2M_MIN', {}).get(m, 0) for m in months]
            precipitation = [parameters.get('PRECTOTCORR', {}).get(m, 0) for m in months]
            gwet_top = [parameters.get('GWETTOP', {}).get(m, 0) for m in months]
            gwet_root = [parameters.get('GWETROOT', {}).get(m, 0) for m in months]
            solar_radiation = [parameters.get('ALLSKY_SFC_SW_DWN', {}).get(m, 0) for m in months]

            # Phân tích rủi ro khí hậu
            max_temp = max(t2m_max) if t2m_max else 35.0
            max_temp_month = months[t2m_max.index(max_temp)] if t2m_max else 'JUN'

            max_rain = max(precipitation) if precipitation else 10.0
            max_rain_month = months[precipitation.index(max_rain)] if precipitation else 'SEP'

            min_rain = min(precipitation) if precipitation else 0.5
            min_rain_month = months[precipitation.index(min_rain)] if precipitation else 'FEB'

            min_soil_moist = min(gwet_top) if gwet_top else 0.4
            min_soil_month = months[gwet_top.index(min_soil_moist)] if gwet_top else 'APR'

            # Đánh giá hạn hán / nắng nóng cực đoan
            extreme_heat_alert = max_temp >= 39.0
            flood_risk_alert = max_rain >= 11.0
            drought_alert = min_soil_moist < 0.65 or min_rain < 1.0

            return {
                "success": True,
                "coordinates": {"lat": latitude, "lon": longitude},
                "months": months,
                "months_vn": ["Th.1", "Th.2", "Th.3", "Th.4", "Th.5", "Th.6", "Th.7", "Th.8", "Th.9", "Th.10", "Th.11", "Th.12"],
                "data": {
                    "t2m_max": t2m_max,
                    "t2m_avg": t2m_avg,
                    "t2m_min": t2m_min,
                    "precipitation": precipitation,
                    "gwet_top": gwet_top,
                    "gwet_root": gwet_root,
                    "solar_radiation": solar_radiation,
                },
                "analysis": {
                    "max_temp": round(max_temp, 1),
                    "max_temp_month": max_temp_month,
                    "extreme_heat_alert": extreme_heat_alert,
                    "max_rain": round(max_rain, 1),
                    "max_rain_month": max_rain_month,
                    "flood_risk_alert": flood_risk_alert,
                    "min_rain": round(min_rain, 2),
                    "min_rain_month": min_rain_month,
                    "min_soil_moist": round(min_soil_moist, 2),
                    "min_soil_month": min_soil_month,
                    "drought_alert": drought_alert,
                }
            }

    except Exception as e:
        logger.error(f"Lỗi khi gọi NASA POWER API: {e}")
        # Trả về fallback dữ liệu mẫu tiêu biểu của miền Trung (Nghệ An) nếu mạng gặp sự cố
        return {
            "success": False,
            "error": str(e),
            "fallback": True,
            "coordinates": {"lat": latitude, "lon": longitude},
            "months_vn": ["Th.1", "Th.2", "Th.3", "Th.4", "Th.5", "Th.6", "Th.7", "Th.8", "Th.9", "Th.10", "Th.11", "Th.12"],
            "data": {
                "t2m_max": [31.4, 34.5, 35.1, 39.2, 40.1, 38.4, 40.9, 36.0, 34.6, 32.4, 32.3, 29.4],
                "precipitation": [1.0, 0.7, 1.4, 1.9, 4.8, 4.1, 7.0, 9.4, 12.4, 9.1, 2.6, 1.3],
                "gwet_top": [0.76, 0.73, 0.69, 0.65, 0.65, 0.66, 0.68, 0.75, 0.83, 0.85, 0.83, 0.79],
                "gwet_root": [0.74, 0.71, 0.68, 0.64, 0.63, 0.64, 0.66, 0.73, 0.82, 0.85, 0.83, 0.78],
            },
            "analysis": {
                "max_temp": 40.9,
                "max_temp_month": "JUL",
                "extreme_heat_alert": True,
                "max_rain": 12.4,
                "max_rain_month": "SEP",
                "flood_risk_alert": True,
                "min_soil_moist": 0.63,
                "drought_alert": True,
            }
        }
