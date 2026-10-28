/**
 * FieldShift - NASA Space Apps Challenge
 * Client-side script handling Leaflet interactive satellite map, AJAX NASA API calls, and Chart.js visualizations.
 */

let map, marker;
let weatherChartInstance = null;
let soilChartInstance = null;

// Khởi tạo bản đồ vệ tinh Leaflet khi DOM sẵn sàng
document.addEventListener("DOMContentLoaded", function() {
    const latInput = document.getElementById("input-lat");
    const lonInput = document.getElementById("input-lon");
    const initLat = parseFloat(latInput ? latInput.value : 18.9950) || 18.9950;
    const initLon = parseFloat(lonInput ? lonInput.value : 105.4740) || 105.4740;

    // Khởi tạo đối tượng Leaflet Map
    map = L.map('map').setView([initLat, initLon], 9);

    // Lớp bản đồ vệ tinh độ phân giải cao ESRI World Imagery
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri &mdash; NASA Space Apps FieldShift',
        maxZoom: 18
    }).addTo(map);

    // Lớp nhãn địa danh đường bộ trong suốt phía trên ảnh vệ tinh
    L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 18
    }).addTo(map);

    // Marker vị trí nông trại có thể kéo thả
    marker = L.marker([initLat, initLon], { draggable: true }).addTo(map);
    marker.bindPopup("<b>Vị trí nông trại đang chọn</b><br>Kéo thả hoặc nhấp để đổi vị trí.").openPopup();

    // Sự kiện click bản đồ để đổi vị trí
    map.on('click', function(e) {
        updateMarkerAndCoords(e.latlng.lat, e.latlng.lng);
        runAnalysis();
    });

    // Sự kiện kéo thả marker
    marker.on('dragend', function(e) {
        const pos = marker.getLatLng();
        updateMarkerAndCoords(pos.lat, pos.lng);
        runAnalysis();
    });

    // Tự động phân tích vị trí mặc định ban đầu và tính toán diện tích
    runAnalysis();
    updateEconomicEstimates();
});

/**
 * Tính toán lợi ích kinh tế (tiền phân bón, lượng nước, đạm sinh học) theo diện tích ruộng
 */
function updateEconomicEstimates() {
    const areaInput = document.getElementById("input-area");
    const unitSelect = document.getElementById("select-area-unit");
    const displayArea = document.getElementById("calc-display-area");
    const calcMoney = document.getElementById("calc-money");
    const calcWater = document.getElementById("calc-water");
    const calcNitrogen = document.getElementById("calc-nitrogen");

    let areaVal = parseFloat(areaInput ? areaInput.value : 1.0) || 1.0;
    const unit = unitSelect ? unitSelect.value : 'ha';

    // Quy đổi ra Hecta (ha)
    let areaInHa = areaVal;
    let unitLabel = "ha";
    if (unit === 'sao_trung_bo') {
        areaInHa = (areaVal * 500) / 10000;
        unitLabel = "sào Trung Bộ";
    } else if (unit === 'sao_bac_bo') {
        areaInHa = (areaVal * 360) / 10000;
        unitLabel = "sào Bắc Bộ";
    }

    if (displayArea) displayArea.innerText = `${areaVal} ${unitLabel}`;

    // Định mức bình quân trên 1 hecta luân canh:
    // Tiết kiệm chi phí đạm: ~4.300.000 VNĐ / ha
    // Nước tưới tiết kiệm: ~7.300 m3 / ha
    // Đạm sinh học tự cố định: ~52 kg N / ha
    const totalMoney = Math.round(areaInHa * 4300000);
    const totalWater = Math.round(areaInHa * 7300);
    const totalNitrogen = Math.round(areaInHa * 52);

    if (calcMoney) calcMoney.innerText = totalMoney.toLocaleString('vi-VN') + " đ";
    if (calcWater) calcWater.innerText = totalWater.toLocaleString('vi-VN') + " m³";
    if (calcNitrogen) calcNitrogen.innerText = "+" + totalNitrogen.toLocaleString('vi-VN') + " kg N";
}

