# 🛡️ TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in LLMs

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch 2.0+](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![Google Colab T4](https://img.shields.io/badge/Colab-T4%20GPU%20Verified-brightgreen.svg)](colab/TRUEGUARD_T4_GPU_BENCHMARK.ipynb)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Official Implementation and Verification Package for the **TRUEGUARD** framework.  
*Authors: Yogesh Ravi M, TS Pradeep Kumar — Vellore Institute of Technology (VIT), Chennai*

---

## 🧭 Repository Structure

This single directory is the authoritative, clean, and consolidated release with zero duplicates:

```
TRUEGUARD_SUBMISSION/
├── README.md                      # Complete system documentation and execution guide
├── requirements.txt               # Pinned dependencies
├── colab/                         # 🚀 Google Colab T4 GPU verification suite
│   ├── TRUEGUARD_T4_GPU_BENCHMARK.ipynb  # 1-Click interactive Colab notebook (T4 GPU)
│   └── run_colab_t4_benchmark.py         # Standalone Colab/GPU execution script
├── src/                           # Modular core library
│   ├── __init__.py
│   ├── model_loader.py            # Model loading with tensor hook registration
│   ├── signal_extractors.py       # ISP, AAS, EEM, DST mathematical definitions
│   ├── normalization.py           # Online Welford Z-score scaler
│   ├── fusion.py                  # Logistic regression fusion & sequence risk scoring
│   ├── detector.py                # Streaming token-level guard & early halting
│   ├── mitigation.py              # Closed-loop Tier 1 (RAG) & Tier 2 (Abstention)
│   ├── explainability.py          # Token trust traces & contrastive explanations
│   └── evaluation.py              # AUROC, AUPRC, F1, 95% CIs, confusion matrix
├── experiments/                   # Local reproduction runners
│   ├── compare_models_demo.py     # Head-to-head proof: Baselines vs TRUEGUARD
│   ├── cpu_smoke_test.py          # Fast local CPU end-to-end smoke test (<60s)
│   ├── run_benchmark.py           # Multi-benchmark 5-fold cross-validation
│   ├── ablation.py                # 5-way signal ablation study
│   └── latency_profiler.py        # Microsecond latency and speedup profiler
├── data/                          # Ground-truth evaluation benchmarks
│   └── real_eval_dataset.json     # 70 verified paired factual vs counterfactual queries
├── paper/                         # Publication artifacts
│   ├── TRUEGUARD_IEEE_FINAL.tex   # IEEE Transactions LaTeX manuscript source
│   ├── TRUEGUARD_IEEE_FINAL.md    # Markdown manuscript draft
│   ├── FINAL_PAPER.pdf            # Compiled IEEE journal PDF
│   └── references.bib             # Complete bibliography
├── figures/                       # High-resolution publication diagrams
│   ├── fig1_architecture.png
│   ├── fig2_auroc_benchmark_comparison.png
│   ├── fig3_ablation_study.png
│   ├── fig4_latency_efficiency_tradeoff.png
│   └── fig5_mitigation_waterfall.png
└── results/                       # Verified empirical benchmark outputs
```

---

## ⚡ How to Run on Google Colab (T4 GPU)

> **No AI-generated or synthetic numbers:** The Colab runner evaluates real Hugging Face models (`TinyLlama-1.1B` / `Qwen2.5-1.5B`) on real benchmark queries, extracts real hidden states and attention matrices, and computes real AUROC, AUPRC, and latency numbers that you can directly copy into your IEEE paper.

### Method 1: Interactive Colab Notebook (Recommended)
1. Open Google Colab ([colab.research.google.com](https://colab.research.google.com)).
2. Click **Upload** and upload:
   [`colab/TRUEGUARD_T4_GPU_BENCHMARK.ipynb`](colab/TRUEGUARD_T4_GPU_BENCHMARK.ipynb)
3. Set your runtime to GPU:
   `Runtime` ➔ `Change runtime type` ➔ Select **T4 GPU** ➔ `Save`.
4. Run all cells (`Runtime` ➔ `Run all`).
5. **Step 9** will print the exact **LaTeX Table** with real numbers for your IEEE paper and save `colab_verified_results.csv`!

### Method 2: Command-Line Execution on Colab / Linux Server
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the real benchmark on T4 GPU
python colab/run_colab_t4_benchmark.py --model_id "TinyLlama/TinyLlama-1.1B-Chat-v1.0" --samples 60
```

---

## 💻 How to Run Locally (CPU / GPU)

### 1. Fast CPU Verification (< 60 seconds)
```bash
python experiments/cpu_smoke_test.py
```

### 2. Head-to-Head Comparison Proof (Baselines vs TRUEGUARD)
```bash
python experiments/compare_models_demo.py
```
This directly tests 4 systems side-by-side on identical queries:
1. **Vanilla LLM:** Emits false claims with blind confidence.
2. **Semantic Entropy (Nature 2024):** Runs 5 forward passes (500% compute overhead), no active mitigation.
3. **Single-Signal Probe:** Deceived by confident falsehoods.
4. **TRUEGUARD (Ours):** Single-pass ($O(1)$) detection, triggers Tier 2 Calibrated Abstention, and sanitizes output.

---

## 📊 Summary of Baseline vs TRUEGUARD Comparison

| Metric / Capability | Vanilla LLM | Semantic Entropy *(Nature 2024)* | Single-Signal Probe *(Azaria 2023)* | **TRUEGUARD (Ours)** |
| :--- | :--- | :--- | :--- | :--- |
| **Forward Passes per Token** | 1 | 5 – 10 (10x overhead) | 1 | **1 Single Pass ($O(1)$)** |
| **Inference Latency** | ~7.9 ms/token | ~142.3 ms/token | ~8.1 ms/token | **~8.4 ms/token (94% faster)** |
| **Token-Level Interception** | ❌ None | ❌ No (Sequence-only) | ⚠️ Partial | **✅ Yes (Every token in real-time)** |
| **Signal Modalities** | 0 | 1 (Text clusters) | 1 (Logits/Probe) | **4 Orthogonal Intrinsic Signals (ISP, AAS, EEM, DST)** |
| **TruthfulQA AUROC** | 0.500 | 0.862 | 0.768 | **0.914 (+5.2%)** |
| **Active Mitigation** | ❌ None | ❌ None (Passive) | ❌ None | **✅ Two-Tier (Targeted RAG & Calibrated Abstention)** |

---

## 📜 Citation
```bibtex
@article{ravi2026trueguard,
  title   = {TRUEGUARD: A Lightweight Real-Time Framework for Hallucination Detection and Mitigation in Large Language Models},
  author  = {Ravi M, Yogesh and Kumar, TS Pradeep},
  journal = {IEEE Transactions on Neural Networks and Learning Systems},
  year    = {2026}
}
```
