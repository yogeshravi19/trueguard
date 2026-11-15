# TRUEGUARD: NEURAL SENTINEL — Final Presentation & Scientific Verification Record

This document provides a line-by-line verification record mapping the university slide requirements, scientific corrections, dataset counts, and experimental results directly to codebase artifacts in `E:\trueguard`.

---

## 1. Slide-by-Slide College PPT Mapping (Strictly 30 Slides)

| Slide No. | Official University / Capstone Required Section | TRUEGUARD: NEURAL SENTINEL Title & Visual Layout | Theme Asset & Figure Embedded |
| :---: | :--- | :--- | :--- |
| **01** | **Title Slide** (VIT Chennai, SCOPE, Candidate & Guide Details) | `TRUEGUARD: NEURAL SENTINEL — Toward Trustworthy LLMs` | `bg_neural_sentinel.jpg`, `vit_logo_hd.png` |
| **02** | **Outline / Agenda** (Roadmap of Presentation) | `OVERVIEW: Presentation Roadmap & Defense Structure` | 6 Modular Cyber-Cards, `#080F25` Grid |
| **03** | **1. Introduction & Background** (LLM Mechanics & Hallucinations) | `FOUNDATIONS: What is an LLM? What is Hallucination?` | `bg_transformer_layers.jpg`, Token Stream |
| **04** | **2. Scope & Problem Statement** (Concrete Research Evidence) | `FOUNDATIONS: Research Evidence & Core Problem Statement` | `bg_hallucination_stream.jpg`, TruthfulQA Case |
| **05** | **3. Research Objectives** (Dual Papers & 4 Core Goals) | `FOUNDATIONS: Two Research Papers & Project Objectives` | Dual Manuscript Badges, 4 Objective Cards |
| **06** | **4. Literature Review (I)** (Pillar 1: Probing & Geometry) | `LITERATURE REVIEW (1/4): Internal State Probing & Geometry` | Table: Papers 1–10 (Su, Azaria, Li, Zou, etc.) |
| **07** | **4. Literature Review (II)** (Pillar 2: Attention & Entropy) | `LITERATURE REVIEW (2/4): Attention Anomalies & Entropy` | Table: Papers 11–20 (Burns, Kadavath, Manakul) |
| **08** | **4. Literature Review (III)** (Pillar 3: Mitigation & Control) | `LITERATURE REVIEW (3/4): Closed-Loop Control & Mitigation` | Table: Papers 21–30 (Lewis, Asai, Dathathri) |
| **09** | **4. Literature Review (IV)** (Pillar 4: Benchmarks & Safety) | `LITERATURE REVIEW (4/4): Factuality Benchmarks & Safety` | Table: Papers 31–40 (Lin, Li, Min, Thorne, etc.) |
| **10** | **5. Research Challenges & Gaps** (Systematic Failure Modes) | `RESEARCH GAPS: Systematic Gaps Across 40 Papers` | 4 Floating Cyber-Hazard Panels |
| **11** | **6. Comparison with Existing Works** (Comparative Matrix) | `BENCHMARK COMPARISON: Feature Matrix (Existing vs TRUEGUARD)` | Full-Screen 7x7 Multi-Feature Matrix Table |
| **12** | **7. Model Choice & Access Paradigm** (White-Box vs Black-Box) | `ARCHITECTURE: TinyLlama-1.1B Backbone & White-Box Access` | `fig_sentinel_white_vs_black_box.png` |
| **13** | **8. Proposed Architecture** (Master Closed-Loop Framework) | `ARCHITECTURE: Master System Closed-Loop Architecture` | `fig_trueguard_architecture_master.png` |
| **14** | **9. The Four Intrinsic Signals** (Telemetry Bank Overview) | `SENSORS: Four-Sensor Internal Telemetry Bank Overview` | `bg_four_sensors.jpg`, 4 Modular Sensor Cards |
| **15** | **10. Sensor Deep Dive (I)** (ISP & AAS Mathematical Details) | `SENSORS: Deep Dive into State Probes (ISP) & Attention (AAS)` | Math Cards: 4 Depths (9,13,16,19) & Layers 16–21 |
| **16** | **10. Sensor Deep Dive (II)** (EEM & DST Mathematical Details) | `SENSORS: Deep Dive into Energy-Entropy (EEM) & Drift (DST)` | `fig_sentinel_entropy_concept.png`, Math Cards |
| **17** | **11. Experimental Methodology (Datasets)** (Curated Corpora) | `DATASETS: Benchmark Dataset Curation & Authentic Counts` | `bg_pipeline_flow.jpg`, 5 Verified Dataset Cards |
| **18** | **11. Experimental Methodology (Samples)** (Real Dataset Pairs) | `DATASETS: Authentic Dataset Examples (Grounded vs False)` | Real Query Records (TruthfulQA, HaluEval) |
| **19** | **12. Implementation Progress (Pipeline)** (Preprocessing Flow) | `DATA PREPARATION: Preprocessing & Dataflow Pipeline` | 6-Stage End-to-End Extraction Workflow |
| **20** | **12. Implementation Progress (Hooks)** (PyTorch Telemetry) | `FEATURE EXTRACTION: PyTorch Forward Hooks & Teacher Forcing` | Non-Invasive Interception & 7-Dim Vectors |
| **21** | **13. Training & Calibration** (Frozen LLM & Logistic Fit) | `TRAINING: Detector Training & Inherent Calibration` | Frozen Backbone vs Trained Probes & Fusion |
| **22** | **13. Validation Protocol** (Leakage-Free GroupKFold) | `VALIDATION: Rigorous 5-Fold Grouped Cross-Validation` | Question ID Grouping & Scaler Isolation |
| **23** | **14. Active Mitigation Engine** (Three-Tier Closed Loop) | `MITIGATION: Three-Tier Closed-Loop Mitigation Actuator` | `fig_sentinel_mitigation_controller.png` |
| **24** | **15. Results: Detection Performance** (Figure 7.1) | `RESULTS (FIG 7.1): Multi-Benchmark Detection AUROC (0.935)` | `fig_hd_7_1.png` (600 DPI High-Definition Plot) |
| **25** | **15. Results: Transfer & Generalization** (Figure 7.2) | `RESULTS (FIG 7.2): Paired vs Own-Gen & Zero-Shot Transfer` | `fig_hd_7_2.png` (600 DPI High-Definition Plot) |
| **26** | **15. Results: Sensor Ablation** (Figures 7.3 & 7.4) | `RESULTS (FIG 7.3 & 7.4): Sensor Ablation & Out-of-Fold ROC` | `fig_hd_7_3.png` & `fig_hd_7_4.png` (Dual 600 DPI) |
| **27** | **16. Results: Mitigation Performance** (Figure 8.1) | `RESULTS (FIG 8.1): 3-Tier Mitigation & 72% Hallucination Drop` | `fig_hd_8_1.png` (600 DPI High-Definition Plot) |
| **28** | **16. Results: Efficiency & Latency** (Figure 8.2) | `RESULTS (FIG 8.2): Risk-Coverage (AURC) & T4 GPU Latency` | `fig_hd_8_2.png` (600 DPI High-Definition Plot) |
| **29** | **17. Applications & Limitations** (Deployment Boundaries) | `DEPLOYMENT: Real-World Applications & Scientific Limitations` | Enterprise Domains vs 4 Core Limitations |
| **30** | **18. Conclusion & Future Work** (Contributions & Viva Defense) | `CONCLUSION: Key Contributions, Summary & Viva Acknowledgment` | `bg_neural_sentinel.jpg`, Viva Defense Statement |

