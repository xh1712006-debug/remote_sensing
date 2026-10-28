"use client";

import React from "react";
import { Sprout, Satellite, Printer, ExternalLink } from "lucide-react";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-40 bg-[#0b1120]/80 backdrop-blur-md border-b border-slate-800/80 px-4 lg:px-8 py-3.5 transition-all no-print">
      <div className="max-w-7xl mx-auto flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 ring-1 ring-white/20">
            <Sprout className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold text-lg lg:text-xl tracking-tight bg-gradient-to-r from-emerald-400 via-teal-300 to-sky-400 bg-clip-text text-transparent">
                FieldShift
              </span>
              <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                NASA Space Apps 2026
              </span>
            </div>
            <p className="text-[11px] text-slate-400 hidden sm:block">
              Hệ thống Hỗ trợ Ra Quyết định Luân canh Thích ứng Dữ liệu Viễn thám Trái đất
            </p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center gap-2.5">
          {/* NASA Badge */}
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900/90 border border-slate-800 text-xs text-slate-300 font-medium">
            <Satellite className="w-3.5 h-3.5 text-sky-400" />
            <span>NASA POWER • MERRA-2 • SMAP</span>
          </div>

          {/* Django Admin Link */}
          <a
            href="http://127.0.0.1:8000/admin/"
            target="_blank"
            rel="noreferrer"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-xs font-semibold text-slate-300 transition"
          >
            <span>Django Admin</span>
            <ExternalLink className="w-3 h-3 text-slate-400" />
          </a>

          {/* Print / Export Report Button */}
          <button
            type="button"
            onClick={() => window.print()}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow-md shadow-emerald-600/30 transition transform hover:-translate-y-0.5 active:translate-y-0"
          >
            <Printer className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">In Báo Cáo (PDF)</span>
            <span className="sm:hidden">In PDF</span>
          </button>
        </div>
      </div>
    </header>
  );
}
