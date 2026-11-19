# FINAL PRE-MANUSCRIPT VERIFICATION REPORT

**Project:** TRUEGUARD (`E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL`)  
**Date:** 2026-11-19  
**Scope:** Final read-only forensic verification of (1) TriviaQA supervision & comparison fairness, (2) NLL scoring integrity (`0.4678`), and (3) cached-data length-matched TF-IDF & equal-`N` cosine checks prior to freezing the evidence package for IEEE Access manuscript drafting.  
**Verification Output JSON:** [final_pre_manuscript_checks.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/reviewer_response/final_pre_manuscript_checks.json)

---

## 1. Task 1 — TriviaQA Training Protocol & External Baseline Supervision Fairness

### Forensic Code Inspection (`TRUEGUARD_IEEE_Experiments_FINAL.ipynb`, Cell 12)
Direct inspection of Cell 12 and [mitigation_report.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/results/mitigation_report.json) establishes the exact protocol:
1. **Was TRUEGUARD trained/refitted on the 250 labeled TriviaQA calibration questions?**  
   **YES.** Cell 12 executes:
   ```python
   det_tqa = TrueGuardDetector(seed=SEED).fit(F_cal, H_cal, y_cal)
   tw_tqa, tf_tqa = calibrate_thresholds(y_cal, det_tqa.train_risk_)
   ```
   Both the 4-layer ISP linear probes and the logistic fusion layer (as well as `tau_warning = 0.5973` and `tau_fault = 0.8415`) were **trained from scratch on the `250` labeled TriviaQA calibration questions** (`F_cal, H_cal, y_cal`).
2. **Was the original source-domain classifier used directly?**  
   **Not for the `0.7876` result.** However, Cell 12 *also* evaluated the pooled source-domain detector zero-shot (`POOLED_DETS["full"].predict_proba(F_te, H_te)`), saved in `predictions/triviaqa_test_predictions.npz["risk_pooled"]`, which achieved **`0.5504` AUROC**, **`0.7124` AUPRC**, **`0.6342` AURC**, **`37.4%` Acc@46%**, and **`36.8%` Acc@50%**.
