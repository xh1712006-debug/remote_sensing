import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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

def add_alert_box(doc, text, title="CẢNH BÁO GIỚI HẠN KỸ THUẬT", box_type="danger"):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)
    
    cell = table.cell(0, 0)
    bg_color = "FEF2F2" if box_type == "danger" else ("FFFBEB" if box_type == "warning" else "EFF6FF")
    border_color = "EF4444" if box_type == "danger" else ("F59E0B" if box_type == "warning" else "3B82F6")
    
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
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
    run_title = p.add_run(f"⚠️ {title}\n")
    run_title.bold = True
    run_title.font.name = "Arial"
    run_title.font.size = Pt(10)
    run_title.font.color.rgb = RGBColor(185, 28, 28) if box_type == "danger" else RGBColor(180, 83, 9)
    
    run_text = p.add_run(text)
    run_text.font.name = "Arial"
    run_text.font.size = Pt(9.5)
    run_text.font.color.rgb = RGBColor(51, 65, 85)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_unresolved_issues_document(output_path):
    doc = Document()
    
    # Lề A4 chuẩn 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
        # Header / Footer
        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("BÁO CÁO KỸ THUẬT: CÁC VẤN ĐỀ CHƯA GIẢI QUYẾT & GIỚI HẠN HỆ THỐNG | FIELDSHIFT 2026")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Dự án FieldShift — Phân tích phản biện khoa học & Lộ trình hoàn thiện")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------
    # TIÊU ĐỀ BÁO CÁO
    # -------------------------------------------------------------
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(4)
    run_main = p_title.add_run("BÁO CÁO PHÂN TÍCH CHUYÊN SÂU:\nCÁC VẤN ĐỀ CHƯA GIẢI QUYẾT, GIỚI HẠN KỸ THUẬT VÀ NGUYÊN NHÂN CỐT LÕI")
    run_main.bold = True
    run_main.font.name = "Arial"
    run_main.font.size = Pt(18)
    run_main.font.color.rgb = RGBColor(153, 27, 27) # Dark Crimson Red

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Đánh Giá Trung Thực Độ Trưởng Thành Hệ Thống, Giới Hạn Vật Lý Cảm Biến Vệ Tinh, Rào Cản Dữ Liệu Nông Học & Phương Hướng Giải Quyết Trong Tương Lai")
    run_sub.font.name = "Arial"
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(71, 85, 105)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(16)
    r_meta = p_meta.add_run(
        "• Dự án nghiên cứu: FieldShift — Adapting Farms with NASA Data (NASA Space Apps 2026)\n"
        "• Mục đích tài liệu: Tự đánh giá (Self-Audit), chỉ rõ 'điểm nghẽn' kỹ thuật để trả lời tự tin trước Ban giám khảo & Hội đồng phản biện khoa học\n"
        "• Phạm vi xem xét: Dữ liệu viễn thám NASA, Thổ nhưỡng, Thủy lực, Thuật toán luân canh và Khả năng áp dụng tại nông hộ Việt Nam"
    )
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(14)
        r.font.color.rgb = RGBColor(153, 27, 27)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(12)
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_body(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = RGBColor(15, 23, 42)
        rt = p.add_run(text)
        rt.font.name = "Arial"
        rt.font.size = Pt(9.5)
        rt.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_bullet(text, bold_prefix=None):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = "Arial"
            rb.font.size = Pt(9.5)
            rb.font.color.rgb = RGBColor(15, 23, 42)
        rt = p.add_run(text)
        rt.font.name = "Arial"
        rt.font.size = Pt(9.5)
        rt.font.color.rgb = RGBColor(51, 65, 85)
        return p

    # =============================================================
    # MỞ ĐẦU
    # =============================================================
    add_h1("LỜI MỞ ĐẦU: TẠI SAO PHẢI THẲNG THẮN NÓI RA CÁC ĐIỂM CHƯA GIẢI QUYẾT ĐƯỢC?")
    add_body(
        "Trong mọi cuộc thi công nghệ quốc tế (đặc biệt là NASA Space Apps Challenge), ban giám khảo là các nhà khoa học, chuyên gia GIS và khí tượng học kỳ cựu. "
        "Họ KHÔNG tìm kiếm một sản phẩm thần thánh hoàn hảo giả tạo, mà họ đánh giá cao nhất các đội thi HIỂU RÕ GIỚI HẠN VẬT LÝ của công nghệ mình đang dùng, "
        "biết chính xác hệ thống của mình đang thiếu sót gì, tại sao chưa giải quyết được và có kế hoạch khoa học nghiêm túc để khắc phục."
    )
    add_body(
        "Dưới đây là bản mổ xẻ 6 vấn đề hóc búa nhất mà dự án FieldShift hiện tại chưa giải quyết trọn vẹn, cùng phân tích nguyên nhân gốc rễ (Root Causes) và rào cản kỹ thuật thực tế."
    )

    # =============================================================
    # VẤN ĐỀ 1
    # =============================================================
    add_h1("VẤN ĐỀ 1: KHOẢNG CÁCH ĐỘ PHÂN GIẢI KHÔNG GIAN (SPATIAL RESOLUTION GAP)")
    
    add_h2("1.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_body(
        "Dữ liệu khí tượng và thổ nhưỡng của NASA cung cấp trên nền tảng FieldShift hiện tại có độ phân giải không gian rất thô:",
        "• Độ phân giải nguồn dữ liệu: "
    )
    add_bullet(" Mô hình tái phân tích khí hậu MERRA-2 (nguồn của NASA POWER) có độ phân giải 0.5° × 0.5° vĩ độ/kinh độ (tương đương khoảng 50 km × 50 km).", "NASA POWER / MERRA-2:")
    add_bullet(" Cảm biến vi sóng băng L đo độ ẩm đất có độ phân giải không gian từ 9 km đến 36 km.", "NASA SMAP (Độ ẩm đất):")
    add_bullet(" Lượng mưa tích lũy IMERG có độ phân giải 0.1° × 0.1° (khoảng 11 km × 11 km).", "NASA GPM (Lượng mưa):")
    add_body(
        "Trong khi đó, đặc thù canh tác nông nghiệp tại Việt Nam (nhất là vùng đồng bằng sông Lam tại Nghệ An hay đồng bằng sông Hồng) là cực kỳ manh mún. "
        "Một thửa ruộng của hộ nông dân thường chỉ rộng từ 1 sào đến 3 sào (500 m² – 1.500 m²), hiếm khi tới vài hecta. "
        "Như vậy, MỘT ĐIỂM ẢNH (PIXEL) của vệ tinh NASA có diện tích bao trùm cả một huyện, thậm chí nửa tỉnh Nghệ An! "
        "Hệ quả là: Nếu nông dân ở xã Nam Anh và nông dân ở xã Nam Thanh (cách nhau 5 km) cùng nhấp vào bản đồ, dữ liệu nhiệt độ và độ ẩm đất NASA trả về là HOÀN TOÀN GIỐNG NHAU, "
        "không phản ánh được sự khác biệt giữa ruộng trũng chân núi và ruộng cồn cát ven sông!",
        "• Hệ quả nông hộ: "
    )

    add_h2("1.2. Tại Sao Lại Chưa Giải Quyết Được? (Nguyên Nhân Cốt Lõi)")
    add_bullet(" Các vệ tinh đo độ ẩm đất (SMAP) và vi sóng mưa (GPM) hoạt động ở dải bước sóng dài (băng L: ~21 cm). Theo định luật nhiễu xạ quang học (Diffraction limit: θ ≈ 1.22 λ / D), để có được ảnh độ phân giải 10m từ quỹ đạo 700km, đường kính ăng-ten vệ tinh phải lớn hàng kilomet — điều hoàn toàn bất khả thi đối với công nghệ phóng vệ tinh hiện nay.", "1. Rào cản vật lý cảm biến vi sóng:")
    add_bullet(" Để biến dữ liệu 50km thành dữ liệu 10m cần kỹ thuật 'Spatial Downscaling' (Hạ tỉ lệ không gian bằng AI). Quy trình này đòi hỏi kết hợp mô hình số độ cao địa hình (DEM 30m), lớp phủ chỉ số thực vật Sentinel-2 (10m), nhiệt độ mặt đất Landsat (100m) và chạy mô hình học sâu (CNN Super-Resolution). Một ứng dụng web Django thông thường không có máy chủ GPU chuyên dụng để chạy suy luận thời gian thực cho hàng ngàn người dùng.", "2. Độ phức tạp tính toán của thuật toán Downscaling:")
    add_bullet(" Chưa có API vệ tinh vi sóng thương mại nào trên thế giới cung cấp độ ẩm đất miễn phí dưới 1km.", "3. Thiếu dữ liệu thay thế thương mại:")

    add_alert_box(
        doc,
        "Hiện tại hệ thống đang giải quyết tình thế bằng kỹ thuật 'Snapping Grid 0.1°': Tọa độ người dùng nhấp được làm tròn về mắt lưới 0.1° gần nhất (~11 km) để truy vấn và cache kết quả. Đây là cách làm thực dụng để demo và tối ưu tốc độ, nhưng KHÔNG THỂ thay thế đo đạc độ ẩm chính xác ở quy mô từng luống đất!",
        title="GIỚI HẠN VỀ ĐỘ PHÂN GIẢI THỰC TẾ",
        box_type="warning"
    )

    # =============================================================
    # VẤN ĐỀ 2
    # =============================================================
    add_h1("VẤN ĐỀ 2: BÀI TOÁN 'MÙ VỆ TINH' DO MÂY NHIỆT ĐỚI CHE PHỦ (CLOUD COVER OCCLUSION)")

    add_h2("2.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_body(
        "Việt Nam nằm trọn trong vùng nhiệt đới gió mùa ven biển. Vào các giai đoạn khí hậu quan trọng nhất trong năm đối với nông dân:",
        "• Thực trạng mây mù: "
    )
    add_bullet(" Mùa mưa lũ Bắc Trung Bộ (Tháng 9 – Tháng 11): Mây mù dày đặc, dông bão liên tục 3–4 tuần liền.", "Tháng 9-11 (Mùa lũ Miền Trung):")
    add_bullet(" Mùa gió mùa Tây Nam ở Nam Bộ (Tháng 6 – Tháng 9): Mây tầng đối lưu che phủ bầu trời hàng ngày.", "Tháng 6-9 (Mùa mưa ĐBSCL):")
    add_body(
        "Vào những giai đoạn này, các vệ tinh viễn thám quang học độ nét cao như Sentinel-2 (10m) và Landsat-8/9 (30m) BỊ TẮT ĐIỆN HOÀN TOÀN. "
        "Ảnh chụp từ trên trời xuống chỉ thấy một màu trắng xóa của mây. Khi pixel bị mây che, không có thuật toán nào có thể tính được NDVI, NDWI hay nhận diện ruộng lúa bên dưới!"
    )

    add_h2("2.2. Tại Sao Chưa Giải Quyết Triệt Để Trong Project?")
    add_bullet(" Trong giao diện FieldShift, chúng ta sử dụng lớp ảnh lưu trữ tuyển chọn không mây 'Esri Clarity' để khi phóng to nhìn thấy ruộng rõ ràng. Nhưng đây là ảnh TĨNH được chụp trong quá khứ (có thể từ 6 tháng hoặc 1 năm trước). Nó chỉ đóng vai trò bản đồ nền (Basemap) cho mắt người nhìn, chứ KHÔNG phản ánh được tình trạng mùa màng của ngày hôm nay!", "1. Giải pháp hiện tại chỉ là Basemap tĩnh:")
    add_bullet(" Phương pháp duy nhất trên thế giới để xuyên thủng mây mù 100% là dùng Radar khẩu độ tổng hợp (SAR) như vệ tinh Sentinel-1. Sóng radar C-band (bước sóng ~5.6 cm) không bị ảnh hưởng bởi hạt nước trong mây. Tuy nhiên, xử lý ảnh SAR đòi hỏi:", "2. Rào cản xử lý ảnh Radar SAR:")
    add_bullet("      • Thuật toán khử nhiễu hạt muối tiêu (Speckle noise filtering: Lee, Frost filter).")
    add_bullet("      • Chuyển đổi dữ liệu nhị phân thô phức tạp sang hệ số tán xạ ngược chuẩn hóa Sigma Nought (σ⁰ tính bằng decibel dB).")
    add_bullet("      • Dung lượng một cảnh ảnh SAR lên tới 1.5 GB – 2.0 GB mỗi khung hình.")
    add_bullet(" Một máy chủ web nhẹ như Django không thể tải và xử lý tức thì các tệp nhị phân SAR 2GB mỗi khi có nông dân truy cập web.", "3. Hạ tầng máy chủ giới hạn:")

    # =============================================================
    # VẤN ĐỀ 3
    # =============================================================
    add_h1("VẤN ĐỀ 3: THIẾU DỮ LIỆU ĐO MẶT ĐẤT ĐỂ HIỆU CHUẨN (LACK OF GROUND TRUTH CALIBRATION)")

    add_h2("3.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_body(
        "Mọi dữ liệu vệ tinh đều là 'ước lượng gián tiếp' (Inferred Estimation):",
        "• Bản chất mô hình hóa: "
    )
    add_bullet(" Vệ tinh không cắm que đo nhiệt độ vào đất mà đo năng lượng bức xạ hồng ngoại nhiệt từ quỹ đạo, sau đó tính ngược ra nhiệt độ bề mặt đất LST dựa trên giả định về hệ số phát xạ bề mặt (Surface Emissivity).", "Nhiệt độ mặt đất:")
    add_bullet(" Độ ẩm tầng rễ (0–100 cm: `GWETROOT`) KHÔNG PHẢI là kết quả đo trực tiếp. Vệ tinh SMAP chỉ đo được 5cm đất tầng mặt; giá trị tầng rễ 1 mét là do mô hình thủy văn ngầm (Catchment Land Surface Model) của NASA tự tính toán suy diễn dựa trên cân bằng nước bốc thoát hơi.", "Độ ẩm vùng rễ:")
    add_body(
        "Tuy nhiên, đất đai ở Việt Nam cực kỳ đa dạng: Đất cát pha ở Nghi Lộc (Nghệ An) thoát nước cực nhanh, chỉ sau 2 ngày nắng là khô khốc; "
        "trong khi đất phù sa thịt nặng ở Hưng Nguyên giữ nước cả tuần. Mô hình toàn cầu của NASA không thể nắm hết được các vi biến dị thổ nhưỡng này nếu không có dữ liệu thực tế tại địa phương."
    )

    add_h2("3.2. Tại Sao Chưa Giải Quyết Được?")
    add_bullet(" Để hiệu chuẩn mô hình vệ tinh cần mạng lưới trạm cảm biến đo độ ẩm đất tự động (In-situ soil moisture stations) cắm rải rác trên các cánh đồng tại Nghệ An và Bến Tre. Chi phí lắp đặt và duy trì các trạm cảm biến IoT này rất tốn kém (vài chục triệu đồng/trạm), dự án hackathon chưa có ngân sách triển khai phần cứng vật lý.", "1. Chi phí trạm đo IoT:")
    add_bullet(" Các dữ liệu đo đạc nông nghiệp chính quy của các Viện Nghiên cứu Nông nghiệp Việt Nam (VAAS, Viện Thổ nhưỡng Nông hóa) thường không mở công khai qua API mà lưu trữ nội bộ dưới dạng báo cáo giấy hoặc file Excel không có tọa độ chuẩn GIS.", "2. Dữ liệu đối chứng bị đóng kín:")

    # =============================================================
    # VẤN ĐỀ 4
    # =============================================================
    add_h1("VẤN ĐỀ 4: ĐỘNG CƠ LUÂN CANH CÂY TRỒNG MANG TÍNH 'QUY TẮC CỐ ĐỊNH' (RULE-BASED VS DYNAMIC SIMULATION)")

    add_h2("4.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_body(
        "Hiện tại, thuật toán đề xuất luân canh trong `rotation_engine.py` vận hành theo cơ chế Hệ Chuyên Gia Dựa Trên Luật (Rule-based Decision Trees):",
        "• Cơ chế hiện tại: "
    )
    add_bullet(" Nếu NASA phát hiện `extreme_heat_alert = True` (nhiệt độ >38°C vào mùa hè) → Đề xuất Lạc Sen Thọ / L14.", "Quy tắc 1:")
    add_bullet(" Nếu phát hiện `flood_risk_alert = True` (mưa lũ tháng 9–10) → Đề xuất lùi vụ xuống sau 15/10 và trồng Khoai lang Hoàng Long / Ngô nếp.", "Quy tắc 2:")
    add_body(
        "Hạn chế lớn: Đây là mô hình bán tĩnh. Nó CHƯA PHẢI là một mô hình mô phỏng sinh thái học nông nghiệp động (Dynamic Crop Simulation Model). "
        "Nó chưa trả lời được các câu hỏi chi tiết của nông dân như: 'Nếu tôi gieo hạt muộn 7 ngày thì năng suất giảm bao nhiêu %?', 'Lượng phân đạm cần bón chính xác là bao nhiêu kg cho thửa ruộng của tôi?'."
    )

    add_h2("4.2. Tại Sao Chưa Có Hướng Giải Quyết Triệt Để?")
    add_bullet(" Các mô hình mô phỏng cây trồng động hàng đầu thế giới (như DSSAT - Decision Support System for Agrotechnology Transfer, hay APSIM) đòi hỏi hàng trăm thông số đầu vào: Độ dày tầng cày, độ dẫn thủy lực bão hòa (Ksat), chỉ số diện tích lá (LAI), nồng độ CO2 cục bộ, hàm lượng cacbon hữu cơ tầng đất (SOC). Người nông dân không thể cung cấp các tham số phức tạp này.", "1. Đòi hỏi quá nhiều tham số đầu vào:")
    add_bullet(" Khuyết thiếu yếu tố 'Thị trường & Kinh tế': Nông dân không trồng cây chỉ vì cây đó chịu được hạn. Họ chỉ trồng cây nếu bán được có lãi! Dự án chưa tích hợp được API giá nông sản thị trường thời gian thực (ví dụ: giá lạc củ, giá khoai thương phẩm tại chợ đầu mối Nghệ An) để tính toán bài toán tối ưu hóa lợi nhuận tài chính.", "2. Bài toán kinh tế chuỗi cung ứng:")

    # =============================================================
    # VẤN ĐỀ 5
    # =============================================================
    add_h1("VẤN ĐỀ 5: BẢN ĐỒ XÂM NHẬP MẶN MANG TÍNH CHẤT MÔ PHỎNG ĐỆM TĨNH (STATIC SPATIAL BUFFER)")

    add_h2("5.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_body(
        "Lớp ranh mặn 4‰ và 1‰ tại Bến Tre và cửa sông Lam trong dự án hiện nay là các đa giác hình học (GeoJSON polygons) được số hóa cố định dựa trên báo cáo kịch bản mùa khô lịch sử.",
        "• Bản chất lớp ranh mặn: "
    )
    add_body(
        "Nhưng trên thực tế, ranh giới mặn ở Đồng bằng Sông Cửu Long KHÔNG HỀ ĐỨNG YÊN. Nó dao động tiến lùi hàng chục kilomet theo từng con nước: "
        "Lúc triều cường (rằm và mùng một âm lịch), lưỡi mặn bị đẩy sâu vào đất liền tới 50–70 km; khi triều kiệt hoặc khi thượng nguồn xả lũ, nước ngọt lại đẩy mặn lùi ra cửa biển. "
        "Bản đồ tĩnh hiện tại chưa thể báo cho nông dân biết: 'Chính xác lúc 14h chiều nay trạm bơm xã Phú Hưng có mở cống lấy nước được không?'."
    )

    add_h2("5.2. Tại Sao Lại Không Giải Quyết Được Ngay?")
    add_bullet(" Dự báo mặn động đòi hỏi chạy mô hình thủy động lực học 1 chiều / 2 chiều (như MIKE 11, HEC-RAS, Delft3D) giải hệ phương trình vi phân Saint-Venant kết hợp phương trình khuếch tán bình lưu nồng độ muối.", "1. Độ phức tạp của Mô hình Thủy văn 1D/2D:")
    add_bullet(" Dữ liệu vận hành thủy điện thượng nguồn bí mật: Lưu lượng nước ngọt đổ về ĐBSCL phụ thuộc trực tiếp vào việc xả nước của các đập thủy điện khổng lồ trên dòng chính Mekong ở Trung Quốc (chuỗi đập Lan Thương) và Lào. Dữ liệu xả nước này không được công bố theo thời gian thực, dẫn đến không thể tính chính xác lưu lượng xả về hạ lưu.", "2. Yếu tố địa chính trị nguồn nước quốc tế:")

    # =============================================================
    # VẤN ĐỀ 6
    # =============================================================
    add_h1("VẤN ĐỀ 6: KHOẢNG CÁCH SỐ & KHẢ NĂNG TIẾP CẬN CỦA BÀ CON NÔNG DÂN (DIGITAL DIVIDE)")

    add_h2("6.1. Hiện Trạng & Vấn Đề Thực Tế")
    add_bullet(" Nông dân Việt Nam đa số lớn tuổi, quen dùng smartphone để lướt Zalo, Facebook hoặc xem video TikTok; họ rất ngại mở trình duyệt web gõ URL hay nhìn các biểu đồ đường Chart.js phức tạp.", "• Thói quen người dùng:")
    add_bullet(" Thuật ngữ khoa học viễn thám như `GWETROOT`, `T2M_MAX`, `Soil Health Score` là quá hàn lâm đối với người làm nông trực tiếp.", "• Ngôn ngữ hiển thị:")

    add_h2("6.2. Hướng Giải Quyết Khả Thi")
    add_bullet(" Tích hợp ứng dụng Zalo Mini App hoặc Chatbot Zalo Official Account: Nông dân chỉ cần bấm 'Gửi vị trí hiện tại' trên Zalo, chatbot sẽ tự động gọi backend Django và trả về tin nhắn thoại ngắn gọn bằng tiếng Việt: 'Chào bác, tuần này nắng gắt gió Lào trên 40 độ, bác không nên cấy lúa mà nên gieo lạc giống L14'.", "1. Zalo Mini App & Voice Chatbot:")
    add_bullet(" Hệ thống SMS cảnh báo thiên tai tự động đẩy về điện thoại khi dữ liệu NASA ghi nhận chỉ số nhiệt độ hoặc lượng mưa vượt ngưỡng an toàn.", "2. Dịch vụ tin nhắn cảnh báo chủ động:")

    # =============================================================
    # TỔNG KẾT & BẢNG MA TRẬN
    # =============================================================
    add_h1("TỔNG KẾT: MA TRẬN PHÂN LOẠI CÁC GIỚI HẠN & KẾ HOẠCH HÀNH ĐỘNG")
    add_body("Bảng tổng hợp phân loại mức độ rào cản kỹ thuật và lộ trình khắc phục cho các phiên bản tiếp theo:")

    tbl_sum = doc.add_table(rows=7, cols=4)
    tbl_sum.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sum.autofit = False
    col_w = [Inches(1.8), Inches(1.3), Inches(2.1), Inches(1.3)]
    for row in tbl_sum.rows:
        for i, w in enumerate(col_w):
            row.cells[i].width = w

    headers_sum = ["Vấn đề kỹ thuật", "Bản chất rào cản", "Nguyên nhân cốt lõi", "Hướng giải quyết (Roadmap)"]
    for i, t in enumerate(headers_sum):
        cell = tbl_sum.cell(0, i)
        set_cell_background(cell, "991B1B") # Dark Red
        set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        r = p.add_run(t)
        r.bold = True
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    data_sum = [
        ["Độ phân giải không gian thô (50km vs 500m²)", "Vật lý vệ tinh & Tài nguyên AI", "Bước sóng vi sóng dài; thiếu GPU server để chạy AI Spatial Downscaling thời gian thực.", "Sử dụng DEM 30m + Sentinel-2 kết hợp mô hình Super-Resolution offline."],
        ["Mù vệ tinh do mây nhiệt đới", "Quang học khí quyển", "Hạt nước trong mây tán xạ hoàn toàn ánh sáng quang học; xử lý Radar SAR quá nặng.", "Xây dựng pipeline xử lý ảnh Radar Sentinel-1 SAR trên Google Earth Engine."],
        ["Thiếu trạm đo mặt đất (Ground Truth)", "Hạ tầng & Tài chính", "Chi phí trạm đo IoT đắt đỏ; dữ liệu thổ nhưỡng viện nghiên cứu bị đóng kín.", "Hợp tác với các hợp tác xã nông nghiệp lắp trạm mẫu thí điểm."],
        ["Động cơ luân canh còn dạng luật tĩnh", "Độ phức tạp nông học & thị trường", "Mô hình sinh trưởng cây trồng DSSAT đòi hỏi quá nhiều tham số; thiếu API giá nông sản.", "Tích hợp mô hình AquaCrop rút gọn và kết nối API giá chợ đầu mối."],
        ["Bản đồ ranh mặn chưa theo thời gian thực", "Thủy văn & Địa chính trị", "Thiếu lưu lượng xả đập thủy điện thượng nguồn Mekong; mô hình 1D MIKE 11 quá đồ sộ.", "Thu thập dữ liệu trạm đo mặn tự động của Tổng cục Thủy lợi qua Web Scraping."],
        ["Rào cản tiếp cận của nông dân", "Trải nghiệm & Thói quen số", "Giao diện web bản đồ quá phức tạp với nông dân lớn tuổi; thuật ngữ hàn lâm.", "Chuyển đổi giao diện sang Zalo Mini App và Chatbot giọng nói tiếng Việt."]
    ]

    for row_idx, row_data in enumerate(data_sum, start=1):
        bg = "FEF2F2" if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, val in enumerate(row_data):
            cell = tbl_sum.cell(row_idx, col_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 80, 80, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Arial"
            r.font.size = Pt(8.5)
            if col_idx == 0:
                r.bold = True
                r.font.color.rgb = RGBColor(153, 27, 27)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    add_alert_box(
        doc,
        "Kinh nghiệm trả lời Ban Giám Khảo: Khi được hỏi 'Tại sao các bạn chưa giải quyết vấn đề độ phân giải 50km của NASA?', hãy tự tin trả lời: 'Chúng tôi hiểu rất rõ giới hạn vật lý của cảm biến vi sóng băng L (SMAP). Hiện tại mục tiêu của FieldShift là Định hướng chiến lược cấp xã/huyện (Strategic Macro-level DSS), giúp chính quyền và hợp tác xã nhận diện nguy cơ sốc nhiệt gió Lào để ban hành lịch thời vụ tổng thể. Ở phiên bản tiếp theo, chúng tôi sẽ tích hợp mô hình AI Downscaling kết hợp ảnh SAR Sentinel-1 để giải quyết bài toán cấp vi mô từng thửa ruộng!'. Cách trả lời này sẽ ghi điểm tuyệt đối!",
        title="BÍ QUYẾT BẢO VỆ DỰ ÁN TRƯỚC BAN GIÁM KHẢO NASA",
        box_type="info"
    )

    # Lưu file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Report saved successfully at: {output_path}")

if __name__ == "__main__":
    out_file = r"d:\project\project-local\vientham\docs\CAC_VAN_DE_CHUA_GIAI_QUYET_VA_GIOI_HAN_PROJECT.docx"
    build_unresolved_issues_document(out_file)
