# Kỹ Năng Tích Hợp Chỉ Số Viễn Thám & Đất Đai Mở Rộng (GIS & Satellite Indices Skill)

Kỹ năng này hướng dẫn cách mở rộng hệ thống để tích hợp thêm các nguồn dữ liệu viễn thám cấp cao của NASA/ESA (MODIS, Landsat) và dữ liệu thổ nhưỡng toàn cầu (SoilGrids ISRIC).

---

## 1. Tích Hợp Chỉ Số Thực Vật Vệ Tinh (NDVI - Crop Vigor)

### Công thức tính NDVI:
$$\text{NDVI} = \frac{\text{NIR} - \text{RED}}{\text{NIR} + \text{RED}}$$
* Trong đó:
  * $\text{RED}$: Kênh sóng ánh sáng đỏ (hấp thụ bởi diệp lục để quang hợp).
  * $\text{NIR}$: Kênh sóng cận hồng ngoại (phản xạ mạnh bởi cấu trúc tế bào lá khỏe mạnh).
* **Thang đánh giá nông nghiệp**:
  * $\text{NDVI} < 0.2$: Đất trống, đất khô nẻ không có cây trồng che phủ.
  * $0.2 \le \text{NDVI} \le 0.4$: Cây con mới gieo hoặc thảm thực vật cằn cỗi vì hạn hán.
  * $\text{NDVI} > 0.6$: Đồng ruộng sinh trưởng khỏe mạnh, sinh khối xanh tối ưu.

---

## 2. Kết Nối API Thổ Nhưỡng Toàn Cầu SoilGrids (ISRIC)

Ngoài dữ liệu vệ tinh khí tượng NASA, hệ thống có thể truy vấn trực tiếp đặc tính lý hóa của đất từ **SoilGrids REST API** (hoàn toàn mở và miễn phí):

```python
import urllib.request
import json

def fetch_soilgrids_properties(lat: float, lon: float):
    """
    Truy vấn độ pH, hàm lượng hữu cơ (SOC) và tỷ lệ cát/sét từ SoilGrids API.
    """
    url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lat={lat}&lon={lon}&property=phh2o&property=soc&property=sand&depth=0-30cm"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'FieldShift/1.0'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        layers = data.get('properties', {}).get('layers', [])
        
        # pH đo bằng đơn vị pH*10 trong SoilGrids
        ph_raw = next((l for l in layers if l['name'] == 'phh2o'), None)
        ph_value = ph_raw['depths'][0]['values']['mean'] / 10.0 if ph_raw else 6.0
        
        return {
            "ph": ph_value,
            "soil_description": "Đất chua (cần bón vôi)" if ph_value < 5.5 else "Đất trung tính (thích hợp đa số cây)"
        }
```

---

## 3. Bản Đồ Nhiệt Vệ Tinh (Land Surface Temperature - LST)
* Nhiệt độ bề mặt đất LST đo từ cảm biến nhiệt TIRS của vệ tinh Landsat 8/9 thường cao hơn nhiệt độ không khí $2 - 5^\circ C$ vào mùa hè.
* Ứng dụng: Nhận diện các "điểm nóng cực hạn" (Hotspots) trên cánh đồng để khuyến cáo nông dân tủ gốc bằng rơm rạ hoặc tưới hạ nhiệt vào ban đêm.