---

## 2. Verification of the 9 Scientific Corrections

| Correction ID | Specific Technical Correction | Status | Verified Codebase / Report Source |
| :---: | :--- | :---: | :--- |
| **Correction A (ISP)** | Verified ISP monitors 4 depths (fractions 0.45, 0.60, 0.75, 0.90 -> Layers 9, 13, 16, 19 of TinyLlama-1.1B), not just Layer 16. | **VERIFIED** | `CAPSTONE/FInal/src/signal_extractors.py` lines 38–55 |
| **Correction B (AAS)** | Verified AAS computes normalized Shannon entropy across all heads over final quartile layers (Layers 16 to 21), normalized by $\ln(S)$, eliminating arbitrary "8 heads". | **VERIFIED** | `CAPSTONE/FInal/src/signal_extractors.py` lines 86–112 |
| **Correction C (EEM)** | Verified EEM combines normalized Shannon entropy ($w_e=0.6$) and Rényi-2 collision entropy ($0.4$). | **VERIFIED** | `CAPSTONE/FInal/src/signal_extractors.py` lines 135–158 |
| **Correction D (DST)** | Verified DST computes temporal cosine distance across late layers (13, 16, 19) and clarified as a statistical signal, not direct factual proof. | **VERIFIED** | `CAPSTONE/FInal/src/signal_extractors.py` lines 170–198 |
| **Correction E (Training)** | Clarified TinyLlama is 100% frozen; only lightweight linear probes and logistic fusion classifier are trained via L-BFGS. Removed un-implemented secondary Platt scaling stage. | **VERIFIED** | `CAPSTONE/FInal/src/fusion.py` lines 20–55 |
| **Correction F (Mitigation)** | Verified Three-Tier Controller parameters: $K=4$ candidate sampling with $T=0.7$, $p=0.9$, Wikipedia RAG, and Safe Abstention. Removed incorrect "temperatures 0.35 and 0.20". | **VERIFIED** | `CAPSTONE/FInal/src/tg_controller.py` lines 85–130 |
| **Correction G (Datasets)** | Replaced any fabricated examples with genuine saved records from TruthfulQA and HaluEval; verified 1,598 paired questions produce 3,196 labeled rows. | **VERIFIED** | `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/detection_report.json` |
| **Correction H (Claims)** | Standardized all experimental numbers to authentic verified results: 0.935 Macro AUROC, 0.795 Own-Gen AUROC, 72.0% hallucination reduction, 43.3% coverage, +8.7% / +17.3% latency. | **VERIFIED** | `detection_report.json`, `mitigation_report.json`, `real_latency.json` |
| **Correction I (Limitations)** | Candidly documented 4 core boundaries: white-box requirement, closed API incompatibility, 56.7% abstention tradeoff, and domain shift sensitivity. | **VERIFIED** | Slide 29 & thesis Chapter 9 |

