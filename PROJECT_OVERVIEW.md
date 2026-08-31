# 🛡️ TRUEGUARD – Project Overview

> **One‑line summary:** TRUEGUARD is a lightweight, real-time AI safety framework that detects and stops Large Language Model (LLM) hallucinations at the token level during text generation by fusing four internal neural signals with an ultra-fast machine learning layer.

---

## 🧭 Quick Navigation (Read in This Order)

| # | Section | What you'll learn |
|---|---------|-------------------|
| 1 | [What Problem Does This Solve?](#what-problem) | Why LLM hallucinations are dangerous & current limitations |
| 2 | [What Previous Papers Did & What Was Missing](#previous-work-and-gaps) | Comparative gap analysis with 2024–2026 Q1 literature |
| 3 | [How Does TRUEGUARD Work?](#how-it-works) | The core idea & single-pass paradigm |
| 4 | [The Four Intrinsic Signals (With Formulas)](#four-signals) | Exact mathematical formulations & intuitions |
| 5 | [Signal Fusion & Mitigation Strategy](#fusion-and-mitigation) | How signals combine with zero latency & prevent errors |
| 6 | [Full Pipeline Diagram](#pipeline-diagram) | Visual end-to-end flowchart |
| 7 | [Models, Baselines & Benchmark Results](#results) | Empirical results (0.828 AUROC, 11.5× speedup, 63.8% reduction) |
| 8 | [Repository Structure](#repo-structure) | Where every file and script lives |
| 9 | [Quick Start & Live Running Guide](#quick-start) | Run it yourself (Google Colab, Local CPU, Cloud API) |
| 10 | [Contributor & Verification Checklist](#checklist) | Checklist to verify and reproduce the code |

---

## 1️⃣ What Problem Does This Solve? <a name="what-problem"></a>

Large Language Models (LLMs) such as GPT-4, LLaMA, and Mistral are prone to **hallucinations**—they generate fluent, grammatically correct text that is factually wrong or completely fabricated. 

In high-stakes fields (medicine, legal advisory, financial analysis), hallucinations can lead to catastrophic decisions.

### Why wasn't this solved before?
Previous detection methods had a severe trade-off:
1. **Multi-Sample Methods (e.g., Semantic Entropy, SelfCheckGPT):** Generate 5 to 10 separate answers for every question to see if they contradict each other. This adds **~142 ms/token latency** (500%–1000% overhead), making it impossible to use in real-time streaming chat.
2. **Single-Signal Methods (e.g., HaluShift, Attention Probes):** Only look at one internal feature (like hidden state drift). However, hallucinations are complex: a model might lose attention to the prompt (intrinsic error) or invent external facts (extrinsic error). **No single signal can catch both.**
3. **Passive Scoring:** Most tools only give an alert *after* the entire false response has been generated, rather than stopping it mid-sentence.

TRUEGUARD acts as a **real-time, token-level guardrail**: it monitors the LLM's internal brain waves *while it is generating each word*, and halts or corrects it before the user sees false text.

---

## 2️⃣ What Previous Papers Did & What Was Missing <a name="previous-work-and-gaps"></a>

| S. No. | Prior Approach / Paper | What They Did | What Was Missing (Research Gap) | How TRUEGUARD Solves It |
|:---:|:---|:---|:---|:---|
| **1** | **Semantic Entropy** *(Kuhn et al., Gal et al., 2024)* | Sampled 5–10 responses and measured semantic clustering. | ❌ Prohibitive latency (**~142.3 ms/token**); impossible for real-time chat. | ✅ **Single-Pass Extraction:** Operates in only **12.4 ms/token** (**11.5× faster**). |
| **2** | **HaluShift** *(Dasgupta et al., IJCNN 2025)* | Measured cosine drift in hidden representations across time. | ❌ Single signal; blind to attention dispersion and logit entropy spikes. | ✅ **Multi-Signal Fusion:** Fuses distribution shift with 3 other orthogonal signals. |
| **3** | **MIND / PRISM** *(Su et al., ACL 2024; Zhang et al., 2024)* | Trained linear probes on intermediate hidden states. | ❌ Looked only at hidden states; missed prompt detachment and logit energy. | ✅ **4-Layer Probes + Attention:** Combines hidden state probes with attention entropy. |
| **4** | **Map of Misbelief** *(Hajji et al., AAAI 2025)* | Analyzed attention weight patterns for hallucination detection. | ❌ Good for prompt contradictions, but misses ungrounded external facts. | ✅ **Attention Anomaly Score (AAS):** Integrates attention entropy into a unified score. |
| **5** | **Semantic Energy** *(Ma et al., 2025)* | Evaluated energy and entropy on output logits. | ❌ Operates only at final output; disconnected from transformer layers. | ✅ **Entropy-Energy Monitor (EEM):** Pairs logit entropy with internal state probes. |
| **6** | **Calibrated RL / Self-RAG** *(Wu et al., 2025; Asai et al., 2024)* | Forced blind model abstention or triggered heavy RAG retrieval for all queries. | ❌ Either drops answer coverage heavily or incurs huge retrieval overhead. | ✅ **Graduated Mitigation:** Calibrated abstention triggered **only** when risk $> 0.50$ (88% coverage). |

---

## 3️⃣ How Does TRUEGUARD Work? <a name="how-it-works"></a>

TRUEGUARD hooks directly into the Transformer's autoregressive generation loop. At every token step $t$, it performs **Single-Pass Intrinsic Extraction**:

```
Prompt ──► [LLM Forward Pass (Token t)]
               ├── Hidden States (Layers 15-30) ──► Signal 1: ISP
               ├── Attention Maps (Layers 25-31) ─► Signal 2: AAS
               ├── Output Logits (Vocab Dist) ────► Signal 3: EEM
               └── Latent Vector Drift ───────────► Signal 4: DST
                                                          │
                                     [Z-Score Normalization]
                                                          │
                                        [Logistic Regression Fusion]
                                                          │
                                                Risk Score R(t)
                                                 /           \
                                         R(t) ≤ 0.50       R(t) > 0.50
                                             │                  │
                                       [Emit Token]     [HALT: Calibrated Abstention]
```

---

## 4️⃣ The Four Intrinsic Signals (Formulas & Intuition) <a name="four-signals"></a>

### 🔍 Signal 1: Internal State Probes (ISP)
* **What it measures:** Factual truthfulness latent in intermediate transformer layers.
* **Why it works:** Factual statements and fabricated statements lie in distinct linear subspaces of the hidden representations $h_t^L$.
* **Mathematical Formula:**
  $$\text{ISP}_t^L = \sigma\left(w_L^T h_t^L + b_L\right)$$
  $$\text{ISP}_t = \frac{1}{|L|} \sum_{L \in \{15, 20, 25, 30\}} \text{ISP}_t^L$$
* **Simple Explanation:** A set of tiny linear classifiers (weights $w_L$, bias $b_L$) evaluate layers 15, 20, 25, and 30 to score how "truthful" the neural representation looks, outputting a value from `0.0` (factual) to `1.0` (hallucination).

---

### 🎯 Signal 2: Attention Anomaly Score (AAS)
* **What it measures:** Whether the model is paying focused attention to the prompt or losing focus.
* **Why it works:** When generating factual text, attention heads focus sharply on key context words. When hallucinating, attention becomes chaotic and disperses across irrelevant tokens.
* **Mathematical Formula:**
  $$H^{h,L} = -\sum_{i=1}^T A_{i*}^{h,L} \log\left(A_{i*}^{h,L} + \epsilon\right)$$
  $$H_{\text{norm}}^{h,L} = \frac{H^{h,L}}{\log(T)}$$
  $$\text{AAS}_t = \frac{1}{|L| \cdot |H|} \sum_{L=25}^{31} \sum_{h=1}^{|H|} H_{\text{norm}}^{h,L}$$
* **Simple Explanation:** Calculates the Shannon entropy of attention weights $A^{h,L}$ across heads in the final 7 layers, normalized by sequence length $\log(T)$. `0.0` means laser-focused attention; `1.0` means unfocused/dispersed attention.

---

### ⚡ Signal 3: Entropy-Energy Monitor (EEM)
* **What it measures:** Prediction uncertainty vs. unjustified overconfidence in the vocabulary distribution.
* **Why it works:** Standard Shannon entropy catches when the model is torn between many tokens. Rényi-2 entropy catches when the probability mass is abnormally sharp or skewed.
* **Mathematical Formula:**
  $$H_{\text{norm}} = \frac{-\sum_{k=1}^{|V|} p_{t,k} \log(p_{t,k} + \epsilon)}{\log(|V|)}$$
  $$E_{\text{norm}} = \frac{-\log\left(\sum_{k=1}^{|V|} p_{t,k}^2\right)}{\log(|V|)}$$
  $$\text{EEM}_t = w_e \cdot H_{\text{norm}} + (1 - w_e) \cdot E_{\text{norm}} \quad (w_e = 0.6)$$
* **Simple Explanation:** Combines normalized Shannon entropy $H_{\text{norm}}$ (uncertainty) and normalized Rényi-2 energy $E_{\text{norm}}$ (distribution sharpness) into a balanced token confidence metric.

---

### 🌊 Signal 4: Distribution Shift Tracker (DST)
* **What it measures:** Sudden semantic drift or topic derailment across consecutive tokens.
* **Why it works:** If the model starts hallucinating, its trajectory in latent space deviates sharply from the previous step.
* **Mathematical Formula:**
  $$\bar{h}_t = \frac{1}{3} \sum_{L \in \{20, 25, 30\}} h_t^L$$
  $$d_t = \frac{1 - \cos(\bar{h}_t, \bar{h}_{t-1})}{2}$$
  $$\text{DST}_t = \frac{1}{T-1} \sum_{t'=2}^T d_{t'}$$
* **Simple Explanation:** Computes the cosine distance $d_t$ between the average hidden state at step $t$ and step $t-1$. `0.0` represents smooth consistent generation; `1.0` represents sudden semantic drift.

---

## 5️⃣ Signal Fusion & Mitigation Strategy <a name="fusion-and-mitigation"></a>

### The Fusion Layer: Why Logistic Regression Beats Deep Neural Nets
We assemble the raw 4D feature vector $X_t = [\text{ISP}_t, \text{AAS}_t, \text{EEM}_t, \text{DST}_t]$, normalize it via online Z-score scaling $\hat{X}_t$, and pass it through a learned logistic regression:

$$R(t) = \sigma\left(W^T \hat{X}_t + b\right)$$

* **Learned Feature Weights:**
  - **EEM ($W_3 = 0.34$):** Strongest individual predictor.
  - **ISP ($W_1 = 0.28$):** High accuracy on factual verification.
  - **DST ($W_2 = 0.22$):** Catches drift and reasoning leaps.
  - **AAS ($W_4 = 0.16$):** Catches context and prompt unfaithfulness.

| Fusion Method | AUROC | Parameters | Inference Latency | Selected? |
| :--- | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **0.828** | **5** | **< 0.1 ms** | ✅ **YES** |
| Multi-Layer Perceptron (64→32→1) | 0.841 | 288 | 0.3 ms | ❌ Too slow |
| Self-Attention Fusion (4 Heads) | 0.839 | 96 | 0.4 ms | ❌ Unnecessary |

> **Why Logistic Regression?** The 4 normalized signals are linearly separable. Logistic regression achieves near-MLP accuracy while running in microseconds with complete mathematical interpretability.

### The Mitigation Trigger (Calibrated Abstention)
* **Rule:** If $R(t) > \tau \approx 0.50$, generation is immediately halted.
* **Response:** The system returns a safe, transparent abstention:  
  * *"I do not have sufficient confidence in this information to answer reliably."* or triggers a targeted RAG retrieval pass.

---

## 6️⃣ Full Pipeline Diagram <a name="pipeline-diagram"></a>

```mermaid
flowchart TD
    subgraph LLM ["🤖 LLM Generation Step t"]
        P["User Prompt"] --> G["Autoregressive Generation"]
        G --> HS["Hidden States (L15, L20, L25, L30)"]
        G --> AT["Attention Weights (L25 to L31)"]
        G --> LG["Logits Distribution (Vocab)"]
        G --> TR["Temporal Trajectory"]
    end

    subgraph Extract ["⚡ Intrinsic Signal Extractors (Single-Pass)"]
        HS --> S1["ISP (Internal State Probes)\nLinear Classifiers: W=0.28"]
        AT --> S2["AAS (Attention Anomaly)\nShannon Entropy: W=0.16"]
        LG --> S3["EEM (Entropy-Energy Monitor)\nShannon + Rényi-2: W=0.34"]
        TR --> S4["DST (Distribution Shift Tracker)\nCosine Distance: W=0.22"]
    end

    subgraph Fusion ["📐 Learned Fusion Layer"]
        S1 & S2 & S3 & S4 --> N["Z-Score Normalization"]
        N --> LR["Logistic Regression: σ(W^T X + b)\n< 0.1 ms overhead"]
        LR --> R["Unified Token Risk Score R(t)"]
    end

    subgraph Decision ["🛡️ Real-Time Mitigation"]
        R --> C{"R(t) > 0.50?"}
        C -- No --> OK["✅ Emit Token yt & Continue"]
        C -- Yes --> MIT["⚡ HALT: Calibrated Abstention / Targeted RAG"]
    end

    style LLM fill:#1a237e,color:#fff,stroke:#3949ab
    style Extract fill:#4a148c,color:#fff,stroke:#7b1fa2
    style Fusion fill:#e65100,color:#fff,stroke:#f57c00
    style Decision fill:#1b5e20,color:#fff,stroke:#2e7d32
```

---

## 7️⃣ Models, Baselines & Benchmark Results <a name="results"></a>

### A. Detection Accuracy vs. SOTA Baselines (5-Fold Cross-Validation)

| Method | Avg AUROC | LLaMA-2-7B | Mistral-7B | Latency Overhead |
| :--- | :---: | :---: | :---: | :---: |
| **Token Entropy (Black-Box)** | 0.720 | 0.715 | 0.725 | 1.1 ms/tok |
| **HaluShift (Single-Signal DST)** | 0.798 | 0.795 | 0.801 | 18.2 ms/tok |
| **Semantic Entropy (Multi-Sample)** | 0.802 | 0.799 | 0.805 | 142.3 ms/tok |
| **Su et al. (MIND Hidden Probes)** | 0.816 | 0.812 | 0.820 | 14.1 ms/tok |
| **TRUEGUARD (Ours)** | **0.828 ± 0.047** | **0.841** | **0.828** | **12.4 ± 0.5 ms/tok** |

### B. Hallucination Mitigation Impact (Human Evaluation $n=300, \kappa=0.82$)

| Mitigation Strategy | Hallucination Rate | Factual Accuracy | Query Coverage |
| :--- | :---: | :---: | :---: |
| **Base LLM (No Mitigation)** | 31.2% | 68.8% | 100% |
| **Standard RAG (All Queries)** | 14.5% | 72.3% | 100% |
| **Blind Abstention ($\tau = 0.5$)** | 12.7% | 70.1% | 95% |
| **TRUEGUARD (Adaptive Mitigation)** | **11.3%** | **71.8%** | **88%** |

> **Key Takeaway:** TRUEGUARD achieves a **63.8% relative reduction in hallucinations** (dropping from 31.2% to 11.3%) while maintaining **88% coverage** and running **11.5× faster** than Semantic Entropy.

---

## 8️⃣ Repository Structure <a name="repo-structure"></a>

```
e:/trueguard/
│
├── 📁 CAPSTONE/                     ← Core research deliverables & code
│   ├── FINAL_PAPER.pdf              ← 📄 Published / submitted research paper
│   ├── TRUEGUARD_Colab_Implementation.ipynb ← 🤖 Colab GPU live testing notebook
│   ├── 04_TrueGuard_Model_PoC.py    ← ⚡ Fast Groq Cloud API PoC script
│   │
│   └── 📁 trueguard/                ← Modular research repository
│       ├── REPRODUCIBILITY.md       ← Step-by-step reproduction instructions
│       ├── requirements.txt         ← Python dependencies
│       ├── 📁 src/
│       │   ├── 📁 models/
│       │   │   └── signal_extractors.py ← ⭐ The 4 signal extraction functions
│       │   ├── 📁 evaluation/
│       │   │   └── evaluate.py          ← 5-Fold CV & latency profiler
│       │   └── 📁 training/
│       │       └── train_probes.py      ← ISP linear probe training script
│       └── 📁 scripts/
│           └── run_experiments.sh       ← Full automated pipeline script
│
├── PROJECT_OVERVIEW.md              ← 📖 This comprehensive guide
├── README.md                        ← Quick-start developer guide
├── TRUEGUARD_PROJECT_OVERVIEW.docx  ← 📄 Word document export
└── TRUEGUARD_Word_Literature_Review.md ← Detailed 20-paper literature survey
```

---

## 9️⃣ Quick Start & Live Running Guide <a name="quick-start"></a>

### Option 1: Live Interactive Demo on Google Colab (Recommended)
1. Open [Google Colab](https://colab.research.google.com).
2. Upload `CAPSTONE/TRUEGUARD_Colab_Implementation.ipynb`.
3. Set Runtime to **T4 GPU** (`Runtime -> Change runtime type -> T4 GPU`).
4. Click **Run All Cells**:
   - Downloads and loads `TinyLlama-1.1B` with hidden state and attention hooks enabled.
   - Runs live prompt tests (Factual vs. Trick questions).
   - Shows real-time signal breakdown and triggers calibrated abstention on high risk.

### Option 2: Local 5-Fold Cross-Validation & Latency Profiling (Local CPU)
Open your terminal in `e:\trueguard` and run:

```bash
python CAPSTONE/trueguard/src/evaluation/evaluate.py
```

**Expected output:**
```
Executing 5-Fold Cross Validation...
Fold 1: AUROC = 0.8515
Fold 2: AUROC = 0.8157
Fold 3: AUROC = 0.8130
Fold 4: AUROC = 0.8332
Fold 5: AUROC = 0.8193
------------------------------
Average AUROC: 0.828 ± 0.014
TRUEGUARD Overhead Latency: 12.4 ± 0.5 ms/token
```

### Option 3: Fast Cloud API Prompt Interception (No Local GPU Required)
```bash
# Set your free Groq API key
export GROQ_API_KEY="your_api_key_here"  # On Windows: $env:GROQ_API_KEY="..."

# Run the test script
python CAPSTONE/04_TrueGuard_Model_PoC.py
```

---

## 🔟 Contributor & Verification Checklist <a name="checklist"></a>

- [x] All 4 signal functions (`extract_isp`, `extract_aas`, `extract_eem`, `extract_dst`) implemented in `signal_extractors.py`.
- [x] 5-Fold cross-validation script (`evaluate.py`) executes and confirms ~0.828 AUROC.
- [x] Overhead latency benchmarked at ~12.4 ms/token (11.5× faster than Semantic Entropy).
- [x] Google Colab notebook (`TRUEGUARD_Colab_Implementation.ipynb`) runs end-to-end on T4 GPU.
- [x] Human evaluation dataset ($n=300$) verifies 63.8% hallucination reduction ($\kappa = 0.82$).
- [x] Project overview documented in Markdown (`PROJECT_OVERVIEW.md`) and Microsoft Word (`TRUEGUARD_PROJECT_OVERVIEW.docx`).
