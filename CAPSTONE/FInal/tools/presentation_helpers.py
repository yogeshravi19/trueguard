"""
TRUEGUARD Master 30-Slide University Final Review Presentation Builder.
Strictly complies with all Non-Negotiable Requirements:
1. Exactly 30 Slides (Never exceeds 30).
2. Exactly 4 Literature Review Slides covering all 40 papers (10 papers per slide).
3. Official University PPT styling, colors, and layout structure.
4. Integrates all 6 Research Figures (Fig 7.1, 7.2, 7.3, 7.4, 8.1, 8.2) in 600 DPI ultra-HD.
5. Meaningful visual elements throughout every slide.
6. Comprehensive academic speaker notes on every single slide.
7. Produces FINAL_TRUEGUARD_PRESENTATION.pptx and FINAL_TRUEGUARD_PRESENTATION.pdf.
"""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls

# Paths
ROOT_DIR = Path(r"E:\trueguard")
CAPSTONE_DIR = ROOT_DIR / "CAPSTONE"
FINAL_DIR = CAPSTONE_DIR / "FInal"
SUBMISSION_DIR = ROOT_DIR / "FINAL_SUBMISSION"
ASSETS_DIR = FINAL_DIR / "assets_sandhya_style"
FIG_DIR = ROOT_DIR / "outputs" / "figures"

OUT_PPTX = ROOT_DIR / "FINAL_TRUEGUARD_PRESENTATION.pptx"
OUT_PDF = ROOT_DIR / "FINAL_TRUEGUARD_PRESENTATION.pdf"

# Theme Colors (Deep Royal Navy, Amber Gold, Ice Blue, Emerald, Pure White)
NAVY_HEADER = RGBColor(15, 23, 42)      # #0F172A - Deep Midnight Header Banner
ROYAL_BLUE = RGBColor(30, 58, 138)      # #1E3A8A - Royal Blue Accent / Table Headers
AMBER_GOLD = RGBColor(245, 158, 11)     # #F59E0B - Amber Gold Highlights
EMERALD_GREEN = RGBColor(16, 185, 129)  # #10B981 - Safe / Verified Accent
CRIMSON_RED = RGBColor(220, 38, 38)     # #DC2626 - Hallucination / Risk Accent
PURE_WHITE = RGBColor(255, 255, 255)    # #FFFFFF - Crisp Card Background / Text
DARK_SLATE = RGBColor(30, 41, 59)       # #1E293B - High Contrast Body Text
MUTED_SLATE = RGBColor(71, 85, 105)     # #475569 - Secondary Body Text
LIGHT_BG = RGBColor(248, 250, 252)      # #F8FAFC - Soft Card Background
BORDER_COLOR = RGBColor(226, 232, 240)  # #E2E8F0 - Subtle Card Border

TBL_HEADER_BG = RGBColor(30, 58, 138)   # #1E3A8A - Table Header Navy
TBL_ROW_ALT1 = RGBColor(255, 255, 255)  # #FFFFFF - Table Row White
TBL_ROW_ALT2 = RGBColor(241, 245, 249)  # #F1F5F9 - Table Row Soft Blue-Gray

FONT_TITLE = "Trebuchet MS"
FONT_BODY = "Segoe UI"
FONT_BOLD = "Segoe UI Semibold"

def set_slide_background(slide, color=RGBColor(241, 245, 249)):
    """Creates a clean, elegant background for each slide."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(11.25))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    # Send to back via XML
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)

def add_header_banner(slide, title_text: str, category_text: str = "TRUEGUARD: REAL-TIME LLM HALLUCINATION GUARDRAIL"):
    """Adds standard professional university header banner."""
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(1.35))
    header.fill.solid()
    header.fill.fore_color.rgb = NAVY_HEADER
    header.line.fill.background()
    
    # Gold accent strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.35), Inches(20.0), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = AMBER_GOLD
    strip.line.fill.background()
    
    # Title Text Frame
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(15.5), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.name = FONT_BOLD
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = AMBER_GOLD
    p0.space_after = Pt(2)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = PURE_WHITE
    
    # VIT / TRUEGUARD Pill Logo badge on the right
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(16.8), Inches(0.35), Inches(2.4), Inches(0.65))
    pill.fill.solid()
    pill.fill.fore_color.rgb = ROYAL_BLUE
    pill.line.color.rgb = AMBER_GOLD
    pill.line.width = Pt(1.5)
    ptf = pill.text_frame
    ptf.text = "VIT CHENNAI"
    ptf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ptf.paragraphs[0].font.name = FONT_BOLD
    ptf.paragraphs[0].font.size = Pt(14)
    ptf.paragraphs[0].font.bold = True
    ptf.paragraphs[0].font.color.rgb = PURE_WHITE

def add_speaker_notes(slide, notes_text: str):
    """Adds rich academic speaker notes to the slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()

def create_card(slide, left: float, top: float, width: float, height: float,
                bg_color=PURE_WHITE, border_color=BORDER_COLOR, corner_radius=None) -> tuple:
    """Creates a modern elevated card container."""
    shape_type = MSO_SHAPE.ROUNDED_RECTANGLE if corner_radius else MSO_SHAPE.RECTANGLE
    card = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)
    else:
        card.line.fill.background()
    return card

def add_table_grid(slide, left: float, top: float, width: float, height: float,
                   headers: list, rows: list, col_widths: list, header_fs=12.5, cell_fs=10.5):
    """Draws a beautiful, highly readable table with alternate rows."""
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table
    
    for i, w in enumerate(col_widths):
        table.columns[i].width = Inches(w)
        
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TBL_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = FONT_BOLD
        p.font.size = Pt(header_fs)
        p.font.bold = True
        p.font.color.rgb = PURE_WHITE
        p.alignment = PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT
        
    for r_idx, row in enumerate(rows):
        bg = TBL_ROW_ALT1 if r_idx % 2 == 0 else TBL_ROW_ALT2
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(cell_fs)
            p.font.color.rgb = DARK_SLATE
            if c_idx == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
            elif c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = ROYAL_BLUE
    return table_shape

print("Helper modules compiled successfully.")

