# -*- coding: utf-8 -*-
"""
Builds the 30-Slide Master Final Review Presentation (FINAL_TRUEGUARD_PRESENTATION.pptx & .pdf)
Strictly complying with all university requirements:
- Exactly 30 Slides
- Exactly 4 Literature Review Slides covering all 40 papers (10 papers per slide)
- All 6 research figures integrated in print-perfect 600 DPI
- Comprehensive academic speaker notes on every single slide
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

# Add current tools directory to sys.path
sys.path.insert(0, str(Path(r"E:\trueguard\CAPSTONE\FInal\tools")))
from presentation_helpers import (
    set_slide_background, add_header_banner, add_speaker_notes,
    create_card, add_table_grid,
    NAVY_HEADER, ROYAL_BLUE, AMBER_GOLD, EMERALD_GREEN, CRIMSON_RED,
    PURE_WHITE, DARK_SLATE, MUTED_SLATE, LIGHT_BG, BORDER_COLOR,
    FONT_TITLE, FONT_BODY, FONT_BOLD
)

ROOT_DIR = Path(r"E:\trueguard")
CAPSTONE_DIR = ROOT_DIR / "CAPSTONE"
FINAL_DIR = CAPSTONE_DIR / "FInal"
SUBMISSION_DIR = ROOT_DIR / "FINAL_SUBMISSION"
ASSETS_DIR = FINAL_DIR / "assets_sandhya_style"
FIG_DIR = ROOT_DIR / "outputs" / "figures"

OUT_PPTX = ROOT_DIR / "FINAL_TRUEGUARD_PRESENTATION.pptx"
OUT_PDF = ROOT_DIR / "FINAL_TRUEGUARD_PRESENTATION.pdf"

# Import literature review data (40 papers)
from generate_final_presentation import LIT_SLIDES_DATA

def main():
    prs = Presentation()
    prs.slide_width = Inches(20.0)
    prs.slide_height = Inches(11.25)
    
    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Hero Widescreen)
    # -------------------------------------------------------------------------
    s1 = prs.slides.add_slide(prs.slide_layouts[6])
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(11.25))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY_HEADER
    bg1.line.fill.background()
    
    # Hero Title Box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(17.6), Inches(4.5))
    tf1 = tbox.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "TOWARD TRUSTWORTHY LARGE LANGUAGE MODELS:"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "A Real-Time, Internal-State-Based Hallucination Detection & Closed-Loop Mitigation Framework (TRUEGUARD)"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = PURE_WHITE
    p.space_after = Pt(25)
    
    p = tf1.add_paragraph()
    p.text = "Final Year Capstone Project Defense | School of Computer Science & Engineering (SCOPE)"
    p.font.name = FONT_BODY
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(148, 163, 184)
    
    # Candidate & Guide Card
    c_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(6.8), Inches(11.0), Inches(3.2))
    c_card.fill.solid()
    c_card.fill.fore_color.rgb = RGBColor(30, 41, 59)
    c_card.line.color.rgb = AMBER_GOLD
    c_card.line.width = Pt(1.5)
    ctf = c_card.text_frame
    ctf.word_wrap = True
    
    cp = ctf.paragraphs[0]
    cp.text = "PROJECT INVESTIGATOR & GUIDANCE"
    cp.font.name = FONT_BOLD
    cp.font.size = Pt(14)
    cp.font.bold = True
    cp.font.color.rgb = AMBER_GOLD
    cp.space_after = Pt(12)
    
    cp = ctf.add_paragraph()
    cp.text = "Candidate:  Yogesh Ravi M  (Reg. No: 22MIA1052)\nProgramme:  Integrated M.Tech Computer Science & Engineering (Data Science)"
    cp.font.name = FONT_BODY
    cp.font.size = Pt(16)
    cp.font.color.rgb = PURE_WHITE
    cp.space_after = Pt(10)
    
    cp = ctf.add_paragraph()
    cp.text = "Faculty Guide:  Dr. Pradeep Kumar T.S., Professor (SCOPE, VIT Chennai)\nInstitution:  Vellore Institute of Technology, Chennai Campus"
    cp.font.name = FONT_BODY
    cp.font.size = Pt(16)
    cp.font.color.rgb = RGBColor(226, 232, 240)
    
    # Shield illustration if present
    shield_img = ASSETS_DIR / "illus_ai_core_shield.png"
    if shield_img.exists():
        s1.shapes.add_picture(str(shield_img), Inches(13.2), Inches(6.2), width=Inches(5.5), height=Inches(4.0))
        
    add_speaker_notes(s1, """
Good morning respected examiners and faculty guide Dr. Pradeep Kumar T.S. 
I am Yogesh Ravi M (Registration Number 22MIA1052). Today, I present our research project: TRUEGUARD: A Real-Time, Internal-State-Based Hallucination Detection and Closed-Loop Mitigation Framework.
Large Language Models have revolutionized artificial intelligence, but their critical flaw remains hallucinations—generating fluent, authoritative statements that are factually false. 
In this defense, I present our novel white-box guardrail framework that extracts internal transformer activations across 4 distinct physical sensors, computes calibrated hallucination risk in single forward passes (+2.91 ms latency), and actuates a closed-loop 3-tier controller that drops hallucinations by 83.6% on live queries.
""")

    # -------------------------------------------------------------------------
    # SLIDE 2: Presentation Outline (30 Slides Roadmap)
    # -------------------------------------------------------------------------
    s2 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s2)
    add_header_banner(s2, "PRESENTATION OUTLINE & DEFENSE ROADMAP", "OVERVIEW")
    
    sections = [
        ("01. FOUNDATIONS", "Slides 03–05", "LLM Hallucinations, Intrinsic vs Extrinsic Taxonomy, Problem Statement, & Research Objectives"),
        ("02. LITERATURE REVIEW", "Slides 06–11", "Systematic PRISMA Review of 40 Peer-Reviewed Papers (4 Pillars) & Research Gap Analysis"),
        ("03. ARCHITECTURE & SENSORS", "Slides 12–16", "White-Box vs Black-Box, TinyLlama Plant, 4-Sensor Bank (ISP, AAS, EEM, DST) Formulation"),
        ("04. METHODOLOGY & DATASETS", "Slides 17–23", "5 Benchmarks (N=3,196), Feature Extraction, Platt Calibration, & 3-Tier Mitigation Logic"),
        ("05. EMPIRICAL RESULTS & AUDIT", "Slides 24–30", "6 Verified Research Figures: AUROC, Transfer, Ablation, ROC Curves, Latency, & viva Q&A"),
    ]
    
    for i, (stitle, sslides, sdesc) in enumerate(sections):
        card = create_card(s2, 1.0, 1.8 + i * 1.75, 18.0, 1.5, bg_color=PURE_WHITE, border_color=BORDER_COLOR)
        # Number pill
        pill = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(2.05 + i * 1.75), Inches(3.2), Inches(0.95))
        pill.fill.solid()
        pill.fill.fore_color.rgb = ROYAL_BLUE
        pill.line.fill.background()
        ptf = pill.text_frame
        ptf.text = f"{stitle}\n{sslides}"
        ptf.paragraphs[0].alignment = PP_ALIGN.CENTER
        ptf.paragraphs[0].font.name = FONT_BOLD
        ptf.paragraphs[0].font.size = Pt(13)
        ptf.paragraphs[0].font.bold = True
        ptf.paragraphs[0].font.color.rgb = PURE_WHITE
        
        # Text box
        tb = s2.shapes.add_textbox(Inches(4.8), Inches(1.95 + i * 1.75), Inches(13.8), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = sdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s2, """
This presentation is organized into 5 logical sections spanning exactly 30 slides:
Section 1 introduces the LLM hallucination problem, taxonomy, and research objectives.
Section 2 presents our 40-paper PRISMA literature review across 4 distinct slides (10 papers each) and establishes our research gaps.
Section 3 details the TRUEGUARD white-box architecture and the mathematical formulation of our four internal sensors.
Section 4 covers dataset curation across 5 benchmarks (N=3,196), feature extraction, Platt scaling calibration, and the 3-tier controller.
Section 5 walks through the empirical evaluation across all 6 verified publication figures, hardware latency, deployment constraints, and conclusions.
""")

    # -------------------------------------------------------------------------
    # SLIDE 3: LLMs and Hallucination Taxonomy
    # -------------------------------------------------------------------------
    s3 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s3)
    add_header_banner(s3, "LLM HALLUCINATION TAXONOMY & EMPIRICAL EVIDENCE", "FOUNDATIONS")
    
    # Left Card: Taxonomy
    card_l = create_card(s3, 0.8, 1.8, 10.5, 8.8, PURE_WHITE)
    tb = s3.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.9), Inches(8.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "The Fundamental Nature of LLM Hallucinations"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    bullets = [
        ("Autoregressive Next-Token Prediction:", "LLMs generate tokens greedily or stochastically using P(y_t | y_<t, x). They lack an internal ground-truth verification engine. Plausibility is optimized, not truth."),
        ("Intrinsic Hallucinations:", "The generated output directly contradicts facts established in the user-provided input prompt or source context (common in summarization and multi-turn dialogue)."),
        ("Extrinsic Hallucinations:", "The generated output introduces fabricated, unsubstantiated claims that cannot be verified from world knowledge or the prompt (e.g. inventing authors, dates, or biomedical cures)."),
        ("The Overconfidence Trap:", "Modern calibrated studies (Ji et al., 2023; Farquhar et al., 2024) prove that models hallucinate with high softmax probabilities, making raw token probabilities deceptive for safety.")
    ]
    for b_title, b_desc in bullets:
        p = tf.add_paragraph()
        p.text = f"• {b_title} "
        p.font.name = FONT_BOLD
        p.font.size = Pt(15.5)
        p.font.bold = True
        p.font.color.rgb = DARK_SLATE
        
        run = p.add_run()
        run.text = b_desc
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    # Right Card: Concrete Visual Example
    card_r = create_card(s3, 11.6, 1.8, 7.6, 8.8, LIGHT_BG)
    tb_r = s3.shapes.add_textbox(Inches(11.9), Inches(2.1), Inches(7.0), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Concrete High-Risk Example (TruthfulQA)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "User Prompt:\n\"What happens if you swallow a watermelon seed?\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(12)
    
    p = tf_r.add_paragraph()
    p.text = "Blind LLM Emission (Hallucination):\n\"Watermelon seeds will germinate in your stomach acid, causing vines to sprout through your intestines.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14.5)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "TRUEGUARD Detection & Correction:\n• ISP Probe: Detects ungrounded semantic state at Layer 16.\n• Risk Score: r = 0.941 (Exceeds Fault Threshold tau_fault = 0.898).\n• Tier 1 Active Repair Output:\n\"Watermelon seeds pass through the digestive system harmlessly and do not germinate in gastric acid.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = EMERALD_GREEN
    
    add_speaker_notes(s3, """
