# -*- coding: utf-8 -*-
"""
Generates the 32-Slide Final Review Presentation (FINAL_PRESENTATION.pptx & .pdf)
for TRUEGUARD (Yogesh Ravi M, 22MIA1052, Guide: Dr. Pradeep Kumar T S),
strictly following the visual design pattern, layout structure, high-contrast
peach/amber tables, white-bordered frames, golden titles, and experimental
interface screenshots of Sandhya's reference presentation.
"""

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

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT_DIR = Path(r"E:\trueguard")
CAPSTONE_DIR = ROOT_DIR / "CAPSTONE"
FINAL_DIR = CAPSTONE_DIR / "FInal"
SUBMISSION_DIR = ROOT_DIR / "FINAL_SUBMISSION"
ASSETS_DIR = FINAL_DIR / "assets_sandhya_style"
FIG_DIR = ROOT_DIR / "outputs" / "figures"

OUT_PPTX = SUBMISSION_DIR / "FINAL_PRESENTATION.pptx"
OUT_PDF = SUBMISSION_DIR / "FINAL_PRESENTATION.pdf"

# ---------------------------------------------------------------------------
# Original TRUEGUARD "Neural-Glass & Royal-Indigo / Emerald" Color & Font Theme
# ---------------------------------------------------------------------------
GOLD_TITLE = RGBColor(29, 78, 216)      # #1D4ED8 - Royal Cobalt Subheadings & Prefixes on White Cards
HERO_GOLD = RGBColor(251, 191, 36)      # #FBBF24 - Warm Amber-Gold Hero Title on Dark Title Slide
WHITE = RGBColor(255, 255, 255)         # #FFFFFF - Crisp White Header Banner Text
INK_SLATE = RGBColor(15, 23, 42)        # #0F172A - Deep Ink-Slate Body Text on White Cards
BADGE_DARK = RGBColor(15, 23, 42)       # #0F172A - Deep Obsidian Pill Badge
CHARCOAL = RGBColor(15, 23, 42)         # #0F172A - Dark Ink Text inside Ice-Blue Tables
CYAN_ACCENT = RGBColor(4, 120, 87)      # #047857 - Deep Emerald Highlight Text on White Cards
HERO_CYAN = RGBColor(56, 189, 248)      # #38BDF8 - Glowing Cyan on Dark Hero Slide

# High-Contrast Royal-Indigo & Ice-Blue Table Colors
TBL_HEADER_PEACH = RGBColor(30, 58, 138)    # #1E3A8A - Royal Indigo Table Header
TBL_ROW_LIGHT = RGBColor(239, 246, 255)     # #EFF6FF - Soft Ice-Blue Row
TBL_ROW_MED = RGBColor(255, 255, 255)       # #FFFFFF - Pure Crisp White Row
TBL_HEADER_ORANGE = RGBColor(6, 95, 70)     # #065F46 - Deep Emerald Metrics Table Header

FONT_TITLE = "Trebuchet MS"
FONT_SANS = "Segoe UI"
FONT_SERIF = "Segoe UI Semibold"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def set_bg_image(slide, img_name):
    img_path = ASSETS_DIR / img_name
    if img_path.exists():
        slide.shapes.add_picture(str(img_path), Inches(0), Inches(0), width=Inches(20.0), height=Inches(11.25))


def set_cell_borders(cell, color_hex="93C5FD", width_emu=14000):
    tcPr = cell._tc.get_or_add_tcPr()
    for tag in ("a:lnL", "a:lnR", "a:lnT", "a:lnB"):
        el = tcPr.find(
            f"{{{tcPr.nsmap.get('a', 'http://schemas.openxmlformats.org/drawingml/2006/main')}}}{tag.split(':')[1]}"
        )
        if el is not None:
            tcPr.remove(el)
    for tag in ("lnL", "lnR", "lnT", "lnB"):
        ln = parse_xml(
            f'<a:{tag} {nsdecls("a")} w="{width_emu}" cap="flat" cmpd="sng" algn="ctr">'
            f'<a:solidFill><a:srgbClr val="{color_hex}"/></a:solidFill>'
            f'<a:prstDash val="solid"/>'
            f'</a:{tag}>'
        )
        tcPr.append(ln)


def set_cell_margins(cell, left=0.14, right=0.14, top=0.10, bottom=0.10):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.set("marL", str(int(Inches(left))))
    tcPr.set("marR", str(int(Inches(right))))
    tcPr.set("marT", str(int(Inches(top))))
    tcPr.set("marB", str(int(Inches(bottom))))


def add_gold_title(slide, text, left=0.65, top=0.20, width=14.2, size=42, align=PP_ALIGN.LEFT):
    """Places a crisp white bold title inside the top Royal-Indigo header banner."""
    tb = slide.shapes.add_textbox(Inches(0.65), Inches(0.18), Inches(14.2), Inches(1.15))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    r = p.add_run()
    r.text = text.upper()
    r.font.name = FONT_TITLE
    r.font.size = Pt(min(size, 44))
    r.font.bold = True
    r.font.color.rgb = WHITE
    return tb


def add_white_bullets(slide, left, top, width, height, items, default_size=25.0, line_spacing=1.22):
    """Renders high-contrast Deep Ink-Slate & Royal-Cobalt bullets inside the elevated white card."""
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for idx, item in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.line_spacing = line_spacing
        if isinstance(item, str):
            p.space_after = Pt(16)
            r = p.add_run()
            r.text = item
            r.font.name = FONT_SANS
            r.font.size = Pt(default_size + 0.5)
            r.font.bold = True
            r.font.color.rgb = INK_SLATE
        elif isinstance(item, dict):
            p.space_after = Pt(item.get("space_after", 14))
            sz = item.get("size", default_size) + 0.5
            if "title" in item:
                rt = p.add_run()
                rt.text = item["title"] + "\n"
                rt.font.name = FONT_TITLE
                rt.font.size = Pt(item.get("title_size", sz + 2.5))
                rt.font.bold = True
                rt.font.underline = item.get("underline", False)
                t_col = item.get("title_color", GOLD_TITLE)
                if t_col == WHITE:
                    t_col = GOLD_TITLE
                rt.font.color.rgb = t_col
            if "bold_prefix" in item:
                rp = p.add_run()
                rp.text = item["bold_prefix"]
                rp.font.name = FONT_SANS
                rp.font.size = Pt(sz)
                rp.font.bold = True
                rp.font.color.rgb = item.get("prefix_color", GOLD_TITLE)
            rb = p.add_run()
            rb.text = item.get("text", "")
            rb.font.name = FONT_SANS
            rb.font.size = Pt(sz)
            rb.font.bold = item.get("bold", False)
            b_col = item.get("color", INK_SLATE)
            if b_col == WHITE:
                b_col = INK_SLATE
            rb.font.color.rgb = b_col
    return tb


def add_peach_table(
    slide,
    left,
    top,
    width,
    height,
    headers,
    rows,
    col_widths,
    header_size=21.5,
    cell_size=19.8,
    header_bg=TBL_HEADER_PEACH,
    font_name=FONT_SANS,
    bold_cols=(),
):
    shape = slide.shapes.add_table(
        len(rows) + 1,
        len(headers),
        Inches(left),
        Inches(top),
        Inches(width),
        Inches(height),
    )
    table = shape.table
    table.first_row = False
    table.horz_banding = False

    for c_idx, w in enumerate(col_widths):
        table.columns[c_idx].width = Inches(w)

    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_bg
        set_cell_margins(cell, left=0.14, right=0.14, top=0.10, bottom=0.10)
        set_cell_borders(cell, "1E40AF", 16000)
        tf = cell.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = h_text
        r.font.name = FONT_TITLE
        r.font.size = Pt(header_size)
        r.font.bold = True
        r.font.color.rgb = WHITE

    for r_idx, row_data in enumerate(rows):
        row_bg = TBL_ROW_LIGHT if r_idx % 2 == 0 else TBL_ROW_MED
        for c_idx, val in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_bg
            set_cell_margins(cell, left=0.14, right=0.14, top=0.10, bottom=0.10)
            set_cell_borders(cell, "93C5FD", 13000)
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.line_spacing = 1.15
            r = p.add_run()
            r.text = str(val)
            r.font.name = font_name
            r.font.size = Pt(cell_size)
            r.font.bold = c_idx in bold_cols
            r.font.color.rgb = GOLD_TITLE if c_idx == 0 else CHARCOAL
    return shape


# ---------------------------------------------------------------------------
# Slide Builders (32 Slides Mirroring Sandhya's Presentation Pattern)
# ---------------------------------------------------------------------------

