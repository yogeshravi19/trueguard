"""
Final Report Polish Script:
1. Fix two-page abstract -> fits strictly on Page i with 100% technical fidelity.
2. Update preliminary Contents page numbers -> accurate Roman numerals (i, ii, iii, vi, vii, ix).
3. Improve split abbreviations table -> clean Part A (Acronyms) and Part B (Mathematical Notation) with repeated headers, cantSplit, and professional typography.
4. Correct remaining typos and verified mathematical notation errors in body and tables.
5. Preserve all chapters, research results, figures, tables, and existing formatting.
"""
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import re

SRC_DOCX = Path("FINAL_REPORT_PRINT_READY.docx")
BACKUP_DOCX = Path("FINAL_REPORT_PRINT_READY_PRE_POLISH_BACKUP.docx")

# Make backup first
import shutil
shutil.copy2(SRC_DOCX, BACKUP_DOCX)
print(f"Created backup: {BACKUP_DOCX}")

doc = docx.Document(SRC_DOCX)

def set_run_font(run, name="Times New Roman", size_pt=11.5, bold=False, italic=False, color=None):
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = color

def set_para_format(p, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=0, space_after=4):
    p.alignment = align
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)

# =============================================================================
# 1. FIX THE TWO-PAGE ABSTRACT -> STRICTLY 1 PAGE (PAGE i)
# =============================================================================
print("\n--- 1. Fixing Abstract ---")
p37 = doc.paragraphs[37] # ABSTRACT heading
p37.text = "ABSTRACT"
set_para_format(p37, align=WD_ALIGN_PARAGRAPH.CENTER, line_spacing=1.15, space_before=6, space_after=10)
for r in p37.runs:
    set_run_font(r, name="Times New Roman", size_pt=14, bold=True)

p38 = doc.paragraphs[38] # Background & Problem
p38.text = (
    "Large Language Models (LLMs) routinely produce fluent, high-confidence statements that are factually "
    "incorrect or unfaithful to context—a critical failure mode termed hallucination. Existing mitigation paradigms "
    "face a severe latency–accuracy trade-off: black-box multi-sample consistency methods (such as SelfCheckGPT and "
    "semantic entropy) require generating 5 to 20 auxiliary completions per prompt, inflating decoding latency by 5x "
    "to 20x. Conversely, single-pass surface heuristics (token entropy, negative log-likelihood, and logit energy) fail "
    "when models state memorized human misconceptions with high confidence or invert polarity under benchmark "
    "answer-length asymmetries."
)
set_para_format(p38, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=0, space_after=4)
for r in p38.runs:
    set_run_font(r, name="Times New Roman", size_pt=11.0)

p39 = doc.paragraphs[39] # Architecture & 4 Sensors
p39.text = (
    "Grounded in a PRISMA 2020 systematic literature review of 40 peer-reviewed studies (2020–2025) organized across "
    "Six Research Pillars, this project presents TRUEGUARD, a unified closed-loop feedback control framework for "
    "single-pass white-box hallucination detection, log-odds explainability, and graded three-tier runtime mitigation. "
    "During a single forward pass of a frozen autoregressive Transformer, TRUEGUARD extracts four complementary "
    "internal signals: (1) an Internal State Probe (ISP) averaging L2-regularized logistic probes across four fractional "
    "residual-stream depths {0.45, 0.60, 0.75, 0.90}L trained via leakage-free inner grouped out-of-fold (OOF) stacking; "
    "(2) a top-quartile Attention Anomaly Score (AAS) measuring normalized causal attention Shannon entropy; "
    "(3) a scale-invariant Energy and Entropy Monitor (EEM) combining normalized Shannon entropy (0.6) and quadratic "
    "Renyi-2 entropy (0.4); and (4) a Directional Semantic Trajectory (DST) sensor tracking consecutive-token hidden-state cosine drift."
)
set_para_format(p39, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=0, space_after=4)
for r in p39.runs:
    set_run_font(r, name="Times New Roman", size_pt=11.0)

