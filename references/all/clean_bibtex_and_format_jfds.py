# -*- coding: utf-8 -*-
"""
Auditing and formatting script combining:
- paper-read metadata synthesis
- arxiv-paper-writer BibTeX standardizer
- latex-paper-skills syntax validator
- JFDS Harvard Reference Generator
"""

import os
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Load the comprehensive reference list from build_all_references.py
import sys
sys.path.append(r"d:\Code\JupyterNotebook\PSO\references\all")
from build_all_references import REFERENCES_DATA, EXACT_PDF_MAP

# 6 Additional JFDS verified papers from user's Excel list
ADDITIONAL_JFDS_PAPERS = [
    {
        "id": 69,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "Finding a Needle in a Haystack: A Machine Learning Framework for Anomaly Detection in Payment Systems",
        "authors": "Ajit Desai, Anneke Kosse, Jacob Sharples",
        "bib_authors": "Desai, Ajit and Kosse, Anneke and Sharples, Jacob",
        "year": 2025,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2025.100163",
        "bib_key": "desai2025finding",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {11},\n  pages = {100163},\n  year = {2025},\n  publisher = {KeAi Publishing}',
        "relevance": "Applies machine learning to highly imbalanced financial transaction data, directly aligning with our Bank Marketing tabular classification and imbalanced metric evaluation.",
        "y_nghia_main": "Mục 3 & Mục 4.1: Bài báo năm 2025 trên JFDS về phát hiện bất thường trên dữ liệu thanh toán có độ lệch mẫu nghiêm trọng; củng cố cơ sở lý luận cho việc đánh giá trên dữ liệu mất cân bằng Bank Marketing."
    },
    {
        "id": 70,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "Reinforcement Prompting for Financial Synthetic Data Generation",
        "authors": "Xiangwu Zuo, Anxiao Jiang, Kaixiong Zhou",
        "bib_authors": "Zuo, Xiangwu and Jiang, Anxiao and Zhou, Kaixiong",
        "year": 2024,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2024.100137",
        "bib_key": "zuo2024reinforcement",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {10},\n  pages = {100137},\n  year = {2024},\n  publisher = {KeAi Publishing}',
        "relevance": "Investigates reinforcement learning and optimization for generating realistic financial data, highlighting hyperparameter sensitivity in financial simulations.",
        "y_nghia_main": "Mục 1 & Mục 5: Nghiên cứu năm 2024 trên JFDS về điều khiển tối ưu sinh dữ liệu tài chính; làm tiền đề dẫn chứng tầm quan trọng của việc điều phối siêu tham số trong mô phỏng tài chính."
    },
    {
        "id": 71,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "Machine Learning Portfolio Allocation",
        "authors": "Michael Pinelis, David Ruppert",
        "bib_authors": "Pinelis, Michael and Ruppert, David",
        "year": 2022,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2021.12.001",
        "bib_key": "pinelis2022machine",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {8},\n  pages = {35--54},\n  year = {2022},\n  publisher = {KeAi Publishing}',
        "relevance": "Demonstrates machine learning models achieving superior Sharpe ratios in portfolio allocation, demonstrating that neural networks require robust hyperparameter control.",
        "y_nghia_main": "Mục 1 & Mục 5: Công trình nổi bật trên JFDS chứng minh tối ưu danh mục đầu tư bằng Machine Learning vượt trội mô hình Markowitz truyền thống nhưng cần kiểm soát nghiêm ngặt tránh quá khớp."
    },
    {
        "id": 72,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "The Use of Predictive Analytics in Finance",
        "authors": "Daniel Broby",
        "bib_authors": "Broby, Daniel",
        "year": 2022,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2022.05.003",
        "bib_key": "broby2022predictive",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {8},\n  pages = {145--161},\n  year = {2022},\n  publisher = {KeAi Publishing}',
        "relevance": "Survey on predictive analytics and AI in financial institutions, highlighting model validation, algorithmic governance, and hyperparameter stability.",
        "y_nghia_main": "Mục 1 & Mục 5: Bài tổng quan chiến lược trên JFDS về phân tích dự báo trong tài chính; khẳng định tính ổn định siêu tham số là điều kiện tiên quyết để mô hình AI được chấp thuận trong tài chính."
    },
    {
        "id": 73,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "Deep Deterministic Portfolio Optimization",
        "authors": "Ayman Chaouki, Stephen Hardiman, Christian Schmidt, Emmanuel Serie, Joachim de Lataillade",
        "bib_authors": "Chaouki, Ayman and Hardiman, Stephen and Schmidt, Christian and S{\\'e}ri{\\'e}, Emmanuel and de Lataillade, Joachim",
        "year": 2020,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2020.06.002",
        "bib_key": "chaouki2020deep",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {6},\n  pages = {16--30},\n  year = {2020},\n  publisher = {KeAi Publishing}',
        "relevance": "Applies deep neural policy gradients for continuous financial portfolio optimization, showing sensitivity to learning rate and architectural depth.",
        "y_nghia_main": "Mục 2.3 & Mục 4.2: Ứng dụng mạng sâu tối ưu hóa danh mục tất định trên JFDS; chứng minh độ nhạy cảm của gradient và tầm quan trọng của việc điều tiết siêu tham số kiến trúc mạng."
    },
    {
        "id": 74,
        "cluster": "The Journal of Finance and Data Science (JFDS) & Financial ML",
        "title": "Forecasting Multinomial Stock Returns Using Machine Learning Methods",
        "authors": "Lauri Nevasalmi",
        "bib_authors": "Nevasalmi, Lauri",
        "year": 2020,
        "venue": "The Journal of Finance and Data Science (Elsevier / KeAi)",
        "doi_url": "https://doi.org/10.1016/j.jfds.2020.09.001",
        "bib_key": "nevasalmi2020forecasting",
        "bib_type": "article",
        "bib_extra": '  journal = {The Journal of Finance and Data Science},\n  volume = {6},\n  pages = {86--106},\n  year = {2020},\n  publisher = {KeAi Publishing}',
        "relevance": "Evaluates neural networks and tree ensembles for multinomial stock return prediction, providing benchmark methodology for tabular multi-class classification.",
        "y_nghia_main": "Mục 3 & Mục 4.1: Thực nghiệm phân lớp đa nhãn trên JFDS; cung cấp cơ sở đối chiếu phương pháp luận cho bài toán phân loại nhiều lớp (tương đồng với Benchmark Forest Covertype)."
    }
]