def build_slide_01_title(prs):
    """Slide 1: Title, Registration Number, Name, and Guide Name (Sandhya Slide 1 Pattern)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_title.png")

    # Left 3D-styled AI Neural Shield overlapping the white frame border
    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(0.55), Inches(1.75), width=Inches(4.75))

    # Main Title inside the dark-glass hero card (Warm Amber-Gold, large, crystal clear)
    tb = slide.shapes.add_textbox(Inches(5.15), Inches(2.45), Inches(13.8), Inches(4.05))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.line_spacing = 1.22
    r = p.add_run()
    r.text = (
        "Toward Trustworthy Large Language Models:\n"
        "A Comprehensive Review of Hallucination Detection,\n"
        "Explainability, and Mitigation Strategies"
    )
    r.font.name = FONT_TITLE
    r.font.size = Pt(42)
    r.font.bold = True
    r.font.color.rgb = HERO_GOLD

    # Dark rounded pill badge for Candidate Name & Reg No
    pill = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(6.95),
        Inches(7.05),
        Inches(9.15),
        Inches(1.08),
    )
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = HERO_CYAN
    pill.line.width = Pt(2.5)
    ptf = pill.text_frame
    ptf.word_wrap = True
    pp = ptf.paragraphs[0]
    pp.alignment = PP_ALIGN.CENTER
    pr = pp.add_run()
    pr.text = "Presented by :  Yogesh Ravi M   |   22MIA1052"
    pr.font.name = FONT_TITLE
    pr.font.size = Pt(29)
    pr.font.bold = True
    pr.font.color.rgb = WHITE

    # Bottom-right Telemetry Diagnostic Scope icon (matching Sandhya's stethoscope)
    scope_path = ASSETS_DIR / "illus_telemetry_scope.png"
    if scope_path.exists():
        slide.shapes.add_picture(str(scope_path), Inches(15.95), Inches(6.25), width=Inches(3.65))

    # Bottom Guide Line (with "Dr." prefix)
    gtb = slide.shapes.add_textbox(Inches(4.40), Inches(9.88), Inches(13.5), Inches(0.85))
    gtf = gtb.text_frame
    gp = gtf.paragraphs[0]
    gr = gp.add_run()
    gr.text = "GUIDED BY - Dr. Pradeep Kumar T S, Professor, SCOPE, VIT Chennai"
    gr.font.name = FONT_SANS
    gr.font.size = Pt(27)
    gr.font.bold = True
    gr.font.color.rgb = WHITE


def build_slide_02_outline(prs):
    """Slide 2: Outline (32-Slide Structure Following Exact Template Flow)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_framed_left.png")
    add_gold_title(slide, "OUTLINE (32 SLIDES)", left=1.0, top=0.32, width=14.0, size=46, align=PP_ALIGN.LEFT)

    items = [
        {"bold_prefix": "1. Introduction, Hallucination Types & Why TinyLlama-1.1B  (Slides 3–4): ", "text": "Why LLMs hallucinate, Intrinsic vs. Extrinsic errors, and 3 simple reasons we used TinyLlama-1.1B & GPT-2."},
        {"bold_prefix": "2. Literature Review — All 40 Papers in 7 Slides  (Slides 5–11): ", "text": "Comprehensive review of all 40 papers (6 papers on Slides 5–9, 5 papers on Slides 10–11) with methods and gaps."},
        {"bold_prefix": "3. Problem Statement, Research Gap, Challenges & Objectives  (Slides 12–13): ", "text": "Single-signal blindness, polarity inversion, probe overfitting, research gaps, and completed objectives."},
        {"bold_prefix": "4. Architecture, Dataset Format, Extraction, Training & Glossary  (Slides 14–18): ", "text": "10-step architecture, 12-stage blueprint, JSON dataset schema, PyTorch hook extraction, 5-fold OOF training & simple terms."},
        {"bold_prefix": "5. Results Discussion — Masks, Calibration, Colab Plots, Tables & UI  (Slides 19–28): ", "text": "Sensor masks, calibration histograms, log-odds trace, 4 Colab output plots, telemetry & metric tables, and live Web UI."},
        {"bold_prefix": "6. Comparison with Existing Works, ₹0 Deployment & Conclusion  (Slides 29–30): ", "text": "Comparison with prior works, ₹0 free Google Colab T4 execution, practical use cases, limitations, and future work."},
        {"bold_prefix": "7. Complete 40-Paper References & Thank You  (Slides 31–32): ", "text": "All 40 bibliographic references in a clean 2-column layout and closing slide."},
    ]
    add_white_bullets(slide, left=0.55, top=1.95, width=14.5, height=7.6, items=items, default_size=21.5, line_spacing=1.18)

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(15.65), Inches(3.25), width=Inches(4.05))


def build_slide_03_intro_and_taxonomy(prs):
    """Slide 3: Introduction & Hallucination Taxonomy (In Simple Words)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_framed_left.png")
    add_gold_title(slide, "INTRODUCTION & HALLUCINATION TAXONOMY", left=0.8, top=0.30, width=15.5, size=40, align=PP_ALIGN.LEFT)

    items = [
        {"bold_prefix": "• Why LLMs Hallucinate (Word-by-Word Guessing): ", "text": "LLMs write one word (token) at a time by guessing what sounds fluent next, rather than checking a database of verified facts."},
        {"bold_prefix": "• Why Normal Confidence Fails: ", "text": "Surface word probability fails on popular myths (TruthfulQA), where the LLM is >95% confident while stating a false belief."},
        {"bold_prefix": "• Intrinsic Hallucination (Twisting Prompt Text): ", "text": "Contradicts the document or chat right in front of it. Caught by AAS (Prompt Focus Tracker)."},
        {"bold_prefix": "• Extrinsic Hallucination (Inventing Outside Facts): ", "text": "Fabricates fake dates, citations, or people. Caught by ISP (Internal Brain Lie Detector)."},
        {"bold_prefix": "• Guessing & Topic Drift: ", "text": "Word hesitation is caught by EEM (Logit Energy), and multi-sentence topic derailment is tracked by DST (Cosine Drift)."},
    ]
    add_white_bullets(slide, left=0.50, top=1.90, width=12.80, height=7.6, items=items, default_size=22.0, line_spacing=1.16)

    inset = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(13.55), Inches(2.55), Inches(6.25), Inches(5.85))
    inset.fill.solid()
    inset.fill.fore_color.rgb = BADGE_DARK
    inset.line.color.rgb = WHITE
    inset.line.width = Pt(6)

    card_path = ASSETS_DIR / "illus_intrinsic_extrinsic.png"
    if card_path.exists():
        slide.shapes.add_picture(str(card_path), Inches(13.80), Inches(2.80), width=Inches(5.75))


def build_slide_04_why_tinyllama_and_gpt2(prs):
    """Slide 4: What is TinyLlama-1.1B & GPT-2 and Why We Used Them (3 Simple Reasons + ₹0 Cost)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "WHAT IS TINYLLAMA-1.1B & WHY WE USED IT", left=0.8, top=0.28, width=16.0, size=40, align=PP_ALIGN.LEFT)

    items = [
        {
            "title": "What is TinyLlama-1.1B-Chat-v1.0? (Meta Llama-2 Architecture, 1.1 Billion Parameters, 22 Layers, 3T Tokens)",
            "text": "",
            "title_size": 25.5,
            "title_color": GOLD_TITLE,
            "space_after": 8,
        },
        {
            "bold_prefix": "1. 100% Open-Source & 'White-Box' (Open Brain): ",
            "text": "Closed models like ChatGPT hide their internal layers. Because TinyLlama is open-weight on HuggingFace, we attach PyTorch hooks (register_forward_hook) directly inside its 22 layers (at Layers 10, 13, 16, and 20 = 45%, 60%, 75%, and 90% depth) to read its internal thoughts in one pass.",
            "size": 21.0,
            "space_after": 12,
        },
        {
            "bold_prefix": "2. Runs for Free (₹0 Cost) on Google Colab: ",
            "text": "Because it has 1.1B parameters, it takes only ~2.2 GB of GPU memory (FP16) — fitting effortlessly on Google Colab's free-tier 16 GB NVIDIA Tesla T4 GPU without paying a single rupee.",
            "size": 21.0,
            "space_after": 12,
        },
        {
            "bold_prefix": "3. Fast Real-Time Speed (33.49 ms/token): ",
            "text": "Generates ~30 words/second, allowing us to evaluate 3,196 benchmark responses + 300 live TriviaQA queries and prove our 4 sensors add only +2.91 ms/token (+8.7%) overhead.",
            "size": 21.0,
            "space_after": 14,
        },
        {
            "bold_prefix": "❖ Why We Also Tested GPT-2 (124M Parameters, 12 Layers): ",
            "text": "To prove TRUEGUARD does not only work on TinyLlama, we also tested OpenAI's GPT-2 (layers 5, 7, 9, 11) on a normal laptop CPU — achieving 85.20% Macro AUROC (96.02% on HaluEval-QA).",
            "size": 21.0,
            "space_after": 0,
        },
    ]
    add_white_bullets(slide, left=0.80, top=1.78, width=18.40, height=8.8, items=items, default_size=21.0, line_spacing=1.15)


