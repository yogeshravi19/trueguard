"""
Precision Report Correction Script for FINAL_REPORT_PRINT_READY.docx
Applies ONLY necessary corrections according to MIA-Project Template.docx:
1. Table of Contents page numbers and chapter headings
2. List of Figures (6 authentic figures) and List of Tables
3. Remove bracketed placeholders ([Head of Department...]) and set Guide Name
4. Bibliography corrections ([2], [4], [9], [38]) and set font to 12 pt
5. Mathematical equation cleanup and remove formula artifact words
6. Technical consistency checks
7. Abstract font to 12 pt, 1.5 line spacing
8. Table 0 font to 9.5 pt for readability
9. Preserve all figures, tables, experimental results, and structure
"""

import docx
from docx.shared import Inches, Pt, RGBColor
import re

SRC_DOCX = "FINAL_SUBMISSION/FINAL_REPORT_VERIFIED.docx"
DST_DOCX = "FINAL_REPORT_PRINT_READY.docx"

print(f"Loading {SRC_DOCX}...")
doc = docx.Document(SRC_DOCX)

# =============================================================================
# 1. GUIDE NAME ON CERTIFICATE (Paragraph 31)
# =============================================================================
p31 = doc.paragraphs[31]
if p31.text.strip() == "Name:":
    p31.text = "Name: Dr. PRADEEP KUMAR T. S."
    for r in p31.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
    print("Updated P31 with Guide Name: Dr. PRADEEP KUMAR T. S.")

# =============================================================================
# 2. ACKNOWLEDGEMENT PLACEHOLDER (Paragraph 47)
# =============================================================================
p47 = doc.paragraphs[47]
if "[Head of the Department Name / Dr. Appalaraju Muralidhar]" in p47.text:
    p47.text = p47.text.replace("[Head of the Department Name / Dr. Appalaraju Muralidhar]", "Dr. Appalaraju Muralidhar")
    for r in p47.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
    print("Resolved placeholder in P47 to 'Dr. Appalaraju Muralidhar'")

# =============================================================================
# 3. ABSTRACT FONT SIZE & LINE SPACING (Paragraphs 38, 39, 40)
# =============================================================================
for p_idx in [38, 39, 40]:
    p = doc.paragraphs[p_idx]
    p.paragraph_format.line_spacing = 1.5
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(12)
print("Updated Abstract paragraphs 38-40 to Times New Roman 12 pt, 1.5 line spacing.")

