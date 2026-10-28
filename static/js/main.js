/**
 * FieldShift - NASA Space Apps Challenge
 * Client-side script handling Leaflet interactive satellite map, AJAX NASA API calls, and Chart.js visualizations.
 */

let map, marker;
let weatherChartInstance = null;
let soilChartInstance = null;

// Quản lý các lớp bản đồ nền (Basemaps)
let baseLayers = {};
let currentBaseLayer = null;
let labelLayer = null;

// Quản lý 3 lớp chuyên đề (Thematic Overlays)
let thematicLayers = {
    drought: null,
    rain: null,
    salinity: null
};
let activeThematic = 'drought';
let currentOpacity = 0.65;

// Khởi tạo bản đồ vệ tinh Leaflet khi DOM sẵn sàng
document.addEventListener("DOMContentLoaded", function() {
    const latInput = document.getElementById("input-lat");
    const lonInput = document.getElementById("input-lon");
    const initLat = parseFloat(latInput ? latInput.value : 18.9950) || 18.9950;
    const initLon = parseFloat(lonInput ? lonInput.value : 105.4740) || 105.4740;

    // Khởi tạo đối tượng Leaflet Map
    map = L.map('map', {
        center: [initLat, initLon],
        zoom: 9,
        maxZoom: 19
    });

    // 1. Định nghĩa các lớp bản đồ nền chuyên nghiệp
    baseLayers['esri_clarity'] = L.tileLayer('https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        attribution: 'Tiles &copy; Esri Clarity (Cloud-Free Archive)',
        maxZoom: 19
    });

    baseLayers['google_hybrid'] = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}', {
        attribution: 'Tiles &copy; Google Hybrid Satellite',
        maxZoom: 20
    });

    baseLayers['osm'] = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap (Kênh mương & Thửa ruộng)',
        maxZoom: 19
    });

    baseLayers['carto_dark'] = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; CARTO Dark Matter',
        maxZoom: 19
    });

    // Lớp nhãn địa danh đường thôn xóm trong suốt
    labelLayer = L.tileLayer('https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19
    });

    // Kích hoạt mặc định lớp Vệ tinh Không mây (Esri Clarity) + Nhãn
    currentBaseLayer = baseLayers['esri_clarity'];
    currentBaseLayer.addTo(map);
    labelLayer.addTo(map);

    // 2. Xây dựng 3 lớp chuyên đề nông nghiệp viễn thám NASA
    initThematicLayers();

    // Kích hoạt mặc định lớp Khô hạn đất (NASA SMAP)
    if (thematicLayers['drought']) {
        thematicLayers['drought'].addTo(map);
        updateLegendUI('drought');
    }

    // 3. Marker vị trí nông trại có thể kéo thả
    marker = L.marker([initLat, initLon], { draggable: true }).addTo(map);
    marker.bindPopup("<b>🌾 Vị trí thửa ruộng đang chọn</b><br>Kéo thả hoặc nhấp bản đồ để phân tích viễn thám.").openPopup();

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
 * Xây dựng 3 lớp chuyên đề: Khô Hạn Đất, Lượng Mưa, Xâm Nhập Mặn
 */