p40 = doc.paragraphs[40] # Results & Mitigation (Typo fixed!)
p40.text = (
    "Evaluated on an NVIDIA Tesla T4 GPU with TinyLlama-1.1B-Chat-v1.0 across 3,196 real responses spanning four "
    "standard benchmarks (5-fold question-grouped cross-validation) and verified on local CPU with GPT-2 (124M), "
    "TRUEGUARD achieves a macro-average AUROC of 0.935 (0.986 on HaluEval-Summarization, 0.975 on HaluEval-QA, "
    "0.903 on HaluEval-Dialogue, and 0.876 on TruthfulQA), macro F1 of 0.882, and Expected Calibration Error of 0.031, "
    "outperforming single-pass entropy baselines by +30.6 AUROC points. Graded three-tier runtime mitigation "
    "(Tier 1 annealed re-sampling, Tier 2 Wikipedia retrieval grounding, and Tier 3 calibrated abstention) reduces "
    "the hallucination rate among answered queries by 35.5% relative (62.0% -> 40.0%, raising accuracy from 38.0% to 60.0%) "
    "and cuts system-wide emitted hallucinations by 72.0% relative (62.0% -> 17.3%) with an AURC of 0.412, while adding "
    "only +2.91 ms/token (+8.7% overhead; 4.65x faster than 5-sample consistency)."
)
set_para_format(p40, align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=0, space_after=6)
for r in p40.runs:
    set_run_font(r, name="Times New Roman", size_pt=11.0)

p41 = doc.paragraphs[41] # Keywords
p41.text = (
    "Keywords: Large Language Models, Hallucination Detection, Internal State Probing, Attention Entropy, "
    "Renyi Entropy, Closed-Loop Feedback Control, Selective Prediction, Retrieval-Augmented Generation, Explainable AI."
)
set_para_format(p41, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.15, space_before=2, space_after=0)
for r in p41.runs:
    set_run_font(r, name="Times New Roman", size_pt=10.5, italic=True)

print("Abstract updated with verified content and 11 pt font for 1-page fit.")

# =============================================================================
# 2. ACKNOWLEDGEMENT FORMATTING -> STRICTLY 1 PAGE (PAGE ii)
# =============================================================================
print("\n--- 2. Checking Acknowledgement Formatting ---")
for p_idx in range(44, 48):
    set_para_format(doc.paragraphs[p_idx], align=WD_ALIGN_PARAGRAPH.JUSTIFY, line_spacing=1.15, space_before=0, space_after=4)
    for r in doc.paragraphs[p_idx].runs:
        set_run_font(r, name="Times New Roman", size_pt=11.5)
print("Acknowledgement paragraphs formatted with 1.15 line spacing.")

# =============================================================================
# 3. UPDATE PRELIMINARY CONTENTS PAGE NUMBERS
# =============================================================================
print("\n--- 3. Updating Preliminary Contents Page Numbers ---")
toc_front_matter_mapping = {
    "ABSTRACT": "i",
    "ACKNOWLEDGEMENT": "ii",
    "CONTENTS": "iii",
    "LIST OF FIGURES": "vi",
    "LIST OF TABLES": "vii",
    "LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE": "ix",
}

for i in range(51, 60):
    p = doc.paragraphs[i]
    t = p.text.strip()
    for key, target_pg in toc_front_matter_mapping.items():
        if t.startswith(key):
            p.text = f"{key}\t{target_pg}"
            set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.15, space_before=0, space_after=2)
            for r in p.runs:
                set_run_font(r, name="Times New Roman", size_pt=12.0, bold=True)
            print(f"  Updated TOC: {p.text}")
            break

# =============================================================================
# 4. IMPROVE SPLIT ABBREVIATIONS TABLE (Table 0)
# =============================================================================
print("\n--- 4. Improving Split Abbreviations Table (Table 0) ---")
t0 = doc.tables[0]

