# TRUEGUARD (Paper 2) — Consolidated Experimental Tables & Hypothesis Audit

## Table 1 — In-Distribution 5-Fold Grouped CV (Detection & Single-Sensor Baselines)

| Benchmark | Pairs | TRUEGUARD Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | Best Raw Baseline | $\Delta$ vs Best Single ($p$) | F1 | ECE |
|---|---:|---|---|---|---|---|---|---|---|---|
| `halueval_dialogue` | 400 | **0.903** [0.883, 0.922] | 0.904 | 0.618 | 0.668 | 0.634 | `LEN`=0.687 | -0.001 (0.78) | 0.820 | 0.034 |
| `halueval_qa` | 400 | **0.975** [0.964, 0.987] | 0.977 | 0.512 | 0.850 | 0.859 | `LEN`=0.953 | -0.002 (1.00) | 0.955 | 0.024 |
| `halueval_summarization` | 400 | **0.986** [0.980, 0.991] | 0.987 | 0.627 | 0.580 | 0.672 | `EEM_mean`=0.581 | -0.000 (0.70) | 0.935 | 0.025 |
| `truthful_qa` | 398 | **0.876** [0.853, 0.900] | 0.877 | 0.607 | 0.522 | 0.533 | `EEM_max`=0.523 | -0.001 (0.77) | 0.817 | 0.042 |

## Table 2 — Leave-One-Sensor-Out Ablation

| Benchmark | Full (4 Sensors) | $-\text{ISP}$ | $-\text{AAS}$ | $-\text{EEM}$ | $-\text{DST}$ | Union Recall @ 10% FPR |
|---|---|---|---|---|---|---|
| `halueval_dialogue` | **0.903** | 0.714 (-0.188) | 0.903 (+0.000) | 0.903 (+0.000) | 0.903 (-0.000) | 0.762 |
| `halueval_qa` | **0.975** | 0.918 (-0.057) | 0.976 (+0.001) | 0.976 (+0.001) | 0.975 (+0.000) | 0.978 |
| `halueval_summarization` | **0.986** | 0.745 (-0.241) | 0.986 (-0.000) | 0.986 (+0.000) | 0.987 (+0.000) | 0.960 |
| `truthful_qa` | **0.876** | 0.626 (-0.251) | 0.876 (-0.001) | 0.877 (+0.000) | 0.877 (+0.001) | 0.603 |

## Table 3 — Before-and-After Three-Tier Mitigation on TriviaQA

- **Model:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0` (`n_cal=150`, `n_test=150`)
- **Calibrated thresholds:** $\tau_{\text{warning}} = 0.611$, $\tau_{\text{fault}} = 0.898$
- **Detection AUROC on model's own TriviaQA generations:** **0.795**
- **Unmitigated hallucination rate:** **62.0%** (accuracy 38.0%)
- **Post-mitigation hallucination rate among answered queries:** **40.0%** (relative drop **35.5%**, coverage **43.3%**)
- **System-wide hallucination rate (answered & wrong):** **17.3%** (relative drop **72.0%**)
- **Tier routing counts:** `SAFE=48`, `TIER1_RESAMPLE=11`, `TIER2_RETRIEVAL=6`, `TIER3_ABSTAIN=85`
- **Greedy hallucinations actively corrected:** Tier 1 fixed **2**, Tier 2 fixed **0**

## Table 4 — Real Per-Token Latency Profile

- **Device:** `cuda` (`TinyLlama/TinyLlama-1.1B-Chat-v1.0`)
- **Vanilla KV-cached decode:** `33.49 ms/tok`
- **TRUEGUARD online decode:** `39.30 ms/tok` (sensor + probe math: `5.21 ms/tok`)
- **TRUEGUARD post-pass decode:** `36.41 ms/tok`
- **5-sample consistency baseline:** `169.31 ms/tok` (**4.3x speedup** for TRUEGUARD online)