# ---------------------------------------------------------------------------
# Slides 6 to 13: Literature Review (All 40 Papers from Our Report, 5 per Slide)
# ---------------------------------------------------------------------------
LIT_SLIDES_DATA = [
    # Slide 6 (Papers 1-5: Pillar 1 — Internal State Probing)
    [
        ["1", "Su et al. [1], 2024 (ACL)", "MIND: Unsupervised MLP Hidden-State Probing", "Formulated an unsupervised MLP probe over intermediate hidden states and released the HELM internal-state dataset.", "Relies solely on hidden states; misses attention dispersion and logit energy; no closed-loop mitigation."],
        ["2", "Zhang et al. [2], 2024 (EMNLP)", "PRISM: Prompt-Guided Internal State Probing", "Used truth-orienting prompt templates to align truthfulness subspaces across domains before linear probing.", "Requires prompt wrapping; passive scoring only with no runtime repair or retrieval grounding."],
        ["3", "Zhang et al. [5], 2025 (Neurocomputing)", "MHAD: Hallucination-Aware Deep Neurons", "Isolated hallucination-sensitive neurons at initial and final decoding steps via layer-wise linear probing.", "Static feature concatenation without dynamic multi-sensor calibration or corrective feedback."],
        ["4", "Dasgupta et al. [13], 2025 (EACL)", "HalluShift: Internal Distribution Shift Tracking", "Tracked layer-to-layer cosine and Wasserstein shifts in hidden states across autoregressive trajectories.", "Captures macro drift but has modest power on short QA when used without supervised probes."],
        ["5", "Nath et al. [16], 2025 (IEEE TPAMI)", "HalluShift++: Hierarchical Multimodal Shift", "Extended internal representation shift tracking to hierarchical vision-language hallucinations.", "Focused on multimodal encoders; provides no closed-loop text retrieval or calibrated abstention."],
    ],
    # Slide 7 (Papers 6-10: Pillar 1 & Pillar 2 — Probes & Logit Energy)
    [
        ["6", "Azaria & Mitchell [27], 2023 (EMNLP)", "SAPLMA: Supervised Middle-Layer Classifier", "Demonstrated that a lightweight classifier on middle-layer hidden activations separates true vs. false claims.", "Sensitive to cross-domain and answer-length distribution shifts without out-of-fold recalibration."],
        ["7", "Li et al. [28], 2023 (NeurIPS)", "ITI: Inference-Time Activation Intervention", "Shifted hidden activations along truthfulness head directions during decoding to boost TruthfulQA accuracy.", "Fixed steering strength degrades fluency and cannot supply external facts when knowledge is absent."],
        ["8", "Chen et al. [38], 2024 (AAAI)", "Truth Forest: Multi-Scale Orthogonal Probes", "Learned orthogonal truthfulness probes (Rap-O) across multiple scales to capture multidimensional truth directions.", "Higher probe complexity; limited to internal knowledge and lacks external retrieval fallback."],
        ["9", "Ma et al. [4], 2025 (arXiv)", "Semantic Energy: Penultimate Logit Energy", "Measured Boltzmann-inspired energy over penultimate logits rather than post-softmax probabilities.", "Operates only at the output layer; misses hidden-state conflict on fluent misconceptions."],
        ["10", "Anonymous [6], 2025 (OpenReview)", "Z-Score Token Entropy Spike + RL Penalty", "Detected abrupt token-entropy spikes during reasoning and penalized overconfident spikes in RL training.", "Requires RL fine-tuning and lacks inference-time external evidence retrieval."],
    ],
    # Slide 8 (Papers 11-15: Pillar 2 & Pillar 3 — Uncertainty & Attention)
    [
        ["11", "Kang et al. [7], 2025 (ACM CSUR)", "Epistemic vs. Aleatoric UQ Taxonomy", "Formalized epistemic vs. aleatoric uncertainty for LLMs and benchmarked single-pass vs. sampling UQ.", "Survey study; highlights 5x–20x latency bottleneck of multi-sample UQ without a closed-loop fix."],
        ["12", "Han, Kossen et al. [14], 2024 (ICML)", "SEPs: Linear Probes for Semantic Entropy", "Trained single-pass linear probes on hidden states to approximate multi-sample semantic entropy cheaply.", "Single-signal approximation; does not integrate attention dispersal, drift, or tiered mitigation."],
        ["13", "Moslonka et al. [17], 2025 (IEEE SPL)", "EPR: Thermodynamic Entropy Production Rate", "Estimated non-equilibrium entropy production from top-k token log-probabilities in black-box APIs.", "Restricted to surface log-probabilities; cannot inspect hidden states or attention maps."],
        ["14", "Manakul et al. [21], 2023 (EMNLP)", "SelfCheckGPT: Multi-Sample Consistency", "Checked sentence-level consistency across 5–20 stochastic generations using BERTScore and NLI.", "Multiplies inference latency by 5x–20x (169.38 ms/tok on T4 GPU) and performs passive detection only."],
        ["15", "Hajji et al. [9], 2025 (TACL)", "Map of Misbelief: Attention Aggregation", "Showed attention drop over prompt tokens catches intrinsic contradictions while entropy catches extrinsic errors.", "Evaluates attention and entropy separately without a learned multi-sensor fusion controller."],
    ],
    # Slide 9 (Papers 16-20: Pillar 3 & Pillar 4 — Attention & Benchmarks)
    [
        ["16", "Vazhentsev et al. [11], 2025 (AAAI)", "RAUQ: Recurrent Attention Head UQ", "Identified uncertainty-aware attention heads and combined them recurrently with token confidence in one pass.", "Ignores deep hidden-state probes and provides no corrective regeneration or retrieval."],
        ["17", "Sriramanan et al. [12], 2024 (NeurIPS)", "LLM-Check: Log-Det Attention + Hidden/Logit", "Combined attention kernel log-determinants, hidden scores, and logit entropy for single-pass detection.", "Static scoring without grouped out-of-fold probe stacking or closed-loop repair."],
        ["18", "Mündler et al. [36], 2024 (ICLR)", "Self-Contradiction Prompting & Critique", "Formalized self-contradictory hallucinations and paired contradiction detection with iterative revision.", "Requires multiple extra LLM calls per sentence and misses non-contradictory factual fabrications."],
        ["19", "Huang et al. [3], 2024 (ICML)", "TrustLLM: 8-Dimension Benchmark Suite", "Benchmarked 16+ LLMs across 30+ datasets spanning truthfulness, safety, fairness, and robustness.", "Offline evaluation suite; not a runtime guardrail or low-latency token detector."],
        ["20", "Jing et al. [10], 2025 (NAACL)", "Calibrated 1–5 Faithfulness Rubric + NLI", "Developed fine-grained 1–5 faithfulness scoring rubrics with LLM-as-judge and fine-tuned NLI evaluators.", "Post-generation judge model adds heavy compute overhead unsuitable for token-rate streaming."],
    ],
    # Slide 10 (Papers 21-25: Pillar 4 — Evaluation & Benchmarks)
    [
        ["21", "Alansari & Luqman [18], 2024 (IEEE Access)", "Full-Lifecycle Hallucination Taxonomy", "Catalogued causes, detection signals, and mitigation stages across pretraining, fine-tuning, and inference.", "Narrative survey; documents the detection-mitigation disconnect without an empirical controller."],
        ["22", "Lin et al. [22], 2022 (ACL)", "TruthfulQA: 817 Adversarial Questions", "Created 817 questions targeting popular human misconceptions where scaling model size alone fails.", "Static benchmark; requires pairing with internal probes to detect fluent misconceptions at runtime."],
        ["23", "Min et al. [23], 2023 (EMNLP)", "FActScore: Atomic Fact Decomposition", "Decomposed long biography generations into atomic facts verified individually against Wikipedia.", "Offline evaluation requiring multiple LLM decomposition and retrieval calls per paragraph."],
        ["24", "Li et al. [29], 2023 (EMNLP)", "HaluEval: 35,000 QA, Dialogue & Summaries", "Constructed 35k paired grounded and hallucinated responses across QA, dialogue, and summarization.", "Static benchmark; single surface metrics fail to generalize across all three HaluEval regimes."],
        ["25", "Chern et al. [34], 2023 (arXiv)", "FacTool: Tool-Augmented Claim Verification", "Verified LLM claims across QA, code, math, and science using web search, Python, and Scholar tools.", "High multi-step tool latency; operates post-hoc rather than reading single-pass internal states."],
    ],
    # Slide 11 (Papers 26-30: Pillar 4 & Pillar 5 — Surveys & Mitigation)
    [
        ["26", "Ji et al. [35], 2023 (ACM CSUR)", "Intrinsic vs. Extrinsic NLG Taxonomy", "Established the foundational intrinsic vs. extrinsic hallucination taxonomy across NLG tasks.", "Pre-LLM-era focus; does not cover white-box transformer activation probing or closed-loop control."],
        ["27", "Bang et al. [37], 2023 (IJCNLP-AACL)", "Multitask & Multimodal ChatGPT Audit", "Quantified extrinsic vs. intrinsic hallucination rates across multilingual and multimodal tasks.", "Black-box empirical audit; proposes no internal detection or automated mitigation mechanism."],
        ["28", "Wu et al. [15], 2025 (ICLR)", "BehCal-RL: Proper Scoring Rule Abstention", "Trained LLMs with strictly proper scoring rewards to state calibrated confidence or abstain when uncertain.", "Requires RL fine-tuning and immediately abstains without attempting retrieval-grounded correction."],
        ["29", "Yao et al. [20], 2025 (WWW)", "ExpandR: Joint LLM-Retriever DPO Alignment", "Optimized query expansion with DPO so retrieved passages improve downstream generation.", "Runs retrieval unconditionally on every query instead of triggering selectively on internal risk."],
        ["30", "Dhuliawala et al. [24], 2024 (ACL)", "CoVe: Chain-of-Verification Prompting", "Prompted the LLM to draft an answer, generate verification questions, answer them, and revise.", "Requires 3–5 sequential generation stages per query and fails when base knowledge is absent."],
    ],
    # Slide 12 (Papers 31-35: Pillar 5 — Retrieval & Multi-Agent Mitigation)
    [
        ["31", "Lewis et al. [25], 2020 (NeurIPS)", "RAG: Non-Parametric Dense Passage Retrieval", "Conditioned sequence generation on top-k Wikipedia passages retrieved via Dense Passage Retrieval.", "Always-on retrieval adds latency to easy queries and still hallucinates when context is noisy."],
        ["32", "Asai et al. [26], 2024 (ICLR)", "Self-RAG: Reflection & Critique Tokens", "Fine-tuned an LLM to emit [Retrieve], [IsRel], and [IsSup] reflection tokens for adaptive retrieval.", "Requires full supervised fine-tuning of the base LLM with custom vocabulary tokens."],
        ["33", "Wei et al. [30], 2022 (NeurIPS)", "CoT: Chain-of-Thought Reasoning Traces", "Showed that intermediate natural-language reasoning steps improve multi-step reasoning accuracy.", "Reasoning chains themselves can hallucinate intermediate premises without internal monitoring."],
        ["34", "Du et al. [31], 2024 (ICML)", "Multi-Agent Iterative Debate", "Multiple LLM instances critique and refine each other's answers over several rounds to reduce errors.", "Multiplies token and latency cost by N_agents x N_rounds (typically 6x–15x overhead)."],
        ["35", "Yin et al. [32], 2024 (Sci. China Inf.)", "Woodpecker: Post-Hoc Visual Verification", "Extracted key concepts from MLLM outputs, verified them with detectors, and rewrote faulty spans.", "Post-processing pipeline tailored to image captions; incurs high multi-model latency."],
    ],
    # Slide 13 (Papers 36-40: Pillar 5 & Pillar 6 — Post-Editing & Human-Trust XAI)
    [
        ["36", "Gao et al. [33], 2023 (ACL)", "RARR: Researching and Revising with LLMs", "Generated search queries for unverified claims in an LLM output and edited unsupported statements.", "Runs after full generation on every output rather than gating on single-pass internal risk."],
        ["37", "Gou et al. [39], 2024 (ICLR)", "CRITIC: Tool-Interactive Self-Correction", "Allowed LLMs to verify and revise their own outputs by interacting with search engines and code tools.", "Requires multiple iterative tool-invocation loops and provides no calibrated abstention guarantee."],
        ["38", "Agrawal et al. [40], 2024 (NAACL)", "KG-Augmented Grounding & Verification", "Synthesized knowledge-graph retrieval, graph-guided decoding, and post-hoc KG triple verification.", "Depends on curated domain knowledge graphs that are often incomplete for open-domain queries."],
        ["39", "Herrera [8], 2025 (Information Fusion)", "Four-Dimension Human-Centered LLM XAI", "Defined faithfulness, truthfulness, plausibility, and contrastivity as the 4 pillars of LLM XAI.", "Conceptual taxonomy; does not provide an algorithmic real-time sensor-attribution engine."],
        ["40", "Sharma et al. [19], 2024 (ACM CHI)", "Contrastive Explanations & Human Trust", "Demonstrated in human trials that comparative and contrastive explanations improve trust calibration.", "Behavioral study using mocked explanations; not connected to live internal hallucination sensors."],
    ],
]


