"""
Build the complete college-formatted FINAL_REPORT.docx and export FINAL_REPORT.pdf
(60 to 70 pages) strictly adhering to MIA-Project Template.docx and verified against
friend report.pdf.

Includes:
  - Exact A4 dimensions (21.0 x 29.7 cm) and margins (Left 3.81 cm, Right/Top/Bottom 2.54 cm)
  - Times New Roman 12pt body text, 12pt Bold CHAPTER N + 16pt Bold Title, 14pt Section, 12pt Subsection
  - Widow/orphan control without whole-paragraph keep_together blocks (eliminates bottom-of-page gaps)
  - Generous, uniform table column spacing and left-aligned cell text (eliminates stretched river gaps)
  - 3-figures-per-page stacked layout on exactly 2 interior visual pages (Chapter 7 & Chapter 8)
  - Clickable blue hyperlinks (#0563C1) and italicized venues in 12pt APA References
  - Two-pass exact page-number resolution via Microsoft Word COM + PyMuPDF
"""
from __future__ import annotations

import os
import re
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import docx
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
from docx.shared import Cm, Inches, Pt, RGBColor
from PIL import Image

ROOT = Path(r"E:\trueguard")
CAPSTONE = ROOT / "CAPSTONE"
FINAL_DIR = CAPSTONE / "FInal"
FIG_DIR = ROOT / "outputs" / "figures"

sys.path.insert(0, str(FINAL_DIR / "tools"))
from generate_hd_stacked_figures import generate_all_hd_figures, generate_hd_vit_logo

LOGO_PATH = generate_hd_vit_logo()
from build_40paper_literature_review import PILLARS
from report_ch1_ch2_data import CH1_SECTIONS, CH2_SECTIONS
from report_ch3_ch4_data import (
    CROSS_PILLAR_SYNTHESIS_ROWS,
    PILLAR_NARRATIVES,
    PILLAR_SECTION_TITLES,
    PILLAR_TABLE_CAPTIONS,
)
from report_ch4_to_ch9_data import (
    CH4_SECTIONS,
    CODE_EXCERPT_1_PIPELINE,
    CODE_EXCERPT_2_SENSORS,
    CODE_EXCERPT_3_FUSION,
    CODE_EXCERPT_4_CONTROLLER,
    DATASET_SUMMARY_TABLE,
    FUNCTIONAL_REQUIREMENTS_TABLE,
    NON_FUNCTIONAL_REQUIREMENTS_TABLE,
    TECH_STACK_TABLE,
)
from report_references_data import ACRONYMS_AND_SYMBOLS, APA_REFERENCES
from report_figure_tables_data import FIG_REPLACEMENT_TABLES

REPORT_TITLE = (
    "TOWARD TRUSTWORTHY LARGE LANGUAGE MODELS: A COMPREHENSIVE REVIEW OF "
    "HALLUCINATION DETECTION, EXPLAINABILITY, AND MITIGATION STRATEGIES"
)
REPORT_TITLE_MIXED = (
    "Toward Trustworthy Large Language Models: A Comprehensive Review of "
    "Hallucination Detection, Explainability, and Mitigation Strategies"
)
CANDIDATE_NAME = "YOGESH RAVI M"
CANDIDATE_REG = "22MIA1052"
GUIDE_NAME = "Dr. PRADEEP KUMAR T.S."
PROGRAMME_NAME = "M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics"
SCHOOL_NAME = "SCHOOL OF COMPUTER SCIENCE AND ENGINEERING"
SUBMISSION_MONTH_YEAR = "NOVEMBER 2026"


# ---------------------------------------------------------------------------
# XML & Formatting Helpers (Strictly Times New Roman, A4, Template Margins)
# ---------------------------------------------------------------------------

def configure_a4_margins(section) -> None:
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(3.81)
    section.right_margin = Cm(2.54)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)