function initThematicLayers() {
    // A. Lớp Khô Hạn Đất & Độ Ẩm Tầng Rễ (NASA SMAP / GWETROOT)
    thematicLayers['drought'] = L.layerGroup([
        // Vùng Bắc Trung Bộ (Nghệ An - Hà Tĩnh) - Hạn gay gắt Gió Lào Foehn
        L.polygon([
            [18.0, 105.0], [19.5, 104.7], [19.9, 105.7], [18.9, 106.1], [18.0, 105.7]
        ], {
            color: '#dc2626',
            fillColor: '#ef4444',
            fillOpacity: currentOpacity,
            weight: 2
        }).bindPopup("<b>🔴 Vùng Báo Động Khô Hạn Tầng Rễ (Gió Lào)</b><br>Độ ẩm tầng rễ GWETROOT &lt; 0.35.<br>Đất kiệt nước nứt nẻ.<br><i>Khuyến nghị: Chuyển sang Lạc L14, Sen Thọ, Mè đen.</i>"),

        // Vùng Tây Nguyên (Đắk Lắk - Gia Lai) - Hạn mùa khô bazan
        L.polygon([
            [12.2, 107.6], [13.4, 107.5], [13.6, 108.6], [12.3, 108.7]
        ], {
            color: '#d97706',
            fillColor: '#f59e0b',
            fillOpacity: currentOpacity * 0.9,
            weight: 2
        }).bindPopup("<b>🟡 Vùng Cảnh Báo Thiếu Ẩm Đất Bazan</b><br>Độ ẩm rễ ~0.40.<br><i>Khuyến nghị: Tưới nhỏ giọt tiết kiệm, tủ bã thực vật giữ ẩm.</i>"),

        // Vùng Đồng bằng Sông Cửu Long (Bến Tre, Trà Vinh)
        L.polygon([
            [9.6, 105.8], [10.4, 106.1], [10.3, 106.8], [9.5, 106.3]
        ], {
            color: '#be185d',
            fillColor: '#ec4899',
            fillOpacity: currentOpacity * 0.9,
            weight: 2
        }).bindPopup("<b>🟣 Vùng Khô Hạn Mùa Khô & Mặn Xâm Lấn</b><br>Cần trữ nước ngọt sớm trước tháng 2.")
    ]);

    // B. Lớp Lượng Mưa & Cảnh Báo Ngập Lụt (NASA GPM)
    thematicLayers['rain'] = L.layerGroup([
        // Vùng Đỉnh Lũ & Mưa Bão Duyên Hải Miền Trung (Tháng 9-10)
        L.polygon([
            [18.1, 105.2], [19.5, 105.1], [19.7, 106.0], [18.2, 106.4]
        ], {
            color: '#1d4ed8',
            fillColor: '#3b82f6',
            fillOpacity: currentOpacity,
            weight: 2
        }).bindPopup("<b>🌧️ Vùng Đỉnh Mưa Lũ NASA GPM (Tháng 9 - 10)</b><br>Lượng mưa đỉnh &gt; 14 mm/ngày.<br>Nguy cơ ngập úng lụt bão rất cao.<br><i>Khuyến nghị: Tránh gieo trồng tháng 9, chỉ xuống giống khoai/ngô sau 15/10 khi lũ rút.</i>"),

        // Vùng Mưa Mùa Tây Nam Bộ
        L.polygon([
            [9.2, 104.8], [10.5, 105.0], [10.2, 106.2], [9.0, 105.5]
        ], {
            color: '#0891b2',
            fillColor: '#06b6d4',
            fillOpacity: currentOpacity * 0.85,
            weight: 2
        }).bindPopup("<b>🌧️ Mưa Mùa Tây Nam (NASA GPM)</b><br>Lượng mưa 8 - 12 mm/ngày, phù hợp lúa vụ Hè Thu.")
    ]);

    // C. Lớp Xâm Nhập Mặn 4‰ & 1‰ (ĐBSCL & Duyên Hải)
    thematicLayers['salinity'] = L.layerGroup([
        // Ranh mặn 4‰ ĐBSCL (Cửa Đại, Hàm Luông, Cổ Chiên - Bến Tre)
        L.polygon([
            [10.15, 106.35], [10.38, 106.65], [10.10, 106.82], [9.90, 106.60]
        ], {
            color: '#991b1b',
            fillColor: '#dc2626',
            fillOpacity: currentOpacity,
            weight: 2
        }).bindPopup("<b>🔴 Ranh Mặn 4‰ (Bến Tre - Hàm Luông / Cổ Chiên)</b><br>Độ mặn &gt; 4g/l cách cửa biển 35 - 45km.<br><b>NGUY HIỂM:</b> Lúa cháy mầm nếu bơm nước.<br><i>Bắt buộc đóng cống ngăn mặn, chuyển sang mô hình Lúa - Tôm.</i>"),

        // Ranh mặn 1‰ ĐBSCL (Vùng đệm vàng)
        L.polygon([
            [10.28, 106.15], [10.48, 106.45], [10.25, 106.68], [9.85, 106.40]
        ], {
            color: '#ca8a04',
            fillColor: '#eab308',
            fillOpacity: currentOpacity * 0.85,
            weight: 2
        }).bindPopup("<b>🟡 Ranh Mặn 1‰ (Vùng đệm cảnh báo)</b><br>Độ mặn 1g/l - 4g/l.<br>Cần kiểm tra độ mặn trước khi vận hành trạm bơm tưới."),

        // Vùng Cửa Lò - Sông Lam (Nghệ An)
        L.polygon([
            [18.70, 105.65], [18.82, 105.75], [18.75, 105.80], [18.68, 105.70]
        ], {
            color: '#ea580c',
            fillColor: '#f97316',
            fillOpacity: currentOpacity * 0.9,
            weight: 2
        }).bindPopup("<b>🟠 Vùng Nhiễm Mặn Cửa Sông Lam (Mùa kiệt)</b><br>Triều mặn dâng sâu vào hạ lưu sông Lam khi nước thượng nguồn kiệt.")
    ]);
}

/**
 * Đổi lớp bản đồ nền (Esri Clarity không mây, Google Hybrid, OSM, Carto Dark)
 */
function changeBasemap(basemapKey) {
    if (!map || !baseLayers[basemapKey]) return;

    if (currentBaseLayer) {
        map.removeLayer(currentBaseLayer);
    }

    currentBaseLayer = baseLayers[basemapKey];
    currentBaseLayer.addTo(map);

    // Lớp nhãn chỉ cần cho vệ tinh Esri
    if (basemapKey === 'esri_clarity') {
        if (!map.hasLayer(labelLayer)) labelLayer.addTo(map);
    } else {
        if (map.hasLayer(labelLayer)) map.removeLayer(labelLayer);
    }
}

/**
 * Bật / Tắt các lớp dữ liệu chuyên đề (Khô hạn, Lượng mưa, Xâm nhập mặn)
 */