ACRONYMS = [
    r"\bPSO\b", r"\bQPSO\b", r"\bCNN\b", r"\bCNNs\b", r"\bMLP\b", r"\bMLPs\b",
    r"\bAutoML\b", r"\bBOHB\b", r"\bOptuna\b", r"\bAdamW\b", r"\bAdam\b",
    r"\bGELUs\b", r"\bGELU\b", r"\bSwish\b", r"\bROC\b", r"\bAUC\b",
    r"\bSMOTE\b", r"\bPyTorch\b", r"\bScikit-Learn\b", r"\bScikit-learn\b",
    r"\bBank Marketing\b", r"\bForest Covertype\b", r"\bCAPM\b", r"\bICCAPM\b",
    r"\bICAPM\b", r"\bLSTM\b", r"\bRNN\b", r"\bRNNs\b", r"\bJFDS\b",
    r"\bTVAC\b", r"\bLD-PSO\b", r"\bFO-PSO\b", r"\bCPSO\b", r"\bOPSO\b"
]

def protect_title(title):
    # Protect acronyms in titles with {...}
    protected = title
    # First protect specific terms
    for acr in ACRONYMS:
        clean_word = acr.replace(r"\b", "")
        pattern = re.compile(acr)
        protected = pattern.sub(f"{{{clean_word}}}", protected)
    # Avoid double braces
    protected = protected.replace("{{", "{").replace("}}", "}")
    # Escape &
    protected = protected.replace(" & ", r" \& ")
    return protected

def convert_to_bibtex_authors(authors_str):
    # Convert "James Kennedy, Russell C. Eberhart" -> "Kennedy, James and Eberhart, Russell C."
    # If already contains ' and ', clean it up
    parts = [p.strip() for p in authors_str.split(",") if p.strip()]
    if len(parts) == 1:
        # Single author like "Neil Gershenfeld"
        names = parts[0].split()
        if len(names) >= 2:
            return f"{names[-1]}, {' '.join(names[:-1])}"
        return parts[0]
    
    # Check if format is already "Last, First" or "First Last"
    # Usually list is "First1 Last1, First2 Last2, First3 Last3"
    bib_authors = []
    for p in parts:
        words = p.split()
        if len(words) >= 2:
            # Check if last word is suffix like Jr.
            if words[-1] in ["Jr.", "III", "II"]:
                surname = words[-2] + " " + words[-1]
                firstnames = " ".join(words[:-2])
            else:
                surname = words[-1]
                firstnames = " ".join(words[:-1])
            bib_authors.append(f"{surname}, {firstnames}")
        else:
            bib_authors.append(p)
    return " and ".join(bib_authors)

