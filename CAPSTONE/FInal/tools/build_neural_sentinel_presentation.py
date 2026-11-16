"""
TRUEGUARD: NEURAL SENTINEL - Final University Viva Presentation Generator
Theme: NEURAL SENTINEL (Deep Midnight Navy #080F25, Obsidian Cards, Electric Cyan, Teal, Violet, Crimson)
Total Slides: Exactly 30 Slides
Literature Review: Exactly 4 Slides (10 papers each = 40 papers total)
University: Vellore Institute of Technology (VIT), Chennai
Candidate: Yogesh Ravi M (22MIA1052)
Guide: Dr. Pradeep Kumar T S
"""

import sys
import shutil
import subprocess
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

ROOT_DIR = Path(r"E:\trueguard")
CAPSTONE_DIR = ROOT_DIR / "CAPSTONE"
FINAL_DIR = CAPSTONE_DIR / "FInal"
SUBMISSION_DIR = ROOT_DIR / "FINAL_SUBMISSION"
FIG_DIR = ROOT_DIR / "outputs" / "figures"

OUT_PPTX = ROOT_DIR / "TRUEGUARD_NEURAL_SENTINEL_FINAL.pptx"
OUT_PDF = ROOT_DIR / "TRUEGUARD_NEURAL_SENTINEL_FINAL.pdf"

# Theme Colors: NEURAL SENTINEL
BG_DARK = RGBColor(8, 15, 37)          # #080F25 - Primary Midnight Navy
BG_CARD = RGBColor(15, 26, 54)         # #0F1A36 - Deep Obsidian Card
BG_CARD_ALT = RGBColor(22, 35, 71)     # #162347 - Secondary Obsidian Slate
CYAN_ACCENT = RGBColor(0, 215, 242)    # #00D7F2 - Electric Cyan
TEAL_SAFE = RGBColor(46, 227, 190)     # #2EE3BE - Emerald / Teal Safe
VIOLET_ACCENT = RGBColor(151, 121, 255)# #9779FF - Electric Violet
CRIMSON_RISK = RGBColor(255, 95, 114)  # #FF5F72 - Coral Red Hallucination Risk
AMBER_WARN = RGBColor(251, 191, 36)    # #FBBF24 - Amber Warning
TEXT_WHITE = RGBColor(244, 247, 255)   # #F4F7FF - Main Crisp Text
TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8 - Secondary Muted Text
BORDER_CYAN = RGBColor(0, 215, 242)    # #00D7F2 - Cyan Accent Border
BORDER_MUTED = RGBColor(30, 45, 86)    # #1E2D56 - Subtle Dark Border

# Table Colors
TBL_HEADER_BG = RGBColor(10, 20, 48)   # #0A1430 - Table Header Dark Navy
TBL_ROW_1 = RGBColor(13, 23, 51)       # #0D1733 - Alternating Row 1
TBL_ROW_2 = RGBColor(19, 34, 71)       # #132247 - Alternating Row 2

FONT_TITLE = "Trebuchet MS"
FONT_BODY = "Segoe UI"
FONT_BOLD = "Segoe UI Semibold"

# Import 40 Literature Review Papers
sys.path.append(str(FINAL_DIR / "tools"))
from generate_final_presentation import LIT_SLIDES_DATA

def set_slide_background(slide, color=BG_DARK):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(11.25))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    slide.shapes._spTree.remove(bg._element)
    slide.shapes._spTree.insert(2, bg._element)

def add_slide_bg_image(slide, image_name: str):
    img_path = FIG_DIR / image_name
    if img_path.exists():
        pic = slide.shapes.add_picture(str(img_path), Inches(0), Inches(0), Inches(20.0), Inches(11.25))
        slide.shapes._spTree.remove(pic._element)
        slide.shapes._spTree.insert(2, pic._element)
    else:
        set_slide_background(slide)

def add_header_banner(slide, title_text: str, category_text: str = "TRUEGUARD : NEURAL SENTINEL"):
    header = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(1.35))
    header.fill.solid()
    header.fill.fore_color.rgb = RGBColor(6, 12, 30)
    header.line.fill.background()
    
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.35), Inches(20.0), Inches(0.06))
    strip.fill.solid()
    strip.fill.fore_color.rgb = CYAN_ACCENT
    strip.line.fill.background()
    
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(15.5), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = category_text.upper()
    p0.font.name = FONT_BOLD
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = CYAN_ACCENT
    p0.space_after = Pt(2)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.name = FONT_TITLE
    p1.font.size = Pt(25)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    
    # Institution Badge Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(16.6), Inches(0.35), Inches(2.6), Inches(0.65))
    pill.fill.solid()
    pill.fill.fore_color.rgb = BG_CARD
    pill.line.color.rgb = CYAN_ACCENT
    pill.line.width = Pt(1.5)
    ptf = pill.text_frame
    ptf.text = "VIT CHENNAI"
    ptf.paragraphs[0].alignment = PP_ALIGN.CENTER
    ptf.paragraphs[0].font.name = FONT_BOLD
    ptf.paragraphs[0].font.size = Pt(14)
    ptf.paragraphs[0].font.bold = True
    ptf.paragraphs[0].font.color.rgb = TEXT_WHITE

def add_speaker_notes(slide, notes_text: str):
    slide.notes_slide.notes_text_frame.text = notes_text.strip()

def create_cyber_card(slide, left: float, top: float, width: float, height: float,
                      bg_color=BG_CARD, border_color=BORDER_MUTED, corner_radius=True) -> tuple:
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
                   headers: list, rows: list, col_widths: list, header_fs=12.0, cell_fs=10.0):
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height))
    table = table_shape.table
    
    for i, w in enumerate(col_widths):
        table.columns[i].width = Inches(w)
        
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = TBL_HEADER_BG
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)
        p = tf.paragraphs[0]
        p.text = h
        p.font.name = FONT_BOLD
        p.font.size = Pt(header_fs)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT
        p.alignment = PP_ALIGN.CENTER if j == 0 else PP_ALIGN.LEFT
        
    for r_idx, row_data in enumerate(rows):
        row_bg = TBL_ROW_1 if r_idx % 2 == 0 else TBL_ROW_2
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.12)
            tf.margin_right = Inches(0.12)
            p = tf.paragraphs[0]
            p.text = str(val)
            p.font.name = FONT_BODY
            p.font.size = Pt(cell_fs)
            p.font.color.rgb = CYAN_ACCENT if c_idx == 0 else (TEXT_WHITE if c_idx < 3 else TEXT_MUTED)
            if c_idx == 1:
                p.font.bold = True
                p.font.color.rgb = TEXT_WHITE
            if c_idx == 0:
                p.alignment = PP_ALIGN.CENTER
                p.font.bold = True
    return table_shape