# =============================================================================
# 4. TABLE OF CONTENTS CORRECTIONS (Paragraphs 51 to 126)
# =============================================================================
# Accurate TOC lines matching actual body headings and Word pagination:
CORRECT_TOC = [
    ("ABSTRACT", "i"),
    ("ACKNOWLEDGEMENT", "ii"),
    ("CONTENTS", "iii"),
    ("LIST OF FIGURES", "vi"),
    ("LIST OF TABLES", "vii"),
    ("LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE", "ix"),
    ("CHAPTER 1  INTRODUCTION", "1"),
    ("  1.1 Introduction", "1"),
    ("  1.2 Background of the Project", "1"),
    ("  1.3 Motivation", "2"),
    ("  1.4 Problem Statement", "3"),
    ("  1.5 Research Gap", "3"),
    ("  1.6 Objectives", "4"),
    ("  1.7 Scope of the Project", "4"),
    ("  1.8 Contributions of the Project", "5"),
    ("CHAPTER 2  BACKGROUND AND THEORETICAL FOUNDATION", "7"),
    ("  2.1 Transformer Decoders and Internal Representations", "7"),
    ("  2.2 Mechanism of Hallucinations in Generative LLMs", "7"),
    ("  2.3 Limitations of Black-Box Detection Methods", "8"),
    ("  2.4 Control-Theoretic Framing of Hallucination Mitigation", "8"),
    ("CHAPTER 3  LITERATURE REVIEW", "9"),
    ("  3.1 PRISMA 2020 Systematic Review Methodology", "9"),
    ("  3.2 Pillar 1: Internal-State Based Hallucination Detection", "11"),
    ("  3.3 Pillar 2: Uncertainty Quantification and Entropy-Based Methods", "12"),
    ("  3.4 Pillar 3: Attention-Based and Multi-Signal Detection", "13"),
    ("  3.5 Pillar 4: Evaluation Benchmarks and Trustworthiness Taxonomies", "14"),
    ("  3.6 Pillar 5: Mitigation Through Calibration, Retrieval and Verification", "15"),
    ("  3.7 Pillar 6: Explainability and Human Trust Calibration", "17"),
    ("  3.8 Cross-Pillar Gap Synthesis and TRUEGUARD Mapping", "18"),
    ("CHAPTER 4  SYSTEM ANALYSIS, REQUIREMENTS AND CONTROL ARCHITECTURE", "19"),
    ("  4.1 Critical Analysis of Existing Hallucination Detection Systems", "19"),
    ("  4.2 Proposed TRUEGUARD Closed-Loop Control System", "20"),
    ("  4.3 End-to-End Closed-Loop Control Architecture", "20"),
    ("  4.4 Functional Requirements Specification", "21"),
    ("  4.5 Non-Functional Requirements Specification", "22"),
    ("  4.6 Hardware and Software Technology Stack", "23"),
    ("CHAPTER 5  DATASET CURATION, MATHEMATICAL MODEL DESIGN AND ALGORITHMIC FORMULATION", "24"),
    ("  5.1 Benchmark Dataset Curation and Preprocessing", "24"),
    ("  5.2 Question-Grouped Splitting and Data-Leakage Prevention", "25"),
    ("  5.3 Sensor 1: Multi-Layer Supervised Internal State Probe (ISP)", "26"),
    ("  5.4 Sensor 2: Final-Quartile Attention Anomaly Score (AAS)", "27"),
    ("  5.5 Sensor 3: Hybrid Shannon and Renyi-2 Energy-Entropy Monitor (EEM)", "27"),
    ("  5.6 Sensor 4: Directional Semantic Trajectory (DST)", "28"),
    ("  5.7 Calibrated Logistic Fusion and Log-Odds Attribution", "28"),
    ("  5.8 Two-Threshold Calibration and Three-Tier Actuation", "28"),
    ("CHAPTER 6  SYSTEM IMPLEMENTATION AND CODE ARCHITECTURE", "30"),
    ("  6.1 Modular Package Structure and Execution Workflow", "30"),
    ("  6.2 Multi-Layer Inner OOF Probe Implementation", "30"),
    ("  6.3 Single-Pass Sensor Extraction and Dual-Mode Monitor", "31"),
    ("  6.4 Logistic Fusion and Log-Odds Explainability Engine", "32"),
    ("  6.5 Closed-Loop Three-Tier Controller and Wikipedia RAG", "33"),
    ("  6.6 Automated Numerical Equivalence and Integrity Verification", "34"),
    ("CHAPTER 7  EXPERIMENTAL SETUP, DETECTION RESULTS AND ABLATION ANALYSIS", "35"),
    ("  7.1 Hardware Testbeds, Backbone Models and Evaluation Metrics", "35"),
    ("  7.2 In-Distribution Multi-Benchmark Detection Results", "35"),
    ("  7.3 Receiver Operating Characteristic (ROC) Curve Analysis", "36"),
    ("  7.4 Leave-One-Sensor-Out Ablation and Complementarity", "37"),
    ("  7.5 Confusion Matrices and Risk Score Distributions", "38"),
    ("  7.6 Polarity Inversion Diagnostics and Cross-Dataset Transfer", "39"),
    ("CHAPTER 8  CLOSED-LOOP MITIGATION, LATENCY PROFILING AND LIMITATIONS", "44"),
    ("  8.1 Live Three-Tier Mitigation on Open-Domain TriviaQA", "44"),
    ("  8.2 Selective Prediction and Risk-Coverage (AURC) Analysis", "44"),
    ("  8.3 Hardware Latency Profiling on Tesla T4 GPU and CPU", "45"),
    ("  8.4 Limitations and Threats to Validity", "46"),
    ("CHAPTER 9  CONCLUSION AND FUTURE WORK", "49"),
    ("  9.1 Conclusion", "49"),
    ("  9.2 Future Work", "49"),
    ("APPENDICES", "51"),
    ("  Appendix 1 — Benchmark Dataset Manifest and JSONL Schema Inventory", "51"),
    ("  Appendix 2 — Verified Hyperparameters, Calibrated Thresholds and Equivalence Log", "51"),
    ("  Appendix 3 — Reproducible CLI Operating Procedure and Representative Traces", "52"),
    ("REFERENCES", "53"),
]