def build_literature_slides(prs):
    """Build Slides 5 to 11 (7 Slides): All 40 papers (6 per slide on 5 slides + 5 per slide on 2 slides = 40)."""
    headers = ["S. No.", "Author(s), Year", "Method / Approach", "Key Contribution", "Gap Identified"]
    col_widths = [1.05, 3.65, 3.85, 5.05, 5.10]

    all_40 = [p for chunk in LIT_SLIDES_DATA for p in chunk]
    # 7 chunks: 6, 6, 6, 6, 6, 5, 5 = 40 papers
    sizes = [6, 6, 6, 6, 6, 5, 5]
    chunks = []
    cur = 0
    for sz in sizes:
        chunks.append(all_40[cur:cur + sz])
        cur += sz

    start_num = 1
    for idx, papers in enumerate(chunks):
        end_num = start_num + len(papers) - 1
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        set_bg_image(slide, "bg_table.png")
        add_gold_title(slide, f"LITERATURE REVIEW ({start_num}–{end_num} OF 40 PAPERS)", left=1.2, top=0.22, width=13.5, size=42, align=PP_ALIGN.LEFT)

        add_peach_table(
            slide,
            left=0.65,
            top=1.78,
            width=18.70,
            height=8.75,
            headers=headers,
            rows=papers,
            col_widths=col_widths,
            header_size=18.5,
            cell_size=15.2 if len(papers) == 6 else 16.2,
            bold_cols=(0, 1),
        )
        start_num = end_num + 1


def build_slide_12_problem_and_gap(prs):
    """Slide 12: Scope, Problem Statement & Research Gap."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_framed_center.png")
    add_gold_title(slide, "PROBLEM STATEMENT & RESEARCH GAP", left=1.0, top=0.32, width=16.5, size=42, align=PP_ALIGN.LEFT)

    items = [
        {"title": "Core Problem Statement (Why Existing Detectors Fail)", "text": "", "title_size": 26.5, "title_color": GOLD_TITLE, "space_after": 6},
        "• Single-Signal Blindness: Surface word probabilities miss confident myths (TruthfulQA), while single-layer probes miss prompt neglect in long summaries.",
        "• Signal Polarity Inversion (Overconfident Lying): On HaluEval-QA and Dialogue, raw token entropy inverts (34.9% and 37.0% AUROC — worse than a coin flip!).",
        "• Multi-Sample Latency Bottleneck: SelfCheckGPT requires 5–20 generations (169.31 ms/token on Tesla T4), making real-time chat impossible.",
        {"title": "Research Gap Identified Across 40 Reviewed Papers", "text": "", "title_size": 26.5, "title_color": CYAN_ACCENT, "space_after": 6},
        "• Disconnected Open-Loop Tools: Prior works treat internal probing, uncertainty, explainability (XAI), and RAG repair as separate offline tasks. No prior system unites 4-sensor single-pass OOF probing + 0.00 ms log-odds XAI + a 3-Tier Closed-Loop Wikipedia RAG Controller.",
    ]
    add_white_bullets(slide, left=1.35, top=2.05, width=16.6, height=7.4, items=items, default_size=21.5, line_spacing=1.15)


def build_slide_13_challenges_and_objectives(prs):
    """Slide 13: Research Challenges & Completed Objectives."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_framed_center.png")
    add_gold_title(slide, "RESEARCH CHALLENGES & OBJECTIVES", left=1.0, top=0.32, width=16.5, size=42, align=PP_ALIGN.LEFT)

    items = [
        {"title": "Key Engineering Challenges Overcome", "text": "", "title_size": 26, "title_color": GOLD_TITLE, "space_after": 6},
        "• Single-Pass Extraction & Overfitting Prevention: Extracting 4 internal signals in <3 ms/tok and preventing 8,192-dim hidden probe overfitting via leak-free 5-fold GroupKFold OOF stacking.",
        "• Zero-Cost Explainability: Replacing slow SHAP/LIME perturbations with exact analytical log-odds attribution (c_k = w_k * z_k) in 0.00 ms.",
        {"title": "Research Objectives (100% Completed & Hardware-Verified)", "text": "", "title_size": 26, "title_color": CYAN_ACCENT, "space_after": 6},
        "• Objective 1 (4-Sensor Extraction): Extract ISP ({0.45, 0.60, 0.75, 0.90}L), AAS (top-25% attention entropy), EEM (0.6 Shannon + 0.4 Renyi-2), and DST (cosine drift) in 1 pass.",
        "• Objective 2 (OOF Calibration & XAI): Fuse sensors via L2 logistic regression to reach 93.51% Macro AUROC (3.10% ECE) on TinyLlama-1.1B and 85.20% on GPT-2.",
        "• Objective 3 (3-Tier Closed-Loop Repair): Validate SAFE -> Tier 1 Re-Sample -> Tier 2 Live Wikipedia RAG -> Tier 3 Abstain across 3,196 static items and 300 live TriviaQA queries.",
    ]
    add_white_bullets(slide, left=1.35, top=2.05, width=16.6, height=7.4, items=items, default_size=21.0, line_spacing=1.15)


def build_slide_17_architecture_overview(prs):
    """Slide 17: High-Level Horizontal Architecture (Sandhya Slide 12 Pattern)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_arch_band.png")
    add_gold_title(slide, "Architecture", left=1.2, top=0.45, width=10.0, size=56, align=PP_ALIGN.LEFT)

    arch_path = ASSETS_DIR / "fig_horiz_arch_10step.png"
    if arch_path.exists():
        slide.shapes.add_picture(str(arch_path), Inches(0.25), Inches(3.15), width=Inches(19.5))


def build_slide_18_proposed_architecture_blueprint(prs):
    """Slide 18: Detailed 12-Stage Proposed Architecture Blueprint."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_split.png")
    add_gold_title(slide, "PROPOSED ARCHITECTURE — 12-STAGE BLUEPRINT", left=0.45, top=0.22, width=9.0, size=42, align=PP_ALIGN.LEFT)

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(0.85), Inches(2.55), width=Inches(5.35))

    bp_path = ASSETS_DIR / "fig_blueprint_12stage.png"
    if bp_path.exists():
        slide.shapes.add_picture(str(bp_path), Inches(6.55), Inches(1.85), width=Inches(12.35))