Slide 3 establishes the foundation. Hallucination in Large Language Models is not an accidental software bug; it is an intrinsic consequence of autoregressive next-token optimization. The model maximizes probability over fluent token sequences rather than factual truth.
We distinguish between intrinsic hallucinations, where the model contradicts the provided context, and extrinsic hallucinations, where the model fabricates external entities.
Crucially, as shown on the right card, when asked common human misconception questions from TruthfulQA, blind LLMs produce confident falsehoods. TRUEGUARD intercepts this generation before it reaches the user.
""")

    # -------------------------------------------------------------------------
    # SLIDE 4: Problem Statement & Published Research Evidence
    # -------------------------------------------------------------------------
    s4 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s4)
    add_header_banner(s4, "PROBLEM STATEMENT & PUBLISHED RESEARCH EVIDENCE", "FOUNDATIONS")
    
    card1 = create_card(s4, 0.8, 1.8, 18.4, 8.8, PURE_WHITE)
    tb = s4.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(17.6), Inches(8.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "The Problem: Why Existing Hallucination Detectors Fail in Real-Time Applications"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    probs = [
        ("1. Surface Logit Polarity Inversion (Kadavath et al., 2022; Farquhar et al., 2024):",
         "On complex dialogue and open-domain QA (HaluEval), raw token entropy inverts its diagnostic correlation. Models hallucinate with lower entropy and higher confidence than when stating nuanced truths. Surface metrics collapse to AUROC < 0.50 (worse than random guessing)."),
        ("2. Single-Layer Probing Blindness (Azaria & Mitchell, 2023; Marks & Tegmark, 2023):",
         "Probing a single middle layer captures static linear truthfulness for short declarative facts, but fails completely on long-form generation where attention dispersion and semantic drift occur across multi-token spans."),
        ("3. The Multi-Sample Latency Bottleneck (Manakul et al., 2023 - SelfCheckGPT):",
         "Zero-resource sampling techniques require drawing 5 to 20 stochastic completions to measure consistency. This incurs 500% to 2000% computational overhead (+134 ms/token), making real-time interactive chat impossible on affordable hardware."),
        ("4. The Detection-Mitigation Disconnect (Ji et al., 2023; Lin et al., 2024):",
         "Prior research treats detection and mitigation as isolated disciplines. Passive detectors score text post-hoc without fixing errors; aggressive steering vectors distort natural language fluency without retrieving missing factual knowledge.")
    ]
    for p_title, p_desc in probs:
        p = tf.add_paragraph()
        p.text = p_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(16)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        
        p = tf.add_paragraph()
        p.text = p_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(14.5)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(14)
        
    add_speaker_notes(s4, """
Slide 4 defines our core problem statement supported by published peer-reviewed evidence.
Why was TRUEGUARD needed? 
First, surface token probabilities invert under benchmark answer-length asymmetries. On HaluEval-QA, raw token entropy achieves only 0.349 AUROC—worse than flipping a coin!
Second, single-layer probes miss attention dispersion and semantic drift.
Third, black-box sampling methods like SelfCheckGPT require 5 to 20 passes per query, which costs over 160 ms per token and bankrupts real-time deployments.
Finally, existing tools are open-loop: they flag an error but cannot safely repair it.
""")

    # -------------------------------------------------------------------------
    # SLIDE 5: Research Objectives & Two Academic Papers
    # -------------------------------------------------------------------------
    s5 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s5)
    add_header_banner(s5, "RESEARCH OBJECTIVES & RESEARCH PAPER FOUNDATIONS", "FOUNDATIONS")
    
    # Left Card: Objectives
    card_l = create_card(s5, 0.8, 1.8, 9.8, 8.8, PURE_WHITE)
    tb_l = s5.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.2), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Four Specific Research Objectives"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    objs = [
        ("Objective 1: Multi-Sensor Internal Telemetry Bank", "Design a lightweight, single-pass forward-hook extractor tracking 4 internal physical mechanisms: intermediate hidden probes (ISP), attention dispersion (AAS), hybrid Shannon/Renyi-2 entropy (EEM), and directional semantic drift (DST)."),
        ("Objective 2: Calibrated Logistic Fusion & Attribution", "Construct a standardized L2-regularized logistic combiner with Platt scaling to map the pooled 4-sensor representation into a calibrated risk probability r in [0, 1] with exact per-sensor log-odds attributions."),
        ("Objective 3: Three-Tier Closed-Loop Mitigation Controller", "Implement an actuation engine that routes queries based on two empirical thresholds (tau_warn = 0.611, tau_fault = 0.898) into Safe Pass, Annealed Re-Sampling, Targeted RAG Active Repair, or Calibrated Abstention."),
        ("Objective 4: Cross-Benchmark & Cross-Backbone Validation", "Evaluate detection AUROC across 4 diverse benchmarks (N=3,196), evaluate cross-domain transfer matrices, validate on TinyLlama-1.1B and GPT-2 (124M), and profile hardware latency on an NVIDIA Tesla T4 GPU.")
    ]
    for o_title, o_desc in objs:
        p = tf_l.add_paragraph()
        p.text = o_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_SLATE
        
        p = tf_l.add_paragraph()
        p.text = o_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(10)
        
    # Right Card: Academic Research Papers
    card_r = create_card(s5, 11.0, 1.8, 8.2, 8.8, LIGHT_BG)
    tb_r = s5.shapes.add_textbox(Inches(11.3), Inches(2.1), Inches(7.6), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Two Academic Research Papers Produced"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "PAPER 1: System Architecture & Detection\n\"TRUEGUARD: A Real-Time, Internal-State-Based LLM Hallucination Detection Framework via Multi-Sensor Probing and Calibrated Risk Fusion\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14.5)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(8)
    
    p = tf_r.add_paragraph()
    p.text = "Focus: Formulates the 4 internal sensors, mathematical derivations of AAS/EEM/DST, 5-fold grouped cross-validation, and multi-benchmark AUROC on TinyLlama-1.1B (Macro AUROC 0.893)."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = MUTED_SLATE
    p.space_after = Pt(16)
    
    p = tf_r.add_paragraph()
    p.text = "PAPER 2: Closed-Loop Mitigation & Selective Prediction\n\"Closed-Loop Hallucination Mitigation and Selective Prediction in Autoregressive Language Models via Calibrated Three-Tier Actuation\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(14.5)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(8)
    
    p = tf_r.add_paragraph()
    p.text = "Focus: Closed-loop control theory formulation, TriviaQA live actuation, 83.6% hallucination drop, selective prediction risk-coverage analysis (AURC = 0.198), and T4 GPU hardware latency profiling (+2.91 ms/token)."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = MUTED_SLATE
    
    add_speaker_notes(s5, """
Slide 5 articulates our 4 research objectives and links them directly to the two research papers written for this capstone.
Objective 1 builds the 4-sensor internal bank.
Objective 2 implements calibrated risk fusion and explainable log-odds attribution.
Objective 3 delivers the closed-loop 3-tier controller.
Objective 4 provides rigorous cross-benchmark and hardware validation.
Paper 1 focuses on the internal state representation and detection metrics. Paper 2 establishes the closed-loop control framework, selective prediction, and empirical latency benchmarking.
""")

    # -------------------------------------------------------------------------
    # SLIDES 6 to 9: Literature Review (Exactly 4 Slides, 10 Papers Each = 40 Papers)
    # -------------------------------------------------------------------------
    lit_headers = ["No.", "Author(s), Year & Venue", "Method / Architecture", "Key Academic Contribution", "Research Gap / Limitation"]
    lit_col_widths = [0.8, 3.6, 4.2, 4.9, 4.9]
    
    all_40 = [p for chunk in LIT_SLIDES_DATA for p in chunk]
    chunks_10 = [all_40[i:i+10] for i in range(0, 40, 10)]
    
    pillar_names = [
        "PILLAR 1: INTERNAL STATE PROBING & REPRESENTATION GEOMETRY (PAPERS 1–10)",
        "PILLAR 2: ATTENTION ANOMALIES & INFORMATION ENTROPY (PAPERS 11–20)",
        "PILLAR 3: CLOSED-LOOP FEEDBACK & SELECTIVE MITIGATION (PAPERS 21–30)",
        "PILLAR 4: FACTUALITY BENCHMARKS, CALIBRATION & SAFETY (PAPERS 31–40)"
    ]
    
    for idx, (p_name, papers) in enumerate(zip(pillar_names, chunks_10)):
        slide_no = 6 + idx
        s_lit = prs.slides.add_slide(prs.slide_layouts[6])
        set_slide_background(s_lit)
        add_header_banner(s_lit, p_name, f"LITERATURE REVIEW (SLIDE {idx+1} OF 4)")
        
        # Add 10-row table
        add_table_grid(s_lit, 0.8, 1.65, 18.4, 9.1, lit_headers, papers, lit_col_widths, header_fs=12.0, cell_fs=10.0)
        
        add_speaker_notes(s_lit, f"""
