# ANALYSIS.md — College Template Specification, Reference Report Audit & 60–70 Page Plan

**Project Title:** Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies

---

## 1. Authoritative Specification of `[COLLEGE_TEMPLATE]` (`MIA-Project Template.docx`)

The college template (`E:\trueguard\CAPSTONE\sample\MIA-Project Template.docx`) establishes the **mandatory formatting and structural rules** for the M.Tech. (Integrated) CSE (Business Analytics) project report at Vellore Institute of Technology (VIT), Chennai. Where any stylistic variation exists between `MIA-Project Template.docx` and `friend report.pdf`, **`MIA-Project Template.docx` takes precedence**.

### 1.1 Mandatory Sequence of Sections
1. **Cover Page** (Unnumbered; White flexible art paper cover, black lettering; includes *"A project report on"* in 12 pt Italic).
2. **Title Page** (Unnumbered; identical to Cover Page except the top *"A project report on"* line is omitted).
3. **Declaration by the Candidate** (Unnumbered; VIT Chennai header logo, `DECLARATION` 14 pt Bold Underlined CAPS, 12 pt body text with 1.5 spacing, `Place: Chennai`, `Date:`, and `Signature of the Candidate` in 14 pt Bold).
4. **Certificate** (Unnumbered; VIT Chennai header logo, `School of Computer Science and Engineering` 12 pt Bold, `CERTIFICATE` 14 pt CAPS, certification paragraph, signature blocks for Guide, Examiner 1, Examiner 2, and `Approved by the Head of Department`).
5. **Abstract** (Roman numeral `i` at bottom center; `ABSTRACT` 14 pt Bold Underlined CAPS; 12 pt justified body text with 1.5 line spacing + Keywords).
6. **Acknowledgement** (Roman numeral `ii` at bottom center; `ACKNOWLEDGEMENT` 12–14 pt Bold CAPS; 4 standard paragraphs thanking the Guide, Chancellor & Vice-Presidents, Dean & Associate Deans of SCOPE, HoD of SCOPE, faculty, parents, and friends; `Place: Chennai`, `Date:`, and Candidate Name in 12 pt Bold).
7. **Table of Contents (`CONTENTS`)** (Roman numerals `iii–v` at bottom center; `CONTENTS` 14–16 pt Bold CAPS; lists front matter, all chapters, sections, subsections, appendices, and references with right-aligned page numbers).
8. **List of Figures (`LIST OF FIGURES`)** (Roman numeral `vi` at bottom center; `LIST OF FIGURES` 14 pt Bold CAPS; lists figure number, title, and page number).
9. **List of Tables (`LIST OF TABLES`)** (Roman numeral `vii` at bottom center; `LIST OF TABLES` 14 pt Bold CAPS; lists table number, title, and page number).
10. **List of Symbols, Abbreviations and Nomenclature (`LIST OF ACRONYMS` / `LIST OF SYMBOLS, ABBREVIATIONS AND NOMENCLATURE`)** (Roman numeral `viii` at bottom center; `LIST OF ACRONYMS` 14 pt Bold CAPS; tabular alphabetical list of all acronyms and mathematical symbols used across the thesis).
11. **Chapters of the Report (Chapters 1 to 8)** (Arabic numerals `1, 2, 3...` at **bottom center** of every page).
12. **Conclusion & Future Work (Chapter 9)** (Final chapter summarizing key findings, limitations/failures as well as successes, performance against targets, and concrete extensions).
13. **Appendices (`Appendix 1`, `Appendix 2`, etc.)** (Numbered using Arabic numerals `Appendix 1`, `Appendix 2`, etc., per template page 15 rule: *"Appendices should be numbered using Arabic numerals, e.g. Appendix 1, Appendix 2 etc."*).
14. **References (`REFERENCES`)** (`REFERENCES` 16 pt Bold CAPS Centered; **all references formatted in APA style** with bracketed citation indices `[1]..[45]` matching in-text citations `[1]` as shown on template pages 13 and 16).

### 1.2 Page Dimensions, Margins & Page Count Rules
- **Paper Size:** **A4** ($21.0\text{ cm} \times 29.7\text{ cm}$ / $8.27\text{ in} \times 11.69\text{ in}$).
- **Margins:**
  - **Left Margin:** `3.81 cm` (`1.5 in`) — binding allowance.
  - **Right Margin:** `2.54 cm` (`1.0 in`).
  - **Top Margin:** `2.54 cm` (`1.0 in`).
  - **Bottom Margin:** `2.54 cm` (`1.0 in`).
