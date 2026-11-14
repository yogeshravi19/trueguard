"""
Generate the official Final Review Presentation (.pptx and .pdf) for TRUEGUARD.
Adheres strictly to the faculty review guidelines:
- 15 Widescreen (16:9) slides
- Slide 1: Title, Registration Number, Name, and Guide Name (with 'Dr.' prefix)
- Slide 2: Outline
- Slides 3-15: Introduction, Literature Review (21 papers table), Scope & Problem Statement,
  Research Challenges, Objectives, Proposed Architecture (with HD diagram), Methodology (Three-Tier),
  Results & Discussion (with HD ROC curves), Live Mitigation & Latency (with HD bars),
  Comparison with Existing Works, Conclusion, Limitations & Future Work, References.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

ROOT = Path(r"E:\trueguard")
CAPSTONE = ROOT / "CAPSTONE"
FINAL_DIR = CAPSTONE / "FInal"
FIG_DIR = ROOT / "outputs" / "figures"
SUBMISSION_DIR = ROOT / "FINAL_SUBMISSION"
SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

# Colors
C_DARK_NAVY = RGBColor(11, 27, 61)       # #0B1B3D (VIT / Tech Dark Navy)
C_PRIMARY_BLUE = RGBColor(27, 58, 107)    # #1B3A6B
C_ROYAL_BLUE = RGBColor(36, 44, 95)       # #242C5F (Official VIT Blue)
C_ACCENT_TEAL = RGBColor(14, 116, 144)    # #0E7490
C_ACCENT_EMERALD = RGBColor(4, 120, 87)   # #047857
C_ACCENT_AMBER = RGBColor(217, 119, 6)    # #D97706
C_ACCENT_CORAL = RGBColor(220, 38, 38)    # #DC2626
C_BG_LIGHT = RGBColor(248, 250, 252)      # #F8FAFC
C_CARD_BG = RGBColor(255, 255, 255)       # #FFFFFF
C_CARD_BORDER = RGBColor(226, 232, 240)   # #E2E8F0
C_TEXT_DARK = RGBColor(15, 23, 42)        # #0F172A
C_TEXT_MUTED = RGBColor(71, 85, 105)      # #475569
C_TEXT_LIGHT = RGBColor(255, 255, 255)
C_TABLE_HEADER = RGBColor(15, 23, 42)
C_ROW_ALT = RGBColor(241, 245, 249)

SLIDE_WIDTH = Inches(13.333)
SLIDE_HEIGHT = Inches(7.5)


def create_base_presentation() -> Presentation:
    prs = Presentation()
    prs.slide_width = SLIDE_WIDTH
    prs.slide_height = SLIDE_HEIGHT
    return prs


def add_blank_slide(prs: Presentation):
    blank_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_BG_LIGHT
    bg.line.fill.background()
    return slide


def add_header(slide, title_text: str, category_text: str, slide_num: int):
    # Top banner subtle line
    top_line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.08))
    top_line.fill.solid()
    top_line.fill.fore_color.rgb = C_ROYAL_BLUE
    top_line.line.fill.background()

    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.28), Inches(2.8), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_PRIMARY_BLUE
    pill.line.fill.background()
    tf_pill = pill.text_frame
    tf_pill.word_wrap = True
    p_p = tf_pill.paragraphs[0]
    p_p.text = category_text.upper()
    p_p.font.name = "Calibri"
    p_p.font.size = Pt(9.5)
    p_p.font.bold = True
    p_p.font.color.rgb = C_TEXT_LIGHT
    p_p.alignment = PP_ALIGN.CENTER

    # Main Slide Title
    tb_title = slide.shapes.add_textbox(Inches(0.75), Inches(0.62), Inches(10.5), Inches(0.65))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = title_text
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = C_DARK_NAVY

    # Slide Number & VIT branding right
    tb_num = slide.shapes.add_textbox(Inches(11.2), Inches(0.35), Inches(1.4), Inches(0.45))
    tf_num = tb_num.text_frame
    p_n = tf_num.paragraphs[0]
    p_n.text = f"{slide_num:02d} / 15"
    p_n.font.name = "Calibri"
    p_n.font.size = Pt(11)
    p_n.font.bold = True
    p_n.font.color.rgb = C_TEXT_MUTED
    p_n.alignment = PP_ALIGN.RIGHT


def add_card(slide, left: float, top: float, width: float, height: float, bg_color=C_CARD_BG, border_color=C_CARD_BORDER):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.2)
    return shape


# ---------------------------------------------------------------------------
# Slide 1: Title Slide
# ---------------------------------------------------------------------------
def build_slide_1(prs: Presentation):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = C_DARK_NAVY
    bg.line.fill.background()

    # Accent decorative banner
    acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_WIDTH, Inches(0.12))
    acc.fill.solid()
    acc.fill.fore_color.rgb = C_ACCENT_AMBER
    acc.line.fill.background()

    # Institutional VIT Logo Container
    logo_path = FIG_DIR / "vit_logo_hd.png"
    if logo_path.exists():
        card_logo = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.6), Inches(4.2), Inches(1.15))
        card_logo.fill.solid()
        card_logo.fill.fore_color.rgb = C_CARD_BG
        card_logo.line.fill.background()
        slide.shapes.add_picture(str(logo_path), Inches(0.95), Inches(0.72), width=Inches(3.9))

    # Review Badge Right
    badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(9.2), Inches(0.6), Inches(3.3), Inches(0.5))
    badge.fill.solid()
    badge.fill.fore_color.rgb = C_ACCENT_TEAL
    badge.line.fill.background()
    p_b = badge.text_frame.paragraphs[0]
    p_b.text = "CAPSTONE FINAL REVIEW / VIVA"
    p_b.font.name = "Calibri"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = C_TEXT_LIGHT
    p_b.alignment = PP_ALIGN.CENTER

    # Project Title Box
    tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(1.95), Inches(11.7), Inches(2.2))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_t = tf_title.paragraphs[0]
    p_t.text = "TOWARD TRUSTWORTHY LARGE LANGUAGE MODELS"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = C_TEXT_LIGHT

    p_sub = tf_title.add_paragraph()
    p_sub.text = "A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(16.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = RGBColor(147, 197, 253)  # Soft blue accent
    p_sub.space_before = Pt(8)

    p_framework = tf_title.add_paragraph()
    p_framework.text = "Implemented Solution: TRUEGUARD — Single-Pass White-Box Probing & Closed-Loop Graded Mitigation"
    p_framework.font.name = "Calibri"
    p_framework.font.size = Pt(13)
    p_framework.font.bold = False
    p_framework.font.italic = True
    p_framework.font.color.rgb = RGBColor(226, 232, 240)
    p_framework.space_before = Pt(6)

    # Candidate & Guide Card (2 Columns)
    c1 = add_card(slide, 0.8, 4.4, 5.65, 2.4, bg_color=RGBColor(17, 34, 68), border_color=RGBColor(30, 58, 110))
    tb_c1 = slide.shapes.add_textbox(Inches(1.0), Inches(4.55), Inches(5.25), Inches(2.1))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    p1 = tf_c1.paragraphs[0]
    p1.text = "PRESENTED BY (CANDIDATE)"
    p1.font.name = "Calibri"
    p1.font.size = Pt(11)
    p1.font.bold = True
    p1.font.color.rgb = C_ACCENT_AMBER

    p1_name = tf_c1.add_paragraph()
    p1_name.text = "YOGESH RAVI M"
    p1_name.font.name = "Calibri"
    p1_name.font.size = Pt(18)
    p1_name.font.bold = True
    p1_name.font.color.rgb = C_TEXT_LIGHT
    p1_name.space_before = Pt(4)

    p1_reg = tf_c1.add_paragraph()
    p1_reg.text = "Register Number: 22MIA1052"
    p1_reg.font.name = "Calibri"
    p1_reg.font.size = Pt(13)
    p1_reg.font.bold = True
    p1_reg.font.color.rgb = RGBColor(203, 213, 225)

    p1_deg = tf_c1.add_paragraph()
    p1_deg.text = "M.Tech. (Integrated) CSE with Specialization in Business Analytics\nSchool of Computer Science and Engineering (SCOPE), VIT Chennai"
    p1_deg.font.name = "Calibri"
    p1_deg.font.size = Pt(10.5)
    p1_deg.font.color.rgb = RGBColor(148, 163, 184)
    p1_deg.space_before = Pt(4)

    c2 = add_card(slide, 6.85, 4.4, 5.65, 2.4, bg_color=RGBColor(17, 34, 68), border_color=RGBColor(30, 58, 110))
    tb_c2 = slide.shapes.add_textbox(Inches(7.05), Inches(4.55), Inches(5.25), Inches(2.1))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True
    p2 = tf_c2.paragraphs[0]
    p2.text = "UNDER THE GUIDANCE OF"
    p2.font.name = "Calibri"
    p2.font.size = Pt(11)
    p2.font.bold = True
    p2.font.color.rgb = C_ACCENT_AMBER

    p2_guide = tf_c2.add_paragraph()
    p2_guide.text = "Dr. PRADEEP KUMAR T.S."
    p2_guide.font.name = "Calibri"
    p2_guide.font.size = Pt(18)
    p2_guide.font.bold = True
    p2_guide.font.color.rgb = C_TEXT_LIGHT
    p2_guide.space_before = Pt(4)

    p2_des = tf_c2.add_paragraph()
    p2_des.text = "Professor"
    p2_des.font.name = "Calibri"
    p2_des.font.size = Pt(13)
    p2_des.font.bold = True
    p2_des.font.color.rgb = RGBColor(203, 213, 225)

    p2_dept = tf_c2.add_paragraph()
    p2_dept.text = "Department of Analytics\nSchool of Computer Science and Engineering (SCOPE)\nVellore Institute of Technology, Chennai"
    p2_dept.font.name = "Calibri"
    p2_dept.font.size = Pt(10.5)
    p2_dept.font.color.rgb = RGBColor(148, 163, 184)
    p2_dept.space_before = Pt(4)


# ---------------------------------------------------------------------------
# Slide 2: Outline / Presentation Agenda
# ---------------------------------------------------------------------------
def build_slide_2(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Presentation Roadmap & Agenda", "Structure", 2)

    cards_data = [
        ("01", "Introduction & Motivation", "• LLM Hallucination Dilemma\n• High-stakes operational risks\n• Latency vs. accuracy trade-offs", C_PRIMARY_BLUE),
        ("02", "Literature Review (40 Papers)", "• PRISMA 2020 corpus (2020-2026)\n• 6 Research Pillars synthesis\n• Key contributions & identified gaps", C_ACCENT_TEAL),
        ("03", "Problem Statement & Challenges", "• Scope & target foundation models\n• 4 Core engineering challenges\n• Open-loop actuation disconnect", C_ROYAL_BLUE),
        ("04", "Research Objectives", "• 5 Concrete measurable goals\n• Single-pass multi-sensor probing\n• Leakage-free calibration & XAI", C_ACCENT_EMERALD),
        ("05", "Proposed TRUEGUARD Framework", "• 4 Internal sensors: ISP, AAS, EEM, DST\n• Standardized L2 logistic combiner\n• Three-Tier Closed-Loop Controller", C_PRIMARY_BLUE),
        ("06", "Results & Hardware Latency", "• 0.935 AUROC on 3,196 responses\n• 72% cut in emitted hallucinations\n• Real Tesla T4 GPU latency profile", C_ACCENT_AMBER),
        ("07", "Comparison with State-of-the-Art", "• vs. SelfCheckGPT, Semantic Entropy, ITI\n• 4.65x speedup over consistency\n• Explainable log-odds attributions", C_ACCENT_TEAL),
        ("08", "Conclusion & Future Work", "• Key engineering takeaways\n• Operational limitations & scope\n• Multilingual & Multimodal roadmap", C_DARK_NAVY),
    ]

    # 4 rows x 2 columns grid
    for idx, (num, heading, bullet_txt, accent_color) in enumerate(cards_data):
        row = idx % 4
        col = idx // 4
        left = 0.8 + col * 5.95
        top = 1.45 + row * 1.35
        add_card(slide, left, top, 5.75, 1.25)

        # Number pill left
        num_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left + 0.15), Inches(top + 0.18), Inches(0.65), Inches(0.88))
        num_box.fill.solid()
        num_box.fill.fore_color.rgb = accent_color
        num_box.line.fill.background()
        tf_n = num_box.text_frame
        p_n = tf_n.paragraphs[0]
        p_n.text = num
        p_n.font.name = "Calibri"
        p_n.font.size = Pt(14)
        p_n.font.bold = True
        p_n.font.color.rgb = C_TEXT_LIGHT
        p_n.alignment = PP_ALIGN.CENTER

        # Text box right
        tb = slide.shapes.add_textbox(Inches(left + 0.9), Inches(top + 0.1), Inches(4.7), Inches(1.05))
        tf = tb.text_frame
        tf.word_wrap = True
        p_h = tf.paragraphs[0]
        p_h.text = heading
        p_h.font.name = "Calibri"
        p_h.font.size = Pt(12.5)
        p_h.font.bold = True
        p_h.font.color.rgb = C_DARK_NAVY

        p_b = tf.add_paragraph()
        p_b.text = bullet_txt
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(9.8)
        p_b.font.color.rgb = C_TEXT_MUTED
        p_b.space_before = Pt(2)


# ---------------------------------------------------------------------------
# Slide 3: Introduction & Motivation
# ---------------------------------------------------------------------------
def build_slide_3(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Introduction & Motivation: The LLM Reliability Crisis", "Context & Urgency", 3)

    # 3 High Impact Feature Cards
    # Card 1: What is Hallucination?
    add_card(slide, 0.8, 1.4, 3.75, 5.5)
    tb1 = slide.shapes.add_textbox(Inches(0.95), Inches(1.55), Inches(3.45), Inches(5.15))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1_t = tf1.paragraphs[0]
    p1_t.text = "1. THE HALLUCINATION PHENOMENON"
    p1_t.font.name = "Calibri"
    p1_t.font.size = Pt(13)
    p1_t.font.bold = True
    p1_t.font.color.rgb = C_ACCENT_CORAL

    bullets1 = [
        ("Superficial Fluency:", "Autoregressive LLMs generate highly articulate, confident statements that lack factual reality or contradict source context."),
        ("Intrinsic vs. Extrinsic:", "Intrinsic errors directly contradict provided context; extrinsic errors fabricate unsupported external claims."),
        ("Root Cause:", "Next-token probability optimization maximizes linguistic plausibility rather than epistemological truth or factual grounding."),
        ("Silent Failure:", "Because text remains grammatically flawless, human evaluators and downstream applications cannot detect errors without ground truth verification."),
    ]
    for b_title, b_desc in bullets1:
        p = tf1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {b_title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_MUTED

    # Card 2: Mission-Critical Operational Stakes
    add_card(slide, 4.8, 1.4, 3.75, 5.5)
    tb2 = slide.shapes.add_textbox(Inches(4.95), Inches(1.55), Inches(3.45), Inches(5.15))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p2_t = tf2.paragraphs[0]
    p2_t.text = "2. MISSION-CRITICAL HIGH STAKES"
    p2_t.font.name = "Calibri"
    p2_t.font.size = Pt(13)
    p2_t.font.bold = True
    p2_t.font.color.rgb = C_ACCENT_AMBER

    bullets2 = [
        ("Clinical & Medical AI:", "Fabricated contraindications, incorrect drug dosages, or synthetic clinical citations pose immediate patient safety hazards."),
        ("Legal Jurisprudence:", "Citing fictitious judicial precedents or misquoting statutes leads to severe regulatory liability and ethical collapse."),
        ("Financial Decision Support:", "Hallucinated quarterly revenues or distorted macroeconomic guidance trigger catastrophic investment decisions."),
        ("Autonomous Cyber Systems:", "Unchecked hallucinations in agentic tool-use cause corrupted database operations and security protocol bypasses."),
    ]
    for b_title, b_desc in bullets2:
        p = tf2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {b_title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_MUTED

    # Card 3: The Existing Mitigation Bottleneck
    add_card(slide, 8.8, 1.4, 3.75, 5.5)
    tb3 = slide.shapes.add_textbox(Inches(8.95), Inches(1.55), Inches(3.45), Inches(5.15))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3_t = tf3.paragraphs[0]
    p3_t.text = "3. THE LATENCY-ACCURACY DILEMMA"
    p3_t.font.name = "Calibri"
    p3_t.font.size = Pt(13)
    p3_t.font.bold = True
    p3_t.font.color.rgb = C_PRIMARY_BLUE

    bullets3 = [
        ("Black-Box Multi-Sampling:", "Techniques like SelfCheckGPT and Semantic Entropy sample 5-20 auxiliary generations per prompt, incurring 5x-20x latency penalty!"),
        ("Single-Pass Heuristic Failure:", "Surface token entropy and negative log-likelihood fail when models state deeply memorized misconceptions."),
        ("Open-Loop Disconnect:", "Existing research stops at offline detection; almost no framework feeds risk signals back into runtime mitigation."),
        ("TRUEGUARD Solution:", "Extract internal multi-sensor representations in a single pass (+8.7% latency) and actuate three-tier closed-loop repair."),
    ]
    for b_title, b_desc in bullets3:
        p = tf3.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {b_title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_MUTED


# ---------------------------------------------------------------------------
# Helper: Render Clean Formatted Slide Table
# ---------------------------------------------------------------------------
def add_slide_table(slide, left: float, top: float, width: float, height: float, headers: List[str], rows: List[Tuple], col_widths: List[float], font_size: float = 8.5):
    rows_cnt = len(rows) + 1
    cols_cnt = len(headers)
    table_shape = slide.shapes.add_table(rows_cnt, cols_cnt, Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table

    for i, w in enumerate(col_widths):
        table.columns[i].width = Inches(w)

    # Style Header Row
    for col_idx, h_text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_TABLE_HEADER
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        tf.margin_right = Inches(0.08)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)
        p = tf.paragraphs[0]
        p.text = h_text
        p.font.name = "Calibri"
        p.font.size = Pt(font_size + 1.0)
        p.font.bold = True
        p.font.color.rgb = C_TEXT_LIGHT
        p.alignment = PP_ALIGN.LEFT if col_idx > 0 else PP_ALIGN.CENTER

    # Style Data Rows
    for row_idx, row_data in enumerate(rows):
        bg_col = C_ROW_ALT if row_idx % 2 == 1 else C_CARD_BG
        for col_idx, cell_value in enumerate(row_data):
            cell = table.cell(row_idx + 1, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_right = Inches(0.08)
            tf.margin_top = Inches(0.03)
            tf.margin_bottom = Inches(0.03)
            p = tf.paragraphs[0]
            p.text = str(cell_value)
            p.font.name = "Calibri"
            p.font.size = Pt(font_size)
            p.font.color.rgb = C_TEXT_DARK
            p.alignment = PP_ALIGN.CENTER if col_idx == 0 else PP_ALIGN.LEFT


# ---------------------------------------------------------------------------
# Slide 4: Literature Review (Part 1: Probing & Uncertainty - 10 Papers)
# ---------------------------------------------------------------------------
def build_slide_4(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Literature Review (Part 1): Internal Probing & Uncertainty Quantification", "PRISMA 2020 Review", 4)

    headers = ["S.No.", "Author(s), Year", "Method / Approach", "Key Contribution", "Gap Identified"]
    col_widths = [0.65, 1.85, 2.75, 3.45, 3.05]

    rows = [
        ("1", "Azaria & Mitchell (2023)", "SAPLMA MLP Classifier", "Trained probes on hidden states; demonstrated truth is linearly separable.", "Evaluated only on simple synthetic binary statements; no multi-task evaluation."),
        ("2", "Li et al. (2024)", "Inference-Time Intervention (ITI)", "Shifted attention activations along truth directions during decoding.", "Requires manually chosen steering hyperparameter; degrades linguistic fluency."),
        ("3", "Su et al. (2024)", "Mind's Mirror Unsupervised Probing", "Extracted unsupervised difference vectors across layer activations.", "Vulnerable to prompt phrasing shifts; lacks closed-loop mitigation."),
        ("4", "Zhang et al. (2024)", "Prompt-Guided Internal States", "Tracked layer representation drift conditioned on prompt templates.", "High computational overhead per prompt; no confidence probability output."),
        ("5", "Zhang et al. (2025)", "Deep Inter-Layer Activation Tracking", "Characterized non-linear truth manifolds across deeper residual layers.", "Heavy multi-layer MLP probe training required; not single-pass lightweight."),
        ("6", "Chen et al. (2025)", "Dynamic Probe Pruning", "Pruned redundant intermediate layers to accelerate probing inference.", "Pruning thresholds sensitive to domain; drops accuracy on complex QA."),
        ("7", "Manakul et al. (2023)", "SelfCheckGPT Multi-Sampling", "Sampled 5-20 stochastic completions; computed n-gram / semantic consistency.", "Multiplies generation latency by 5x-20x; impractical for real-time systems."),
        ("8", "Han et al. (2024)", "Semantic Entropy via Clustering", "Grouped sampled completions by entailment to compute semantic entropy.", "Requires expensive NLI cross-encoder; unable to detect memorized falsehoods."),
        ("9", "Ma et al. (2025)", "Semantic Energy Probing", "Combined free logit energy with semantic clustering for uncertainty bounds.", "High false alarm rate under skewed token frequency distributions."),
        ("10", "Kang et al. (2025)", "Multi-Sample Uncertainty Bounds", "Derived PAC-Bayesian empirical bounds on hallucination probability.", "Demands high sample size (N >= 15); offline post-hoc evaluation only."),
    ]

    add_slide_table(slide, 0.8, 1.35, 11.75, 5.65, headers, rows, col_widths, font_size=8.2)


# ---------------------------------------------------------------------------
# Slide 5: Literature Review (Part 2: Attention, Mitigation & Benchmarks - 11 Papers)
# ---------------------------------------------------------------------------
def build_slide_5(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Literature Review (Part 2): Attention, Mitigation, RAG & Benchmarks", "PRISMA 2020 Review", 5)

    headers = ["S.No.", "Author(s), Year", "Method / Approach", "Key Contribution", "Gap Identified"]
    col_widths = [0.65, 1.85, 2.75, 3.45, 3.05]

    rows = [
        ("11", "Hajji et al. (2025)", "The Map of Misbelief (Attention)", "Traced hallucination to attention head dispersion away from prompt tokens.", "Looked at attention in isolation without hidden state or logit fusion."),
        ("12", "Vazhentsev et al. (2025)", "Uncertainty-Aware Attention Heads", "Ranked attention heads by factual predictive entropy across layers.", "Handcrafted head subset does not generalize across distinct model scales."),
        ("13", "Lin et al. (2022)", "TruthfulQA Benchmark", "Curated 817 questions exposing human misconceptions and false superstitions.", "Benchmark dataset only; does not provide an integrated mitigation system."),
        ("14", "Li et al. (2023)", "HaluEval Benchmark Suite", "Generated 35k paired positive/negative samples across QA, Dial & Summ.", "Contains synthetic LLM-generated distractor errors with subtle artifacts."),
        ("15", "Min et al. (2023)", "FActScore Atomic Evaluation", "Decomposed biographical generations into atomic factual propositions.", "Requires auxiliary LLM or search API calls per atomic claim; slow."),
        ("16", "Lewis et al. (2020)", "Retrieval-Augmented Generation (RAG)", "Retrieved dense Wikipedia passages to ground decoder generations.", "Blindly retrieves for every prompt, introducing retrieval latency and noise."),
        ("17", "Asai et al. (2024)", "Self-RAG Reflection Tokens", "Trained model to emit [Retrieve] and [IsRel] special reflection tokens.", "Requires expensive pre-training and fine-tuning; inaccessible for frozen models."),
        ("18", "Dhuliawala et al. (2024)", "Chain-of-Verification (CoVe)", "Generated verification questions, answered them, and revised initial text.", "Quadruples execution time (4 separate prompting steps); high latency."),
        ("19", "Gao et al. (2023)", "RARR Automated Editor", "Employed external search query generation and token-level editor.", "Complex multi-component pipeline; breaks down on conversational prompts."),
        ("20", "Sharma et al. (2024)", "Human Trust & Contrastive XAI", "Formulated 4D XAI taxonomy to calibrate operator trust in model outputs.", "Theoretical evaluation without automated real-time attribution scoring."),
        ("21", "Huang et al. (2024)", "TrustLLM Trustworthiness Matrix", "Comprehensive taxonomy evaluating truthfulness, safety and fairness.", "High-level survey; lacks unified closed-loop feedback control architecture."),
    ]

    add_slide_table(slide, 0.8, 1.35, 11.75, 5.65, headers, rows, col_widths, font_size=8.0)


# ---------------------------------------------------------------------------
# Slide 6: Scope & Problem Statement
# ---------------------------------------------------------------------------
def build_slide_6(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Problem Statement & Project Scope", "Foundation", 6)

    # Left: Formal Problem Statement Card
    add_card(slide, 0.8, 1.4, 5.75, 5.5)
    tb_p = slide.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.35), Inches(5.15))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p_pt = tf_p.paragraphs[0]
    p_pt.text = "FORMAL PROBLEM STATEMENT"
    p_pt.font.name = "Calibri"
    p_pt.font.size = Pt(13)
    p_pt.font.bold = True
    p_pt.font.color.rgb = C_ACCENT_CORAL

    p_pdesc = tf_p.add_paragraph()
    p_pdesc.text = (
        "Modern autoregressive Large Language Models operating in high-stakes domains lack "
        "calibrated self-awareness of factual veracity during generation. Current mitigation strategies "
        "either suffer from crippling inference latency (5x-20x overhead in multi-sample consistency) or "
        "rely on surface scalar heuristics that invert polarity under answer-length variations.\n\n"
        "Crucially, there is an architectural void: no existing system connects single-pass, multi-sensor "
        "white-box internal probing (hidden manifolds, causal attention entropy, and logit dynamics) to a "
        "calibrated, graded closed-loop feedback controller that provides real-time repair and per-sensor explainability."
    )
    p_pdesc.font.name = "Calibri"
    p_pdesc.font.size = Pt(11)
    p_pdesc.font.color.rgb = C_TEXT_MUTED
    p_pdesc.space_before = Pt(8)

    p_sub = tf_p.add_paragraph()
    p_sub.text = "CORE RESEARCH QUESTIONS:"
    p_sub.font.name = "Calibri"
    p_sub.font.size = Pt(11.5)
    p_sub.font.bold = True
    p_sub.font.color.rgb = C_DARK_NAVY
    p_sub.space_before = Pt(14)

    rqs = [
        "RQ1: Can truthfulness be reliably detected in a single forward pass without sampling auxiliary completions?",
        "RQ2: Do internal hidden activations, causal attention entropy, and logit geometry provide complementary factual signals?",
        "RQ3: How can a closed-loop controller dynamically route high-risk generations to appropriate mitigation tiers?",
    ]
    for rq in rqs:
        p = tf_p.add_paragraph()
        p.text = f"• {rq}"
        p.font.name = "Calibri"
        p.font.size = Pt(10)
        p.font.color.rgb = C_PRIMARY_BLUE
        p.space_before = Pt(4)

    # Right: Scope Card
    add_card(slide, 6.8, 1.4, 5.75, 5.5)
    tb_s = slide.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.35), Inches(5.15))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p_st = tf_s.paragraphs[0]
    p_st.text = "PROJECT BOUNDARIES & SCOPE"
    p_st.font.name = "Calibri"
    p_st.font.size = Pt(13)
    p_st.font.bold = True
    p_st.font.color.rgb = C_ACCENT_TEAL

    scopes = [
        ("Target Foundation Models:", "Autoregressive decoder Transformers: TinyLlama-1.1B-Chat-v1.0 (production testbed) and GPT-2 (124M) for cross-architecture verification."),
        ("Multi-Task In-Distribution Benchmarks:", "3,196 paired responses spanning 4 standard benchmark tasks: HaluEval-QA, HaluEval-Dialogue, HaluEval-Summarization, and TruthfulQA."),
        ("Live Open-Domain Closed-Loop Testing:", "Open-domain TriviaQA live generations (n_cal=150, n_test=150) under real-world Wikipedia retrieval grounding."),
        ("Hardware Constraints:", "Designed for real deployment on a single NVIDIA Tesla T4 GPU (16GB VRAM) and local standard CPU (32GB RAM)."),
        ("Out of Scope:", "Closed-weights proprietary APIs (GPT-4/Claude 3.5) where internal residual activations cannot be accessed; multi-modal image generation."),
    ]
    for title, desc in scopes:
        p = tf_s.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = f"• {title} "
        r1.font.bold = True
        r1.font.size = Pt(11)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_TEXT_MUTED


# ---------------------------------------------------------------------------
# Slide 7: Research Challenges
# ---------------------------------------------------------------------------
def build_slide_7(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Research Challenges: The Four System Engineering Hurdles", "Challenges", 7)

    challenges = [
        (
            "CHALLENGE 1: THE SEVERE LATENCY–ACCURACY TRADE-OFF",
            "Multi-Sample Sampling Overhead",
            "State-of-the-art consistency detectors (SelfCheckGPT, Semantic Entropy) require generating 5 to 20 auxiliary completions per prompt.\n\n"
            "This multiplies token decoding latency by 500% to 2,000%, rendering them completely unviable for interactive chatbots, clinical assistants, or latency-critical APIs (< 100 ms).",
            C_ACCENT_CORAL,
        ),
        (
            "CHALLENGE 2: SURFACE HEURISTIC POLARITY INVERSION",
            "Fragility of Token Entropy & Log-Likelihood",
            "Single-pass scalar heuristics (token entropy, negative log-likelihood, logit energy) fail when models recite deeply memorized falsehoods.\n\n"
            "Furthermore, our empirical tests show these baselines suffer from polarity inversion—shorter answers artificially exhibit lower entropy regardless of truthfulness.",
            C_ACCENT_AMBER,
        ),
        (
            "CHALLENGE 3: SILOED SENSOR CAPABILITIES",
            "Lack of Unified Multi-Sensor Internal Fusion",
            "Prior literature explores internal states (Pillar 1), attention entropy (Pillar 3), or logit uncertainty (Pillar 2) in isolated research silos.\n\n"
            "No single internal signal is sufficient across all tasks: hidden states capture semantic truth, while attention entropy detects source grounding collapse.",
            C_ACCENT_TEAL,
        ),
        (
            "CHALLENGE 4: THE OPEN-LOOP ACTUATION DISCONNECT",
            "Absence of Real-Time Graded Closed-Loop Control",
            "Almost 90% of published hallucination papers focus strictly on post-hoc offline scoring (Pillar 4).\n\n"
            "There is no dynamic closed-loop mechanism that maps risk probability r(x,y) to proportionate runtime interventions: safe pass-through, retry, or RAG grounding.",
            C_PRIMARY_BLUE,
        ),
    ]

    # 2x2 grid
    for idx, (title, sub, body, color) in enumerate(challenges):
        r = idx // 2
        c = idx % 2
        left = 0.8 + c * 5.95
        top = 1.45 + r * 2.75
        add_card(slide, left, top, 5.75, 2.55)

        # Header bar inside card
        hbar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(5.75), Inches(0.42))
        hbar.fill.solid()
        hbar.fill.fore_color.rgb = color
        hbar.line.fill.background()
        tf_h = hbar.text_frame
        p_h = tf_h.paragraphs[0]
        p_h.text = title
        p_h.font.name = "Calibri"
        p_h.font.size = Pt(10.5)
        p_h.font.bold = True
        p_h.font.color.rgb = C_TEXT_LIGHT

        tb_b = slide.shapes.add_textbox(Inches(left + 0.15), Inches(top + 0.45), Inches(5.45), Inches(2.0))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        p_s = tf_b.paragraphs[0]
        p_s.text = sub
        p_s.font.name = "Calibri"
        p_s.font.size = Pt(11)
        p_s.font.bold = True
        p_s.font.color.rgb = C_DARK_NAVY

        p_desc = tf_b.add_paragraph()
        p_desc.text = body
        p_desc.font.name = "Calibri"
        p_desc.font.size = Pt(9.8)
        p_desc.font.color.rgb = C_TEXT_MUTED
        p_desc.space_before = Pt(3)


# ---------------------------------------------------------------------------
# Slide 8: Research Objectives
# ---------------------------------------------------------------------------
def build_slide_8(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Research Objectives & Contributions of TRUEGUARD", "Objectives", 8)

    objectives = [
        (
            "Objective 1: Single-Pass Multi-Sensor Extraction",
            "Extract four non-invasive internal signals—(1) Multi-layer residual states, (2) Causal attention entropy, (3) Hybrid Shannon/Renyi-2 entropy, and (4) Semantic hidden drift—during a single forward pass without secondary generation.",
            "Outcome: Realized via hooks into frozen Transformer; zero retraining of model weights.",
            C_PRIMARY_BLUE,
        ),
        (
            "Objective 2: Leakage-Free Inner Grouped OOF Calibration",
            "Design an inner grouped 5-fold cross-validation stacking pipeline that trains intermediate linear probes without prompt/question-level memory leakage across folds.",
            "Outcome: Eliminates artificial inflated performance common in naive train/test splits.",
            C_ACCENT_TEAL,
        ),
        (
            "Objective 3: Calibrated Fusion & Per-Sensor Explainability",
            "Train an L2-regularized logistic combiner mapping the 4-sensor vector into a calibrated risk score r(x,y) in [0, 1] with exact signed log-odds attribution c_k = w_k * z_k.",
            "Outcome: Delivers full transparency into which specific sensor flagged the hallucination.",
            C_ROYAL_BLUE,
        ),
        (
            "Objective 4: Closed-Loop Three-Tier Graded Actuation",
            "Implement a feedback controller with two calibrated thresholds (tau_warning = 0.611, tau_fault = 0.898) actuating SAFE pass-through, Tier 1 re-sampling, Tier 2 RAG grounding, and Tier 3 abstention.",
            "Outcome: First closed-loop control system dynamically intervening based on risk.",
            C_ACCENT_EMERALD,
        ),
        (
            "Objective 5: Real-World Hardware Benchmarking & Profiling",
            "Evaluate across 3,196 responses on four diverse benchmarks and profile per-token inference latency on NVIDIA Tesla T4 GPU and standard consumer CPU.",
            "Outcome: Macro AUROC of 0.935 (+30.6 gain) with only +2.91 ms/token overhead (+8.7%).",
            C_ACCENT_AMBER,
        ),
    ]

    for idx, (title, desc, outcome, col) in enumerate(objectives):
        top = 1.35 + idx * 1.15
        add_card(slide, 0.8, top, 11.75, 1.05)

        # Left indicator tag
        tag = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.9), Inches(top + 0.12), Inches(0.55), Inches(0.81))
        tag.fill.solid()
        tag.fill.fore_color.rgb = col
        tag.line.fill.background()
        p_t = tag.text_frame.paragraphs[0]
        p_t.text = f"O{idx+1}"
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_LIGHT
        p_t.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(1.6), Inches(top + 0.08), Inches(10.8), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p_head = tf.paragraphs[0]
        p_head.text = title
        p_head.font.name = "Calibri"
        p_head.font.size = Pt(12)
        p_head.font.bold = True
        p_head.font.color.rgb = C_DARK_NAVY

        p_desc = tf.add_paragraph()
        r1 = p_desc.add_run()
        r1.text = desc + " "
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_TEXT_MUTED
        r2 = p_desc.add_run()
        r2.text = f"[{outcome}]"
        r2.font.size = Pt(9.5)
        r2.font.bold = True
        r2.font.color.rgb = col
        p_desc.space_before = Pt(1)


# ---------------------------------------------------------------------------
# Slide 9: Proposed Architecture: TRUEGUARD Framework
# ---------------------------------------------------------------------------
def build_slide_9(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Proposed Architecture: The TRUEGUARD Multi-Sensor Suite", "System Architecture", 9)

    # Left: Embed High-Definition Figure 7.1
    fig_7_1 = FIG_DIR / "fig_hd_7_1.png"
    if fig_7_1.exists():
        add_card(slide, 0.8, 1.35, 6.2, 5.55)
        slide.shapes.add_picture(str(fig_7_1), Inches(0.9), Inches(1.45), width=Inches(6.0))
        # Caption below figure
        tb_cap = slide.shapes.add_textbox(Inches(0.9), Inches(6.55), Inches(6.0), Inches(0.35))
        p_cap = tb_cap.text_frame.paragraphs[0]
        p_cap.text = "Figure 1: TRUEGUARD Closed-Loop Architecture & Sensor Fusion Pipeline"
        p_cap.font.name = "Calibri"
        p_cap.font.size = Pt(9.5)
        p_cap.font.bold = True
        p_cap.font.color.rgb = C_TEXT_MUTED
        p_cap.alignment = PP_ALIGN.CENTER

    # Right: Four Sensor Mathematical Formulations Card
    add_card(slide, 7.2, 1.35, 5.35, 5.55)
    tb_s = slide.shapes.add_textbox(Inches(7.35), Inches(1.45), Inches(5.05), Inches(5.35))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p_t = tf_s.paragraphs[0]
    p_t.text = "FOUR COMPLEMENTARY SENSORS"
    p_t.font.name = "Calibri"
    p_t.font.size = Pt(13)
    p_t.font.bold = True
    p_t.font.color.rgb = C_PRIMARY_BLUE

    sensors = [
        ("Sensor 1: Internal State Probe (ISP)", "Multi-layer L2-logistic probes at depths {0.45, 0.60, 0.75, 0.90}L trained with 5-fold inner OOF stacking to prevent test leakage.", "Detects truthfulness encoded in hidden manifolds."),
        ("Sensor 2: Attention Anomaly Score (AAS)", "Final-quartile normalized Shannon entropy of causal attention matrices H_norm(A^(l,h)) across upper-layer attention heads.", "Detects collapse of source context grounding."),
        ("Sensor 3: Energy-Entropy Monitor (EEM)", "Scale-invariant combination: 0.6 * normalized Shannon token entropy + 0.4 * quadratic Renyi-2 logit entropy.", "Captures predictive distribution dispersion."),
        ("Sensor 4: Directional Semantic Trajectory (DST)", "Hidden-state cosine drift cos(h_t, h_{t-1}) tracking consecutive-token representational drift.", "Captures cumulative hallucination divergence."),
    ]

    for title, math_desc, role in sensors:
        p = tf_s.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"• {title}\n"
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_DARK_NAVY

        r2 = p.add_run()
        r2.text = f"  Mechanism: {math_desc}\n"
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED

        r3 = p.add_run()
        r3.text = f"  Role: {role}"
        r3.font.size = Pt(9.5)
        r3.font.bold = True
        r3.font.color.rgb = C_ACCENT_TEAL

    p_fus = tf_s.add_paragraph()
    p_fus.text = "CALIBRATED LOGISTIC COMBINER:\nz = w0 + sum(wk * zk)  ==>  r(x, y) = 1 / (1 + exp(-z))\nAttribution: c_k = w_k * z_k (Exact per-sensor log-odds)"
    p_fus.font.name = "Consolas"
    p_fus.font.size = Pt(9.2)
    p_fus.font.bold = True
    p_fus.font.color.rgb = C_ROYAL_BLUE
    p_fus.space_before = Pt(8)


# ---------------------------------------------------------------------------
# Slide 10: Proposed Methodology: Closed-Loop Three-Tier Control
# ---------------------------------------------------------------------------
def build_slide_10(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Proposed Methodology: Closed-Loop Graded Three-Tier Control", "Methodology & Actuation", 10)

    # 4 Tiers Horizontally Formatted Cards
    tiers_data = [
        (
            "ZONE 1: SAFE",
            "r(x, y) < 0.611",
            "PASS-THROUGH",
            "• Direct delivery to user\n• 0 ms mitigation overhead\n• 100% latency preservation\n• Verified truthful responses\n• Zero downstream friction",
            C_ACCENT_EMERALD,
        ),
        (
            "ZONE 2: TIER 1",
            "0.611 <= r < 0.898",
            "ANNEALED RE-SAMPLING",
            "• Moderate hallucination risk\n• Re-sample with annealed temp\n  (T = 0.35, min-p = 0.05)\n• Fast internal retry pass\n• Avoids external network calls\n• Resolves stochastic errors",
            C_ACCENT_AMBER,
        ),
        (
            "ZONE 3: TIER 2",
            "r >= 0.898 (Retrievable)",
            "WIKIPEDIA RAG GROUNDING",
            "• Severe hallucination fault\n• Query reformulation for RAG\n• Dense Wikipedia retrieval\n• Injects authoritative facts\n• Active factual repair",
            C_ACCENT_TEAL,
        ),
        (
            "ZONE 4: TIER 3",
            "r >= 0.898 (Unresolvable)",
            "SELECTIVE ABSTENTION",
            "• Irreparable hallucination\n• Calibrated safety refusal\n• 'Insufficient evidence'\n• Eliminates toxic falsehoods\n• Guaranteed safe fallback",
            C_ACCENT_CORAL,
        ),
    ]

    card_width = 2.75
    gap = 0.24
    for idx, (zone_name, cond, action, bullets, color) in enumerate(tiers_data):
        left = 0.8 + idx * (card_width + gap)
        add_card(slide, left, 1.4, card_width, 4.3)

        # Header tag
        tag = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(1.4), Inches(card_width), Inches(0.45))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.fill.background()
        p_t = tag.text_frame.paragraphs[0]
        p_t.text = zone_name
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(11)
        p_t.font.bold = True
        p_t.font.color.rgb = C_TEXT_LIGHT
        p_t.alignment = PP_ALIGN.CENTER

        tb = slide.shapes.add_textbox(Inches(left + 0.1), Inches(1.9), Inches(card_width - 0.2), Inches(3.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p_cond = tf.paragraphs[0]
        p_cond.text = cond
        p_cond.font.name = "Consolas"
        p_cond.font.size = Pt(10)
        p_cond.font.bold = True
        p_cond.font.color.rgb = color
        p_cond.alignment = PP_ALIGN.CENTER

        p_act = tf.add_paragraph()
        p_act.text = action
        p_act.font.name = "Calibri"
        p_act.font.size = Pt(11.5)
        p_act.font.bold = True
        p_act.font.color.rgb = C_DARK_NAVY
        p_act.alignment = PP_ALIGN.CENTER
        p_act.space_before = Pt(4)

        p_b = tf.add_paragraph()
        p_b.text = bullets
        p_b.font.name = "Calibri"
        p_b.font.size = Pt(9.5)
        p_b.font.color.rgb = C_TEXT_MUTED
        p_b.space_before = Pt(8)

    # Bottom Closed-Loop Guarantee Card
    add_card(slide, 0.8, 5.85, 11.75, 1.1, bg_color=C_PRIMARY_BLUE, border_color=C_PRIMARY_BLUE)
    tb_bot = slide.shapes.add_textbox(Inches(0.95), Inches(5.92), Inches(11.45), Inches(0.95))
    tf_bot = tb_bot.text_frame
    tf_bot.word_wrap = True
    p_b1 = tf_bot.paragraphs[0]
    p_b1.text = "CLOSED-LOOP FEEDBACK ADVANTAGE OVER OPEN-LOOP DETECTORS"
    p_b1.font.name = "Calibri"
    p_b1.font.size = Pt(11)
    p_b1.font.bold = True
    p_b1.font.color.rgb = C_ACCENT_AMBER

    p_b2 = tf_bot.add_paragraph()
    p_b2.text = (
        "Unlike prior methods that merely output a passive scalar score or post-hoc flag, TRUEGUARD dynamically closes the control loop. "
        "SAFE generations incur ZERO overhead (+0 ms), Tier 1 attempts fast local repair, Tier 2 grounds high-risk queries in external evidence, "
        "and Tier 3 cleanly abstains—achieving maximum factual safety with minimal system overhead."
    )
    p_b2.font.name = "Calibri"
    p_b2.font.size = Pt(9.8)
    p_b2.font.color.rgb = C_TEXT_LIGHT
    p_b2.space_before = Pt(2)


# ---------------------------------------------------------------------------
# Slide 11: Experimental Results & Benchmarks
# ---------------------------------------------------------------------------
def build_slide_11(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Experimental Results & Multi-Benchmark Detection Performance", "Empirical Evaluation", 11)

    # Left: Embed High-Definition Figure 7.2 (ROC Curves)
    fig_7_2 = FIG_DIR / "fig_hd_7_2.png"
    if fig_7_2.exists():
        add_card(slide, 0.8, 1.35, 5.5, 5.55)
        slide.shapes.add_picture(str(fig_7_2), Inches(0.9), Inches(1.45), width=Inches(5.3))
        tb_c = slide.shapes.add_textbox(Inches(0.9), Inches(6.55), Inches(5.3), Inches(0.35))
        p_c = tb_c.text_frame.paragraphs[0]
        p_c.text = "Figure 2: Multi-Benchmark ROC Curves (TinyLlama-1.1B on Tesla T4 GPU)"
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(9.2)
        p_c.font.bold = True
        p_c.font.color.rgb = C_TEXT_MUTED
        p_c.alignment = PP_ALIGN.CENTER

    # Right: Results Table & Highlights Card
    add_card(slide, 6.5, 1.35, 6.05, 5.55)
    tb_r = slide.shapes.add_textbox(Inches(6.65), Inches(1.45), Inches(5.75), Inches(5.35))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_rt = tf_r.paragraphs[0]
    p_rt.text = "MULTI-TASK BENCHMARK VERIFICATION (N = 3,196)"
    p_rt.font.name = "Calibri"
    p_rt.font.size = Pt(12)
    p_rt.font.bold = True
    p_rt.font.color.rgb = C_DARK_NAVY

    # Mini Table
    headers = ["Benchmark Dataset", "Sample N", "AUROC", "AUPRC", "Macro F1"]
    col_w = [1.9, 0.8, 0.95, 0.95, 0.95]
    rows = [
        ("HaluEval-Summarization", "1,000", "0.986", "0.981", "0.942"),
        ("HaluEval-QA", "1,000", "0.975", "0.968", "0.923"),
        ("HaluEval-Dialogue", "1,000", "0.903", "0.892", "0.841"),
        ("TruthfulQA (Adversarial)", "196", "0.876", "0.864", "0.822"),
        ("MACRO AVERAGE", "3,196", "0.935", "0.926", "0.882"),
    ]
    # Add table directly into right container
    add_slide_table(slide, 6.65, 1.85, 5.75, 2.1, headers, rows, col_w, font_size=8.5)

    # Key Takeaways below table
    tb_t = slide.shapes.add_textbox(Inches(6.65), Inches(4.15), Inches(5.75), Inches(2.65))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    p_th = tf_t.paragraphs[0]
    p_th.text = "KEY EMPIRICAL FINDINGS:"
    p_th.font.name = "Calibri"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = C_ACCENT_TEAL

    points = [
        ("+30.6 AUROC Point Gain:", "Outperforms standard single-pass token entropy baseline (0.629 AUROC) by +30.6 points across all four benchmarks."),
        ("Near-Perfect Summarization:", "Achieves 0.986 AUROC on HaluEval-Summarization, where attention entropy detects prompt source grounding detachment."),
        ("Cross-Architecture Robustness:", "Verified on GPT-2 (124M) with 0.908 macro AUROC, proving framework universality across different Transformer scales."),
        ("Calibrated Confidence (ECE = 0.031):", "Expected Calibration Error of 0.031 confirms predicted risk matches true empirical error frequency."),
    ]
    for h, b in points:
        p = tf_t.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED


# ---------------------------------------------------------------------------
# Slide 12: Live Closed-Loop Mitigation & Hardware Latency Profile
# ---------------------------------------------------------------------------
def build_slide_12(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Live Closed-Loop Mitigation & Hardware Latency Profiling", "Hardware & Live Trials", 12)

    # Left: Embed High-Definition Figure 8.3 (Hardware Latency Profiles)
    fig_8_3 = FIG_DIR / "fig_hd_8_3.png"
    if fig_8_3.exists():
        add_card(slide, 0.8, 1.35, 5.5, 5.55)
        slide.shapes.add_picture(str(fig_8_3), Inches(0.9), Inches(1.45), width=Inches(5.3))
        tb_c = slide.shapes.add_textbox(Inches(0.9), Inches(6.55), Inches(5.3), Inches(0.35))
        p_c = tb_c.text_frame.paragraphs[0]
        p_c.text = "Figure 3: Real Hardware Per-Token Latency on Tesla T4 GPU & CPU"
        p_c.font.name = "Calibri"
        p_c.font.size = Pt(9.2)
        p_c.font.bold = True
        p_c.font.color.rgb = C_TEXT_MUTED
        p_c.alignment = PP_ALIGN.CENTER

    # Right: Live TriviaQA Results Card
    add_card(slide, 6.5, 1.35, 6.05, 5.55)
    tb_l = slide.shapes.add_textbox(Inches(6.65), Inches(1.45), Inches(5.75), Inches(5.35))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    p_lt = tf_l.paragraphs[0]
    p_lt.text = "LIVE CLOSED-LOOP REPAIR ON TRIVIAQA (N = 150)"
    p_lt.font.name = "Calibri"
    p_lt.font.size = Pt(12)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_DARK_NAVY

    # Metric comparison box
    m_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.65), Inches(1.85), Inches(5.75), Inches(1.75))
    m_box.fill.solid()
    m_box.fill.fore_color.rgb = C_ROW_ALT
    m_box.line.color.rgb = C_CARD_BORDER
    tf_m = m_box.text_frame
    tf_m.word_wrap = True

    metrics = [
        ("System-Wide Emitted Hallucinations:", "62.0%  -->  17.3%  (-72.0% Relative Reduction)", C_ACCENT_EMERALD),
        ("Factual Accuracy on Answered Queries:", "38.0%  -->  60.0%  (+22.0% Absolute Boost)", C_ACCENT_TEAL),
        ("Active Repair Success Rate (Tier 1 & 2):", "41.7% of triggered faults fully corrected", C_PRIMARY_BLUE),
        ("Selective Risk-Coverage Metric:", "AURC = 0.412 (Area Under Risk-Coverage Curve)", C_ACCENT_AMBER),
    ]
    for idx, (label, val, col) in enumerate(metrics):
        p = tf_m.paragraphs[0] if idx == 0 else tf_m.add_paragraph()
        p.space_before = Pt(3) if idx > 0 else Pt(0)
        r1 = p.add_run()
        r1.text = f"{label} "
        r1.font.bold = True
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = val
        r2.font.bold = True
        r2.font.size = Pt(10)
        r2.font.color.rgb = col

    # Latency Breakdown Table below
    tb_lat = slide.shapes.add_textbox(Inches(6.65), Inches(3.75), Inches(5.75), Inches(3.0))
    tf_lat = tb_lat.text_frame
    tf_lat.word_wrap = True

    p_lh = tf_lat.paragraphs[0]
    p_lh.text = "HARDWARE LATENCY COMPARISON (NVIDIA TESLA T4):"
    p_lh.font.name = "Calibri"
    p_lh.font.size = Pt(11)
    p_lh.font.bold = True
    p_lh.font.color.rgb = C_PRIMARY_BLUE

    l_items = [
        ("Base Transformer Decoding:", "33.42 ms / token (Native frozen autoregressive pass)"),
        ("TRUEGUARD Multi-Sensor Extraction:", "36.33 ms / token (+2.91 ms overhead, ONLY +8.7%)"),
        ("5-Sample Consistency Baseline:", "169.10 ms / token (+135.68 ms overhead, +405%)"),
        ("Real Hardware Speedup:", "TRUEGUARD is 4.65x FASTER than 5-sample SelfCheckGPT"),
    ]
    for h, b in l_items:
        p = tf_lat.add_paragraph()
        p.space_before = Pt(4)
        r1 = p.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED


# ---------------------------------------------------------------------------
# Slide 13: Comparison with Existing Works
# ---------------------------------------------------------------------------
def build_slide_13(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Comparative Analysis with State-of-the-Art Mitigation Methods", "Benchmarking", 13)

    headers = [
        "Architectural Dimension",
        "Token Entropy (Heuristic)",
        "SelfCheckGPT (Consistency)",
        "ITI (Activation Steering)",
        "Self-RAG (Reflection)",
        "TRUEGUARD (Proposed)",
    ]
    col_widths = [2.25, 1.85, 1.95, 1.90, 1.90, 1.90]

    rows = [
        ("Decoding Passes", "Single-pass", "Multi-pass (5 to 20x)", "Single-pass", "Single / Multi", "Single-pass (1x)"),
        ("Inspection Level", "Surface Logits", "Generated Text", "Hidden Residuals", "Output Tokens", "Residuals + Attention + Logits"),
        ("Model Weights", "Frozen", "Frozen", "Modified (Intervention)", "Retrained / Tuned", "100% Frozen Weights"),
        ("Latency Overhead", "~0% (Scalar)", "+400% to +1,900%", "+5% to +8%", "+50% to +150%", "+8.7% (+2.91 ms/token)"),
        ("Speedup vs. 5-Sample", "5.06x", "1.00x (Baseline)", "4.82x", "2.10x", "4.65x FASTER"),
        ("Detection AUROC", "0.629 (Polarity Inverts)", "0.884", "0.841", "0.872", "0.935 (State-of-the-Art)"),
        ("Explainability", "None (Black Box)", "Sentence Alignment", "Fixed Vector Steering", "Reflection Tokens", "Exact Signed Log-Odds (c_k)"),
        ("Closed-Loop Control", "No (Passive)", "No (Detection Only)", "Static Intervention", "Heuristic Prompting", "Three-Tier Feedback Actuator"),
    ]

    add_slide_table(slide, 0.8, 1.35, 11.75, 4.4, headers, rows, col_widths, font_size=8.3)

    # Highlight box at bottom
    add_card(slide, 0.8, 5.95, 11.75, 1.05, bg_color=C_ROW_ALT)
    tb_b = slide.shapes.add_textbox(Inches(0.95), Inches(6.0), Inches(11.45), Inches(0.9))
    tf_b = tb_b.text_frame
    tf_b.word_wrap = True
    p1 = tf_b.paragraphs[0]
    p1.text = "SUMMARY OF COMPETITIVE ADVANTAGES"
    p1.font.name = "Calibri"
    p1.font.size = Pt(10.5)
    p1.font.bold = True
    p1.font.color.rgb = C_PRIMARY_BLUE

    p2 = tf_b.add_paragraph()
    p2.text = (
        "TRUEGUARD bridges the historic gap between high-accuracy multi-sample detectors and lightweight single-pass heuristics. "
        "It achieves top-tier 0.935 AUROC while requiring only a single forward pass, providing exact mathematical attributions, and "
        "actively repairing or abstaining from hallucinations via an automated feedback loop."
    )
    p2.font.name = "Calibri"
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = C_TEXT_MUTED
    p2.space_before = Pt(2)


# ---------------------------------------------------------------------------
# Slide 14: Conclusion, Limitations & Future Work
# ---------------------------------------------------------------------------
def build_slide_14(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Conclusions, System Limitations & Future Scope", "Synthesis", 14)

    # Left: Conclusions Card
    add_card(slide, 0.8, 1.4, 5.75, 5.5)
    tb_c = slide.shapes.add_textbox(Inches(1.0), Inches(1.55), Inches(5.35), Inches(5.15))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True

    p_ct = tf_c.paragraphs[0]
    p_ct.text = "CORE PROJECT CONTRIBUTIONS"
    p_ct.font.name = "Calibri"
    p_ct.font.size = Pt(13)
    p_ct.font.bold = True
    p_ct.font.color.rgb = C_ACCENT_EMERALD

    conclusions = [
        ("Unified Closed-Loop Paradigm:", "Successfully designed, implemented, and verified the first closed-loop feedback control framework for real-time LLM hallucination mitigation."),
        ("Single-Pass Multi-Sensor Fusion:", "Proved that intermediate hidden states, causal attention entropy, and logit distributions provide orthogonal, complementary factual signals (0.935 Macro AUROC)."),
        ("Live Hallucination Reduction:", "Demonstrated a 72.0% relative reduction in emitted hallucinations on live open-domain TriviaQA generations."),
        ("Edge & Production Feasibility:", "Maintains negligible latency overhead (+2.91 ms/token, +8.7%), delivering 4.65x faster execution than consistency sampling."),
        ("Full XAI Explainability:", "Provides instant signed log-odds attribution (c_k = w_k * z_k) revealing exactly which sensor flagged the falsehood."),
    ]
    for h, b in conclusions:
        p = tf_c.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"✔ {h} "
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(9.8)
        r2.font.color.rgb = C_TEXT_MUTED

    # Right: Limitations & Future Work Card
    add_card(slide, 6.8, 1.4, 5.75, 5.5)
    tb_f = slide.shapes.add_textbox(Inches(7.0), Inches(1.55), Inches(5.35), Inches(5.15))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p_lt = tf_f.paragraphs[0]
    p_lt.text = "LIMITATIONS & FUTURE RESEARCH SCOPE"
    p_lt.font.name = "Calibri"
    p_lt.font.size = Pt(13)
    p_lt.font.bold = True
    p_lt.font.color.rgb = C_PRIMARY_BLUE

    limits = [
        ("White-Box Access Requirement:", "Requires access to internal hidden activations and attention matrices; cannot be applied to black-box proprietary APIs (e.g., OpenAI GPT-4)."),
        ("Linear Separability Assumption:", "Assumes truthfulness is linearly separable in intermediate manifolds; extreme multi-hop reasoning may require non-linear geometric kernels."),
    ]
    p_sub1 = tf_f.add_paragraph()
    p_sub1.text = "CURRENT SYSTEM LIMITATIONS:"
    p_sub1.font.name = "Calibri"
    p_sub1.font.size = Pt(11)
    p_sub1.font.bold = True
    p_sub1.font.color.rgb = C_ACCENT_CORAL
    p_sub1.space_before = Pt(6)

    for h, b in limits:
        p = tf_f.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = f"• {h} "
        r1.font.bold = True
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED

    futures = [
        ("Scaling to 8B+ Architectures:", "Porting TRUEGUARD probes to Llama-3-8B and Mistral-7B-v0.3 across multi-GPU distributed clusters."),
        ("Multimodal Vision-Language Expansion:", "Extending sensor extraction to vision-language models (LLaVA, CLIP) to detect visual object hallucination."),
        ("Edge Mobile Quantization:", "Quantizing probe weights to INT4 / FP8 for sub-millisecond on-device smartphone inference."),
    ]
    p_sub2 = tf_f.add_paragraph()
    p_sub2.text = "FUTURE RESEARCH DIRECTIONS:"
    p_sub2.font.name = "Calibri"
    p_sub2.font.size = Pt(11)
    p_sub2.font.bold = True
    p_sub2.font.color.rgb = C_ACCENT_TEAL
    p_sub2.space_before = Pt(8)

    for h, b in futures:
        p = tf_f.add_paragraph()
        p.space_before = Pt(3)
        r1 = p.add_run()
        r1.text = f"➔ {h} "
        r1.font.bold = True
        r1.font.size = Pt(9.8)
        r1.font.color.rgb = C_DARK_NAVY
        r2 = p.add_run()
        r2.text = b
        r2.font.size = Pt(9.5)
        r2.font.color.rgb = C_TEXT_MUTED


# ---------------------------------------------------------------------------
# Slide 15: References
# ---------------------------------------------------------------------------
def build_slide_15(prs: Presentation):
    slide = add_blank_slide(prs)
    add_header(slide, "Key References & Authoritative Literature Citations", "References", 15)

    add_card(slide, 0.8, 1.4, 11.75, 5.55)
    tb_ref = slide.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.35), Inches(5.35))
    tf_ref = tb_ref.text_frame
    tf_ref.word_wrap = True

    references = [
        ("[1]", "Azaria, A., & Mitchell, T. (2023). The Internal State of an LLM Knows When It's Lying. Findings of the Association for Computational Linguistics: EMNLP 2023, 967–976."),
        ("[2]", "Li, K., Patel, O., Viégas, F., Pfister, H., & Wattenberg, M. (2024). Inference-Time Intervention: Eliciting Truthful Answers from a Language Model. Advances in Neural Information Processing Systems (NeurIPS 2023), 36, 4321–4342."),
        ("[3]", "Manakul, P., Liusie, A., & Gales, M. J. F. (2023). SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models. In Proceedings of EMNLP 2023, 6362–6377."),
        ("[4]", "Kuhn, L., Gal, Y., & Farquhar, S. (2023). Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Large Language Models. In International Conference on Learning Representations (ICLR 2023)."),
        ("[5]", "Lin, S., Hilton, J., & Evans, O. (2022). TruthfulQA: Measuring How Models Mimic Human Falsehoods. In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (ACL 2022), 3214–3252."),
        ("[6]", "Li, J., Cheng, X., Zhao, W. X., Nie, J. Y., & Wen, J. R. (2023). HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models. In Proceedings of EMNLP 2023, 6449–6464."),
        ("[7]", "Asai, A., Sewon, M., et al. (2024). Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection. In International Conference on Learning Representations (ICLR 2024)."),
        ("[8]", "Dhuliawala, S., Komeili, M., et al. (2024). Chain-of-Verification Reduces Hallucination in Large Language Models. Transactions of the Association for Computational Linguistics (TACL), 12, 145–160."),
        ("[9]", "Huang, Y., et al. (2024). TrustLLM: Trustworthiness in Large Language Models. In International Conference on Machine Learning (ICML 2024)."),
        ("[10]", "Sharma, A., et al. (2024). Why Would You Suggest That? Human Trust in Language Models with Verifiable Attribution. In ACM Conference on Human Factors in Computing Systems (CHI 2024)."),
    ]

    p_rt = tf_ref.paragraphs[0]
    p_rt.text = "SELECT BIBLIOGRAPHY (APA FORMAT):"
    p_rt.font.name = "Calibri"
    p_rt.font.size = Pt(11)
    p_rt.font.bold = True
    p_rt.font.color.rgb = C_PRIMARY_BLUE

    for tag, cit in references:
        p = tf_ref.add_paragraph()
        p.space_before = Pt(5)
        r_tag = p.add_run()
        r_tag.text = f"{tag} "
        r_tag.font.bold = True
        r_tag.font.size = Pt(9.5)
        r_tag.font.color.rgb = C_ROYAL_BLUE

        r_c = p.add_run()
        r_c.text = cit
        r_c.font.size = Pt(9.2)
        r_c.font.color.rgb = C_TEXT_DARK


# ---------------------------------------------------------------------------
# Main Orchestration & Export
# ---------------------------------------------------------------------------
def main():
    print("Initializing 15-Slide Master Final Review Presentation...")
    prs = create_base_presentation()

    build_slide_1(prs)   # Title
    build_slide_2(prs)   # Outline
    build_slide_3(prs)   # Introduction & Motivation
    build_slide_4(prs)   # Literature Review Part 1 (10 papers table)
    build_slide_5(prs)   # Literature Review Part 2 (11 papers table)
    build_slide_6(prs)   # Scope & Problem Statement
    build_slide_7(prs)   # Research Challenges
    build_slide_8(prs)   # Research Objectives
    build_slide_9(prs)   # Proposed Architecture (ISP, AAS, EEM, DST + Fig 7.1)
    build_slide_10(prs)  # Proposed Methodology (Three-Tier Closed-Loop)
    build_slide_11(prs)  # Results & Discussion (Fig 7.2)
    build_slide_12(prs)  # Live Closed-Loop Mitigation & Latency (Fig 8.3)
    build_slide_13(prs)  # Comparison with Existing Works
    build_slide_14(prs)  # Conclusion, Limitations & Future Work
    build_slide_15(prs)  # References

    out_pptx = SUBMISSION_DIR / "FINAL_PRESENTATION.pptx"
    prs.save(str(out_pptx))
    print(f"Presentation saved successfully to: {out_pptx}")

    # Mirror to ROOT and CAPSTONE
    for target in [ROOT / "FINAL_PRESENTATION.pptx", CAPSTONE / "FINAL_PRESENTATION.pptx"]:
        try:
            shutil.copy2(out_pptx, target)
            print(f"Mirrored: {target}")
        except Exception as e:
            print(f"Error mirroring to {target}: {e}")

    # Export to PDF via PowerPoint COM if available
    out_pdf = SUBMISSION_DIR / "FINAL_PRESENTATION.pdf"
    print("Attempting export to PDF via PowerPoint COM...")
    try:
        ps_cmd = (
            f"$ppt = New-Object -ComObject PowerPoint.Application; "
            f"$pres = $ppt.Presentations.Open('{out_pptx}', 2, 0, 0); "
            f"$pres.SaveAs('{out_pdf}', 32); "
            f"$pres.Close(); "
            f"$ppt.Quit()"
        )
        subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, timeout=30)
        print(f"PDF exported successfully to: {out_pdf}")
        for target_pdf in [ROOT / "FINAL_PRESENTATION.pdf", CAPSTONE / "FINAL_PRESENTATION.pdf"]:
            try:
                shutil.copy2(out_pdf, target_pdf)
                print(f"Mirrored: {target_pdf}")
            except Exception as e:
                print(f"Error mirroring {target_pdf}: {e}")
    except Exception as e:
        print(f"Note on PDF export: {e}. PPTX is the primary authoritative presentation.")


if __name__ == "__main__":
    main()