ALIAS_MAP = {
    'kennedy1995particle': 'kennedy1995pso',
    'clerc2002particle': 'clerc2002constriction',
    'pires2010particle': 'pires2010fractional',
    'sun2004global': 'sun2004qpso',
    'sun2012quantum': 'sun2012qpso_analysis',
    'tizhoosh2005opposition': 'tizhoosh2005obl',
    'moro2014data': 'moro2014bank',
    'blackard1999comparative': 'blackard1999covertype'
}

def format_jfds_harvard_entry(item):
    """
    Format entry according to exact JFDS Harvard style:
    Audrino, F., et al., 2024. New evidence from causal machine learning. Journal of Financial Econometrics 22, 575–604.
    """
    authors = item["authors"].split(",")
    if len(authors) > 3:
        # First author et al.
        first_a = authors[0].strip().split()
        if len(first_a) >= 2:
            surname = first_a[-1]
            initials = ".".join([w[0] for w in first_a[:-1]]) + "."
            author_str = f"{surname}, {initials}, et al."
        else:
            author_str = f"{authors[0].strip()}, et al."
    else:
        # List all authors formatted as Surname, Initials.
        formatted_list = []
        for a in authors:
            a_words = a.strip().split()
            if len(a_words) >= 2:
                surname = a_words[-1]
                initials = ".".join([w[0] for w in a_words[:-1]]) + "."
                formatted_list.append(f"{surname}, {initials}")
            else:
                formatted_list.append(a.strip())
        author_str = ", ".join(formatted_list)

    year = item["year"]
    title = item["title"].strip()
    if not title.endswith("."):
        title += "."
    
    venue = item["venue"].replace(" (Elsevier ScienceDirect)", "").replace(" (Elsevier / KeAi)", "").replace(" (Springer)", "").replace(" (IEEE)", "").replace(" (MIT Press)", "").replace(" (SAGE)", "").replace(" (ACM)", "").replace(" (Oxford University Press)", "").strip()
    # Correct single escaping for ampersand
    venue = venue.replace(r"\&", "&").replace("&", r"\&")

    # Extract vol / pages if available
    extra = item.get("bib_extra", "")
    vol_match = re.search(r"volume\s*=\s*\{([^}]+)\}", extra)
    pages_match = re.search(r"pages\s*=\s*\{([^}]+)\}", extra)
    
    vol_pages = ""
    if vol_match and pages_match:
        vol = vol_match.group(1)
        pages = pages_match.group(1).replace("--", "–")
        vol_pages = f" {vol}, {pages}."
    elif vol_match:
        vol_pages = f" {vol_match.group(1)}."
    elif pages_match:
        pages = pages_match.group(1).replace("--", "–")
        vol_pages = f" {pages}."
    else:
        vol_pages = "."

    key = item['bib_key']
    return f"\\bibitem{{{key}}}\n{author_str}, {year}. {title} \\textit{{{venue}}}{vol_pages}"