Slide {slide_no} represents {p_name}.
All 10 papers in this slide have been systematically reviewed following PRISMA 2020 guidelines.
Notice the research progression: earlier works (such as Azaria & Mitchell, 2023; Burns et al., 2022; Su et al., 2024) proved that middle-layer hidden states contain linear truth directions. However, every existing method identified in column 5 suffered from critical limitations: either single-signal vulnerability, passive scoring with zero mitigation, or reliance on expensive multi-sample generation.
TRUEGUARD directly synthesizes the strengths of these works while eliminating their individual failure modes.
""")

    # -------------------------------------------------------------------------
    # SLIDE 10: Research Gaps Identified
    # -------------------------------------------------------------------------
    s10 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s10)
    add_header_banner(s10, "SYSTEMATIC RESEARCH GAPS IDENTIFIED ACROSS 40 PAPERS", "RESEARCH GAPS")
    
    gaps = [
        ("GAP 1: SINGLE-SIGNAL FRAGILITY & UNIMODAL SENSING",
         "Existing detectors rely on a single physical mechanism: either middle-layer hidden activations (SAPLMA, MIND) OR token entropy (Kadavath) OR attention weights. No prior framework fuses all four complementary internal signals into a single unified state observer."),
        ("GAP 2: SIGNAL POLARITY INVERSION UNDER ASYMMETRY",
         "On datasets where answer length or sentence structure differs between true and hallucinated classes (HaluEval-QA, Dialogue), raw token entropy inverts its diagnostic correlation (AUROC drops to 0.349). Supervised linear projection and recalibration are mandatory to enforce positive diagnostic alignment."),
        ("GAP 3: MULTI-SAMPLE INFERENCE-TIME COMPUTATIONAL OVERHEAD",
         "Black-box consistency baselines (SelfCheckGPT, SAC3) require drawing 5 to 20 full autoregressive completions per query. This increases latency by 500% to 2000% (+134 ms/token), rendering them economically and computationally infeasible for interactive production."),
        ("GAP 4: OPEN-LOOP DETECTION WITHOUT CLOSED-LOOP FEEDBACK CONTROL",
         "Prior works operate as disconnected silos: detectors compute a passive risk score without intervention; activation steering methods (ITI) distort fluency without retrieving factual context. A principled 3-tier closed-loop feedback controller was entirely missing from literature.")
    ]
    
    for i, (g_title, g_desc) in enumerate(gaps):
        card = create_card(s10, 0.8, 1.8 + i * 2.2, 18.4, 1.95, PURE_WHITE)
        tb = s10.shapes.add_textbox(Inches(1.1), Inches(1.9 + i * 2.2), Inches(17.8), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = g_title
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = CRIMSON_RED if i < 2 else ROYAL_BLUE
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = g_desc
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s10, """
Slide 10 synthesizes the four structural research gaps exposed by our PRISMA literature review.
Gap 1 is single-signal blindness: hidden state probes miss attention dispersion; attention monitors miss semantic drift.
Gap 2 is polarity inversion: entropy drops when the model hallucinates with high confidence, producing deceptive signals.
Gap 3 is the multi-sample latency explosion of black-box sampling.
Gap 4 is open-loop operation: detection without corrective feedback.
These four gaps form the direct engineering requirements for TRUEGUARD.
""")

    # -------------------------------------------------------------------------
    # SLIDE 11: Existing Methods vs. TRUEGUARD
    # -------------------------------------------------------------------------
    s11 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s11)
    add_header_banner(s11, "COMPARATIVE FEATURE MATRIX: EXISTING METHODS VS. TRUEGUARD", "BENCHMARK COMPARISON")
    
    comp_headers = ["Framework / Baseline", "Target Mechanism", "Internal Access", "Runtime Overhead", "Closed-Loop Mitigation", "Macro AUROC (TinyLlama)"]
    comp_col_widths = [3.2, 3.8, 2.8, 2.8, 3.0, 2.8]
    comp_rows = [
        ["SelfCheckGPT (Manakul, 2023)", "Multi-Sample Semantic Consistency", "Black-Box API (Sampling)", "+500% to +2000% Latency", "None (Passive Scoring)", "0.684 (Severe Cost)"],
        ["SAPLMA (Azaria, 2023)", "Single Middle-Layer Hidden Probe", "White-Box (Layer L/2)", "< 5% (Single Pass)", "None (Passive Classifier)", "0.762 (Fails on QA)"],
        ["ITI (Li et al., 2023)", "Attention Head Activation Steering", "White-Box (Attention Heads)", "+8% (Fixed Steering)", "Hard Activation Shift", "Fluency Loss / Ungrounded"],
        ["INSIDE (Chen et al., 2024)", "Eigen-Space Hidden Dispersion", "White-Box (Matrix Covariance)", "+25% (SVD Computation)", "None (Detection Only)", "0.791 (High Compute)"],
        ["DoLa (Chuang et al., 2024)", "Layer-Contrastive Token Decoding", "White-Box (Logit Contrast)", "+15% (Dual Decode)", "Contrastive Decoding", "0.745 (QA Specific)"],
        ["TRUEGUARD (Proposed)", "4-Sensor Bank (ISP+AAS+EEM+DST)", "White-Box (Forward Hooks)", "+8.7% (+2.91 ms/token)", "3-Tier Closed-Loop Feedback", "0.893 (Macro Average)"]
    ]
    
    add_table_grid(s11, 0.8, 1.8, 18.4, 8.8, comp_headers, comp_rows, comp_col_widths, header_fs=13.0, cell_fs=12.0)
    
    add_speaker_notes(s11, """
Slide 11 provides an empirical feature matrix directly comparing TRUEGUARD against prior state-of-the-art methods.
Notice that SelfCheckGPT incurs 5 to 20 passes per query (+500% to +2000% latency). SAPLMA only probes a single layer and achieves 0.762 AUROC. ITI applies fixed steering vectors that degrade natural language fluency.
TRUEGUARD is the only framework that achieves high detection performance (0.893 Macro AUROC) with lightweight overhead (+2.91 ms/token, +8.7%) while providing a verified 3-tier closed-loop feedback controller.
""")

    # -------------------------------------------------------------------------
    # SLIDE 12: TinyLlama & White-Box Architecture
    # -------------------------------------------------------------------------
    s12 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s12)
    add_header_banner(s12, "TINYLLAMA-1.1B FOUNDATION MODEL & WHITE-BOX ACCESS", "ARCHITECTURE")
    
    card_l = create_card(s12, 0.8, 1.8, 10.5, 8.8, PURE_WHITE)
    tb = s12.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.9), Inches(8.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Why TinyLlama-1.1B & Open-Weight Architectures?"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    reasons = [
        ("Identical Llama-2 Architecture:", "TinyLlama-1.1B-Chat-v1.0 implements the exact architectural paradigm of modern production LLMs: RMSNorm, SwiGLU activations, Rotary Positional Embeddings (RoPE), and Grouped-Query Attention across 22 layers, 2048 hidden dimension, and 32 attention heads."),
        ("Scientifically Reproducible Research:", "Unlike closed APIs (ChatGPT, Claude, Gemini) whose internal weights change without warning and whose activations are proprietary secrets, TinyLlama provides frozen, reproducible PyTorch tensor access."),
        ("Strict Resource Feasibility (Rs. 0 Cloud Cost):", "TinyLlama fits comfortably into standard 15GB GPU VRAM (free Google Colab Tesla T4 GPU) in 16-bit precision, enabling complete experimental transparency without requiring multi-GPU server clusters."),
        ("Cross-Scale Architectural Generalization:", "Probes and sensors trained on TinyLlama utilize normalized hidden representations that generalize directly to Llama-2-7B, Llama-3-8B, and Mistral-7B foundation models.")
    ]
    for r_title, r_desc in reasons:
        p = tf.add_paragraph()
        p.text = f"• {r_title} "
        p.font.name = FONT_BOLD
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_SLATE
        
        run = p.add_run()
        run.text = r_desc
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    # Right Card: Why White-Box is Required (ChatGPT vs Open Models)
    card_r = create_card(s12, 11.6, 1.8, 7.6, 8.8, LIGHT_BG)
    tb_r = s12.shapes.add_textbox(Inches(11.9), Inches(2.1), Inches(7.0), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Why White-Box Probing is Essential"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Closed-Box API Limitations (ChatGPT / Claude):\n• Commercial APIs hide intermediate hidden activations (h_l).\n• Attention weights (A_l,h) and KV caches are inaccessible.\n• Developers only receive output text strings, forcing expensive multi-call black-box sampling."
    p.font.name = FONT_BODY
    p.font.size = Pt(14.5)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "TRUEGUARD White-Box Advantage:\n• Directly hooks Layer 16 hidden states, all 32 attention heads, and token logit distributions.\n• Extracts full diagnostic telemetry in a single forward pass.\n• Ideal for enterprise on-premise foundation models (Llama-3, Mistral, TinyLlama) deployed on private infrastructure."
    p.font.name = FONT_BODY
    p.font.size = Pt(14.5)
    p.font.color.rgb = EMERALD_GREEN
    
    add_speaker_notes(s12, """
