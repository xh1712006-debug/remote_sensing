"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import Navbar from "@/components/Navbar";
import WeatherCharts from "@/components/WeatherCharts";
import {
  Thermometer,
  CloudRain,
  Droplets,
  Activity,
  Calculator,
  ShieldAlert,
  Calendar,
  Sparkles,
  ArrowRight,
  TrendingUp,
  MapPin,
  RefreshCw,
} from "lucide-react";

// Dynamically import MapComponent to disable SSR for Leaflet
const MapComponent = dynamic(() => import("@/components/MapComponent"), {
  ssr: false,
  loading: () => (
    <div className="h-[380px] w-full rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-center text-slate-400 text-xs">
      Đang tải bản đồ vệ tinh viễn thám...
    </div>
  ),
});

export default function DashboardPage() {
  const [lat, setLat] = useState<number>(18.995);
  const [lon, setLon] = useState<number>(105.474);
  const [goal, setGoal] = useState<string>("soil_health");
  const [area, setArea] = useState<number>(1.0);
  const [areaUnit, setAreaUnit] = useState<string>("ha");
  const [loading, setLoading] = useState<boolean>(false);
  const [activePreset, setActivePreset] = useState<string>("nghe_an");

  // Fallback initial data
  const [analysisResult, setAnalysisResult] = useState<any>({
    nasa: {
      analysis: {
        max_temp: 41.23,
        max_rain: 13.71,
        min_root_moisture: 0.28,
        extreme_heat_alert: true,
        flood_risk_alert: true,
      },
    },
    plan: {
      schedule: [
        {
          season_name: "Vụ 1: Vụ Đông Xuân (Tháng 1 – Tháng 5)",
          weather_summary: "Thời tiết mát mẻ ấm dần, độ ẩm đất ổn định (0.68 - 0.76).",
          recommended_crop: "Lúa thuần chất lượng cao (Jasmine / ST24)",
          crop_type: "Ngũ cốc",
          growth_days: "105 - 115 ngày",
          why: "Tận dụng nguồn nước tích trữ đầu năm và điều kiện nhiệt độ lý tưởng (22 - 28°C) để đạt sản lượng lúa chính trong năm.",
          soil_action: "Bón lót phân chuồng ủ hoai và vôi bột để ổn định pH đất sau mùa đông.",
          icon: "🌾",
        },
        {
          season_name: "Vụ 2: Vụ Hè Thu (Tháng 5 – Tháng 8) [Ứng phó Nắng Nóng & Gió Lào]",
          weather_summary: "Dữ liệu NASA cảnh báo nhiệt độ đỉnh điểm đạt 41.23°C, hạn hán cục bộ.",
          recommended_crop: "Lạc (Đậu phộng) Sen Thọ / L14 hoặc Mè đen chịu hạn",
          crop_type: "Cây họ Đậu cố định đạm (Legume)",
          growth_days: "80 - 90 ngày",
          why: "KHÔNG trồng lúa vụ này. Cây lạc chịu được nhiệt độ >40°C, tiêu thụ nước chỉ bằng 30% lúa. Đặc biệt có nốt sần rễ giúp tự cố định 40 - 60 kg Nitơ (Đạm)/ha tự nhiên vào đất.",
          soil_action: "Sau khi thu hoạch củ, cày vùi toàn bộ thân lá lạc vào ruộng để làm phân xanh tăng hàm lượng mùn hữu cơ (SOC).",
          icon: "🥜",
        },
        {
          season_name: "Vụ 3: Vụ Thu Đông (Tháng 9 – Tháng 12) [Ứng phó Mưa Bão Lũ]",
          weather_summary: "Dữ liệu NASA ghi nhận mưa bão đạt đỉnh (13.71 mm/ngày vào tháng 9-10). Nguy cơ ngập úng cao.",
          recommended_crop: "Ngô nếp vụ đông / Khoai lang Hoàng Long (Gieo sau 15/10 khi lũ rút)",
          crop_type: "Cây lấy củ & màu ưa lạnh",
          growth_days: "85 - 95 ngày",
          why: "Tránh đỉnh lũ tháng 9. Đưa cây khoai lang/ngô vào vừa tận dụng phù sa bồi đắp sau mưa lũ, vừa tạo lớp thảm thực vật chống xói mòn rửa trôi đất tầng mặt.",
          soil_action: "Lên luống cao thoát nước, tận dụng đất phù sa tơi xốp.",
          icon: "🍠",
        },
      ],
      comparison: {
        monoculture: {
          title: "Nếu tiếp tục độc canh (Lúa 3 vụ/năm)",
          soil_health_score: 42,
          soil_status: "Báo động: Đất bạc màu, chai cứng, suy kiệt mùn hữu cơ",
          water_consumption_m3: 14500,
          chemical_fertilizer_cost_vnđ: "7.800.000 đ/ha",
          drought_flood_risk: "85% (Rất cao: Dễ mất trắng lúa hè thu vì gió Lào)",
        },
        crop_rotation: {
          title: "Áp dụng luân canh thích ứng dữ liệu NASA (Lúa ➔ Lạc ➔ Khoai lang)",
          soil_health_score: 89,
          soil_status: "Tối ưu: Đất tơi xốp, giàu đạm tự nhiên, cắt đứt sâu bệnh",
          water_consumption_m3: 7200,
          chemical_fertilizer_cost_vnđ: "3.500.000 đ/ha (Tiết kiệm 55% chi phí đạm)",
          drought_flood_risk: "18% (Rất thấp: Né được cả khô hạn lẫn bão lũ)",
          nitrogen_added_kg_ha: "+52 kg N/ha (Nhờ nốt sần cây họ đậu)",
          water_saved_percent: "50.3%",
        },
      },
    },
  });

  // Fetch API function
  const fetchAnalysis = async (targetLat: number, targetLon: number, targetGoal: string) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/analyze/?lat=${targetLat}&lon=${targetLon}&goal=${targetGoal}`);
      if (res.ok) {
        const data = await res.json();
        if (data.success) {
          setAnalysisResult(data);
        }
      }
    } catch (err) {
      console.warn("Could not reach backend API, using cached simulation", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalysis(lat, lon, goal);
  }, []);

  // Preset selector
  const handleSelectPreset = (pLat: number, pLon: number, presetId: string) => {
    setLat(pLat);
    setLon(pLon);
    setActivePreset(presetId);
    fetchAnalysis(pLat, pLon, goal);
  };

  // Convert area to ha for calculations
  let areaInHa = area;
  let unitName = "ha";
  if (areaUnit === "sao_trung_bo") {
    areaInHa = (area * 500) / 10000;
    unitName = "sào Trung Bộ (500m²)";
  } else if (areaUnit === "sao_bac_bo") {
    areaInHa = (area * 360) / 10000;
    unitName = "sào Bắc Bộ (360m²)";
  }

  const calcSavedMoney = Math.round(areaInHa * 4300000);
  const calcSavedWater = Math.round(areaInHa * 7300);
  const calcAddedNitrogen = Math.round(areaInHa * 52);

  const analysis = analysisResult?.nasa?.analysis || {};
  const schedule = analysisResult?.plan?.schedule || [];
  const comparison = analysisResult?.plan?.comparison || {};

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-8 space-y-6">
        {/* Top Intro Banner */}
        <section className="glass-card p-5 lg:p-6 rounded-2xl relative overflow-hidden">
          <div className="absolute -right-12 -top-12 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none" />
          <div className="relative z-10 space-y-2">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider text-emerald-400 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                Thử Thách: Field Shift - Adapting Farms with NASA Data
              </span>
              <span className="text-xs text-slate-400">
                Tích Hợp Vệ Tinh Viễn Thám MERRA-2 & SMAP
              </span>
            </div>
            <h1 className="text-xl lg:text-2xl font-extrabold text-slate-100">
              Chuyển Đổi Vụ Mùa Thích Ứng Khí Hậu Cực Đoan & Phục Hồi Độ Phì Đất
            </h1>
            <p className="text-xs lg:text-sm text-slate-300 max-w-4xl leading-relaxed">
              Giải pháp hỗ trợ nông hộ vượt qua 2 cú sốc khí hậu đo lường từ vệ tinh NASA:{" "}
              <strong className="text-rose-400">nắng nóng gay gắt do gió Lào (&gt;40°C)</strong> vào vụ hè thu và{" "}
              <strong className="text-sky-400">mưa bão dồn dập ngập úng</strong> vào vụ đông, thay thế độc canh lúa
              bằng công thức luân canh phục hồi sinh thái.
            </p>
          </div>
        </section>

        {/* Main 2-Column Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* LEFT COLUMN: Map & Farmer Inputs (5 cols) */}
          <div className="lg:col-span-5 space-y-4">
            {/* Presets */}
            <div className="glass-card p-4 rounded-xl space-y-2">
              <label className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5 text-emerald-400" /> Vùng Khí Hậu Thí Điểm:
              </label>
              <div className="grid grid-cols-3 gap-2">
                <button
                  type="button"
                  onClick={() => handleSelectPreset(18.995, 105.474, "nghe_an")}
                  className={`p-2 rounded-lg text-xs font-semibold border transition text-left ${
                    activePreset === "nghe_an"
                      ? "bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-sm shadow-emerald-500/20"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <div>🌾 Nghệ An</div>
                  <div className="text-[10px] text-rose-400 font-normal">Gió Lào &gt;40°C</div>
                </button>
                <button
                  type="button"
                  onClick={() => handleSelectPreset(10.2433, 106.3753, "ben_tre")}
                  className={`p-2 rounded-lg text-xs font-semibold border transition text-left ${
                    activePreset === "ben_tre"
                      ? "bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-sm shadow-emerald-500/20"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <div>🥥 Bến Tre</div>
                  <div className="text-[10px] text-amber-400 font-normal">Hạn mặn ĐBSCL</div>
                </button>
                <button
                  type="button"
                  onClick={() => handleSelectPreset(12.67, 108.04, "dak_lak")}
                  className={`p-2 rounded-lg text-xs font-semibold border transition text-left ${
                    activePreset === "dak_lak"
                      ? "bg-emerald-500/20 border-emerald-500 text-emerald-300 shadow-sm shadow-emerald-500/20"
                      : "bg-slate-900/60 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  <div>☕ Đắk Lắk</div>
                  <div className="text-[10px] text-orange-400 font-normal">Hạn đất Bazan</div>
                </button>
              </div>
            </div>

            {/* Interactive Leaflet Satellite GIS Map */}
            <div className="glass-card p-4 rounded-xl">
              <MapComponent
                lat={lat}
                lon={lon}
                onCoordChange={(nLat, nLon) => {
                  setLat(nLat);
                  setLon(nLon);
                  setActivePreset("custom");
                  fetchAnalysis(nLat, nLon, goal);
                }}
              />
            </div>

            {/* Inputs & Goal Form */}
            <div className="glass-card p-4 rounded-xl space-y-3 text-xs">
              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-slate-400 font-semibold mb-1 block">Vĩ Độ (Lat)</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={lat}
                    onChange={(e) => setLat(parseFloat(e.target.value) || 0)}
                    className="w-full bg-slate-900/80 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-slate-100 outline-none focus:border-emerald-500"
                  />
                </div>
                <div>
                  <label className="text-slate-400 font-semibold mb-1 block">Kinh Độ (Lon)</label>
                  <input
                    type="number"
                    step="0.0001"
                    value={lon}
                    onChange={(e) => setLon(parseFloat(e.target.value) || 0)}
                    className="w-full bg-slate-900/80 border border-slate-700/80 rounded-lg px-2.5 py-1.5 text-slate-100 outline-none focus:border-emerald-500"
                  />
                </div>
              </div>

              <div>
                <label className="text-slate-400 font-semibold mb-1 block">Mục Tiêu Ưu Tiên Của Nông Dân:</label>
                <select
                  value={goal}
                  onChange={(e) => {
                    setGoal(e.target.value);
                    fetchAnalysis(lat, lon, e.target.value);
                  }}
                  className="w-full bg-slate-900/80 border border-slate-700/80 rounded-lg px-2.5 py-2 text-slate-100 outline-none focus:border-emerald-500 text-xs"
                >
                  <option value="soil_health">🌱 Cải tạo đất & Bổ sung Đạm sinh học (Tối ưu)</option>
                  <option value="water_saving">💧 Tiết kiệm nước & Chống chịu hạn hán</option>
                  <option value="economic_balance">💰 Cân bằng kinh tế & Phòng ngừa thiên tai</option>
                </select>
              </div>

              {/* Area Input & Economic Estimator */}
              <div className="p-3 rounded-lg bg-slate-900/90 border border-slate-800 space-y-2">
                <div className="flex items-center justify-between text-slate-300 font-semibold">
                  <span className="flex items-center gap-1.5 text-emerald-400">
                    <Calculator className="w-3.5 h-3.5" /> Diện Tích Đất Của Hộ Nông Dân:
                  </span>
                  <span className="text-[11px] text-slate-400">
                    {area} {unitName}
                  </span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <input
                    type="number"
                    min="0.1"
                    step="0.1"
                    value={area}
                    onChange={(e) => setArea(parseFloat(e.target.value) || 1.0)}
                    className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-100 outline-none focus:border-emerald-500"
                  />
                  <select
                    value={areaUnit}
                    onChange={(e) => setAreaUnit(e.target.value)}
                    className="w-full bg-slate-800 border border-slate-700 rounded px-2 py-1 text-slate-100 outline-none focus:border-emerald-500"
                  >
                    <option value="ha">Hecta (ha)</option>
                    <option value="sao_trung_bo">Sào Trung Bộ (500m²)</option>
                    <option value="sao_bac_bo">Sào Bắc Bộ (360m²)</option>
                  </select>
                </div>

                {/* Real-time Economic Results */}
                <div className="grid grid-cols-3 gap-2 pt-2 border-t border-slate-800 text-center">
                  <div className="p-1.5 rounded bg-slate-800/60 border border-slate-700/40">
                    <div className="text-[10px] text-slate-400">Tiết Kiệm Phân Bón</div>
                    <div className="font-bold text-emerald-400 text-xs">
                      {calcSavedMoney.toLocaleString("vi-VN")} đ
                    </div>
                  </div>
                  <div className="p-1.5 rounded bg-slate-800/60 border border-slate-700/40">
                    <div className="text-[10px] text-slate-400">Nước Tưới Giảm</div>
                    <div className="font-bold text-sky-400 text-xs">
                      {calcSavedWater.toLocaleString("vi-VN")} m³
                    </div>
                  </div>
                  <div className="p-1.5 rounded bg-slate-800/60 border border-slate-700/40">
                    <div className="text-[10px] text-slate-400">Đạm Tự Nhiên</div>
                    <div className="font-bold text-amber-400 text-xs">
                      +{calcAddedNitrogen} kg N
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Button */}
              <button
                type="button"
                onClick={() => fetchAnalysis(lat, lon, goal)}
                disabled={loading}
                className="w-full py-2.5 rounded-lg bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition transform active:scale-[0.99]"
              >
                {loading ? (
                  <>
                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                    <span>Đang đồng bộ dữ liệu NASA...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Cập Nhật Đề Xuất Luân Canh</span>
                  </>
                )}
              </button>
            </div>
          </div>

          {/* RIGHT COLUMN: KPIs, Rotation Schedule, Charts & Matrix (7 cols) */}
          <div className="lg:col-span-7 space-y-5">
            {/* 4 Live KPI Cards */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {/* Temp */}
              <div className="glass-card p-3 rounded-xl border-l-4 border-l-rose-500 space-y-1">
                <div className="flex items-center justify-between text-slate-400 text-[11px]">
                  <span>Nhiệt Độ Đỉnh</span>
                  <Thermometer className="w-3.5 h-3.5 text-rose-400" />
                </div>
                <div className="text-lg lg:text-xl font-extrabold text-slate-100">
                  {analysis.max_temp || 41.23}°C
                </div>
                <div className="text-[10px] text-rose-400 font-medium">Cảnh báo Gió Lào T5–7</div>
              </div>

              {/* Rain */}
              <div className="glass-card p-3 rounded-xl border-l-4 border-l-sky-500 space-y-1">
                <div className="flex items-center justify-between text-slate-400 text-[11px]">
                  <span>Mưa Lũ Đỉnh</span>
                  <CloudRain className="w-3.5 h-3.5 text-sky-400" />
                </div>
                <div className="text-lg lg:text-xl font-extrabold text-slate-100">
                  {analysis.max_rain || 13.71} <span className="text-xs font-normal">mm/d</span>
                </div>
                <div className="text-[10px] text-sky-400 font-medium">Báo động ngập lụt T9–10</div>
              </div>

              {/* Soil Root Moisture */}
              <div className="glass-card p-3 rounded-xl border-l-4 border-l-amber-500 space-y-1">
                <div className="flex items-center justify-between text-slate-400 text-[11px]">
                  <span>Ẩm Đất Tầng Rễ</span>
                  <Droplets className="w-3.5 h-3.5 text-amber-400" />
                </div>
                <div className="text-lg lg:text-xl font-extrabold text-slate-100">
                  {analysis.min_root_moisture || 0.28} <span className="text-xs font-normal">GWET</span>
                </div>
                <div className="text-[10px] text-amber-400 font-medium">Đất nứt nẻ vụ hè</div>
              </div>

              {/* Soil Health Score */}
              <div className="glass-card p-3 rounded-xl border-l-4 border-l-emerald-500 space-y-1">
                <div className="flex items-center justify-between text-slate-400 text-[11px]">
                  <span>Điểm Sức Khỏe Đất</span>
                  <Activity className="w-3.5 h-3.5 text-emerald-400" />
                </div>
                <div className="text-lg lg:text-xl font-extrabold text-emerald-400 flex items-baseline gap-1">
                  89 <span className="text-xs text-slate-400 font-normal">/ 100</span>
                </div>
                <div className="text-[10px] text-emerald-400 font-medium">Tăng +47đ (vs Độc canh)</div>
              </div>
            </div>

            {/* 3-Season Rotation Timeline Cards */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <h3 className="font-extrabold text-sm text-slate-100 flex items-center gap-2">
                  <Calendar className="w-4 h-4 text-emerald-400" /> Kế Hoạch Luân Canh 3 Vụ Thích Ứng Khí Hậu NASA:
                </h3>
                <span className="text-[11px] text-emerald-400 font-medium bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-900/60">
                  Phục hồi hệ sinh thái
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                {schedule.map((season: any, idx: number) => (
                  <div
                    key={idx}
                    className="glass-card p-3.5 rounded-xl border border-slate-800 space-y-2 hover:border-emerald-500/50 transition"
                  >
                    <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                      <span className="text-lg">{season.icon || "🌱"}</span>
                      <span className="text-[10px] uppercase font-bold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">
                        {season.growth_days || "90 ngày"}
                      </span>
                    </div>

                    <div>
                      <h4 className="font-bold text-xs text-slate-200">{season.season_name}</h4>
                      <div className="text-emerald-400 font-extrabold text-xs mt-1">
                        {season.recommended_crop}
                      </div>
                    </div>

                    <p className="text-[11px] text-slate-300 leading-relaxed bg-slate-900/60 p-2 rounded border border-slate-800/60">
                      <strong>Lý do nông học:</strong> {season.why}
                    </p>

                    <div className="text-[10px] text-amber-300/90 pt-1">
                      <strong>Cải tạo đất:</strong> {season.soil_action}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Charts Section */}
            <WeatherCharts />

            {/* Comparison Matrix */}
            <div className="glass-card p-4 rounded-xl space-y-3">
              <h3 className="font-extrabold text-sm text-slate-100 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-emerald-400" /> Bảng So Sánh Hiệu Quả: Độc Canh vs. Luân Canh NASA
              </h3>

              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr className="border-b border-slate-800 text-slate-400 uppercase text-[10px]">
                      <th className="py-2 px-3">Tiêu Chí Đánh Giá</th>
                      <th className="py-2 px-3 text-rose-400">Độc Canh Lúa (3 Vụ/Năm)</th>
                      <th className="py-2 px-3 text-emerald-400 font-bold">Luân Canh FieldShift</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-800/60 text-slate-300">
                    <tr>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">Điểm Sức Khỏe Đất (SHS)</td>
                      <td className="py-2.5 px-3 text-rose-400 font-bold">42 / 100 (Bạc màu)</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-extrabold">89 / 100 (+47đ tối ưu)</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">Nhu Cầu Nước Tưới</td>
                      <td className="py-2.5 px-3">14.500 m³/ha</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-bold">7.200 m³/ha (Tiết kiệm 50.3%)</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">Chi Phí Đạm Hóa Học</td>
                      <td className="py-2.5 px-3 text-rose-300">7.800.000 đ/ha</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-bold">3.500.000 đ/ha (Tiết kiệm 55%)</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">Bổ Sung Đạm Tự Nhiên</td>
                      <td className="py-2.5 px-3 text-slate-500">0 kg N (Kiệt quệ)</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-bold">+52 kg N/ha (Nốt sần vi khuẩn)</td>
                    </tr>
                    <tr>
                      <td className="py-2.5 px-3 font-semibold text-slate-200">Rủi Ro Khô Hạn & Lũ</td>
                      <td className="py-2.5 px-3 text-rose-400 font-bold">85% (Mất trắng vụ hè)</td>
                      <td className="py-2.5 px-3 text-emerald-400 font-bold">18% (Né hạn và bão lũ)</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#0b1120] py-6 px-4 text-center text-xs text-slate-400 space-y-2 no-print">
        <div className="flex flex-wrap items-center justify-center gap-4 text-slate-400">
          <span>Dự Án: <strong>FieldShift</strong></span>
          <span>•</span>
          <span>Thử Thách: <strong>NASA Space Apps Challenge 2026</strong></span>
          <span>•</span>
          <span>Nền Tảng: <strong>Next.js 15 + Django 6 REST API + PostgreSQL 18</strong></span>
        </div>
        <p className="text-[11px] text-slate-400">
          Dữ liệu viễn thám Trái đất cung cấp bởi NASA POWER Agroclimatology API, MERRA-2, và NASA SMAP.
        </p>
      </footer>
    </div>
  );
}