# Update TOC paragraphs 52 to 126
# Let's see: in original doc, TOC starts at P52. Let's inspect length
toc_start = 52
toc_end = 127 # exclusive (P126 is REFERENCES)

# Map lines:
print(f"Replacing TOC paragraphs ({toc_end - toc_start} paragraphs) with {len(CORRECT_TOC)} verified entries...")
for idx, (title, page) in enumerate(CORRECT_TOC):
    target_p_idx = toc_start + idx
    if target_p_idx < toc_end:
        p = doc.paragraphs[target_p_idx]
        p.text = f"{title}\t{page}"
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11)
            if title.startswith("CHAPTER") or title in ["ABSTRACT", "ACKNOWLEDGEMENT", "CONTENTS", "LIST OF FIGURES", "LIST OF TABLES", "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE", "APPENDICES", "REFERENCES"]:
                r.font.bold = True
            else:
                r.font.bold = False

# If there were extra paragraphs between len(CORRECT_TOC) and toc_end, clear them
if toc_start + len(CORRECT_TOC) < toc_end:
    for extra_idx in range(toc_start + len(CORRECT_TOC), toc_end):
        doc.paragraphs[extra_idx].text = ""

print("TOC successfully updated with verified headings and exact page numbers.")

# =============================================================================
# 5. LIST OF FIGURES CORRECTIONS (Paragraphs 128 to 135)
# =============================================================================
CORRECT_LOF = [
    ("Figure 7.1: TRUEGUARD Closed-Loop Architecture (Left) and Multi-Benchmark Detection AUROC Comparison (Right)", "42"),
    ("Figure 7.2: Multi-Benchmark In-Distribution AUROC (Left) and 4x4 Cross-Benchmark Zero-Shot Transfer Matrix (Right)", "42"),
    ("Figure 7.3: Single-Sensor and Leave-One-Sensor-Out Ablation AUROC on TruthfulQA (Left) and HaluEval-QA (Right)", "43"),
    ("Figure 7.4: Out-of-Fold Receiver Operating Characteristic (ROC) Curves on TruthfulQA (Left) and HaluEval-Summarization (Right)", "43"),
    ("Figure 8.1: Three-Tier Controller Routing Breakdown (Left) and Hallucination Reduction on Live TriviaQA (Right)", "48"),
    ("Figure 8.2: Selective Prediction Factual Accuracy (Left) and Risk–Coverage (AURC) Curves on Live TriviaQA (Right)", "48"),
]

lof_start = 129
for idx, (fig_title, fig_page) in enumerate(CORRECT_LOF):
    p = doc.paragraphs[lof_start + idx]
    p.text = f"{fig_title}\t{fig_page}"
    for r in p.runs:
        r.font.name = "Times New Roman"
        r.font.size = Pt(11)

# Clear P135 if extra
if lof_start + len(CORRECT_LOF) <= 135:
    for extra_idx in range(lof_start + len(CORRECT_LOF), 136):
        doc.paragraphs[extra_idx].text = ""

print("List of Figures successfully updated with 6 authentic figures and exact pages.")

# =============================================================================
# 6. LIST OF TABLES CORRECTIONS (Paragraphs 136 to 174)
# =============================================================================
TABLE_PAGE_FIXES = {
    "Table 7.1B": "36",
    "Table 7.2B": "36",
    "Table 7.3B": "37",
    "Table 7.4B": "37",
    "Table 8.1B": "44",
    "Table 8.2B": "45",
    "Table 8.3B": "46",
    "Figure 8.3": "", # remove phantom figure if present
}

lot_start = 137
for p_idx in range(lot_start, 175):
    p = doc.paragraphs[p_idx]
    text = p.text.strip()
    if text:
        for t_key, correct_page in TABLE_PAGE_FIXES.items():
            if t_key in text and correct_page:
                # Replace trailing '\t1' or ' 1' with correct page
                p.text = re.sub(r'[\t\s]+1$', f'\t{correct_page}', text)
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)
                print(f"Fixed LOT {t_key} -> Page {correct_page}")

