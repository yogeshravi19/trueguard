"""
End-to-End Document Assembler & Two-Pass Exact Page-Number Resolver for FINAL_REPORT.docx
and FINAL_REPORT.pdf.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List

import docx
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm, Pt
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
from build_final_report_front import build_front_matter
from build_final_report_helpers import (
    FIG_DIR,
    add_apa_reference_paragraph,
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
from report_references_data import APA_REFERENCES


def render_section_list(doc, sections_list) -> None:
    for sec_h, sub_h, paras in sections_list:
        if sec_h:
            add_section_heading(doc, sec_h)
        if sub_h:
            add_subsection_heading(doc, sub_h)
        for p_txt in paras:
            if p_txt.startswith("EQUATION_"):
                parts = p_txt.split(":", 1)
                eq_id = parts[0].replace("EQUATION_", "").replace("_", ".")
                add_equation_block(doc, parts[1].strip(), eq_id)
            else:
                add_p(doc, p_txt)


def build_chapter_1_and_2(doc) -> None:
    # Start new section for Main Text (Arabic page numbering 1, 2, 3...)
    sec_main = doc.add_section(WD_SECTION.NEW_PAGE)
    configure_a4_margins(sec_main)
    set_section_page_numbering(sec_main, fmt="decimal", start=1)

    add_chapter_heading(doc, 1, "INTRODUCTION", page_break_before=False)
    render_section_list(doc, CH1_SECTIONS)

    add_chapter_heading(doc, 2, "BACKGROUND AND THEORETICAL FOUNDATION", page_break_before=True)
    render_section_list(doc, CH2_SECTIONS)


def build_chapter_3(doc) -> None:
    add_chapter_heading(doc, 3, "LITERATURE REVIEW")

    add_section_heading(doc, "3.1 PRISMA 2020 SYSTEMATIC REVIEW METHODOLOGY")
    add_p(doc, "To establish a transparent, rigorous, and repeatable synthesis of the hallucination detection, explainability, and mitigation landscape prior to designing TRUEGUARD, a systematic literature review was conducted in strict accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA 2020) guidelines. We queried five major computer science and systems engineering databases—arXiv.org (214 records), Scopus (186 records), IEEE Xplore Digital Library (112 records), Web of Science Core Collection (92 records), and ACM Digital Library (84 records)—over the search window from January 1, 2020 through February 28, 2026 using the boolean query: (\"Large Language Models\" OR \"LLM\") AND (\"hallucination\" OR \"factual error\") AND (\"detection\" OR \"mitigation\" OR \"uncertainty\" OR \"attention\" OR \"internal states\" OR \"explainability\").")
    add_p(doc, "Six formal Inclusion Criteria (IC1: direct focus on LLM hallucination detection, uncertainty, explainability, and mitigation; IC2: clear mathematical formulations or public benchmark evaluations; IC3: autoregressive transformers such as LLaMA, GPT, Mistral, or Falcon; IC4: peer-reviewed journals/conferences or recognized technical preprints; IC5: English manuscripts; IC6: alignment with systems and control concepts such as state monitoring, fault detection, and closed-loop feedback) and four Exclusion Criteria (EC1: general NLP without hallucination evaluation; EC2: non-empirical editorials/notes; EC3: insufficient architectural detail; EC4: duplicate/superseded workshop abstracts) were enforced. As depicted in Figure 3.1 and summarized in Table 3.1, Stage 1 identification returned 688 initial records; removing 196 cross-database duplicates left 492 unique records. In Stage 2 title and abstract screening, 324 off-topic records were excluded (218 general NLP/off-topic papers and 106 non-technical notes/demos), leaving 168 candidate articles for Stage 3 full-text eligibility appraisal across four quality criteria (Methodological Rigor, Benchmark Validity, Metric Reliability, and Deployment Transparency). Full-text review excluded 128 articles (54 prompt heuristics without internal probing, 42 lacking standard baselines, and 32 redundant methodologies), yielding the final authoritative corpus of n = 40 studies (20 Core Architectural Studies and 20 Foundational Benchmarks and Mitigation Frameworks) organized across Six Research Pillars.")
    add_figure_with_caption(doc, FIG_DIR / "fig_prisma_flow.png", "3.1", "PRISMA 2020 Systematic Literature Review Selection Flow (2020–2025)", width_cm=13.8)
    add_styled_table(
        doc,
        "3.1",
        "PRISMA 2020 Screening Criteria and Six-Pillar Distribution of 40 Primary Studies",
        ["Pillar ID & Thematic Scope", "Included Papers", "Primary Signal / Mechanism Investigated", "Representative Studies"],
        [
            ("Pillar 1: Internal-State Based Detection", "8 papers (20.0%)", "Residual-stream hidden state linear/MLP probes, activation steering, and layer distribution shift.", "Azaria & Mitchell [27], Li et al. [28], Su et al. [1], Zhang et al. [2, 5], Dasgupta et al. [13], Chen et al. [38]"),
            ("Pillar 2: Uncertainty & Entropy Methods", "6 papers (15.0%)", "Shannon/Renyi entropy, Boltzmann logit energy, semantic entropy probes, and multi-sample consistency.", "Manakul et al. [21], Han et al. [14], Ma et al. [4], Kang et al. [7], Moslonka et al. [17]"),
            ("Pillar 3: Attention & Multi-Signal Detection", "4 papers (10.0%)", "Causal attention head entropy, source-token grounding drop, and kernel log-determinants.", "Hajji et al. [9], Vazhentsev et al. [11], Sriramanan et al. [12], Mundler et al. [36]"),
            ("Pillar 4: Benchmarks & Taxonomies", "9 papers (22.5%)", "Adversarial misconception QA, paired QA/dialogue/summary datasets, and atomic factuality rubrics.", "Lin et al. [22], Li et al. [29], Min et al. [23], Huang et al. [3], Ji et al. [35], Chern et al. [34]"),
            ("Pillar 5: Mitigation, Calibration & RAG", "11 papers (27.5%)", "Dense passage RAG, self-reflective tokens, Chain-of-Verification, RARR, CRITIC, and RL abstention.", "Lewis et al. [25], Asai et al. [26], Dhuliawala et al. [24], Gao et al. [33], Wu et al. [15], Du et al. [31]"),
            ("Pillar 6: Explainability & Human Trust", "2 papers (5.0%)", "Four-dimensional LLM XAI taxonomy and human trust calibration via contrastive explanations.", "Herrera [8], Sharma et al. [19]"),
        ],
        [3.4, 1.8, 5.0, 4.4],
        font_size=8.8,
    )

    # Render each of the 6 Pillars: Narrative + Structured Matrix Table (all 40 papers)
    for idx, (_, pillar_title, pillar_desc, rows) in enumerate(PILLARS):
        p_num = idx + 1
        add_section_heading(doc, PILLAR_SECTION_TITLES[idx])
        for para_text in PILLAR_NARRATIVES[p_num]:
            add_p(doc, para_text)
        tab_id = f"3.{idx + 2}"
        cap_clean = PILLAR_TABLE_CAPTIONS[idx].split(": ", 1)[1]
        add_styled_table(
            doc,
            tab_id,
            cap_clean,
            ["Paper Title", "Author(s) & ID", "Year", "Method / Framework", "Key Contribution", "Gap Identified"],
            rows,
            [3.0, 1.8, 0.9, 2.3, 3.3, 3.3],
            font_size=8.5,
        )

    add_section_heading(doc, "3.8 CROSS-PILLAR GAP SYNTHESIS AND TRUEGUARD MAPPING")
    add_p(doc, "Synthesizing all 40 primary studies across Pillars 1 through 6 reveals a clear structural convergence: while individual internal signals (hidden states, attention maps, and output logits) and individual post-hoc interventions (re-sampling, RAG, and abstention) have matured rapidly, no unified architecture connects single-pass multi-sensor white-box estimation to a graded, risk-verified closed-loop actuator with per-sensor explainability. Table 3.8 maps each pillar's cross-corpus gap directly to the corresponding module and verified hardware result in TRUEGUARD v2.")
    add_styled_table(
        doc,
        "3.8",
        "Cross-Pillar Synthesis of Research Gaps and TRUEGUARD Architectural Resolution (40-Study Corpus)",
        ["Research Pillar & IDs", "Core Literature Finding", "Cross-Corpus Gap Identified", "TRUEGUARD v2 Architectural Module", "Verified Tesla T4 GPU Outcome"],
        CROSS_PILLAR_SYNTHESIS_ROWS,
        [2.5, 2.7, 2.9, 3.2, 3.3],
        font_size=8.5,
    )


def build_chapter_4(doc) -> None:
    add_chapter_heading(doc, 4, "SYSTEM ANALYSIS, REQUIREMENTS AND CONTROL ARCHITECTURE")
    render_section_list(doc, CH4_SECTIONS)

    add_section_heading(doc, "4.3 END-TO-END CLOSED-LOOP CONTROL ARCHITECTURE")
    add_p(doc, "Figure 4.1 illustrates the complete end-to-end closed-loop control block diagram of TRUEGUARD, showing the five interacting subsystems: (1) Input Prompt Tokenization, (2) Frozen Autoregressive Transformer Plant, (3) Single-Pass 4-Sensor Bank (`ISP`, `AAS`, `EEM`, `DST`), (4) Leakage-Free Out-of-Fold State Estimator & Log-Odds Attribution Engine, and (5) Two-Threshold Three-Tier Graded Actuator with closed-loop risk re-verification.")
    add_figure_with_caption(doc, FIG_DIR / "fig_system_architecture.png", "4.1", "TRUEGUARD Closed-Loop Hallucination Detection and Mitigation Architecture", width_cm=14.4)

    add_section_heading(doc, "4.4 FUNCTIONAL REQUIREMENTS SPECIFICATION")
    add_p(doc, "Table 4.1 specifies the eight core functional requirements (`FR-01` through `FR-08`) governing sensor extraction, out-of-fold calibration, log-odds attribution, and three-tier actuation in TRUEGUARD v2.")
    add_styled_table(
        doc,
        "4.1",
        "Functional Requirements Specification for TRUEGUARD v2",
        ["Req. ID", "Functional Requirement Title", "Detailed Technical Specification"],
        FUNCTIONAL_REQUIREMENTS_TABLE,
        [1.8, 4.0, 8.8],
        font_size=9.2,
    )

    add_section_heading(doc, "4.5 NON-FUNCTIONAL REQUIREMENTS SPECIFICATION")
    add_p(doc, "Table 4.2 specifies the five non-functional requirements (`NFR-01` through `NFR-05`) enforcing dual-mode numerical equivalence, single-pass latency bounds, zero group leakage, deterministic seeding, and graceful sensor fallback.")
    add_styled_table(
        doc,
        "4.2",
        "Non-Functional Requirements Specification for TRUEGUARD v2",
        ["Req. ID", "Non-Functional Requirement", "Verification Criterion & Measured Compliance"],
        NON_FUNCTIONAL_REQUIREMENTS_TABLE,
        [1.8, 4.0, 8.8],
        font_size=9.2,
    )

    add_section_heading(doc, "4.6 HARDWARE AND SOFTWARE TECHNOLOGY STACK")
    add_p(doc, "Table 4.3 summarizes the hardware, deep learning, statistical, retrieval, and dataset stack used to build and verify TRUEGUARD v2.")
    add_styled_table(
        doc,
        "4.3",
        "Hardware and Software Technology Stack",
        ["Layer / Category", "Technology / Component", "Operational Role in TRUEGUARD v2"],
        TECH_STACK_TABLE,
        [3.2, 4.4, 7.0],
        font_size=9.2,
    )


def build_references_section(doc) -> None:
    p_ref = add_p(doc, "REFERENCES", size=16, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=0, space_after=12, keep_with_next=True)
    p_ref.paragraph_format.page_break_before = True
    for ref in APA_REFERENCES:
        add_apa_reference_paragraph(doc, ref)


def assemble_docx(docx_path: Path, page_map: Dict[str, str]) -> None:
    doc = docx.Document()
    normal_style = doc.styles["Normal"]
    normal_style.font.name = "Times New Roman"
    normal_style.font.size = Pt(12)

    build_front_matter(doc, page_map)
    build_chapter_1_and_2(doc)
    build_chapter_3(doc)
    build_chapter_4(doc)
    build_chapter_5(doc)
    build_chapter_6(doc)
    build_chapter_7(doc)
    build_chapter_8(doc)
    build_chapter_9(doc)
    build_appendices(doc)
    build_references_section(doc)

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(docx_path))


def export_docx_to_pdf_via_word(docx_path: Path, pdf_path: Path) -> None:
    from generate_hd_stacked_figures import inject_hd_images_into_pdf
    ps_cmd = (
        f"$w = New-Object -ComObject Word.Application; "
        f"$w.Visible = $false; "
        f"$d = $w.Documents.Open('{docx_path}'); "
        f"$d.Repaginate(); "
        f"foreach ($f in $d.Fields) {{ $f.Update() | Out-Null }}; "
        f"$d.Save(); "
        f"$d.SaveAs([ref]'{pdf_path}', [ref]17); "
        f"$d.Close(); "
        f"$w.Quit()"
    )
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True)
    inject_hd_images_into_pdf(pdf_path)


def int_to_roman(n: int) -> str:
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    res = []
    for v, s in vals:
        while n >= v:
            res.append(s)
            n -= v
    return "".join(res)


def extract_exact_page_map_from_pdf(pdf_path: Path) -> Tuple[Dict[str, str], int, int]:
    """
    Scan the rendered PDF with PyMuPDF to determine:
      - Total PDF pages
      - The PDF page index where CHAPTER 1 begins (Arabic page 1)
      - Exact Roman numeral page for front-matter sections (LOF, LOT, ACRONYMS)
      - Exact Arabic page number for every chapter, section, figure, table, appendix, and REFERENCES
    """
    pdf = fitz.open(str(pdf_path))
    total_pages = len(pdf)
    ch1_pdf_idx = None

    for idx in range(total_pages):
        txt = pdf[idx].get_text("text")
        if "CHAPTER 1" in txt and "1.1 INTRODUCTION" in txt:
            ch1_pdf_idx = idx
            break
    if ch1_pdf_idx is None:
        ch1_pdf_idx = 10

    page_map: Dict[str, str] = {}
    # Front matter Roman pages (Abstract starts at PDF index 4 -> Roman 'i')
    for idx in range(4, ch1_pdf_idx):
        txt = pdf[idx].get_text("text")
        roman_str = int_to_roman(idx - 3)
        if "LIST OF FIGURES" in txt and "Figure 7.1:" in txt and "LOF" not in page_map:
            page_map["LOF"] = roman_str
        if "LIST OF TABLES" in txt and "Table 3.1:" in txt and "LOT" not in page_map:
            page_map["LOT"] = roman_str
        if "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE" in txt and "Acronym / Mathematical Symbol" in txt and "ACRONYMS" not in page_map:
            page_map["ACRONYMS"] = roman_str

    # Main matter Arabic pages (starting at ch1_pdf_idx -> Arabic page 1)
    search_targets = [
        ("CH1", "CHAPTER 1"),
        ("CH2", "CHAPTER 2"),
        ("CH3", "CHAPTER 3"),
        ("CH4", "CHAPTER 4"),
        ("CH5", "CHAPTER 5"),
        ("CH6", "CHAPTER 6"),
        ("CH7", "CHAPTER 7"),
        ("CH8", "CHAPTER 8"),
        ("CH9", "CHAPTER 9"),
        ("APPENDICES", "APPENDICES"),
        ("APPENDIX 1", "APPENDIX 1 — BENCHMARK DATASET MANIFEST"),
        ("APPENDIX 2", "APPENDIX 2 — VERIFIED HYPERPARAMETERS"),
        ("APPENDIX 3", "APPENDIX 3 — REPRODUCIBLE CLI OPERATING PROCEDURE"),
        ("REFERENCES", "REFERENCES"),
    ]
    # Add all section headings X.Y
    sec_prefixes = [
        "1.1 INTRODUCTION", "1.2 BACKGROUND OF THE PROJECT", "1.3 MOTIVATION", "1.4 PROBLEM STATEMENT",
        "1.5 RESEARCH GAP", "1.6 OBJECTIVES", "1.7 SCOPE OF THE PROJECT", "1.8 CONTRIBUTIONS OF THE PROJECT",
        "2.1 AUTOREGRESSIVE TRANSFORMER DECODING MECHANICS", "2.2 TAXONOMY OF HALLUCINATIONS IN LARGE LANGUAGE MODELS",
        "2.3 GEOMETRY OF TRUTHFULNESS IN INTERMEDIATE HIDDEN MANIFOLDS", "2.4 CAUSAL SELF-ATTENTION GROUNDING AND ENTROPY DYNAMICS",
        "2.5 INFORMATION-THEORETIC UNCERTAINTY: SHANNON, RENYI-2 AND FREE ENERGY", "2.6 DIRECTIONAL SEMANTIC TRAJECTORY AND REPRESENTATION DRIFT",
        "2.7 SELECTIVE PREDICTION AND CLOSED-LOOP FEEDBACK CONTROL THEORY",
        "3.1 PRISMA 2020 SYSTEMATIC REVIEW METHODOLOGY",
        *PILLAR_SECTION_TITLES,
        "3.8 CROSS-PILLAR GAP SYNTHESIS AND TRUEGUARD MAPPING",
        "4.1 CRITICAL ANALYSIS OF EXISTING HALLUCINATION DETECTION SYSTEMS",
        "4.2 PROPOSED TRUEGUARD CLOSED-LOOP CONTROL SYSTEM",
        "4.3 END-TO-END CLOSED-LOOP CONTROL ARCHITECTURE",
        "4.4 FUNCTIONAL REQUIREMENTS SPECIFICATION",
        "4.5 NON-FUNCTIONAL REQUIREMENTS SPECIFICATION",
        "4.6 HARDWARE AND SOFTWARE TECHNOLOGY STACK",
        "5.1 BENCHMARK DATASET CURATION AND PREPROCESSING",
        "5.2 QUESTION-GROUPED SPLITTING AND DATA-LEAKAGE PREVENTION",
        "5.3 SENSOR 1: MULTI-LAYER SUPERVISED INTERNAL STATE PROBE (ISP)",
        "5.4 SENSOR 2: FINAL-QUARTILE ATTENTION ANOMALY SCORE (AAS)",
        "5.5 SENSOR 3: HYBRID SHANNON AND RENYI-2 ENERGY-ENTROPY MONITOR (EEM)",
        "5.6 SENSOR 4: DIRECTIONAL SEMANTIC TRAJECTORY (DST)",
        "5.7 CALIBRATED LOGISTIC FUSION AND LOG-ODDS ATTRIBUTION",
        "5.8 TWO-THRESHOLD CALIBRATION AND THREE-TIER ACTUATION",
        "6.1 MODULAR PACKAGE STRUCTURE AND EXECUTION WORKFLOW",
        "6.2 MULTI-LAYER INNER OOF PROBE IMPLEMENTATION",
        "6.3 SINGLE-PASS SENSOR EXTRACTION AND DUAL-MODE MONITOR",
        "6.4 LOGISTIC FUSION AND LOG-ODDS EXPLAINABILITY ENGINE",
        "6.5 CLOSED-LOOP THREE-TIER CONTROLLER AND WIKIPEDIA RAG",
        "6.6 AUTOMATED NUMERICAL EQUIVALENCE AND INTEGRITY VERIFICATION",
        "7.1 HARDWARE TESTBEDS, BACKBONE MODELS AND EVALUATION METRICS",
        "7.2 IN-DISTRIBUTION MULTI-BENCHMARK DETECTION RESULTS",
        "7.3 RECEIVER OPERATING CHARACTERISTIC (ROC) CURVE ANALYSIS",
        "7.4 LEAVE-ONE-SENSOR-OUT ABLATION AND COMPLEMENTARITY",
        "7.5 CONFUSION MATRICES AND RISK SCORE DISTRIBUTIONS",
        "7.6 POLARITY INVERSION DIAGNOSTICS AND CROSS-DATASET TRANSFER",
        "8.1 LIVE THREE-TIER MITIGATION ON OPEN-DOMAIN TRIVIAQA",
        "8.2 SELECTIVE PREDICTION AND RISK-COVERAGE (AURC) ANALYSIS",
        "8.3 HARDWARE LATENCY PROFILING ON TESLA T4 GPU AND CPU",
        "8.4 LIMITATIONS AND THREATS TO VALIDITY",
        "9.1 CONCLUSION",
        "9.2 FUTURE WORK",
    ]
    for s in sec_prefixes:
        search_targets.append((s, s))

    fig_ids = ["7.1", "7.2", "7.3", "8.1", "8.2", "8.3"]
    for fid in fig_ids:
        search_targets.append((f"FIGURE {fid}", f"FIGURE {fid}:"))

    tab_ids = [
        "3.1", "3.1B", "3.2", "3.3", "3.4", "3.5", "3.6", "3.7", "3.8",
        "4.1B", "4.1", "4.2", "4.3",
        "5.1", "5.1B",
        "6.1",
        "7.1", "7.2", "7.1B", "7.2B", "7.3B", "7.3", "7.4B", "7.5B", "7.6B", "7.7B", "7.4", "7.8B",
        "8.1", "8.1B", "8.2", "8.2B", "8.3", "8.3B",
        "A1.1", "A2.1", "A3.1",
    ]
    for tid in tab_ids:
        search_targets.append((f"TABLE {tid}", f"TABLE {tid}:"))

    for idx in range(ch1_pdf_idx, total_pages):
        arabic_pg = str(idx - ch1_pdf_idx + 1)
        txt = " ".join(pdf[idx].get_text("text").split())
        for key, needle in search_targets:
            if key not in page_map and needle in txt:
                page_map[key] = arabic_pg

    arabic_total = total_pages - ch1_pdf_idx
    pdf.close()
    return page_map, total_pages, arabic_total


if __name__ == "__main__":
    import time
    ts = int(time.time())
    out_docx = ROOT / "FINAL_REPORT.docx"
    out_pdf = ROOT / "FINAL_REPORT.pdf"
    tmp_docx1 = FINAL_DIR / "results" / "_ref" / f"temp_build_{ts}_p1.docx"
    tmp_pdf1 = FINAL_DIR / "results" / "_ref" / f"temp_build_{ts}_p1.pdf"
    tmp_docx2 = FINAL_DIR / "results" / "_ref" / f"temp_build_{ts}_p2.docx"
    tmp_pdf2 = FINAL_DIR / "results" / "_ref" / f"temp_build_{ts}_p2.pdf"
    tmp_docx1.parent.mkdir(parents=True, exist_ok=True)

    print("Pass 1: Building initial FINAL_REPORT.docx and exporting PDF to measure exact page layout...")
    assemble_docx(tmp_docx1, {})
    export_docx_to_pdf_via_word(tmp_docx1, tmp_pdf1)

    page_map, total_pdf_pages, arabic_pages = extract_exact_page_map_from_pdf(tmp_pdf1)
    print(f"Pass 1 complete: Total PDF Pages = {total_pdf_pages} (Front Matter = {total_pdf_pages - arabic_pages}, Main Arabic Pages = {arabic_pages}).")

    print("Pass 2: Rebuilding FINAL_REPORT.docx with exact page numbers in CONTENTS, LIST OF FIGURES, and LIST OF TABLES...")
    assemble_docx(tmp_docx2, page_map)
    export_docx_to_pdf_via_word(tmp_docx2, tmp_pdf2)

    page_map2, total_pdf_pages2, arabic_pages2 = extract_exact_page_map_from_pdf(tmp_pdf2)
    print(f"Pass 2 complete: Total PDF Pages = {total_pdf_pages2} (Front Matter = {total_pdf_pages2 - arabic_pages2}, Main Arabic Pages = {arabic_pages2}).")

    for target_docx in [out_docx, CAPSTONE / "FINAL_REPORT.docx", ROOT / "FINAL_REPORT_NO_IMAGES.docx", ROOT / "FINAL_REPORT_OPTIMIZED.docx"]:
        try:
            shutil.copy2(tmp_docx2, target_docx)
            print(f"Saved: {target_docx}")
        except PermissionError:
            print(f"Note: {target_docx} is open in Word.")
    for target_pdf in [out_pdf, CAPSTONE / "FINAL_REPORT.pdf", ROOT / "FINAL_REPORT_NO_IMAGES.pdf", ROOT / "FINAL_REPORT_OPTIMIZED.pdf"]:
        try:
            shutil.copy2(tmp_pdf2, target_pdf)
            print(f"Saved: {target_pdf}")
        except PermissionError:
            print(f"Note: {target_pdf} is open in a PDF viewer.")
    print("Done exporting all DOCX and PDF targets.")