def set_section_page_numbering(section, fmt: Optional[str] = "decimal", start: Optional[int] = 1) -> None:
    """
    Configure footer bottom-center page numbering for a Word section in Times New Roman 12pt.
    fmt=None suppresses page numbers (Cover, Title, Declaration, Certificate).
    fmt="lowerRoman" sets Roman numerals (i, ii, iii...).
    fmt="decimal" sets Arabic numerals (1, 2, 3...).
    """
    footer = section.footer
    footer.is_linked_to_previous = False
    for p in list(footer.paragraphs):
        p.text = ""
    sectPr = section._sectPr
    pgNumType = sectPr.find(qn("w:pgNumType"))
    if pgNumType is None:
        pgNumType = OxmlElement("w:pgNumType")
        sectPr.append(pgNumType)
    if fmt is None:
        return
    pgNumType.set(qn("w:fmt"), fmt)
    if start is not None:
        pgNumType.set(qn("w:start"), str(start))

    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    run = p.add_run()
    run.font.name = "Times New Roman"
    run.font.size = Pt(12)

    fldChar1 = OxmlElement("w:fldChar")
    fldChar1.set(qn("w:fldCharType"), "begin")
    instrText = OxmlElement("w:instrText")
    instrText.set(qn("xml:space"), "preserve")
    instrText.text = " PAGE "
    fldChar2 = OxmlElement("w:fldChar")
    fldChar2.set(qn("w:fldCharType"), "separate")
    fldChar3 = OxmlElement("w:fldChar")
    fldChar3.set(qn("w:fldCharType"), "end")
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)


def set_cell_borders(cell, color: str = "000000", sz: str = "6") -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for edge in ("top", "bottom", "left", "right"):
        el = tcBorders.find(qn(f"w:{edge}"))
        if el is None:
            el = OxmlElement(f"w:{edge}")
            tcBorders.append(el)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), sz)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)


def set_cell_shading(cell, fill_hex: str) -> None:
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shd)


def set_cell_margins(cell, top_dxa: int = 70, bottom_dxa: int = 70, left_dxa: int = 100, right_dxa: int = 100) -> None:
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement("w:tcMar")
    for side, val in (("top", top_dxa), ("bottom", bottom_dxa), ("left", left_dxa), ("right", right_dxa)):
        m = OxmlElement(f"w:{side}")
        m.set(qn("w:w"), str(val))
        m.set(qn("w:type"), "dxa")
        tcMar.append(m)
    tcPr.append(tcMar)