def build_slide_19_data_collection(prs):
    """Slide 19: Benchmark Corpus & Internal Telemetry Collection (Sandhya Slide 14 Pattern)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_framed_left.png")
    add_gold_title(slide, "BENCHMARK & TELEMETRY DATA", left=1.5, top=0.35, width=16.5, size=48, align=PP_ALIGN.LEFT)

    left_items = [
        {"title": "Evaluated across N = 3,496 total responses:", "text": "", "title_size": 26, "title_color": GOLD_TITLE, "space_after": 10},
        {"title": "4 Static Benchmarks (N = 3,196)", "underline": True, "title_size": 26, "title_color": CYAN_ACCENT, "text": "• HaluEval-QA: 800 (400 True / 400 Halluc.)\n• HaluEval-Dialogue: 800 responses\n• HaluEval-Summarization: 800 summaries\n• TruthfulQA: 796 adversarial myths", "bold": True, "size": 22.5, "space_after": 14},
        {"title": "Live Closed-Loop Trial (N = 300)", "underline": True, "title_size": 26, "title_color": CYAN_ACCENT, "text": "• Open-Domain TriviaQA queries decoded live with real-time Wikipedia REST API RAG", "bold": True, "size": 22.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=0.55, top=1.95, width=7.5, height=7.4, items=left_items, default_size=22.5, line_spacing=1.18)

    right_items = [
        {"title": "Per-Query Telemetry Captured", "underline": True, "title_size": 26, "title_color": GOLD_TITLE, "text": (
            "• Question Group ID (for leak-free GroupKFold)\n"
            "• Hidden states h_l at {0.45, 0.60, 0.75, 0.90}L\n"
            "• Top-quartile multi-head attention weights A_{t,j}\n"
            "• Pre-softmax logits z_t & token probabilities p_t\n"
            "• Final-layer consecutive cosine drift 1 - cos(h_t, h_{t-1})\n"
            "• Standardized sensor vector z = [z_ISP, z_AAS, z_EEM, z_DST]\n"
            "• Signed log-odds attributions c_k = w_k * z_k\n"
            "• Calibrated risk probability r(x, y) in [0, 1]"
        ), "bold": True, "size": 22.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=8.25, top=1.95, width=7.0, height=7.4, items=right_items, default_size=22.5, line_spacing=1.22)

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(15.65), Inches(3.25), width=Inches(4.0))


def build_slide_20_telemetry_details(prs):
    """Slide 16: Benchmark Datasets (N=3,496), JSON Format & Single-Pass Extraction Pipeline."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_split.png")
    add_gold_title(slide, "DATASET FORMAT & EXTRACTION PIPELINE", left=0.8, top=0.28, width=15.5, size=40, align=PP_ALIGN.LEFT)

    # Left Soft Ice-Blue Card: Dataset Format & Benchmark Corpus
    lbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(2.00), Inches(9.25), Inches(8.35))
    lbox.adjustments[0] = 0.03
    lbox.fill.solid()
    lbox.fill.fore_color.rgb = RGBColor(239, 246, 255)
    lbox.line.color.rgb = GOLD_TITLE
    lbox.line.width = Pt(2.5)

    left_items = [
        {"title": "1. Benchmark Corpus & JSON Format (N = 3,496 Total)", "title_size": 21.5, "title_color": GOLD_TITLE, "space_after": 6},
        {"bold_prefix": "• Evaluated Datasets (N = 3,496): ", "text": "4 Static Benchmarks (N=3,196: HaluEval-QA 800, Dialogue 800, Summarization 800, TruthfulQA 796) + Live TriviaQA Trial (N=300).", "size": 18.0},
        {"bold_prefix": "• Paired Ground-Truth JSON Schema:\n", "text": "  {\n    \"question_id\": \"qa_0412\",\n    \"prompt\": \"What causes the green aurora borealis?\",\n    \"response\": \"Excited oxygen atoms emitting at 557.7nm...\",\n    \"ground_truth\": \"Atmospheric particle collision...\",\n    \"label\": 0   // 0 = Factual, 1 = Hallucinated\n  }", "size": 16.5, "space_after": 6},
        {"bold_prefix": "• Balanced Pair Evaluation: ", "text": "Every question is paired with both truthful and hallucinated responses to prevent detector length or keyword bias.", "size": 18.0, "space_after": 0},
    ]
    add_white_bullets(slide, left=1.10, top=2.18, width=8.75, height=8.0, items=left_items, default_size=18.0, line_spacing=1.14)

    # Right Soft Mint-Emerald Card: Single-Pass PyTorch Extraction Pipeline
    rbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.45), Inches(2.00), Inches(8.70), Inches(8.35))
    rbox.adjustments[0] = 0.03
    rbox.fill.solid()
    rbox.fill.fore_color.rgb = RGBColor(236, 253, 245)
    rbox.line.color.rgb = CYAN_ACCENT
    rbox.line.width = Pt(2.5)

    right_items = [
        {"title": "2. Single-Pass PyTorch Forward-Hook Extraction", "title_size": 21.5, "title_color": CYAN_ACCENT, "space_after": 6},
        {"bold_prefix": "• Non-Invasive Hooks: ", "text": "Using register_forward_hook() directly inside the LLM during token generation — 0% model retraining or weights altered.", "size": 17.5},
        {"bold_prefix": "• Sensor 1 (ISP - Brain Probe): ", "text": "Hidden states h_l at 4 depths {10, 13, 16, 20} (45%, 60%, 75%, 90% depth) on TinyLlama ({5, 7, 9, 11} on GPT-2).", "size": 17.5},
        {"bold_prefix": "• Sensor 2 (AAS - Focus Tracker): ", "text": "Attention weights from top-quartile heads to measure prompt dispersion 1 - sum_{i in prompt} A_{t,i}.", "size": 17.5},
        {"bold_prefix": "• Sensor 3 (EEM - Word Hesitation): ", "text": "Pre-softmax vocabulary logits -> 0.6*Shannon + 0.4*Renyi-2 entropy.", "size": 17.5},
        {"bold_prefix": "• Sensor 4 (DST - Topic Drift): ", "text": "Final residual stream cosine drift 1 - cos(h_t, h_{t-1}).", "size": 17.5},
        {"bold_prefix": "• Free Tesla T4 Execution: ", "text": "+2.91 ms/token (+8.7%) latency overhead, 4.65x faster than 5-sample blackbox approaches.", "size": 17.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=10.70, top=2.18, width=8.20, height=8.0, items=right_items, default_size=17.5, line_spacing=1.14)


def build_slide_21_why_4sensor_oof(prs):
    """Slide 17: Training Methodology, Calibration & Log-Odds XAI (With 4-Layer Probe Visual)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_split.png")
    add_gold_title(slide, "MODEL TRAINING, CALIBRATION & LOG-ODDS XAI", left=0.8, top=0.28, width=15.8, size=40, align=PP_ALIGN.LEFT)

    # Left Soft Ice-Blue Box: 4-Step Training & Calibration Pipeline
    lbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(2.00), Inches(9.55), Inches(8.35))
    lbox.adjustments[0] = 0.03
    lbox.fill.solid()
    lbox.fill.fore_color.rgb = RGBColor(239, 246, 255)
    lbox.line.color.rgb = GOLD_TITLE
    lbox.line.width = Pt(2.5)

    left_items = [
        {"title": "3. How We Used Data to Train & Calibrate the Detector", "title_size": 21.5, "title_color": GOLD_TITLE, "space_after": 5},
        {"bold_prefix": "• Step 1 — Sequence-Level Pooling: ", "text": "Token-level sensor trajectories are mean-pooled across answer tokens into a 4D feature vector phi(x,y) = [phi_ISP, phi_AAS, phi_EEM, phi_DST].", "size": 17.5},
        {"bold_prefix": "• Step 2 — Leak-Free 5-Fold GroupKFold OOF: ", "text": "Partitioned strictly by question_id so training questions NEVER leak into validation or testing folds — zero memorization.", "size": 17.5},
        {"bold_prefix": "• Step 3 — Z-Score & L2 Logistic Fusion: ", "text": "Standardizes z_k = (phi_k - mu_k)/sigma_k and fits L2 Logistic Regression to learn w = [w_ISP, w_AAS, w_EEM, w_DST], reaching 93.51% Macro AUROC (3.10% ECE).", "size": 17.5},
        {"bold_prefix": "• Step 4 — Log-Odds XAI & 3-Tier Thresholds: ", "text": "Instant blame c_k = w_k * z_k (0.00 ms). Held-out calibration sets Green (<0.611 SAFE), Amber (Tier 1 Resample), Red (>=0.898 Tier 2 Wiki RAG / Tier 3 Abstain).", "size": 17.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=1.10, top=2.16, width=9.05, height=8.0, items=left_items, default_size=17.5, line_spacing=1.13)

    # Right Dark Inset Box with 4-Layer Probe Visual
    rbox = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.65), Inches(2.00), Inches(8.45), Inches(8.35))
    rbox.adjustments[0] = 0.03
    rbox.fill.solid()
    rbox.fill.fore_color.rgb = BADGE_DARK
    rbox.line.color.rgb = GOLD_TITLE
    rbox.line.width = Pt(2.5)

    swarm_path = ASSETS_DIR / "illus_4layers_swarm.png"
    if swarm_path.exists():
        slide.shapes.add_picture(str(swarm_path), Inches(10.90), Inches(2.85), width=Inches(7.95))


def build_slide_21b_simple_terms_glossary(prs):
    """Slide 22: Key Technical Terms in Simple Everyday Words (Viva Quick-Guide Slide)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "KEY TECHNICAL TERMS — IN SIMPLE WORDS", left=1.0, top=0.25, width=16.5, size=44, align=PP_ALIGN.LEFT)

    headers = ["Technical Term in PPT", "Simple Meaning (In Plain Everyday Words)", "Why We Used It in TRUEGUARD"]
    rows = [
        ["White-Box PyTorch Hooks", "Listening to the LLM's internal brain layers while it writes", "Lets us catch lies inside the model in 1 pass without changing weights"],
        ["ISP (Internal State Probe)", "Brain Lie Detector at 45%, 60%, 75%, and 90% layer depth", "Catches when the LLM's internal memory knows a claim is false"],
        ["AAS (Attention Anomaly)", "Prompt Focus Tracker across top-25% attention heads", "Catches when the LLM stops reading the given document or chat"],
        ["EEM (Energy & Entropy)", "Word Hesitation Meter (60% Shannon + 40% Renyi-2)", "Catches when the LLM is confused and guessing between words"],
        ["DST (Drift Score Tracker)", "Topic Derailment Meter (step-to-step cosine angle jump)", "Catches when the LLM slowly wanders off-topic in long answers"],
        ["Polarity Inversion", "Overconfident lying (model is 99% sure when stating a myth)", "Explains why raw word confidence fails (34.9% on HaluEval-QA)"],
        ["5-Fold GroupKFold OOF", "5-round leak-free exam on unseen questions (no memorizing)", "Learns honest sensor weights and boosts accuracy to 93.51%"],
        ["Log-Odds XAI (c_k = w_k*z_k)", "Instant blame score showing WHICH sensor caught the lie", "Explains the exact reason for every alert in 0.00 ms (zero extra cost)"],
        ["AUROC / ECE / AURC", "AUROC = Separation accuracy | ECE = Honesty of % | AURC = Risk", "Proves 93.51% accuracy, 3.10% error, and safe selective answering"],
        ["3-Tier RAG Controller", "Traffic-light auto-fixer (Green=Pass, Amber=Retry, Red=Wikipedia)", "Cuts final hallucinations on live TriviaQA from 62.0% down to 17.33%"],
    ]

    add_peach_table(
        slide,
        left=0.65,
        top=1.78,
        width=18.70,
        height=8.75,
        headers=headers,
        rows=rows,
        col_widths=[4.35, 7.35, 7.00],
        header_size=20.0,
        cell_size=17.5,
        bold_cols=(0,),
    )


