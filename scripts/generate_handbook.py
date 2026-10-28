import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Đặt màu nền cho ô trong bảng"""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Đặt lề trong cho ô bảng (dựa trên twips: 20 twips = 1 pt)"""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def add_callout_box(doc, text, title="GHI CHÚ CHUYÊN GIA / THỰC TIỄN", box_type="note"):
    """Tạo hộp thông tin nổi bật (Callout Box)"""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    bg_color = "ECFDF5" if box_type == "success" else ("EFF6FF" if box_type == "info" else "FFFBEB")
    border_color = "10B981" if box_type == "success" else ("3B82F6" if box_type == "info" else "F59E0B")
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Border trái đậm
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run_title = p.add_run(f"📌 {title}\n")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(10.5)
    run_title.font.color.rgb = RGBColor(15, 23, 42)
    
    run_text = p.add_run(text)
    run_text.font.name = "Arial"
    run_text.font.size = Pt(10)
    run_text.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_remote_sensing_handbook(output_path):
    doc = Document()
    
    # Cấu hình lề trang A4 chuẩn (1 inch = 2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header & Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("CẨM NANG TOÀN TẬP VỀ CÔNG NGHỆ VIỄN THÁM & DỮ LIỆU VỆ TINH | NASA SPACE APPS 2026")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Dự án FieldShift — Hệ thống Hỗ trợ Ra Quyết định Thích ứng Nông nghiệp Viễn thám")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # TRANG BÌA & TIÊU ĐỀ CHÍNH
    # -------------------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(12)
    title_p.paragraph_format.space_after = Pt(4)
    run_main = title_p.add_run("CẨM NANG TOÀN TẬP VỀ CÔNG NGHỆ VIỄN THÁM & DỮ LIỆU VỆ TINH TRÁI ĐẤT")
    run_main.bold = True
    run_main.font.name = "Arial"
    run_main.font.size = Pt(22)
    run_main.font.color.rgb = RGBColor(11, 37, 69) # Deep Navy

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Từ Lý Thuyết Cốt Lõi, Hệ Thống Vệ Tinh (Landsat, Sentinel, NASA POWER/SMAP), Các Chỉ Số Quang Học (NDVI, NDWI, LST) Đến Hệ Sinh Thái Thư Viện Python & Ứng Dụng Thực Tế")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(16, 185, 129) # Emerald Green

    # Metadata hộp tác giả
    meta_p = doc.add_paragraph()
    meta_p.paragraph_format.space_after = Pt(18)
    run_meta = meta_p.add_run("• Tài liệu biên soạn phục vụ: Đội thi NASA Space Apps Challenge 2026 (Chủ đề: Field Shift)\n• Nền tảng công nghệ: Python 3.14 • Django • GIS • NASA Earth Observations • Leaflet\n• Trọng tâm nghiên cứu: Thích ứng Biến đổi khí hậu (Hạn hán Gió Lào Nghệ An & Xâm nhập mặn ĐBSCL)")
    run_meta.font.name = "Arial"
    run_meta.font.size = Pt(9.5)
    run_meta.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # -------------------------------------------------------------
    # HÀM TRỢ GIÚP TIÊU ĐỀ
    # -------------------------------------------------------------
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(15)
        run.font.color.rgb = RGBColor(11, 37, 69)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(12.5)
        run.font.color.rgb = RGBColor(16, 185, 129)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(11)
        run.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.bold = True
            r_bold.font.name = "Arial"
            r_bold.font.size = Pt(10)
            r_bold.font.color.rgb = RGBColor(15, 23, 42)
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            r_bold.bold = True
            r_bold.font.name = "Arial"
            r_bold.font.size = Pt(10)
            r_bold.font.color.rgb = RGBColor(15, 23, 42)
        r_text = p.add_run(text)
        r_text.font.name = "Arial"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # =============================================================
    # PHẦN 1
    # =============================================================
    add_h1("PHẦN 1: TỔNG QUAN & BẢN CHẤT VẬT LÝ CỦA VIỄN THÁM (REMOTE SENSING FUNDAMENTALS)")
    
    add_h2("1.1. Viễn Thám Là Gì? Nguyên Lý Hoạt Động Cơ Bản")
    add_body("Viễn thám (Remote Sensing) là khoa học và nghệ thuật thu thập thông tin về các đối tượng hoặc hiện tượng trên bề mặt Trái Đất từ khoảng cách xa (thông qua cảm biến gắn trên vệ tinh, máy bay hoặc máy bay không người lái UAV) mà không cần tiếp xúc vật lý trực tiếp với đối tượng đó.")
    add_body("Hệ thống viễn thám vận hành dựa trên việc đo lường năng lượng bức xạ điện từ (Electromagnetic Radiation - EMR) phát ra hoặc phản xạ từ bề mặt các vật thể. Quá trình này bao gồm 5 mắt xích cốt lõi:")
    add_bullet(" Nguồn năng lượng tự nhiên (Mặt Trời) hoặc nhân tạo (Bộ phát radar vệ tinh).", "1. Nguồn bức xạ:")
    add_bullet(" Bức xạ truyền qua khí quyển, chịu hiện tượng tán xạ (Scattering: Rayleigh, Mie, Non-selective) và hấp thụ (Absorption bởi hơi nước, CO2, Ozone).", "2. Lan truyền khí quyển:")
    add_bullet(" Năng lượng chạm vào bề mặt đối tượng (đất, cây trồng, mặt nước) và bị phản xạ, hấp thụ hoặc truyền qua tùy thuộc vào cấu trúc lý hóa.", "3. Tương tác bề mặt:")
    add_bullet(" Cảm biến (Sensor) gắn trên vệ tinh ghi nhận năng lượng phản xạ thành tín hiệu số (Digital Number - DN).", "4. Thu nhận dữ liệu:")
    add_bullet(" Dữ liệu số được hiệu chuẩn, xử lý khí quyển và phân tích thành thông tin hữu ích phục vụ nông nghiệp, khí tượng, lâm nghiệp.", "5. Xử lý & Ứng dụng:")

    add_h2("1.2. Phân Loại Viễn Thám: Thụ Động (Passive) vs Chủ Động (Active)")
    add_bullet(" Cảm biến chỉ ghi nhận năng lượng tự nhiên phản xạ từ ánh sáng Mặt Trời (ban ngày) hoặc bức xạ nhiệt do chính vật thể phát ra (ban đêm). Ví dụ: Landsat 8/9, Sentinel-2, MODIS. Nhược điểm chí mạng: BỊ MÂY VÀ BÓNG TỐI CHE KHUẤT.", "• Viễn thám Thụ động (Passive Remote Sensing):")
    add_bullet(" Vệ tinh tự mang theo nguồn phát năng lượng riêng (như chùm sóng vi sóng viễn thám hoặc xung laser LiDAR), chiếu xuống mặt đất rồi đo thời gian và cường độ chùm sóng dội ngược về. Ví dụ: Sentinel-1 (Radar SAR C-band), ALOS PALSAR. Ưu điểm vượt trội: XUYÊN MÂY, XUYÊN KHÓI MÙ VÀ HOẠT ĐỘNG CẢ NGÀY LẪN ĐÊM.", "• Viễn thám Chủ động (Active Remote Sensing):")

    add_h2("1.3. Phổ Bức Xạ Điện Từ & Các Dải Kênh Sóng Then Chốt Trong Nông Nghiệp")
    add_body("Trong viễn thám nông nghiệp, cảm biến không chụp như mắt thường (chỉ có Đỏ, Xanh lá, Xanh dương) mà phân tích sâu các dải sóng tàng hình:")
    
    # Bảng dải phổ
    tbl_em = doc.add_table(rows=6, cols=4)
    tbl_em.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_em.autofit = False
    col_widths = [Inches(1.2), Inches(1.2), Inches(2.3), Inches(1.8)]
    for row in tbl_em.rows:
        for i, w in enumerate(col_widths):
            row.cells[i].width = w

    headers_em = ["Kênh sóng (Band)", "Bước sóng (λ)", "Đặc trưng phản xạ sinh thái", "Ứng dụng chuyên môn"]
    for i, title in enumerate(headers_em):
        cell = tbl_em.cell(0, i)
        set_cell_background(cell, "0B2545")
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    data_em = [
        ["Visible (Blue, Green, Red)", "0.40 – 0.70 µm", "Diệp lục (Chlorophyll) trong lá hấp thụ mạnh ánh sáng Xanh dương và Đỏ để quang hợp, phản xạ màu Xanh lục.", "Nhận diện ranh giới cây trồng, quan sát màu lá, mắt thường."],
        ["Red Edge (Vùng biên đỏ)", "0.70 – 0.75 µm", "Vùng chuyển tiếp dốc đứng giữa khả năng hấp thụ của chất diệp lục và phản xạ của cấu trúc tế bào lá.", "Đo lường nhạy cảm hàm lượng đạm (N) và phát hiện sớm sâu bệnh."],
        ["NIR (Cận hồng ngoại)", "0.75 – 1.30 µm", "Cấu trúc xốp của màng tế bào diệp nhục (mesophyll cells) phản xạ cực mạnh (>50% năng lượng).", "Đo sức sống cây trồng (NDVI), phân biệt cây khỏe vs cây suy kiệt."],
        ["SWIR (Hồng ngoại ngắn)", "1.30 – 2.50 µm", "Bị hấp thụ cực mạnh bởi các phân tử nước tự do trong lá cây và trong lỗ rỗng của đất.", "Đo độ ẩm lá (NDWI), phân biệt hạn đất nứt nẻ và cháy rừng."],
        ["TIR (Hồng ngoại nhiệt)", "10.0 – 12.5 µm", "Đo năng lượng bức xạ nhiệt nội tại phát ra từ bề mặt vật chất Trái Đất (theo định luật Stefan-Boltzmann).", "Nhiệt độ bề mặt đất LST, sốc nhiệt gió Lào, nhu cầu tưới tiêu."]
    ]

    for row_idx, row_data in enumerate(data_em, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = tbl_em.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            if col_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(11, 37, 69)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_h2("1.4. Bốn Độ Phân Giải Quyết Định Chất Lượng Viễn Thám")
    add_bullet(" Kích thước thực tế trên mặt đất tương ứng với 1 điểm ảnh (pixel). Ví dụ: Sentinel-2 có độ phân giải 10m (1 pixel đại diện cho 100 m² trên ruộng); MODIS là 250m; vệ tinh thương mại WorldView là 0.3m (30cm, thấy rõ từng luống cày).", "1. Độ phân giải Không gian (Spatial Resolution):")
    add_bullet(" Số lượng và độ hẹp của các dải sóng mà cảm biến ghi lại. Càng nhiều dải sóng hẹp (Hyperspectral - Siêu phổ với hàng trăm kênh), khả năng nhận diện phân biệt chính xác từng giống lúa hay loại phân bón càng cao.", "2. Độ phân giải Phổ (Spectral Resolution):")
    add_bullet(" Chu kỳ thời gian để vệ tinh quay trở lại chụp đúng một tọa độ mặt đất. Ví dụ: Landsat cần 16 ngày; Sentinel-2 (với cặp vệ tinh 2A & 2B) chỉ mất 5 ngày; MODIS quay lại hàng ngày (1 ngày/lần). Trong theo dõi hạn hán và sâu bệnh, độ phân giải thời gian cao là yếu tố sống còn.", "3. Độ phân giải Thời gian (Temporal Resolution):")
    add_bullet(" Độ nhạy của bộ cảm biến số khi ghi nhận các biến đổi nhỏ của cường độ bức xạ, biểu thị bằng số bit. 8-bit (256 mức giá trị xám), 12-bit (4.096 mức), 16-bit (65.536 mức như Landsat 9). Càng nhiều bit, ảnh chụp càng ít bị cháy sáng và thấy rõ chi tiết trong vùng tối bóng mây.", "4. Độ phân giải Bức xạ (Radiometric Resolution):")

    add_callout_box(
        doc,
        "Định luật quan trọng trong viễn thám nông nghiệp: Khi lá cây khỏe mạnh, chất diệp lục hấp thụ 85% ánh sáng Đỏ để quang hợp và tế bào xốp phản xạ 60% ánh sáng Cận hồng ngoại (NIR). Nhưng khi cây bị hạn hán hoặc sâu bệnh phá hoại, cấu trúc tế bào xẹp xuống khiến phản xạ NIR tụt dốc, đồng thời diệp lục thoái hóa làm phản xạ ánh sáng Đỏ tăng vọt. Sự đối nghịch này là nền tảng cho mọi chỉ số thực vật!",
        title="BẢN CHẤT QUANG HỌC CỦA ĐỒNG RUỘNG",
        box_type="success"
    )

    # =============================================================
    # PHẦN 2
    # =============================================================
    add_h1("PHẦN 2: CÁC HỆ THỐNG VỆ TINH TRÁI ĐẤT QUAN TRỌNG NHẤT THẾ GIỚI")
    add_body("Hiện nay trên quỹ đạo có hàng trăm vệ tinh quan sát Trái Đất, nhưng đối với nông nghiệp và biến đổi khí hậu tại Việt Nam, các kỹ sư GIS cần nắm vững 6 chùm vệ tinh sau:")

    add_h2("2.1. NASA / USGS Landsat (Landsat 8 & 9)")
    add_bullet(" 1972 đến nay (hơn 50 năm dữ liệu liên tục — chuỗi dữ liệu dài nhất lịch sử nhân loại).", "• Lịch sử sứ mệnh:")
    add_bullet(" Cảm biến quang học OLI (Operational Land Imager) với 9 kênh phổ (độ phân giải 30m, kênh toàn sắc 15m) và Cảm biến nhiệt TIRS (Thermal Infrared Sensor) 2 kênh hồng ngoại nhiệt (100m).", "• Cảm biến chính:")
    add_bullet(" Đánh giá biến động sử dụng đất qua nhiều thập kỷ, phân tích nhiệt độ mặt đất LST cấp tiểu vùng, đối chiếu hiện trạng thoái hóa đất nông nghiệp.", "• Ứng dụng:")

    add_h2("2.2. ESA Copernicus Sentinel (Sentinel-1 & Sentinel-2)")
    add_bullet(" 10m (RGB, NIR), 20m (Red Edge, SWIR). Chu kỳ 5 ngày tại xích đạo.", "• Sentinel-2 (Quang học):")
    add_body("Được mệnh danh là 'cỗ máy cứu tinh' cho nông nghiệp chính xác hiện đại. Với 3 kênh Red Edge cực nhạy, Sentinel-2 cho phép định lượng hàm lượng đạm trong cây trồng và ước tính năng suất lúa chính xác đến từng thửa ruộng.")
    add_bullet(" Cảm biến Radar C-band (Synthetic Aperture Radar - SAR).", "• Sentinel-1 (Radar xuyên mây):")
    add_body("Vũ khí chiến lược tại vùng khí hậu nhiệt đới gió mùa nhiều mây như Việt Nam. Sóng radar của Sentinel-1 đâm xuyên qua mây mù dày đặc mùa mưa bão, giúp lập bản đồ ngập lụt tức thời tại Miền Trung và theo dõi diện tích gieo cấy lúa nước tại Đồng bằng Sông Cửu Long.")

    add_h2("2.3. NASA Terra & Aqua MODIS")
    add_bullet(" 36 kênh phổ, độ phân giải 250m (Red, NIR), 500m và 1.000m.", "• Đặc tính kỹ thuật:")
    add_bullet(" Điểm mạnh nhất của MODIS là độ phân giải thời gian: bay qua Việt Nam 2 lần mỗi ngày (Terra buổi sáng, Aqua buổi chiều).", "• Ưu thế:")
    add_bullet(" Theo dõi chu kỳ sinh thái toàn cầu, phát hiện điểm cháy rừng/đốt rơm rạ thời gian thực, lập bản đồ hạn hán cấp quốc gia.", "• Ứng dụng:")

    add_h2("2.4. NASA GPM (Global Precipitation Measurement)")
    add_bullet(" Chùm vệ tinh đa quốc gia do NASA và JAXA (Nhật Bản) chủ trì, mang cảm biến Radar Mưa lưỡng tần (DPR) và Cảm biến vi sóng thụ động (GMI).", "• Nguyên lý:")
    add_bullet(" Cung cấp sản phẩm **NASA IMERG** — đo lượng mưa tích lũy toàn cầu sau mỗi 30 phút ở độ phân giải 0.1° (~10km).", "• Sản phẩm cốt lõi:")
    add_bullet(" Là nguồn dữ liệu cho hệ thống FieldShift nhận diện đỉnh mưa bão tháng 9–10 tại Nghệ An (>14 mm/ngày) để cảnh báo nông dân né vụ gieo trồng.", "• Ứng dụng trong FieldShift:")

    add_h2("2.5. NASA SMAP (Soil Moisture Active Passive)")
    add_bullet(" Sử dụng cảm biến vi sóng băng L (L-band: 1.41 GHz) đo lượng nước nằm trong lỗ rỗng của đất ở độ sâu 0 – 5 cm (tầng mặt) và suy diễn độ ẩm vùng rễ (0 – 100 cm).", "• Cơ chế:")
    add_bullet(" Băng L có khả năng đâm xuyên qua tán lá cây trồng để 'cảm nhận' độ ẩm thực tế của lớp đất bên dưới, không phụ thuộc vào mây mù hay bóng tối.", "• Khả năng vượt trội:")
    add_bullet(" Cung cấp chỉ số `GWETROOT` trong FieldShift để phát hiện đất khô nẻ kiệt nước (<0.35) do gió Lào Foehn, kích hoạt khuyến nghị chuyển sang cây họ đậu (Lạc L14).", "• Đóng góp cho nông nghiệp:")

    add_h2("2.6. NASA POWER & MERRA-2 (Agroclimatology API)")
    add_bullet(" Dự án chuyên biệt của NASA Langley Research Center kết hợp mô hình tái phân tích khí quyển MERRA-2 với các vệ tinh địa tĩnh và cực.", "• Đặc điểm:")
    add_bullet(" Hoàn toàn miễn phí, truy vấn REST API trực tiếp theo kinh độ/vĩ độ, không cần tài khoản hay API Key phức tạp.", "• Điểm tuyệt vời:")
    add_bullet(" Trả về hơn 20 thông số khí tượng nông học lịch sử từ năm 1981 đến nay: Nhiệt độ đỉnh `T2M_MAX`, bức xạ mặt trời `ALLSKY_SFC_SW_DWN`, lượng mưa `PRECTOTCORR`, độ ẩm đất `GWETTOP`/`GWETROOT`.", "• Thông số cung cấp:")

    # =============================================================
    # PHẦN 3
    # =============================================================
    add_h1("PHẦN 3: CÁC CHỈ SỐ QUANG HỌC & VIỄN THÁM NÔNG NGHIỆP CỐT LÕI (SPECTRAL INDICES)")
    add_body("Chỉ số viễn thám là các công thức toán học kết hợp năng lượng từ 2 hoặc nhiều kênh phổ để làm nổi bật đặc tính vật lý/sinh học của đối tượng và loại trừ các yếu tố nhiễu môi trường.")

    # Bảng chỉ số
    tbl_idx = doc.add_table(rows=7, cols=4)
    tbl_idx.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_idx.autofit = False
    col_w_idx = [Inches(1.1), Inches(2.2), Inches(1.8), Inches(1.4)]
    for row in tbl_idx.rows:
        for i, w in enumerate(col_w_idx):
            row.cells[i].width = w

    headers_idx = ["Chỉ số", "Công thức toán học", "Ngưỡng giá trị tiêu chuẩn", "Ý nghĩa nông học"]
    for i, title in enumerate(headers_idx):
        cell = tbl_idx.cell(0, i)
        set_cell_background(cell, "0B2545")
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    data_idx = [
        ["NDVI (Normalized Difference Vegetation Index)", "NDVI = (NIR - RED) / (NIR + RED)", "< 0.2: Đất trống, cát nẻ\n0.2 - 0.4: Cây mới gieo\n0.6 - 0.9: Rừng rậm, lúa trổ bông", "Đo mật độ sinh khối xanh và sức sống quang hợp."],
        ["EVI (Enhanced Vegetation Index)", "EVI = 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)", "0.2 - 0.8: Thảm thực vật xanh tốt", "Khử nhiễu khí quyển bằng kênh Blue, không bị bão hòa ở tán rừng rậm."],
        ["SAVI (Soil Adjusted Vegetation Index)", "SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)\n(Thường L = 0.5)", "Hiệu chỉnh cho vùng có độ che phủ cây trồng thấp (<40%)", "Khử ảnh hưởng của độ sáng nền đất khi cây còn nhỏ hoặc đất khô."],
        ["NDRE (Normalized Difference Red Edge)", "NDRE = (NIR - RedEdge) / (NIR + RedEdge)", "0.3 - 0.7: Sinh trưởng lý tưởng", "Đo hàm lượng Đạm (Nitơ) trong lá, tối ưu bón phân đạm theo nhu cầu."],
        ["NDWI (Normalized Difference Water Index)", "NDWI = (GREEN - NIR) / (GREEN + NIR) (Mặt nước)\nNDWI = (NIR - SWIR) / (NIR + SWIR) (Ẩm lá)", "> 0: Mặt nước ngập, ao hồ\n< 0: Đất khô ráo", "Phát hiện lũ lụt, ranh mặn và hàm lượng nước trong mô tế bào thực vật."],
        ["LST (Land Surface Temperature)", "LST = γ * (1/ε * (ψ1*L_sensor + ψ2) + ψ3) + δ (Từ TIR)", "Đo bằng độ Kelvin (K) hoặc độ C (°C)", "Nhiệt độ mặt đất thực tế; phát hiện các điểm nóng sốc nhiệt gió Lào."]
    ]

    for row_idx, row_data in enumerate(data_idx, start=1):
        bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = tbl_idx.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.name = "Arial"
            run.font.size = Pt(8.5)
            if col_idx == 0:
                run.bold = True
                run.font.color.rgb = RGBColor(11, 37, 69)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # =============================================================
    # PHẦN 4
    # =============================================================
    add_h1("PHẦN 4: HỆ SINH THÁI THƯ VIỆN & CÔNG CỤ VIỄN THÁM (PYTHON & GIS ECOSYSTEM)")
    add_body("Để xây dựng các ứng dụng viễn thám như FieldShift, kỹ sư cần làm chủ các thư viện Python chuyên ngành hàng đầu thế giới được chia thành 4 nhóm:")

    add_h2("4.1. Nhóm Xử Lý Dữ Liệu Raster (Ảnh Vệ Tinh Đa Chiều)")
    add_bullet(" Thư viện nền tảng số 1 để đọc/ghi ảnh định dạng GeoTIFF dựa trên thư viện C++ GDAL danh tiếng. Hỗ trợ đọc từng cửa sổ ảnh (Windowed reading) giúp mở file ảnh vệ tinh nặng 5GB mà chỉ tốn vài megabyte RAM.", "1. rasterio (GDAL Pythonic wrapper):")
    add_bullet(" Kết hợp sức mạnh của xarray (mảng đa chiều có nhãn) và rasterio. Thích hợp nhất cho chuỗi thời gian vệ tinh (Time-series) như phân tích 12 tháng nhiệt độ hoặc lượng mưa tại cùng 1 tọa độ.", "2. rioxarray & xarray:")
    add_bullet(" Thực hiện phép tính Đại Số Bản Đồ (Map Algebra) trên từng mảng pixel ma trận. Mọi công thức tính NDVI, NDWI đều là phép toán ma trận NumPy tốc độ cao chạy trên C-backend.", "3. numpy & scipy:")
    add_bullet(" Nhận diện bờ bao ruộng lúa, làm sạch mây mù, lọc bóng râm và phân đoạn thửa đất (Image Segmentation).", "4. scikit-image / OpenCV:")

    add_h2("4.2. Nhóm Xử Lý Dữ Liệu Vector & Không Gian (GIS Geometry)")
    add_bullet(" Mở rộng từ Pandas DataFrame, cho phép lưu trữ cột hình học (`geometry`: Polygon, LineString, Point) và thực hiện các phép truy vấn không gian như: 'Thửa ruộng này có nằm trong vùng ngập mặn 4‰ không?'.", "1. geopandas:")
    add_bullet(" Xử lý các phép toán hình học thuần túy: Giao nhau (Intersection), Hợp nhất (Union), Vùng đệm (Buffer ranh mặn 30km).", "2. shapely:")
    add_bullet(" Chuyển đổi hệ tọa độ trắc địa. Cực kỳ quan trọng ở Việt Nam khi cần chuyển đổi giữa Hệ tọa độ quốc tế WGS-84 (EPSG:4326 - vệ tinh GPS) sang Hệ tọa độ quốc gia VN-2000 (EPSG:3405 / EPSG:3406 dùng trong đo đạc ruộng đất chính quy).", "3. pyproj:")

    add_h2("4.3. Nhóm Điện Toán Đám Mây & Big Data Viễn Thám")
    add_bullet(" Thư viện Python kết nối siêu máy tính của Google. Cho phép lọc hàng ngàn cảnh ảnh Sentinel-2 trên toàn lãnh thổ Việt Nam, lọc mây và tính toán NDVI trung bình trong vài giây mà không cần tải bất kỳ gigabyte ảnh nào về máy tính cá nhân.", "1. earthengine-api (Google Earth Engine):")
    add_bullet(" Chuẩn tìm kiếm danh mục dữ liệu không gian thời gian mở của NASA, Microsoft, ESA. Giúp tìm nhanh ảnh vệ tinh theo ngày chụp và tỷ lệ mây che phủ.", "2. pystac & pystac-client:")
    add_bullet(" Thư viện trực quan hóa dữ liệu vệ tinh không gian trong Jupyter Notebook do Giáo sư Qiusheng Wu phát triển, hỗ trợ so sánh ảnh trước/sau thiên tai (Split-map slider).", "3. leafmap & geemap:")

    add_h2("4.4. Nhóm Trực Quan Hóa Bản Đồ Web (Web Mapping GIS)")
    add_bullet(" Thư viện JavaScript bản đồ web phổ biến nhất thế giới. Nhẹ (chỉ ~40KB), hỗ trợ tải tile vệ tinh đa nguồn (Esri, Google, OSM), vẽ GeoJSON và xử lý tương tác người dùng mượt mà (chính là công nghệ cốt lõi trong giao diện FieldShift của chúng ta).", "1. Leaflet.js:")
    add_bullet(" Sử dụng WebGL render bản đồ vector mượt mà 60 FPS trên chip đồ họa GPU, hỗ trợ mô phỏng địa hình 3D.", "2. MapLibre GL JS:")
    add_bullet(" Thư viện GIS hoàn chỉnh dành cho các hệ thống thông tin địa lý cấp chuyên gia, hỗ trợ mọi hệ quy chiếu và chuẩn OGC khắt khe.", "3. OpenLayers:")

    # =============================================================
    # PHẦN 5
    # =============================================================
    add_h1("PHẦN 5: CÁC ĐỊNH DẠNG DỮ LIỆU & GIAO THỨC CHUẨN TRONG VIỄN THÁM")
    
    add_h2("5.1. Định Dạng File Viễn Thám")
    add_bullet(" File ảnh TIFF thông thường được nhúng siêu dữ liệu không gian (tọa độ 4 góc, hệ quy chiếu CRS, kích thước pixel).", "• GeoTIFF:")
    add_bullet(" Đỉnh cao công nghệ viễn thám hiện đại. COG sắp xếp các điểm ảnh bên trong file theo từng ô nhỏ (tiling) kèm các cấp độ thu nhỏ (overviews). Nhờ đó, trình duyệt web có thể dùng HTTP Range Requests để chỉ tải đúng vài kilobyte hình ảnh ở mức zoom hiện tại mà không phải tải cả file ảnh 2GB từ máy chủ!", "• Cloud Optimized GeoTIFF (COG):")
    add_bullet(" Định dạng file khoa học chuyên dụng cho dữ liệu mảng n-chiều (thời gian, độ cao, vĩ độ, kinh độ). Chuẩn mực của dữ liệu khí hậu toàn cầu như NASA MERRA-2 hay ECMWF ERA5.", "• NetCDF (.nc) & HDF5 (.h5):")
    add_bullet(" Định dạng mở dạng văn bản JSON biểu diễn các đối tượng hình học thửa ruộng, ranh giới hành chính kèm bảng thuộc tính (tên nông hộ, loại đất, diện tích).", "• GeoJSON:")

    add_h2("5.2. Các Giao Thức Web Map Dịch Vụ Mở (OGC Standards)")
    add_bullet(" Máy chủ render ảnh bản đồ sẵn và trả về dạng ảnh tĩnh PNG/JPEG theo tọa độ Bounding Box.", "• WMS (Web Map Service):")
    add_bullet(" Bản đồ được cắt sẵn thành các mảnh vuông 256x256 pixel ở các mức zoom khác nhau. Siêu nhanh và được trình duyệt cache tối ưu (như các lớp Esri Clarity, Google Hybrid trong FieldShift).", "• WMTS / XYZ Tiles:")
    add_bullet(" Máy chủ trả về chính xác tọa độ vector hình học để máy khách tự do chỉnh màu, filter thuộc tính và tính toán diện tích.", "• WFS (Web Feature Service):")

    # =============================================================
    # PHẦN 6
    # =============================================================
    add_h1("PHẦN 6: ỨNG DỤNG VIỄN THÁM THỰC TIỄN TRONG DỰ ÁN FIELDSHIFT")
    add_body("Trong khuôn khổ đề tài NASA Space Apps Challenge 'Field Shift: Adapting Farms with NASA Data', viễn thám không phải là lý thuyết suông mà được áp dụng cụ thể vào nông nghiệp Việt Nam:")

    add_h2("6.1. Hóa Giải Sốc Nhiệt Gió Lào Foehn Tại Nghệ An")
    add_body("Vào các tháng 5, 6, 7 tại Bắc Trung Bộ, gió Tây Nam vượt dãy Trường Sơn tạo hiệu ứng phơn (Foehn) khiến nhiệt độ không khí vượt 40°C và độ ẩm không khí tụt xuống dưới 30%.")
    add_bullet(" Vệ tinh MERRA-2 và cảm biến nhiệt hồng ngoại TIR đo được nhiệt độ đỉnh `T2M_MAX` đạt 41.23°C vào tháng 5.", "• Dữ liệu NASA phát hiện:")
    add_bullet(" Cảm biến vi sóng SMAP ghi nhận độ ẩm đất tầng rễ `GWETROOT` tụt xuống mức báo động đỏ 0.28.", "• Thổ nhưỡng phản ứng:")
    add_bullet(" Hệ thống FieldShift khuyến nghị bà con KHÔNG cấy lúa hè thu (tránh nguy cơ mất trắng lúa trổ bông gặp gió lào bị nghẹn hạt), thay bằng cây họ đậu (Lạc L14, Sen Thọ). Cây lạc chịu được nhiệt độ >40°C, tiêu thụ nước chỉ bằng 30% lúa và nốt sần rễ tự cố định +52 kg đạm N/ha tự nhiên.", "• Giải pháp chuyển đổi:")

    add_h2("6.2. Ứng Phó Đỉnh Mưa Lũ Vụ Thu Đông Tháng 9 – 10")
    add_bullet(" Dữ liệu NASA GPM IMERG ghi nhận lượng mưa đạt đỉnh 13.71 mm/ngày vào tháng 9-10 tại Nghệ An (nguy cơ úng ngập và lũ lụt rất cao).", "• Đo lường NASA:")
    add_bullet(" Khuyến cáo nông dân né hoàn toàn việc xuống giống trước ngày 15/10. Chỉ gieo trồng khoai lang Hoàng Long hoặc ngô nếp sau ngày 15/10 khi nước lũ rút, tận dụng lớp phù sa màu mỡ và tạo thảm thực vật chống xói mòn đất tầng mặt.", "• Quyết định vụ mùa:")

    add_h2("6.3. Giám Sát Xâm Nhập Mặn Vùng Đồng Bằng Sông Cửu Long (Bến Tre)")
    add_bullet(" Bản đồ chuyên đề phân định ranh mặn 4‰ (cách cửa biển 35-45km trên sông Hàm Luông, Cổ Chiên). Nồng độ muối >4g/l khiến hạt lúa thối mầm, rễ cháy khô.", "• Ranh mặn báo động:")
    add_bullet(" Cảnh báo thời gian thực giúp nông dân đóng cống ngăn mặn kịp thời, chuyển đổi sang mô hình kinh tế sinh thái thích ứng mặn (Tôm - Lúa hoặc lúa chịu mặn ST24/ST25).", "• Giá trị hỗ trợ:")

    # =============================================================
    # PHẦN 7
    # =============================================================
    add_h1("PHẦN 7: LỘ TRÌNH TỰ HỌC & CÁC NGUỒN TÀI NGUYÊN HỌC TẬP TỐT NHẤT")
    
    add_h2("7.1. Các Cổng Tải Dữ Liệu Vệ Tinh Mở Miễn Phí")
    add_bullet(" https://power.larc.nasa.gov — Cổng truy vấn thời tiết nông nghiệp NASA (miễn phí, không cần tài khoản, dùng trong FieldShift).", "1. NASA POWER API:")
    add_bullet(" https://dataspace.copernicus.eu — Cổng tải toàn bộ ảnh Sentinel-1, Sentinel-2, Sentinel-3 mới nhất của Châu Âu.", "2. Copernicus Data Space Ecosystem:")
    add_bullet(" https://earthexplorer.usgs.gov — Kho tải ảnh vệ tinh Landsat 1 đến 9, mô hình số hóa độ cao địa hình SRTM DEM.", "3. USGS EarthExplorer:")
    add_bullet(" https://search.earthdata.nasa.gov — Cổng tìm kiếm tổng hợp hàng trăm petabyte dữ liệu khoa học Trái Đất của NASA.", "4. NASA Earthdata Search:")

    add_h2("7.2. Checklist 10 Kỹ Năng Cốt Lõi Để Trở Thành Kỹ Sư Viễn Thám Giỏi")
    add_bullet(" Hiểu bản chất các dải bước sóng (RGB, NIR, Red Edge, SWIR, TIR, SAR).", "1. Vật lý bức xạ:")
    add_bullet(" Làm chủ Python căn bản và xử lý mảng số NumPy.", "2. Lập trình Python:")
    add_bullet(" Đọc ghi và biến đổi ảnh GeoTIFF với thư viện `rasterio`.", "3. Thao tác Raster:")
    add_bullet(" Thao tác polygon thửa ruộng, ranh giới hành chính với `geopandas` và `shapely`.", "4. Thao tác Vector:")
    add_bullet(" Hiểu các hệ tọa độ trắc địa (WGS-84 EPSG:4326 vs VN-2000).", "5. Hệ quy chiếu tọa độ (CRS):")
    add_bullet(" Viết script tính toán các chỉ số nông nghiệp (NDVI, NDWI, EVI, LST).", "6. Đại số bản đồ:")
    add_bullet(" Xử lý dữ liệu viễn thám chuỗi thời gian lớn với Google Earth Engine.", "7. Cloud GIS (GEE):")
    add_bullet(" Tích hợp bản đồ vệ tinh lên ứng dụng web bằng Leaflet.js hoặc MapLibre.", "8. Web GIS Development:")
    add_bullet(" Hiểu mối liên hệ giữa các chỉ số vệ tinh với sinh lý cây trồng, khí hậu và đất đai.", "9. Nghiệp vụ nông học:")
    add_bullet(" Trực quan hóa dữ liệu bản đồ thành biểu đồ, dashboard giúp người dùng dễ dàng ra quyết định.", "10. Kỹ năng trình bày dữ liệu:")

    # Lưu tài liệu
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Document saved successfully at: {output_path}")

if __name__ == "__main__":
    out_file = r"d:\project\project-local\vientham\docs\CAM_NANG_VIEN_THAM_TOAN_TAP.docx"
    build_remote_sensing_handbook(out_file)