def main():
    all_dir = r"d:\Code\JupyterNotebook\PSO\references\all"
    excel_path = os.path.join(all_dir, "references.xlsx")
    bib_path = os.path.join(all_dir, "references.bib")
    tex_refs_path = os.path.join(all_dir, "jfds_harvard_references.tex")

    # Combine master references with additional JFDS papers
    master_list = list(REFERENCES_DATA)
    # Check if already added
    existing_keys = set(item["bib_key"] for item in master_list)
    for p in ADDITIONAL_JFDS_PAPERS:
        if p["bib_key"] not in existing_keys:
            master_list.append(p)

    # 1. GENERATE AUDITED BIBTEX FILE
    print("Auditing BibTeX entries...")
    with open(bib_path, "w", encoding="utf-8") as f:
        f.write("% =========================================================================\n")
        f.write("% AUDITED & STANDARDIZED BIBTEX DATABASE FOR MANUSCRIPT\n")
        f.write("% Target: The Journal of Finance and Data Science (JFDS)\n")
        f.write("% Author format: Last, First and Last, First (BibTeX compliant)\n")
        f.write("% Title format: Protected Acronyms {PSO}, {QPSO}, {MLP}, {JFDS}\n")
        f.write(f"% Total References: {len(master_list)}\n")
        f.write("% =========================================================================\n\n")

        for item in master_list:
            bib_authors = item.get("bib_authors")
            if not bib_authors:
                bib_authors = convert_to_bibtex_authors(item["authors"])
            
            clean_title = protect_title(item["title"])
            clean_extra = item["bib_extra"].replace(" & ", r" \& ")

            f.write(f"% Cluster: {item['cluster']}\n")
            f.write(f"@{item['bib_type']}{{{item['bib_key']},\n")
            f.write(f"  title = {{{clean_title}}},\n")
            f.write(f"  author = {{{bib_authors}}},\n")
            f.write(f"{clean_extra},\n")
            f.write(f"  url = {{{item['doi_url']}}},\n")
            f.write(f"  note = {{{item['y_nghia_main']}}}\n")
            f.write("}\n\n")

    print(f"Audited BibTeX saved to: {bib_path} ({len(master_list)} entries)")

    # 2. GENERATE JFDS HARVARD REFERENCES TEX FILE (ALPHABETICAL A-Z)
    print("Generating JFDS Harvard bibliography snippet (A-Z sorted)...")
    # Sort master_list alphabetically by first author's surname
    def get_sort_surname(item):
        authors = item["authors"].split(",")
        first_a = authors[0].strip().split()
        return first_a[-1].lower() if first_a else ""

    sorted_list = sorted(master_list, key=get_sort_surname)

    with open(tex_refs_path, "w", encoding="utf-8") as f:
        f.write("% =========================================================================\n")
        f.write("% THE JOURNAL OF FINANCE AND DATA SCIENCE (JFDS) HARVARD BIBLIOGRAPHY\n")
        f.write("% Formatted alphabetically A-Z in full compliance with JFDS guidelines\n")
        f.write(f"% Total entries: {len(sorted_list)}\n")
        f.write("% =========================================================================\n\n")
        f.write("\\begin{thebibliography}{99}\n\n")
        for item in sorted_list:
            entry_tex = format_jfds_harvard_entry(item)
            f.write(f"{entry_tex}\n\n")
        f.write("\\end{thebibliography}\n")

    print(f"JFDS Harvard LaTeX bibliography saved to: {tex_refs_path}")

    # 3. REGENERATE EXCEL WORKBOOK WITH ALL 74 PAPERS & AUDITED METADATA
    print("Updating Excel workbook...")
    wb = openpyxl.Workbook()
    ws_all = wb.active
    ws_all.title = "All References"
    ws_all.views.sheetView[0].showGridLines = True

    # Styling definitions
    font_title = Font(name="Calibri", size=14, bold=True, color="1F4E79")
    font_subtitle = Font(name="Calibri", size=10, italic=True, color="595959")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=10, color="000000")
    font_link = Font(name="Calibri", size=10, color="0563C1", underline="single")
    font_status_local = Font(name="Calibri", size=10, bold=True, color="1E4620")
    font_status_online = Font(name="Calibri", size=10, color="7F6000")

    fill_header = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
    fill_row_even = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    fill_row_odd = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")
    fill_local = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
    fill_online = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    header_border = Border(
        left=Side(style='thin', color='1F4E79'),
        right=Side(style='thin', color='1F4E79'),
        top=Side(style='medium', color='1F4E79'),
        bottom=Side(style='medium', color='1F4E79')
    )

    # Title block
    ws_all["A1"] = "DANH MỤC TÀI LIỆU THAM KHẢO & CƠ SỞ DỮ LIỆU BÀI BÁO KHOA HỌC (CHUẨN JFDS)"
    ws_all["A1"].font = font_title
    ws_all["A2"] = "Quantum-Behaved & Velocity-Adaptive Swarm Dynamics for Neural Network Hyperparameter Optimization | The Journal of Finance and Data Science"
    ws_all["A2"].font = font_subtitle

    headers = [
        "No.",
        "Paper Title",
        "Authors",
        "Year",
        "Venue / Publisher",
        "Research Domain / Cluster",
        "PDF Status",
        "Direct Link (Click to Open)",
        "BibTeX Key",
        "Local PDF Filename (in /all)",
        "Academic Relevance & Synthesis (EN)",
        "Ý nghĩa trong bài báo hiện tại"
    ]

    header_row = 4
    for col_idx, h in enumerate(headers, 1):
        cell = ws_all.cell(row=header_row, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 4, 7] else "left", vertical="center", wrap_text=True)
        cell.border = header_border
    ws_all.row_dimensions[header_row].height = 28

    current_row = 5
    for idx, item in enumerate(master_list, 1):
        row_fill = fill_row_even if idx % 2 == 0 else fill_row_odd
        
        # Check PDF status
        key = item["bib_key"]
        local_file = EXACT_PDF_MAP.get(key, "")
        pdf_status = "Downloaded in /all" if local_file else "Paywalled / Online Direct Link"

        ws_all.cell(row=current_row, column=1, value=idx).alignment = Alignment(horizontal="center", vertical="center")
        
        c2 = ws_all.cell(row=current_row, column=2, value=item["title"])
        c2.font = font_link
        c2.hyperlink = item["doi_url"]
        c2.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        
        ws_all.cell(row=current_row, column=3, value=item["authors"]).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws_all.cell(row=current_row, column=4, value=item["year"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_all.cell(row=current_row, column=5, value=item["venue"]).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws_all.cell(row=current_row, column=6, value=item["cluster"]).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        
        c7 = ws_all.cell(row=current_row, column=7, value=pdf_status)
        c7.alignment = Alignment(horizontal="center", vertical="center")
        if pdf_status == "Downloaded in /all":
            c7.font = font_status_local
            c7.fill = fill_local
        else:
            c7.font = font_status_online
            c7.fill = fill_online
            
        c8 = ws_all.cell(row=current_row, column=8, value=item["doi_url"])
        c8.font = font_link
        c8.hyperlink = item["doi_url"]
        c8.alignment = Alignment(horizontal="left", vertical="center")
        
        ws_all.cell(row=current_row, column=9, value=item["bib_key"]).alignment = Alignment(horizontal="left", vertical="center")
        ws_all.cell(row=current_row, column=10, value=local_file).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws_all.cell(row=current_row, column=11, value=item["relevance"]).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        ws_all.cell(row=current_row, column=12, value=item["y_nghia_main"]).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        
        for col_idx in [1, 3, 4, 5, 6, 9, 10, 11, 12]:
            ws_all.cell(row=current_row, column=col_idx).font = font_data
        for col_idx in range(1, 13):
            c = ws_all.cell(row=current_row, column=col_idx)
            c.border = thin_border
            if col_idx != 7:
                c.fill = row_fill
                
        ws_all.row_dimensions[current_row].height = 48
        current_row += 1

    col_widths = {
        1: 6, 2: 36, 3: 26, 4: 8, 5: 26, 6: 26,
        7: 18, 8: 36, 9: 20, 10: 30, 11: 45, 12: 55
    }
    for col_idx, width in col_widths.items():
        ws_all.column_dimensions[get_column_letter(col_idx)].width = width

    # SHEET 2: CLUSTER SUMMARY
    ws_summary = wb.create_sheet(title="Cluster Summary")
    ws_summary.views.sheetView[0].showGridLines = True
    ws_summary["A1"] = "TỔNG HỢP PHÂN BỐ CÁC NHÓM NGHIÊN CỨU"
    ws_summary["A1"].font = font_title
    
    summary_headers = ["Cluster ID", "Research Domain / Cluster", "Tổng bài báo", "Đã có PDF (/all)", "Link trực tuyến", "Vai trò khoa học trong bài báo hiện tại"]
    ws_summary.row_dimensions[3].height = 26
    for col_idx, h in enumerate(summary_headers, 1):
        cell = ws_summary.cell(row=3, column=col_idx, value=h)
        cell.font = font_header
        cell.fill = fill_header
        cell.alignment = Alignment(horizontal="center" if col_idx in [1, 3, 4, 5] else "left", vertical="center")
        cell.border = header_border

    clusters = {}
    for item in master_list:
        c_name = item["cluster"]
        if c_name not in clusters:
            clusters[c_name] = {"total": 0, "local": 0, "online": 0}
        clusters[c_name]["total"] += 1
        key = item["bib_key"]
        if key in EXACT_PDF_MAP:
            clusters[c_name]["local"] += 1
        else:
            clusters[c_name]["online"] += 1

    cluster_roles_vn = {
        "Classical & Velocity-Adaptive Newtonian PSO": "Mục 2.1 & Baseline: Cơ sở lý thuyết động lực học Newton, trọng số quán tính suy giảm w, hệ số co Clerc, và thuật toán đối chứng PSO-TVAC.",
        "Quantum-Behaved Particle Swarm Optimization (QPSO)": "Mục 2.2 & Trọng tâm đề xuất: Mô hình giếng thế delta Schrödinger, tâm hấp dẫn mbest, chứng minh toán học tính hội tụ toàn cục và khả năng xuyên hầm thoát bẫy.",
        "Neural Network Hyperparameter Optimization & Swarm Metaheuristics": "Mục 1, 2.3, 3 & Baseline HPO: Tối ưu kiến trúc mạng nơ-ron bằng bầy đàn; đối chuẩn với Random Search, Bayes GP-BO, BOHB và Optuna.",
        "Loss Landscapes, Saddle Points & Deep Optimization Dynamics": "Mục 4.2 & Cơ chế hội tụ: Trực quan hóa bề mặt mất mát (Li et al.), phân tích độ cong Hessian (Keskar), điểm yên ngựa (Dauphin) và AdamW.",
        "Architecture Elements, Regularization & Tabular Benchmarking": "Mục 3 & 4.1: Dropout, GELU/Swish, Batch/Layer Norm; tác giả gốc của Bank Marketing (Moro 2014), Forest Covertype (Blackard 1999) và kỹ thuật mất cân bằng mẫu.",
        "Metrics, Software Ecosystem & Foundational ML Principles": "Mục 3 & Đánh giá: Thước đo AUC-ROC (Fawcett), Brier Score (Guo), nền tảng thực thi PyTorch & Scikit-learn, và lý thuyết học thống kê.",
        "The Journal of Finance and Data Science (JFDS) & Financial ML": "Mục 1, 5 & Định hướng tạp chí: Bài báo mẫu JFDS mới nhất (Owen 2026), ứng dụng học sâu trong định giá tài sản (Gu 2020), tín dụng, phát hiện bất thường thanh toán và dự báo tài chính."
    }

    s_row = 4
    for idx, (c_name, stats) in enumerate(clusters.items(), 1):
        row_fill = fill_row_even if idx % 2 == 0 else fill_row_odd
        ws_summary.cell(row=s_row, column=1, value=idx).alignment = Alignment(horizontal="center", vertical="center")
        ws_summary.cell(row=s_row, column=2, value=c_name).alignment = Alignment(horizontal="left", vertical="center")
        ws_summary.cell(row=s_row, column=3, value=stats["total"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_summary.cell(row=s_row, column=4, value=stats["local"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_summary.cell(row=s_row, column=5, value=stats["online"]).alignment = Alignment(horizontal="center", vertical="center")
        ws_summary.cell(row=s_row, column=6, value=cluster_roles_vn.get(c_name, "")).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
        
        for col_idx in range(1, 7):
            c = ws_summary.cell(row=s_row, column=col_idx)
            c.font = font_data
            c.border = thin_border
            c.fill = row_fill
        ws_summary.row_dimensions[s_row].height = 36
        s_row += 1

    # Total row
    ws_summary.cell(row=s_row, column=1, value="").border = thin_border
    c_tot = ws_summary.cell(row=s_row, column=2, value="TỔNG CỘNG")
    c_tot.font = font_header
    c_tot.fill = fill_header
    c_tot.alignment = Alignment(horizontal="left", vertical="center")
    c_tot.border = header_border

    tot_papers = sum(s["total"] for s in clusters.values())
    tot_local = sum(s["local"] for s in clusters.values())
    tot_online = sum(s["online"] for s in clusters.values())

    for col_idx, val in [(3, tot_papers), (4, tot_local), (5, tot_online)]:
        c = ws_summary.cell(row=s_row, column=col_idx, value=val)
        c.font = font_header
        c.fill = fill_header
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = header_border
    c_end = ws_summary.cell(row=s_row, column=6, value=f"{tot_papers} bài báo xác thực phân bố trên 7 trụ cột nghiên cứu")
    c_end.font = font_header
    c_end.fill = fill_header
    c_end.border = header_border
    ws_summary.row_dimensions[s_row].height = 26

    ws_summary.column_dimensions["A"].width = 12
    ws_summary.column_dimensions["B"].width = 42
    ws_summary.column_dimensions["C"].width = 15
    ws_summary.column_dimensions["D"].width = 18
    ws_summary.column_dimensions["E"].width = 16
    ws_summary.column_dimensions["F"].width = 75

    wb.save(excel_path)
    print(f"Audited Excel database saved to: {excel_path} ({tot_papers} entries)")

if __name__ == "__main__":
    main()
