# Toward Trustworthy Large Language Models: A Comprehensive Review of Hallucination Detection, Explainability, and Mitigation Strategies

**Project / Framework:** TRUEGUARD (Closed-Loop Multi-Signal Hallucination Detection and Three-Tier Mitigation)  
**Candidate:** Yogesh Ravi M (`22MIA1052`)  
**Supervisor:** Dr. Pradeep Kumar T.S.  
**Programme:** M.Tech. (Integrated) Computer Science and Engineering with Specialization in Business Analytics  
**Institution:** School of Computer Science and Engineering (SCOPE), Vellore Institute of Technology (VIT), Chennai  

---

## 1. Overview

**TRUEGUARD** is a closed-loop feedback control framework for real-time hallucination detection and graded runtime mitigation in autoregressive Large Language Models (LLMs). Grounded in a PRISMA 2020 systematic literature review of **40 peer-reviewed primary studies (2020–2025)** across **Six Research Pillars**, TRUEGUARD extracts **four complementary single-pass internal signals** during generation and routes risky outputs through a **two-threshold, three-tier corrective controller**.

### Core Architecture

1. **Four Single-Pass Internal Sensors (`src/tg_pipeline.py`):**
   - **Sensor 1 — Internal State Probe (`ISP`, $F_t$):** Supervised L2-regularized logistic probes trained across 4 fractional transformer depths $\{0.45, 0.60, 0.75, 0.90\}L$ using leakage-free inner grouped out-of-fold (`GroupKFold`) stacking.
   - **Sensor 2 — Attention Anomaly Score (`AAS`, $A_t$):** Normalized Shannon entropy of causal attention distributions across heads in the final quartile of transformer layers ($\mathcal{L}_{\text{top}} = [\lfloor 3L/4 \rfloor, L)$).
   - **Sensor 3 — Energy & Entropy Monitor (`EEM`, $H_{\text{ent},t}$):** Scale-invariant hybrid vocabulary uncertainty combining normalized Shannon entropy ($0.6$) and quadratic Rényi-2 entropy ($0.4$).
   - **Sensor 4 — Directional Semantic Trajectory (`DST`, $D_t$):** Consecutive-token cosine distance $1 - \cos(h_{L,t}, h_{L,t-1})$ in the final hidden manifold.
2. **State Estimator & Explainable Fusion (`TrueGuardDetector`):**
   - Pools token-level trajectories into a 4-dimensional sequence vector $\phi(x,y) = [\bar{F}, \bar{A}, \bar{H}_{\text{ent}}, \bar{D}]^\top$, applies `StandardScaler` + L2-regularized logistic regression, and outputs calibrated risk $r(x,y) \in [0,1]$ together with exact per-sensor log-odds attributions (`explain()`).
3. **Closed-Loop Three-Tier Graded Actuator (`src/tg_controller.py`):**
   - **SAFE ($r < \tau_{\text{warning}}$):** Emits initial greedy answer $y^{(0)}$ with zero extra decoding passes.
   - **TIER 1 — Local Re-Sampling ($\tau_{\text{warning}} \le r < \tau_{\text{fault}}$):** Re-samples with annealed temperatures $T \in \{0.35, 0.20\}$ and accepts $y^{(k)}$ if re-scored risk drops below $r^{(0)}$ and $\tau_{\text{fault}}$.
   - **TIER 2 — Targeted Retrieval Grounding ($r \ge \tau_{\text{fault}}$ or Tier 1 Failure):** Queries Wikipedia via keyword-cleaned `WikipediaRetriever`, prepends top-3 evidence passages, regenerates $y^{\text{RAG}}$, and re-verifies internal risk.
   - **TIER 3 — Calibrated Abstention ($r_{\text{RAG}} \ge \tau_{\text{fault}}$):** Emits a transparent refusal accompanied by per-sensor log-odds attributions.

---

## 2. Repository Structure

