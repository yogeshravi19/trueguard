# 🛡️ TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in LLMs

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/🤗%20Transformers-4.35+-yellow.svg)](https://huggingface.co/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**Official Implementation & Verification Suite for the TRUEGUARD Framework**  
*Yogesh Ravi M, TS Pradeep Kumar* — *Vellore Institute of Technology, Chennai*

---

## 🧭 Navigation Index

1. [Overview & Mathematical Formulation](#-overview--mathematical-formulation)
2. [Repository Structure](#-repository-structure)
3. [Environment Setup](#-environment-setup)
4. [Reproducibility & Execution Commands](#-reproducibility--execution-commands)
   - [A. Fast CPU Smoke Test](#a-fast-cpu-smoke-test-60s)
   - [B. Multi-Benchmark Evaluation (5-Fold CV)](#b-multi-benchmark-evaluation-5-fold-cv)
   - [C. Signal Ablation Study](#c-signal-ablation-study)
   - [D. Latency & Speedup Profiling](#d-latency--speedup-profiling)
   - [E. Publication Figure Generation](#e-publication-figure-generation)
5. [Google Colab Workflow](#-google-colab-workflow)
6. [Empirical Results Summary](#-empirical-results-summary)
7. [Hardware Requirements](#-hardware-requirements)
8. [Citation & Contact](#-citation--contact)

---

## 🔍 Overview & Mathematical Formulation

Existing hallucination detection methods suffer from a severe trade-off: sampling-based approaches (such as Semantic Entropy) require 5 to 10 stochastic forward passes ($\sim 142.3\text{ ms/token}$), while single-signal white-box methods (such as HaluShift) fail to detect multi-faceted failure modes.

**TRUEGUARD** resolves this trade-off by concurrently monitoring four complementary intrinsic signals in a **single forward pass**:

```
Prompt C ──► [ LLM Forward Pass ] ──► (h_t^L, A_t, z_t)
                    │
   ┌────────────────┼────────────────┬────────────────┐
   ▼                ▼                ▼                ▼
 [ISP]            [AAS]            [EEM]            [DST]
Hidden State    Attention        Entropy-Energy   Distribution
 Probes          Anomaly          Monitor          Shift Tracker
   │                │                │                │
   └────────────────┴────────┬───────┴────────────────┘
                             ▼
              Online Z-Score Normalization
                             ▼
              Learned Logistic Regression: R(t) = σ(W^T X̂_t + b)
                             ▼
                    [ Risk Decision ]
                   /                 \
        R(t) ≤ 0.50                   R(t) > 0.50
     [ Safe Emission ]             [ Active Mitigation ]
                                   /                   \
                        Tier 1: Targeted RAG     Tier 2: Abstention
```

### Signal Definitions:
1. **Internal State Probes (ISP):** Evaluates hidden states $h_t^L$ across intermediate layers ($L \in \{15, 20, 25, 30\}$ for 32-layer models):
   $$\text{ISP}_t = \frac{1}{|L|}\sum_{L} \sigma(w_L^T h_t^L + b_L)$$
2. **Attention Anomaly Score (AAS):** Quantifies attention dispersal via normalized Shannon entropy across heads in the final quartile layers:
   $$\text{AAS}_t = \frac{1}{|L| \cdot |H|}\sum_L \sum_h \frac{-\sum_{i=1}^T A_{i*}^{h,L} \log(A_{i*}^{h,L} + \epsilon)}{\log(T)}$$
3. **Entropy-Energy Monitor (EEM):** Combines Shannon uncertainty with Rényi-2 sharpness directly on output logits $z_t$:
   $$\text{EEM}_t = w_e \cdot H_{\text{norm}}(t) + (1 - w_e) \cdot E_{\text{norm}}(t), \quad w_e = 0.6$$
4. **Distribution Shift Tracker (DST):** Tracks temporal drift between consecutive averaged layer representations:
   $$d_t = \frac{1 - \cos(\bar{h}_t, \bar{h}_{t-1})}{2}$$
5. **Multi-Signal Learned Fusion:**
   $$R(t) = \sigma(W^T \hat{X}_t + b), \quad \hat{X}_t = \text{Standardize}([\text{ISP}_t, \text{AAS}_t, \text{EEM}_t, \text{DST}_t])$$

---

## 📂 Repository Structure

```
TRUEGUARD_FINAL/
├── README.md                      # Reproducibility guide and command reference
├── requirements.txt               # Pinned dependencies
├── config/
│   └── config.yaml               # Hyperparameters, layer sets, thresholds
├── src/
│   ├── __init__.py
│   ├── model_loader.py           # Model and tokenizer initialization with hooks
│   ├── signal_extractors.py      # Core ISP, AAS, EEM, DST mathematical logic
│   ├── normalization.py          # Welford online Z-score standardization
│   ├── fusion.py                 # Logistic regression fusion layer & R_seq scoring
│   ├── detector.py               # Token-level generation and guard interception
│   ├── mitigation.py             # Tier 1 Targeted RAG & Tier 2 Calibrated Abstention
│   ├── explainability.py         # Token trust markers and contrastive explanations
│   └── evaluation.py             # AUROC, AUPRC, F1, 95% CIs, confusion matrix
├── experiments/
│   ├── cpu_smoke_test.py         # Standalone CPU verification script (<60s)
│   ├── run_benchmark.py          # 5-fold cross-validation on benchmarks
│   ├── ablation.py               # 5-way ablation experiment (Full vs ablated signals)
│   └── latency_profiler.py       # Latency breakdown and speedup measurement
├── notebooks/
│   └── TRUEGUARD_Colab.ipynb     # Interactive Google Colab workflow (GPU/CPU)
├── tools/
│   ├── build_colab_notebook.py   # Notebook compiler
│   └── generate_figures.py       # Publication figure rendering script (300 DPI)
├── results/                      # Output metric CSVs, JSON records, logs
└── figures/                      # High-resolution publication plots
```

---

## 💻 Environment Setup

### Prerequisites:
- Python 3.9, 3.10, or 3.11
- PyTorch 2.0+ (CPU or CUDA)

```bash
# 1. Clone repository
git clone https://github.com/yogeshravi19/trueguard.git
cd trueguard/TRUEGUARD_FINAL

# 2. Install dependencies
pip install -r requirements.txt
```

---

## 🚀 Reproducibility & Execution Commands (TRUEGUARD v2 — Real Model Pipeline)

### A. Unit & Data-Leakage Verification (<30s on CPU/GPU)
Verifies mathematical equivalence between teacher-forced `score_answer` and cached step-by-step `OnlineSignalMonitor`, checks for zero probe-to-fusion leakage on noise, and tests `ThreeTierController` state transitions:
```bash
python -u tests/test_equivalence.py
```

### B. Download Real Benchmark Datasets
Downloads and verifies `TruthfulQA`, `HaluEval-QA`, `HaluEval-Summarization`, `HaluEval-Dialogue`, and `TriviaQA` into `datasets/` (with provenance recorded in `datasets/manifest.json` and `datasets/DATASET_SOURCES.md`):
```bash
python -u tools/download_datasets.py
```

### C. Step 1 — Extract Real Sensor Features & Hidden States
Runs real forward passes on `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (or `gpt2` / 4-bit 7B models) and caches the 4 sensor features and 4-layer hidden representations:
```bash
python -u experiments/extract_features.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n 400
```

### D. Step 2 — 5-Fold Grouped CV Detection, Ablations, Baselines & Cross-Dataset Transfer
Computes leakage-free 5-fold `GroupKFold` CV with inner out-of-fold probe stacking, single-sensor baselines, leave-one-sensor-out ablations, paired bootstrap CIs, and cross-dataset transfer matrices:
```bash
python -u experiments/evaluate_detection.py --cache results/cache/TinyLlama__TinyLlama-1.1B-Chat-v1.0 --out results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0
```

### E. Step 3 — End-to-End Three-Tier Mitigation on Live TriviaQA Generations
Calibrates $(\tau_{\text{warning}}, \tau_{\text{fault}})$ on 150 calibration questions and evaluates `SAFE` / `TIER1_RESAMPLE` / `TIER2_RETRIEVAL` / `TIER3_ABSTAIN` on 150 unseen test questions:
```bash
python -u experiments/evaluate_mitigation.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n_cal 150 --n_test 150 --out results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/mitigation
```

### F. Step 4 — Real Per-Token Latency Profiling
Measures real per-token decoding latency across `vanilla_decode`, `trueguard_online`, `trueguard_postpass`, and `multi_sample_5x_baseline`:
```bash
python -u experiments/profile_real_latency.py --model TinyLlama/TinyLlama-1.1B-Chat-v1.0 --n_prompts 25 --n_tokens 24 --out results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/real_latency.json
```

---

## ☁️ Google Colab Workflow

For GPU-accelerated reproduction (NVIDIA Tesla T4, L4, or A100):
1. Open Google Colab: [colab.research.google.com](https://colab.research.google.com)
2. Upload `notebooks/TRUEGUARD_Colab_REAL.ipynb` (or `notebooks/TRUEGUARD_Colab.ipynb`)
3. Select GPU Runtime: `Runtime -> Change runtime type -> T4 GPU`
4. Run all cells sequentially (`Runtime -> Run all`) and upload `trueguard_final.zip` in Cell 2

---

## 📊 Verified Empirical Results (`TinyLlama-1.1B-Chat-v1.0` on NVIDIA Tesla T4 GPU)

### 1. In-Distribution Detection Performance (5-Fold Grouped CV, $3{,}196$ Real Answers)
| Benchmark | Pairs ($2N$ rows) | TRUEGUARD Fusion AUROC [95% CI] | ISP (Trained) | AAS | EEM | DST | Best Raw Baseline | F1 | ECE |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Dialogue** | 400 (800) | **0.903** [0.883, 0.922] | 0.904 | 0.618 | 0.668 | 0.634 | `LEN` = 0.687 | 0.820 | 0.034 |
| **HaluEval-QA** | 400 (800) | **0.975** [0.964, 0.987] | 0.977 | 0.512 | 0.850 | 0.859 | `LEN` = 0.953 | 0.955 | 0.024 |
| **HaluEval-Summarization** | 400 (800) | **0.986** [0.980, 0.991] | 0.987 | 0.627 | 0.580 | 0.672 | `EEM_mean` = 0.581 | 0.935 | 0.025 |
| **TruthfulQA** | 398 (796) | **0.876** [0.853, 0.900] | 0.877 | 0.607 | 0.522 | 0.533 | `EEM_max` = 0.523 | 0.817 | 0.042 |
| **4-Benchmark Macro Mean** | **1,598 (3,196)** | **0.935** | **0.936** | **0.591** | **0.655** | **0.675** | --- | **0.882** | **0.031** |

### 2. Leave-One-Sensor-Out Ablation Study
| Benchmark | Full (4 Sensors) | $-\text{ISP}$ (No Hidden Probe) | $-\text{AAS}$ | $-\text{EEM}$ | $-\text{DST}$ | Union Recall @ 10% FPR |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Dialogue** | **0.903** | **0.714** ($-0.188$) | 0.903 ($+0.000$) | 0.903 ($+0.000$) | 0.903 ($-0.000$) | 0.762 |
| **HaluEval-QA** | **0.975** | **0.918** ($-0.057$) | 0.976 ($+0.001$) | 0.976 ($+0.001$) | 0.975 ($+0.000$) | 0.978 |
| **HaluEval-Summarization** | **0.986** | **0.745** ($-0.241$) | 0.986 ($-0.000$) | 0.986 ($+0.000$) | 0.987 ($+0.000$) | 0.960 |
| **TruthfulQA** | **0.876** | **0.626** ($-0.251$) | 0.876 ($-0.001$) | 0.877 ($+0.000$) | 0.877 ($+0.001$) | 0.603 |

### 3. Real Tesla T4 GPU Latency & Speedup (`results/v2/TinyLlama__TinyLlama-1.1B-Chat-v1.0/real_latency.json`)
| Decoding Mode | Measured Latency (ms / token) | Overhead vs. Vanilla | Speedup vs. 5-Sample Consistency |
| :--- | :---: | :---: | :---: |
| **Vanilla KV-Cached Greedy Decode** | $33.49\text{ ms/tok}$ | --- | --- |
| **TRUEGUARD Post-Pass Decode** | **$36.41\text{ ms/tok}$** | **$+2.92\text{ ms/tok}$ ($+8.7\%$)** | **$4.65\times$ faster** ✅ |
| **TRUEGUARD Online Step-by-Step Decode** | **$39.30\text{ ms/tok}$** | **$+5.81\text{ ms/tok}$ ($+17.3\%$)** | **$4.31\times$ faster** ✅ |
| **5-Sample Consistency Baseline** | $169.31\text{ ms/tok}$ | $+135.82\text{ ms/tok}$ ($+405.6\%$) | $1.00\times$ (Baseline) |

### 4. End-to-End Three-Tier Mitigation on Live `TriviaQA` Generations (`n_cal=150`, `n_test=150`)
- **Calibrated Thresholds (from calibration split only):** $\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$
- **Detection AUROC on TinyLlama's Own Open-Ended Generations:** **$0.795$**
- **Unmitigated Hallucination Rate:** $62.0\%$ (accuracy $38.0\%$)
- **Post-Mitigation Hallucination Rate Among Answered Queries:** **$40.0\%$** (**$35.5\%$ relative reduction**; accuracy among answered queries rises from $38.0\% \to \mathbf{60.0\%}$ at $43.3\%$ coverage)
- **System-Wide Emitted Hallucination Rate:** **$17.3\%$** (**$72.0\%$ relative reduction**)
- **Selective-Prediction Area Under Risk–Coverage Curve (AURC, lower is better):** **TRUEGUARD $= 0.412$** vs. Entropy $= 0.526$ and NLL $= 0.603$

---

## 🖥️ Hardware Requirements

| Configuration | Supported Target | Minimum RAM / VRAM | Recommended Models |
| :--- | :--- | :--- | :--- |
| **CPU Smoke Test** | Local PC / Laptop | 8 GB System RAM | `gpt2` |
| **Standard GPU** | Google Colab (Free T4) | 16 GB VRAM | `TinyLlama-1.1B`, `Llama-2-7b-chat` (4-bit) |
| **High-End GPU** | Workstation / L4 / A100 | 24+ GB VRAM | `Llama-2-7b-chat-hf`, `Mistral-7B-Instruct-v0.2` |

---

## 📖 Citation & Contact

If you find TRUEGUARD useful for your research, please cite our IEEE paper:

```bibtex
@article{ravi2026trueguard,
  title={TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models},
  author={Ravi M, Yogesh and Pradeep Kumar, T. S.},
  journal={IEEE Transactions on Artificial Intelligence},
  year={2026}
}
```

**Correspondence:** Yogesh Ravi M (`yogeshravi.m2022@vitstudent.ac.in`), Dr. T. S. Pradeep Kumar (`pradeepkumar.ts@vit.ac.in`).