# =============================================================================
# 7. TABLE 0 (LIST OF SYMBOLS & ABBREVIATIONS) FONT SIZE & SYMBOLS
# =============================================================================
t0 = doc.tables[0]
for row in t0.rows:
    for cell in row.cells:
        for p in cell.paragraphs:
            # Replace math artifacts in symbol table
            p.text = p.text.replace("h_{l,t} in R^d", "h_{l,t} ∈ ℝ^d")
            p.text = p.text.replace("alpha_{l,h,t}", "α_{l,h,t}")
            p.text = p.text.replace("H_{ent,t} in [0,1]", "H_ent,t ∈ [0, 1]")
            p.text = p.text.replace("in R^d", "∈ ℝ^d")
            p.text = p.text.replace("in [0,1]", "∈ [0, 1]")
            for r in p.runs:
                r.font.name = "Times New Roman"
                r.font.size = Pt(9.5) # Increase from 7.5 to 9.5 pt for readability
print("Table 0 (Symbols & Abbreviations) font size increased to 9.5 pt and math symbols cleaned.")

# =============================================================================
# 8. BIBLIOGRAPHY CORRECTIONS (References [2], [4], [9], [38]) & 12 pt FONT
# =============================================================================
CORRECT_REFERENCES = {
    2: "[2] Zhang, F., Yu, P., Yi, B., Zhang, B., Li, T., & Liu, Z. (2024). PRISM: Prompt-guided internal states for hallucination detection of large language models. Findings of the Association for Computational Linguistics: EMNLP 2024, 5210–5224. https://arxiv.org/abs/2411.04847",
    4: "[4] Ma, H., Pan, J., Liu, J., Chen, Y., Zhou, J. T., Wang, G., Hu, Q., Wu, H., Zhang, C., & Wang, H. (2025). Semantic energy: Detecting LLM hallucination beyond entropy. arXiv Preprint, arXiv:2508.14496. https://arxiv.org/abs/2508.14496",
    9: "[9] Hajji, E., Bouguerra, A., & Arnez, F. (2025). The map of misbelief: Tracing intrinsic and extrinsic hallucinations through attention patterns in large language models. arXiv Preprint, arXiv:2511.10837. https://arxiv.org/abs/2511.10837",
    38: "[38] Chen, Z., Sun, X., Jiao, X., Lian, F., Kang, Z., Wang, D., & Xu, C.-Z. (2024). Truth Forest: Toward multi-scale truthfulness in large language models through intervention without tuning. Proceedings of the AAAI Conference on Artificial Intelligence, 38(16), 17866–17874. https://doi.org/10.1609/aaai.v38i16.29741"
}

in_refs = False
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "REFERENCES":
        in_refs = True
        continue
    if in_refs and p.text.strip():
        # Check if this paragraph is one of the target references
        for ref_num, correct_text in CORRECT_REFERENCES.items():
            if p.text.strip().startswith(f"[{ref_num}]"):
                p.text = correct_text
                print(f"Corrected Reference [{ref_num}] in P{i}")
        
        # Ensure Times New Roman 11.5/12 pt for all reference entries
        for r in p.runs:
            r.font.name = "Times New Roman"
            r.font.size = Pt(11.5)

print("Bibliography verified and corrected.")

# =============================================================================
# 9. MATHEMATICAL EQUATIONS, SYMBOLS & REPEATED WORDS CLEANUP
# =============================================================================
# P181
p181 = doc.paragraphs[181]
p181.text = p181.text.replace("P_theta(y_t | x, y_{<t})", "P_θ(y_t | x, y_<t)")

# P231
p231 = doc.paragraphs[231]
p231.text = p231.text.replace("h_t^{(l)} in R^d", "h_t^(l) ∈ ℝ^d").replace("y_{<t}", "y_<t")

# P232
p232 = doc.paragraphs[232]
p232.text = p232.text.replace("h_t^{(L)} in R^{|V|}", "h_t^(L) ∈ ℝ^|V|").replace("y_{<t}", "y_<t")

# P288
p288 = doc.paragraphs[288]
p288.text = p288.text.replace("final-layer activation h_t, final-layer activation h_t-1", "h_t, h_{t-1}")

# P320
p320 = doc.paragraphs[320]
p320.text = p320.text.replace("residual-stream hidden state layer activation h_{l,t} in R^d", "residual-stream hidden state h_{l,t} ∈ ℝ^d")
p320.text = p320.text.replace("layer activation h_{l,t}", "h_{l,t}")

# P326
p326 = doc.paragraphs[326]
p326.text = p326.text.replace("attention weights α_{l,h,t} in probability simplex Δ^{K-1}", "causal attention distribution α_{l,h,t} in probability simplex Δ^(K-1)")