```text
E:\trueguard\
├── FINAL_REPORT.docx                     # Official College-Formatted Final Project Report (60-70 pages)
├── FINAL_REPORT.pdf                      # Rendered PDF Export of Final Project Report
├── PROJECT_STATE.md                      # Step 1 Git Audit, Inventory & Mismatch Cross-Check Table
├── ANALYSIS.md                           # Step 2 College Template Rules, Friend Report Audit & Page Plan
├── QA_REPORT.md                          # Step 5 Full Verification & Quality Assurance Audit
├── TRUEGUARD_40_Papers_Literature_Review_By_Pillars.docx  # Standalone 40-Paper 6-Pillar Review
├── requirements.txt                      # Pinned Reproducible Python Dependencies
├── outputs/                              # Step 3 Verified Metrics, CSV Tables, Logs & 34 Figures
│   ├── figures/                          # High-resolution PNG figures used in FINAL_REPORT.docx
│   ├── tables/                           # CSV summary tables (TinyLlama, GPT-2, TriviaQA, Latency)
│   └── logs/                             # JSON evaluation reports & equivalence test logs
└── CAPSTONE/
    ├── FINAL_REPORT.docx                 # Mirror copy of Final Project Report
    ├── FINAL_REPORT.pdf                  # Mirror copy of Final Project Report PDF
    ├── PROJECT_STATE.md                  # Mirror copy of Project State Audit
    ├── ANALYSIS.md                       # Mirror copy of Template Analysis
    ├── QA_REPORT.md                      # Mirror copy of QA Report
    ├── outputs/                          # Mirror copy of verified outputs
    └── FInal/                            # Core TRUEGUARD v2 Python Package & Experiments
        ├── src/
        │   ├── tg_pipeline.py            # 4 single-pass sensors, OnlineSignalMonitor, TrueGuardDetector
        │   ├── tg_controller.py          # 3-Tier closed-loop actuator & WikipediaRetriever
        │   ├── tg_eval.py                # Grouped K-Fold CV, bootstrap CIs, AURC & plotters
        │   └── tg_data.py                # HuggingFace dataset downloader & answer grader
        ├── experiments/
        │   ├── extract_activations.py    # Extracts real hidden-state & sensor caches (.npz)
        │   ├── evaluate_detection.py     # Multi-benchmark grouped CV & cross-dataset evaluation
        │   ├── evaluate_mitigation.py    # Live TriviaQA 3-tier closed-loop mitigation evaluation
        │   └── benchmark_latency.py      # Per-token latency & memory profiler
        ├── tests/
        │   └── test_equivalence.py       # Teacher-forced vs. online KV-cached equivalence tests
        ├── datasets/                     # Downloaded JSONL benchmark datasets (48,761 total records)
        └── results/v2/                   # Verified Tesla T4 GPU (TinyLlama-1.1B) & CPU (GPT-2) results
```

---

## 3. Reproducible Execution Instructions

### 3.1 Environment Setup

```powershell
python -m venv CAPSTONE/FInal/.venv
CAPSTONE\FInal\.venv\Scripts\activate
pip install -r requirements.txt
```

### 3.2 Run End-to-End Verification & Populate `/outputs`

```powershell
CAPSTONE\FInal\.venv\Scripts\python.exe CAPSTONE\FInal\tests\test_equivalence.py
CAPSTONE\FInal\.venv\Scripts\python.exe CAPSTONE\FInal\tools\populate_outputs.py
```

### 3.3 Run Detection, Mitigation & Latency Benchmarks

```powershell
# 1. Extract activations on GPU/CPU (Fixed seed = 42)
python CAPSTONE/FInal/experiments/extract_activations.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --max-questions 400 --seed 42

# 2. Run 5-Fold Grouped CV Detection & Cross-Dataset Transfer
python CAPSTONE/FInal/experiments/evaluate_detection.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --folds 5 --seed 42

# 3. Run Live TriviaQA 3-Tier Mitigation
python CAPSTONE/FInal/experiments/evaluate_mitigation.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n-cal 150 --n-test 150 --seed 42

# 4. Profile Real Per-Token Latency
python CAPSTONE/FInal/experiments/benchmark_latency.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n-prompts 25 --max-new-tokens 24
```

---

## 4. Summary of Verified Headlines (`TinyLlama-1.1B` on NVIDIA Tesla T4 GPU)

- **Multi-Benchmark Detection ($N = 3{,}196$ answers, 5-Fold Grouped CV):** **`0.935` macro AUROC** (`0.986` `HaluEval-Summarization`, `0.975` `HaluEval-QA`, `0.903` `HaluEval-Dialogue`, `0.876` `TruthfulQA`), macro F1 = **`0.882`**, macro ECE = **`0.031`**.
- **Live Open-Domain QA Mitigation (`TriviaQA`, $n_{\text{cal}}=150, n_{\text{test}}=150$):** Answered-query hallucination rate drops **`62.0% -> 40.0%`** (**`35.5%` relative reduction**; factual accuracy rises **`38.0% -> 60.0%`** at `43.3%` coverage); system-wide emitted hallucination rate drops **`62.0% -> 17.3%`** (**`72.0%` relative reduction**); Risk–Coverage **`AURC = 0.412`** vs. `0.526` (Entropy) and `0.603` (NLL).
- **Per-Token Inference Latency (Tesla T4 GPU):** Vanilla decode = `33.49 ms/tok`; TRUEGUARD Post-pass = **`36.41 ms/tok`** (`+2.91 ms/tok`, `+8.7%`, **`4.65x` faster** than 5-sample consistency at `169.31 ms/tok`); TRUEGUARD Online = **`39.30 ms/tok`** (**`4.31x` faster**).