def add_p(
    doc,
    text: str = "",
    size: float = 12.0,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    align=WD_ALIGN_PARAGRAPH.JUSTIFY,
    line_spacing: float = 1.22,
    space_before: float = 0.0,
    space_after: float = 5.0,
    keep_with_next: bool = False,
    keep_together: bool = False,
):
    p = doc.add_paragraph()
    p.alignment = align
    pf = p.paragraph_format
    pf.line_spacing = line_spacing
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.widow_control = True
    pf.keep_with_next = keep_with_next
    pf.keep_together = keep_together
    if text:
        clean_text = text.replace("`", "")
        r = p.add_run(clean_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(size)
        r.bold = bold
        r.italic = italic
        r.underline = underline
        r.font.color.rgb = RGBColor(0, 0, 0)
    return p


def add_chapter_heading(doc, ch_num: int, title: str, page_break_before: bool = True) -> None:
    """
    Matches MIA-Project Template.docx (P382 + P386) and friend report.pdf (Page 13):
      Line 1: CHAPTER <N> — Times New Roman, 12 pt, Bold, Centered, ALL CAPS
      Line 2: <CHAPTER TITLE> — Times New Roman, 16 pt, Bold, Centered, ALL CAPS
    """
    p_ch = add_p(
        doc,
        f"CHAPTER {ch_num}",
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.15,
        space_before=0,
        space_after=6,
        keep_with_next=True,
    )
    if page_break_before:
        p_ch.paragraph_format.page_break_before = True
    add_p(
        doc,
        title.upper(),
        size=16,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        line_spacing=1.15,
        space_before=0,
        space_after=14,
        keep_with_next=True,
    )


def add_section_heading(doc, sec_title: str) -> None:
    add_p(
        doc,
        sec_title.upper(),
        size=14,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.15,
        space_before=10,
        space_after=5,
        keep_with_next=True,
    )


def add_subsection_heading(doc, sub_title: str) -> None:
    add_p(
        doc,
        sub_title.upper(),
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.15,
        space_before=7,
        space_after=3.5,
        keep_with_next=True,
    )


def format_clean_math(eq_str: str) -> str:
    """Format raw equation ASCII / LaTeX commands into standard publication-grade math symbols."""
    eq = eq_str
    replacements = [
        ("prod_{t=1}^{n}", "∏_(t=1..n)"),
        ("sum_{t=1}^{n}", "∑_(t=1..n)"),
        ("sum_{v in V}", "∑_(v∈V)"),
        ("sum_{v=1}^{|V|}", "∑_(v=1..|V|)"),
        ("sum_{j=1}^{K_t}", "∑_(j=1..K_t)"),
        ("sum_{k=1}^{K_t}", "∑_(k=1..K_t)"),
        ("sum_{k=1}^{4}", "∑_(k=1..4)"),
        ("sum_{l in L_probe}", "∑_(l∈L_probe)"),
        ("sum_{l in L_top}", "∑_(l∈L_top)"),
        ("sum_{h=1}^{H}", "∑_(h=1..H)"),
        ("empty_set", "∅"),
        ("intersect", "∩"),
        (" in ", " ∈ "),
        ("sigma(", "σ("),
        ("alpha_", "α_"),
        ("epsilon", "ε"),
        ("sqrt(", "√("),
        ("tau_", "τ_"),
        ("theta", "θ"),
        ("hbar_", "h̄_"),
        ("Fbar", "F̄"),
        ("Abar", "Ā"),
        ("Hbar_", "H̄_"),
        ("Dbar", "D̄"),
        ("phi(", "φ("),
        ("ztilde_", "z̃_"),
        ("htilde_", "h̃_"),
        ("mu_", "μ_"),
        ("sigma_", "σ_"),
        ("integral_{0}^{1}", "∫_(0..1)"),
    ]
    for src, dst in replacements:
        eq = eq.replace(src, dst)
    return eq


def add_equation_block(doc, lhs_rhs: str, eq_num: str) -> None:
    """Render a centered mathematical equation block with right-aligned equation number (X.Y)."""
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    c0, c1 = tbl.cell(0, 0), tbl.cell(0, 1)
    c0.width = Cm(12.65)
    c1.width = Cm(2.0)
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(3)
    p0.paragraph_format.space_after = Pt(3)
    r0 = p0.add_run(format_clean_math(lhs_rhs))
    r0.font.name = "Times New Roman"
    r0.font.size = Pt(11.5)
    r0.italic = True

    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.space_before = Pt(3)
    p1.paragraph_format.space_after = Pt(3)
    r1 = p1.add_run(f"({eq_num})")
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11.5)
    r1.bold = True


TABLE_SUPPLEMENT_CAPTIONS: Dict[str, Tuple[str, str]] = {
    "3.1": ("3.1B", "PRISMA 2020 Stage-by-Stage Screening and Exclusion Breakdown (2020–2026)"),
    "4.1": ("4.1B", "Closed-Loop Feedback Control Subsystem Block Specification for TRUEGUARD"),
    "5.1": ("5.1B", "Two-Level Question-Grouped Cross-Validation and Inner OOF Stacking Protocol"),
    "7.1": ("7.1B", "Comprehensive 10-Method Detection Comparison Across Benchmarks on TinyLlama-1.1B"),
    "7.2": ("7.2B", "Out-of-Fold ROC True Positive Rate (TPR) Operating Points on TruthfulQA"),
    "7.3": ("7.3B", "Out-of-Fold ROC True Positive Rate (TPR) Operating Points on HaluEval-Summarization"),
    "7.4": ("7.4B", "Single-Sensor and Leave-One-Out Ablation Metrics on TruthfulQA (TinyLlama-1.1B)"),
    "7.5": ("7.5B", "Single-Sensor and Leave-One-Out Ablation Metrics on HaluEval-QA (TinyLlama-1.1B)"),
    "7.6": ("7.6B", "Out-of-Fold 2x2 Confusion Matrix Counts and Classification Metrics Across All Benchmarks"),
    "7.7": ("7.7B", "Calibrated Out-of-Fold Risk Score Distribution and Empirical Calibration by Regime"),
    "7.8": ("7.8B", "Cross-Benchmark Transfer Pairs and Learned Sensor Weight Vectors on TinyLlama-1.1B"),
    "8.1": ("8.1B", "Controller Tier-by-Tier Routing, Active Repair Count, and Hallucination Reduction on TriviaQA"),
    "8.2": ("8.2B", "Selective Prediction Factual Accuracy and Risk Across Coverage Operating Points"),
    "8.3": ("8.3B", "Per-Stage Computational Latency Breakdown on Tesla T4 GPU and Local CPU"),
}


