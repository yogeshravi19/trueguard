"""
Master Builder for FINAL_REPORT.docx and FINAL_REPORT.pdf (60 to 70 pages).
Strictly follows MIA-Project Template.docx formatting, section sequence, margins,
typography, bottom-center page numbering, and two-pass exact PDF page-number sync.
"""
from __future__ import annotations

import os
import re
import shutil
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import docx
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Cm, Pt, RGBColor
import fitz

ROOT = Path(r"E:\trueguard")
CAPSTONE = ROOT / "CAPSTONE"
FINAL_DIR = CAPSTONE / "FInal"
sys.path.insert(0, str(FINAL_DIR / "tools"))

from build_40paper_literature_review import PILLARS
from build_final_report_ch5_ch6 import build_chapter_5, build_chapter_6
from build_final_report_ch7_to_app import (
    build_appendices,
    build_chapter_7,
    build_chapter_8,
    build_chapter_9,
)
from build_final_report_helpers import (
    CANDIDATE_NAME,
    CANDIDATE_REG,
    FIG_DIR,
    GUIDE_NAME,
    LOGO_PATH,
    PROGRAMME_NAME,
    REPORT_TITLE,
    REPORT_TITLE_MIXED,
    SCHOOL_NAME,
    SUBMISSION_MONTH_YEAR,
    add_chapter_heading,
    add_equation_block,
    add_figure_with_caption,
    add_p,
    add_section_heading,
    add_styled_table,
    add_subsection_heading,
    configure_a4_margins,
    set_section_page_numbering,
)
from report_ch1_ch2_data import CH1_SECTIONS, CH2_SECTIONS
from report_ch3_ch4_data import (
    CROSS_PILLAR_SYNTHESIS_ROWS,
    PILLAR_NARRATIVES,
    PILLAR_SECTION_TITLES,
    PILLAR_TABLE_CAPTIONS,
)
from report_ch4_to_ch9_data import (
    CH4_SECTIONS,
    FUNCTIONAL_REQUIREMENTS_TABLE,
    NON_FUNCTIONAL_REQUIREMENTS_TABLE,
    TECH_STACK_TABLE,
)
from report_references_data import ACRONYMS_AND_SYMBOLS, APA_REFERENCES


def add_vit_logo(doc, width_cm: float = 13.8) -> None:
    if LOGO_PATH.exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(14)
        p.add_run().add_picture(str(LOGO_PATH), width=Cm(width_cm))