# Add XML helper functions for cantSplit and tblHeader
def set_cell_margins(cell, top=30, bottom=30, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_row_cant_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def set_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

# Clean and enhance definitions in Table 0
enhanced_abbrevs = {
    # Acronyms (Rows 1 to 26)
    "AAS": ("AAS", "Attention Anomaly Score (normalized final-quartile causal attention Shannon entropy)"),
    "AUPRC": ("AUPRC", "Area Under the Precision–Recall Curve"),
    "AURC": ("AURC", "Area Under the Risk–Coverage Curve (selective prediction empirical risk metric)"),
    "AUROC": ("AUROC", "Area Under the Receiver Operating Characteristic Curve"),
    "CI": ("CI", "Confidence Interval (500-draw question-grouped bootstrap 95% confidence bounds)"),
    "CoT": ("CoT", "Chain-of-Thought Prompting"),
    "CoVe": ("CoVe", "Chain-of-Verification Multi-Step Hallucination Mitigation"),
    "CV": ("CV", "Cross-Validation (Leakage-free Question-Grouped K-Fold evaluation)"),
    "DST": ("DST", "Directional Semantic Trajectory (consecutive-token hidden-state cosine drift)"),
    "ECE": ("ECE", "Expected Calibration Error (10-bin reliability diagram calibration metric)"),
    "EEM": ("EEM", "Energy and Entropy Monitor (hybrid 0.6 normalized Shannon + 0.4 Renyi-2 logit entropy)"),
    "EM": ("EM", "Exact Match (normalized factual string equivalence metric)"),
    "FPR": ("FPR", "False Positive Rate (Type I error rate: 1 - Specificity)"),
    "ISP": ("ISP", "Internal State Probe (4-layer supervised L2 logistic residual-stream probes)"),
    "ITI": ("ITI", "Inference-Time Intervention"),
    "KV Cache": ("KV Cache", "Key–Value Attention Cache for O(1) per-step autoregressive generation"),
    "LLM": ("LLM", "Large Language Model"),
    "NLI": ("NLI", "Natural Language Inference"),
    "NLL": ("NLL", "Negative Log-Likelihood (sequence-averaged cross-entropy loss)"),
    "OOF": ("OOF", "Out-of-Fold (inner grouped K-fold predictions used for leakage-free probe stacking)"),
    "PRISMA": ("PRISMA", "Preferred Reporting Items for Systematic Reviews and Meta-Analyses 2020"),
    "RAG": ("RAG", "Retrieval-Augmented Generation"),
    "SAPLMA": ("SAPLMA", "Statement Accuracy Prediction based on Language Model Activations"),
    "TPR": ("TPR", "True Positive Rate (Sensitivity / Hallucination Recall)"),
    "UQ": ("UQ", "Uncertainty Quantification"),
    "XAI": ("XAI", "Explainable Artificial Intelligence"),

    # Mathematical Symbols & Nomenclature (Rows 27 to 39)
    "x": ("x = (x_1, ..., x_m)", "Input prompt token sequence of length m"),
    "y": ("y = (y_1, ..., y_n)", "Generated response token sequence of length n"),
    "h": ("h_{l,t} ∈ ℝ^d", "Residual-stream hidden state vector at layer l and token step t"),
    "alpha": ("α_{l,h,t} ∈ Δ^(K_t-1)", "Causal self-attention weight distribution for head h at layer l and step t"),
    "F_t": ("F_t ∈ [0, 1]", "Token-level Internal State Probe (ISP) hallucination probability"),
    "A_t": ("A_t ∈ [0, 1]", "Token-level Attention Anomaly Score (AAS) normalized Shannon entropy"),
    "H_ent": ("H_ent,t ∈ [0, 1]", "Token-level Energy and Entropy Monitor (EEM) hybrid entropy score"),
    "D_t": ("D_t ∈ [0, 2]", "Token-level Directional Semantic Trajectory (DST) consecutive cosine drift"),
    "phi": ("φ(x, y) ∈ ℝ^4", "Sequence-pooled 4-sensor feature vector [F̄, Ā, H̄_ent, D̄]^T"),
    "r(x,y)": ("r(x, y) ∈ [0, 1]", "Calibrated sequence-level hallucination risk probability output by TRUEGUARD"),
    "c_k": ("c_k = w_k · z_k", "Signed log-odds attribution of sensor k to the fused hallucination risk"),
    "tau_w": ("τ_warning", "Lower calibrated threshold (0.611) separating SAFE from Tier 1 Re-Sampling"),
    "tau_f": ("τ_fault", "Upper calibrated threshold (0.898) separating Tier 1 from Tier 2 RAG / Tier 3 Abstain"),
}

# Style Header Row
hdr_row = t0.rows[0]
set_table_header(hdr_row)
set_row_cant_split(hdr_row)
hdr_row.cells[0].text = "Acronym / Mathematical Symbol"
hdr_row.cells[1].text = "Full Expansion and Technical Definition"
for c in hdr_row.cells:
    set_cell_margins(c, top=40, bottom=40, left=80, right=80)
    for p in c.paragraphs:
        set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.05, space_before=2, space_after=2)
        for r in p.runs:
            set_run_font(r, name="Times New Roman", size_pt=9.5, bold=True)