- **Total Page Count:** Template specifies **Minimum 60 – Maximum 100 pages**; user requirement specifies **60 to 70 pages** (`FINAL_REPORT.docx` and `FINAL_REPORT.pdf`).

### 1.3 Typography, Headings & Paragraph Rules
- **Font Family:** **Times New Roman** consistently throughout the entire report.
- **Body Text:** **12 pt**, Justified alignment, **1.5 line spacing**, with `keep_lines_together` / `widow_control` enabled so no paragraph has an isolated opening line at the bottom of a page.
- **Chapter Heading:**
  - Line 1: `CHAPTER <N>` — **Times New Roman, 12 pt to 16 pt, Bold, Centered, ALL CAPS**.
  - Line 2: `<CHAPTER TITLE>` — **Times New Roman, 16 pt, Bold, Centered, ALL CAPS**.
- **Section Heading (`X.Y`):** **Times New Roman, 14 pt, Bold, ALL CAPS** (e.g., `1.1 INTRODUCTION`).
- **Subsection Heading (`X.Y.Z`):** **Times New Roman, 12 pt, Bold, ALL CAPS** (e.g., `1.8.1 UNIFIED MULTI-SIGNAL DETECTION FRAMEWORK`).
- **Captions for Figures & Tables:** **Times New Roman, 10 pt to 11 pt, Italic/Bold**, single-spaced (not smaller than 10 pt), centered below figures (`FIGURE X.Y: ...`) and above tables (`TABLE X.Y: ...`).
- **Page Numbers:** All text pages, appendices, and references numbered using **Arabic numerals at the bottom center** of the pages (following lowercase Roman numerals `i, ii, iii...` on front matter pages starting at `ABSTRACT`).

---

## 2. Structural Analysis of `[FRIEND_REPORT]` (`friend report.pdf`)

The friend's finished report (*"GeoFence: A Unified Geofencing-Based Asset Monitoring, Encroachment Detection and Alert Management System"* by Abishek B, `22MIA1075`, supervised by Dr. Sivagami M) is 84 PDF pages long (12 front-matter pages + 72 numbered Arabic pages `1–72`).

### 2.1 Chapter Breakdown & Depth in `friend report.pdf`