def add_dotted_leader_entry(doc, left_text: str, right_page: str, bold: bool = False, indent_cm: float = 0.0, space_before: float = 2.0, space_after: float = 2.0) -> None:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p.paragraph_format
    pf.left_indent = Cm(indent_cm)
    pf.line_spacing = 1.18
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.tab_stops.add_tab_stop(Cm(14.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

    r1 = p.add_run(left_text)
    r1.font.name = "Times New Roman"
    r1.font.size = Pt(11.0 if not bold else 11.5)
    r1.bold = bold

    r2 = p.add_run(f"\t{right_page}")
    r2.font.name = "Times New Roman"
    r2.font.size = Pt(11.0 if not bold else 11.5)
    r2.bold = bold


def build_front_matter(doc, page_map: Dict[str, str]) -> None:
    # Section 0: Unnumbered Front Pages (1. Cover Page, 2. Title Page, 3. Declaration, 4. Certificate)
    sec0 = doc.sections[0]
    configure_a4_margins(sec0)
    set_section_page_numbering(sec0, fmt=None)

    # 1. COVER PAGE (Matches MIA-Project Template.docx page 3 and friend report.pdf)
    add_p(doc, "A project report on", size=12, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=14, space_after=14)
    add_p(doc, REPORT_TITLE, size=19.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.25, space_before=8, space_after=22)
    add_p(doc, "Submitted in partial fulfillment for the award of the degree of", size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=10, space_after=14)
    add_p(doc, "M.Tech. (Integrated) Computer Science and\nEngineering with Specialization in Business Analytics", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.25, space_before=8, space_after=22)
    add_p(doc, "by", size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=10, space_after=14)
    add_p(doc, f"{CANDIDATE_NAME} ({CANDIDATE_REG})", size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=6, space_after=22)
    add_vit_logo(doc, width_cm=13.8)
    add_p(doc, SCHOOL_NAME, size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=18, space_after=12)
    add_p(doc, SUBMISSION_MONTH_YEAR, size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=6, space_after=0)

    # 2. TITLE PAGE (Matches MIA-Project Template.docx page 4 and friend report.pdf)
    doc.add_page_break()
    add_p(doc, REPORT_TITLE, size=19.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.25, space_before=24, space_after=22)
    add_p(doc, "Submitted in partial fulfillment for the award of the degree of", size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=10, space_after=14)
    add_p(doc, "M.Tech. (Integrated) Computer Science and\nEngineering with Specialization in Business Analytics", size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.25, space_before=8, space_after=22)
    add_p(doc, "by", size=14, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=10, space_after=14)
    add_p(doc, f"{CANDIDATE_NAME} ({CANDIDATE_REG})", size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=6, space_after=22)
    add_vit_logo(doc, width_cm=13.8)
    add_p(doc, SCHOOL_NAME, size=17, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=18, space_after=12)
    add_p(doc, SUBMISSION_MONTH_YEAR, size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=6, space_after=0)

    # 3. DECLARATION BY THE CANDIDATE (Matches MIA-Project Template.docx page 5)
    doc.add_page_break()
    add_vit_logo(doc, width_cm=13.0)
    add_p(doc, "DECLARATION", size=14, bold=True, underline=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=28, space_after=26)
    add_p(
        doc,
        f'I hereby declare that the thesis entitled "{REPORT_TITLE_MIXED}" submitted by me, for the award of the degree of '
        f"{PROGRAMME_NAME}, Vellore Institute of Technology, Chennai, is a record of bonafide work carried out by me under the supervision of {GUIDE_NAME.rstrip('.')}.",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        line_spacing=1.5,
        space_before=12,
        space_after=20,
    )
    add_p(
        doc,
        "I further declare that the work reported in this thesis has not been submitted and will not be submitted, either in part or in full, "
        "for the award of any other degree or diploma in this institute or any other institute or university.",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        line_spacing=1.5,
        space_before=12,
        space_after=90,
    )
    add_p(doc, "Place: Chennai", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3, space_before=60, space_after=16)
    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.tab_stops.add_tab_stop(Cm(14.5), WD_TAB_ALIGNMENT.RIGHT)
    p_sig.paragraph_format.space_before = Pt(24)
    r_d = p_sig.add_run("Date: [Date of Submission]\tSignature of the Candidate")
    r_d.font.name = "Times New Roman"
    r_d.font.size = Pt(12)
    r_d.bold = True

    # 4. CERTIFICATE (Matches MIA-Project Template.docx page 6)
    doc.add_page_break()
    add_vit_logo(doc, width_cm=13.0)
    add_p(doc, "School of Computer Science and Engineering", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=8, space_after=8)
    add_p(doc, "CERTIFICATE", size=14, bold=True, underline=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=6, space_after=18)
    add_p(
        doc,
        f'This is to certify that the report entitled "{REPORT_TITLE_MIXED}" is prepared and submitted by '
        f"{CANDIDATE_NAME} ({CANDIDATE_REG}) to Vellore Institute of Technology, Chennai, in partial fulfillment of the requirement for the award of the degree of "
        f"{PROGRAMME_NAME} programme is a bonafide record carried out under my guidance. The project fulfills the requirements as per the regulations of this University "
        "and in my opinion meets the necessary standards for submission. The contents of this report have not been submitted and will not be submitted either in part or in full, "
        "for the award of any other degree or diploma and the same is certified.",
        size=12,
        align=WD_ALIGN_PARAGRAPH.JUSTIFY,
        line_spacing=1.5,
        space_before=6,
        space_after=24,
    )
    add_p(doc, "Signature of the Guide:", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.2, space_before=10, space_after=6)
    add_p(doc, f"Name: {GUIDE_NAME}", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.2, space_before=2, space_after=6)
    add_p(doc, "Date: [Date]", size=12, bold=False, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.2, space_before=2, space_after=24)

    for line_l, line_r in [
        ("Signature of the Examiner 1", "Signature of the Examiner 2"),
        ("Name: [Examiner 1 Name]", "Name: [Examiner 2 Name]"),
        ("Date: [Date]", "Date: [Date]"),
    ]:
        pe = doc.add_paragraph()
        pe.paragraph_format.tab_stops.add_tab_stop(Cm(14.5), WD_TAB_ALIGNMENT.RIGHT)
        pe.paragraph_format.space_before = Pt(8)
        pe.paragraph_format.space_after = Pt(6)
        re_run = pe.add_run(f"{line_l}\t{line_r}")
        re_run.font.name = "Times New Roman"
        re_run.font.size = Pt(12)
        re_run.bold = "Signature" in line_l

    add_p(doc, "Approved by the Head of Department\n[Name of HoD, SCOPE]", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.RIGHT, line_spacing=1.25, space_before=36, space_after=0)

    # Section 1: Roman Numeral Front Matter (5. Abstract, 6. Acknowledgement, 7. TOC, 8. LOF, 9. LOT, 10. Acronyms)
    sec_roman = doc.add_section(WD_SECTION.NEW_PAGE)
    configure_a4_margins(sec_roman)
    set_section_page_numbering(sec_roman, fmt="lowerRoman", start=1)

    # 5. ABSTRACT (Page i)
    add_p(doc, "ABSTRACT", size=14, bold=True, underline=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=0, space_after=6)
    add_p(
        doc,
        "Large Language Models (LLMs) routinely produce fluent, high-confidence statements that are factually incorrect or unfaithful to source context—a phenomenon known as hallucination. Existing mitigation paradigms face a severe latency–accuracy trade-off: black-box multi-sample consistency methods (such as SelfCheckGPT and semantic entropy) require generating 5 to 20 auxiliary completions per prompt, multiplying decoding latency by 5x to 20x, whereas single-pass scalar heuristics (surface token entropy, negative log-likelihood, and logit energy) fail when models state memorized human misconceptions or invert their polarity under benchmark answer-length asymmetries. Moreover, white-box internal probing and runtime mitigation have historically operated as disconnected silos.",
        size=11.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=1, space_after=4,
    )
    add_p(
        doc,
        "Grounded in a PRISMA 2020 systematic literature review of 40 peer-reviewed studies (2020–2025) organized across Six Research Pillars, this project presents TRUEGUARD, a closed-loop feedback control framework for single-pass white-box hallucination detection and graded three-tier runtime mitigation. During a single forward pass of a frozen autoregressive Transformer, TRUEGUARD extracts four complementary internal signals: (1) an Internal State Probe (ISP) averaging L2-regularized logistic probes across four fractional residual-stream depths {0.45, 0.60, 0.75, 0.90}L trained via leakage-free inner grouped out-of-fold (OOF) stacking; (2) a final-quartile Attention Anomaly Score (AAS) measuring normalized causal attention Shannon entropy; (3) a scale-invariant Energy and Entropy Monitor (EEM) combining normalized Shannon entropy (0.6) and quadratic Renyi-2 entropy (0.4); and (4) a Directional Semantic Trajectory (DST) sensor tracking consecutive-token hidden-state cosine drift. The pooled 4-sensor vector is mapped by a standardized L2 logistic combiner into a calibrated risk score r(x,y) in [0, 1] with exact per-sensor log-odds attributions.",
        size=11.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=1, space_after=4,
    )
    add_p(
        doc,
        "Evaluated on an NVIDIA Tesla T4 GPU with TinyLlama-1.1B-Chat-v1.0 across 3,196 real responses spanning four standard benchmarks (5-fold question-grouped cross-validation) and verified on local CPU with GPT-2 (124M), TRUEGUARD achieves a macro-average AUROC of 0.935 (0.986 on HaluEval-Summarization, 0.975 on HaluEval-QA, 0.903 on HaluEval-Dialogue, and 0.876 on TruthfulQA), macro F1 of 0.882, and Expected Calibration Error of 0.031, outperforming single-pass entropy baselines by +30.6 AUROC points. On live open-domain TriviaQA generations (n_cal = 150, n_test = 150), our two-threshold Three-Tier Controller (tau_warning = 0.611, tau_fault = 0.898; SAFE pass-through, Tier 1 annealed re-sampling, Tier 2 Wikipedia retrieval grounding, and Tier 3 calibrated abstention) reduces the hallucination rate among answered queries by 35.5% relative (62.0% -> 40.0%, raising accuracy from 38.0% to 60.0%) and cuts system-wide emitted hallucinations by 72.0% relative (62.0% -> 17.3%) with an AURC of 0.412, while adding only +2.91 ms/token (+8.7% overhead; 4.65x faster than 5-sample consistency).",
        size=11.0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=1, space_after=4,
    )
    add_p(
        doc,
        "Keywords: Large Language Models, Hallucination Detection, Internal State Probing, Attention Entropy, Renyi Entropy, Closed-Loop Feedback Control, Selective Prediction, Retrieval-Augmented Generation, Explainable AI.",
        size=10.5, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=2, space_after=0,
    )

    # 6. ACKNOWLEDGEMENT (Page ii — Matches MIA-Project Template.docx page 8)
    doc.add_page_break()
    add_p(doc, "ACKNOWLEDGEMENT", size=14, bold=True, underline=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.3, space_before=0, space_after=16)
    add_p(
        doc,
        f"It is my pleasure to express with deep sense of gratitude to {GUIDE_NAME}, Professor, School of Computer Science and Engineering, "
        "Vellore Institute of Technology, Chennai, for his constant guidance, continual encouragement, understanding; more than all, he taught me patience in my endeavour. "
        "My association with him is not confined to academics only, but it is a great opportunity for my part of work with an intellectual and expert in the field of Artificial Intelligence and Large Language Model Reliability.",
        size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=10,
    )
    add_p(
        doc,
        "It is with gratitude that I would like to extend my thanks to the visionary leader Dr. G. Viswanathan our Honourable Chancellor, Mr. Sankar Viswanathan, "
        "Dr. Sekar Viswanathan, Dr. G. V. Selvam Vice Presidents, Dr. Sandhya Pentareddy, Executive Director, Ms. Kadhambari S. Viswanathan, Assistant Vice-President, "
        "Dr. V. S. Kanchana Bhaaskaran Vice-Chancellor, and Dr. T. Thyagarajan Pro-Vice Chancellor, VIT Chennai for providing an exceptional working environment and inspiring all of us during the tenure of the course.",
        size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=10,
    )
    add_p(
        doc,
        "Special mention to Dr. Viswanathan V, Dean, Dr. Nithyanandam P, Dr. Suganya G, and Dr. Sweetlin Hemalatha C, Associate Deans, School of Computer Science and Engineering, "
        "Vellore Institute of Technology, Chennai, for spending their valuable time and efforts in sharing their knowledge and for helping us in every aspect.",
        size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=10,
    )
    add_p(
        doc,
        "In jubilant state, I express ingeniously my whole-hearted thanks to [Head of the Department Name / Dr. Appalaraju Muralidhar], Head of the Department, SCOPE, "
        "Vellore Institute of Technology, Chennai, for their valuable support and encouragement to take up and complete the thesis. My sincere thanks to all the faculty and staff members at "
        "Vellore Institute of Technology, Chennai, who helped me acquire the requisite knowledge. I would like to thank my parents for their support. It is indeed a pleasure to thank my friends who encouraged me to take up and complete this task.",
        size=12, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.5, space_before=4, space_after=24,
    )
    add_p(doc, "Place: Chennai", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.3, space_before=12, space_after=6)
    p_ack = doc.add_paragraph()
    p_ack.paragraph_format.tab_stops.add_tab_stop(Cm(14.5), WD_TAB_ALIGNMENT.RIGHT)
    r_ack = p_ack.add_run(f"Date: [Date of Submission]\t{CANDIDATE_NAME}")
    r_ack.font.name = "Times New Roman"
    r_ack.font.size = Pt(12)
    r_ack.bold = True

    # 7. TABLE OF CONTENTS (CONTENTS)
    doc.add_page_break()
    add_p(doc, "CONTENTS", size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=12)
    front_entries = [
        ("ABSTRACT", "i", True, 0.0),
        ("ACKNOWLEDGEMENT", "ii", True, 0.0),
        ("CONTENTS", "iii", True, 0.0),
        ("LIST OF FIGURES", page_map.get("LOF", "v"), True, 0.0),
        ("LIST OF TABLES", page_map.get("LOT", "vi"), True, 0.0),
        ("LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE", page_map.get("ACRONYMS", "vii"), True, 0.0),
    ]
    for title_txt, pg_txt, is_b, ind in front_entries:
        add_dotted_leader_entry(doc, title_txt, pg_txt, bold=is_b, indent_cm=ind, space_before=2.5, space_after=2.5)

    toc_items = [
        ("CHAPTER 1  INTRODUCTION", "CH1", True, 0.0),
        ("1.1 Introduction", "1.1 INTRODUCTION", False, 0.6),
        ("1.2 Background of the Project", "1.2 BACKGROUND OF THE PROJECT", False, 0.6),
        ("1.3 Motivation", "1.3 MOTIVATION", False, 0.6),
        ("1.4 Problem Statement", "1.4 PROBLEM STATEMENT", False, 0.6),
        ("1.5 Research Gap", "1.5 RESEARCH GAP", False, 0.6),
        ("1.6 Objectives", "1.6 OBJECTIVES", False, 0.6),
        ("1.7 Scope of the Project", "1.7 SCOPE OF THE PROJECT", False, 0.6),
        ("1.8 Contributions of the Project", "1.8 CONTRIBUTIONS OF THE PROJECT", False, 0.6),
        ("CHAPTER 2  BACKGROUND AND THEORETICAL FOUNDATION", "CH2", True, 0.0),
        ("2.1 Autoregressive Transformer Decoding Mechanics", "2.1 AUTOREGRESSIVE TRANSFORMER DECODING MECHANICS", False, 0.6),
        ("2.2 Taxonomy of Hallucinations in Large Language Models", "2.2 TAXONOMY OF HALLUCINATIONS IN LARGE LANGUAGE MODELS", False, 0.6),
        ("2.3 Geometry of Truthfulness in Intermediate Hidden Manifolds", "2.3 GEOMETRY OF TRUTHFULNESS IN INTERMEDIATE HIDDEN MANIFOLDS", False, 0.6),
        ("2.4 Causal Self-Attention Grounding and Entropy Dynamics", "2.4 CAUSAL SELF-ATTENTION GROUNDING AND ENTROPY DYNAMICS", False, 0.6),
        ("2.5 Information-Theoretic Uncertainty: Shannon, Renyi-2 and Free Energy", "2.5 INFORMATION-THEORETIC UNCERTAINTY: SHANNON, RENYI-2 AND FREE ENERGY", False, 0.6),
        ("2.6 Directional Semantic Trajectory and Representation Drift", "2.6 DIRECTIONAL SEMANTIC TRAJECTORY AND REPRESENTATION DRIFT", False, 0.6),
        ("2.7 Selective Prediction and Closed-Loop Feedback Control Theory", "2.7 SELECTIVE PREDICTION AND CLOSED-LOOP FEEDBACK CONTROL THEORY", False, 0.6),
        ("CHAPTER 3  LITERATURE REVIEW", "CH3", True, 0.0),
        ("3.1 PRISMA 2020 Systematic Review Methodology", "3.1 PRISMA 2020 SYSTEMATIC REVIEW METHODOLOGY", False, 0.6),
        ("3.2 Pillar 1: Internal-State Based Hallucination Detection", "3.2 PILLAR 1: INTERNAL-STATE BASED HALLUCINATION DETECTION", False, 0.6),
        ("3.3 Pillar 2: Uncertainty Quantification and Entropy-Based Methods", "3.3 PILLAR 2: UNCERTAINTY QUANTIFICATION AND ENTROPY-BASED METHODS", False, 0.6),
        ("3.4 Pillar 3: Attention-Based and Multi-Signal Detection", "3.4 PILLAR 3: ATTENTION-BASED AND MULTI-SIGNAL DETECTION", False, 0.6),
        ("3.5 Pillar 4: Evaluation Benchmarks and Trustworthiness Taxonomies", "3.5 PILLAR 4: EVALUATION BENCHMARKS AND TRUSTWORTHINESS TAXONOMIES", False, 0.6),
        ("3.6 Pillar 5: Mitigation Through Calibration, Retrieval and Verification", "3.6 PILLAR 5: MITIGATION THROUGH CALIBRATION, RETRIEVAL AND VERIFICATION", False, 0.6),
        ("3.7 Pillar 6: Explainability and Human Trust Calibration", "3.7 PILLAR 6: EXPLAINABILITY AND HUMAN TRUST CALIBRATION", False, 0.6),
        ("3.8 Cross-Pillar Gap Synthesis and TRUEGUARD Mapping", "3.8 CROSS-PILLAR GAP SYNTHESIS AND TRUEGUARD MAPPING", False, 0.6),
        ("CHAPTER 4  SYSTEM ANALYSIS, REQUIREMENTS AND CONTROL ARCHITECTURE", "CH4", True, 0.0),
        ("4.1 Critical Analysis of Existing Hallucination Detection Systems", "4.1 CRITICAL ANALYSIS OF EXISTING HALLUCINATION DETECTION SYSTEMS", False, 0.6),
        ("4.2 Proposed TRUEGUARD Closed-Loop Control System", "4.2 PROPOSED TRUEGUARD CLOSED-LOOP CONTROL SYSTEM", False, 0.6),
        ("4.3 End-to-End Closed-Loop Control Architecture", "4.3 END-TO-END CLOSED-LOOP CONTROL ARCHITECTURE", False, 0.6),
        ("4.4 Functional Requirements Specification", "4.4 FUNCTIONAL REQUIREMENTS SPECIFICATION", False, 0.6),
        ("4.5 Non-Functional Requirements Specification", "4.5 NON-FUNCTIONAL REQUIREMENTS SPECIFICATION", False, 0.6),
        ("4.6 Hardware and Software Technology Stack", "4.6 HARDWARE AND SOFTWARE TECHNOLOGY STACK", False, 0.6),
        ("CHAPTER 5  DATASET CURATION, MATHEMATICAL MODEL DESIGN AND ALGORITHMIC FORMULATION", "CH5", True, 0.0),
        ("5.1 Benchmark Dataset Curation and Preprocessing", "5.1 BENCHMARK DATASET CURATION AND PREPROCESSING", False, 0.6),
        ("5.2 Question-Grouped Splitting and Data-Leakage Prevention", "5.2 QUESTION-GROUPED SPLITTING AND DATA-LEAKAGE PREVENTION", False, 0.6),
        ("5.3 Sensor 1: Multi-Layer Supervised Internal State Probe (ISP)", "5.3 SENSOR 1: MULTI-LAYER SUPERVISED INTERNAL STATE PROBE (ISP)", False, 0.6),
        ("5.4 Sensor 2: Final-Quartile Attention Anomaly Score (AAS)", "5.4 SENSOR 2: FINAL-QUARTILE ATTENTION ANOMALY SCORE (AAS)", False, 0.6),
        ("5.5 Sensor 3: Hybrid Shannon and Renyi-2 Energy-Entropy Monitor (EEM)", "5.5 SENSOR 3: HYBRID SHANNON AND RENYI-2 ENERGY-ENTROPY MONITOR (EEM)", False, 0.6),
        ("5.6 Sensor 4: Directional Semantic Trajectory (DST)", "5.6 SENSOR 4: DIRECTIONAL SEMANTIC TRAJECTORY (DST)", False, 0.6),
        ("5.7 Calibrated Logistic Fusion and Log-Odds Attribution", "5.7 CALIBRATED LOGISTIC FUSION AND LOG-ODDS ATTRIBUTION", False, 0.6),
        ("5.8 Two-Threshold Calibration and Three-Tier Actuation", "5.8 TWO-THRESHOLD CALIBRATION AND THREE-TIER ACTUATION", False, 0.6),
        ("CHAPTER 6  SYSTEM IMPLEMENTATION AND CODE ARCHITECTURE", "CH6", True, 0.0),
        ("6.1 Modular Package Structure and Execution Workflow", "6.1 MODULAR PACKAGE STRUCTURE AND EXECUTION WORKFLOW", False, 0.6),
        ("6.2 Multi-Layer Inner OOF Probe Implementation", "6.2 MULTI-LAYER INNER OOF PROBE IMPLEMENTATION", False, 0.6),
        ("6.3 Single-Pass Sensor Extraction and Dual-Mode Monitor", "6.3 SINGLE-PASS SENSOR EXTRACTION AND DUAL-MODE MONITOR", False, 0.6),
        ("6.4 Logistic Fusion and Log-Odds Explainability Engine", "6.4 LOGISTIC FUSION AND LOG-ODDS EXPLAINABILITY ENGINE", False, 0.6),
        ("6.5 Closed-Loop Three-Tier Controller and Wikipedia RAG", "6.5 CLOSED-LOOP THREE-TIER CONTROLLER AND WIKIPEDIA RAG", False, 0.6),
        ("6.6 Automated Numerical Equivalence and Integrity Verification", "6.6 AUTOMATED NUMERICAL EQUIVALENCE AND INTEGRITY VERIFICATION", False, 0.6),
        ("CHAPTER 7  EXPERIMENTAL SETUP, DETECTION RESULTS AND ABLATION ANALYSIS", "CH7", True, 0.0),
        ("7.1 Hardware Testbeds, Backbone Models and Evaluation Metrics", "7.1 HARDWARE TESTBEDS, BACKBONE MODELS AND EVALUATION METRICS", False, 0.6),
        ("7.2 In-Distribution Multi-Benchmark Detection Results", "7.2 IN-DISTRIBUTION MULTI-BENCHMARK DETECTION RESULTS", False, 0.6),
        ("7.3 Receiver Operating Characteristic (ROC) Curve Analysis", "7.3 RECEIVER OPERATING CHARACTERISTIC (ROC) CURVE ANALYSIS", False, 0.6),
        ("7.4 Leave-One-Sensor-Out Ablation and Complementarity", "7.4 LEAVE-ONE-SENSOR-OUT ABLATION AND COMPLEMENTARITY", False, 0.6),
        ("7.5 Confusion Matrices and Risk Score Distributions", "7.5 CONFUSION MATRICES AND RISK SCORE DISTRIBUTIONS", False, 0.6),
        ("7.6 Polarity Inversion Diagnostics and Cross-Dataset Transfer", "7.6 POLARITY INVERSION DIAGNOSTICS AND CROSS-DATASET TRANSFER", False, 0.6),
        ("CHAPTER 8  CLOSED-LOOP MITIGATION, LATENCY PROFILING AND LIMITATIONS", "CH8", True, 0.0),
        ("8.1 Live Three-Tier Mitigation on Open-Domain TriviaQA", "8.1 LIVE THREE-TIER MITIGATION ON OPEN-DOMAIN TRIVIAQA", False, 0.6),
        ("8.2 Selective Prediction and Risk-Coverage (AURC) Analysis", "8.2 SELECTIVE PREDICTION AND RISK-COVERAGE (AURC) ANALYSIS", False, 0.6),
        ("8.3 Hardware Latency Profiling on Tesla T4 GPU and CPU", "8.3 HARDWARE LATENCY PROFILING ON TESLA T4 GPU AND CPU", False, 0.6),
        ("8.4 Limitations and Threats to Validity", "8.4 LIMITATIONS AND THREATS TO VALIDITY", False, 0.6),
        ("CHAPTER 9  CONCLUSION AND FUTURE WORK", "CH9", True, 0.0),
        ("9.1 Conclusion", "9.1 CONCLUSION", False, 0.6),
        ("9.2 Future Work", "9.2 FUTURE WORK", False, 0.6),
        ("APPENDICES", "APPENDICES", True, 0.0),
        ("Appendix 1 — Benchmark Dataset Manifest and JSONL Schema Inventory", "APPENDIX 1", False, 0.6),
        ("Appendix 2 — Verified Hyperparameters, Calibrated Thresholds and Equivalence Log", "APPENDIX 2", False, 0.6),
        ("Appendix 3 — Reproducible CLI Operating Procedure and Representative Traces", "APPENDIX 3", False, 0.6),
        ("REFERENCES", "REFERENCES", True, 0.0),
    ]
    for label_txt, key, is_b, ind in toc_items:
        add_dotted_leader_entry(doc, label_txt, page_map.get(key, "1"), bold=is_b, indent_cm=ind, space_before=3.5 if is_b else 1.5, space_after=1.5)

    # 8. LIST OF FIGURES (6 Consolidated Visual Figures Arranged 3-per-Page on 2 Dedicated Pages)
    doc.add_page_break()
    add_p(doc, "LIST OF FIGURES", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=12)
    lof_items = [
        ("Figure 7.1: TRUEGUARD Closed-Loop Architecture (Left) and Multi-Benchmark Detection AUROC Comparison (Right)", "FIGURE 7.1"),
        ("Figure 7.2: Out-of-Fold ROC Curves on TruthfulQA (Left) and HaluEval-Summarization (Right) on TinyLlama-1.1B", "FIGURE 7.2"),
        ("Figure 7.3: Leave-One-Sensor-Out Ablation on TruthfulQA (Left) and 4x4 Cross-Benchmark Transfer Matrix (Right)", "FIGURE 7.3"),
        ("Figure 8.1: Three-Tier Controller Routing Breakdown and Hallucination Reduction on Live TriviaQA (n = 150)", "FIGURE 8.1"),
        ("Figure 8.2: Selective Prediction Factual Accuracy and Risk–Coverage (AURC) Curves on Live TriviaQA", "FIGURE 8.2"),
        ("Figure 8.3: Per-Token Inference Latency Comparison on NVIDIA Tesla T4 GPU (TinyLlama-1.1B) and Local CPU (GPT-2)", "FIGURE 8.3"),
    ]
    for fig_label, fig_key in lof_items:
        add_dotted_leader_entry(doc, fig_label, page_map.get(fig_key, "1"), bold=False, indent_cm=0.0, space_before=4.0, space_after=4.0)

    # 9. LIST OF TABLES
    doc.add_page_break()
    add_p(doc, "LIST OF TABLES", size=14, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.2, space_before=0, space_after=10)
    lot_items = [
        ("Table 3.1: PRISMA 2020 Screening Criteria and Six-Pillar Distribution of 40 Primary Studies", "TABLE 3.1"),
        ("Table 3.1B: PRISMA 2020 Stage-by-Stage Screening and Exclusion Breakdown (2020–2026)", "TABLE 3.1B"),
        ("Table 3.2: Pillar 1 Literature Review Matrix — Internal-State Based Detection (Papers 1–8)", "TABLE 3.2"),
        ("Table 3.3: Pillar 2 Literature Review Matrix — Uncertainty Quantification & Entropy (Papers 9–14)", "TABLE 3.3"),
        ("Table 3.4: Pillar 3 Literature Review Matrix — Attention & Multi-Signal Detection (Papers 15–18)", "TABLE 3.4"),
        ("Table 3.5: Pillar 4 Literature Review Matrix — Evaluation Benchmarks & Taxonomies (Papers 19–27)", "TABLE 3.5"),
        ("Table 3.6: Pillar 5 Literature Review Matrix — Mitigation via Calibration, RAG & Verification (Papers 28–38)", "TABLE 3.6"),
        ("Table 3.7: Pillar 6 Literature Review Matrix — Explainability & Human Trust Calibration (Papers 39–40)", "TABLE 3.7"),
        ("Table 3.8: Cross-Pillar Synthesis of Research Gaps and TRUEGUARD Architectural Resolution", "TABLE 3.8"),
        ("Table 4.1B: Closed-Loop Feedback Control Subsystem Block Specification for TRUEGUARD", "TABLE 4.1B"),
        ("Table 4.1: Functional Requirements Specification for TRUEGUARD v2", "TABLE 4.1"),
        ("Table 4.2: Non-Functional Requirements Specification for TRUEGUARD v2", "TABLE 4.2"),
        ("Table 4.3: Hardware and Software Technology Stack", "TABLE 4.3"),
        ("Table 5.1: Curated Benchmark Datasets and Evaluation Split Architecture", "TABLE 5.1"),
        ("Table 5.1B: Two-Level Question-Grouped Cross-Validation and Inner OOF Stacking Protocol", "TABLE 5.1B"),
        ("Table 6.1: TRUEGUARD v2 Production Source Modules and Functional Responsibilities", "TABLE 6.1"),
        ("Table 7.1: In-Distribution 5-Fold Grouped CV Detection Performance on TinyLlama-1.1B (Tesla T4 GPU)", "TABLE 7.1"),
        ("Table 7.2: Architecture-Generality Detection Verification on GPT-2 124M (Local CPU)", "TABLE 7.2"),
        ("Table 7.1B: Comprehensive 10-Method Detection Comparison Across Benchmarks on TinyLlama-1.1B", "TABLE 7.1B"),
        ("Table 7.2B: Out-of-Fold ROC True Positive Rate (TPR) Operating Points on TruthfulQA", "TABLE 7.2B"),
        ("Table 7.3B: Out-of-Fold ROC True Positive Rate (TPR) Operating Points on HaluEval-Summarization", "TABLE 7.3B"),
        ("Table 7.3: Leave-One-Sensor-Out Ablation AUROC and 10% FPR Complementarity on TinyLlama-1.1B", "TABLE 7.3"),
        ("Table 7.4B: Single-Sensor and Leave-One-Out Ablation Metrics on TruthfulQA", "TABLE 7.4B"),
        ("Table 7.5B: Single-Sensor and Leave-One-Out Ablation Metrics on HaluEval-QA", "TABLE 7.5B"),
        ("Table 7.6B: Out-of-Fold 2x2 Confusion Matrix Counts and Classification Metrics", "TABLE 7.6B"),
        ("Table 7.7B: Calibrated Out-of-Fold Risk Score Distribution by Regime", "TABLE 7.7B"),
        ("Table 7.4: Cross-Benchmark Zero-Shot Transfer AUROC Matrix on TinyLlama-1.1B", "TABLE 7.4"),
        ("Table 7.8B: Cross-Benchmark Transfer Pairs and Learned Sensor Weight Vectors", "TABLE 7.8B"),
        ("Table 8.1: Closed-Loop Three-Tier Mitigation Results on Live TriviaQA Generations", "TABLE 8.1"),
        ("Table 8.1B: Controller Tier-by-Tier Routing, Active Repair Count, and Hallucination Reduction", "TABLE 8.1B"),
        ("Table 8.2: Selective Prediction Factual Accuracy (%) Across Coverage Levels and AURC on TriviaQA", "TABLE 8.2"),
        ("Table 8.2B: Selective Prediction Factual Accuracy and Risk Across Coverage Operating Points", "TABLE 8.2B"),
        ("Table 8.3: Real Hardware Per-Token Inference Latency and Speedup Profile (Tesla T4 GPU and CPU)", "TABLE 8.3"),
        ("Table 8.3B: Per-Stage Computational Latency Breakdown on Tesla T4 GPU and Local CPU", "TABLE 8.3B"),
        ("Table A1.1: Verified Benchmark JSONL Dataset Manifest", "TABLE A1.1"),
        ("Table A2.1: Complete Hyperparameter and Calibrated Threshold Registry for TRUEGUARD v2", "TABLE A2.1"),
        ("Table A3.1: Representative Query-Level Closed-Loop Controller Decision Traces on Live TriviaQA", "TABLE A3.1"),
    ]
    for tab_label, tab_key in lot_items:
        add_dotted_leader_entry(doc, tab_label, page_map.get(tab_key, "1"), bold=False, indent_cm=0.0, space_before=1.2, space_after=1.2)

    # 10. LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE
    doc.add_page_break()
    add_p(doc, "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE", size=13, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.1, space_before=0, space_after=4)
    add_styled_table(
        doc,
        None,
        None,
        ["Acronym / Mathematical Symbol", "Full Expansion and Technical Definition"],
        ACRONYMS_AND_SYMBOLS,
        [4.2, 10.4],
        font_size=7.8,
    )