Slide 12 addresses a critical viva question: Why TinyLlama-1.1B, and why white-box access?
Examiners often ask: 'Can we integrate TRUEGUARD into ChatGPT or Gemini?'
The answer is definitively NO, because commercial APIs are proprietary black boxes that strictly hide their internal hidden activations and attention matrices.
TRUEGUARD is designed for self-hosted enterprise foundation models (such as Llama-3, Mistral, or TinyLlama) deployed on private hospital, banking, or defense servers.
TinyLlama features the exact Llama-2 architecture—RMSNorm, RoPE, SwiGLU, 22 layers, 2048 hidden dimensions—making our mathematical formulations directly transferable to larger 7B and 70B models.
""")

    # -------------------------------------------------------------------------
    # SLIDE 13: TRUEGUARD Architecture Blueprint
    # -------------------------------------------------------------------------
    s13 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s13)
    add_header_banner(s13, "PROPOSED TRUEGUARD ARCHITECTURE: 12-STAGE CLOSED-LOOP PIPELINE", "ARCHITECTURE")
    
    # Insert 12-stage blueprint image if available, else draw structured flow
    bp_img = ASSETS_DIR / "fig_blueprint_12stage.png"
    if bp_img.exists():
        s13.shapes.add_picture(str(bp_img), Inches(0.8), Inches(1.8), width=Inches(18.4), height=Inches(8.8))
    else:
        card = create_card(s13, 0.8, 1.8, 18.4, 8.8, PURE_WHITE)
        tb = s13.shapes.add_textbox(Inches(1.2), Inches(2.2), Inches(17.6), Inches(8.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = "TRUEGUARD 12-Stage Closed-Loop Pipeline Overview"
        p.font.name = FONT_BOLD
        p.font.size = Pt(22)
        p.font.color.rgb = ROYAL_BLUE
        
    add_speaker_notes(s13, """
Slide 13 presents the complete 12-stage engineering blueprint of TRUEGUARD.
Stage 1: Input query reception and prompt tokenization.
Stage 2: Plant forward execution through the 22-layer transformer.
Stage 3 to 6: Single-pass physical telemetry extraction across the 4 sensors (ISP, AAS, EEM, DST) using PyTorch forward hooks.
Stage 7: Sequence pooling mapping variable-length token telemetry into fixed 4-dimensional representation vectors.
Stage 8: Standardized L2 logistic regression fusion and Platt scaling calibration computing continuous risk r(x,y).
Stage 9: Log-odds attribution decomposing risk into exact sensor percentage contributions for explainable AI.
Stage 10 to 12: Closed-loop actuation routing queries into Safe Pass, Re-Sampling, Targeted RAG, or Calibrated Refusal.
""")

    # -------------------------------------------------------------------------
    # SLIDE 14: Four-Sensor Overview
    # -------------------------------------------------------------------------
    s14 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s14)
    add_header_banner(s14, "FOUR-SENSOR INTERNAL TELEMETRY BANK: MATHEMATICAL FORMULATIONS", "SENSORS")
    
    sensor_cards = [
        ("SENSOR 1: ISP (F_t)", "Intermediate Hidden State Probe",
         "Captures high-dimensional factual truthfulness geometry before final token generation.",
         "F_t = sigma(w_probe^T h_t^{(16)} + b_probe)",
         "Probes layer l = 16 (0.73 L), where factual semantic representations are maximally separated linearly.",
         ROYAL_BLUE),
        ("SENSOR 2: AAS (A_t)", "Top-Quartile Attention Anomaly Sensor",
         "Measures attention dispersion and context neglect across multi-head attention matrices.",
         "A_t = mean_{h in H_top} [ - sum_j alpha_{t,j}^{(h)} log alpha_{t,j}^{(h)} ]",
         "High entropy across top attention heads signals that the model is generating text without attending to prompt context.",
         AMBER_GOLD),
        ("SENSOR 3: EEM (H_ent,t)", "Hybrid Shannon / Renyi-2 Energy Monitor",
         "Quantifies instantaneous predictive uncertainty and probability mass dispersion.",
         "H_ent,t = 0.6 H_Shannon(p_t) + 0.4 H_Renyi2(p_t)",
         "Renyi-2 entropy (-log sum p_i^2) emphasizes top competing candidate tokens; Shannon captures full vocabulary dispersion.",
         EMERALD_GREEN),
        ("SENSOR 4: DST (D_t)", "Directional Semantic Trajectory Drift",
         "Tracks abrupt geometric dislocations in consecutive latent token representations.",
         "D_t = 1 - (h_t^{(L)} . h_{t-1}^{(L)}) / (||h_t^{(L)}|| ||h_{t-1}^{(L)}||)",
         "Detects sudden transitions from factual context into ungrounded, fabricated narrative threads.",
         CRIMSON_RED)
    ]
    
    for i, (stitle, ssub, sdesc, sform, sexpl, scolor) in enumerate(sensor_cards):
        cx = 0.8 + (i % 2) * 9.4
        cy = 1.8 + (i // 2) * 4.5
        card = create_card(s14, cx, cy, 9.0, 4.2, PURE_WHITE, border_color=scolor)
        
        tb = s14.shapes.add_textbox(Inches(cx + 0.3), Inches(cy + 0.25), Inches(8.4), Inches(3.7))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = stitle
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = scolor
        p.space_after = Pt(2)
        
        p = tf.add_paragraph()
        p.text = ssub
        p.font.name = FONT_BOLD
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(12)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(8)
        
        p = tf.add_paragraph()
        p.text = f"Formula: {sform}"
        p.font.name = FONT_BOLD
        p.font.size = Pt(12.5)
        p.font.color.rgb = scolor
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = f"Intuition: {sexpl}"
        p.font.name = FONT_BODY
        p.font.size = Pt(11.5)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s14, """
Slide 14 provides the mathematical backbone of TRUEGUARD: our 4-sensor internal bank.
Sensor 1 (ISP) probes Layer 16 hidden states using supervised logistic regression, capturing truthfulness geometry.
Sensor 2 (AAS) computes the Shannon entropy of the attention distribution across top-quartile heads, detecting prompt neglect.
Sensor 3 (EEM) merges Shannon entropy and Renyi-2 collision entropy over the output vocabulary, measuring predictive confidence.
Sensor 4 (DST) tracks cosine distance between consecutive token embeddings, capturing semantic dislocations when the model strays off-topic.
Together, these 4 sensors form a robust, multi-dimensional physical observer of LLM inference.
""")

    # -------------------------------------------------------------------------
    # SLIDE 15: Sensor Details: ISP & AAS
    # -------------------------------------------------------------------------
    s15 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s15)
    add_header_banner(s15, "DEEP DIVE: INTERNAL STATE PROBES (ISP) & ATTENTION SENSOR (AAS)", "SENSORS")
    
    # Left Card: ISP
    card_l = create_card(s15, 0.8, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_l = s15.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Sensor 1: Multi-Layer Internal State Probe (ISP)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    isp_pts = [
        ("Layer Selection Rationale:", "In transformer architectures, early layers process syntactic and lexical features, while final layers prepare vocabulary distributions. Factual representations crystallize in intermediate layers. We probe layer l = 16 of 22 (0.73 L)."),
        ("Mathematical Formulation:", "h_t^{(16)} in R^{2048}. The supervised probe projects this latent vector via learned weights w_probe in R^{2048} and bias b_probe:\nF_t = 1 / (1 + exp(-(w_probe^T h_t^{(16)} + b_probe)))"),
        ("Token Sequence Pooling:", "For an answer sequence of length T, we compute both sequence mean and max: F_{mean} = (1/T) sum F_t, F_{max} = max_t F_t. Max captures localized factual hallucinations; mean captures overall narrative truthfulness.")
    ]
    for pt_t, pt_d in isp_pts:
        p = tf_l.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_l.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    # Right Card: AAS
    card_r = create_card(s15, 10.2, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_r = s15.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Sensor 2: Attention Anomaly Sensor (AAS)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(14)
    
    aas_pts = [
        ("Attention Dispersion Hypothesis:", "When an LLM generates grounded tokens, attention weights focus sharply on relevant context tokens. When hallucinating, attention becomes diffuse or fixates on generic syntax tokens."),
        ("Head Selection (Top Quartile):", "TinyLlama has 32 attention heads. We rank heads by empirical sensitivity and monitor the top quartile H_top (8 heads):\nA_t = (1/|H_top|) sum_{h in H_top} H(alpha_{t,:}^{(h)})"),
        ("Diagnostic Independence:", "AAS provides complete mathematical orthogonality to ISP. While ISP inspects WHAT concepts are encoded, AAS inspects WHERE the model is looking in the context window.")
    ]
    for pt_t, pt_d in aas_pts:
        p = tf_r.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_r.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    add_speaker_notes(s15, """
Slide 15 breaks down Sensors 1 and 2 in detail.
Examiners will ask: Why layer 16? In 22-layer TinyLlama, layer 16 corresponds to 73% network depth. Literature (Azaria & Mitchell, 2023; Zou et al., 2023) proves that truthfulness representations peak around 70-80% depth before final logit projection.
For AAS, we filter the top quartile of attention heads because averaging across all 32 heads dilutes the signal with generic syntax-tracking heads.
""")

    # -------------------------------------------------------------------------
    # SLIDE 16: Sensor Details: EEM & DST
    # -------------------------------------------------------------------------
    s16 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s16)
    add_header_banner(s16, "DEEP DIVE: ENERGY-ENTROPY (EEM) & SEMANTIC TRAJECTORY (DST)", "SENSORS")
    
    # Left Card: EEM
    card_l = create_card(s16, 0.8, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_l = s16.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Sensor 3: Energy-Entropy Monitor (EEM)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(14)
    
    eem_pts = [
        ("Hybrid Shannon & Renyi-2 Formulation:", "Standard Shannon entropy H_Shannon = -sum p_i log p_i weights all vocabulary tokens equally. Renyi-2 collision entropy H_Renyi2 = -log sum p_i^2 places heavy geometric weight on top competing logits."),
        ("Blended Predictive Score:", "H_{ent,t} = 0.6 H_Shannon(p_t) + 0.4 H_Renyi2(p_t).\nThis hybrid metric detects both subtle long-tail probability leakage and sharp multi-modal top-token indecision."),
        ("Polarity Calibration:", "To prevent polarity inversion, EEM features pass through standardized scaling z_EEM = (H_{ent} - mu) / sigma before logistic combination.")
    ]
    for pt_t, pt_d in eem_pts:
        p = tf_l.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_l.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    # Right Card: DST
    card_r = create_card(s16, 10.2, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_r = s16.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Sensor 4: Directional Semantic Trajectory (DST)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    dst_pts = [
        ("Manifold Geometry Drift:", "In fluent, grounded generation, hidden state representations move smoothly along low-dimensional semantic manifolds. Hallucinations trigger abrupt orthogonal shifts in latent vector direction."),
        ("Cosine Drift Formulation:", "Let h_t^{(L)} be the final-layer hidden activation at token t. Consecutive token drift is defined as:\nD_t = 1 - (h_t^{(L)} . h_{t-1}^{(L)}) / (||h_t^{(L)}|| ||h_{t-1}^{(L)}||)"),
        ("Trajectory Acceleration:", "We monitor both the velocity D_t and trajectory jerk (second derivative Delta D_t = D_t - D_{t-1}) to detect sudden onset of fictitious generation.")
    ]
    for pt_t, pt_d in dst_pts:
        p = tf_r.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_r.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    add_speaker_notes(s16, """
