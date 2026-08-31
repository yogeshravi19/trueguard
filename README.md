# 🛡️ TRUEGUARD – Real-Time LLM Hallucination Detection & Mitigation

> A lightweight, real-time safety guardrail that detects and prevents hallucinations in Large Language Models (LLMs) at the token level by fusing four internal neural signals with a microsecond machine learning layer.

## 📊 Key Results & Baseline Comparison

All models were evaluated across 8 benchmarks (*TruthfulQA, HaluEval, HELM, HumanEval, MATH, MuSiQue*) using 5-Fold Cross-Validation:

| Model / Framework | AUROC Accuracy | Latency Overhead | Hallucination Rate | Query Coverage |
| :--- | :---: | :---: | :---: | :---: |
| **Token Entropy (Black-Box)** | 0.720 ± 0.02 | 1.1 ms/tok | 31.2% | 100% |
| **Semantic Entropy (Multi-Sample)** | 0.802 ± 0.01 | 142.3 ms/tok | 18.5% | 100% |
| **HaluShift (Single-Signal DST)** | 0.798 ± 0.02 | 18.2 ms/tok | 21.0% | 100% |
| **Su et al. (MIND Linear Probes)** | 0.816 ± 0.02 | 14.1 ms/tok | 19.4% | 100% |
| **TRUEGUARD (Ours)** ✅ | **0.828 ± 0.047** | **12.4 ± 0.5 ms/tok** | **11.3%** | **88%** |

> **Conclusion:** TRUEGUARD achieves the highest AUROC (**0.828**) and reduces hallucination occurrences by **63.8%** while operating **11.5× faster** than multi-sampling methods (12.4 ms vs 142.3 ms).

---

## 🛠️ Methodology

The **TRUEGUARD** framework follows a principled, single-pass intrinsic monitoring pipeline:

1. **Single-Pass Feature Extraction:**
   - At each generation step $t$, intercepts the transformer's forward pass to extract 4 complementary signals without launching secondary generation passes:
     - **ISP (Internal State Probes):** Linear probes on layers $\{15, 20, 25, 30\}$ evaluating latent truthfulness.
     - **AAS (Attention Anomaly Score):** Normalized Shannon entropy of attention heads in final layers $\{25 \dots 31\}$.
     - **EEM (Entropy-Energy Monitor):** Blended Shannon uncertainty and Rényi-2 confidence energy from logits.
     - **DST (Distribution Shift Tracker):** Cosine distance tracking semantic drift between consecutive hidden states.

2. **Online Z-Score Normalization & Fusion:**
   - Normalizes the 4D feature vector and passes it to a learned logistic regression:
     $$R(t) = \sigma\left(W^T \hat{X}_t + b\right) \quad (\text{Overhead } < 0.1\text{ ms})$$
   - Learned signal weights: **EEM (0.34)**, **ISP (0.28)**, **DST (0.22)**, **AAS (0.16)**.

3. **Active Mitigation & Calibrated Abstention:**
   - When token risk $R(t) > \tau \approx 0.50$, generation is immediately halted to prevent error propagation.
   - The system triggers epistemic abstention (*"I don't have enough confident information..."*) or invokes targeted RAG.

---

## 📋 Requirements

| Requirement | Version | Notes |
| :--- | :--- | :--- |
| **Python** | 3.9 or higher | Standard Python installation |
| **PyTorch** | 2.0+ | GPU required for real-time model inference; CPU works for evaluation |
| **Transformers** | 4.35+ | HuggingFace library for model weights |
| **scikit-learn** | 1.0+ | For logistic regression fusion and cross-validation |

### Quick Package Installation:
```bash
pip install torch transformers scikit-learn numpy scipy requests
```

---

## 🚀 How to Run the Code

### 1. Live Interactive Model Run (Google Colab GPU - Recommended)
Open the notebook in Google Colab with a free T4 GPU:
* **Notebook:** [`CAPSTONE/TRUEGUARD_Colab_Implementation.ipynb`](file:///e:/trueguard/CAPSTONE/TRUEGUARD_Colab_Implementation.ipynb)
* **What it does:** Loads `TinyLlama-1.1B` with hidden state & attention hooks, extracts signals token-by-token, and intercepts hallucinations live.

### 2. Local 5-Fold Cross-Validation & Latency Profiling (Local CPU)
Run the automated evaluation harness directly in your terminal:
```bash
python CAPSTONE/trueguard/src/evaluation/evaluate.py
```
* **Output:** Executes 5-fold CV of the fusion layer and calculates extraction latency per token.

### 3. Fast Cloud API Prompt Interception PoC (Zero GPU Needed)
```bash
# On Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key"
python CAPSTONE/04_TrueGuard_Model_PoC.py
```

---

## 📁 Repository Structure

```
trueguard/
├── 📁 CAPSTONE/                     ← Core deliverables
│   ├── FINAL_PAPER.pdf              ← 📄 Full publication paper
│   ├── TRUEGUARD_Colab_Implementation.ipynb ← 🤖 Colab GPU live testing notebook
│   ├── 04_TrueGuard_Model_PoC.py    ← ⚡ Fast Groq Cloud API PoC script
│   └── 📁 trueguard/                ← Modular codebase
│       ├── 📁 src/models/           ← signal_extractors.py (The 4 signals)
│       ├── 📁 src/evaluation/       ← evaluate.py (5-Fold CV & latency)
│       └── 📁 src/training/         ← train_probes.py (ISP probe training)
│
├── PROJECT_OVERVIEW.md              ← 📖 Comprehensive guide with all formulas & theory
├── README.md                        ← Quick start & developer overview
├── TRUEGUARD_PROJECT_OVERVIEW.docx  ← 📄 Formatted Word report
└── TRUEGUARD_Word_Literature_Review.md ← 20-paper literature survey
```

---

## 📖 Full Documentation

See **[PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** for:
- Detailed breakdown of previous papers vs. TRUEGUARD
- Complete mathematical derivations and variable definitions for all 4 signals
- In-depth ablation studies and human evaluation statistics ($n=300, \kappa=0.82$)
- Step-by-step reproduction and verification checklist
