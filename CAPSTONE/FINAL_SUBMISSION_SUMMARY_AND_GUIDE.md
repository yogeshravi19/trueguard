# FINAL SUBMISSION GUIDE & COMPLETE ARCHIVE
## Systems Science & Control Engineering (Taylor & Francis)
**Manuscript No.:** Ms. No. 269790004  
**Title:** Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies  
**Authors:** Yogesh Ravi M, Dr. Pradeep Kumar T S  
**Editorial Office Contact:** Dr. Ajith Kumar BS  
**Submission Portal URL:** https://rp.tandfonline.com/dashboard/

---

## ⚡ URGENT: Technical Checks Action Guide (Dr. Ajith Kumar BS)

When you click **'Resume'** on the Author Submission Portal (https://rp.tandfonline.com/dashboard/), follow these exact 3 steps:

### Action 1: Upload the Rebuttal Document (Addressing Point 1)
* **What happened:** The portal required a separate file designated as **"Response to Reviewers"**.
* **What to upload:** Upload `E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx`.
* **File Designation on Portal:** Select **"Response to Reviewers"** (or **"Rebuttal / Author Response"**).

### Action 2: Update Portal Abstract Metadata (Addressing Point 2)
* **What happened:** The portal's metadata form still contained the old draft abstract from your first submission.
* **What to do:** In the portal step for **"Manuscript Details" / "Abstract"**, delete the old text and paste the exact text below:

> **COPY & PASTE THIS EXACT ABSTRACT INTO THE PORTAL:**
> 
> Large language models can write clear and convincing text, but they often state false things while sounding completely sure of themselves. This problem is called hallucination. In critical areas like healthcare, law, and finance, these mistakes can cause serious real world harm. Researchers have tried to tackle this in different ways like looking inside the model, measuring uncertainty and entropy, tracking attention patterns, pulling in facts from outside sources, and fine-tuning the model. However, most of these methods rely on isolated signals and are built separately. Because of this, current systems have a major gap: they might spot an error, but they fail to connect finding the mistake with fixing it and explaining it clearly to the user. In this paper, we conduct a systematic review of 40 research studies in accordance with PRISMA guidelines. We organize the existing literature into a six-pillar taxonomy and compare practical trade-offs, including computational requirements, additional latency, and constraints across both white-box and black-box (API-based) models. Based on this analysis, we identify five major research gaps. To address these limitations, we propose TRUEGUARD, a conceptual framework grounded in closed-loop control principles. TRUEGUARD combines multiple hallucination-detection signals, applies tiered closed-loop corrections when errors are detected, and provides understandable explanations to help users calibrate their trust in the model's output.

### Action 3: Resubmit the Updated Manuscripts (Addressing Point 3)
* **What happened:** Some figures and tables were previously not referenced in the body prose or had numbering mismatches.
* **Fix applied:** Both `.docx` files have been updated. Every single Figure (Figures 1–12) and Table (Tables 1–4) now has a verified, explicit in-text reference in the prose and matching captions.
* **Files to upload:**
  * **Main Document (Clean):** `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx`
  * **Marked Manuscript (Highlighted Changes):** `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx`

---

## 1. Verified Complete File Archive (`E:	rueguard\CAPSTONE\`)

| Portal File Role | Exact File Path | Verified Status & Contents |
| :--- | :--- | :--- |
| **Response to Reviewers** | `E:\trueguard\CAPSTONE\Response_to_Reviewers_269790004.docx` | **UPDATED & VERIFIED.** Includes Part A (Editorial Technical Checks 1–3) and Part B (Reviewer 1 Comments 1–4 & Reviewer 2 Points 1–7). |
| **Marked Manuscript** | `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models.docx` | **UPDATED & VERIFIED.** 10,078 words, all 12 figures and 4 tables referenced in text, yellow-highlighted modifications. |
| **Clean Manuscript** | `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_nocolour.docx` | **UPDATED & VERIFIED.** 10,078 words, clean publication-ready typography without highlights. |
| **Figure / Supplementary** | `E:\trueguard\figures\prisma_diagram.tif` (or `.png`) | **VERIFIED.** PRISMA 2020 compliant, 300 DPI high resolution. |

---

## 2. Full In-Text Callout Verification Matrix (All 16 Assets Referenced)

| Asset | Caption Title | In-Text Reference Location in Body Text |
| :--- | :--- | :--- |
| **Figure 1** | Semantic Entropy vs. Attention Intrinsic/Extrinsic | Section I (Introduction, paragraph on hallucination manifestations) |
| **Figure 2** | PRISMA Flow Diagram (688 → 40 studies) | Section II (Methodology, Subsection 2.3 Included Studies) |
| **Figure 3** | SEP vs. Semantic Entropy Accuracy and Cost | Section III (Pillar 2, paragraph on uncertainty quantification) |
| **Figure 4** | LLM-Check Black-Box 450x Speedup | Section III (Pillar 3, paragraph on attention-based detection) |
| **Figure 5** | TrustLLM Multi-Dimensional Benchmark Results | Section III (Pillar 4, paragraph on benchmarking) |
| **Figure 6** | Calibration & Explainability Percentage Gains | Section III (Pillar 4, paragraph on benchmarking improvements) |
| **Figure 7** | ExpandR Joint LLM-Retriever Optimization | Section III (Pillar 5, paragraph on ExpandR framework) |
| **Figure 8** | BehCal RL Expected Calibration Error Minimization | Section III (Pillar 5, paragraph on calibrated reinforcement learning) |
| **Figure 9** | Impact of Explanation Framing on User Trust | Section III (Pillar 6, paragraph on explainability and trust) |
| **Figure 10** | AUROC vs. F1 Scatter Distribution | Section IV (Comparative Analysis, paragraph on accuracy trade-offs) |
| **Figure 11** | Comprehensive AUROC vs. F1 Annotated by Speedup | Section IV (Comparative Analysis, paragraph on detection comparisons) |
| **Figure 12** | Speedup Factor vs. AUROC Operational Trade-Off | Section IV (Comparative Analysis, paragraph on computational efficiency) |
| **Table 1** | Literature Search and Systematic Selection Summary | Section II (Methodology, Subsection 2.3 Included Studies) |
| **Table 2** | Key Benchmarks and Evaluation Limitations | Section III (Pillar 4, paragraph on benchmark fragmentation) |
| **Table 3** | Summary of Mitigation Frameworks & Access Types | Section III (Pillar 5, paragraph on mitigation takeaways) |
| **Table 4** | Comparative Analysis of Hallucination Detection Methods | Section IV (Comparative Analysis, paragraph on practical dimensions) |