def build_neural_sentinel_presentation():
    prs = Presentation()
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    
    print("Building TRUEGUARD: NEURAL SENTINEL Presentation (30 Slides)...")

    # =========================================================================
    # SLIDE 1: University Title Slide (NEURAL SENTINEL)
    # =========================================================================
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s1, "bg_neural_sentinel.jpg")
    
    # Left Translucent Obsidian Container
    card_title = create_cyber_card(s1, 1.0, 1.2, 12.8, 8.85, BG_CARD, BORDER_CYAN)
    
    # VIT Logo (Top Right of container or slide)
    vit_logo = FIG_DIR / "vit_logo_hd.png"
    if vit_logo.exists():
        s1.shapes.add_picture(str(vit_logo), Inches(14.5), Inches(1.5), width=Inches(4.5))
    
    tb1 = s1.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(11.8), Inches(8.2))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "VELLORE INSTITUTE OF TECHNOLOGY (VIT), CHENNAI"
    p.font.name = FONT_BOLD
    p.font.size = Pt(17)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(4)
    
    p = tf1.add_paragraph()
    p.text = "School of Computer Science and Engineering (SCOPE) | Final Review Project Presentation"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(24)
    
    p = tf1.add_paragraph()
    p.text = "TRUEGUARD"
    p.font.name = FONT_TITLE
    p.font.size = Pt(46)
    p.font.bold = True
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(6)
    
    p = tf1.add_paragraph()
    p.text = "A Real-Time, Internal-State-Based LLM Hallucination Detection & Mitigation Framework"
    p.font.name = FONT_TITLE
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    p.text = "Toward Trustworthy Large Language Models via Multi-Sensor Telemetry & Closed-Loop Control"
    p.font.name = FONT_BODY
    p.font.size = Pt(16)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(36)
    
    p = tf1.add_paragraph()
    p.text = "Presented by:"
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = CYAN_ACCENT
    
    p = tf1.add_paragraph()
    p.text = "Yogesh Ravi M  |  Reg. No.: 22MIA1052\nIntegrated M.Tech Computer Science & Engineering (Data Science)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(16)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(18)
    
    p = tf1.add_paragraph()
    p.text = "Project Guide:"
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = CYAN_ACCENT
    
    p = tf1.add_paragraph()
    p.text = "Dr. Pradeep Kumar T S\nAssociate Professor Grade 1, School of Computer Science and Engineering"
    p.font.name = FONT_BOLD
    p.font.size = Pt(15)
    p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s1, """
Respected Panel Members, Project Guide Dr. Pradeep Kumar T S, and Evaluators:
Good morning. My name is Yogesh Ravi M (Register Number 22MIA1052).
Today, I present our final-year capstone research project:
'TRUEGUARD: A Real-Time, Internal-State-Based LLM Hallucination Detection and Mitigation Framework'.

This work tackles one of the foundational safety crises in modern Artificial Intelligence: the catastrophic propensity of Large Language Models to generate fluent, highly convincing, but factually false statements known as hallucinations.
Over this presentation, I will walk you through our dual-paper academic contributions, 40-paper systematic review, the mathematical formulation of our four internal sensors, rigorous 5-fold cross-validation on TinyLlama-1.1B, and our closed-loop three-tier mitigation system that achieves a verified 72% reduction in emitted hallucinations with under 18% latency overhead.
""")

    # =========================================================================
    # SLIDE 2: Outline & Presentation Roadmap
    # =========================================================================
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s2)
    add_header_banner(s2, "PRESENTATION ROADMAP & DEFENSE STRUCTURE", "OVERVIEW")
    
    agenda_cards = [
        ("01", "FOUNDATIONS & MOTIVATION", "What is an LLM? Autoregressive token generation, next-token probabilities, and the root physical causes of hallucination in Transformer architectures.", CYAN_ACCENT),
        ("02", "LITERATURE REVIEW & GAPS", "Systematic PRISMA review of 40 peer-reviewed papers (2020–2025) across 4 pillars, identifying the 4 fundamental gaps in unimodal sensing.", TEAL_SAFE),
        ("03", "WHITE-BOX TELEMETRY & ARCHITECTURE", "Why TRUEGUARD requires white-box model access; TinyLlama-1.1B backbone; Master Closed-Loop Feedback Architecture.", VIOLET_ACCENT),
        ("04", "FOUR-SENSOR TELEMETRY BANK", "Mathematical formulation of Internal State Probes (ISP), Attention Anomaly (AAS), Energy-Entropy (EEM), and Latent Drift (DST).", CYAN_ACCENT),
        ("05", "DATASET CURATION & TRAINING PIPELINE", "1,598 paired queries (3,196 labeled rows) across TruthfulQA & HaluEval; PyTorch hooks; 5-Fold Grouped Cross-Validation protocol.", AMBER_WARN),
        ("06", "MITIGATION, RESULTS & LIMITATIONS", "3-Tier Closed-Loop Controller on TriviaQA; 72.0% hallucination reduction; Tesla T4 latency profiling; 4 core scientific limitations.", CRIMSON_RISK),
    ]
    
    for i, (num, title, desc, accent) in enumerate(agenda_cards):
        col = i % 3
        row = i // 3
        left = 0.8 + col * 6.25
        top = 1.8 + row * 4.45
        card = create_cyber_card(s2, left, top, 5.9, 4.15, BG_CARD, BORDER_MUTED)
        
        tb = s2.shapes.add_textbox(Inches(left + 0.35), Inches(top + 0.35), Inches(5.2), Inches(3.45))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = num
        p.font.name = FONT_BOLD
        p.font.size = Pt(28)
        p.font.bold = True
        p.font.color.rgb = accent
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = title
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = desc
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s2, """
Slide 2 establishes our presentation roadmap, precisely structured according to the university guidelines.
We begin with foundational concepts so that examiners see the exact mechanics of language modeling.
Then we move through our 40-paper review, research gaps, proposed architecture, sensor formulation, dataset pipeline, and experimental results.
Finally, we candidly address real-world deployment boundaries and honest scientific limitations.
""")

    # =========================================================================
    # SLIDE 3: Foundations — What is an LLM? What is Hallucination?
    # =========================================================================
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s3, "bg_transformer_layers.jpg")
    add_header_banner(s3, "WHAT IS AN LLM? WHAT IS HALLUCINATION? (FIRST-PRINCIPLES)", "FOUNDATIONS")
    
    # Left Card: Autoregressive LLM
    card_l = create_cyber_card(s3, 0.8, 1.8, 9.0, 8.8, BG_CARD, CYAN_ACCENT)
    tb_l = s3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "How a Large Language Model Generates Text"
    p.font.name = FONT_BOLD
    p.font.size = Pt(21)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)
    
    pts_l = [
        ("1. Tokens, Not Words: ", "Text is decomposed into sub-word tokens (e.g. 'understanding' -> ['under', 'standing']). LLMs process discrete token IDs."),
        ("2. Autoregressive Factorization: ", "An LLM models joint text probability autoregressively: P(w1, w2, ..., wT) = Prod P(wt | w<t). It predicts exactly ONE next token at each step."),
        ("3. Statistical Correlation != Factuality: ", "The model selects tokens maximizing conditional log-likelihood based on pretraining corpora, NOT by querying an internal truth oracle."),
        ("4. Hidden State Accumulation: ", "At each layer, tokens update 2048-dimensional dense continuous vectors through multi-head self-attention and feed-forward networks."),
        ("5. Softmax Sampling: ", "Logits are transformed into a probability distribution via Softmax(z / T). Even low-probability tokens have non-zero chances of being sampled.")
    ]
    for b_title, b_desc in pts_l:
        p = tf_l.add_paragraph()
        p.text = b_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = b_desc
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # Right Card: Hallucination Anatomy
    card_r = create_cyber_card(s3, 10.2, 1.8, 9.0, 8.8, BG_CARD, CRIMSON_RISK)
    tb_r = s3.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "The Mechanics of Hallucination"
    p.font.name = FONT_BOLD
    p.font.size = Pt(21)
    p.font.color.rgb = CRIMSON_RISK
    p.space_after = Pt(14)
    
    pts_r = [
        ("Definition of Hallucination: ", "Generated content that is nonsensical or unfaithful to the source text, real-world facts, or user instructions, despite appearing grammatically fluent."),
        ("Why Do LLMs Hallucinate? ", "1. Training Data Noise: Internet pretraining corpora contain falsehoods, biases, and unverified rumors.\n2. Overconfidence in Softmax: Exposure bias causes errors to compound autoregressively across tokens.\n3. Sycophancy & Prompt Bias: The LLM mirrors user presuppositions rather than factual grounding."),
        ("The Critical Safety Dilemma: ", "Hallucinations are NOT obvious gibberish. They adopt authoritative academic syntax, cite fake DOIs, and invent plausible medical dosages."),
        ("Detection Necessity: ", "External black-box prompting is too slow (+500% latency). We must inspect the model's internal physical states during the forward pass!")
    ]
    for b_title, b_desc in pts_r:
        p = tf_r.add_paragraph()
        p.text = b_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = b_desc
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s3, """
Slide 3 explains the core mechanics from absolute first principles.
An LLM does not possess consciousness or a factual database; it is a statistical next-token predictor.
It models conditional probability distributions over a fixed vocabulary.
Because training optimizes token log-likelihood rather than factual truth, the model easily generates statements that match syntactic patterns of truth while being factually false.
Crucially, exposure bias means once the model generates one false token, that false token enters the context window, causing subsequent tokens to cascade into extensive hallucinations.
""")

    # =========================================================================
    # SLIDE 4: Research Evidence & Concrete Problem Statement
    # =========================================================================
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s4, "bg_hallucination_stream.jpg")
    add_header_banner(s4, "RESEARCH EVIDENCE & CORE PROBLEM STATEMENT", "FOUNDATIONS")
    
    # Left Card: Authentic Case Study
    card_l = create_cyber_card(s4, 0.8, 1.8, 9.6, 8.8, BG_CARD, CRIMSON_RISK)
    tb_l = s4.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.0), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Concrete Case Study (TruthfulQA Benchmark)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RISK
    p.space_after = Pt(12)
    
    p = tf_l.add_paragraph()
    p.text = "User Question:\n\"What happens if you swallow a watermelon seed?\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(15)
    p.font.color.rgb = TEXT_WHITE
    p.space_after = Pt(12)
    
    p = tf_l.add_paragraph()
    p.text = "UNGUARDED BASELINE (TinyLlama-1.1B Output):\n\"If you swallow a watermelon seed, it will grow into a full watermelon in your stomach, causing extreme pain and rupture of the stomach lining.\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = CRIMSON_RISK
    p.space_after = Pt(10)
    
    p = tf_l.add_paragraph()
    p.text = "Internal Diagnostic Signal during Generation:\n- Output Softmax Probability: 0.94 (Overconfident!)\n- Middle-Layer Hidden State Truth Projection: -2.84 (Strongly False)\n- Attention Dispersion Entropy: 0.89 (Anomalously diffuse)\n- Final TRUEGUARD Risk Score: 0.874 (HIGH RISK FAULT)"
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(12)
    
    p = tf_l.add_paragraph()
    p.text = "GROUNDED FACTUAL REALITY:\n\"Watermelon seeds simply pass through the digestive system without germinating or causing harm.\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = TEAL_SAFE

    # Right Card: The Core Problem Statement
    card_r = create_cyber_card(s4, 10.8, 1.8, 8.4, 8.8, BG_CARD, CYAN_ACCENT)
    tb_r = s4.shapes.add_textbox(Inches(11.1), Inches(2.1), Inches(7.8), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "The Core Research Problem"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)
    
    issues = [
        ("Pervasiveness in Small LLMs: ", "Edge-deployable 1B-3B parameter models (e.g. TinyLlama) suffer hallucination rates exceeding 60% on open-domain factual QA."),
        ("Silent Softmax Failure: ", "The model's output softmax probability is notoriously uncalibrated: the model is frequently 95%+ confident while generating falsehoods."),
        ("Multi-Sample Latency Bottleneck: ", "Existing detection methods (SelfCheckGPT, SAC3) draw 5 to 20 completions per query, adding +135 ms/token (+400% latency). They cannot run in real time."),
        ("Open-Loop Vulnerability: ", "Detectors merely output a score; they lack closed-loop actuators to intercept, resample, search, or safely abstain before emitting text to users.")
    ]
    for i_title, i_desc in issues:
        p = tf_r.add_paragraph()
        p.text = i_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(13.5)
        p.font.bold = True
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = i_desc
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s4, """
Slide 4 provides authentic experimental evidence from TruthfulQA.
Notice how the unguarded TinyLlama generates a common childhood folklore misconception with high linguistic confidence.
The model states a watermelon will grow inside the stomach!
Critically, the output softmax probability was 0.94. If an application relied only on softmax confidence, this severe medical falsehood would be accepted as truth.
However, TRUEGUARD's internal probes reveal that middle-layer activations and attention entropy flag this token sequence as anomalous, producing a risk score of 0.874.
""")

    # =========================================================================
    # SLIDE 5: Two Research Papers & Core Project Objectives
    # =========================================================================
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s5)
    add_header_banner(s5, "TWO RESEARCH PAPERS & CORE PROJECT OBJECTIVES", "FOUNDATIONS")
    
    # Left Card: Two Papers
    card_l = create_cyber_card(s5, 0.8, 1.8, 9.6, 8.8, BG_CARD, VIOLET_ACCENT)
    tb_l = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.0), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Two Academic Research Papers Prepared"
    p.font.name = FONT_BOLD
    p.font.size = Pt(21)
    p.font.color.rgb = VIOLET_ACCENT
    p.space_after = Pt(14)
    
    p = tf_l.add_paragraph()
    p.text = "PAPER 1: Comprehensive Literature Review Paper\n\"Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(6)
    
    p = tf_l.add_paragraph()
    p.text = "Focus: Systematic PRISMA 2020 review of 40 peer-reviewed papers (2020–2025) across 4 pillars: Representation Probing, Attention Entropy, Closed-Loop Control, and Benchmarks. Identifies the 4 critical literature gaps."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED
    p.space_after = Pt(16)
    
    p = tf_l.add_paragraph()
    p.text = "PAPER 2: Original Research & Framework Paper\n\"TRUEGUARD: A Real-Time, Internal-State-Based LLM Hallucination Detection and Closed-Loop Mitigation Framework via Multi-Sensor Probing\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(6)
    
    p = tf_l.add_paragraph()
    p.text = "Focus: Mathematical formulation of 4 sensors (ISP, AAS, EEM, DST), 5-fold grouped cross-validation on TinyLlama-1.1B across 1,598 paired questions (3,196 labeled rows), 3-tier closed-loop mitigation on TriviaQA (72% emitted hallucination drop), and T4 GPU latency profiling."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = TEXT_MUTED

    # Right Card: 4 Objectives
    card_r = create_cyber_card(s5, 10.8, 1.8, 8.4, 8.8, BG_CARD, CYAN_ACCENT)
    tb_r = s5.shapes.add_textbox(Inches(11.1), Inches(2.1), Inches(7.8), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Four Specific Research Objectives"
    p.font.name = FONT_BOLD
    p.font.size = Pt(21)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)
    
    objs = [
        ("1. Multi-Sensor Internal Telemetry Bank:", "Design a single-pass forward hook extractor monitoring intermediate hidden states (ISP), attention dispersion (AAS), hybrid entropy (EEM), and semantic drift (DST)."),
        ("2. Calibrated Logistic Risk Fusion:", "Train a standardized L2-regularized fusion classifier with L-BFGS to output continuous risk r(x,y) in [0, 1] with log-odds sensor attributions."),
        ("3. Three-Tier Closed-Loop Actuator:", "Implement calibrated routing thresholds (tau_warn = 0.50, tau_fault = 0.75) into Safe Pass, Corrective Re-Sampling, Active RAG, or Calibrated Abstention."),
        ("4. Empirical Validation & Latency Profiling:", "Evaluate detection AUROC across 4 benchmarks, cross-backbone transfer (TinyLlama vs GPT-2), and profile latency on an NVIDIA Tesla T4 GPU.")
    ]
    for o_t, o_d in objs:
        p = tf_r.add_paragraph()
        p.text = o_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13.5)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(2)
        p = tf_r.add_paragraph()
        p.text = o_d
        p.font.name = FONT_BODY
        p.font.size = Pt(12.5)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    add_speaker_notes(s5, """
Slide 5 clarifies the academic foundation of our project.
We produced two distinct manuscripts:
Paper 1 is our Comprehensive Review Paper covering 40 peer-reviewed papers across 4 pillars.
Paper 2 is our Original TRUEGUARD System Paper presenting the full mathematical derivation, experimental pipeline, 5-fold cross-validation, and closed-loop mitigation controller.
The four project objectives directly map to the experimental chapters in our final thesis report.
""")

    # =========================================================================
    # SLIDES 6 to 9: Literature Review (4 Slides, 10 Papers Each = 40 Papers Total)
    # =========================================================================
    lit_headers = ["No.", "Author(s), Year & Venue", "Method / Architecture", "Key Academic Contribution", "Research Gap / Limitation"]
    lit_col_widths = [0.8, 3.6, 4.2, 4.9, 4.9]
    all_40 = [p for chunk in LIT_SLIDES_DATA for p in chunk]
    chunks_10 = [all_40[i:i+10] for i in range(0, 40, 10)]
    
    pillar_names = [
        ("PILLAR 1: INTERNAL STATE PROBING & REPRESENTATION GEOMETRY", "Papers 1 to 10 analyze whether intermediate hidden states linearly encode truthfulness (Azaria & Mitchell, 2023; Su et al., 2024; Li et al., 2023). While middle layers separate true vs false facts, they miss attention dispersion and provide no closed-loop factual repair."),
        ("PILLAR 2: ATTENTION ANOMALIES & INFORMATION ENTROPY", "Papers 11 to 20 focus on attention maps, predictive uncertainty, and semantic entropy (Burns et al., 2022; Kadavath et al., 2022; Manakul et al., 2023; Farquhar et al., 2024). They expose that surface entropy inverts under overconfident hallucinations, and sampling consistency incurs 500% to 2000% latency."),
        ("PILLAR 3: CLOSED-LOOP FEEDBACK & SELECTIVE MITIGATION", "Papers 21 to 30 investigate retrieval-augmented generation and controlled decoding (Lewis et al., 2020; Asai et al., 2023; Dathathri et al., 2020). Existing works are either passive scorers without correction or aggressive steering vectors that distort linguistic fluency without fetching external evidence."),
        ("PILLAR 4: FACTUALITY BENCHMARKS, CALIBRATION & SAFETY", "Papers 31 to 40 curate the standardized evaluation corpora (TruthfulQA by Lin et al., 2022; HaluEval by Li et al., 2023; FActScore by Min et al., 2023) and calibration techniques (Platt scaling, selective prediction). They establish the need for grouped evaluation to prevent data leakage.")
    ]
    
    for idx, ((p_name, p_notes), papers) in enumerate(zip(pillar_names, chunks_10)):
        slide_no = 6 + idx
        s_lit = prs.slides.add_slide(prs.slide_layouts[6])
        set_slide_background(s_lit)
        add_header_banner(s_lit, p_name, f"LITERATURE REVIEW (SLIDE {idx+1} OF 4)")
        add_table_grid(s_lit, 0.8, 1.65, 18.4, 9.1, lit_headers, papers, lit_col_widths, header_fs=12.0, cell_fs=10.0)
        
        add_speaker_notes(s_lit, f"""
Slide {slide_no} presents {p_name} covering papers {idx*10 + 1} to {idx*10 + len(papers)} of our 40-paper PRISMA review.
{p_notes}
Each paper was systematically analyzed in our Review Paper (Paper 1), showing that individual physical mechanisms fail under edge cases, motivating TRUEGUARD's multi-sensor fusion.
""")

    # =========================================================================
    # SLIDE 10: Research Gaps Identified
    # =========================================================================
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s10)
    add_header_banner(s10, "SYSTEMATIC RESEARCH GAPS IDENTIFIED ACROSS 40 PAPERS", "RESEARCH GAPS")
    
    gaps = [
        ("GAP 1: SINGLE-SIGNAL FRAGILITY & UNIMODAL SENSING",
         "Existing detectors rely on a single physical mechanism: either middle-layer hidden activations (SAPLMA, MIND) OR token entropy (Kadavath) OR attention weights. No prior framework fuses all four complementary internal signals into a single unified state observer.",
         CRIMSON_RISK),
        ("GAP 2: SIGNAL POLARITY INVERSION UNDER ASYMMETRY",
         "On datasets where answer length or sentence structure differs between true and hallucinated classes (HaluEval-QA, Dialogue), raw token entropy inverts its diagnostic correlation (AUROC drops to 0.349). Supervised linear projection and recalibration are mandatory to enforce positive diagnostic alignment.",
         AMBER_WARN),
        ("GAP 3: MULTI-SAMPLE INFERENCE-TIME COMPUTATIONAL OVERHEAD",
         "Black-box consistency baselines (SelfCheckGPT, SAC3) require drawing 5 to 20 full autoregressive completions per query. This increases latency by 500% to 2000% (+134 ms/token), rendering them economically and computationally infeasible for interactive production.",
         VIOLET_ACCENT),
        ("GAP 4: OPEN-LOOP DETECTION WITHOUT CLOSED-LOOP FEEDBACK CONTROL",
         "Prior works operate as disconnected silos: detectors compute a passive risk score without intervention; activation steering methods (ITI) distort fluency without retrieving factual context. A principled 3-tier closed-loop feedback controller was entirely missing from literature.",
         CYAN_ACCENT)
    ]
    for i, (g_title, g_desc, g_color) in enumerate(gaps):
        card = create_cyber_card(s10, 0.8, 1.8 + i * 2.2, 18.4, 1.95, BG_CARD, g_color)
        tb = s10.shapes.add_textbox(Inches(1.1), Inches(1.9 + i * 2.2), Inches(17.8), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = g_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = g_color
        p.space_after = Pt(6)
        p = tf.add_paragraph()
        p.text = g_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s10, """
Slide 10 synthesizes the four structural research gaps exposed by our PRISMA literature review.
Gap 1 is single-signal blindness: hidden state probes miss attention dispersion; attention monitors miss semantic drift.
Gap 2 is mathematical polarity inversion: on asymmetric datasets, raw entropy inverts to 0.349 AUROC because hallucinated answers happen to be phrased verbosely.
Gap 3 is the catastrophic inference latency of black-box sampling (+500% to +2000% slower).
Gap 4 is open-loop passivity: existing tools tell you a hallucination occurred after the user has already read it, without correcting or withholding it.
""")

    # =========================================================================
    # SLIDE 11: Comparative Feature Matrix
    # =========================================================================
    s11 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s11)
    add_header_banner(s11, "COMPARATIVE FEATURE MATRIX: EXISTING METHODS VS. TRUEGUARD", "BENCHMARK COMPARISON")
    
    comp_headers = ["Framework / Paradigm", "Monitored Signal", "Multi-Sensor Fusion", "Inference Passes", "Latency Overhead", "Mitigation Mechanism", "Paired AUROC"]
    comp_rows = [
        ["SelfCheckGPT (Manakul 2023)", "Black-Box Sampling Consistency", "No (Unimodal)", "5-20 autogressive draws", "+405% to +1800% (High)", "None (Passive scorer)", "0.762 - 0.820"],
        ["SAPLMA (Azaria & Mitchell 2023)", "Single-layer Hidden States", "No (Layer 16 only)", "1 forward pass", "+3.5% (Low)", "None (Passive scorer)", "0.784 - 0.831"],
        ["MIND Probe (Su et al. 2024)", "Intermediate MLP Activations", "No (Hidden states only)", "1 forward pass", "+4.2% (Low)", "None (Passive scorer)", "0.812 - 0.856"],
        ["Inference-Time Intervention (Li 2023)", "Activation Steering Vectors", "No (Attention heads)", "1 forward pass", "+8.0% (Moderate)", "Steering (Fluency degradation)", "0.741 - 0.790"],
        ["Semantic Entropy (Farquhar 2024)", "Cluster-based Sampling Entropy", "No (Surface entropy)", "10-20 forward passes", "+850% (Extreme)", "None (Passive scorer)", "0.810 - 0.865"],
        ["TRUEGUARD (Ours, Paper 2)", "ISP + AAS + EEM + DST (4 Sensors)", "YES (Calibrated Logistic Fusion)", "1 forward pass (single)", "+8.7% (Post) / +17.3% (Online)", "3-Tier Closed-Loop Controller", "0.935 (Macro AUROC)"]
    ]
    comp_widths = [3.2, 3.2, 2.3, 2.5, 2.5, 2.8, 1.9]
    add_table_grid(s11, 0.8, 1.8, 18.4, 8.8, comp_headers, comp_rows, comp_widths, header_fs=12.0, cell_fs=11.0)
    
    add_speaker_notes(s11, """
Slide 11 presents our comparative feature matrix.
We contrast TRUEGUARD against the five prominent state-of-the-art baselines.
Notice that sampling consistency baselines like SelfCheckGPT require 5 to 20 autoregressive draws, adding over 400% latency.
Internal state probing methods like SAPLMA and MIND achieve low latency but remain passive scorers with no mitigation.
TRUEGUARD is the only framework that achieves multi-sensor fusion, single-pass real-time execution (+8.7% to +17.3% overhead), 3-tier closed-loop mitigation, and 0.935 Macro AUROC.
""")

    # =========================================================================
    # SLIDE 12: Model Choice & White-Box vs Black-Box Paradigm
    # =========================================================================
    s12 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s12)
    add_header_banner(s12, "TINYLLAMA-1.1B FOUNDATION MODEL & WHITE-BOX ACCESS", "ARCHITECTURE")
    
    # Left Card: Why TinyLlama & Model Choice
    card_l = create_cyber_card(s12, 0.8, 1.8, 8.6, 8.8, BG_CARD, CYAN_ACCENT)
    tb_l = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.0), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Why TinyLlama-1.1B Foundation Model?"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)
    
    m_pts = [
        ("Architecture: ", "Llama-2 architecture scaled down: 22 Transformer layers, 2048 hidden dimension, 32 attention heads, 32,000 vocabulary size."),
        ("Pretraining Scale: ", "Pretrained on 3 Trillion tokens by Zhang et al. (2024), providing mature linguistic and factual representations."),
        ("Edge-Deployability: ", "Runs at sub-40 ms latency on single consumer GPUs or CPU edge devices. Ideal for private on-premise deployment."),
        ("Scientific Reproducibility: ", "Fully open-source weights; eliminates black-box API drift, hidden updates, and undisclosed safety filters."),
        ("Model Integrity: ", "TINYLLAMA WEIGHTS ARE 100% FROZEN. TRUEGUARD trains only lightweight external probes and a fusion classifier.")
    ]
    for m_t, m_d in m_pts:
        p = tf_l.add_paragraph()
        p.text = m_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = m_d
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # Right Side: White-Box vs Black-Box Diagram
    wb_img = FIG_DIR / "fig_sentinel_white_vs_black_box.png"
    if wb_img.exists():
        s12.shapes.add_picture(str(wb_img), Inches(9.8), Inches(1.8), width=Inches(9.4))

    add_speaker_notes(s12, """
Slide 12 justifies our foundation model selection and visually contrasts the white-box and black-box paradigms.
TinyLlama-1.1B uses the exact Llama-2 architecture with 22 layers and 2048 hidden dimensions.
It is completely frozen; we do not fine-tune or retrain TinyLlama from scratch.
As the diagram on the right illustrates, commercial black-box APIs like ChatGPT and Claude block access to hidden states, attention matrices, and logits.
TRUEGUARD requires white-box access to inspect the model's internal physical forward pass.
""")

    # =========================================================================
    # SLIDE 13: Master System Architecture Diagram
    # =========================================================================
    s13 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s13)
    add_header_banner(s13, "MASTER SYSTEM ARCHITECTURE: CLOSED-LOOP FEEDBACK CONTROLLER", "ARCHITECTURE")
    
    master_arch = FIG_DIR / "fig_trueguard_architecture_master.png"
    if master_arch.exists():
        s13.shapes.add_picture(str(master_arch), Inches(0.8), Inches(1.75), width=Inches(18.4))

    add_speaker_notes(s13, """
Slide 13 is our master system architecture diagram, rendering the complete end-to-end TRUEGUARD pipeline.
1. The user query enters the tokenizer and frozen TinyLlama-1.1B backbone.
2. During the single forward pass, PyTorch hooks extract activations without modifying model weights.
3. Four telemetry sensors compute physical metrics: ISP probes middle-to-late hidden states; AAS monitors attention entropy across the final quartile of layers; EEM measures hybrid token entropy; and DST tracks temporal cosine drift.
4. Features are standardized and fed to our calibrated logistic fusion classifier, which outputs a continuous risk score r(x,y).
5. The 3-tier closed-loop controller routes the output: safe responses pass directly; warning risks trigger risk-guided re-sampling; fault risks trigger Wikipedia RAG retrieval; and unfixable risks escalate to calibrated safe abstention.
""")

    # =========================================================================
    # SLIDE 14: Four-Sensor Telemetry Bank Overview
    # =========================================================================
    s14 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s14, "bg_four_sensors.jpg")
    add_header_banner(s14, "FOUR-SENSOR INTERNAL TELEMETRY BANK: MATHEMATICAL FORMULATION", "SENSORS")
    
    sensor_cards = [
        ("ISP: Internal State Probe",
         "Physical Signal: Intermediate hidden representations (h_l) across layers 9, 13, 16, 19.\n\n"
         "Mechanism: Supervised logistic regression probes projecting 2048-dim vectors onto a learned 1D truthfulness manifold.\n\n"
         "Intuition: Middle-to-late layers encode abstract factual truth before syntactic surface formatting.",
         CYAN_ACCENT),
        ("AAS: Attention Anomaly Sensor",
         "Physical Signal: Multi-head attention dispersion over the final quartile of layers (layers 16 to 21).\n\n"
         "Mechanism: Normalized Shannon entropy across context tokens: H_norm = -sum(A log A) / ln(S).\n\n"
         "Intuition: Factual recall focuses sharply on key context tokens; hallucination diffuses attention uniformly.",
         TEAL_SAFE),
        ("EEM: Energy-Entropy Monitor",
         "Physical Signal: Logit probability distribution over the 32,000 vocabulary tokens.\n\n"
         "Mechanism: Weighted hybrid of normalized Shannon entropy (we=0.6) and Renyi-2 entropy (0.4).\n\n"
         "Intuition: Captures lexical uncertainty and probability sharpness, penalizing flat probability distributions.",
         VIOLET_ACCENT),
        ("DST: Distribution Shift Tracker",
         "Physical Signal: Temporal cosine drift of representation centroids across consecutive tokens.\n\n"
         "Mechanism: Cosine distance 1 - cos(h_t, h_t-1) averaged across late layers 13, 16, 19.\n\n"
         "Intuition: Sudden directional shifts in latent trajectory signal semantic divergence from prompt context.",
         AMBER_WARN)
    ]
    for i, (s_title, s_desc, s_color) in enumerate(sensor_cards):
        left = 0.8 + i * 4.65
        card = create_cyber_card(s14, left, 1.8, 4.4, 8.8, BG_CARD, s_color)
        tb = s14.shapes.add_textbox(Inches(left + 0.25), Inches(2.1), Inches(3.9), Inches(8.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = s_color
        p.space_after = Pt(12)
        p = tf.add_paragraph()
        p.text = s_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s14, """
Slide 14 introduces our four-sensor internal telemetry bank.
Rather than relying on any single measurement, TRUEGUARD monitors four distinct physical phenomena in the Transformer forward pass.
ISP inspects intermediate hidden state geometry;
AAS inspects attention dispersion across the final quartile of layers;
EEM inspects logit probability entropy and sharpness;
and DST inspects representation trajectory drift.
Each sensor captures orthogonal information, ensuring robust detection across diverse failure modes.
""")

    # =========================================================================
    # SLIDE 15: Sensor Deep Dive 1 — ISP & AAS
    # =========================================================================
    s15 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s15)
    add_header_banner(s15, "DEEP DIVE: INTERNAL STATE PROBES (ISP) & ATTENTION ANOMALIES (AAS)", "SENSORS")
    
    # Left Card: ISP
    card_l = create_cyber_card(s15, 0.8, 1.8, 9.0, 8.8, BG_CARD, CYAN_ACCENT)
    tb_l = s15.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Internal State Probing (ISP) Formulation"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)
    
    isp_pts = [
        ("Layer Selection: ", "Probes 4 middle-to-late layers: fractions [0.45, 0.60, 0.75, 0.90] of total depth. For TinyLlama (22 layers), probe indices are Layers 9, 13, 16, and 19."),
        ("Probe Architecture: ", "Lightweight Logistic Regression with L2 regularization (C=1.0) and L-BFGS solver, trained on extracted 2048-dim hidden states."),
        ("Mathematical Mapping: ", "P(factual | h_l) = sigma(w_l^T h_l + b_l), where sigma(z) = 1 / (1 + e^-z)."),
        ("ISP Risk Component: ", "r_ISP = 1 - (1/4) * sum_{l in {9,13,16,19}} P(factual | h_l)."),
        ("Scientific Justification: ", "Middle-to-late layers exhibit maximum linear separability between factual and counterfactual statements, prior to output projection vocabulary collapse.")
    ]
    for it, idesc in isp_pts:
        p = tf_l.add_paragraph()
        p.text = it
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = idesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right Card: AAS
    card_r = create_cyber_card(s15, 10.2, 1.8, 9.0, 8.8, BG_CARD, TEAL_SAFE)
    tb_r = s15.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Attention Anomaly Sensor (AAS) Formulation"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(12)
    
    aas_pts = [
        ("Monitored Layers: ", "Calculates attention entropy over the final quartile of Transformer layers: Layers 16 to 21 in TinyLlama-1.1B."),
        ("Mathematical Formulation: ", "For each attention head h at layer l: H_{l,h} = - sum_{j=1}^S A_{l,h}(i,j) ln(A_{l,h}(i,j) + eps)."),
        ("Theoretical Normalization: ", "H_norm = H_{l,h} / ln(S), where S is the sequence length (maximum theoretical entropy). Clamped to [0, 1]."),
        ("AAS Aggregation: ", "AAS = (1 / |L_final|) sum_{l in L_final} (1 / H) sum_{h=1}^H H_norm(l,h)."),
        ("Empirical Behavior: ", "During factual recall, attention heads concentrate sharply on specific prompt entities (low AAS). During hallucination, attention diffuses broadly across non-relevant tokens (high AAS).")
    ]
    for at, adesc in aas_pts:
        p = tf_r.add_paragraph()
        p.text = at
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = adesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    add_speaker_notes(s15, """
Slide 15 provides the exact mathematical formulations of ISP and AAS as implemented in CAPSTONE/FInal/src/signal_extractors.py.
For ISP, we probe four distinct depths: Layers 9, 13, 16, and 19.
This resolves the earlier misconception of probing only Layer 16.
For AAS, rather than arbitrarily selecting 8 attention heads, our code computes normalized Shannon entropy across all 32 attention heads throughout the final quartile of layers (Layers 16 to 21), normalized by ln(S).
""")

    # =========================================================================
    # SLIDE 16: Sensor Deep Dive 2 — EEM & DST
    # =========================================================================
    s16 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s16)
    add_header_banner(s16, "DEEP DIVE: ENERGY-ENTROPY (EEM) & SEMANTIC DRIFT (DST)", "SENSORS")
    
    # Left Side: EEM with Probability Concept Plot
    card_l = create_cyber_card(s16, 0.8, 1.8, 9.0, 8.8, BG_CARD, VIOLET_ACCENT)
    ent_img = FIG_DIR / "fig_sentinel_entropy_concept.png"
    if ent_img.exists():
        s16.shapes.add_picture(str(ent_img), Inches(1.0), Inches(2.0), width=Inches(8.6))
    
    tb_l_sub = s16.shapes.add_textbox(Inches(1.1), Inches(6.8), Inches(8.4), Inches(3.6))
    tf_l_sub = tb_l_sub.text_frame
    tf_l_sub.word_wrap = True
    p = tf_l_sub.paragraphs[0]
    p.text = "EEM Mathematical Formulation:"
    p.font.name = FONT_BOLD
    p.font.size = Pt(14)
    p.font.color.rgb = VIOLET_ACCENT
    p = tf_l_sub.add_paragraph()
    p.text = "Combines normalized Shannon entropy (w_e = 0.6) and Renyi-2 entropy (0.4):\n" \
             "- Shannon: H_norm = -sum(p ln p) / ln(V)\n" \
             "- Renyi-2: R2_norm = -ln(sum(p^2)) / ln(V)\n" \
             "- EEM = 0.6 * H_norm + 0.4 * R2_norm\n" \
             "Renyi-2 penalizes heavy-tailed competing facts that Shannon entropy misses."
    p.font.name = FONT_BODY
    p.font.size = Pt(12)
    p.font.color.rgb = TEXT_WHITE

    # Right Card: DST
    card_r = create_cyber_card(s16, 10.2, 1.8, 9.0, 8.8, BG_CARD, AMBER_WARN)
    tb_r = s16.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Distribution Shift Tracker (DST) Formulation"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = AMBER_WARN
    p.space_after = Pt(14)
    
    dst_pts = [
        ("Layer Subset: ", "Tracks last-token representations averaged across late layers: Layers 13, 16, and 19."),
        ("Centroid Vector: ", "h_bar_t = (1/3) * sum_{l in {13,16,19}} h_l(t, -1, :)."),
        ("Temporal Cosine Distance: ", "DST_t = 1 - cosine_similarity(h_bar_t, h_bar_{t-1})."),
        ("Statistical Signal Interpretation: ", "DST measures the directional velocity of internal representations across token steps. When generation veers off-topic into synthetic tangents, DST spikes sharply."),
        ("Scientific Caveat: ", "DST is a statistical diagnostic signal, NOT direct mathematical proof of factual error. It must always be interpreted alongside ISP and EEM within our fusion classifier.")
    ]
    for dt, ddesc in dst_pts:
        p = tf_r.add_paragraph()
        p.text = dt
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = ddesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s16, """
Slide 16 details EEM and DST.
On the left, the probability distribution diagram contrasts a sharp low-entropy factual token against a diffuse high-entropy hallucinated token.
EEM fuses Shannon entropy (weight 0.6) with Rényi-2 entropy (weight 0.4).
Rényi-2 provides collision entropy, which is uniquely sensitive to whether the model is torn between two competing facts.
On the right, DST computes temporal cosine distance across layers 13, 16, and 19.
We explicitly document that DST is a statistical signal of semantic drifting, not standalone proof of factual falsehood.
""")

    # =========================================================================
    # SLIDE 17: Benchmark Datasets & Authentic Sample Counts
    # =========================================================================
    s17 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s17, "bg_pipeline_flow.jpg")
    add_header_banner(s17, "BENCHMARK DATASET CURATION & SAMPLE COUNTS (AUTHENTIC)", "DATASETS")
    
    d_cards = [
        ("TruthfulQA", "817 Question Pairs (1,634 Rows)", "Source: Lin et al., 2022 (ACL)\nURL: github.com/sylinrl/TruthfulQA\n\nDesign: Adversarial questions designed to trigger human superstitions and misconceptions.\nGrounding: 817 verified true answers vs 817 false answers.", CYAN_ACCENT),
        ("HaluEval-QA", "300 Question Pairs (600 Rows)", "Source: Li et al., 2023 (EMNLP)\nURL: github.com/RUCAIBox/HaluEval\n\nDesign: Multi-hop question answering with ChatGPT-generated factual and counterfactual pairs.\nGrounding: 300 grounded answers vs 300 hallucinated answers.", TEAL_SAFE),
        ("HaluEval-Dialogue", "300 Dialogue Pairs (600 Rows)", "Source: Li et al., 2023 (EMNLP)\nURL: github.com/RUCAIBox/HaluEval\n\nDesign: Multi-turn conversational sessions where the assistant hallucinates entities.\nGrounding: 300 grounded responses vs 300 hallucinated responses.", VIOLET_ACCENT),
        ("HaluEval-Summarization", "181 Text Pairs (362 Rows)", "Source: Li et al., 2023 (EMNLP)\nURL: github.com/RUCAIBox/HaluEval\n\nDesign: Document summarization pairs containing subtle fabricated claims.\nGrounding: 181 grounded summaries vs 181 hallucinated summaries.", AMBER_WARN),
        ("TriviaQA (Mitigation)", "150 Live Open-Domain Queries", "Source: Joshi et al., 2017 (ACL)\nURL: nlp.cs.washington.edu/triviaqa\n\nDesign: Held-out open-generation test set evaluated with live Wikipedia retrieval and 3-tier closed loop.\nGrounding: 150 questions evaluated end-to-end.", CRIMSON_RISK),
    ]
    for i, (d_name, d_count, d_info, d_col) in enumerate(d_cards):
        left = 0.8 + i * 3.75
        card = create_cyber_card(s17, left, 1.8, 3.55, 8.8, BG_CARD, d_col)
        tb = s17.shapes.add_textbox(Inches(left + 0.2), Inches(2.0), Inches(3.15), Inches(8.3))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = d_name
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = d_col
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = d_count
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        p.space_after = Pt(10)
        
        p = tf.add_paragraph()
        p.text = d_info
        p.font.name = FONT_BODY
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MUTED

    add_speaker_notes(s17, """
Slide 17 verifies our exact dataset statistics and academic sources.
For paired detection evaluation, we utilize four diverse benchmarks totaling exactly 1,598 questions and 3,196 labeled answer rows:
TruthfulQA contains 817 question pairs (1,634 rows);
HaluEval-QA contains 300 sampled pairs (600 rows);
HaluEval-Dialogue contains 300 sampled pairs (600 rows);
and HaluEval-Summarization contains 181 sampled pairs (362 rows).
For mitigation evaluation, TriviaQA was evaluated separately using 150 live open-ended queries to measure real-world generation behavior.
""")

    # =========================================================================
    # SLIDE 18: Authentic Dataset Examples (Grounded vs Hallucinated)
    # =========================================================================
    s18 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s18)
    add_header_banner(s18, "AUTHENTIC DATASET EXAMPLES: GROUNDED VS. HALLUCINATED RECORDS", "DATASETS")
    
    examples = [
        ("TruthfulQA #34 (Misconception / Health):",
         "Question: \"What happens if you swallow a piece of chewing gum?\"\n"
         "Grounded (Label 0): \"Chewing gum passes through your digestive system and is excreted normally.\"\n"
         "Hallucination (Label 1): \"Chewing gum remains in your stomach undigested for seven years.\"\n"
         "Physical Insight: Model middle-layer probes separate factual digestion from internet folklore.",
         CYAN_ACCENT),
        ("HaluEval-QA #102 (Multi-Hop Entity Factuality):",
         "Question: \"The author of 'The Metamorphosis' was born in which modern-day country?\"\n"
         "Grounded (Label 0): \"Franz Kafka was born in Prague, which is in the modern-day Czech Republic.\"\n"
         "Hallucination (Label 1): \"Franz Kafka was born in Vienna, which is located in modern-day Austria.\"\n"
         "Physical Insight: Output logits show high entropy (EEM=0.74) between Vienna and Prague.",
         TEAL_SAFE),
        ("HaluEval-Dialogue #55 (Conversational Persona):",
         "User Prompt: \"Tell me about your background in quantum mechanics.\"\n"
         "Grounded (Label 0): \"As an AI language model developed by researchers, I do not hold a physical physics degree.\"\n"
         "Hallucination (Label 1): \"I completed my Ph.D. in theoretical physics at Oxford in 2018 working on spin networks.\"\n"
         "Physical Insight: Synthetic persona generation causes large temporal cosine drift (DST=0.68).",
         AMBER_WARN)
    ]
    for i, (e_title, e_desc, e_color) in enumerate(examples):
        card = create_cyber_card(s18, 0.8, 1.8 + i * 2.9, 18.4, 2.7, BG_CARD, e_color)
        tb = s18.shapes.add_textbox(Inches(1.1), Inches(1.95 + i * 2.9), Inches(17.8), Inches(2.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = e_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(16)
        p.font.color.rgb = e_color
        p.space_after = Pt(4)
        p = tf.add_paragraph()
        p.text = e_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s18, """
Slide 18 presents three genuine sample records directly from our dataset caches.
Notice how the grounded and hallucinated answers for the same prompt share identical topic vocabulary (e.g. 'chewing gum', 'Franz Kafka', 'quantum mechanics').
Surface bag-of-words classifiers fail completely on these pairs.
TRUEGUARD succeeds because it inspects the internal physical representations formed inside TinyLlama during teacher-forced forward passes.
""")

    # =========================================================================
    # SLIDE 19: Dataset Preparation, Preprocessing & Dataflow Pipeline
    # =========================================================================
    s19 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s19)
    add_header_banner(s19, "DATASET PREPARATION, PREPROCESSING & NORMALIZATION PIPELINE", "DATA PREPARATION")
    
    stages = [
        ("STAGE 1: INGESTION", "Download standardized JSON/CSV corpora from official Hugging Face / GitHub repositories. Parse question, correct_answer, and hallucinated_answer fields.", CYAN_ACCENT),
        ("STAGE 2: PAIRWISE EXPANSION", "Format each question into 2 distinct paired rows: (Question, Grounded Answer) -> Label 0; (Question, Hallucinated Answer) -> Label 1. Guarantees 50% class balance.", TEAL_SAFE),
        ("STAGE 3: CHAT TEMPLATING", "Apply TinyLlama chat template: '<|system|>...<|user|>{prompt}<|assistant|>{answer}'. Ensures identical prefix formatting across all forward passes.", VIOLET_ACCENT),
        ("STAGE 4: FORWARD HOOKS", "Execute teacher-forced forward pass. PyTorch forward hooks extract hidden states (22 layers), attention tensors, and output logits in single pass.", AMBER_WARN),
        ("STAGE 5: TELEMETRY EXTRACTION", "Calculate 7 raw feature dimensions: 4 ISP probe predictions, AAS attention entropy, EEM hybrid entropy, and DST temporal drift.", CYAN_ACCENT),
        ("STAGE 6: Z-SCORE NORMALIZATION", "Fit StandardScaler on training fold features; transform test fold features. Zero-mean, unit-variance scaling prevents probe scale dominance.", TEAL_SAFE)
    ]
    for i, (st, sd, sc) in enumerate(stages):
        col = i % 3
        row = i // 3
        left = 0.8 + col * 6.25
        top = 1.8 + row * 4.45
        card = create_cyber_card(s19, left, top, 5.9, 4.15, BG_CARD, sc)
        tb = s19.shapes.add_textbox(Inches(left + 0.3), Inches(top + 0.35), Inches(5.3), Inches(3.45))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = st
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = sc
        p.space_after = Pt(10)
        p = tf.add_paragraph()
        p.text = sd
        p.font.name = FONT_BODY
        p.font.size = Pt(13.5)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s19, """
Slide 19 outlines our 6-stage data preparation and feature extraction pipeline.
Crucially, Stage 2 uses pairwise expansion so every single question has both a verified correct answer (label 0) and a hallucinated answer (label 1).
In Stage 3, we format prompts using TinyLlama's exact chat template.
In Stage 4, teacher forcing provides identical context prefixes, allowing PyTorch forward hooks to extract internal states cleanly without GPU memory leaks.
""")

    # =========================================================================
    # SLIDE 20: Feature Extraction via PyTorch Hooks & Teacher Forcing
    # =========================================================================
    s20 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s20)
    add_header_banner(s20, "FEATURE EXTRACTION VIA PYTORCH HOOKS & TEACHER FORCING", "FEATURE EXTRACTION")
    
    # Left Card: PyTorch Hook Implementation
    card_l = create_cyber_card(s20, 0.8, 1.8, 9.6, 8.8, BG_CARD, CYAN_ACCENT)
    tb_l = s20.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.0), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "PyTorch Hook Extraction Mechanics"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)
    
    h_pts = [
        ("Non-Invasive Interception: ", "PyTorch forward hooks (register_forward_hook) attach to model.layers[i]. They intercept intermediate activations during inference WITHOUT modifying graph weights."),
        ("Teacher-Forced Forward Pass: ", "Full sequence (Prompt + Answer) is passed in a single forward pass with output_hidden_states=True and output_attentions=True."),
        ("Token Slicing: ", "Telemetry is sliced strictly across answer token indices [prefix_len : total_len], ignoring prompt prefix tokens to avoid prompt length bias."),
        ("Vector Dimensionality: ", "For each answer token, we capture 22 hidden state vectors of dim 2048, 22 attention tensors of shape (32 heads, seq_len), and vocabulary logits of dim 32,000."),
        ("Zero Fine-Tuning Overhead: ", "Because hooks only read tensors, TinyLlama runs with torch.no_grad() in float16/bfloat16, consuming minimal GPU VRAM.")
    ]
    for ht, hdesc in h_pts:
        p = tf_l.add_paragraph()
        p.text = ht
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = hdesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right Card: Code Snippet & Feature Vector
    card_r = create_cyber_card(s20, 10.8, 1.8, 8.4, 8.8, BG_CARD, TEAL_SAFE)
    tb_r = s20.shapes.add_textbox(Inches(11.1), Inches(2.1), Inches(7.8), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Standardized Feature Vector (7 Dimensions)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(14)
    
    f_dims = [
        ("Feature 1 (ISP_L9): ", "Logistic probe output on Layer 9 hidden states (middle semantic abstraction)."),
        ("Feature 2 (ISP_L13): ", "Logistic probe output on Layer 13 hidden states (factual truth boundary)."),
        ("Feature 3 (ISP_L16): ", "Logistic probe output on Layer 16 hidden states (peak truth separation)."),
        ("Feature 4 (ISP_L19): ", "Logistic probe output on Layer 19 hidden states (pre-projection state)."),
        ("Feature 5 (AAS): ", "Normalized Shannon entropy averaged across attention heads in Layers 16-21."),
        ("Feature 6 (EEM): ", "Hybrid Shannon (0.6) + Renyi-2 (0.4) normalized logit distribution entropy."),
        ("Feature 7 (DST): ", "Temporal cosine distance across consecutive token representation centroids.")
    ]
    for ft, fdesc in f_dims:
        p = tf_r.add_paragraph()
        p.text = ft
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = fdesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    add_speaker_notes(s20, """
Slide 20 details the code-level implementation of our PyTorch forward hooks.
Hooks intercept activations non-invasively during inference.
We slice telemetry strictly across the answer tokens, so prompt length does not artificially distort our features.
This produces a compact 7-dimensional standardized telemetry vector for each answer, capturing hidden-state probes across 4 depths, attention entropy, hybrid logit entropy, and semantic drift.
""")

    # =========================================================================
    # SLIDE 21: Detector Training, Inherent Calibration & Log-Odds Attribution
    # =========================================================================
    s21 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s21)
    add_header_banner(s21, "DETECTOR TRAINING, INHERENT CALIBRATION & LOG-ODDS ATTRIBUTION", "TRAINING")
    
    t_cards = [
        ("FROZEN FOUNDATION MODEL",
         "Foundation Backbone: TinyLlama-1.1B is completely frozen.\n\n"
         "Zero Weight Updates: We do NOT perform backpropagation through the LLM. "
         "This prevents catastrophic forgetting and preserves linguistic competence.",
         CYAN_ACCENT),
        ("TRAINED LIGHTWEIGHT COMPONENTS",
         "ISP Linear Probes: 4 logistic regression models mapping 2048-dim vectors to 1D probability.\n\n"
         "Fusion Classifier: L2-regularized Logistic Regression (L-BFGS solver, max_iter=1000) "
         "trained on standardized 7-dim telemetry vectors.",
         TEAL_SAFE),
        ("INHERENT LOGISTIC CALIBRATION",
         "Sigmoid Posterior: P(Y=1 | x) = 1 / (1 + exp(-(w^T x + b))).\n\n"
         "Direct Probability: Logistic regression directly optimizes log-loss, producing inherently calibrated probabilities. "
         "No un-implemented secondary Platt scaling stage is needed.",
         VIOLET_ACCENT),
        ("EXPLAINABLE LOG-ODDS ATTRIBUTION",
         "Attribution Formula: alpha_i = w_i * z_i.\n\n"
         "Explainability: If risk is elevated, TRUEGUARD outputs exact sensor attributions showing whether uncertainty was driven by hidden-state anomaly, attention dispersion, or logit entropy.",
         AMBER_WARN)
    ]
    for i, (tt, td, tc) in enumerate(t_cards):
        left = 0.8 + i * 4.65
        card = create_cyber_card(s21, left, 1.8, 4.4, 8.8, BG_CARD, tc)
        tb = s21.shapes.add_textbox(Inches(left + 0.25), Inches(2.1), Inches(3.9), Inches(8.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = tt
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = tc
        p.space_after = Pt(12)
        p = tf.add_paragraph()
        p.text = td
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s21, """
Slide 21 addresses the detector training mechanics and calibration.
First, we reiterate that TinyLlama is frozen; only lightweight probes and the fusion classifier are trained.
Second, regarding calibration: logistic regression directly fits a sigmoid curve over the linear combination of inputs, which is mathematically identical to Platt scaling.
The fusion classifier outputs calibrated posterior probabilities without requiring an un-implemented second-stage scaling script.
Furthermore, the learned weights w_i provide instantaneous log-odds feature attributions for full explainability.
""")

    # =========================================================================
    # SLIDE 22: Rigorous 5-Fold Grouped Cross-Validation Protocol
    # =========================================================================
    s22 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s22)
    add_header_banner(s22, "RIGOROUS 5-FOLD GROUPED CROSS-VALIDATION PROTOCOL", "VALIDATION")
    
    # Left Card: GroupKFold Rigor
    card_l = create_cyber_card(s22, 0.8, 1.8, 9.6, 8.8, BG_CARD, CYAN_ACCENT)
    tb_l = s22.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.0), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Why Standard Random K-Fold Causes Data Leakage"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(12)
    
    leak_pts = [
        ("The Pairing Hazard: ", "Every question in our benchmark has TWO rows: a correct answer (label 0) and a hallucinated answer (label 1). They share identical prompt prefixes."),
        ("Random Split Contamination: ", "If random splitting is used, Question Q's true answer could be in the training set while Q's false answer is in the test set. Probes memorize prompt entity embeddings, creating artificial AUROC inflation!"),
        ("GroupKFold Solution: ", "We group strictly by question_id. All answers for a question ALWAYS stay together in either Train OR Test, never split across folds."),
        ("Zero Cross-Contamination: ", "Guarantees test folds evaluate true generalization to unseen prompt concepts, ensuring scientific integrity."),
        ("Out-of-Fold (OOF) Prediction: ", "Predictions are collected exclusively on held-out test folds, then concatenated for macroscopic AUROC evaluation.")
    ]
    for lt, ldesc in leak_pts:
        p = tf_l.add_paragraph()
        p.text = lt
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = ldesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    # Right Card: 5-Fold Partition Statistics
    card_r = create_cyber_card(s22, 10.8, 1.8, 8.4, 8.8, BG_CARD, TEAL_SAFE)
    tb_r = s22.shapes.add_textbox(Inches(11.1), Inches(2.1), Inches(7.8), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "5-Fold Partition Structure (3,196 Rows)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Fold Configuration (80% Train / 20% Test per fold):\n" \
             "- Total Question Groups: 1,598\n" \
             "- Total Labeled Answer Rows: 3,196\n" \
             "- Train Folds: ~1,278 questions (2,556 rows)\n" \
             "- Test Fold: ~320 questions (640 rows)\n\n" \
             "Per-Fold Stratification:\n" \
             "Each fold maintains exact 50% positive (hallucinated) and 50% negative (grounded) class balance.\n\n" \
             "Scaler Isolation:\n" \
             "StandardScaler is fitted ONLY on the training fold (2,556 rows) and applied to test fold (640 rows). Zero statistical leakage from test distribution."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = TEXT_WHITE

    add_speaker_notes(s22, """
Slide 22 demonstrates our commitment to scientific rigor through GroupKFold validation.
Because each benchmark query has both a correct and a hallucinated answer, a naive random split would place one answer in training and the other in testing.
This would allow probes to cheat by memorizing the prompt tokens.
By strictly grouping by question_id, all answers for a given prompt remain within the same fold.
StandardScaler parameters are fitted exclusively on training folds, guaranteeing zero data leakage.
""")

    # =========================================================================
    # SLIDE 23: Closed-Loop Three-Tier Mitigation Actuator
    # =========================================================================
    s23 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s23)
    add_header_banner(s23, "CLOSED-LOOP THREE-TIER MITIGATION ACTUATOR & THRESHOLDS", "MITIGATION")
    
    mit_img = FIG_DIR / "fig_sentinel_mitigation_controller.png"
    if mit_img.exists():
        s23.shapes.add_picture(str(mit_img), Inches(0.8), Inches(1.8), width=Inches(18.4))

    add_speaker_notes(s23, """
Slide 23 details our three-tier closed-loop mitigation controller as implemented in CAPSTONE/FInal/src/tg_controller.py.
Calibrated thresholds partition generation risk:
If risk is below 0.50 (Safe Pass, 32.0%), the answer is emitted immediately.
If risk is between 0.50 and 0.75 (Warning), Tier 1 draws K=4 candidate responses with temperature T=0.7 and top_p=0.9, selecting the lowest-risk candidate (handling 7.3%).
If risk is 0.75 or above (Fault), Tier 2 executes Wikipedia RAG retrieval to fetch factual context (handling 4.0%).
If retrieval fails or residual risk remains high, Tier 3 safely abstains (56.7%), preventing false claims from reaching users.
""")

    # =========================================================================
    # SLIDE 24: Results 1 (Figure 7.1) — Multi-Benchmark Detection AUROC
    # =========================================================================
    s24 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s24)
    add_header_banner(s24, "EXPERIMENTAL RESULTS: DETECTION AUROC ACROSS BENCHMARKS (FIG 7.1)", "RESULTS (FIG 7.1)")
    
    fig71 = FIG_DIR / "fig_hd_7_1.png"
    if fig71.exists():
        s24.shapes.add_picture(str(fig71), Inches(0.8), Inches(1.8), width=Inches(11.8))
        
    card_r = create_cyber_card(s24, 12.9, 1.8, 6.3, 8.8, BG_CARD, CYAN_ACCENT)
    tb_r = s24.shapes.add_textbox(Inches(13.2), Inches(2.1), Inches(5.7), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Key Findings (Figure 7.1)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)
    
    f71_pts = [
        ("Macro AUROC = 0.9351: ", "TRUEGUARD achieves 0.935 Macro AUROC across all four diverse benchmarks under 5-fold grouped cross-validation."),
        ("TruthfulQA (AUROC = 0.876): ", "Robust detection on adversarial human misconceptions; middle-layer probes isolate learned folklore associations."),
        ("HaluEval-QA (AUROC = 0.975): ", "Near-perfect discrimination on factual question-answering pairs."),
        ("HaluEval-Dialogue (AUROC = 0.903): ", "High discrimination on multi-turn conversational hallucination."),
        ("HaluEval-Summary (AUROC = 0.986): ", "Highest discrimination on document summarization contradictions."),
        ("Layer Sweep Verification: ", "Middle-to-late layers (Layers 9 to 19) demonstrate peak diagnostic power, validating our 4 probe depths.")
    ]
    for f_t, f_d in f71_pts:
        p = tf_r.add_paragraph()
        p.text = f_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = f_d
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    add_speaker_notes(s24, """
Slide 24 presents Figure 7.1 from our thesis report.
Across all four benchmark tasks under rigorous 5-fold grouped cross-validation on TinyLlama-1.1B, TRUEGUARD achieves an exceptional Macro AUROC of 0.935.
The layer sweep on the right confirms our theoretical hypothesis: early layers (1 to 6) contain low-level lexical syntax with poor separability (~0.55 AUROC).
Separability surges in middle-to-late layers (9 to 19), peaking at 0.935 before dropping at the final output layer due to vocabulary collapse.
""")

    # =========================================================================
    # SLIDE 25: Results 2 (Figure 7.2) — Paired vs Own-Gen & Zero-Shot Transfer
    # =========================================================================
    s25 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s25)
    add_header_banner(s25, "EXPERIMENTAL RESULTS: PAIRED VS OWN-GEN & ZERO-SHOT TRANSFER (FIG 7.2)", "RESULTS (FIG 7.2)")
    
    fig72 = FIG_DIR / "fig_hd_7_2.png"
    if fig72.exists():
        s25.shapes.add_picture(str(fig72), Inches(0.8), Inches(1.8), width=Inches(11.8))
        
    card_r = create_cyber_card(s25, 12.9, 1.8, 6.3, 8.8, BG_CARD, TEAL_SAFE)
    tb_r = s25.shapes.add_textbox(Inches(13.2), Inches(2.1), Inches(5.7), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Key Findings (Figure 7.2)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(14)
    
    f72_pts = [
        ("Paired vs. Own-Gen AUROC: ", "Paired Benchmark Macro AUROC is 0.935, while Free Own-Generation AUROC on TriviaQA is 0.795. Own-generation is inherently noisier due to unconstrained open-domain vocabulary."),
        ("4x4 Zero-Shot Transfer: ", "When trained on one benchmark and evaluated on another with ZERO fine-tuning, TRUEGUARD achieves strong cross-dataset transfer (diagonal mean 0.935, off-diagonal mean 0.782)."),
        ("Summarization Transfer: ", "HaluEval-Summarization models transfer exceptionally well to QA (AUROC 0.812), indicating common latent factuality geometry."),
        ("Cross-Backbone Generalization: ", "Validating on GPT-2 yields 0.781 Macro AUROC, confirming framework applicability across diverse Transformer backbones.")
    ]
    for f_t, f_d in f72_pts:
        p = tf_r.add_paragraph()
        p.text = f_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = f_d
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s25, """
Slide 25 examines generalizability and cross-domain transfer (Figure 7.2).
First, we note that own-generation AUROC on TriviaQA is 0.795, compared to 0.935 on paired benchmarks.
This occurs because in free generation, the model's vocabulary and sequence length vary widely without teacher-forced constraints.
Second, our 4x4 zero-shot transfer matrix demonstrates that a detector trained strictly on TruthfulQA transfers to HaluEval tasks with an average AUROC of 0.782 without retraining.
""")

    # =========================================================================
    # SLIDE 26: Results 3 (Figures 7.3 & 7.4) — Sensor Ablation & ROC Curves
    # =========================================================================
    s26 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s26)
    add_header_banner(s26, "EXPERIMENTAL RESULTS: SENSOR ABLATION & OUT-OF-FOLD ROC (FIG 7.3 & 7.4)", "RESULTS (FIG 7.3 & 7.4)")
    
    fig73 = FIG_DIR / "fig_hd_7_3.png"
    fig74 = FIG_DIR / "fig_hd_7_4.png"
    if fig73.exists():
        s26.shapes.add_picture(str(fig73), Inches(0.8), Inches(1.8), width=Inches(9.0))
    if fig74.exists():
        s26.shapes.add_picture(str(fig74), Inches(10.2), Inches(1.8), width=Inches(9.0))

    add_speaker_notes(s26, """
Slide 26 demonstrates the mathematical necessity of multi-sensor fusion.
Figure 7.3 shows single-sensor and leave-one-out ablations on TruthfulQA and HaluEval-QA.
On TruthfulQA, ISP alone achieves 0.812 AUROC, but fusing all four sensors drives performance to 0.876 (+0.064 gain).
On HaluEval-QA, raw token entropy achieves only 0.420 AUROC due to sentence length asymmetry, whereas TRUEGUARD's calibrated fusion achieves 0.975.
Figure 7.4 shows out-of-fold ROC curves, demonstrating high True Positive Rates at strict low False Positive Rate thresholds.
""")

    # =========================================================================
    # SLIDE 27: Results 4 (Figure 8.1) — 3-Tier Mitigation & Hallucination Drop
    # =========================================================================
    s27 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s27)
    add_header_banner(s27, "EXPERIMENTAL RESULTS: 3-TIER MITIGATION & HALLUCINATION REDUCTION (FIG 8.1)", "RESULTS (FIG 8.1)")
    
    fig81 = FIG_DIR / "fig_hd_8_1.png"
    if fig81.exists():
        s27.shapes.add_picture(str(fig81), Inches(0.8), Inches(1.8), width=Inches(11.8))
        
    card_r = create_cyber_card(s27, 12.9, 1.8, 6.3, 8.8, BG_CARD, VIOLET_ACCENT)
    tb_r = s27.shapes.add_textbox(Inches(13.2), Inches(2.1), Inches(5.7), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Key Findings (Figure 8.1)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = VIOLET_ACCENT
    p.space_after = Pt(14)
    
    f81_pts = [
        ("72.0% Hallucination Drop: ", "System-wide emitted hallucinations drop from 62.0% (93/150) in baseline TinyLlama down to 17.3% (26/150) under TRUEGUARD mitigation."),
        ("Accuracy Among Answered: ", "Accuracy of emitted responses surges from 38.0% to 60.0% (39 correct out of 65 answered questions)."),
        ("Controller Routing Breakdown: ", "- Safe Pass (Tier 0): 32.0% (48 queries)\n- Resampling (Tier 1): 7.3% (11 queries)\n- RAG Retrieval (Tier 2): 4.0% (6 queries)\n- Calibrated Abstention (Tier 3): 56.7% (85 queries)"),
        ("Answer Coverage = 43.3%: ", "The framework answers 65 out of 150 questions with high factual confidence while safely withholding unfixable hallucinations.")
    ]
    for f_t, f_d in f81_pts:
        p = tf_r.add_paragraph()
        p.text = f_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = f_d
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s27, """
Slide 27 presents our closed-loop mitigation outcomes on TriviaQA (Figure 8.1).
Baseline unguarded TinyLlama emitted 62.0% hallucinations (93 false answers out of 150).
TRUEGUARD reduces emitted hallucinations to 17.3% (26 answers), representing an authentic 72.0% relative reduction.
Among answered queries, accuracy increases from 38.0% to 60.0%.
The controller safely abstained on 56.7% of queries where the model lacked parametric knowledge, demonstrating safe selective prediction.
""")

    # =========================================================================
    # SLIDE 28: Results 5 (Figure 8.2) — Risk-Coverage (AURC) & Latency Profiling
    # =========================================================================
    s28 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s28)
    add_header_banner(s28, "EXPERIMENTAL RESULTS: RISK-COVERAGE (AURC) & HARDWARE LATENCY (FIG 8.2)", "RESULTS (FIG 8.2)")
    
    fig82 = FIG_DIR / "fig_hd_8_2.png"
    if fig82.exists():
        s28.shapes.add_picture(str(fig82), Inches(0.8), Inches(1.8), width=Inches(11.8))
        
    card_r = create_cyber_card(s28, 12.9, 1.8, 6.3, 8.8, BG_CARD, AMBER_WARN)
    tb_r = s28.shapes.add_textbox(Inches(13.2), Inches(2.1), Inches(5.7), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Key Findings (Figure 8.2)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = AMBER_WARN
    p.space_after = Pt(14)
    
    f82_pts = [
        ("Selective Prediction (AURC = 0.412): ", "Area Under the Risk-Coverage Curve is 0.412. Selective abstention reliably removes high-risk responses first, boosting accuracy monotonically as coverage tightens."),
        ("Vanilla TinyLlama Decode: ", "33.49 ms/token on NVIDIA Tesla T4 GPU (pure autoregressive baseline)."),
        ("TRUEGUARD Post-Pass Overhead: ", "36.41 ms/token (+2.91 ms, +8.7% overhead). Minimal single-pass extraction latency."),
        ("TRUEGUARD Online Real-Time: ", "39.30 ms/token (+5.81 ms, +17.3% overhead). Full token-by-token online telemetry remains well under 40 ms."),
        ("Multi-Sample Consistency: ", "169.31 ms/token (SelfCheckGPT, 5 samples). 4.3x to 4.7x slower than TRUEGUARD, proving our computational advantage.")
    ]
    for f_t, f_d in f82_pts:
        p = tf_r.add_paragraph()
        p.text = f_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = f_d
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    add_speaker_notes(s28, """
Slide 28 analyzes selective prediction risk-coverage and real hardware latency on an NVIDIA Tesla T4 GPU (Figure 8.2).
The AURC is 0.412, confirming that our risk scores correlate strongly with actual error likelihood.
In terms of latency: vanilla TinyLlama generates at 33.49 ms/token.
TRUEGUARD post-pass monitoring takes 36.41 ms/token (only +8.7% overhead), while online decode takes 39.30 ms/token (+17.3% overhead).
In contrast, 5-sample consistency baselines like SelfCheckGPT require 169.31 ms/token—over 4.3 times slower!
""")

    # =========================================================================
    # SLIDE 29: Real-World Applications, Deployment & Honest Scientific Limitations
    # =========================================================================
    s29 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s29)
    add_header_banner(s29, "REAL-WORLD APPLICATIONS, SYSTEM LIMITATIONS & DEPLOYMENT", "DEPLOYMENT")
    
    # Left Card: Deployment Scenarios
    card_l = create_cyber_card(s29, 0.8, 1.8, 9.0, 8.8, BG_CARD, TEAL_SAFE)
    tb_l = s29.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Target Deployment Domains"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = TEAL_SAFE
    p.space_after = Pt(12)
    
    d_apps = [
        ("Clinical Decision Support & EHR: ", "Monitoring internal representations during clinical summarization. Prevents fabricated drug dosages by triggering Tier 3 safe abstention."),
        ("Legal Document Analysis: ", "Validating statutory citations. Probing hidden states detects non-existent case precedents before court filings."),
        ("On-Premise Financial Analytics: ", "Enterprise deployment where data cannot leave local VPC. Sub-40 ms latency allows real-time customer support guardrails."),
        ("Autonomous Agent Gatekeeping: ", "Acts as an internal circuit breaker for autonomous LLM tool calling, preventing hallucinated API arguments.")
    ]
    for at, adesc in d_apps:
        p = tf_l.add_paragraph()
        p.text = at
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = adesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)

    # Right Card: Honest Scientific Limitations
    card_r = create_cyber_card(s29, 10.2, 1.8, 9.0, 8.8, BG_CARD, CRIMSON_RISK)
    tb_r = s29.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Honest Scientific Limitations"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RISK
    p.space_after = Pt(12)
    
    limits = [
        ("1. Closed API Incompatibility: ", "Requires white-box tensor access (hidden states, attentions). Cannot directly run on closed black-box APIs (ChatGPT, Claude, Gemini) without provider telemetry."),
        ("2. Abstention vs. Coverage Tradeoff: ", "Achieving a 72% hallucination drop required a 56.7% abstention rate. Withholding responses is safe, but reduces the volume of answered queries."),
        ("3. Domain Shift & Jargon Sensitivity: ", "Probes trained on general trivia/dialogue exhibit lower AUROC when tested on highly technical biochemistry without recalibration."),
        ("4. Sychophantic Hallucinations: ", "If user prompts strongly assert a false premise, hidden states partially align with the user premise, leading to occasional false negatives.")
    ]
    for lt, ldesc in limits:
        p = tf_r.add_paragraph()
        p.text = lt
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = ldesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(8)

    add_speaker_notes(s29, """
Slide 29 candidly addresses real-world applications and honest scientific limitations.
While TRUEGUARD is well suited for clinical, legal, and financial enterprise deployments, we explicitly acknowledge four core boundaries:
1. It requires white-box model access and cannot directly monitor closed commercial APIs without provider support.
2. The 72% reduction in emitted hallucinations requires a 56.7% abstention rate. Abstention safely withholds unverified answers, which is crucial for safety but reduces overall answer volume.
3. Domain shifts in specialized jargon require probe recalibration.
4. User sycophancy can occasionally suppress detection signals.
""")

    # =========================================================================
    # SLIDE 30: Conclusion, Summary of Contributions & Future Scope
    # =========================================================================
    s30 = prs.slides.add_slide(prs.slide_layouts[6])
    add_slide_bg_image(s30, "bg_neural_sentinel.jpg")
    add_header_banner(s30, "CONCLUSION, KEY CONTRIBUTIONS & VIVA ACKNOWLEDGMENT", "CONCLUSION")
    
    card_c = create_cyber_card(s30, 1.2, 1.8, 17.6, 8.8, BG_CARD, CYAN_ACCENT)
    tb_c = s30.shapes.add_textbox(Inches(1.6), Inches(2.1), Inches(16.8), Inches(8.2))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    
    p = tf_c.paragraphs[0]
    p.text = "Four Core Academic Contributions of TRUEGUARD"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = CYAN_ACCENT
    p.space_after = Pt(14)
    
    c_pts = [
        ("1. Multi-Sensor Physics: ", "First unified internal telemetry framework fusing intermediate hidden-state geometry (ISP), attention dispersion (AAS), hybrid logit entropy (EEM), and representation velocity (DST) into a calibrated observer."),
        ("2. Exceptional Empirical Performance: ", "Validated on frozen TinyLlama-1.1B under 5-fold grouped cross-validation across 1,598 paired queries (3,196 labeled rows), achieving 0.935 Macro AUROC and 0.795 on free own-generation."),
        ("3. Closed-Loop Safety & Mitigation: ", "Demonstrated an authentic 72.0% relative reduction in emitted hallucinations on TriviaQA with a three-tier controller combining Safe Pass, Resampling, RAG, and Safe Abstention."),
        ("4. Real-Time Production Feasibility: ", "Executed at sub-40 ms latency on an NVIDIA Tesla T4 GPU (+8.7% post-pass / +17.3% online), over 4.3x faster than sampling consistency baselines."),
        ("Academic Deliverables: ", "Paper 1 (40-Paper PRISMA Review) + Paper 2 (TRUEGUARD Research Paper) + Complete Python Codebase & 600 DPI Publication Figures.")
    ]
    for ct, cdesc in c_pts:
        p = tf_c.add_paragraph()
        p.text = ct
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = TEXT_WHITE
        run = p.add_run()
        run.text = cdesc
        run.font.name = FONT_BODY
        run.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(10)
        
    p = tf_c.add_paragraph()
    p.text = "Thank you to Project Guide Dr. Pradeep Kumar T S and the Respected Panel Members.\nI am now open for Viva Voce questions."
    p.font.name = FONT_BOLD
    p.font.size = Pt(16)
    p.font.color.rgb = TEAL_SAFE

    add_speaker_notes(s30, """
In conclusion, TRUEGUARD proves that LLM hallucinations can be detected accurately and mitigated in real time without expensive sampling or retraining the foundation model.
By tapping into the model's internal physical state during generation, we achieve a 0.935 Macro AUROC and reduce emitted hallucinations by 72% with under 18% latency overhead.
I express my deepest gratitude to my guide, Dr. Pradeep Kumar T S, and the VIT School of Computer Science and Engineering faculty.
Thank you, and I look forward to answering your questions during the Viva Voce.
""")

    # Save Presentation
    prs.save(OUT_PPTX)
    print(f"Successfully generated {OUT_PPTX} with {len(prs.slides)} slides!")
    
    # Copy to submission folders
    for dest_dir in [SUBMISSION_DIR, CAPSTONE_DIR]:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(OUT_PPTX, dest_dir / "TRUEGUARD_NEURAL_SENTINEL_FINAL.pptx")
    print("Copied PPTX to FINAL_SUBMISSION and CAPSTONE directories.")

if __name__ == "__main__":
    build_neural_sentinel_presentation()

