import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FieldShift | Hệ Thống Thích Ứng Nông Nghiệp Dữ Liệu Vệ Tinh NASA",
  description:
    "NASA Space Apps Challenge 2026: Field Shift - Decision Support System utilizing NASA POWER, MERRA-2, and SMAP data for adaptive 3-season crop rotation and soil restoration.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" className="h-full antialiased dark">
      <body className="min-h-full flex flex-col bg-[#0b1120] text-slate-100 selection:bg-emerald-500 selection:text-white">
        {children}
      </body>
    </html>
  );
}