def build_slide_22a_colab_detection_benchmarks(prs):
    """Slide 22: Actual Paper Output Plot — 5-Fold OOF AUROC & Cross-Domain Transfer (fig_hd_7_2.png)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — 4-BENCHMARK AUROC", left=0.8, top=0.25, width=16.5, size=38, align=PP_ALIGN.LEFT)

    fig_path = FIG_DIR / "fig_hd_7_2.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(2.40), Inches(1.62), width=Inches(15.20))

    items = [
        {"bold_prefix": "Left Plot (a) — 5-Fold OOF Detection Accuracy (N = 3,196): ", "text": "TRUEGUARD (dark blue) achieves 97.5% on HaluEval-QA, 90.3% on Dialogue, 98.6% on Summarization, and 87.6% on TruthfulQA (93.51% Macro Average), beating Raw Entropy (34.9%–58.0%).", "size": 19.5, "space_after": 6},
        {"bold_prefix": "Right Plot (b) — Cross-Benchmark Transfer Heatmap: ", "text": "Shows how well a detector trained on one dataset works on another — proving strong generalization across QA, Dialogue, and Summarization.", "size": 19.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=0.95, top=8.22, width=18.10, height=2.35, items=items, default_size=19.5, line_spacing=1.12)


def build_slide_22b_colab_sensor_ablation(prs):
    """Slide 23: Actual Paper Output Plot — Leave-One-Out Sensor Ablation (fig_hd_7_3.png)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — SENSOR ABLATION", left=0.8, top=0.25, width=16.5, size=38, align=PP_ALIGN.LEFT)

    fig_path = FIG_DIR / "fig_hd_7_3.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(2.40), Inches(1.62), width=Inches(15.20))

    items = [
        {"bold_prefix": "What This Paper Plot Proves (In Simple Words): ", "text": "We tested each sensor alone (blue bars) and tested removing one sensor at a time ('w/o' bars).", "size": 19.5, "space_after": 6},
        {"bold_prefix": "Key Finding — Why Internal Brain Probing (ISP) Is Essential: ", "text": "When we remove ISP (red bar 'w/o ISP'), accuracy drops from 87.63% to 62.58% on TruthfulQA and from 97.49% to 91.77% on HaluEval-QA, proving that deep brain probes catch lies that surface metrics miss.", "size": 19.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=0.95, top=8.22, width=18.10, height=2.35, items=items, default_size=19.5, line_spacing=1.12)


def build_slide_22_results_sensor_mask(prs):
    """Slide 22: Results Discussion — 3-Panel Sensor Mask Trace."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — TOKEN SENSOR MASK", left=2.0, top=0.35, width=15.0, size=50, align=PP_ALIGN.CENTER)

    mask_path = ASSETS_DIR / "fig_3panel_sensor_mask.png"
    if mask_path.exists():
        slide.shapes.add_picture(str(mask_path), Inches(0.65), Inches(2.05), width=Inches(12.85))

    cap = slide.shapes.add_textbox(Inches(0.65), Inches(6.65), Inches(12.85), Inches(0.85))
    cp = cap.text_frame.paragraphs[0]
    cr = cp.add_run()
    cr.text = "Figure: Token-Level Internal Sensor Masking Using Single-Pass Hooks (ISP + AAS)"
    cr.font.name = FONT_TITLE
    cr.font.size = Pt(23.5)
    cr.font.bold = True
    cr.font.color.rgb = GOLD_TITLE

    right_items = [
        {"bold_prefix": "1. Input Token Stream\n", "text": "Autoregressive tokens generated during the initial pass y^(0).", "size": 22.0},
        {"bold_prefix": "2. Sensor Activation Mask\n", "text": "Binary fault mask from ISP & AAS:\n 1. White = internal anomaly spike\n 2. Black = grounded safe tokens", "size": 22.0},
        {"bold_prefix": "3. Pinpointed Hallucination\n", "text": "The mask isolates the exact fabricated date ('1984') and entity ('Lord Vane') in one pass.", "size": 22.0, "space_after": 0},
    ]
    add_white_bullets(slide, left=13.75, top=2.05, width=5.45, height=7.2, items=right_items, default_size=22.0, line_spacing=1.18)


def build_slide_23_results_baseline_vs_calibrated(prs):
    """Slide 23: Results Discussion — Baseline vs. TRUEGUARD Calibration."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — RISK CALIBRATION", left=2.0, top=0.30, width=15.0, size=50, align=PP_ALIGN.CENTER)

    cmp_path = ASSETS_DIR / "fig_baseline_vs_calibrated.png"
    if cmp_path.exists():
        slide.shapes.add_picture(str(cmp_path), Inches(3.15), Inches(1.75), width=Inches(12.85))

    items = [
        {"title": "Figure: Comparison of Baseline Token Entropy and TRUEGUARD OOF-Calibrated Risk", "text": "", "title_size": 26, "title_color": GOLD_TITLE, "space_after": 10},
        {"bold_prefix": "Left : Raw Token Entropy Baseline (Macro AUROC = 0.529)\n", "text": "Raw softmax entropy before multi-sensor fusion. Factual and hallucinated distributions overlap heavily, and polarity inverts on HaluEval-QA (0.349 raw AUROC) and Dialogue (0.370 raw AUROC).", "size": 22.0, "space_after": 10},
        {"bold_prefix": "Right : TRUEGUARD 4-Sensor OOF Optimized (Macro AUROC = 0.935)\n", "text": "After inner 5-fold GroupKFold OOF stacking and L2 logistic calibration across ISP, AAS, EEM, and DST, factual and hallucinated responses separate cleanly (Macro F1 = 0.882, Macro ECE = 0.031).", "size": 22.0, "space_after": 0},
    ]
    add_white_bullets(slide, left=1.45, top=6.85, width=17.1, height=3.8, items=items, default_size=22.0, line_spacing=1.15)


def build_slide_24_results_terminal_roi(prs):
    """Slide 24: Results Discussion — Terminal & Log-Odds Attribution Trace."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — LOG-ODDS DIAGNOSTIC TRACE", left=2.0, top=0.35, width=15.0, size=50, align=PP_ALIGN.CENTER)

    roi_path = ASSETS_DIR / "fig_terminal_detection_roi.png"
    if roi_path.exists():
        slide.shapes.add_picture(str(roi_path), Inches(1.65), Inches(2.05), width=Inches(16.70))

    cap = slide.shapes.add_textbox(Inches(1.65), Inches(8.85), Inches(16.70), Inches(0.85))
    cp = cap.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run()
    cr.text = "Figure: Candidate Hallucination Detection, 4-Layer ISP Activation, and Log-Odds Attribution Trace"
    cr.font.name = FONT_TITLE
    cr.font.size = Pt(24.5)
    cr.font.bold = True
    cr.font.color.rgb = GOLD_TITLE


def build_slide_25_table_telemetry_features(prs):
    """Slide 25: Results Discussion — Table of Extracted Telemetry Features."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — EXTRACTED TELEMETRY", left=2.0, top=0.30, width=15.0, size=50, align=PP_ALIGN.CENTER)

    headers = ["Extracted Telemetry Feature / Parameter", "Query Q075 (TinyLlama-1.1B)"]
    rows = [
        ["ISP Probe Layer 10 (0.45L Depth Probability)", "0.782"],
        ["ISP Probe Layer 13 (0.60L Depth Probability)", "0.941"],
        ["ISP Probe Layer 16 (0.75L Depth Probability)", "0.958"],
        ["ISP Probe Layer 20 (0.90L Depth Probability)", "0.893"],
        ["Stacked 5-Fold OOF ISP Score (s_ISP / z_ISP)", "0.934  (z = +1.94)"],
        ["AAS Top-Quartile Attention Entropy (s_AAS / z_AAS)", "0.684  (z = +0.82)"],
        ["EEM Blended Logit Entropy (0.6 Shannon + 0.4 Renyi-2)", "0.241  (z = -0.35)"],
        ["DST Consecutive Hidden Cosine Drift (1 - cos)", "0.318  (z = +0.61)"],
        ["Dominant Analytical Log-Odds Attribution (c_ISP = w_1*z_1)", "+2.180  (Parametric Memory Fault)"],
        ["Secondary Log-Odds Attributions (c_AAS / c_DST / c_EEM)", "+0.490 / +0.280 / -0.110"],
        ["Fused Initial Risk Probability r(x, y^(0))", "0.914  (>= tau_fault 0.898 -> Tier 2 RAG)"],
        ["Post-RAG Grounded Risk Probability r(x, y^(2))", "0.182  (< tau_warn 0.611 -> VERIFIED SAFE)"],
    ]

    add_peach_table(
        slide,
        left=3.20,
        top=1.75,
        width=13.60,
        height=7.35,
        headers=headers,
        rows=rows,
        col_widths=[7.80, 5.80],
        header_size=20.5,
        cell_size=18.5,
        bold_cols=(0,),
    )

    cap = slide.shapes.add_textbox(Inches(3.20), Inches(9.35), Inches(13.60), Inches(0.85))
    cp = cap.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run()
    cr.text = "Table : TRUEGUARD – Extracted Single-Pass Telemetry & Log-Odds Features"
    cr.font.name = FONT_TITLE
    cr.font.size = Pt(25)
    cr.font.bold = True
    cr.font.color.rgb = GOLD_TITLE

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(0.35), Inches(6.05), width=Inches(2.75))


def build_slide_26_table_performance_metrics(prs):
    """Slide 26: Results Discussion — Table of Performance Metrics."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — PERFORMANCE METRICS", left=2.0, top=0.30, width=15.0, size=50, align=PP_ALIGN.CENTER)

    headers = ["Evaluation Benchmark / System Metric (Colab Verified)", "Verified Value (TRUEGUARD vs. Baseline)"]
    rows = [
        ["HaluEval-QA Detection AUROC (N = 800, 400 Pairs)", "97.50%   [F1 = 0.955, ECE = 0.024 | Raw ENT = 34.9%]"],
        ["HaluEval-Dialogue Detection AUROC (N = 800, 400 Pairs)", "90.28%   [F1 = 0.820, ECE = 0.034 | Raw ENT = 37.0%]"],
        ["HaluEval-Summarization Detection AUROC (N = 800, 400 Pairs)", "98.63%   [F1 = 0.935, ECE = 0.025 | Raw ENT = 58.0%]"],
        ["TruthfulQA Generation Detection AUROC (N = 796, 398 Pairs)", "87.63%   [F1 = 0.817, ECE = 0.042 | Raw ENT = 49.5%]"],
        ["Macro Average AUROC — TinyLlama-1.1B (N = 3,196)", "93.51%   [Macro F1 = 0.882 | Without ISP Grey-Box = 75.1%]"],
        ["Macro Average AUROC — GPT-2 Backbone (N = 320 Cross-Model)", "85.20%   [HaluEval-QA = 96.02%, TruthfulQA = 74.40%]"],
        ["Macro Expected Calibration Error (ECE ↓)", "3.10%     (Down from 18.40% Raw Entropy & 24.10% NLL)"],
        ["Live TriviaQA Factual Accuracy (N = 300: 150 Cal / 150 Test)", "60.00%   (Up from 38.00% Unmitigated Greedy Baseline)"],
        ["Live TriviaQA System-Wide Emitted Hallucination Rate (↓)", "17.33%   (Down from 62.00% — 72.04% Relative Reduction)"],
        ["Google Colab Free T4 GPU Telemetry Latency Overhead", "+8.70%   (36.41 vs. 33.49 ms/tok — 4.65x Faster than 5-Sample)"],
    ]

    add_peach_table(
        slide,
        left=2.60,
        top=1.75,
        width=14.60,
        height=7.15,
        headers=headers,
        rows=rows,
        col_widths=[7.60, 7.00],
        header_size=21.0,
        cell_size=19.0,
        header_bg=TBL_HEADER_ORANGE,
        font_name=FONT_SERIF,
        bold_cols=(0, 1),
    )

    cap = slide.shapes.add_textbox(Inches(2.60), Inches(9.25), Inches(14.60), Inches(0.85))
    cp = cap.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run()
    cr.text = "Table : Performance Metrics of the Proposed TRUEGUARD Framework"
    cr.font.name = FONT_TITLE
    cr.font.size = Pt(25)
    cr.font.bold = True
    cr.font.color.rgb = CYAN_ACCENT

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(17.25), Inches(5.85), width=Inches(2.55))


def build_slide_27_results_webapp_ui(prs):
    """Slide 27: Results Discussion — Experimental Web Interface Screenshot."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — PROTOTYPE INTERFACE", left=2.0, top=0.25, width=15.0, size=50, align=PP_ALIGN.CENTER)

    ui_path = ASSETS_DIR / "fig_webapp_ui_screenshot.png"
    if ui_path.exists():
        slide.shapes.add_picture(str(ui_path), Inches(2.65), Inches(1.68), width=Inches(14.70))

    cap = slide.shapes.add_textbox(Inches(1.45), Inches(9.65), Inches(17.10), Inches(0.80))
    cp = cap.text_frame.paragraphs[0]
    cp.alignment = PP_ALIGN.CENTER
    cr = cp.add_run()
    cr.text = "Figure : Experimental TRUEGUARD Live Detection & Closed-Loop Wikipedia RAG Interface"
    cr.font.name = FONT_TITLE
    cr.font.size = Pt(24)
    cr.font.bold = True
    cr.font.color.rgb = GOLD_TITLE