/**
 * Xuất / In báo cáo tóm tắt kế hoạch mùa vụ (PDF)
 */
function printReport() {
    window.print();
}

/**
 * Cập nhật tọa độ trên giao diện và vị trí của Marker
 */
function updateMarkerAndCoords(lat, lon) {
    if (marker) marker.setLatLng([lat, lon]);
    const latInput = document.getElementById("input-lat");
    const lonInput = document.getElementById("input-lon");
    if (latInput) latInput.value = lat.toFixed(4);
    if (lonInput) lonInput.value = lon.toFixed(4);
}

/**
 * Chọn nhanh các vùng trọng điểm mẫu (Nghệ An, Bến Tre, Tây Nguyên)
 */
function selectPreset(lat, lon, name) {
    document.querySelectorAll('.preset-btn').forEach(btn => btn.classList.remove('active'));
    if (window.event && window.event.currentTarget) {
        window.event.currentTarget.classList.add('active');
    }
    
    if (map) map.setView([lat, lon], 10);
    updateMarkerAndCoords(lat, lon);
    runAnalysis();
}

/**
 * Gửi yêu cầu AJAX tới backend để lấy dữ liệu vệ tinh NASA và kế hoạch luân canh
 */
function runAnalysis() {
    const latInput = document.getElementById("input-lat");
    const lonInput = document.getElementById("input-lon");
    const goalSelect = document.getElementById("select-goal");
    const loading = document.getElementById("loading");

    const lat = parseFloat(latInput ? latInput.value : 18.9950);
    const lon = parseFloat(lonInput ? lonInput.value : 105.4740);
    const goal = goalSelect ? goalSelect.value : 'soil_health';

    if (loading) loading.style.display = "flex";

    fetch(`/api/analyze/?lat=${lat}&lon=${lon}&goal=${goal}`)
        .then(res => res.json())
        .then(data => {
            if (loading) loading.style.display = "none";
            if (data.success) {
                renderDashboard(data.nasa, data.plan);
            } else {
                alert("Lỗi khi tải dữ liệu: " + data.error);
            }
        })
        .catch(err => {
            if (loading) loading.style.display = "none";
            console.error("Lỗi mạng khi gọi API FieldShift:", err);
        });
}

/**
 * Hiển thị dữ liệu lên các thẻ chỉ số KPI, biểu đồ và timeline mùa vụ
 */
function renderDashboard(nasa, plan) {
    // 1. Cập nhật thẻ KPI
    const ana = nasa.analysis;
    const valTmax = document.getElementById("val-tmax");
    const subTmax = document.getElementById("sub-tmax");
    if (valTmax) valTmax.innerText = ana.max_temp;
    if (subTmax) subTmax.innerText = `Đạt đỉnh vào Tháng ${ana.max_temp_month} (${ana.extreme_heat_alert ? 'Cực đoan' : 'Bình thường'})`;

    const valRain = document.getElementById("val-rain");
    const subRain = document.getElementById("sub-rain");
    if (valRain) valRain.innerText = ana.max_rain;
    if (subRain) subRain.innerText = `Đỉnh mưa Tháng ${ana.max_rain_month} (Nguy cơ úng bão)`;

    const valMoist = document.getElementById("val-moist");
    const subMoist = document.getElementById("sub-moist");
    if (valMoist) valMoist.innerText = ana.min_soil_moist;
    if (subMoist) subMoist.innerText = `Khô nẻ vào Tháng ${ana.min_soil_month}`;

    // 2. Cập nhật biểu đồ Thời tiết NASA
    renderWeatherChart(nasa.months_vn, nasa.data.t2m_max, nasa.data.precipitation);

    // 3. Cập nhật biểu đồ Độ ẩm đất NASA
    renderSoilChart(nasa.months_vn, nasa.data.gwet_top, nasa.data.gwet_root);

    // 4. Cập nhật tóm tắt và lộ trình luân canh 3 vụ
    const recText = document.getElementById("recommendation-text");
    if (recText) recText.innerText = plan.recommendation_summary;
    renderTimeline(plan.schedule);
}

