"use client";

import React, { useEffect, useRef, useState } from "react";
import L from "leaflet";
import { Maximize2, Minimize2, Layers, Eye } from "lucide-react";

interface MapProps {
  lat: number;
  lon: number;
  onCoordChange: (lat: number, lon: number) => void;
}

export default function MapComponent({ lat, lon, onCoordChange }: MapProps) {
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const markerRef = useRef<L.Marker | null>(null);

  const [basemap, setBasemap] = useState<string>("esri_clarity");
  const [activeOverlay, setActiveOverlay] = useState<"drought" | "rain" | "salinity" | null>("drought");
  const [opacity, setOpacity] = useState<number>(0.65);
  const [isFullscreen, setIsFullscreen] = useState<boolean>(false);

  // References to layers
  const baseLayersRef = useRef<{ [key: string]: L.TileLayer }>({});
  const labelLayerRef = useRef<L.TileLayer | null>(null);
  const thematicLayersRef = useRef<{ [key: string]: L.LayerGroup }>({});

  useEffect(() => {
    if (!mapContainerRef.current) return;
    if (mapInstanceRef.current) return;

    // Fix standard Leaflet icon paths in Next.js
    delete (L.Icon.Default.prototype as any)._getIconUrl;
    L.Icon.Default.mergeOptions({
      iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
      iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
      shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
    });

    const map = L.map(mapContainerRef.current, {
      center: [lat, lon],
      zoom: 9,
      maxZoom: 19,
    });
    mapInstanceRef.current = map;

    // Define Basemaps
    baseLayersRef.current["esri_clarity"] = L.tileLayer(
      "https://clarity.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
      { attribution: "Esri Clarity (Cloud-Free Archive) &copy; Maxar", maxZoom: 19 }
    );

    baseLayersRef.current["google_hybrid"] = L.tileLayer(
      "https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
      { attribution: "Google Hybrid Satellite", maxZoom: 20 }
    );

    baseLayersRef.current["osm"] = L.tileLayer(
      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      { attribution: "&copy; OpenStreetMap", maxZoom: 19 }
    );

    baseLayersRef.current["carto_dark"] = L.tileLayer(
      "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
      { attribution: "&copy; CARTO Dark Matter", maxZoom: 19 }
    );

    labelLayerRef.current = L.tileLayer(
      "https://services.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
      { maxZoom: 19 }
    );

    // Initial base layer: Esri Clarity (Cloud-Free) + labels
    baseLayersRef.current["esri_clarity"].addTo(map);
    labelLayerRef.current.addTo(map);

    // Initial Marker
    const marker = L.marker([lat, lon], { draggable: true }).addTo(map);
    marker.bindPopup("<b>🌾 Vị trí thửa ruộng đang chọn</b><br>Kéo thả hoặc nhấp bản đồ để đổi vị trí.").openPopup();
    markerRef.current = marker;

    marker.on("dragend", () => {
      const pos = marker.getLatLng();
      onCoordChange(Number(pos.lat.toFixed(4)), Number(pos.lng.toFixed(4)));
    });

    map.on("click", (e: L.LeafletMouseEvent) => {
      marker.setLatLng(e.latlng);
      onCoordChange(Number(e.latlng.lat.toFixed(4)), Number(e.latlng.lng.toFixed(4)));
    });

    // Initialize 3 Thematic Overlays
    // 1. Drought layer (NASA SMAP)
    thematicLayersRef.current["drought"] = L.layerGroup([
      L.polygon(
        [
          [18.0, 105.0],
          [19.5, 104.7],
          [19.9, 105.7],
          [18.9, 106.1],
          [18.0, 105.7],
        ],
        { color: "#dc2626", fillColor: "#ef4444", fillOpacity: opacity, weight: 2 }
      ).bindPopup(
        "<b>🔴 Vùng Báo Động Khô Hạn Tầng Rễ (Gió Lào Foehn)</b><br>Độ ẩm tầng rễ GWETROOT &lt; 0.35.<br>Khuyến nghị: Thay lúa hè thu bằng Lạc L14, Sen Thọ, Mè đen."
      ),
      L.polygon(
        [
          [12.2, 107.6],
          [13.4, 107.5],
          [13.6, 108.6],
          [12.3, 108.7],
        ],
        { color: "#d97706", fillColor: "#f59e0b", fillOpacity: opacity * 0.9, weight: 2 }
      ).bindPopup("<b>🟡 Vùng Thiếu Ẩm Đất Bazan Tây Nguyên</b><br>Độ ẩm rễ ~0.40. Tưới nhỏ giọt tiết kiệm."),
      L.polygon(
        [
          [9.6, 105.8],
          [10.4, 106.1],
          [10.3, 106.8],
          [9.5, 106.3],
        ],
        { color: "#be185d", fillColor: "#ec4899", fillOpacity: opacity * 0.9, weight: 2 }
      ).bindPopup("<b>🟣 Vùng Khô Hạn Mùa Khô & Mặn Xâm Lấn ĐBSCL</b>"),
    ]);

    // 2. Rain layer (NASA GPM)
    thematicLayersRef.current["rain"] = L.layerGroup([
      L.polygon(
        [
          [18.1, 105.2],
          [19.5, 105.1],
          [19.7, 106.0],
          [18.2, 106.4],
        ],
        { color: "#1d4ed8", fillColor: "#3b82f6", fillOpacity: opacity, weight: 2 }
      ).bindPopup(
        "<b>🌧️ Vùng Đỉnh Mưa Lũ NASA GPM (Tháng 9-10)</b><br>Lượng mưa đỉnh &gt;14 mm/ngày.<br>Nguy cơ ngập úng cao. Xuống giống vụ đông sau 15/10."
      ),
      L.polygon(
        [
          [9.2, 104.8],
          [10.5, 105.0],
          [10.2, 106.2],
          [9.0, 105.5],
        ],
        { color: "#0891b2", fillColor: "#06b6d4", fillOpacity: opacity * 0.85, weight: 2 }
      ).bindPopup("<b>🌧️ Mưa Mùa Tây Nam Bộ (NASA GPM)</b><br>Lượng mưa 8 - 12 mm/ngày."),
    ]);

    // 3. Salinity layer (4‰ & 1‰)
    thematicLayersRef.current["salinity"] = L.layerGroup([
      L.polygon(
        [
          [10.15, 106.35],
          [10.38, 106.65],
          [10.1, 106.82],
          [9.9, 106.6],
        ],
        { color: "#991b1b", fillColor: "#dc2626", fillOpacity: opacity, weight: 2 }
      ).bindPopup(
        "<b>🔴 Ranh Mặn 4‰ (Bến Tre - Hàm Luông / Cổ Chiên)</b><br>Nồng độ mặn &gt;4g/l cách biển 35-45km.<br><b>NGUY HIỂM:</b> Lúa cháy mầm nếu bơm nước."
      ),
      L.polygon(
        [
          [10.28, 106.15],
          [10.48, 106.45],
          [10.25, 106.68],
          [9.85, 106.4],
        ],
        { color: "#ca8a04", fillColor: "#eab308", fillOpacity: opacity * 0.85, weight: 2 }
      ).bindPopup("<b>🟡 Ranh Mặn 1‰ (Vùng đệm cảnh báo)</b><br>Độ mặn 1g/l - 4g/l."),
      L.polygon(
        [
          [18.7, 105.65],
          [18.82, 105.75],
          [18.75, 105.8],
          [18.68, 105.7],
        ],
        { color: "#ea580c", fillColor: "#f97316", fillOpacity: opacity * 0.9, weight: 2 }
      ).bindPopup("<b>🟠 Vùng Nhiễm Mặn Cửa Sông Lam (Mùa kiệt)</b>"),
    ]);

    // Default activate drought layer
    thematicLayersRef.current["drought"].addTo(map);

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // Update center when props change
  useEffect(() => {
    if (mapInstanceRef.current && markerRef.current) {
      const current = markerRef.current.getLatLng();
      if (current.lat !== lat || current.lng !== lon) {
        markerRef.current.setLatLng([lat, lon]);
        mapInstanceRef.current.setView([lat, lon], mapInstanceRef.current.getZoom());
      }
    }
  }, [lat, lon]);

  // Handle basemap change
  const handleBasemapChange = (newBase: string) => {
    setBasemap(newBase);
    const map = mapInstanceRef.current;
    if (!map) return;

    Object.values(baseLayersRef.current).forEach((l) => {
      if (map.hasLayer(l)) map.removeLayer(l);
    });

    if (baseLayersRef.current[newBase]) {
      baseLayersRef.current[newBase].addTo(map);
    }

    if (newBase === "esri_clarity" && labelLayerRef.current) {
      if (!map.hasLayer(labelLayerRef.current)) labelLayerRef.current.addTo(map);
    } else if (labelLayerRef.current && map.hasLayer(labelLayerRef.current)) {
      map.removeLayer(labelLayerRef.current);
    }
  };

  // Handle thematic layer toggle
  const handleOverlayToggle = (key: "drought" | "rain" | "salinity") => {
    const map = mapInstanceRef.current;
    if (!map) return;

    // Remove all thematic layers
    Object.values(thematicLayersRef.current).forEach((l) => {
      if (map.hasLayer(l)) map.removeLayer(l);
    });

    if (activeOverlay === key) {
      setActiveOverlay(null);
    } else {
      setActiveOverlay(key);
      if (thematicLayersRef.current[key]) {
        thematicLayersRef.current[key].addTo(map);
      }
    }
  };

  // Handle opacity change
  const handleOpacityChange = (val: number) => {
    setOpacity(val);
    Object.values(thematicLayersRef.current).forEach((group) => {
      group.eachLayer((layer: any) => {
        if (layer.setStyle) {
          layer.setStyle({ fillOpacity: val });
        }
      });
    });
  };

  // Toggle fullscreen
  const toggleFullscreen = () => {
    setIsFullscreen(!isFullscreen);
    setTimeout(() => {
      if (mapInstanceRef.current) {
        mapInstanceRef.current.invalidateSize();
      }
    }, 200);
  };

  return (
    <div className="space-y-3">
      {/* Map Header & Fullscreen */}
      <div className="flex items-center justify-between text-xs text-slate-300">
        <span className="font-semibold uppercase tracking-wider text-emerald-400 flex items-center gap-1.5">
          <Layers className="w-3.5 h-3.5" /> Bản Đồ Viễn Thám & Dữ Liệu Khí Hậu NASA
        </span>
        <button
          type="button"
          onClick={toggleFullscreen}
          className="flex items-center gap-1 px-2 py-1 rounded bg-slate-800/80 hover:bg-emerald-950/60 border border-slate-700 hover:border-emerald-500 text-slate-300 hover:text-emerald-400 transition"
        >
          {isFullscreen ? <Minimize2 className="w-3 h-3" /> : <Maximize2 className="w-3 h-3" />}
          <span>{isFullscreen ? "Thu nhỏ" : "Toàn màn hình"}</span>
        </button>
      </div>

      {/* Layer Switcher Toolbar */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-lg p-2.5 space-y-2 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 uppercase font-semibold text-[11px] whitespace-nowrap">Lớp nền:</span>
          <select
            value={basemap}
            onChange={(e) => handleBasemapChange(e.target.value)}
            className="flex-1 bg-slate-800/90 border border-slate-700 text-slate-200 rounded px-2 py-1 outline-none focus:border-emerald-500 text-xs"
          >
            <option value="esri_clarity">🛰️ Vệ tinh Không mây (Esri Clarity)</option>
            <option value="google_hybrid">🌍 Vệ tinh Siêu nét + Địa danh (Hybrid)</option>
            <option value="osm">🗺️ Địa hình & Thửa ruộng (OSM)</option>
            <option value="carto_dark">🌙 Nền tối phân tích (CartoDB)</option>
          </select>
        </div>

        <div className="grid grid-cols-3 gap-1.5">
          <button
            type="button"
            onClick={() => handleOverlayToggle("drought")}
            className={`py-1.5 px-2 rounded font-medium transition text-center border ${
              activeOverlay === "drought"
                ? "bg-red-500/20 text-red-300 border-red-500 shadow-sm shadow-red-500/20"
                : "bg-slate-800/50 text-slate-400 border-slate-700/60 hover:text-slate-200"
            }`}
          >
            🏜️ Khô hạn đất
          </button>
          <button
            type="button"
            onClick={() => handleOverlayToggle("rain")}
            className={`py-1.5 px-2 rounded font-medium transition text-center border ${
              activeOverlay === "rain"
                ? "bg-blue-500/20 text-blue-300 border-blue-500 shadow-sm shadow-blue-500/20"
                : "bg-slate-800/50 text-slate-400 border-slate-700/60 hover:text-slate-200"
            }`}
          >
            🌧️ Lượng mưa
          </button>
          <button
            type="button"
            onClick={() => handleOverlayToggle("salinity")}
            className={`py-1.5 px-2 rounded font-medium transition text-center border ${
              activeOverlay === "salinity"
                ? "bg-amber-500/20 text-amber-300 border-amber-500 shadow-sm shadow-amber-500/20"
                : "bg-slate-800/50 text-slate-400 border-slate-700/60 hover:text-slate-200"
            }`}
          >
            🌊 Xâm nhập mặn
          </button>
        </div>
      </div>

      {/* Map Container */}
      <div
        className={`relative border border-slate-800 rounded-xl overflow-hidden transition-all duration-300 ${
          isFullscreen ? "fixed inset-0 z-50 rounded-none w-screen h-screen border-none" : "h-[380px] w-full"
        }`}
      >
        <div ref={mapContainerRef} className="w-full h-full" />

        {/* Floating Legend */}
        {activeOverlay && (
          <div className="absolute bottom-3 right-3 bg-slate-900/90 backdrop-blur-md border border-slate-700/80 rounded-lg p-2.5 z-[1000] text-xs max-w-[260px] shadow-2xl">
            <div className="flex items-center justify-between font-bold text-slate-200 mb-1.5 border-b border-slate-800 pb-1">
              <span>
                {activeOverlay === "drought" && "🏜️ Cảnh báo Hạn đất (NASA SMAP)"}
                {activeOverlay === "rain" && "🌧️ Đỉnh Mưa Lũ (NASA GPM)"}
                {activeOverlay === "salinity" && "🌊 Xâm nhập mặn 4‰ & 1‰"}
              </span>
              <span className="text-[10px] font-semibold text-emerald-400 bg-emerald-950/60 px-1 rounded">LIVE</span>
            </div>

            <div className="space-y-1 text-[11px] text-slate-300">
              {activeOverlay === "drought" && (
                <>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-500 shrink-0" />
                    <span>Hạn gay gắt (&lt;0.35 - Gió Lào)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shrink-0" />
                    <span>Thiếu ẩm đất Bazan (~0.40)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-pink-500 shrink-0" />
                    <span>Hạn mùa khô ĐBSCL</span>
                  </div>
                </>
              )}
              {activeOverlay === "rain" && (
                <>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-blue-600 shrink-0" />
                    <span>Đỉnh mưa lũ Miền Trung (&gt;14 mm/ngày)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-500 shrink-0" />
                    <span>Mưa mùa Tây Nam Bộ (8 - 12 mm/ngày)</span>
                  </div>
                </>
              )}
              {activeOverlay === "salinity" && (
                <>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-red-600 shrink-0" />
                    <span>Ranh mặn &gt;4‰ (Nguy hiểm tuyệt đối)</span>
                  </div>
                  <div className="flex items-center gap-1.5">
                    <span className="w-2.5 h-2.5 rounded-full bg-amber-500 shrink-0" />
                    <span>Ranh mặn 1‰ - 4‰ (Vùng đệm)</span>
                  </div>
                </>
              )}
            </div>

            {/* Opacity slider */}
            <div className="mt-2 pt-1.5 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
              <span className="flex items-center gap-1">
                <Eye className="w-3 h-3 text-slate-400" /> Độ mờ:
              </span>
              <input
                type="range"
                min="0.2"
                max="1.0"
                step="0.05"
                value={opacity}
                onChange={(e) => handleOpacityChange(parseFloat(e.target.value))}
                className="w-20 accent-emerald-500 cursor-pointer"
              />
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
