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

## 🚀 Reproducibility & Execution Commands

### A. Fast CPU Smoke Test (<60s)
Validates the entire pipeline end-to-end on CPU (model loading, token generation, 4-signal extraction, normalization, risk scoring, mitigation, and metric calculation):
```bash
python experiments/cpu_smoke_test.py
```
*Expected Output: `[SUCCESS] All CPU smoke tests PASSED! Output logged to results/smoke_test_results.json`*

### B. Multi-Benchmark Evaluation (5-Fold CV)
Executes 5-fold cross-validation across TruthfulQA, HaluEval (QA, Summ, Dial), and HELM:
```bash
python experiments/run_benchmark.py
```
*Outputs generated: `results/benchmark_results.json` and `results/metrics.csv`*

### C. Signal Ablation Study
Measures the individual contribution of each intrinsic signal:
```bash
python experiments/ablation.py
```
*Outputs generated: `results/ablation_results.json`*

### D. Latency & Speedup Profiling
Profiles per-token overhead across warm-up and timed iterations:
```bash
python experiments/latency_profiler.py
```
*Outputs generated: `results/latency_results.json` and `results/latency.log`*

### E. Publication Figure Generation
Renders all 6 figures at 300 DPI into `figures/`:
```bash
python tools/generate_figures.py
```

---

## ☁️ Google Colab Workflow

For GPU-accelerated reproduction (T4, L4, or A100):
1. Open Google Colab: [colab.research.google.com](https://colab.research.google.com)
2. Upload `notebooks/TRUEGUARD_Colab.ipynb`
3. Select GPU Runtime: `Runtime -> Change runtime type -> T4 GPU`
4. Run all cells sequentially (`Runtime -> Run all`)

---

## 📊 Empirical Results Summary

### 1. Benchmark Detection Performance (5-Fold CV)
| Benchmark | AUROC | 95% Confidence Interval | AUPRC | F1 Score |
| :--- | :---: | :---: | :---: | :---: |
| **TruthfulQA** | **0.8533** | [0.8066, 0.9001] | 0.8140 | 0.7186 |
| **HaluEval-QA** | **0.8840** | [0.8678, 0.9003] | 0.8739 | 0.7874 |
| **HaluEval-Summ** | **0.8797** | [0.8411, 0.9184] | 0.8459 | 0.7252 |
| **HaluEval-Dial** | **0.8872** | [0.8533, 0.9212] | 0.8484 | 0.7373 |
| **HELM** | **0.9063** | [0.8665, 0.9461] | 0.8552 | 0.7545 |
| **Overall Average** | **0.8821 ± 0.0170** | --- | **0.8475** | **0.7446** |

### 2. Signal Ablation Study
| Configuration | AUROC | $\Delta$ from Full | Key Takeaway |
| :--- | :---: | :---: | :--- |
| **Full TRUEGUARD (4 Signals)** | **0.8475 ± 0.0324** | **Reference** | **Optimal multi-signal synergy** |
| $- \text{EEM}$ (Without Entropy/Energy) | 0.7957 ± 0.0316 | $-0.0518$ | Largest single-signal performance drop |
| $- \text{ISP}$ (Without Hidden Probes) | 0.8093 ± 0.0465 | $-0.0382$ | Hidden states contain critical factual cues |
| $- \text{DST}$ (Without Dist. Shift) | 0.8320 ± 0.0237 | $-0.0155$ | Prevents temporal cognitive drift |
| $- \text{AAS}$ (Without Attention Anomaly) | 0.8370 ± 0.0395 | $-0.0105$ | Attention focus catches context detachment |

### 3. Inference Latency & Speedup
| Method | Passes per Token | Overhead Latency | Speedup vs Semantic Entropy |
| :--- | :---: | :---: | :---: |
| **Semantic Entropy** | 5 to 10 | $142.3 \pm 3.8\text{ ms}$ | $1.0\times$ (Baseline) |
| **HaluShift (DST Only)** | 1 | $18.2 \pm 0.6\text{ ms}$ | $7.8\times$ faster |
| **TRUEGUARD (4 Signals)** | **1** | **$12.4 \pm 0.5\text{ ms}$** | **$11.5\times$ faster** ✅ |

### 4. Closed-Loop Mitigation Impact ($n=300, \kappa=0.82$)
- **Base LLM Hallucination Rate:** $31.2\%$
- **TRUEGUARD Protected Hallucination Rate:** $11.3\%$
- **Relative Hallucination Reduction:** **$63.8\%$**
- **Query Answer Coverage:** **$88.0\%$** (only $12.0\%$ abstentions)

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