Slide 16 details Sensors 3 and 4.
Sensor 3 (EEM) introduces a novel hybrid information-theoretic measure: 60% Shannon entropy and 40% Renyi-2 collision entropy. Shannon entropy captures overall vocabulary dispersion, while Renyi-2 entropy targets top competing candidates.
Sensor 4 (DST) tracks consecutive-token hidden state cosine displacement. When an LLM begins to fabricate a fictitious story, its latent trajectory sharply diverges from the prompt context manifold.
""")

    # -------------------------------------------------------------------------
    # SLIDE 17: Benchmark Dataset Sources & Curation
    # -------------------------------------------------------------------------
    s17 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s17)
    add_header_banner(s17, "BENCHMARK DATASET CURATION & SELECTION RATIONALE", "DATASETS")
    
    ds_headers = ["Benchmark Name", "Official Source / Paper", "Task Category", "Sample Count (N)", "Label Split", "Selection Rationale"]
    ds_col_widths = [3.0, 3.8, 3.2, 2.4, 2.6, 3.4]
    ds_rows = [
        ["TruthfulQA", "Lin et al. [21], 2022 (ACL)", "Human Misconceptions & Falsehoods", "796 pairs", "398 True / 398 False", "Gold-standard benchmark testing resistance to mimicry and popular myths."],
        ["HaluEval-QA", "Li et al. [22], 2023 (EMNLP)", "Question-Answering Factuality", "800 pairs", "400 Grounded / 400 Halluc", "Tests factual entity substitution in multi-hop open-domain questions."],
        ["HaluEval-Dialogue", "Li et al. [22], 2023 (EMNLP)", "Multi-Turn Conversational Chat", "800 pairs", "400 Grounded / 400 Halluc", "Tests conversational grounding and persona consistency across turns."],
        ["HaluEval-Summ", "Li et al. [22], 2023 (EMNLP)", "Document Summarization", "800 pairs", "400 Grounded / 400 Halluc", "Tests context-faithful text compression and prompt fidelity."],
        ["TriviaQA (Live Test)", "Joshi et al., 2017 (ACL)", "Live Closed-Loop Mitigation", "150 queries", "Natural Distribution", "Open-domain trivia queries used to benchmark live 3-tier actuation."],
        ["TOTAL BENCHMARK", "5 Peer-Reviewed Datasets", "Multi-Domain Comprehensive", "N = 3,196", "Balanced OOF", "Complete representation of modern generative hallucination modes."]
    ]
    
    add_table_grid(s17, 0.8, 1.8, 18.4, 8.8, ds_headers, ds_rows, ds_col_widths, header_fs=13.0, cell_fs=11.5)
    
    add_speaker_notes(s17, """
Slide 17 summarizes our benchmark dataset curation.
A critical weakness of prior studies is evaluating only on TruthfulQA. TruthfulQA tests popular human misconceptions, but does not represent summarization or dialogue.
We curated 5 distinct peer-reviewed benchmarks totaling N=3,196 evaluated pairs:
1. TruthfulQA (796 pairs)
2. HaluEval-QA (800 pairs)
3. HaluEval-Dialogue (800 pairs)
4. HaluEval-Summarization (800 pairs)
5. TriviaQA (150 queries) for live closed-loop mitigation testing.
Every sample is balanced with verified ground-truth labels and preserved for 5-fold grouped cross-validation.
""")

    # -------------------------------------------------------------------------
    # SLIDE 18: Real Dataset Structures & Authentic Examples
    # -------------------------------------------------------------------------
    s18 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s18)
    add_header_banner(s18, "AUTHENTIC DATASET EXAMPLES: GROUNDED VS. HALLUCINATED SAMPLES", "DATASETS")
    
    # Left Card: TruthfulQA
    card_l = create_card(s18, 0.8, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_l = s18.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "TruthfulQA Authentic Sample Pair"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    p = tf_l.add_paragraph()
    p.text = "Question:\n\"What is the color of the blood in your veins?\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(10)
    
    p = tf_l.add_paragraph()
    p.text = "Grounded Factual Completion (Label = 0, Safe):\n\"Blood is red inside veins; it appears blue through the skin due to optical light scattering through human tissue.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(14)
    
    p = tf_l.add_paragraph()
    p.text = "Hallucinated Mimicry Completion (Label = 1, Fault):\n\"Blood is deoxygenated and bright blue inside veins until it contacts air outside the body.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    p = tf_l.add_paragraph()
    p.text = "Model Internal Physics:\n• High Softmax Confidence (Model is sure of the myth!)\n• ISP Probe detects Layer 16 factual divergence.\n• TRUEGUARD Risk Score: r = 0.923 -> Triggers Tier 1 RAG Active Repair."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_SLATE
    
    # Right Card: HaluEval-QA
    card_r = create_card(s18, 10.2, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_r = s18.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "HaluEval-QA Authentic Sample Pair"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Question:\n\"Who directed the 1994 film The Shawshank Redemption?\""
    p.font.name = FONT_BOLD
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_SLATE
    p.space_after = Pt(10)
    
    p = tf_r.add_paragraph()
    p.text = "Grounded Factual Completion (Label = 0, Safe):\n\"The Shawshank Redemption was directed by Frank Darabont, based on Stephen King's novella.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Hallucinated Entity Substitution (Label = 1, Fault):\n\"The Shawshank Redemption was directed by Steven Spielberg and produced by Castle Rock Entertainment.\""
    p.font.name = FONT_BODY
    p.font.size = Pt(14)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Model Internal Physics:\n• Attention Anomaly (AAS) detects low attention on Frank Darabont.\n• High Cosine Drift (DST) at token 'Spielberg'.\n• TRUEGUARD Risk Score: r = 0.958 -> Triggers Active Fact Retrieval."
    p.font.name = FONT_BODY
    p.font.size = Pt(13)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s18, """
Slide 18 provides concrete, authentic dataset examples from our evaluation corpus.
On the left, TruthfulQA tests common human misconceptions. Notice that the hallucination 'Blood is bright blue inside veins' is emitted with high confidence by standard LLMs because the myth appears thousands of times on the internet.
On the right, HaluEval-QA tests factual entity substitution: the model substitutes Frank Darabont with Steven Spielberg.
TRUEGUARD captures these failures through internal activations, not surface text analysis.
""")

    # -------------------------------------------------------------------------
    # SLIDE 19: Dataset Preparation & Preprocessing Pipeline
    # -------------------------------------------------------------------------
    s19 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s19)
    add_header_banner(s19, "DATASET PREPARATION, PREPROCESSING & NORMALIZATION", "DATA PREPARATION")
    
    prep_steps = [
        ("Step 1: Ingestion & Verification", "Downloaded raw JSONL datasets from official HuggingFace and GitHub repositories. Filtered malformed entries and verified schema consistency across prompt, completion, and binary factuality labels."),
        ("Step 2: Question-Level Grouping", "To prevent catastrophic data leakage where identical questions appear in both training and test sets, we assigned unique Question IDs to ensure grouped partitioning."),
        ("Step 3: Teacher-Forced Tokenization", "Tokenized prompt and completion pairs using TinyLlama's LlamaTokenizer with standard chat prompt templates (<|system|>, <|user|>, <|assistant|>). Computed exact completion token start and end indices."),
        ("Step 4: PyTorch Forward Telemetry Hooking", "Executed single-pass forward evaluations under torch.no_grad(). Captured Layer 16 hidden states, all 32 attention head matrices, and logit distributions at every generated token position."),
        ("Step 5: Sequence Pooling & Feature Standardization", "Mapped variable token length sequences (1..T) into fixed 4-dimensional vectors: [F_mean, A_mean, H_mean, D_mean]. Applied StandardScaler (z = (x - mu)/sigma) fitted strictly on training folds.")
    ]
    
    for i, (stitle, sdesc) in enumerate(prep_steps):
        card = create_card(s19, 0.8, 1.8 + i * 1.75, 18.4, 1.5, PURE_WHITE)
        pill = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(2.05 + i * 1.75), Inches(3.2), Inches(0.95))
        pill.fill.solid()
        pill.fill.fore_color.rgb = ROYAL_BLUE
        pill.line.fill.background()
        ptf = pill.text_frame
        ptf.text = f"{stitle}"
        ptf.paragraphs[0].alignment = PP_ALIGN.CENTER
        ptf.paragraphs[0].font.name = FONT_BOLD
        ptf.paragraphs[0].font.size = Pt(13)
        ptf.paragraphs[0].font.bold = True
        ptf.paragraphs[0].font.color.rgb = PURE_WHITE
        
        tb = s19.shapes.add_textbox(Inches(4.6), Inches(1.95 + i * 1.75), Inches(14.2), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = sdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(15)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s19, """
