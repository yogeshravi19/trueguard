# TRUEGUARD — Architecture Verification & Implementation Report

**Repository:** `E:\trueguard\CAPSTONE\FInal`  
**Reference Manuscript:** `E:\trueguard\CAPSTONE\Toward Trustworthy Large Language Models_standard.docx` (Section 6)  
**Target:** Second research paper (Implementation & Empirical Evaluation of TRUEGUARD)

---

## 1. Audit of the Original Repository vs. the Review Paper

| Component in Review Paper (Section 6) | Original Repository (`src/`, `experiments/`) | Status Before Refactor | Action Taken in TRUEGUARD v2 |
|---|---|---|---|
| **Sensor 1 — Internal State Probe (ISP)** (§6.1): supervised probes attached to middle-to-late hidden layers | `src/signal_extractors.py`: when `probes=None` (which was always the case), fell back to `sigmoid(std(h) - 1.0)` — an untrained hidden-state dispersion proxy | **Incomplete (proxy only)** | Implemented supervised per-layer `LogisticRegression` probes trained on real hidden states at depth fractions $(0.45, 0.60, 0.75, 0.90)$ with grouped inner CV for $C$ and inner out-of-fold stacking (`src/tg_pipeline.py`, `TrueGuardDetector`) |
| **Sensor 2 — Attention Anomaly Score (AAS)** (§6.1): normalised Shannon entropy across deep attention heads | Implemented in `src/signal_extractors.py`, but model loader did not force `attn_implementation="eager"` (SDPA drops attention weights in newer Transformers) | **Partially working** | Enforced `attn_implementation="eager"` in `load_model` and implemented both teacher-forced (`signals_from_forward`) and cached step-by-step (`OnlineSignalMonitor`) extraction |
| **Sensor 3 — Entropy-Energy Monitor (EEM)** (§6.1): $w_e H_{\text{Shannon,norm}} + (1-w_e) H_{\text{Rényi-2,norm}}$ on output logits | Implemented in `src/signal_extractors.py` | **Working** | Preserved exact formula ($w_e=0.6$) in both teacher-forced and online modes |
| **Sensor 4 — Distribution Shift Tracker (DST)** (§6.1): $(1 - \cos(\bar h_t, \bar h_{t-1}))/2$ on layer-averaged hidden states | Implemented in `src/signal_extractors.py` | **Working** | Preserved exact formula at depth fractions $(0.60, 0.75, 0.90)$ |
| **Multi-signal Fusion** (§6.2): adaptive weighting producing risk $\in [0,1]$ | `src/fusion.py`: hardcoded default weights `[0.28, 0.16, 0.34, 0.22]` | **Hardcoded weights** | Learned `StandardScaler + LogisticRegression` trained on `[logit(ISP_oof), AAS_mean, AAS_max, EEM_mean, EEM_max, DST_mean, DST_max]` |
| **Two Calibrated Thresholds** ($\tau_{\text{warning}}, \tau_{\text{fault}}$) & **Three Operating Regimes** (§6.3) | Single hardcoded `risk_threshold = 0.50` | **Missing warning threshold** | Implemented `calibrate_thresholds(y_val, risk_val)`: $\tau_{\text{warning}}$ = Youden-optimal point; $\tau_{\text{fault}} = \max(\text{threshold at FPR}\le 10\%, \tau_{\text{warning}})$ (`src/tg_eval.py`) |
| **Three-Tier Closed-Loop Corrective Actions** (§6.4): Tier 1 local re-sampling, Tier 2 targeted retrieval, Tier 3 calibrated abstention | `src/mitigation.py`: only 2 tiers (RAG and abstention); Tier 1 re-sampling was absent | **Missing Tier 1** | Implemented all 3 tiers (`SAFE`, `TIER1_RESAMPLE`, `TIER2_RETRIEVAL`, `TIER3_ABSTAIN`) with automatic escalation in `src/tg_controller.py` |
| **Explainability** (§6.5): sensor attribution | `src/explainability.py`: static comparison against 0.50 | **Heuristic** | Added `TrueGuardDetector.explain(F, H)` returning the exact signed log-odds contribution of each sensor (`ISP`, `AAS`, `EEM`, `DST`) from the fitted logistic model |
| **Benchmark Evaluation** (`experiments/run_benchmark.py`) | Generated synthetic features via `rng.normal(...)`; never loaded a model or dataset | **Simulated** | Replaced by `experiments/extract_features.py` + `experiments/evaluate_detection.py` using real datasets (`datasets/*.jsonl`) and real LLM forward passes |
| **Latency Profiler** (`experiments/latency_profiler.py`) | Timed random tensors without an LLM forward pass | **Simulated** | Replaced by `experiments/profile_real_latency.py` timing actual decoding (`vanilla`, `trueguard_online`, `trueguard_postpass`, `multi_sample_5x`) |

