# Kỹ Năng Tối Ưu Tốc Độ & Cache Dữ Liệu Vệ Tinh (Satellite Data Cache Optimization)

Kỹ năng này hướng dẫn cách áp dụng cơ chế bộ nhớ đệm (Caching) cho các lời gọi API viễn thám NASA, giúp giảm thời gian phản hồi giao diện từ **3.000 mili-giây xuống dưới 30 mili-giây** (nhanh gấp 100 lần), mang lại trải nghiệm mượt mà khi người dùng tương tác bản đồ.

---

## 1. Bản Chất Khoa Học Của Dữ Liệu Khí Hậu NASA

1. **Độ phân giải không gian của NASA MERRA-2**: Dữ liệu NASA POWER có độ phân giải lưới tự nhiên khoảng **$0.5^\circ \times 0.5^\circ$** (khoảng $50 \times 50$ km). Do đó, hai thửa ruộng cách nhau 5–10 km sẽ dùng chung một khối dữ liệu khí tượng.
2. **Tính chu kỳ của dữ liệu Khí hậu học (Climatology)**: Dữ liệu trung bình khí hậu nhiều năm là dữ liệu tĩnh, không thay đổi theo từng giây hay từng phút.
3. 👉 **Nguyên lý Tối ưu**: Khi người dùng click chọn tọa độ, hệ thống sẽ làm tròn tọa độ về mắt lưới gần nhất ($0.1^\circ$) và lưu vào bộ nhớ đệm (Cache) trong **30 ngày**.

---

## 2. Kỹ Thuật Làm Tròn Lưới Tọa Độ (Grid Snapping)

Hàm chuẩn hóa khóa Cache theo tọa độ:

```python
def generate_cache_key(lat: float, lon: float) -> str:
    """
    Làm tròn tọa độ về bước lưới 0.1 độ (~11km).
    Ví dụ: Lat 18.9950, Lon 105.4740 -> 'nasa_cache_19.0_105.5'
    """
    grid_lat = round(lat, 1)
    grid_lon = round(lon, 1)
    return f"nasa_power_grid_{grid_lat}_{grid_lon}"
```

---

## 3. Tích Hợp Caching Vào `nasa_service.py`

Sử dụng thư viện cache tích hợp sẵn của Django (`django.core.cache`):

```python
from django.core.cache import cache
import json

def get_cached_nasa_data(lat: float, lon: float):
    cache_key = generate_cache_key(lat, lon)
    
    # 1. Kiểm tra trong Cache xem đã có chưa
    cached_data = cache.get(cache_key)
    if cached_data:
        # Phản hồi ngay trong 5 - 15 mili-giây!
        return cached_data

    # 2. Nếu chưa có, gọi NASA API thật (mất ~2s)
    fresh_data = fetch_nasa_climate_data(lat, lon)
    
    # 3. Lưu vào Cache trong 30 ngày (2,592,000 giây)
    if fresh_data.get("success"):
        cache.set(cache_key, fresh_data, timeout=60 * 60 * 24 * 30)

    return fresh_data
```

---

## 4. Cấu Hình Backend Cache Trong `core/settings.py`

### 4.1 Môi trường Phát triển (Local Development):
Sử dụng `LocMemCache` (Bộ nhớ RAM nhanh nhất trên máy cá nhân):
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'fieldshift-nasa-cache',
    }
}
```

### 4.2 Môi trường Chạy Thật (Production):
Sử dụng `RedisCache` để cache phân tán giữa nhiều worker:
```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```
