# FINAL IEEE ACCESS RESEARCH-READINESS REPORT

**Project:** TRUEGUARD — A White-Box Framework for LLM Hallucination Detection and Risk-Based Mitigation  
**Workspace:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL`  
**Date:** 2026-11-19  

---

## 1. Component-by-Component Verification Status

| Experimental Component | Status | Verification Evidence |
| :--- | :---: | :--- |
| **Original 10-Dataset GPU Run (`32,590` seq)** | **VERIFIED** | Byte-identical SHA-256 match with `CAPSTONE/FInal/src/`; 0 NaNs/Infs; independent recomputation matches to `1.11e-16`. |
| **In-Domain 5-Fold Group CV (5 Datasets)** | **VERIFIED** | `0.877–0.994` AUROC (`ECE <= 0.025`) on paired benchmarks; `0.720` AUROC (`0.387` AUPRC, `ECE = 0.0055`) on HaluEval-General. |
| **Zero-Shot Cross-Domain Diagnosis (4 Datasets)** | **VERIFIED** | Proven mechanisms: near-orthogonal ISP rotation (`cos in [-0.031, +0.051]`), >96% ISP fusion weight dominance (`+2.935`), and synthetic-vs-natural uncertainty sign inversion. |
| **Few-Shot Target Adaptation (`K=50, 100, 250`)** | **VERIFIED** | 0 group overlap across 60/40 splits; 10 seeds; exact Colab `.npz` zero-shot baseline corrected for local sklearn unpickling drift (`0.4929` FaithDial, `0.4883` WikiBio, `0.5205` FEVER, `0.4597` XSum) -> `K=250` recovers `0.8231`, `0.6698`, `0.7325`, `0.6456` AUROC and cuts ECE by `82–93%`. |
| **External Baselines (`SelfCheckGPT-NLI`, `Semantic Entropy`)** | **VERIFIED** | Recomputed directly from `external_baseline_predictions.npz` on identical 250 TriviaQA test questions (`n_cal=250`, `M=10`); finite-sample bootstrap p-values (`B=1000`, Holm-adjusted). |
| **TriviaQA Closed-Book Mitigation** | **VERIFIED** | `66.0% -> 20.8%` system hallucination at `46.0%` coverage (`54.8%` answered acc); transparent accounting of `112` TP abstentions, `23` FP abstentions, and `4` active Tier 1/2 repairs. |
| **Latency & Resource Accounting** | **VERIFIED (NON-EQUIVALENCE DISCLOSED)** | Controlled sequential benchmark (`real_latency.json`) confirms `4.20x–4.60x` speedup over 5x sequential sampling; batched `M=10` external baseline timings are explicitly marked non-equivalent (different attention kernel, batch size, forced length, and omitted greedy pass). |

---

## 2. Corrected Final External Baseline Comparison (TriviaQA `n_test = 250`, Finite-Sample `p`)

| Method | AUROC [95% CI] | AUPRC | F1 (Cal Thr) | AURC [95% CI] | Acc@46% | $\Delta$ AUROC ($p_{	ext{Holm}}$) | $\Delta$ AURC ($p_{	ext{Holm}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TRUEGUARD 4-Sensor** | **0.7876** [0.720, 0.852] | 0.8460 | **0.8084** | **0.4360** [0.360, 0.524] | **55.6%** | — | — |
| **TRUEGUARD ISP-Only** | 0.7706 [0.701, 0.834] | 0.8476 | 0.8062 | 0.4473 [0.369, 0.532] | 53.9% | `+0.0170` (`0.478`, n.s.) | `-0.0113` (`0.451`, n.s.) |
| **SelfCheckGPT-NLI ($M=10$)** | 0.7477 [0.681, 0.812] | **0.8537** | 0.5920 | 0.4659 [0.385, 0.559] | 50.4% | `+0.0399` (`0.478`, n.s.) | `-0.0299` (`0.362`, n.s.) |
| **Semantic Entropy LN ($M=10$)** | 0.6859 [0.621, 0.756] | 0.8059 | 0.6377 | 0.5411 [0.450, 0.627] | 49.6% | **`+0.1017` (`0.012`)** | **`-0.1051` (`0.006`)** |
| **Semantic Entropy Disc. ($M=10$)** | 0.6856 [0.620, 0.753] | 0.8025 | 0.6403 | 0.5414 [0.452, 0.629] | 48.7% | **`+0.1020` (`0.012`)** | **`-0.1054` (`0.006`)** |
| **Predictive Entropy** | 0.6583 [0.587, 0.730] | 0.7471 | 0.5985 | 0.5309 [0.448, 0.617] | 45.2% | **`+0.1293` (`0.006`)** | **`-0.0949` (`0.006`)** |
| **Length-Norm. NLL** | 0.4678 [0.396, 0.543] | 0.6453 | 0.5423 | 0.6843 [0.603, 0.760] | 31.3% | **`+0.3198` (`0.006`)** | **`-0.2483` (`0.006`)** |

---

## 3. Supported Contributions & Mandatory Manuscript Qualifications

### Supported Contributions
1. **Single-Pass Frozen-Model White-Box Risk Detection:** Achieves `0.877–0.994` AUROC (`ECE <= 0.025`) on paired benchmarks, `0.720` AUROC (`2.1x` random AUPRC) on imbalanced HaluEval-General, and the highest observed AUROC (`0.7876`) and lowest AURC (`0.4360`) on closed-book TriviaQA—significantly outperforming Semantic Entropy (`p_Holm = 0.012 / 0.006`), Predictive Entropy (`p_Holm = 0.006`), and NLL (`p_Holm = 0.006`), while demonstrating competitive performance against SelfCheckGPT-NLI with `1` generation and `0` external NLI models.
2. **Mechanistic Diagnosis of Cross-Domain Failure & Lightweight Few-Shot Recovery:** Proves why zero-shot white-box probes fail (orthogonal ISP hyperplane rotation, >96% ISP weight dominance, sensor sign inversion) and demonstrates that `<2s` CPU few-shot re-fitting (`K=250`) restores `+0.186` to `+0.330` AUROC and reduces ECE by `82–93%`.
3. **Risk-Controlled Selective Prediction & Mitigation with Explicit Coverage Trade-Offs:** Reduces system-wide hallucinations on TriviaQA by `68.5%` (`66.0% -> 20.8%`) at `46.0%` coverage (`54.8%` answered accuracy) with transparent reporting of abstention vs. repair trade-offs.

### Mandatory Qualifications (Must Appear in Manuscript)
- TRUEGUARD does **not** significantly outperform SelfCheckGPT-NLI in AUROC (`p_Holm=0.478`) or AURC (`p_Holm=0.362`), and SelfCheckGPT-NLI achieves slightly higher observed AUPRC (`0.8537` vs. `0.8460`).
- Four-sensor fusion does **not** consistently outperform ISP-only in AUROC; AAS/EEM/DST are justified by zero-shot fallback (EEM), low-`K`/severe-imbalance stabilization (`XSum K=50/100`), low-FPR unique catches, and per-sensor explainability.
- Original zero-shot cross-domain generalization remains weak (`0.460–0.521`); few-shot adaptation requires labeled target-domain examples and was evaluated on 40% splits of previously inspected benchmarks (not unexamined external confirmation).
- FEVER is reported separately as claim-verification transfer.
- Most TriviaQA mitigation improvement comes from selective abstention (`112/165` blocked, `23/85` correct abstained) rather than factual correction (`4/165` repaired).
- The `4.20x–4.60x` speedup applies **only** to the controlled sequential 5-sample benchmark (`real_latency.json`), not automatically to GPU-batched SelfCheckGPT or Semantic Entropy; monitoring-only latency is strictly separated from end-to-end mitigation latency.
- Single foundation model (`TinyLlama-1.1B-Chat-v1.0`); scaling to 7B–70B models is future work.

---

## 4. Final Verdict

# **READY FOR IEEE ACCESS MANUSCRIPT PREPARATION**

Zero essential experimental or statistical issues remain. All discrepancies (sklearn unpickling drift, finite-sample bootstrap p-value bounds, and latency protocol non-equivalence) have been audited, corrected, and transparently documented.