/**
 * Trực quan hóa 3 vụ mùa luân canh dưới dạng các thẻ timeline
 */
function renderTimeline(schedule) {
    const container = document.getElementById("timeline-container");
    if (!container) return;
    container.innerHTML = "";

    schedule.forEach((season, idx) => {
        const isHighlight = idx === 1; // Vụ hè thu là trọng tâm luân canh thích ứng
        const card = document.createElement("div");
        card.className = `season-card ${isHighlight ? 'highlight' : ''}`;
        card.innerHTML = `
            <div class="season-top">
                <span class="season-tag">${season.season_name.split(':')[0]}</span>
                <span class="season-icon">${season.icon}</span>
            </div>
            <div class="season-crop">${season.recommended_crop}</div>
            <div class="season-meta">
                <span><i class="fa-regular fa-clock"></i> ${season.growth_days}</span>
                <span><i class="fa-solid fa-tag"></i> ${season.crop_type}</span>
            </div>
            <div class="season-desc">${season.why}</div>
            <div class="season-action">
                <strong>Hành động đất:</strong> ${season.soil_action}
            </div>
        `;
        container.appendChild(card);
    });
}

/**
 * Vẽ biểu đồ Nhiệt độ & Lượng mưa bằng Chart.js
 */
function renderWeatherChart(labels, temps, rains) {
    const canvas = document.getElementById('weatherChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (weatherChartInstance) weatherChartInstance.destroy();

    weatherChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Lượng mưa (mm/ngày)',
                    data: rains,
                    backgroundColor: 'rgba(56, 189, 248, 0.45)',
                    borderColor: '#38bdf8',
                    borderWidth: 1.5,
                    yAxisID: 'yRain',
                    order: 2
                },
                {
                    label: 'Nhiệt độ Tmax (°C)',
                    data: temps,
                    type: 'line',
                    borderColor: '#f43f5e',
                    backgroundColor: 'rgba(244, 63, 94, 0.1)',
                    borderWidth: 2.5,
                    tension: 0.35,
                    pointBackgroundColor: '#f43f5e',
                    yAxisID: 'yTemp',
                    order: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8', font: { size: 11 } } }
            },
            scales: {
                x: { ticks: { color: '#64748b' }, grid: { display: false } },
                yTemp: {
                    type: 'linear',
                    position: 'left',
                    ticks: { color: '#f43f5e' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    title: { display: true, text: 'Nhiệt độ (°C)', color: '#f43f5e' }
                },
                yRain: {
                    type: 'linear',
                    position: 'right',
                    ticks: { color: '#38bdf8' },
                    grid: { display: false },
                    title: { display: true, text: 'Mưa (mm/ngày)', color: '#38bdf8' }
                }
            }
        }
    });
}

/**
 * Vẽ biểu đồ Độ ẩm đất tầng mặt & tầng rễ bằng Chart.js
 */
function renderSoilChart(labels, topSoil, rootSoil) {
    const canvas = document.getElementById('soilChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (soilChartInstance) soilChartInstance.destroy();

    soilChartInstance = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Độ ẩm tầng mặt (0-5cm)',
                    data: topSoil,
                    borderColor: '#10b981',
                    backgroundColor: 'rgba(16, 185, 129, 0.15)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.35
                },
                {
                    label: 'Độ ẩm tầng rễ (0-100cm)',
                    data: rootSoil,
                    borderColor: '#f59e0b',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.35
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { labels: { color: '#94a3b8', font: { size: 11 } } }
            },
            scales: {
                x: { ticks: { color: '#64748b' }, grid: { display: false } },
                y: {
                    min: 0.4,
                    max: 1.0,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    title: { display: true, text: 'Chỉ số ẩm độ (0 - 1)', color: '#94a3b8' }
                }
            }
        }
    });
}
