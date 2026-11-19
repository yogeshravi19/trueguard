# TRUEGUARD — Final Publication-Readiness & Research-Integrity Audit Report

**Target Venue:** IEEE Access  
**Foundation Model:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (100% frozen, `attn_implementation="eager"`, `trainable_params = 0`)  
**Audit Date:** 2026-11-19  
**Audit Directory:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\publication_audit\`  
**Final Verdict:** **READY FOR MANUSCRIPT PREPARATION** *(0 unresolved blockers; 5 explicit methodological disclosures required in manuscript text)*

---

## 1. Programmatic Integrity Verification (Task 1 & Task 2)

| Verification Dimension | Check Result | Supporting Evidence |
| :--- | :---: | :--- |
| **Original Sensor Formula Fidelity** | **PASS** | Byte-identical SHA-256 match between `CAPSTONE/FInal/src/` and Colab-executed embedded modules: `tg_pipeline.py` (`a9c08ea0df69c145`), `tg_controller.py` (`c094c8cbbe632b3b`), `tg_eval.py` (`b65ac0291b8b111b`). |
| **Colab Pipeline Completion** | **PASS** | All 8 pipeline stages `COMPLETED` on CUDA GPU (`85.1 min` total runtime; `32,590` real extracted sequences across 11 checkpoints; 0 NaNs, 0 Infs). |
| **Metric Re-Verification** | **PASS** | Recomputed AUROC, AUPRC, F1, Precision, Recall, Accuracy, ECE, and Brier from all saved `.npz` prediction files match `final_experiment_report.json` to **`1.11e-16`**. |
| **Grouped CV & Zero Leakage** | **PASS** | In-domain 5-fold `GroupKFold` keeps all pairs/questions/documents/dialogs disjoint across folds; ISP inner-OOF `C` selection, scalers, fusion weights, and thresholds fit strictly on training folds. |
| **TriviaQA Disjoint Splits** | **PASS** | `n_cal = 250` and `n_test = 250` verified 100% disjoint (`disjoint_verified = True`). |
| **Few-Shot Adaptation Splits** | **PASS** | `GroupShuffleSplit(test_size=0.40, random_state=2026)` verified **`group_overlap = 0`** on all 4 target datasets (`faithdial`, `wikibio_gpt3`, `fever`, `xsum_factuality`); zero-shot and adapted detectors evaluated on identical test rows; scalers/probes/fusion/thresholds fit strictly on $K$ adaptation examples across 10 fixed seeds with Holm-Bonferroni correction. |
| **FEVER Separation** | **PASS** | Strictly categorized and reported separately as **claim-verification / truthfulness transfer**, never as model-generated hallucination. |
| **Latency Arithmetic** | **PASS** | Exact match verified directly from raw CUDA `ms/token` timings (`real_latency.json`). |

> **Mandatory Scientific Disclosure (Task 2):** Because the 4 held-out datasets (`faithdial`, `wikibio_gpt3`, `fever`, `xsum_factuality`) were examined during zero-shot failure diagnosis prior to running the few-shot adaptation study, the 40% group-disjoint test splits validate few-shot target adaptation on unseen test groups within those benchmarks, **not** as a completely unexamined external confirmation set. This must be stated explicitly in the manuscript.

---

## 2. Verified 10-Dataset Suite & Sample Counts

| # | Dataset | Evaluation Protocol | Raw Rows | Usable Rows | Groups | Class 0 / Class 1 | Exclusions |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
| **1** | `halueval_dialogue` | In-Domain 5-Fold Group CV + Pool | 10,000 pairs | 4,000 (2,000 pairs) | 2,000 | 2,000 / 2,000 | Computational cap (5× orig.) |
| **2** | `halueval_qa` | In-Domain 5-Fold Group CV + Pool | 10,000 pairs | 4,000 (2,000 pairs) | 2,000 | 2,000 / 2,000 | Computational cap (5× orig.) |
| **3** | `halueval_summarization` | In-Domain 5-Fold Group CV + Pool | 10,000 pairs | 4,000 (2,000 pairs) | 2,000 | 2,000 / 2,000 | Computational cap (5× orig.) |
| **4** | `truthful_qa` | In-Domain 5-Fold Group CV + Pool | 817 pairs | 1,634 (100%) | 817 | 817 / 817 | 0 |
| **5** | `halueval_general` | In-Domain 5-Fold Group CV + Pool | 4,507 | 4,507 (100%) | 4,507 | 3,692 / 815 | 0 (18.1% natural prev.) |
| **6** | `faithdial` | Unseen Zero-Shot + Few-Shot Adapt. | 3,539 | 3,507 (100% grounded) | 791 dialogs | 946 / 2,561 | 32 Generic-only turns |
| **7** | `wikibio_gpt3` | Unseen Zero-Shot + Few-Shot Adapt. | 1,908 sent. | 1,908 (100%) | 238 articles | 516 / 1,392 | 0 |
| **8** | `xsum_factuality` | Unseen Zero-Shot + Few-Shot Adapt. | 5,597 ratings | 1,868 (100% consensus) | 498 articles | 185 / 1,683 | 1 tie vote; 0 missing BBC docs |
| **9** | `fever` | **Claim-Verification Transfer** (Separate) | 18,999 | 6,666 (100% unique) | 6,666 claims | 3,333 / 3,333 | NEI + duplicate evidence rows |
| **10** | `trivia_qa` | Closed-Book Mitigation | 17,944 | 250 cal + 250 test | 500 | Dynamic (66.0% test wrong) | 0 |

---

## 3. Verified Core Experimental Results

### 3.1 In-Domain 5-Fold Group-Preserving CV (18,141 sequences)
| Dataset | Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | w/o ISP | AUPRC | F1 | ECE | Brier |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Dialogue** | **0.9218** [0.915, 0.929] | 0.9221 | 0.6441 | 0.6704 | 0.6153 | 0.7249 | 0.9305 | 0.8351 | 0.0220 | 0.1117 |
| **HaluEval-QA** | **0.9880** [0.984, 0.991] | 0.9880 | 0.5243 | 0.8542 | 0.8568 | 0.9296 | 0.9914 | 0.9679 | 0.0095 | 0.0265 |
| **HaluEval-Summ.** | **0.9936** [0.992, 0.995] | 0.9936 | 0.6048 | 0.5859 | 0.6602 | 0.7233 | 0.9938 | 0.9624 | 0.0099 | 0.0293 |
| **TruthfulQA** | **0.8773** [0.861, 0.894] | 0.8772 | 0.5910 | 0.5313 | 0.5284 | 0.6073 | 0.8575 | 0.8024 | 0.0251 | 0.1404 |
| **HaluEval-General** | **0.7204** [0.702, 0.740] | 0.7225 | 0.6194 | 0.5404 | 0.5365 | 0.6226 | 0.3868 | 0.4255 | 0.0055 | 0.1319 |

### 3.2 Zero-Shot Transfer vs. Few-Shot Target-Domain Adaptation (Group-Disjoint 40% Test, 10 Seeds)
| Target Benchmark | Zero-Shot Unadapted | Raw EEM (Unsup.) | $K=50$ Fusion | $K=100$ Fusion | $K=250$ Fusion | $K=250$ ISP Only | $K=250$ vs. Unad. ($p_{\text{Holm}}$) | $K=250$ ECE (Unad.) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **FaithDial** ($n=1396$) | 0.4881 | 0.7473 | 0.6987 ± 0.088 | 0.7899 ± 0.031 | **0.8231 ± 0.012** | 0.8320 ± 0.010 | **+0.3350** ($<10^{-6}$) | **0.044** (0.657) |
| **WikiBio-GPT3** ($n=734$) | 0.4868 | 0.5223 | 0.5088 ± 0.056 | 0.4939 ± 0.084 | **0.6698 ± 0.038** | 0.6842 ± 0.031 | **+0.1830** ($3\times 10^{-6}$) | **0.074** (0.434) |
| **XSum Factuality** ($n=752$) | 0.4678 | 0.6352 | 0.5401 ± 0.069 | 0.6058 ± 0.043 | **0.6456 ± 0.041** | 0.6175 ± 0.103 | **+0.1778** ($7\times 10^{-6}$) | **0.038** (0.563) |
| **FEVER** *(Claim-Verif., $n=2667$)* | 0.5209 | 0.5439 | 0.5394 ± 0.048 | 0.6195 ± 0.040 | **0.7325 ± 0.014** | 0.7437 ± 0.012 | **+0.2115** ($<10^{-6}$) | **0.043** (0.342) |

### 3.3 TriviaQA Closed-Book Mitigation & Matched-Coverage Selective Prediction ($n_{\text{cal}}=250$, $n_{\text{test}}=250$)
- **Baseline (Unmitigated):** Accuracy = `34.0%`, Hallucination Rate = `66.0%`.
- **Three-Tier Controller (`tau_warning=0.597`, `tau_fault=0.842`):** Coverage = `46.0%` (`115/250`), Abstention = `54.0%` (`135/250`: `112` true hallucinations blocked [`67.9%` of hallucinations; `83.0%` precision] + `23` correct answers dropped [`27.1%` of correct]), Answered Accuracy = `54.8%` (`45.2%` hallucination among answered; `20.8%` system-wide hallucination = **`68.5%` relative system-wide drop**). Active repairs: `2` via Tier 1 resample (`23` triggered) + `2` via Tier 2 Wikipedia retrieval (`11` triggered).
- **Matched-Coverage Selective Prediction (46% Coverage / AURC):**
  - **TRUEGUARD 4-Sensor:** `AUROC = 0.7876`, `AURC = 0.4360 [0.360, 0.524]`, `Acc@46% = 55.7%`
  - **ISP Only:** `AUROC = 0.7706`, `AURC = 0.4473` ($\Delta = -0.0113$, $p = 0.225$, n.s.)
  - **Scalars Only:** `AUROC = 0.7130`, `AURC = 0.4891` ($\Delta = -0.0531$, $p < 0.0001$)
  - **Entropy Baseline:** `AUROC = 0.6583`, `AURC = 0.5309` ($\Delta = -0.0949$, $p < 0.0001$)
  - **NLL Baseline:** `AUROC = 0.4678`, `AURC = 0.6843` ($\Delta = -0.2483$, $p < 0.0001$)

### 3.4 Genuine CUDA Per-Token Latency Profiling (`25 prompts × 24 tokens`)
- **Vanilla decode:** `29.78 ms/tok`
- **TRUEGUARD post-pass:** `34.52 ms/tok` (`+15.9%` overhead; **4.60× faster** than 5× sampling)
- **TRUEGUARD online (per-token):** `37.84 ms/tok` (`+27.1%` overhead; sensor math = `4.93 ms/tok`; **4.20× faster** than 5× sampling)
- **5× multi-sample baseline:** `158.77 ms/tok`

---

## 4. Claim-by-Claim Scientific Validation (Task 3)

### Supported Claims (Safe for IEEE Access Manuscript)
1. **Strong In-Domain Detection & Calibration:** TRUEGUARD achieves `0.877–0.994` AUROC (`ECE <= 0.025`) across 4 standard paired benchmarks and `0.720` AUROC (`2.1×` random AUPRC, `ECE = 0.006`) on imbalanced HaluEval-General, with zero LLM fine-tuning.
2. **Diagnostic Discovery of Zero-Shot Failure Mechanisms:** Supervised linear probes fail under strict zero-shot transfer (`0.448–0.521` AUROC) due to (a) near-orthogonal hidden-state hyperplane rotation ($\cos \in [-0.031, +0.051]$), (b) >96% fusion weight dominance by ISP (`+2.935`), and (c) directional sign inversion of uncertainty sensors between synthetic (HaluEval) and natural (FaithDial/XSum) hallucinations.
3. **Lightweight Few-Shot Adaptation Restores Generalization & Calibration:** Re-fitting only the lightweight linear probes and fusion gate on `K = 250` target examples (in `<2s` on CPU) yields statistically significant gains ($p_{\text{Holm}} \le 7\times 10^{-6}$) of `+0.178` to `+0.335` AUROC and cuts ECE by `82–93%` across all 4 target domains.
4. **Risk-Controlled Selective Prediction Superiority over Uncertainty Baselines:** On TriviaQA on-policy generations, calibrated TRUEGUARD significantly outperforms Entropy (`-0.095` AURC, $p < 0.0001$) and NLL (`-0.248` AURC, $p < 0.0001$) at matched coverage, and delivers `4.2–4.6×` speedup over 5× multi-sampling.

### Claims That MUST Be Qualified (Caveats Required)
1. **ISP vs. 4-Sensor Fusion:** Do **not** claim 4-sensor fusion universally beats ISP-only in AUROC. State honestly that ISP dominates in-domain and large-$K$ AUROC, while AAS/EEM/DST provide (i) unsupervised zero-shot fallback (EEM reaches `0.747` on FaithDial and `0.635` on XSum when ISP collapses), (ii) variance stabilization under severe class imbalance (`+0.071` to `+0.106` over ISP on XSum $K=50/100$), (iii) low-FPR unique catches (`+18.1%` union recall on HaluEval-General), and (iv) per-sensor explainability.
2. **Mitigation Mechanism:** Do **not** claim Tier 1/2 regeneration/retrieval resolves most hallucinations. State honestly that **risk-controlled abstention drives the bulk of system-wide hallucination reduction** (`112/165` blocked vs. `4/165` repaired), at a cost of `27.1%` false-positive abstention among originally correct answers.

### Claims NOT Supported (Do Not Include)
- Do **not** describe $K > 0$ few-shot adaptation as "zero-shot generalization."
- Do **not** describe the 40% few-shot test splits as "completely unexamined external confirmation."
- Do **not** claim universal cross-model generalization beyond frozen TinyLlama-1.1B without multi-model experiments.

---

## 5. Final Verdict

### **READY FOR MANUSCRIPT PREPARATION**

Zero unresolved technical, statistical, or data-leakage blockers remain. All original experimental artifacts and improvement audits are verified, reproducible, and ready to support a rigorous, transparent IEEE Access manuscript.