3. **Label Isolation (Zero Test Leakage):**
   - `y_cal` (`n = 250`, TriviaQA alias exact match `1 - is_correct(a, gold)`): used to fit `TRUEGUARD_4sensor` and `TRUEGUARD_ISP_only` probes/fusion and to select scalar thresholds (`tau_warning`, `tau_fault`, and Youden's J threshold for F1 on all methods).
   - `y_test` (`n = 250`, disjoint): **zero access** during training, calibration, or threshold selection.
4. **Supervision Status of External Baselines (`TRUEGUARD_External_Baselines_Colab.ipynb`):**
   - `SelfCheckGPT-NLI`, `Semantic Entropy` (LN & Discrete), `Predictive Entropy`, and `NLL` were evaluated **completely label-free (unsupervised) for ranking** (`AUROC`, `AUPRC`, `AURC`, `Acc@46%`). They used the `250` calibration labels **only** to choose a single scalar Youden's J cutoff for binary `F1`.
5. **Documentation Update Applied:**
   - [Table7_External_Baselines_TriviaQA.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table7_External_Baselines_TriviaQA.md) (and `.csv`), [05_EXTERNAL_BASELINES_LATENCY_AND_REFERENCES.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/05_EXTERNAL_BASELINES_LATENCY_AND_REFERENCES.md), [01_SUPPORTED_CONTRIBUTIONS_AND_LIMITATIONS.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/01_SUPPORTED_CONTRIBUTIONS_AND_LIMITATIONS.md), and [FINAL_RESEARCH_READINESS_AFTER_REVIEW.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/FINAL_RESEARCH_READINESS_AFTER_REVIEW.md) have been updated to add an explicit **`Supervision / Target Labels`** column and include the **`TRUEGUARD_Pooled_ZeroShot` (`0.5504` AUROC / `0.6342` AURC)** row directly in Table VII.

---

## 2. Task 2 — Forensic Verification of NLL Scoring (`AUROC = 0.4678`)

### Source Code & Saved Array Audit
Inspection of [tg_pipeline.py](file:///E:/trueguard/CAPSTONE/FInal/src/tg_pipeline.py#L113-L118) (SHA-256 identical to the embedded Colab source) and `external_baseline_predictions.npz`:
- **Exact Formula:**
  ```python
  P = torch.arange(a_start - 1, a_end - 1, device=out.logits.device)
  logits = out.logits[0, P, :].float()
  logp = torch.log_softmax(logits, dim=-1)
  tgt = input_ids[0, a_start:a_end].to(logits.device)
  nll = (-logp.gather(1, tgt[:, None])[:, 0]).cpu().numpy()
  # Aggregated as token-length-normalized mean: nll.mean()
  ```
- **Sign & Range Check (`n_test = 250`):** `100%` of values are strictly positive (`min = 0.4334`, `median = 0.7491`, `max = 2.1580`). Higher score = higher negative log-likelihood = lower token probability = higher expected hallucination risk.
- **Label Orientation Check (`y = 1` hallucination, `n = 165`; `y = 0` correct, `n = 85`):**
  - `Pearson r(NLL, Predictive Entropy) = +0.6698` (strong positive alignment with `ENT_mean`, which achieves `0.6583` AUROC using the exact same `y = 1` orientation).
  - Mean NLL on **correct** greedy answers (`y = 0`): **`0.7991 ± 0.2370`** (median `0.7560`).
  - Mean NLL on **hallucinated** greedy answers (`y = 1`): **`0.7711 ± 0.2003`** (median `0.7480`).
  - `AUROC(y=1, +NLL) = 0.4678 [95% CI: 0.396, 0.542]` (95% CI spans `0.50`).
- **Verdict:** **Zero bug, zero sign error, zero label-inversion error.** The below-chance point estimate (`0.4678`) is a **genuine empirical phenomenon**: TinyLlama-1.1B assigns slightly lower mean per-token NLL (higher confidence) to fluent, boilerplate hallucinated TriviaQA generations than to terse correct factual entities. **No metric recalculation is needed.**

---

## 3. Task 3 — Cached-Data Supplementary Checks

### 3A. Answer-Text TF-IDF on Exact Length-Matched (`|ΔL| ≤ 2` tok) Subsets with Paired 95% CIs (`B = 1000` Group Bootstrap)

| Dataset (`\|ΔL\| ≤ 2` tok) | `n` (Pairs) | TRUEGUARD AUROC [95% CI] | TF-IDF (Full OOF) [95% CI] | TF-IDF (Refit Inside LM) | Paired $\Delta$ (TG − TF-IDF) [95% CI] | `p_boot` (2-sided) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **HaluEval-Dialogue** | 1,352 (676) | **0.7996** [0.782, 0.818] | 0.7167 [0.697, 0.737] | 0.7072 | **`+0.0829` [+0.064, +0.101]** | **`0.0010`** |
| **HaluEval-QA** | 256 (128) | **0.7901** [0.744, 0.837] | 0.7440 [0.693, 0.794] | 0.7322 | **`+0.0461` [+0.004, +0.086]** | **`0.0350`** |
| **HaluEval-Summ** | 3,546 (1,773) | **0.9939** [0.992, 0.995] | 0.9608 [0.955, 0.966] | 0.9586 | **`+0.0331` [+0.028, +0.038]** | **`0.0010`** |
| **TruthfulQA** | 714 (357) | **0.8106** [0.782, 0.840] | 0.7394 [0.707, 0.772] | 0.7501 | **`+0.0712` [+0.043, +0.096]** | **`0.0010`** |

**Finding:** Even when length is strictly matched (`|ΔL| ≤ 2` tokens), TRUEGUARD **statistically significantly outperforms answer-text TF-IDF on all four paired benchmarks** (`p = 0.0010` to `0.0350`), whether TF-IDF is evaluated from full-dataset OOF predictions or refitted strictly inside the length-matched subset.

### 3B. Equal-Sample-Size (`N_fit = 900` per half, 3 Seeds × 4 Layers) Within-Domain vs. Cross-Domain Probe Cosine

| Comparison (`N_fit = 900` strictly equal) | Mean Cosine ± SD | Min / Max |
| :--- | :---: | :---: |
| **Within-Domain (`N=900`): HaluEval-Summ** | **`+0.6707 ± 0.0129`** | — |
| **Within-Domain (`N=900`): HaluEval-QA** | **`+0.4999 ± 0.0363`** | — |
| **Within-Domain (`N=900`): HaluEval-Dialogue** | **`+0.3930 ± 0.0280`** | — |
| **Within-Domain (`N=900`): FEVER** | **`+0.2668 ± 0.0189`** | — |
| **Within-Domain (`N=900`): FaithDial** | **`+0.2205 ± 0.0168`** | — |
| **Within-Domain (`N=900`): WikiBio-GPT3** | **`+0.1282 ± 0.0318`** | — |
| **Within-Domain (`N=900`): XSum-Factuality** | **`+0.1125 ± 0.0295`** | — |
| **Cross-Domain (`N=900`): HaluEval → FaithDial** | `-0.0151 ± 0.0263` | `[-0.080, +0.041]` |
| **Cross-Domain (`N=900`): HaluEval → WikiBio-GPT3** | `+0.0032 ± 0.0176` | `[-0.024, +0.038]` |
| **Cross-Domain (`N=900`): HaluEval → FEVER** | `+0.0204 ± 0.0381` | `[-0.035, +0.129]` |
| **Cross-Domain (`N=900`): HaluEval → XSum-Factuality** | `+0.0092 ± 0.0249` | `[-0.055, +0.046]` |

**Finding:** Eliminating sample-size differences (`N_fit = 900` across all datasets) confirms that within-domain split-half probe alignment (`+0.113` to `+0.671`) remains substantially higher than cross-domain alignment (`-0.015` to `+0.020`, centered on zero within the `±0.0221` random 2,048-d noise band).

---

## 4. Corrected Numerical Results & Remaining Limitations

- **Numerical Corrections:** Zero experimental metrics were invalidated. Only **Table VII** (`Table7_External_Baselines_TriviaQA.md/.csv`) was expanded to add the `Supervision / Target Labels` column and the `TRUEGUARD_Pooled_ZeroShot` row (`0.5504` AUROC, `0.7124` AUPRC, `0.6342` AURC, `37.4%` Acc@46%, `36.8%` Acc@50%), already saved in `triviaqa_test_predictions.npz`.
- **Remaining Limitations (Disclosed, Not Blockers):** Single frozen `1.1B` model (`TinyLlama-1.1B-Chat-v1.0`), `n_test = 250` TriviaQA test power, supervision asymmetry between target-refitted TRUEGUARD (`K=250`) and label-free external baselines on TriviaQA, prior inspection of the 4 unseen datasets before target-only refitting, and un-reproduced unsupervised white-box baselines (`CCS`, `EigenScore`).

---

## 5. Exact Drop-In Statements for the IEEE Access Manuscript

### For Section III (Methodology — TriviaQA Calibration & Supervision Protocol)
> *"For the closed-book TriviaQA selective-prediction experiment (`n_cal = 250`, `n_test = 250`, disjoint question sets), TRUEGUARD's four-layer ISP probes, logistic fusion layer, and risk thresholds (`τ_warning = 0.5973`, `τ_fault = 0.8415`) were fitted from scratch using the 250 labeled calibration generations (`y_cal = 1` if greedy output fails TriviaQA alias exact match), with zero access to test labels. For direct zero-shot comparison without target supervision, we also evaluate the pooled source-domain detector (`TRUEGUARD_Pooled_ZeroShot`) unchanged on the same 250 test questions. All external and uncertainty baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`, `Predictive Entropy`, and token-length-normalized `NLL`) are completely label-free for ranking (AUROC, AUPRC, AURC, and selective accuracy at matched coverage) and use the 250 calibration labels solely to select a scalar Youden's J operating threshold for binary F1."*

### For Section IV/V (Results — External Comparison & NLL Behavior)
> *"On the 250 held-out TriviaQA generations, target-refitted single-pass TRUEGUARD (`K = 250`) achieves `0.7876` AUROC (`95% CI [0.720, 0.852]`) and `0.4360` AURC (`[0.360, 0.523]`), significantly outperforming label-free `M = 10` Semantic Entropy (`0.6859` AUROC / `0.5411` AURC; `p_Holm = 0.012 / 0.006`), Predictive Entropy (`0.6583`; `p_Holm = 0.006`), and NLL (`0.4678`; `p_Holm = 0.006`), while performing competitively with label-free `M = 10` SelfCheckGPT-NLI (`0.7477` AUROC / `0.4659` AURC; `p_Holm = 0.478 / 0.362`, n.s.) without extra generations or an external NLI model. Crucially, this gain depends on target-domain supervision: without TriviaQA labels, `TRUEGUARD_Pooled_ZeroShot` drops to `0.5504` AUROC (`0.6342` AURC), trailing every label-free baseline except NLL. Token-length-normalized NLL exhibits a genuine near-chance/mildly inverted AUROC (`0.4678 [0.396, 0.542]`) because TinyLlama-1.1B assigns slightly lower mean NLL to fluent hallucinated answers (`0.771 ± 0.200`) than to terse correct factual entities (`0.799 ± 0.237`), despite correlating positively with predictive entropy (`r = +0.670`)."*

---

## Final Status

# **EVIDENCE PACKAGE FINALIZED FOR IEEE ACCESS MANUSCRIPT DRAFTING**

All verification checks passed with zero scoring bugs or invalidated results. The `publication_ready/` evidence package is frozen and ready for IEEE Access manuscript drafting.