---

## 3. Strict Source Mapping Linking Every Number to Repository Artifacts

### A. Detection Metrics (Table 7.1 & Figure 7.1)
- **Source**: `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/detection_report.json`
  - `truthful_qa`: AUROC = **0.8756** (0.876)
  - `halueval_qa`: AUROC = **0.9754** (0.975)
  - `halueval_dialogue`: AUROC = **0.9029** (0.903)
  - `halueval_summarization`: AUROC = **0.9863** (0.986)
  - **Macro-Averaged AUROC**: **0.9351** (0.935)

### B. Free Own-Generation & Mitigation Metrics (Table 8.1 & Figure 8.1)
- **Source**: `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/mitigation_report.json`
  - Total queries evaluated: **150**
  - Baseline unguarded Accuracy: **38.0%** (57/150)
  - Baseline unguarded Hallucinations: **62.0%** (93/150)
  - Own-Generation AUROC on TriviaQA: **0.7948** (0.795)
  - Controller Tier Distribution:
    - Safe Pass (Tier 0): **48** (32.0%)
    - Resampling (Tier 1): **11** (7.3%)
    - Wikipedia RAG (Tier 2): **6** (4.0%)
    - Calibrated Abstention (Tier 3): **85** (56.7%)
  - Total Answered Queries (Coverage): **65 / 150 = 43.33%** (43.3%)
  - Accuracy among answered: **39 / 65 = 60.0%** (up from 38.0%)
  - Emitted Hallucinations system-wide: **26 / 150 = 17.33%** (down from 62.0%)
  - **Relative Hallucination Reduction**: $(62.0 - 17.33) / 62.0 = \mathbf{72.04\%}$ (**72.0%**)

### C. Latency Profiling on NVIDIA Tesla T4 GPU (Table 8.2 & Figure 8.2)
- **Source**: `results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/real_latency.json`
  - Vanilla TinyLlama decode: **33.49 ms/token**
  - TRUEGUARD Post-pass telemetry: **36.41 ms/token** (+2.91 ms, **+8.7%** overhead)
  - TRUEGUARD Online real-time telemetry: **39.30 ms/token** (+5.81 ms, **+17.3%** overhead)
  - 5-Sample Consistency baseline: **169.31 ms/token** (+135.82 ms, **4.3x to 4.7x slower**, +405% overhead)
  - Area Under the Risk-Coverage Curve (AURC): **0.412**
