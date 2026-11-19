# Task 4 — Final External Validation & Publication-Readiness Assessment

**Directory:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\external_validation\`  
**Verified Artifacts:** `external_baselines_report.json`, `external_baseline_predictions.npz`, `fig_external_baselines_risk_coverage.png`, `selfcheckgpt_nli_scores.json`, `semantic_entropy_scores.json`, `triviaqa_m10_samples.json`, `independent_reproducibility_audit.py`, `independent_verification_report.json`, `INDEPENDENT_VERIFICATION_REPORT.md`.

---

## 1. Head-to-Head Comparison on Identical 250 TriviaQA Test Questions (`n_cal=250`, `n_test=250`, $M=10$)

All scores independently re-verified from `external_baseline_predictions.npz` (`max_diff <= 4.7e-5` rounding). Thresholds for F1 were calibrated strictly on the 250-question calibration split using Youden's $J$ (zero test-label access).

| Method | AUROC [95% CI] | AUPRC | F1 (Cal Thr) | AURC [95% CI] | Acc@46% | Acc@50% | $\Delta$ AUROC vs. TG ($p$) | $\Delta$ AURC vs. TG ($p_{\text{Holm}}$) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **TRUEGUARD 4-Sensor** | **0.7876** [0.720, 0.852] | 0.8460 | **0.8084** | **0.4360** [0.360, 0.524] | **55.6%** | **54.4%** | — | — |
| **TRUEGUARD ISP-Only** | 0.7706 [0.701, 0.834] | 0.8476 | 0.8062 | 0.4473 [0.369, 0.532] | 53.9% | 52.0% | `+0.0170` ($p=0.446$, n.s.) | `-0.0113` ($0.450$, n.s.) |
| **SelfCheckGPT-NLI ($M=10$)** | 0.7477 [0.681, 0.812] | **0.8537** | 0.5920 | 0.4659 [0.385, 0.559] | 50.4% | 49.6% | `+0.0399` ($p=0.238$, n.s.) | `-0.0299` ($0.360$, n.s.) |
| **Semantic Entropy LN ($M=10$)** | 0.6859 [0.621, 0.756] | 0.8059 | 0.6377 | 0.5411 [0.450, 0.627] | 49.6% | 48.0% | **`+0.1017` ($p=0.002$)** | **`-0.1051` ($<0.0001$)** |
| **Semantic Entropy Disc. ($M=10$)** | 0.6856 [0.620, 0.753] | 0.8025 | 0.6403 | 0.5414 [0.452, 0.629] | 48.7% | 48.0% | **`+0.1020` ($p=0.002$)** | **`-0.1054` ($<0.0001$)** |
| **Predictive Entropy** | 0.6583 [0.587, 0.730] | 0.7471 | 0.5985 | 0.5309 [0.448, 0.617] | 45.2% | 46.4% | **`+0.1293` ($<0.0001$)** | **`-0.0949` ($<0.0001$)** |
| **Length-Norm. NLL** | 0.4678 [0.396, 0.543] | 0.6453 | 0.5423 | 0.6843 [0.603, 0.760] | 31.3% | 32.8% | **`+0.3198` ($<0.0001$)** | **`-0.2483` ($<0.0001$)** |

---

## 2. End-to-End Computational Cost Accounting (Transparent Comparison)

| System | Total LLM Generations / Q | Extra External Model | End-to-End GPU Time / Q | Extra VRAM |
| :--- | :---: | :--- | :---: | :---: |
| **TRUEGUARD Post-Pass** | **1** (greedy + 1 sensor pass) | **None** | **`0.8285 s`** | **0 GB** |
| **TRUEGUARD Online** | **1** (per-token monitoring) | **None** | **`0.9082 s`** | **0 GB** |
| **SelfCheckGPT-NLI ($M=10$ batched)** | **11** (1 greedy + 10 sampled) | `potsawee/deberta-v3-large-mnli` (435M) | **`1.421 s`** (`0.715 s` greedy + `0.655 s` batched $M=10$ + `0.052 s` NLI) | **+1.004 GB** |
| **Semantic Entropy ($M=10$ batched)** | **10** (sampled) | `microsoft/deberta-large-mnli` (435M) | **`1.662 s`** (`0.655 s` batched $M=10$ + `1.008 s` bidirectional NLI) | **+2.474 GB** |

- **Transparent Speedup Reporting:**
  - Under **sequential / high-concurrency serving** (where GPU batch slots are saturated by concurrent requests), TRUEGUARD is **4.20×–4.60× faster** than 5× multi-sampling (`real_latency.json`).
  - Under **single-query idle-GPU batching** (batching all 10 stochastic samples in parallel on T4), TRUEGUARD post-pass (`0.829 s/q`) is **1.72× faster** than full end-to-end SelfCheckGPT-NLI (`1.421 s/q` including the initial greedy generation) and **2.01× faster** than Semantic Entropy (`1.662 s/q`), while using **10×–11× fewer generated tokens** and **zero external NLI models** (`1.00–2.47 GB` VRAM saved).

---

## 3. Honest Assessment of Statistical & Practical Significance (Task 4)

1. **TRUEGUARD vs. Semantic Entropy (Kuhn et al., ICLR 2023; Farquhar et al., Nature 2024):**
   - **Statistically & practically superior:** TRUEGUARD beats both length-normalized and discrete Semantic Entropy by **`+0.102` AUROC ($p = 0.002$)**, **`-0.105` AURC ($p_{\text{Holm}} < 0.0001$)**, **`+0.171` F1**, and **`+6.0%` accuracy at 46% coverage**, while running **2.01× faster** (batched) without a 435M DeBERTa-large NLI model.
2. **TRUEGUARD vs. SelfCheckGPT-NLI (Manakul et al., EMNLP 2023):**
   - **Higher point estimates, not statistically significant on AUROC/AURC at $n=250$:** TRUEGUARD achieves higher AUROC (`0.7876` vs. `0.7477`, `+0.040`, $p=0.238$), lower AURC (`0.4360` vs. `0.4659`, `-0.030`, $p_{\text{Holm}}=0.360$), higher accuracy at 46% coverage (`55.6%` vs. `50.4%`, `+5.2%`), and substantially higher F1 at calibrated thresholds (`0.8084` vs. `0.5920`, `+0.216`), while SelfCheckGPT edges AUPRC slightly (`0.8537` vs. `0.8460`).
   - **Practical advantage:** TRUEGUARD achieves competitive-to-stronger detection with **1 generation instead of 11**, **zero extra NLI models (+1.00 GB VRAM saved)**, and **1.72×–4.60× lower latency** depending on batching regime. Do **not** claim statistically significant AUROC superiority over SelfCheckGPT-NLI; report competitive/numerically higher accuracy at dramatically lower token & model overhead.
3. **TRUEGUARD vs. Predictive Entropy & NLL:**
   - **Decisively & significantly superior** on every metric ($p_{\text{Holm}} < 0.0001$).
4. **Do All Three Research Contributions Remain Supported?**
   - **YES.** All three contributions (single-pass white-box detection, mechanistic zero-shot failure diagnosis + lightweight few-shot adaptation, and risk-controlled selective prediction / mitigation) are now reinforced by faithful head-to-head external baselines and a zero-dependency independent reproducibility audit.
5. **Final Decision:**
   - **READY TO WRITE IEEE ACCESS MANUSCRIPT** — zero essential experimental gaps remain.