| Section / Chapter in `friend report.pdf` | Numbered Pages | Page Span | Content Structure & Depth Applied |
| :--- | :--- | :--- | :--- |
| Front Matter (Cover, Title, Declaration, Certificate, Abstract, Ack, TOC, LOF, LOT) | Unnumbered (4) + `i–viii` (8) | 12 pages | Exact VIT Chennai boilerplate, 3-paragraph Abstract with Keywords, 4-page TOC, 1-page LOF (15 figures), 1-page LOT (12 tables). *(Note: `friend report.pdf` omitted `LIST OF ACRONYMS`; we include `LIST OF ACRONYMS` per `MIA-Project Template.docx` rule #10).* |
| **Chapter 1: Introduction** | pp. 1–9 | 8.5 pages | `1.1 Introduction`, `1.2 Background`, `1.3 Motivation`, `1.4 Problem Statement`, `1.5 Research Gap`, `1.6 Objectives`, `1.7 Scope`, `1.8 Contributions` (9 numbered sub-contributions). |
| **Chapter 2: Background and Theoretical Foundation** | pp. 9–19 | 10.5 pages | 15 theoretical subsections (`2.1` to `2.15`) explaining domain concepts, mathematical foundations, uncertainty, and risk scoring weights. |
| **Chapter 3: Literature Review** | pp. 20–23 | 4 pages | `3.1 Literature Review Matrix` (20-row multi-page structured comparison table with columns: S.No., Author/Year, Method/Approach, Key Contribution, Gap Identified). |
| **Chapter 4: System Analysis and Requirements** | pp. 24–28 | 5 pages | `4.1 Existing System` & fragmentation analysis, `4.2 Proposed System` & design principles, `4.3 Functional Requirements` (tabular), `4.4 Non-Functional Requirements` (tabular), `4.5 Technology Stack` (tabular). |
| **Chapter 5: System Architecture and Data Design** | pp. 29–37 | 9 pages | `5.1 Architecture Overview`, `5.2 Architectural Layers` (6 layers), `5.3–5.5 Data Model`, `5.6 System Data Flow` with architecture & data-flow diagrams. |
| **Chapter 6: Methodology and Algorithmic Design** | pp. 38–46 | 9 pages | `6.1 Overall Methodology` through `6.11` covering mathematical equations, algorithmic workflows, scoring formulas, classifier formulation, and decision thresholds. |
| **Chapter 7: System Implementation** | pp. 47–54 | 8 pages | `7.1 Implementation Environment`, `7.2 Core Pipeline Implementation`, `7.3 Module Integration`, `7.4 Key Code Excerpts & Schemas`, `7.5 Reporting & Monitoring Output`. |
| **Chapter 8: Testing, Results and Discussion** | pp. 55–63 | 9 pages | `8.1 Testing Methodology`, `8.2 Functional Verification`, `8.3 Quantitative Model Performance Evaluation` (ROC-AUC, F1, confusion matrices, feature importance), `8.4 End-to-End Mitigation & Ablation Discussion`. |
| **Chapter 9: Conclusion and Future Work** | pp. 64 | 1 page | `9.1 Conclusion`, `9.2 Future Work`. |
| **Appendices** | pp. 65–70 | 6 pages | 6 structured appendices covering API/module inventory, data schemas, verification evidence, decision logic, and operating procedure. *(We number ours `Appendix 1`..`Appendix 4` per template page 15 rule).* |
| **References** | pp. 71–72 | 2 pages | Numbered APA references `[1]..[20]` with DOIs. |

---

## 3. Summary of Core Technical Inputs (`[RESEARCH_PAPER]` & `[FINDINGS_REPORT]`)

### 3.1 Research Paper 1 (`Toward Trustworthy Large Language Models_standard.docx` & 40-Paper Pillar Review)
- **Title & Scope:** *Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies*.
- **Methodology:** PRISMA 2020 systematic review screening $688$ initial records across 5 databases (`arXiv 214, Scopus 186, IEEE Xplore 112, Web of Science 92, ACM Digital Library 84` $\to$ $492$ unique $\to$ $168$ full-text) down to **$40$ peer-reviewed primary studies** (`20 Core Architectural Studies + 20 Foundational Benchmarks and Mitigation Frameworks`, `2020–2026`), organized across **Six Research Pillars**:
  1. **Pillar 1 — Internal-State Based Detection (7 papers):** Azaria & Mitchell (2023) `SAPLMA`, Burns et al. (2023) `CCS`, Li et al. (2023) `ITI`, Marks & Tegmark (2024) Geometry of Truth, Zou et al. (2023) `RepE`, Chen et al. (2024) `INSIDE` (`EigenScore`), Chuang et al. (2024) `DoLa`.
  2. **Pillar 2 — Attention Mechanism Analysis (5 papers):** Yuksekgonul et al. (2024) Attention Satisfies, Huang et al. (2024) `OPERA`, Chuang et al. (2024) `Lookback Lens`, Bhattacharya et al. (2024) Attention Entropy, Sriramanan et al. (2024) `LLM-Check`.
  3. **Pillar 3 — Uncertainty & Entropy Estimation (7 papers):** Kadavath et al. (2022) $P(\text{True})$, Kuhn et al. (2023) Semantic Entropy, Farquhar et al. (2024) Semantic Entropy in *Nature*, Lin et al. (2024) Uncertainty Quantification in LLMs, Liu et al. (2020) Energy-Based OOD, Fadeeva et al. (2024) `LM-Polygraph`, Duan et al. (2024) `SAR`.
  4. **Pillar 4 — Post-Hoc Verification & Self-Consistency (7 papers):** Manakul et al. (2023) `SelfCheckGPT`, Min et al. (2023) `FActScore`, Dhuliawala et al. (2024) `CoVe`, Gao et al. (2023) `RARR`, Chern et al. (2023) `FacTool`, Gou et al. (2024) `CRITIC`, Wang et al. (2023) Self-Consistency.
  5. **Pillar 5 — Knowledge Grounding & RAG (7 papers):** Lewis et al. (2020) `RAG`, Asai et al. (2024) `Self-RAG`, Jiang et al. (2023) `FLARE`, Yan et al. (2024) `CRAG`, Shi et al. (2024) `REPLUG`, Baek et al. (2023) `KAPING`, Trivedi et al. (2023) `IRCoT`.
  6. **Pillar 6 — Taxonomies, Benchmarks & Surveys (7 papers):** Ji et al. (2023) Survey of Hallucination in NLG, Huang et al. (2025) Survey on Hallucination in LLMs, Zhang et al. (2023) Siren's Song, Lin et al. (2022) `TruthfulQA`, Li et al. (2023) `HaluEval`, Min et al. (2023) `FActScore` Benchmark, Liang et al. (2023) `HELM`.
- **Architectural Contribution (`TRUEGUARD`):** Formulates LLM hallucination detection and mitigation as a **closed-loop feedback control system** comprising a **Plant** (autoregressive LLM), a **4-Sensor Bank** (`ISP`, `AAS`, `EEM`, `DST`), a **State Estimator** (sequence pooling + L2-regularized logistic fusion with log-odds attribution), and a **3-Tier Graded Actuator** governed by two calibrated risk thresholds ($\tau_{\text{warning}}, \tau_{\text{fault}}$).

### 3.2 Empirical Findings Report & Paper 2 (`results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/` & `gpt2/`)
- **Detection Evaluation ($N = 3{,}196$ real answers on `TinyLlama-1.1B`, Tesla T4 GPU, 5-fold grouped CV):**
  - `TRUEGUARD_full` achieves **`0.935` macro AUROC** (`0.876` `TruthfulQA`, `0.975` `HaluEval-QA`, `0.903` `HaluEval-Dialogue`, `0.986` `HaluEval-Summarization`), **`0.938` macro AUPRC**, **`0.882` macro F1**, **`0.095` Brier score**, and **`0.031` Expected Calibration Error (ECE)**.
  - Outperforms all single-pass scalar baselines (`Normalized_Entropy` `0.629`, `Mean_Token_NLL` `0.583`, `Max_Token_NLL` `0.602`, `Energy_Score` `0.415`) by **$+30.6$ AUROC points**.
  - Outperforms every individual sensor (`ISP_only` `0.928`, `EEM_only` `0.629`, `AAS_only` `0.562`, `DST_only` `0.530`) and every leave-one-out ablation (`no_ISP` `0.680`, `no_EEM` `0.928`, `no_AAS` `0.935`, `no_DST` `0.935`).
- **Architecture-Generality Evaluation ($N = 480$ real answers on `GPT-2 124M`, Local CPU, 3-fold grouped CV):**
  - `TRUEGUARD_full` achieves **`0.802` macro AUROC** (`0.818` `TruthfulQA`, `0.946` `HaluEval-QA`, `0.640` `HaluEval-Dialogue`, `0.803` `HaluEval-Summarization`), outperforming `Normalized_Entropy` (`0.619`) by **$+18.3$ AUROC points**.
- **Closed-Loop 3-Tier Mitigation (`TriviaQA`, $n_{\text{cal}}=150, n_{\text{test}}=150$, Tesla T4 GPU):**
  - Calibrated thresholds: $\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$; live detection AUROC = **`0.795`**.
  - Tier routing: `15.3%` `SAFE` ($23/150$), `18.0%` `TIER1_RESAMPLE` ($27/150$), `10.0%` `TIER2_RETRIEVAL` ($15/150$), `56.7%` `TIER3_ABSTAIN` ($85/150$).
  - Answered-query hallucination rate drops **`62.0% -> 40.0%`** (**`35.5%` relative reduction**; factual accuracy rises **`38.0% -> 60.0%`**, $+22.0\text{ pp}$ at `43.3%` coverage).
  - System-wide emitted hallucination rate drops **`62.0% -> 17.3%`** (**`72.0%` relative reduction**).
  - Selective prediction Area Under Risk–Coverage curve: **`AURC = 0.412`** vs. `0.526` (`Normalized_Entropy`), `0.603` (`Mean_Token_NLL`), and `0.620` (unranked baseline).
- **Hardware Latency Profiling (Tesla T4 GPU & CPU):**
  - Tesla T4 GPU: Vanilla decode = `33.49 ms/tok`; TRUEGUARD Post-pass = **`36.41 ms/tok`** (`+2.92 ms/tok`, `+8.7%`, **`4.65x` faster** than 5-sample consistency at `169.31 ms/tok`); TRUEGUARD Online = **`39.30 ms/tok`** (`+5.81 ms/tok`, **`4.31x` faster**).

---

## 4. Proposed Chapter Outline & Page Budget (Target: 64–68 Total Pages)

To satisfy the **60 to 70 total pages** requirement cleanly without filler or near-empty pages, the report is structured into **10 Front-Matter pages (`4` unnumbered + `i–vi` Roman)** and **56 Numbered Arabic Pages (`1–56`)**, yielding **66 total pages**:

| Section / Chapter | Target Page Span | Page Count | Core Content Summary |
| :--- | :--- | :--- | :--- |
| **Front Matter** (Cover, Title, Declaration, Certificate, Abstract, Acknowledgement, TOC, LOF, LOT, List of Acronyms & Symbols) | Unnumbered (4) + `i–vi` (6) | **10 pages** | Strictly formatted to `MIA-Project Template.docx`. |
| **CHAPTER 1: INTRODUCTION** (`1.1`–`1.8`) | pp. 1–6 | **6 pages** | Generative reliability crisis, open-loop vs. closed-loop control motivation, formal problem statement, 6-pillar research gaps, project objectives, scope, and 8 core contributions. |
| **CHAPTER 2: BACKGROUND AND THEORETICAL FOUNDATION** (`2.1`–`2.8`) | pp. 7–13 | **7 pages** | Autoregressive transformer mechanics, formal taxonomy of hallucinations (intrinsic vs. extrinsic; factuality vs. faithfulness), geometry of truthfulness in hidden manifolds, attention head grounding & sink dynamics, Shannon/Rényi/free-energy uncertainty, directional semantic drift, and discrete-time feedback control theory. |
| **CHAPTER 3: LITERATURE REVIEW** (`3.1`–`3.9`) | pp. 14–23 | **10 pages** | PRISMA 2020 systematic review protocol + diagram, synthesis across all **6 Research Pillars** (`Pillar 1` through `Pillar 6`), complete **40-Paper Pillar-Classified Literature Review Matrix** (Tables 3.2–3.7), and quantitative synthesis of open architectural gaps. |
| **CHAPTER 4: SYSTEM ANALYSIS, REQUIREMENTS AND CONTROL ARCHITECTURE** (`4.1`–`4.6`) | pp. 24–29 | **6 pages** | Critical analysis of existing open-loop and multi-sample paradigms, proposed `TRUEGUARD` closed-loop control architecture, system block diagram, functional & non-functional requirements tables, and hardware/software technology stack. |
| **CHAPTER 5: DATASET CURATION, MATHEMATICAL MODEL DESIGN AND ALGORITHMIC FORMULATION** (`5.1`–`5.8`) | pp. 30–37 | **8 pages** | 5 real benchmark datasets (`TruthfulQA`, `HaluEval-QA/Dialogue/Summarization`, `TriviaQA`), leakage-free grouped splitting, numbered equations (`Eq. 5.1`–`Eq. 5.18`) for all 4 sensors (`ISP`, `AAS`, `EEM`, `DST`), inner OOF stacking, logistic fusion, log-odds attribution, and the 2-threshold 3-tier closed-loop actuation algorithm. |
| **CHAPTER 6: SYSTEM IMPLEMENTATION AND CODE ARCHITECTURE** (`6.1`–`6.6`) | pp. 38–44 | **7 pages** | End-to-end modular package layout, key production code excerpts from `src/tg_pipeline.py`, `src/tg_controller.py`, `src/tg_eval.py`, and `src/tg_data.py`, teacher-forced vs. KV-cached online equivalence verification (`tests/test_equivalence.py`), and reproducibility design. |
| **CHAPTER 7: EXPERIMENTAL SETUP, DETECTION RESULTS AND ABLATION ANALYSIS** (`7.1`–`7.7`) | pp. 45–52 | **8 pages** | Hardware/software testbeds (Tesla T4 GPU & CPU), 12-method evaluation protocol, multi-benchmark detection tables (`TinyLlama-1.1B` & `GPT-2`), ROC curves, leave-one-out ablation bar charts, confusion matrices, risk score distributions, sensor correlation & error-overlap matrices, and $4 \times 4$ cross-dataset transfer heatmap. |
| **CHAPTER 8: CLOSED-LOOP MITIGATION, LATENCY PROFILING AND LIMITATIONS** (`8.1`–`8.5`) | pp. 53–56 | **4 pages** | Live `TriviaQA` calibration & 3-tier mitigation results, Risk–Coverage (`AURC`) curves, Tesla T4 GPU & CPU per-token latency profiling, legacy v1 vs. verified v2 audit transparency, and honest engineering limitations. |
| **CHAPTER 9: CONCLUSION AND FUTURE WORK** (`9.1`–`9.2`) | pp. 57–58 | **2 pages** | Summary of achievements against objectives, key empirical takeaways, and concrete future research directions (adaptive layer routing, NLI-verified RAG, conformal risk control, 7B–70B scaling). |
| **APPENDICES (`Appendix 1` – `Appendix 3`)** | pp. 59–61 | **3 pages** | `Appendix 1`: Dataset Manifest & Schema Inventory; `Appendix 2`: Complete Hyperparameter, Calibration & Equivalence Test Log; `Appendix 3`: Reproducible Execution & CLI Operating Procedure. |
| **REFERENCES (`REFERENCES`)** | pp. 62–65 | **4 pages** | All **45 real peer-reviewed references** formatted in **APA style** (`[1]..[45]`) with full publication venues and DOIs/URLs. |
| **TOTAL REPORT LENGTH** | **10 Front + 55–58 Main** | **65–68 pages** | Strictly inside the **60–70 page** target window. |

