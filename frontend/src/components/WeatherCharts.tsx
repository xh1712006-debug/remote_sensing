"use client";

import React from "react";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler,
} from "chart.js";
import { Line, Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

interface WeatherChartsProps {
  monthlyData?: {
    months: string[];
    t2m_max: number[];
    precipitation: number[];
    gwet_root: number[];
    gwet_top: number[];
  };
}

export default function WeatherCharts({ monthlyData }: WeatherChartsProps) {
  const months = monthlyData?.months || [
    "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"
  ];
  const t2mMax = monthlyData?.t2m_max || [23, 24, 27, 33, 41.2, 39.8, 40.7, 36.5, 32, 29, 26, 23.5];
  const precip = monthlyData?.precipitation || [1.8, 2.1, 3.2, 4.5, 7.8, 6.2, 5.5, 9.4, 13.7, 12.1, 4.2, 2.0];
  const gwetRoot = monthlyData?.gwet_root || [0.72, 0.70, 0.65, 0.52, 0.32, 0.28, 0.31, 0.48, 0.85, 0.88, 0.76, 0.74];
  const gwetTop = monthlyData?.gwet_top || [0.68, 0.65, 0.58, 0.45, 0.25, 0.20, 0.22, 0.42, 0.90, 0.92, 0.72, 0.70];

  const weatherChartData = {
    labels: months,
    datasets: [
      {
        type: "line" as const,
        label: "Nhiệt độ cực đại T2M_MAX (°C)",
        data: t2mMax,
        borderColor: "#f43f5e",
        backgroundColor: "rgba(244, 63, 94, 0.15)",
        borderWidth: 2.5,
        tension: 0.35,
        yAxisID: "y_temp",
      },
      {
        type: "bar" as const,
        label: "Lượng mưa PRECTOTCORR (mm/ngày)",
        data: precip,
        backgroundColor: "rgba(56, 189, 248, 0.65)",
        borderColor: "#38bdf8",
        borderWidth: 1,
        borderRadius: 4,
        yAxisID: "y_rain",
      },
    ],
  };

  const weatherOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "#94a3b8", font: { size: 11 } },
      },
      tooltip: {
        backgroundColor: "rgba(15, 23, 42, 0.95)",
        titleColor: "#f8fafc",
        bodyColor: "#cbd5e1",
        borderColor: "rgba(255, 255, 255, 0.1)",
        borderWidth: 1,
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(255, 255, 255, 0.05)" },
        ticks: { color: "#94a3b8", font: { size: 10 } },
      },
      y_temp: {
        type: "linear",
        position: "left",
        title: { display: true, text: "Nhiệt độ (°C)", color: "#f43f5e", font: { size: 10 } },
        grid: { color: "rgba(255, 255, 255, 0.05)" },
        ticks: { color: "#f43f5e", font: { size: 10 } },
      },
      y_rain: {
        type: "linear",
        position: "right",
        title: { display: true, text: "Lượng mưa (mm/ngày)", color: "#38bdf8", font: { size: 10 } },
        grid: { drawOnChartArea: false },
        ticks: { color: "#38bdf8", font: { size: 10 } },
      },
    },
  };

  const soilChartData = {
    labels: months,
    datasets: [
      {
        label: "Độ ẩm rễ GWETROOT (0 - 100cm)",
        data: gwetRoot,
        borderColor: "#10b981",
        backgroundColor: "rgba(16, 185, 129, 0.15)",
        borderWidth: 2.5,
        fill: true,
        tension: 0.35,
      },
      {
        label: "Độ ẩm tầng mặt GWETTOP (0 - 5cm)",
        data: gwetTop,
        borderColor: "#f59e0b",
        borderDash: [5, 5],
        borderWidth: 1.8,
        tension: 0.35,
      },
    ],
  };

  const soilOptions: any = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "#94a3b8", font: { size: 11 } },
      },
      tooltip: {
        backgroundColor: "rgba(15, 23, 42, 0.95)",
        titleColor: "#f8fafc",
        bodyColor: "#cbd5e1",
      },
    },
    scales: {
      x: {
        grid: { color: "rgba(255, 255, 255, 0.05)" },
        ticks: { color: "#94a3b8", font: { size: 10 } },
      },
      y: {
        min: 0,
        max: 1.0,
        title: { display: true, text: "Tỷ lệ độ ẩm đất (0.0 - 1.0)", color: "#10b981", font: { size: 10 } },
        grid: { color: "rgba(255, 255, 255, 0.05)" },
        ticks: { color: "#10b981", font: { size: 10 } },
      },
    },
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
      {/* Weather Chart */}
      <div className="glass-card p-4 rounded-xl space-y-2">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <h4 className="font-semibold text-sm text-slate-100 flex items-center gap-1.5">
            📈 Diễn biến Nhiệt độ Cực Đại & Lượng Mưa (NASA POWER)
          </h4>
          <span className="text-[10px] text-rose-400 bg-rose-950/60 border border-rose-900/60 px-1.5 py-0.5 rounded font-medium">
            Gió Lào &gt;40°C
          </span>
        </div>
        <div className="h-[230px] w-full">
          <Line data={weatherChartData as any} options={weatherOptions} />
        </div>
      </div>

      {/* Soil Moisture Chart */}
      <div className="glass-card p-4 rounded-xl space-y-2">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <h4 className="font-semibold text-sm text-slate-100 flex items-center gap-1.5">
            💧 Độ Ẩm Đất Tầng Mặt & Tầng Rễ (NASA SMAP / GWET)
          </h4>
          <span className="text-[10px] text-amber-400 bg-amber-950/60 border border-amber-900/60 px-1.5 py-0.5 rounded font-medium">
            Hạn đất T5–T7
          </span>
        </div>
        <div className="h-[230px] w-full">
          <Line data={soilChartData} options={soilOptions} />
        </div>
      </div>
    </div>
  );
}