def add_figure_with_caption(doc, img_path: Path, fig_id: str, caption_text: str, width_cm: float = 13.0) -> None:
    """
    Preserves all quantitative/architectural details in-place as a structured analytical table
    so that redundant single-figure pages are eliminated while 100% of the data is retained.
    The 6 essential visual figures (Figures 7.1-7.3 and Figures 8.1-8.3) are rendered 3-per-page
    on 2 dedicated visual pages via `add_stacked_figure_page`.
    """
    if fig_id in FIG_REPLACEMENT_TABLES:
        headers, rows, col_widths_cm, font_size = FIG_REPLACEMENT_TABLES[fig_id]
        sup_id, sup_cap = TABLE_SUPPLEMENT_CAPTIONS.get(fig_id, (None, None))
        add_styled_table(
            doc,
            sup_id,
            sup_cap,
            headers,
            rows,
            col_widths_cm,
            font_size=max(font_size, 9.0),
            header_fill="E8ECEF",
        )


def ensure_composite_panels() -> Dict[str, Path]:
    """
    Generates ultra-high-resolution (450 DPI, 4725 x 1980 px) figures proportioned to 14.5 x 6.07 cm
    so that 3 figures fit cleanly on 1 page in Chapter 7 and 3 figures fit on 1 page in Chapter 8
    without any right-margin overflow or pixelation when zoomed.
    """
    return generate_all_hd_figures()


def add_stacked_figure_page(doc, items: List[Tuple[str, Path, str]]) -> None:
    """
    Arranges 3 ultra-crisp 450-DPI figures cleanly on a SINGLE page (matching friend report.pdf Page 75)
    with centered 14.5-cm full-width images and 10.5pt Italic centered captions below each figure.
    """
    for idx, (fig_id, img_path, cap_text) in enumerate(items):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = p_img.paragraph_format
        if idx == 0:
            pf.page_break_before = True
        pf.space_before = Pt(2)
        pf.space_after = Pt(1)
        pf.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(str(img_path), width=Cm(14.5))

        add_p(
            doc,
            f"FIGURE {fig_id}: {cap_text.upper()}",
            size=10.0,
            bold=False,
            italic=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            line_spacing=1.08,
            space_before=1,
            space_after=5 if idx < len(items) - 1 else 2,
            keep_with_next=(idx < len(items) - 1),
        )


def add_styled_table(
    doc,
    table_id: Optional[str],
    caption_text: Optional[str],
    headers: List[str],
    rows: List[Tuple[str, ...]],
    col_widths_cm: List[float],
    font_size: float = 9.5,
    header_fill: str = "E8ECEF",
) -> None:
    if table_id and caption_text:
        add_p(
            doc,
            f"TABLE {table_id}: {caption_text.upper()}",
            size=10.5,
            bold=True,
            italic=True,
            align=WD_ALIGN_PARAGRAPH.CENTER,
            line_spacing=1.15,
            space_before=8,
            space_after=4,
            keep_with_next=True,
        )
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Normalize column widths to exact printable width 14.65 cm (21.0 - 3.81 - 2.54)
    total_w = sum(col_widths_cm)
    scale = 14.65 / total_w if total_w > 0 else 1.0
    norm_widths = [w * scale for w in col_widths_cm]

    # Repeat header row on page splits
    trPr = tbl.rows[0]._tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:tblHeader"))

    for j, h_text in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.width = Cm(norm_widths[j])
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        set_cell_borders(cell, color="000000", sz="6")
        set_cell_shading(cell, header_fill)
        set_cell_margins(cell, 75, 75, 95, 95)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.line_spacing = 1.12
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(font_size)
        r.bold = True

    for i, row in enumerate(rows, 1):
        trPr_row = tbl.rows[i]._tr.get_or_add_trPr()
        trPr_row.append(OxmlElement("w:cantSplit"))
        for j, val in enumerate(row):
            cell = tbl.cell(i, j)
            cell.width = Cm(norm_widths[j])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
            set_cell_borders(cell, color="404040", sz="4")
            if i % 2 == 0:
                set_cell_shading(cell, "F8F9FA")
            set_cell_margins(cell, 55, 55, 85, 85)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing = 1.12
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            r = p.add_run(str(val))
            r.font.name = "Times New Roman"
            r.font.size = Pt(font_size)
            if j == 0:
                r.bold = True

    if table_id is not None:
        add_p(doc, "", size=3, space_before=0, space_after=2)