# Format all rows in Table 0
for r_idx in range(1, len(t0.rows)):
    row = t0.rows[r_idx]
    set_row_cant_split(row)
    sym_text = row.cells[0].text.strip()
    
    # Check for math symbols to enhance notation
    if "h_{" in sym_text or "h_" in sym_text:
        row.cells[0].text = "h_{l,t} ∈ ℝ^d"
    elif "α" in sym_text or "alpha" in sym_text:
        row.cells[0].text = "α_{l,h,t} ∈ Δ^(K_t-1)"
    elif "phi" in sym_text or "φ" in sym_text:
        row.cells[0].text = "φ(x, y) ∈ ℝ^4"
    elif "tau_warning" in sym_text or "τ_warning" in sym_text:
        row.cells[0].text = "τ_warning"
    elif "tau_fault" in sym_text or "τ_fault" in sym_text:
        row.cells[0].text = "τ_fault"
    elif "c_k" in sym_text:
        row.cells[0].text = "c_k = w_k · z_k"
    elif "D_t" in sym_text:
        row.cells[0].text = "D_t ∈ [0, 2]"
    elif "H_ent" in sym_text:
        row.cells[0].text = "H_ent,t ∈ [0, 1]"
    elif "x =" in sym_text:
        row.cells[0].text = "x = (x_1, ..., x_m)"
    elif "y =" in sym_text:
        row.cells[0].text = "y = (y_1, ..., y_n)"
    elif "r(x,y)" in sym_text:
        row.cells[0].text = "r(x, y) ∈ [0, 1]"

    # Set cell padding and font
    row.cells[0].width = Inches(1.8)
    row.cells[1].width = Inches(4.2)
    for c_idx, cell in enumerate(row.cells):
        set_cell_margins(cell, top=25, bottom=25, left=60, right=60)
        for p in cell.paragraphs:
            set_para_format(p, align=WD_ALIGN_PARAGRAPH.LEFT, line_spacing=1.05, space_before=1, space_after=1)
            for r in p.runs:
                set_run_font(r, name="Times New Roman", size_pt=9.0, bold=(c_idx == 0))

print(f"Table 0 formatted with cantSplit, tblHeader, 1.8 in/4.2 in columns, and verified math notation.")

# =============================================================================
# 5. BODY TEXT TYPOS AND MATHEMATICAL NOTATION ERRORS
# =============================================================================
print("\n--- 5. Correcting Body Text & Equation Notation Errors ---")

# P232: fix h_t^{(l)}
p232 = doc.paragraphs[232]
if "h_t^{(l)}" in p232.text or "h_t^(L)" in p232.text:
    p232.text = (
        "At layer L, final hidden states are projected via lm_head onto vocabulary logits z_t = W_u h_t^(L) ∈ ℝ^|V|, "
        "yielding next-token probabilities P(y_t | x, y_<t) = softmax(z_t). Crucially, middle-to-late residual representations "
        "h_t^(l) (fractional depths 0.45L to 0.90L) linearize semantic factual associations before final vocabulary selection, "
        "providing a direct observation window into model truthfulness [27, 28]."
    )
    set_para_format(p232, line_spacing=1.5, space_after=6)
    for r in p232.runs:
        set_run_font(r, name="Times New Roman", size_pt=12.0)
    print("Fixed P232 mathematical notation.")

# P286: fix unbalanced bracket in Sensor 2
p286 = doc.paragraphs[286]
if "L_top = [floor(3L/4), L)" in p286.text:
    p286.text = p286.text.replace("L_top = [floor(3L/4), L)", "L_top = {floor(3L/4), ..., L - 1}")
    set_para_format(p286, line_spacing=1.5, space_after=4)
    for r in p286.runs:
        set_run_font(r, name="Times New Roman", size_pt=12.0)
    print("Fixed P286 bracket notation.")

# P288: fix h_{t-1} raw LaTeX
p288 = doc.paragraphs[288]
if "h_{t-1}" in p288.text:
    p288.text = p288.text.replace("h_{t-1}", "h_(t-1)")
    set_para_format(p288, line_spacing=1.5, space_after=4)
    for r in p288.runs:
        set_run_font(r, name="Times New Roman", size_pt=12.0)
    print("Fixed P288 raw LaTeX string.")

# P320: fix M_theta, h_{l,t} in R^d, Lambda
p320 = doc.paragraphs[320]
if "M_theta" in p320.text or "in R^d" in p320.text:
    p320.text = (
        "Let M_θ be a frozen causal Transformer with L layers. Given prompt tokens x = (x_1, ..., x_m) and generated "
        "answer tokens y = (y_1, ..., y_n), let h_{l,t} ∈ ℝ^d denote the residual-stream hidden state at layer l and "
        "generated token step t in {1, ..., n}. Rather than probing only the final layer, TRUEGUARD attaches four "
        "supervised L2-regularized logistic probes at fractional network depths Λ = {0.45, 0.60, 0.75, 0.90}L:"
    )
    set_para_format(p320, line_spacing=1.5, space_after=6)
    for r in p320.runs:
        set_run_font(r, name="Times New Roman", size_pt=12.0)
    print("Fixed P320 mathematical variables (M_θ, ℝ^d, Λ).")