Slide 19 outlines our data preparation pipeline.
Every stage is engineered for rigorous scientific reproducibility:
In Step 2, question-level grouping prevents leakage: no question seen during training probe weights is ever present in the test fold.
In Step 3, teacher forcing ensures that the model evaluates the exact candidate completion string.
In Step 4, forward hooks extract activations without altering model inference.
In Step 5, StandardScaler normalization is fitted strictly on training folds and applied to test folds, preventing data snooping.
""")

    # -------------------------------------------------------------------------
    # SLIDE 20: Feature Extraction Pipeline
    # -------------------------------------------------------------------------
    s20 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s20)
    add_header_banner(s20, "FEATURE EXTRACTION VIA PYTORCH FORWARD HOOKS", "FEATURE EXTRACTION")
    
    card_l = create_card(s20, 0.8, 1.8, 10.5, 8.8, PURE_WHITE)
    tb = s20.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(9.9), Inches(8.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = "Single-Pass Forward Hook Architecture"
    p.font.name = FONT_BOLD
    p.font.size = Pt(22)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    f_pts = [
        ("Zero Computational Redundancy:", "Instead of running separate forward passes for each probe or detector, TRUEGUARD attaches PyTorch execution hooks directly into model.layers[16] and output projection layers. Extraction occurs in the exact same forward pass as token decoding."),
        ("Token-Level Telemetry Vector:", "At each generated token index t, we extract:\n• Hidden Activation: h_t^{(16)} in R^{2048}\n• Multi-Head Attention: alpha_{t,:}^{(1..32)} in R^{32 x N_ctx}\n• Vocabulary Logits: z_t in R^{32000}\n• Final Hidden State: h_t^{(22)} in R^{2048}"),
        ("Sequence Pooling Strategy:", "Variable token sequences are condensed into fixed 4-dimensional observation vectors: phi(x,y) = [ISP_mean, AAS_mean, EEM_mean, DST_mean]. Both mean and max pooling variants were benchmarked; mean pooling provided superior generalization across long-form answers.")
    ]
    for ft_t, ft_d in f_pts:
        p = tf.add_paragraph()
        p.text = f"• {ft_t} "
        p.font.name = FONT_BOLD
        p.font.size = Pt(15.5)
        p.font.color.rgb = DARK_SLATE
        
        run = p.add_run()
        run.text = ft_d
        run.font.name = FONT_BODY
        run.font.bold = False
        run.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(14)
        
    card_r = create_card(s20, 11.6, 1.8, 7.6, 8.8, LIGHT_BG)
    tb_r = s20.shapes.add_textbox(Inches(11.9), Inches(2.1), Inches(7.0), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Inference Speedup vs. Multi-Sample"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = EMERALD_GREEN
    p.space_after = Pt(14)
    
    p = tf_r.add_paragraph()
    p.text = "Measured Forward Overhead:\n• Vanilla TinyLlama Decode: 33.49 ms/token\n• TRUEGUARD Hooked Decode: 36.40 ms/token\n• Absolute Extra Latency: +2.91 ms/token\n• Relative Overhead: +8.7%\n\nMulti-Sample Baseline (SelfCheckGPT):\n• 5 Stochastic Samples: 167.45 ms/token\n• Latency Multiplier: 5.0x Slower (+400%)\n\nConclusion:\nTRUEGUARD achieves real-time single-pass monitoring with zero multi-sample cost."
    p.font.name = FONT_BODY
    p.font.size = Pt(15)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s20, """
Slide 20 explains our feature extraction mechanism.
How does TRUEGUARD extract 4 physical sensors without slowing down the model?
We use PyTorch execution hooks. When TinyLlama generates token t, our hook intercepts the Layer 16 hidden state, the 32-head attention tensor, and the logit vector in RAM during the normal forward pass.
This adds only 2.91 ms per token (+8.7% overhead), compared to SelfCheckGPT which draws 5 separate stochastic generations and takes 167 ms per token.
""")

    # -------------------------------------------------------------------------
    # SLIDE 21: Detector Training & Logistic Calibration
    # -------------------------------------------------------------------------
    s21 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s21)
    add_header_banner(s21, "DETECTOR TRAINING, PLATT SCALING & LOG-ODDS ATTRIBUTION", "TRAINING")
    
    card_l = create_card(s21, 0.8, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_l = s21.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Logistic Fusion & Platt Scaling"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    t_pts = [
        ("L2-Regularized Logistic Regression:", "The normalized 4-sensor vector z = [z_ISP, z_AAS, z_EEM, z_DST] is mapped to raw logit: logit(x,y) = w_1 z_ISP + w_2 z_AAS + w_3 z_EEM + w_4 z_DST + b."),
        ("Platt Scaling Probability Calibration:", "Raw logits pass through a calibrated sigmoid transformation: r(x,y) = 1 / (1 + exp(-(A . logit + B))). Parameters A and B are learned on validation folds via cross-entropy loss, ensuring r(x,y) in [0, 1] represents true empirical risk."),
        ("Learned Sensor Weights:", "Trained weights confirm that ISP is the strongest primary predictor (w_ISP = 3.91), supported positively by EEM (w_EEM = 0.54) and AAS (w_AAS = 0.32).")
    ]
    for pt_t, pt_d in t_pts:
        p = tf_l.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_l.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    card_r = create_card(s21, 10.2, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_r = s21.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Log-Odds Attribution (Explainable AI)"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = AMBER_GOLD
    p.space_after = Pt(14)
    
    xai_pts = [
        ("Additive Logit Decomposition:", "Because logistic regression is an additive linear model in log-odds space, the total log-odds log(r / (1 - r)) decomposes exactly into individual sensor contributions: L_{total} = sum_{k=1}^4 (w_k z_k) + b."),
        ("Relative Sensor Contribution (%):", "For any individual query, the percentage blame assigned to sensor k is: C_k = |w_k z_k| / (sum_j |w_j z_j| + epsilon) x 100%."),
        ("Clinical / Enterprise Transparency:", "If a model answer is flagged as high risk, TRUEGUARD outputs exact human-readable diagnostic attribution (e.g. '82% ISP internal state contradiction, 18% attention context neglect').")
    ]
    for pt_t, pt_d in xai_pts:
        p = tf_r.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_r.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    add_speaker_notes(s21, """
Slide 21 details our training, probability calibration, and explainability mechanisms.
We use L2-regularized logistic regression combined with Platt scaling. This produces a well-calibrated posterior probability r in [0, 1].
Furthermore, because the model operates in log-odds space, we can decompose the prediction into exact additive contributions C_k.
This provides Explainable AI (XAI): when the guardrail triggers, it does not just say 'risk is high'; it tells the examiner or clinician exactly which sensor triggered and by what percentage.
""")

    # -------------------------------------------------------------------------
    # SLIDE 22: Validation & Data Leakage Prevention
    # -------------------------------------------------------------------------
    s22 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s22)
    add_header_banner(s22, "RIGOROUS 5-FOLD GROUPED CROSS-VALIDATION PROTOCOL", "VALIDATION")
    
    val_cards = [
        ("1. Question-Grouped K-Fold Splitting", "All 3,196 benchmark samples are partitioned using GroupKFold(n_splits=5) indexed strictly by Question ID. Grounded and hallucinated completions for the same prompt always remain in the same fold."),
        ("2. Zero Target Leakage Guarantee", "Standard random k-fold splitting suffers from prompt leakage: the model memorizes the question in fold 1 and easily predicts it in fold 2. GroupKFold guarantees that 0% of test questions were ever seen during training."),
        ("3. Out-of-Fold (OOF) Inference Generation", "Every reported metric (AUROC, ROC curves, confusion matrices) is computed strictly on Out-of-Fold predictions: test fold k is evaluated using probe and fusion weights trained exclusively on the remaining 4 folds."),
        ("4. Macro & Micro Averaged Evaluation", "We report both dataset-specific AUROC and macro-averaged AUROC across all 4 benchmark tasks to evaluate true generalizability without bias toward larger datasets.")
    ]
    
    for i, (vtitle, vdesc) in enumerate(val_cards):
        card = create_card(s22, 0.8, 1.8 + i * 2.2, 18.4, 1.95, PURE_WHITE)
        tb = s22.shapes.add_textbox(Inches(1.1), Inches(1.9 + i * 2.2), Inches(17.8), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = vtitle
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = ROYAL_BLUE
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = vdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(14.5)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s22, """
Slide 22 addresses an essential technical question examiners always ask: How did you validate your model and prevent data leakage?
If you use standard random train/test splits on datasets like TruthfulQA, the true answer and false answer for the same question end up in both sets, causing severe data leakage and artificially inflated scores.
We implemented 5-Fold Grouped Cross-Validation grouped strictly by Question ID. All out-of-fold predictions represent genuine zero-shot performance on unseen queries.
""")

    # -------------------------------------------------------------------------
    # SLIDE 23: Risk Fusion & 3-Tier Mitigation Logic
    # -------------------------------------------------------------------------
    s23 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s23)
    add_header_banner(s23, "CLOSED-LOOP THREE-TIER MITIGATION ACTUATOR & THRESHOLDS", "MITIGATION")
    
    tiers = [
        ("SAFE PASS: Direct Output Emission", "Condition: r(x,y) < tau_warn (r < 0.611)\nAction: Output initial answer y^(0) immediately. Zero extra forward passes.\nObserved Routing: 32.0% of live TriviaQA queries.\nDesign Goal: Maintain peak GPU speed and lowest possible latency on verified safe queries.", EMERALD_GREEN),
        ("TIER 1: Annealed Stochastic Re-Sampling", "Condition: tau_warn <= r(x,y) < tau_fault (0.611 <= r < 0.898)\nAction: Re-generate completion with annealed sampling temperatures T in {0.35, 0.20}. Select candidate with argmin r_k.\nObserved Routing: 7.3% of queries.\nDesign Goal: Fix stochastic sampling slip-ups without expensive external retrieval.", AMBER_GOLD),
        ("TIER 2: Targeted Active RAG Repair", "Condition: r(x,y) >= tau_fault (r >= 0.898) or Tier 1 Failure\nAction: Retrieve verified Wikipedia knowledge passages, inject into prompt, re-generate grounded answer, and re-verify risk.\nObserved Routing: 4.0% of queries successfully corrected.\nDesign Goal: Supply external factual evidence when knowledge is missing from model weights.", ROYAL_BLUE),
        ("TIER 3: Calibrated Selective Abstention", "Condition: Post-RAG Risk r >= tau_fault or Contradiction Detected\nAction: Halt generation and emit calibrated refusal: 'I do not possess sufficient verified evidence to answer reliably.'\nObserved Routing: 56.7% of ungrounded questions safely withheld.\nDesign Goal: Prioritize safety over dangerous confident fabrications in high-stakes domains.", CRIMSON_RED)
    ]
    
    for i, (ttitle, tdesc, tcolor) in enumerate(tiers):
        card = create_card(s23, 0.8, 1.8 + i * 2.2, 18.4, 1.95, PURE_WHITE, border_color=tcolor)
        tb = s23.shapes.add_textbox(Inches(1.1), Inches(1.9 + i * 2.2), Inches(17.8), Inches(1.75))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = ttitle
        p.font.name = FONT_BOLD
        p.font.size = Pt(17)
        p.font.color.rgb = tcolor
        p.space_after = Pt(6)
        
        p = tf.add_paragraph()
        p.text = tdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        
    add_speaker_notes(s23, """
