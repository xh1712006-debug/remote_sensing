# Kỹ Năng Phân Tích Dữ Liệu Vệ Tinh NASA (NASA Earth Data Analysis Skill)

Kỹ năng này hướng dẫn cách truy vấn, trích xuất và diễn giải các chỉ số vệ tinh quan sát Trái Đất từ hệ thống **NASA POWER** để làm đầu vào cho thuật toán nông nghiệp thông minh.

---

## 1. Bản Đồ Tham Số Vệ Tinh Của NASA

| Ký hiệu NASA | Tên đầy đủ | Đơn vị | Ý nghĩa đối với Nông nghiệp |
| :--- | :--- | :---: | :--- |
| `T2M` | Temperature at 2 Meters | °C | Nhiệt độ không khí trung bình để xác định thời vụ sinh trưởng lý tưởng. |
| `T2M_MAX` | Temperature at 2 Meters Maximum | °C | Nhiệt độ đỉnh điểm trong ngày; dùng để phát hiện sốc nhiệt, gió Lào, cháy lá. |
| `T2M_MIN` | Temperature at 2 Meters Minimum | °C | Nhiệt độ thấp nhất; dùng để cảnh báo rét đậm rét hại vào vụ đông xuân. |
| `PRECTOTCORR` | Precipitation Corrected | mm/ngày | Lượng mưa thực tế đo bằng vệ tinh MERRA-2; dùng để phát hiện hạn hán và lũ lụt. |
| `GWETTOP` | Surface Soil Wetness | 0 - 1 | Độ ẩm đất tầng mặt (0 - 5 cm); cảnh báo đất khô nẻ tầng mặt, ảnh hưởng nảy mầm. |
| `GWETROOT` | Root Zone Soil Wetness | 0 - 1 | Độ ẩm đất tầng rễ cây (0 - 100 cm); xác định cây có đủ nước nuôi thân củ hay không. |
| `ALLSKY_SFC_SW_DWN` | All Sky Surface Shortwave Downward Irradiance | $MJ/m^2/ngày$ | Bức xạ mặt trời; dùng để tính toán quang hợp và tốc độ bốc thoát hơi nước (PET). |

---

## 2. Quy Trình Truy Vấn Dữ Liệu Bằng Python

Khi cần lấy dữ liệu cho một tọa độ mới, Agent thực hiện theo cấu trúc chuẩn:

```python
import urllib.request
import json

def query_nasa_climatology(lat: float, lon: float):
    # Tham số chuẩn nông nghiệp
    params = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,GWETTOP,GWETROOT,ALLSKY_SFC_SW_DWN"
    url = f"https://power.larc.nasa.gov/api/temporal/climatology/point?parameters={params}&community=AG&longitude={lon:.4f}&latitude={lat:.4f}&format=JSON"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'FieldShift-NASA-Agent/1.0'})
    with urllib.request.urlopen(req, timeout=12) as response:
        payload = json.loads(response.read().decode('utf-8'))
        return payload['properties']['parameter']
```

---

## 3. Quy Tắc Diễn Giải Chỉ Số & Gán Nhãn Khí Hậu

1. **Nhận diện Gió Lào & Nắng nóng cực đoan**:
   * Nếu $\max(\text{T2M\_MAX}) \ge 39.0^\circ C$ trong tháng 5, 6 hoặc 7:
     $\rightarrow$ Gán nhãn `extreme_heat_alert = True`.
     $\rightarrow$ Khuyến cáo: *Tránh gieo sạ lúa; bắt buộc chuyển đổi cơ cấu cây trồng sang Lạc hoặc Mè chịu hạn.*
2. **Nhận diện Nguy cơ Bão Lũ**:
   * Nếu $\max(\text{PRECTOTCORR}) \ge 11.0$ mm/ngày trong tháng 9 hoặc 10:
     $\rightarrow$ Gán nhãn `flood_risk_alert = True`.
     $\rightarrow$ Khuyến cáo: *Thu hoạch dứt điểm vụ 2 trước tháng 9; không xuống giống lúa muộn; lên luống cao cho vụ đông.*
3. **Nhận diện Khô hạn Tầng Đất**:
   * Nếu $\min(\text{GWETTOP}) < 0.65$ hoặc Lượng mưa tháng $< 1.0$ mm/ngày:
     $\rightarrow$ Gán nhãn `drought_alert = True`.
     $\rightarrow$ Khuyến cáo: *Đất nứt nẻ, cần phủ rơm rạ hoặc trồng cây họ đậu che phủ đất để giảm bốc hơi nước.*