# P326: fix α_{l,h,t} and Δ^(K-1)
p326 = doc.paragraphs[326]
if "α_{l,h,t}" in p326.text or "Δ^(K-1)" in p326.text:
    p326.text = (
        "Let L_top = {floor(3L/4), ..., L - 1} denote the final quartile of transformer layers (layers 16..21 on TinyLlama-1.1B; "
        "layers 9..11 on GPT-2), and let causal attention distribution α_{l,h,t} ∈ Δ^(K_t - 1) denote the causal attention "
        "distribution of head h in {1, ..., H} at generated step t over the K_t = m + t available context tokens. "
        "The step-wise Attention Anomaly Score A_t measures the normalized Shannon entropy averaged across all heads in L_top:"
    )
    set_para_format(p326, line_spacing=1.5, space_after=6)
    for r in p326.runs:
        set_run_font(r, name="Times New Roman", size_pt=12.0)
    print("Fixed P326 attention simplex notation.")

# =============================================================================
# 6. TABLE TYPOS AND MATHEMATICAL ARTIFACTS
# =============================================================================
print("\n--- 6. Correcting Table Typos and Artifacts ---")

# Table 10 R5C3
t10 = doc.tables[10]
for row in t10.rows:
    for cell in row.cells:
        if "tau_warn=0.611" in cell.text:
            cell.text = cell.text.replace("tau_warn=0.611", "τ_warn = 0.611").replace("tau_fault=0.898", "τ_fault = 0.898")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=9.5)
            print("Fixed Table 10 threshold notation.")

# Table 11
t11 = doc.tables[11]
for row in t11.rows:
    for cell in row.cells:
        t = cell.text
        if "alpha_{l,h,t}" in t or "tau_warning" in t or "phi(x,y)" in t or "mu_k, sigma_k" in t:
            t_new = t.replace("alpha_{l,h,t}", "α_{l,h,t}").replace("phi(x,y)", "φ(x, y)")
            t_new = t_new.replace("tau_warning", "τ_warning").replace("tau_fault", "τ_fault")
            t_new = t_new.replace("mu_k, sigma_k", "μ_k, σ_k").replace("y_{<t}", "y_<t")
            cell.text = t_new
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=9.5)
print("Fixed Table 11 system block parameters.")

# Table 12: remove "layer activation" artifact and clean notation
t12 = doc.tables[12]
for row in t12.rows:
    for cell in row.cells:
        t = cell.text
        if "layer activation h_{l,t}" in t:
            cell.text = t.replace("layer activation h_{l,t}", "hidden states h_{l,t}")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=9.5)
            print("Removed 'layer activation' artifact in Table 12 R1C2.")
        elif "alpha_{l,h,t}" in t or "phi(x,y)" in t or "tau_warning" in t:
            cell.text = t.replace("alpha_{l,h,t}", "α_{l,h,t}").replace("phi(x,y)", "φ(x, y)").replace("tau_warning", "τ_warning").replace("tau_fault", "τ_fault")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=9.5)
print("Fixed Table 12 functional requirements notation.")

# Table 26: Equation 5.10
t26 = doc.tables[26]
for row in t26.rows:
    for cell in row.cells:
        if "∈ R^4" in cell.text:
            cell.text = cell.text.replace("∈ R^4", "∈ ℝ⁴")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=10.0, bold=True)
            print("Fixed Table 26 vector space notation.")

# Table 28: Equation 5.12
t28 = doc.tables[28]
for row in t28.rows:
    for cell in row.cells:
        if "phi_k(x, y)" in cell.text:
            cell.text = cell.text.replace("phi_k(x, y)", "φ_k(x, y)")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=10.0, bold=True)
            print("Fixed Table 28 attribution notation.")

# Table 29: Equation 5.13
t29 = doc.tables[29]
for row in t29.rows:
    for cell in row.cells:
        if "argmax_(tau" in cell.text:
            cell.text = cell.text.replace("argmax_(tau", "arg max_(τ")
            for p in cell.paragraphs:
                for r in p.runs:
                    set_run_font(r, name="Times New Roman", size_pt=10.0, bold=True)
            print("Fixed Table 29 argmax notation.")

# Save modified DOCX
doc.save(str(SRC_DOCX))
print(f"\nSuccessfully saved polished docx to: {SRC_DOCX}")

# Copy to FINAL_SUBMISSION folder as well
dst_sub = Path("FINAL_SUBMISSION/FINAL_REPORT_PRINT_READY.docx")
shutil.copy2(SRC_DOCX, dst_sub)
print(f"Copied to: {dst_sub}")