function toggleThematicLayer(layerKey) {
    const btn = document.getElementById(`btn-layer-${layerKey}`);
    const isCurrentlyActive = (activeThematic === layerKey);

    // Gỡ tất cả lớp chuyên đề
    Object.keys(thematicLayers).forEach(k => {
        if (thematicLayers[k] && map.hasLayer(thematicLayers[k])) {
            map.removeLayer(thematicLayers[k]);
        }
        const b = document.getElementById(`btn-layer-${k}`);
        if (b) b.classList.remove('active');
    });

    if (isCurrentlyActive) {
        // Tắt lớp nếu bấm lại chính nó
        activeThematic = null;
        const legend = document.getElementById("map-legend");
        if (legend) legend.style.display = "none";
    } else {
        // Kích hoạt lớp mới
        activeThematic = layerKey;
        if (thematicLayers[layerKey]) {
            thematicLayers[layerKey].addTo(map);
        }
        if (btn) btn.classList.add('active');
        updateLegendUI(layerKey);
        const legend = document.getElementById("map-legend");
        if (legend) legend.style.display = "block";
    }
}

/**
 * Cập nhật nội dung bảng chú giải màu (Legend)
 */
function updateLegendUI(layerKey) {
    const title = document.getElementById("legend-title");
    const items = document.getElementById("legend-items");
    if (!title || !items) return;

    if (layerKey === 'drought') {
        title.innerHTML = "🏜️ Cảnh báo Khô hạn tầng rễ (NASA SMAP)";
        items.innerHTML = `
            <div class="legend-item"><span class="legend-color-dot" style="background:#ef4444"></span> Hạn cực hạn (&lt;0.35 - Gió Lào)</div>
            <div class="legend-item"><span class="legend-color-dot" style="background:#f59e0b"></span> Thiếu ẩm đất bazan (~0.40)</div>
            <div class="legend-item"><span class="legend-color-dot" style="background:#ec4899"></span> Hạn mùa khô ĐBSCL</div>
        `;
    } else if (layerKey === 'rain') {
        title.innerHTML = "🌧️ Lượng mưa & Ngập úng (NASA GPM)";
        items.innerHTML = `
            <div class="legend-item"><span class="legend-color-dot" style="background:#1d4ed8"></span> Đỉnh mưa lũ Miền Trung (&gt;14 mm/ngày)</div>
            <div class="legend-item"><span class="legend-color-dot" style="background:#06b6d4"></span> Mưa mùa Tây Nam Bộ (8 - 12 mm/ngày)</div>
        `;
    } else if (layerKey === 'salinity') {
        title.innerHTML = "🌊 Cảnh báo Xâm nhập mặn 4‰ & 1‰";
        items.innerHTML = `
            <div class="legend-item"><span class="legend-color-dot" style="background:#dc2626"></span> Ranh mặn &gt;4‰ (Nguy hiểm tuyệt đối)</div>
            <div class="legend-item"><span class="legend-color-dot" style="background:#eab308"></span> Ranh mặn 1‰ - 4‰ (Vùng đệm)</div>
            <div class="legend-item"><span class="legend-color-dot" style="background:#f97316"></span> Triều mặn cửa sông Lam</div>
        `;
    }
}

/**
 * Điều chỉnh độ mờ (Opacity) của các lớp chuyên đề
 */
function changeLayerOpacity(val) {
    currentOpacity = parseFloat(val) || 0.65;
    Object.keys(thematicLayers).forEach(k => {
        const group = thematicLayers[k];
        if (group) {
            group.eachLayer(layer => {
                if (layer.setStyle) {
                    layer.setStyle({ fillOpacity: currentOpacity });
                }
            });
        }
    });
}

/**
 * Bật / Tắt chế độ xem bản đồ Toàn màn hình
 */
function toggleMapFullscreen() {
    const wrapper = document.getElementById("map-wrapper");
    const icon = document.getElementById("expand-icon");
    if (!wrapper) return;

    wrapper.classList.toggle("fullscreen");
    const isFull = wrapper.classList.contains("fullscreen");
    if (icon) icon.innerText = isFull ? "✖" : "⛶";

    setTimeout(() => {
        if (map) map.invalidateSize();
    }, 200);
}

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
    } else if (unit === 'cong_nam_bo') {
        areaInHa = (areaVal * 1000) / 10000;
        unitLabel = "công Nam Bộ";
    } else if (unit === 'm2') {
        areaInHa = areaVal / 10000;
        unitLabel = "m²";
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

    const rawLat = parseFloat(latInput ? latInput.value : 18.9950);
    const rawLon = parseFloat(lonInput ? lonInput.value : 105.4740);
    const lat = isNaN(rawLat) ? 18.9950 : rawLat;
    const lon = isNaN(rawLon) ? 105.4740 : rawLon;
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
                    min: 0.1,
                    max: 1.0,
                    ticks: { color: '#94a3b8' },
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    title: { display: true, text: 'Chỉ số ẩm độ (0 - 1)', color: '#94a3b8' }
                }
            }
        }
    });
}