def build_slide_27b_colab_mitigation_plot(prs):
    """Slide 24: Actual Paper Output Plot — 3-Tier Controller Routing & Hallucination Drop (fig_hd_8_1.png)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — LIVE TRIVIAQA MITIGATION", left=0.8, top=0.25, width=16.5, size=38, align=PP_ALIGN.LEFT)

    fig_path = FIG_DIR / "fig_hd_8_1.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(2.40), Inches(1.62), width=Inches(15.20))

    items = [
        {"bold_prefix": "Left Plot (a) — 3-Tier Routing on 150 Live TriviaQA Test Queries: ", "text": "48 SAFE Pass-Through (32.0%), 11 Tier-1 Re-sampled (7.3%), 6 Tier-2 Wikipedia RAG Grounded (4.0%), and 85 Tier-3 Safe Abstentions (56.7%).", "size": 19.5, "space_after": 6},
        {"bold_prefix": "Right Plot (b) — 72.0% Hallucination Drop: ", "text": "Emitted hallucinations fall from 62.0% to 17.3%, while answered accuracy jumps from 38.0% to 60.0% (+22.0%) and overall system safety reaches 82.7%.", "size": 19.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=0.95, top=8.22, width=18.10, height=2.35, items=items, default_size=19.5, line_spacing=1.12)


def build_slide_27c_colab_latency_plot(prs):
    """Slide 25: Actual Paper Output Plot — Free Google Colab T4 GPU vs. Local CPU Latency (fig_hd_8_3.png)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "RESULTS DISCUSSION — T4 GPU & CPU LATENCY", left=0.8, top=0.25, width=16.5, size=38, align=PP_ALIGN.LEFT)

    fig_path = FIG_DIR / "fig_hd_8_3.png"
    if fig_path.exists():
        slide.shapes.add_picture(str(fig_path), Inches(2.40), Inches(1.62), width=Inches(15.20))

    items = [
        {"bold_prefix": "Left Plot (a) — Free Google Colab NVIDIA Tesla T4 GPU (₹0 Cost): ", "text": "Vanilla TinyLlama takes 33.49 ms/token; TRUEGUARD takes 36.41 ms/token (+2.91 ms = +8.7% overhead), which is 4.65x faster than 5-Sample Consistency (169.31 ms/token).", "size": 19.5, "space_after": 6},
        {"bold_prefix": "Right Plot (b) — Local Laptop CPU (GPT-2 124M, ₹0 Cost): ", "text": "Online KV-cached telemetry (143.37 ms/token) runs at near-zero overhead compared to vanilla decoding (159.88 ms/token) and is 9.5x faster than 5-sample consistency (1361.49 ms/token).", "size": 19.5, "space_after": 0},
    ]
    add_white_bullets(slide, left=0.95, top=8.22, width=18.10, height=2.35, items=items, default_size=19.5, line_spacing=1.12)


def build_slide_28_comparison_and_real_world_cost(prs):
    """Slide 29: Comparison with Existing Works & Real-World Zero-Cost (₹0) Deployment."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "COMPARISON & REAL-WORLD ₹0 DEPLOYMENT", left=0.8, top=0.28, width=15.0, size=40, align=PP_ALIGN.LEFT)

    items = [
        {
            "bold_prefix": "❖ Single-Pass 4-Sensor Fusion vs. Single-Signal / Multi-Sample: ",
            "text": "Beats raw token entropy (0.529 Macro AUROC) and is 4.65x faster than 5-sample SelfCheckGPT (36.41 vs. 169.31 ms/token) while reaching 0.935 Macro AUROC.",
            "size": 20.5,
            "space_after": 10,
        },
        {
            "bold_prefix": "❖ Leak-Free OOF Calibration & Review 2 -> Final Review Progression: ",
            "text": "Fixes severe polarity inversion on QA (0.349 -> 0.975) and Dialogue (0.370 -> 0.903). All open Review 2 questions (sensor weights, 0.00 ms log-odds XAI, 3-Tier Wikipedia RAG) are now 100% hardware-verified.",
            "size": 20.5,
            "space_after": 10,
        },
        {
            "bold_prefix": "❖ 100% Free Execution & Tiny Footprint (₹0 / $0.00 Spent): ",
            "text": "Run entirely on Google Colab's free-tier T4 GPU (16 GB VRAM) and a local laptop CPU using open-weight LLMs (TinyLlama-1.1B & GPT-2). The 4 linear probes occupy < 50 KB RAM with 0% LLM retraining.",
            "size": 20.5,
            "space_after": 10,
        },
        {
            "bold_prefix": "❖ Real-World Drop-In Middleware & Industry Use Cases: ",
            "text": "Wraps any HuggingFace/PyTorch model via forward hooks (`trueguard.detector` & `trueguard.controller`) for clinical note assistants, legal contract summarization, and enterprise chatbots.",
            "size": 20.5,
            "space_after": 0,
        },
    ]
    add_white_bullets(slide, left=0.85, top=1.72, width=18.2, height=8.8, items=items, default_size=20.5, line_spacing=1.15)


def build_slide_30_conclusion_and_future_work(prs):
    """Slide 30: Conclusion, Limitations & Future Work."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "CONCLUSION, LIMITATIONS & FUTURE WORK", left=0.8, top=0.28, width=16.5, size=40, align=PP_ALIGN.LEFT)

    items = [
        {
            "title": "Conclusion (Hardware-Verified Across N = 3,496 Responses)",
            "text": "• TRUEGUARD unites 4 single-pass internal sensors (ISP, AAS, EEM, DST), leak-free 5-fold GroupKFold OOF calibration (93.51% Macro AUROC on TinyLlama-1.1B, 85.20% on GPT-2), 0.00 ms log-odds XAI (c_k = w_k * z_k), and a 3-Tier Wikipedia RAG Controller that cuts live TriviaQA hallucinations by 72.04% (62.0% -> 17.33%).",
            "title_size": 25.5,
            "title_color": GOLD_TITLE,
            "size": 20.5,
            "space_after": 12,
        },
        {
            "title": "Operational Limitations",
            "text": "• Requires white-box PyTorch forward hooks (cannot inspect closed text-only APIs); Tier 2 RAG depends on Wikipedia coverage for niche domains.",
            "title_size": 25.5,
            "title_color": CYAN_ACCENT,
            "size": 20.5,
            "space_after": 12,
        },
        {
            "title": "Future Work",
            "text": "• Scale fractional-depth probing to 8B–70B models with Sparse Autoencoders (SAEs), adapt AAS to multimodal Vision-Language LLMs, and trigger mid-sentence KV-cache token rollback.",
            "title_size": 25.5,
            "title_color": GOLD_TITLE,
            "size": 20.5,
            "space_after": 0,
        },
    ]
    add_white_bullets(slide, left=0.85, top=1.75, width=18.2, height=8.8, items=items, default_size=20.5, line_spacing=1.15)


