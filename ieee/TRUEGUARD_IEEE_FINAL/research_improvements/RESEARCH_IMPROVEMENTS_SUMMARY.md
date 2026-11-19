# TRUEGUARD — Research Improvements & Statistical Validation Summary

**Workspace:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\research_improvements`  
**Original Evidence Status:** 100% preserved and untouched in `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\`.

---

## Phase 1 — Independent Evidence Verification Audit (`phase1_verification_audit.json`)
- **Exact Metric Re-Verification:** Recomputed AUROC, AUPRC, F1, Precision, Recall, Accuracy, ECE, and Brier directly from all 9 saved `.npz` prediction files (`in_domain_oof_*.npz`, `unseen_zeroshot_*.npz`). Maximum absolute discrepancy vs. `final_experiment_report.json` is **`1.11e-16`** (exact machine precision).
- **Checkpoint Integrity:** All 11 feature checkpoints (`32,590` total extracted rows) contain **0 NaNs and 0 Infs**.
- **Latency Arithmetic:** Verified exact match (`29.78 ms` vanilla, `37.84 ms` online = `+27.08%`, `34.52 ms` post-pass = `+15.93%`, `158.77 ms` 5× sampling $\rightarrow$ **4.20×** online / **4.60×** post-pass speedup). Note: relative overhead is higher than the earlier Capstone run (`+17.3%`) primarily because vanilla decoding was faster (`29.78` vs. `33.49 ms/tok`) and this run profiled the real pooled 4-layer detector.
- **TriviaQA Abstention Audit:** Out of 135 abstentions (54.0% of 250 test questions), **112** were true-positive blocks of hallucinations (**67.9%** of all 165 hallucinations blocked; **83.0%** abstention precision) and **23** were false-positive abstentions of originally correct answers (**27.1%** of the 85 correct answers).

---

## Phase 2 — Why Zero-Shot Cross-Domain Transfer Failed (`phase2_cross_domain_diagnostics.json`)
Three empirically verified mechanisms explain why pooled in-domain TRUEGUARD dropped to `0.448–0.519` AUROC zero-shot while raw EEM reached `0.746` (FaithDial) and `0.665` (XSum):

1. **Frozen Hidden States DO Contain Strong Target-Domain Signal, But Linear Hyperplanes Rotate Nearly 90° Across Domains:**
   - Diagnostic 5-fold GroupKFold ISP AUROC on target domains: **FaithDial `0.8927`**, **FEVER `0.8754`**, **WikiBio-GPT3 `0.7427`**, **XSum `0.6794`**.
   - Mean cosine similarity $\cos(w_{\text{pool}}, w_{\text{target}})$ across the 4 probed layers is near zero: FaithDial **`-0.0306`**, WikiBio **`-0.0045`**, FEVER **`+0.0510`**, XSum **`+0.0280`**.
2. **Extreme Fusion Weight Dominance by ISP:**
   - Standardized fusion coefficients in `trueguard_pooled_in_domain.joblib`: `ISP_logit = +2.9353` (>96% of total weight magnitude) vs. `EEM_mean = +0.0680`, `AAS_mean = +0.0146`, `DST_mean = -0.0137`, `DST_max = +0.0047`, `AAS_max = +0.0036`, `EEM_max = -0.0028`.
   - When ISP rotated orthogonally on unseen domains, fusion could not fall back on EEM.
3. **Domain-Dependent Sensor Sign Inversion:**
   - Raw `EEM_mean` is **inverted** on synthetic HaluEval (`0.374` Dialogue, `0.363` QA), neutral on TruthfulQA (`0.491`) and HaluEval-General (`0.483`), and strongly **positive** on natural/human-evaluated hallucinations (`0.746` FaithDial, `0.665` XSum).
- See: `figures/fig_phase2_sensor_sign_inversion.png`.

---

## Phase 3 & 6 — Selected Lightweight Improvement: Few-Shot Target-Domain Adaptation (`phase3_fewshot_adaptation_results.json`)
- **Method Selection Rationale:** Unsupervised feature normalization cannot undo a 90° linear hyperplane rotation ($\cos \approx 0$), and monotonic calibration cannot change AUROC. Re-fitting TRUEGUARD's lightweight linear probes and regularized 4-sensor fusion on $K \in \{50, 100, 250\}$ labeled target examples (frozen TinyLlama unchanged; runs in <2s on CPU) directly re-aligns both the ISP subspace and target-domain sensor signs.
- **Leakage-Free Protocol:** Fixed, group-disjoint **60% Adaptation Pool / 40% Untouched Final Test Set** per dataset; **10 fixed seeds** per $K$; all scalers, probes, inner-OOF `C` selection, fusion weights, and thresholds fit strictly on the $K$ examples; Holm-Bonferroni correction applied across all 36 tests.
- **Explicit Distinction:** Methods with $K > 0$ are **few-shot target-domain adaptation**, *never* zero-shot. FEVER is reported separately as **claim-verification transfer**.

| Target Dataset (Untouched 40% Test) | Zero-Shot Unadapted Fusion | Raw EEM (Unsup.) | Few-Shot $K=50$ Fusion (10 seeds) | Few-Shot $K=100$ Fusion (10 seeds) | Few-Shot $K=250$ Fusion (10 seeds) | $K=250$ vs. Unadapted ($p_{\text{Holm}}$) | $K=250$ ECE (vs. Unad.) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **FaithDial** ($n=1396$, 317 dialogs) | 0.4881 | 0.7473 | 0.6987 ± 0.088 | 0.7899 ± 0.031 | **0.8231 ± 0.012** | **+0.3350** ($<10^{-6}$) | **0.044** (0.657) |
| **WikiBio-GPT3** ($n=734$, 96 articles) | 0.4868 | 0.5223 | 0.5088 ± 0.056 | 0.4939 ± 0.084 | **0.6698 ± 0.038** | **+0.1830** ($3\times 10^{-6}$) | **0.074** (0.434) |
| **XSum Factuality** ($n=752$, 200 articles) | 0.4678 | 0.6352 | 0.5401 ± 0.069 | 0.6058 ± 0.043 | **0.6456 ± 0.041** | **+0.1778** ($7\times 10^{-6}$) | **0.038** (0.563) |
| **FEVER** *(Claim-Verif. Transfer, $n=2667$)* | 0.5209 | 0.5439 | 0.5394 ± 0.048 | 0.6195 ± 0.040 | **0.7325 ± 0.014** | **+0.2115** ($<10^{-6}$) | **0.043** (0.342) |

- See: `figures/fig_phase3_fewshot_adaptation_curves.png`.

---

## Phase 4 — Honest Assessment of Four-Sensor Necessity
1. **In-Domain (Large $N$, 5-Fold CV):** ISP alone matches 4-sensor fusion within $\pm 0.002$ AUROC; removing ISP causes large drops (`-0.058` to `-0.271`). However, AAS/EEM/DST provide low-FPR unique catches (e.g., `+18.1%` union recall on HaluEval-General, `+6.5%` on TruthfulQA) and per-sensor explainability.
2. **Zero-Shot Shift (0 target labels):** Unsupervised **EEM** decisively beats supervised ISP on FaithDial (`0.747` vs. `0.487`) and XSum (`0.635` vs. `0.468`), demonstrating that scalar sensors are vital when target labels are unavailable.
3. **Few-Shot Regime:**
   - Under severe class imbalance or small $K$ (XSum $K=50/100$, FaithDial $K=50$), 2,048-dim ISP suffers high variance or collapses (`0.470–0.500` on XSum), whereas 4-sensor fusion stabilizes variance and outperforms ISP-only by `+0.032` to `+0.106` AUROC (raw $p = 0.007$ on XSum $K=100$, $p_{\text{Holm}} = 0.149$).
   - At $K = 250$ on balanced/moderately imbalanced targets (FaithDial, WikiBio, FEVER), ISP-only slightly edges 4-sensor fusion by `0.009–0.014` AUROC (significant on FEVER $K=250$, $p_{\text{Holm}} = 0.045$, where scalar sensors carry near-chance signal `0.535`).
4. **Conclusion:** Report honestly that **ISP is the dominant in-domain and large-$K$ signal, while AAS/EEM/DST act as low-dimensional stabilizers under severe class imbalance, zero-shot shift (EEM), low-FPR complementarity, and explainable attribution.**

---

## Phase 5 — Strengthened TriviaQA Mitigation Evidence (`phase5_mitigation_deep_analysis.json`)
On the exact same 250 closed-book TriviaQA test questions (matched 46.0% answer coverage):

| Method | AUROC | AURC [95% CI] | Acc @ 46% Cov (Risk) | Acc @ 50% Cov | Paired $\Delta$ AURC vs. TRUEGUARD ($p$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **TRUEGUARD 4-Sensor** | **0.7876** | **0.4360** [0.360, 0.524] | **55.7%** (44.3%) | **54.4%** | — |
| **ISP Only** | 0.7706 | 0.4473 [0.369, 0.532] | 53.9% (46.1%) | 52.0% | `-0.0113` ($p = 0.225$, n.s.) |
| **Scalars Only (AAS+EEM+DST)** | 0.7130 | 0.4891 [0.404, 0.577] | 49.6% (50.4%) | 48.0% | **`-0.0531` ($p < 0.0001$)** |
| **Entropy Baseline** | 0.6583 | 0.5309 [0.448, 0.617] | 45.2% (54.8%) | 46.4% | **`-0.0949` ($p < 0.0001$)** |
| **NLL Baseline** | 0.4678 | 0.6843 [0.603, 0.760] | 31.3% (68.7%) | 32.8% | **`-0.2483` ($p < 0.0001$)** |

- **Controller vs. Pure Abstention:** At 46.0% coverage, the full 3-tier controller achieves `54.8%` answered accuracy vs. `55.7%` for pure selective abstention (`-0.9%`), with `112/165` hallucinations blocked by abstention and `4/165` (`2.4%`) actively corrected by Tier 1/2 (`2` resample + `2` Wikipedia retrieval). We must frame mitigation honestly as **risk-controlled selective abstention with modest corrective recovery**, not exaggerate Tier 1/2 repair rates.
- **Missing Evidence Note:** Comparing full regenerative Tier 1/2 trajectories driven by Entropy/NLL thresholds would require new GPU generations; matched-coverage selective abstention is compared cleanly on the identical 250 test questions.
- See: `figures/fig_phase5_triviaqa_matched_coverage.png`.