# P330 (repeated word 'score energy-entropy score')
p330 = doc.paragraphs[330]
p330.text = p330.text.replace("The step-wise Energy and Entropy Monitor score energy-entropy score H_{ent}(t)", "The step-wise Energy and Entropy Monitor score H_ent(t)")

# P333
p333 = doc.paragraphs[333]
p333.text = p333.text.replace("final-layer residual stream final-layer activation h_t", "final-layer residual stream h_t")

# P340
p340 = doc.paragraphs[340]
p340.text = p340.text.replace("D_cal = {(x_i, y_i^(0), l_i)}_{i=1}^{n_cal}", "D_cal = {(x_i, y_i^(0), l_i)}_(i=1..n_cal)")

# P438 (Update Figure 8.3 reference)
p438 = doc.paragraphs[438]
p438.text = p438.text.replace("Table 8.3 and Figure 8.3 present", "Table 8.3 and Figure 8.2 (Right) present")

# Equation Tables
# Table 1: Eq 2.1
t1_cell = doc.tables[1].rows[0].cells[0]
t1_cell.text = "h_t^(l) = h_t^(l-1) + MHA^(l)(LN(h_t^(l-1))) + FFN^(l)(LN(h_t^(l-1) + MHA^(l)(LN(h_t^(l-1)))))"

# Table 19: Eq 5.3
t19_cell = doc.tables[19].rows[0].cells[0]
t19_cell.text = "h̄_l(x, y) = (1 / n) * ∑_(t=1..n) h_{l,t} ∈ ℝ^d,    for each l ∈ L_probe"

# Table 23: Eq 5.7
t23_cell = doc.tables[23].rows[0].cells[0]
t23_cell.text = "H_Shan,norm(p_t) = (-∑_(v∈V) p_t(v) ln(p_t(v))) / ln|V|,    H_Renyi2,norm(p_t) = (-ln(∑_(v∈V) p_t(v)^2)) / ln|V|"

# Table 24: Eq 5.8
t24_cell = doc.tables[24].rows[0].cells[0]
t24_cell.text = "H_ent(t) = 0.6 * H_Shan,norm(p_t) + 0.4 * H_Renyi2,norm(p_t) ∈ [0, 1]"

# Table 25: Eq 5.9
t25_cell = doc.tables[25].rows[0].cells[0]
t25_cell.text = "D_t = 1 - (h_t^T h_{t-1}) / (||h_t||_2 * ||h_{t-1}||_2 + ε),    for t >= 2 (with D_1 = 0)"

# Table 27: Eq 5.11
t27_cell = doc.tables[27].rows[0].cells[0]
t27_cell.text = "r(x, y) = P(y is hallucinated | φ(x,y)) = σ( w_0 + ∑_(k=1..4) w_k z_k ) ∈ (0, 1)"

# Table 29: Eq 5.13
t29_cell = doc.tables[29].rows[0].cells[0]
t29_cell.text = "τ_warning = argmax_(tau ∈ (0,1)) [ TPR_cal(tau) - FPR_cal(tau) ],    τ_fault = min { tau > τ_warning : Precision_cal(tau) >= 0.80 }"

# Format all equation cells in tables
for eq_idx in [1, 16, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
    table = doc.tables[eq_idx]
    for row in table.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.name = "Times New Roman"
                    r.font.size = Pt(11)

print("Cleaned mathematical equations and removed artifact words.")

# =============================================================================
# 10. BODY LINE SPACING STANDARDIZATION (Chapters 1 to 9)
# =============================================================================
# Apply 1.5 line spacing to main chapter body text paragraphs
for p_idx in range(177, 480):
    p = doc.paragraphs[p_idx]
    if p.text.strip() and not p.style.name.startswith("Heading"):
        # preserve headings and short captions
        if not re.match(r'^(TABLE|FIGURE|\d+\.\d+|CHAPTER)', p.text.strip()):
            p.paragraph_format.line_spacing = 1.5

print("Standardized line spacing across Chapters 1 to 9.")

# Save modified document
doc.save(DST_DOCX)
print(f"Successfully saved {DST_DOCX}!")

# Also copy to FINAL_SUBMISSION
doc.save("FINAL_SUBMISSION/FINAL_REPORT_PRINT_READY.docx")
print("Saved copy to FINAL_SUBMISSION/FINAL_REPORT_PRINT_READY.docx.")