def build_slide_31_references(prs):
    """Slide 31: All 40 References in a clean 2-column layout (20 Left, 20 Right)."""
    refs_part1 = [
        "[1] W. Su et al., “MIND: Unsupervised Real-Time Hallucination Detection,” ACL, 2024.",
        "[2] X. Zhang et al., “PRISM: Prompt-Guided Internal States,” EMNLP, 2024.",
        "[3] Y. Huang et al., “TrustLLM: Trustworthiness in LLMs,” ICML, 2024.",
        "[4] H. Ma et al., “Semantic Energy: Detecting Hallucination Beyond Entropy,” arXiv, 2025.",
        "[5] Y. Zhang et al., “MHAD: Deep Internal Representation Analysis,” Neurocomputing, 2025.",
        "[6] Anonymous, “Entropy Spike Detection & Calibration in Reasoning,” OpenReview, 2025.",
        "[7] M. Kang et al., “Uncertainty Quantification for Hallucination Detection,” ACM CSUR, 2025.",
        "[8] F. Herrera, “Survey & Challenges for XAI in LLMs,” Information Fusion, 2025.",
        "[9] M. Hajji et al., “Map of Misbelief: Attention Patterns,” TACL, 2025.",
        "[10] L. Jing et al., “Quantifying Faithfulness via Calibrated Rubrics,” NAACL, 2025.",
        "[11] A. Vazhentsev et al., “RAUQ: Uncertainty-Aware Attention Heads,” AAAI, 2025.",
        "[12] G. Sriramanan et al., “LLM-Check: Investigating Hallucinations,” NeurIPS, 2024.",
        "[13] S. Dasgupta et al., “HalluShift: Distribution Shifts in LLMs,” EACL, 2025.",
        "[14] J. Han, J. Kossen et al., “Semantic Entropy Probes (SEPs),” ICML, 2024.",
        "[15] Z. Wu et al., “BehCal-RL: Behaviorally Calibrated RL,” ICLR, 2025.",
        "[16] S. Nath et al., “HalluShift++: Language & Vision Shifts,” IEEE TPAMI, 2025.",
        "[17] C. Moslonka et al., “Token-Level Entropy Production Rate,” IEEE SPL, 2025.",
        "[18] A. Alansari & H. Luqman, “LLM Hallucination Survey Across Lifecycle,” IEEE Access, 2024.",
        "[19] N. Sharma et al., “Human Trust in Language Model Responses,” ACM CHI, 2024.",
        "[20] Z. Yao et al., “ExpandR: Dense Retrievers with LLM Guidance,” ACM WWW, 2025.",
    ]

    refs_part2 = [
        "[21] P. Manakul et al., “SelfCheckGPT: Zero-Resource Detection,” EMNLP, 2023.",
        "[22] S. Lin, J. Hilton, and O. Evans, “TruthfulQA: Measuring Human Falsehoods,” ACL, 2022.",
        "[23] S. Min et al., “FActScore: Atomic Evaluation of Factual Precision,” EMNLP, 2023.",
        "[24] S. Dhuliawala et al., “CoVe: Chain-of-Verification in LLMs,” ACL Findings, 2024.",
        "[25] P. Lewis et al., “RAG: Retrieval-Augmented Generation,” NeurIPS, 2020.",
        "[26] A. Asai et al., “Self-RAG: Retrieve, Generate, and Critique,” ICLR, 2024.",
        "[27] A. Azaria and T. Mitchell, “SAPLMA: Internal State of an LLM,” EMNLP, 2023.",
        "[28] K. Li et al., “ITI: Inference-Time Intervention for Truthfulness,” NeurIPS, 2023.",
        "[29] J. Li et al., “HaluEval: Large-Scale Hallucination Benchmark,” EMNLP, 2023.",
        "[30] J. Wei et al., “Chain-of-Thought Prompting in LLMs,” NeurIPS, 2022.",
        "[31] Y. Du et al., “Improving Factuality via Multiagent Debate,” ICML, 2024.",
        "[32] S. Yin et al., “Woodpecker: Multimodal Hallucination Correction,” Sci. China, 2024.",
        "[33] L. Gao et al., “RARR: Researching and Revising with LLMs,” ACL, 2023.",
        "[34] I.-C. Chern et al., “FacTool: Tool-Augmented Factuality Detection,” arXiv, 2023.",
        "[35] Z. Ji et al., “Survey of Hallucination in NLG,” ACM CSUR, 2023.",
        "[36] N. Mündler et al., “Self-Contradictory Hallucinations of LLMs,” ICLR, 2024.",
        "[37] Y. Bang et al., “Multitask Evaluation of ChatGPT on Hallucination,” AACL, 2023.",
        "[38] Z. Chen et al., “Truth Forest: Multi-Scale Truthfulness in LLMs,” AAAI, 2024.",
        "[39] Z. Gou et al., “CRITIC: Tool-Interactive Self-Correction,” ICLR, 2024.",
        "[40] G. Agrawal et al., “Can Knowledge Graphs Reduce Hallucinations?,” NAACL, 2024.",
    ]

    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_table.png")
    add_gold_title(slide, "REFERENCES (ALL 40 REVIEWED PAPERS)", left=1.0, top=0.20, width=17.0, size=42, align=PP_ALIGN.LEFT)

    for col_idx, ref_chunk in enumerate([refs_part1, refs_part2]):
        left_pos = 0.65 if col_idx == 0 else 10.10
        tb = slide.shapes.add_textbox(Inches(left_pos), Inches(1.72), Inches(9.25), Inches(8.95))
        tf = tb.text_frame
        tf.word_wrap = True
        for idx, line in enumerate(ref_chunk):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.space_after = Pt(2.5)
            p.line_spacing = 1.08
            r = p.add_run()
            r.text = line
            r.font.name = FONT_SANS
            r.font.size = Pt(13.2)
            r.font.bold = True
            r.font.color.rgb = INK_SLATE


def build_slide_32_thank_you(prs):
    """Slide 32: Thank You."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg_image(slide, "bg_title.png")

    shield_path = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_path.exists():
        slide.shapes.add_picture(str(shield_path), Inches(0.55), Inches(1.45), width=Inches(5.25))

    tb = slide.shapes.add_textbox(Inches(5.85), Inches(3.55), Inches(13.2), Inches(3.3))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "THANK YOU"
    r.font.name = FONT_TITLE
    r.font.size = Pt(92)
    r.font.bold = True
    r.font.color.rgb = HERO_GOLD

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(14)
    r2 = p2.add_run()
    r2.text = "Yogesh Ravi M (22MIA1052)  |  Guided by Dr. Pradeep Kumar T S"
    r2.font.name = FONT_TITLE
    r2.font.size = Pt(27)
    r2.font.bold = True
    r2.font.color.rgb = WHITE

    scope_path = ASSETS_DIR / "illus_telemetry_scope.png"
    if scope_path.exists():
        slide.shapes.add_picture(str(scope_path), Inches(15.95), Inches(6.25), width=Inches(3.65))


# ---------------------------------------------------------------------------
# Export & Main
# ---------------------------------------------------------------------------
def export_pptx_to_pdf(pptx_path: Path, pdf_path: Path):
    ps_script = f"""
$ErrorActionPreference = 'Stop'
$ppt = New-Object -ComObject PowerPoint.Application
try {{
    $pres = $ppt.Presentations.Open('{str(pptx_path.resolve())}', $true, $false, $false)
    $pres.SaveAs('{str(pdf_path.resolve())}', 32)
    $pres.Close()
}} finally {{
    $ppt.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($ppt) | Out-Null
}}
"""
    subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps_script],
        check=True,
        timeout=150,
    )


def main():
    SUBMISSION_DIR.mkdir(parents=True, exist_ok=True)

    prs = Presentation()
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)

    build_slide_01_title(prs)                              # Slide 1: Title Slide (Sandhya Slide 1)
    build_slide_02_outline(prs)                            # Slide 2: Outline (32 Slides)
    build_slide_03_intro_and_taxonomy(prs)                 # Slide 3: Introduction & Hallucination Taxonomy (Sandhya Slides 2-4)
    build_slide_04_why_tinyllama_and_gpt2(prs)             # Slide 4: Why TinyLlama-1.1B & GPT-2 (3 Simple Reasons + ₹0 Cost)
    build_literature_slides(prs)                           # Slides 5 to 11: Literature Review (All 40 Papers in 7 Slides)
    build_slide_12_problem_and_gap(prs)                    # Slide 12: Problem Statement & Research Gap (Sandhya Slides 9 & 11)
    build_slide_13_challenges_and_objectives(prs)          # Slide 13: Research Objectives & Challenges (Sandhya Slides 10 & 17)
    build_slide_17_architecture_overview(prs)              # Slide 14: High-Level Architecture (Sandhya Slide 12)
    build_slide_18_proposed_architecture_blueprint(prs)    # Slide 15: Proposed 12-Stage Architecture Blueprint (Sandhya Slide 13)
    build_slide_20_telemetry_details(prs)                  # Slide 16: Dataset Format & PyTorch Extraction Pipeline (Sandhya Slides 14-15)
    build_slide_21_why_4sensor_oof(prs)                    # Slide 17: Model Training, Calibration & Log-Odds XAI (Sandhya Slide 16)
    build_slide_21b_simple_terms_glossary(prs)             # Slide 18: Key Technical Terms in Simple Words (Viva Glossary)
    build_slide_22_results_sensor_mask(prs)                # Slide 19: Results Discussion — Token Sensor Mask (Sandhya Slide 18)
    build_slide_23_results_baseline_vs_calibrated(prs)     # Slide 20: Results Discussion — Baseline vs Calibrated Risk (Sandhya Slide 19)
    build_slide_24_results_terminal_roi(prs)               # Slide 21: Results Discussion — Log-Odds Diagnostic Trace (Sandhya Slide 20)
    build_slide_22a_colab_detection_benchmarks(prs)        # Slide 22: Results Discussion — 4-Benchmark AUROC & Transfer Plot
    build_slide_22b_colab_sensor_ablation(prs)             # Slide 23: Results Discussion — Sensor Ablation Study Plot
    build_slide_27b_colab_mitigation_plot(prs)             # Slide 24: Results Discussion — Live TriviaQA Mitigation Plot
    build_slide_27c_colab_latency_plot(prs)                # Slide 25: Results Discussion — Tesla T4 GPU & CPU Latency Plot
    build_slide_25_table_telemetry_features(prs)           # Slide 26: Results Discussion — Extracted Telemetry Table (Sandhya Slide 21)
    build_slide_26_table_performance_metrics(prs)          # Slide 27: Results Discussion — Performance Metrics Table (Sandhya Slide 22)
    build_slide_27_results_webapp_ui(prs)                  # Slide 28: Results Discussion — Prototype Web Interface (Sandhya Slide 23)
    build_slide_28_comparison_and_real_world_cost(prs)     # Slide 29: Comparison with Existing Works & ₹0 Deployment (Sandhya Slides 24-25)
    build_slide_30_conclusion_and_future_work(prs)         # Slide 30: Conclusion, Limitations & Future Work (Sandhya Slides 26-27)
    build_slide_31_references(prs)                         # Slide 31: Complete 40 References (Sandhya Slide 28)
    build_slide_32_thank_you(prs)                          # Slide 32: Thank You (Sandhya Slide 29)

    prs.save(str(OUT_PPTX))
    print(f"[OK] Saved Sandhya-style PPTX ({len(prs.slides)} slides): {OUT_PPTX}")

    export_pptx_to_pdf(OUT_PPTX, OUT_PDF)
    print(f"[OK] Exported PDF: {OUT_PDF}")

    for dest_dir in (ROOT_DIR, CAPSTONE_DIR):
        shutil.copy2(OUT_PPTX, dest_dir / "FINAL_PRESENTATION.pptx")
        shutil.copy2(OUT_PDF, dest_dir / "FINAL_PRESENTATION.pdf")
    print("[OK] Mirrored FINAL_PRESENTATION.pptx & .pdf to ROOT and CAPSTONE.")


if __name__ == "__main__":
    main()