def add_code_listing_box(doc, listing_title: str, code_text: str) -> None:
    add_p(
        doc,
        listing_title,
        size=10.5,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.LEFT,
        line_spacing=1.15,
        space_before=6,
        space_after=2,
        keep_with_next=True,
    )
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    cell = tbl.cell(0, 0)
    cell.width = Cm(14.65)
    set_cell_borders(cell, color="000000", sz="6")
    set_cell_shading(cell, "F5F5F5")
    set_cell_margins(cell, 90, 90, 120, 120)
    p = cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.line_spacing = 1.08
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r = p.add_run(code_text.strip())
    r.font.name = "Times New Roman"
    r.font.size = Pt(9.5)
    add_p(doc, "", size=4, space_before=0, space_after=3)


def add_hyperlink(paragraph, url: str, text: str) -> None:
    """
    Inserts a genuine clickable Word hyperlink (<w:hyperlink>) styled in standard blue (#0563C1)
    with underline, matching friend report.pdf and Microsoft Word APA reference conventions.
    """
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = OxmlElement("w:hyperlink")
    hyperlink.set(qn("r:id"), r_id)

    new_run = OxmlElement("w:r")
    rPr = OxmlElement("w:rPr")

    rFonts = OxmlElement("w:rFonts")
    rFonts.set(qn("w:ascii"), "Times New Roman")
    rFonts.set(qn("w:hAnsi"), "Times New Roman")
    rFonts.set(qn("w:cs"), "Times New Roman")
    rPr.append(rFonts)

    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "24")  # 12 pt
    szCs = OxmlElement("w:szCs")
    szCs.set(qn("w:val"), "24")
    rPr.append(sz)
    rPr.append(szCs)

    color = OxmlElement("w:color")
    color.set(qn("w:val"), "0563C1")
    rPr.append(color)

    u = OxmlElement("w:u")
    u.set(qn("w:val"), "single")
    rPr.append(u)

    new_run.append(rPr)
    t = OxmlElement("w:t")
    t.text = text
    new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)


def add_apa_reference_paragraph(doc, ref_str: str) -> None:
    """
    Renders an APA reference in 12pt Times New Roman with 1.15 line spacing,
    hanging indent, italicized venue/journal segment, and a clickable blue URL hyperlink.
    """
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.line_spacing = 1.15
    pf.space_before = Pt(0)
    pf.space_after = Pt(6.0)
    pf.left_indent = Cm(0.8)
    pf.first_line_indent = Cm(-0.8)
    pf.widow_control = True

    url_match = re.search(r"(https?://\S+)$", ref_str.strip())
    if url_match:
        url = url_match.group(1)
        body_part = ref_str[:url_match.start()].rstrip() + " "
    else:
        url = None
        body_part = ref_str

    # Split body_part into [Author (Year). Title.] and [Venue/Journal info] so venue is italicized
    m_yr = re.search(r"\(\d{4}\)\.\s+", body_part)
    if m_yr:
        after_yr = body_part[m_yr.end():]
        dot_idx = after_yr.find(". ")
        if dot_idx != -1:
            prefix_and_title = body_part[: m_yr.end() + dot_idx + 2]
            venue_rest = after_yr[dot_idx + 2 :]
            comma_idx = venue_rest.find(",")
            if comma_idx != -1:
                venue_ital = venue_rest[:comma_idx]
                venue_tail = venue_rest[comma_idx:]
            else:
                venue_ital = venue_rest
                venue_tail = ""

            r1 = p.add_run(prefix_and_title)
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(12)

            r2 = p.add_run(venue_ital)
            r2.font.name = "Times New Roman"
            r2.font.size = Pt(12)
            r2.italic = True

            if venue_tail:
                r3 = p.add_run(venue_tail)
                r3.font.name = "Times New Roman"
                r3.font.size = Pt(12)
        else:
            r1 = p.add_run(body_part)
            r1.font.name = "Times New Roman"
            r1.font.size = Pt(12)
    else:
        r1 = p.add_run(body_part)
        r1.font.name = "Times New Roman"
        r1.font.size = Pt(12)

    if url:
        add_hyperlink(p, url, url)