---

## 2. Documented Technical Adjustments (Where Exact Paper Wording Needed a Scientifically Valid Realisation)

1. **Answer-level aggregation of token signals:** Public benchmarks (HaluEval, TruthfulQA, TriviaQA) provide ground-truth labels per **answer**, not per token. Therefore, per-token signals are aggregated over the answer tokens via `(mean, max)` for AAS, EEM, and DST, and via the **mean hidden state** across answer tokens for each ISP layer.
2. **Tier 1 re-sampling granularity:** Section 6.4 describes rolling back a few tokens and re-sampling. Because short factual answers are only 10–25 tokens long and the detector is calibrated on complete answers, `ThreeTierController` draws $K=4$ temperature-sampled candidate answers ($T=0.7, p=0.9$), scores each candidate with the full 4-sensor detector, and accepts the lowest-risk candidate if its risk drops below $\tau_{\text{warning}}$ (otherwise escalating to Tier 2 retrieval).
3. **Two mathematically equivalent extraction modes:**
   - **Teacher-forced single pass (`score_answer`)** is used when scoring benchmark answer pairs and candidate answers (1 forward pass per answer instead of $T$ passes).
   - **Cached token-by-token (`OnlineSignalMonitor`)** is used during real-time step-by-step decoding and latency profiling.
   - `tests/test_equivalence.py` proves that both paths return identical features within floating-point precision ($\max|\Delta F| = 3.5\times 10^{-6}$, $\max|\Delta H| = 1.5\times 10^{-5}$ on GPT-2).

---

## 3. Data-Leakage Prevention Checklist

1. **Question-level grouping (`GroupKFold`):** In paired datasets (`halueval_qa`, `halueval_dialogue`, `halueval_summarization`, `truthful_qa`), each question produces one grounded answer (`label=0`) and one hallucinated answer (`label=1`) sharing a `group` ID. All CV splits use `GroupKFold`, so the two answers of a question are never split across train and test.
2. **Probe-to-fusion stacking without leakage:** A high-dimensional linear probe ($d \in [768, 4096]$) has much higher in-sample than out-of-sample accuracy. If the fusion layer were trained on in-sample probe probabilities, it would assign nearly 100% weight to ISP and ignore AAS, EEM, and DST. `TrueGuardDetector.fit` computes **inner 5-fold out-of-fold probe probabilities** on the training split and fits the fusion logistic regression on those out-of-fold scores.
3. **Hyperparameter isolation:** The probe regularisation strength $C \in \{0.001, 0.01, 0.1\}$ is selected by inner grouped CV inside each training fold only.
4. **Threshold isolation:** $(\tau_{\text{warning}}, \tau_{\text{fault}})$ are calibrated on training/validation risk scores only and applied unchanged to test folds, cross-dataset targets, and the TriviaQA mitigation test split.

---

## 4. Local Verification Completed vs. Awaiting Google Colab GPU Execution

### Verified locally on CPU (`E:\trueguard\CAPSTONE\FInal`)
- `tests/test_equivalence.py` — **PASSED**:
  - Teacher-forced vs. online cached signal equivalence ($\max|\Delta F| = 3.49\times 10^{-6}$, $\max|\Delta H| = 1.53\times 10^{-5}$).
  - Pure-noise leakage check ($4\times 256$ random hidden states $\to$ out-of-fold AUROC near chance, confirming no probe-to-fusion leakage).
  - `ThreeTierController` state transitions across `SAFE`, `TIER2_RETRIEVAL`, and `TIER3_ABSTAIN`.
- All 5 benchmark datasets downloaded and verified in `datasets/` (`manifest.json`, `DATASET_SOURCES.md`).
- End-to-end execution of `extract_features.py` $\to$ `evaluate_detection.py` verified locally on `gpt2` (`results/v2/gpt2/`).

### Awaiting your execution in Google Colab (T4 GPU)
- Full feature extraction and 5-fold grouped CV with `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (and optionally a 4-bit 7B model such as `mistralai/Mistral-7B-Instruct-v0.2`) across `halueval_qa`, `halueval_dialogue`, `halueval_summarization`, and `truthful_qa` ($N=400$ questions / $800$ answers per dataset).
- End-to-end TriviaQA before-and-after mitigation evaluation (`evaluate_mitigation.py`, 150 calibration + 150 test questions with live Wikipedia retrieval).
- GPU latency profiling (`profile_real_latency.py`).