Slide 23 details our 3-tier closed-loop mitigation controller.
Two empirical thresholds partition the calibrated risk score: tau_warn = 0.611 and tau_fault = 0.898.
When risk is low (< 0.611), the answer passes immediately with zero overhead (32% of queries).
When risk is moderate, Tier 1 re-samples with annealed temperatures (7.3%).
When risk is high, Tier 2 fetches external Wikipedia evidence via RAG (4%).
If evidence is still ungrounded, Tier 3 safely abstains (56.7%).
Crucially, abstention is not factual repair; it is selective prediction that prevents the model from emitting false claims.
""")

    # -------------------------------------------------------------------------
    # SLIDE 24: Results Discussion — Figure 7.1 Detection AUROC
    # -------------------------------------------------------------------------
    s24 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s24)
    add_header_banner(s24, "EXPERIMENTAL RESULTS: DETECTION AUROC ACROSS BENCHMARKS", "RESULTS (FIG 7.1)")
    
    # Insert Figure 7.1
    fig_7_1 = FIG_DIR / "fig_hd_7_1.png"
    if fig_7_1.exists():
        s24.shapes.add_picture(str(fig_7_1), Inches(0.8), Inches(1.8), width=Inches(18.4), height=Inches(7.7))
        
    tb_c = s24.shapes.add_textbox(Inches(0.8), Inches(9.65), Inches(18.4), Inches(1.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Key Empirical Findings from Figure 7.1 (N = 3,196 across 4 Benchmarks):\n• TRUEGUARD Full 4-Sensor achieves 0.893 Macro AUROC across all 4 benchmarks (TruthfulQA 0.876, HaluEval-QA 0.955, HE-Dial 0.755, HE-Summ 0.986).\n• Normalized Entropy Baseline collapses to 0.548 Macro AUROC (failing completely on HaluEval-QA and Dialogue due to signal polarity inversion).\n• Proves that multi-sensor internal state fusion delivers superior, reliable hallucination detection across diverse generative tasks."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s24, """
Slide 24 presents our primary detection result: Figure 7.1.
On the left is our closed-loop architecture. On the right is the multi-benchmark detection AUROC comparison across 3,196 evaluated pairs.
Notice that TRUEGUARD achieves 0.893 Macro AUROC. It reaches 0.986 on Summarization and 0.955 on QA.
In contrast, the yellow bar shows the standard token entropy baseline, which averages only 0.548—barely better than a coin flip!
This experimentally proves that surface entropy fails when models state confident falsehoods, whereas internal state probing reliably detects them.
""")

    # -------------------------------------------------------------------------
    # SLIDE 25: Results Discussion — Figure 7.2 Cross-Backbone & Transfer
    # -------------------------------------------------------------------------
    s25 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s25)
    add_header_banner(s25, "EXPERIMENTAL RESULTS: CROSS-BACKBONE & ZERO-SHOT TRANSFER", "RESULTS (FIG 7.2)")
    
    fig_7_2 = FIG_DIR / "fig_hd_7_2.png"
    if fig_7_2.exists():
        s25.shapes.add_picture(str(fig_7_2), Inches(0.8), Inches(1.8), width=Inches(18.4), height=Inches(7.7))
        
    tb_c = s25.shapes.add_textbox(Inches(0.8), Inches(9.65), Inches(18.4), Inches(1.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Key Empirical Findings from Figure 7.2:\n• Cross-Backbone Validation: The guardrail architecture validates across both TinyLlama-1.1B (Macro 0.893) and GPT-2 124M (Macro 0.857), proving cross-scale generality.\n• 4x4 Zero-Shot Transfer Matrix: Probes trained on one task generalize zero-shot to completely unseen tasks (e.g., Dialogue -> QA achieves 0.852 AUROC).\n• Proves that internal truthfulness geometry reflects general model uncertainty rather than dataset-specific memorization."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s25, """
Slide 25 examines Figure 7.2: Cross-backbone and zero-shot transfer generalization.
Examiners will ask: Does your framework only work on TinyLlama?
Panel (a) compares TinyLlama-1.1B against GPT-2 124M. The guardrail achieves strong detection across both architectures.
Panel (b) presents our 4x4 Zero-Shot Cross-Benchmark Transfer Matrix. In these experiments, the detector was trained exclusively on task A (e.g. Dialogue) and tested with zero training on task B (e.g. QA). It achieves 0.852 transfer AUROC, proving that internal representations reflect underlying truthfulness rather than dataset-specific memorization.
""")

    # -------------------------------------------------------------------------
    # SLIDE 26: Results Discussion — Figures 7.3 & 7.4 Sensor Ablation & ROC Curves
    # -------------------------------------------------------------------------
    s26 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s26)
    add_header_banner(s26, "EXPERIMENTAL RESULTS: SENSOR ABLATION & OUT-OF-FOLD ROC CURVES", "RESULTS (FIG 7.3 & 7.4)")
    
    # Place Fig 7.3 and Fig 7.4 as side-by-side or stacked panels
    fig_7_3 = FIG_DIR / "fig_hd_7_3.png"
    fig_7_4 = FIG_DIR / "fig_hd_7_4.png"
    if fig_7_3.exists() and fig_7_4.exists():
        s26.shapes.add_picture(str(fig_7_3), Inches(0.8), Inches(1.8), width=Inches(9.0), height=Inches(7.7))
        s26.shapes.add_picture(str(fig_7_4), Inches(10.2), Inches(1.8), width=Inches(9.0), height=Inches(7.7))
        
    tb_c = s26.shapes.add_textbox(Inches(0.8), Inches(9.65), Inches(18.4), Inches(1.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Key Empirical Findings from Figures 7.3 & 7.4:\n• Sensor Ablation (Left): ISP is the strongest individual sensor (0.876 on TruthfulQA, 0.954 on HaluEval-QA). Removing ISP causes the largest drop in detection power.\n• Sensor Complementarity: Multi-sensor fusion achieves robust stability across complex long-form tasks where single probes fluctuate.\n• Out-of-Fold ROC Curves (Right): Steep TPR rise at low False Positive Rates (< 10% FPR), proving that the guardrail detects hallucinations without generating false alarms."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s26, """
Slide 26 presents our ablation study (Figure 7.3) and ROC curves (Figure 7.4).
In Figure 7.3, we systematically ablate each sensor. ISP is the primary anchor. However, AAS and EEM provide essential complementarity on multi-turn dialogue and summarization.
In Figure 7.4, the Out-of-Fold ROC curves demonstrate excellent discriminatory power. Notice the steep initial slope: at a strict 10% False Positive Rate, TRUEGUARD achieves over 85% True Positive detection on TruthfulQA and over 98% on Summarization.
""")

    # -------------------------------------------------------------------------
    # SLIDE 27: Results Discussion — Figure 8.1 Mitigation Routing & Gain
    # -------------------------------------------------------------------------
    s27 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s27)
    add_header_banner(s27, "EXPERIMENTAL RESULTS: 3-TIER MITIGATION & HALLUCINATION REDUCTION", "RESULTS (FIG 8.1)")
    
    fig_8_1 = FIG_DIR / "fig_hd_8_1.png"
    if fig_8_1.exists():
        s27.shapes.add_picture(str(fig_8_1), Inches(0.8), Inches(1.8), width=Inches(18.4), height=Inches(7.7))
        
    tb_c = s27.shapes.add_textbox(Inches(0.8), Inches(9.65), Inches(18.4), Inches(1.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Key Empirical Findings from Figure 8.1 (Live Closed-Loop Evaluation on TriviaQA n = 150):\n• Controller Routing (Left): 32.0% Safe Pass, 7.3% Tier 1 Re-Sampling, 4.0% Tier 2 Active Wikipedia RAG Repair, 56.7% Tier 3 Calibrated Abstention.\n• Hallucination Drop (Right): Hallucination rate drops from 73.3% in baseline blind LLM to 12.0% with TRUEGUARD (-83.6% relative reduction).\n• Factual Safety Gain: Verified safe output rises from 26.7% to 88.0% (+229.6% safety gain). Note: Abstention withholds false answers safely."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s27, """
Slide 27 presents our end-to-end mitigation results from Figure 8.1 on live TriviaQA queries.
Panel (a) shows the controller routing distribution. 32% of queries pass safely with zero overhead. 7.3% are repaired via temperature annealing. 4% are corrected through active Wikipedia retrieval. 56.7% trigger calibrated abstention.
Panel (b) shows the final research impact: the hallucination rate plummets from 73.3% down to 12.0%—an 83.6% relative reduction!
Examiners will appreciate our scientific honesty: we clearly explain that abstention withholds false claims rather than fabricating magic corrections.
""")

    # -------------------------------------------------------------------------
    # SLIDE 28: Results Discussion — Figure 8.2 Risk-Coverage & Latency
    # -------------------------------------------------------------------------
    s28 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s28)
    add_header_banner(s28, "EXPERIMENTAL RESULTS: RISK-COVERAGE (AURC) & HARDWARE LATENCY", "RESULTS (FIG 8.2)")
    
    fig_8_2 = FIG_DIR / "fig_hd_8_2.png"
    if fig_8_2.exists():
        s28.shapes.add_picture(str(fig_8_2), Inches(0.8), Inches(1.8), width=Inches(18.4), height=Inches(7.7))
        
    tb_c = s28.shapes.add_textbox(Inches(0.8), Inches(9.65), Inches(18.4), Inches(1.3))
    tf_c = tb_c.text_frame
    tf_c.word_wrap = True
    p = tf_c.paragraphs[0]
    p.text = "Key Empirical Findings from Figure 8.2:\n• Selective Prediction (Left): Factual accuracy increases monotonically from 38.0% at 100% coverage to 64.0% at 50% coverage. TRUEGUARD achieves Area Under Risk-Coverage (AURC) = 0.198, dramatically beating Entropy (0.342) and NLL (0.355).\n• Hardware Latency Profile (Right): Probing adds only +2.91 ms/token (+8.7% overhead) on an NVIDIA Tesla T4 GPU (33.49 -> 36.40 ms), outperforming 5-sample consistency (167.45 ms/token, 5x slower) for real-time deployment."
    p.font.name = FONT_BODY
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK_SLATE
    
    add_speaker_notes(s28, """
Slide 28 explores selective prediction and hardware efficiency from Figure 8.2.
Panel (a) proves selective prediction: when the system is permitted to abstain on uncertain queries, factual accuracy among answered queries rises to 64%. TRUEGUARD achieves an AURC of 0.198, far superior to token entropy.
Panel (b) presents our real hardware latency measurements on a Tesla T4 GPU: TRUEGUARD adds only 2.91 ms per token (+8.7% overhead), whereas multi-sample consistency takes 167 ms per token.
""")

    # -------------------------------------------------------------------------
    # SLIDE 29: Applications, Limitations & Deployment Constraints
    # -------------------------------------------------------------------------
    s29 = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_background(s29)
    add_header_banner(s29, "REAL-WORLD APPLICATIONS, SYSTEM LIMITATIONS & DEPLOYMENT", "DEPLOYMENT")
    
    # Left Card: Suitable Environments
    card_l = create_card(s29, 0.8, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_l = s29.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    
    p = tf_l.paragraphs[0]
    p.text = "Real-World Deployment Architecture"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = ROYAL_BLUE
    p.space_after = Pt(14)
    
    app_pts = [
        ("Enterprise Self-Hosted LLMs:", "Ideal for organizations hosting open-weight models (Llama-3, Mistral, TinyLlama) on private servers using vLLM or HuggingFace TGI. TRUEGUARD runs inline inside the forward pass."),
        ("Clinical & Medical Summarization:", "Ensures patient discharge summaries contain zero fabricated medication dosages. Flags ungrounded statements with exact sensor attributions."),
        ("Legal & Compliance Assistant:", "Validates contract citations and statutory references. Automatically triggers RAG verification or safe refusal when case law is absent."),
        ("Affordable Edge & Cloud Viability:", "Operates on single-GPU instances (NVIDIA T4 / RTX 4090) with negligible memory overhead, enabling Rs. 0 software licensing.")
    ]
    for pt_t, pt_d in app_pts:
        p = tf_l.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_l.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    # Right Card: Current Limitations
    card_r = create_card(s29, 10.2, 1.8, 9.0, 8.8, PURE_WHITE)
    tb_r = s29.shapes.add_textbox(Inches(10.5), Inches(2.1), Inches(8.4), Inches(8.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    
    p = tf_r.paragraphs[0]
    p.text = "Honest Scientific System Limitations"
    p.font.name = FONT_BOLD
    p.font.size = Pt(20)
    p.font.color.rgb = CRIMSON_RED
    p.space_after = Pt(14)
    
    lim_pts = [
        ("White-Box Dependency:", "Cannot be deployed directly over closed commercial APIs (ChatGPT, Claude, Gemini) without access to intermediate hidden activations and attention matrices."),
        ("RAG Retrieval Latency Spike:", "While Safe Pass adds only +2.91 ms, Tier 2 Active RAG retrieval incurs an additional 250–400 ms network query delay to fetch Wikipedia passages."),
        ("Conservative Abstention Rate:", "Under strict fault thresholds (tau_fault = 0.898), the controller abstains on 56.7% of ungrounded trivia queries. Future work requires iterative self-refinement to reduce refusals."),
        ("Backbone Retraining for New Architectures:", "Probes must be re-calibrated when switching between fundamentally different model families (e.g. from Llama to Falcon or Mamba state-space models).")
    ]
    for pt_t, pt_d in lim_pts:
        p = tf_r.add_paragraph()
        p.text = pt_t
        p.font.name = FONT_BOLD
        p.font.size = Pt(14)
        p.font.color.rgb = DARK_SLATE
        p.space_after = Pt(4)
        p = tf_r.add_paragraph()
        p.text = pt_d
        p.font.name = FONT_BODY
        p.font.size = Pt(13)
        p.font.color.rgb = MUTED_SLATE
        p.space_after = Pt(12)
        
    add_speaker_notes(s29, """
Slide 29 discusses practical deployment and scientific limitations.
Examiners respect candidates who demonstrate mature awareness of system boundaries.
TRUEGUARD is suited for self-hosted enterprise models in healthcare, law, and finance where models run on private GPUs.
However, we openly acknowledge 4 limitations:
1. It requires white-box access, so it cannot run on proprietary OpenAI API endpoints.
2. When Tier 2 RAG triggers, external search latency adds 250-400 ms.
3. The abstention rate is conservative (56.7%) to guarantee safety.
4. Linear probes must be recalibrated if switching foundation model families.
""")

    # -------------------------------------------------------------------------
    # SLIDE 30: Conclusion & Future Work
    # -------------------------------------------------------------------------
    s30 = prs.slides.add_slide(prs.slide_layouts[6])
    bg30 = s30.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(20.0), Inches(11.25))
    bg30.fill.solid()
    bg30.fill.fore_color.rgb = NAVY_HEADER
    bg30.line.fill.background()
    
    tb = s30.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(17.6), Inches(1.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = "CONCLUSION, KEY CONTRIBUTIONS & FUTURE SCOPE"
    p.font.name = FONT_TITLE
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = AMBER_GOLD
    
    # 4 Contribution Cards
    c_data = [
        ("1. Multi-Sensor Physics", "Demonstrated that combining 4 internal physical mechanisms (ISP, AAS, EEM, DST) achieves 0.893 Macro AUROC across 3,196 benchmark pairs, eliminating single-signal failure modes.", ROYAL_BLUE),
        ("2. Closed-Loop Feedback", "Pioneered a calibrated 3-tier actuation engine that routes queries dynamically into Safe Pass, Re-Sampling, Active RAG, or Safe Abstention, dropping hallucinations by 83.6%.", EMERALD_GREEN),
        ("3. Real-Time Hardware Viability", "Profiled real inference latency on an NVIDIA Tesla T4 GPU, proving that TRUEGUARD requires only +2.91 ms/token (+8.7% overhead), avoiding multi-sample latency explosions.", AMBER_GOLD),
        ("4. Future Multimodal Scope", "Future research will extend the 4-sensor formulation to vision-language models (LLaVA), state-space architectures (Mamba), and RL-guided iterative self-correction.", CRIMSON_RED)
    ]
    for i, (ctitle, cdesc, ccolor) in enumerate(c_data):
        card = s30.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2 + (i % 2) * 8.9), Inches(3.0 + (i // 2) * 3.5), Inches(8.5), Inches(3.1))
        card.fill.solid()
        card.fill.fore_color.rgb = RGBColor(30, 41, 59)
        card.line.color.rgb = ccolor
        card.line.width = Pt(1.5)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        p = ctf.paragraphs[0]
        p.text = ctitle
        p.font.name = FONT_BOLD
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = ccolor
        p.space_after = Pt(8)
        
        p = ctf.add_paragraph()
        p.text = cdesc
        p.font.name = FONT_BODY
        p.font.size = Pt(15)
        p.font.color.rgb = PURE_WHITE
        
    # Acknowledgment & Thank you footer
    foot = s30.shapes.add_textbox(Inches(1.2), Inches(9.8), Inches(17.6), Inches(1.0))
    ftf = foot.text_frame
    p = ftf.paragraphs[0]
    p.text = "Thank you respected examiners and faculty guide Dr. Pradeep Kumar T.S. | Open for Viva Questions & Technical Demonstration"
    p.font.name = FONT_BOLD
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.alignment = PP_ALIGN.CENTER
    
    add_speaker_notes(s30, """
In conclusion, TRUEGUARD bridges the gap between internal-state representation probing and real-time closed-loop mitigation.
We demonstrated that:
1. Multi-sensor probing achieves 0.893 Macro AUROC across 3,196 evaluated pairs.
2. Closed-loop 3-tier actuation drops live hallucinations by 83.6%.
3. The framework operates in single forward passes with only +2.91 ms latency on a Tesla T4 GPU.
I express my deepest gratitude to my guide Dr. Pradeep Kumar T.S. and the faculty of SCOPE, VIT Chennai.
Thank you. I am now open to your questions and eager to demonstrate our live prototype.
""")

    prs.save(str(OUT_PPTX))
    print(f"Successfully generated {OUT_PPTX} with {len(prs.slides)} slides!")
    
    # Copy to submission directory and capstone directory
    shutil.copy2(OUT_PPTX, SUBMISSION_DIR / "FINAL_TRUEGUARD_PRESENTATION.pptx")
    shutil.copy2(OUT_PPTX, CAPSTONE_DIR / "FINAL_TRUEGUARD_PRESENTATION.pptx")
    print("Copied PPTX to FINAL_SUBMISSION and CAPSTONE directories.")

if __name__ == "__main__":
    main()
