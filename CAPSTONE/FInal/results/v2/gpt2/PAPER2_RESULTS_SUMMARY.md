# TRUEGUARD (Paper 2) — Consolidated Experimental Tables & Hypothesis Audit

## Table 1 — In-Distribution 5-Fold Grouped CV (Detection & Single-Sensor Baselines)

| Benchmark | Pairs | TRUEGUARD Fusion AUROC [95% CI] | ISP | AAS | EEM | DST | Best Raw Baseline | $\Delta$ vs Best Single ($p$) | F1 | ECE |
|---|---:|---|---|---|---|---|---|---|---|---|
| `halueval_qa` | 80 | **0.960** [0.916, 0.992] | 0.957 | 0.486 | 0.857 | 0.894 | `LEN`=0.951 | +0.002 (0.36) | 0.948 | 0.102 |
| `truthful_qa` | 80 | **0.744** [0.669, 0.820] | 0.766 | 0.485 | 0.383 | 0.489 | `ENT_max`=0.517 | -0.021 (0.98) | 0.729 | 0.080 |

## Table 2 — Leave-One-Sensor-Out Ablation

| Benchmark | Full (4 Sensors) | $-\text{ISP}$ | $-\text{AAS}$ | $-\text{EEM}$ | $-\text{DST}$ | Union Recall @ 10% FPR |
|---|---|---|---|---|---|---|
| `halueval_qa` | **0.960** | 0.926 (-0.034) | 0.959 (-0.001) | 0.962 (+0.001) | 0.959 (-0.001) | 0.975 |
| `truthful_qa` | **0.744** | 0.548 (-0.196) | 0.747 (+0.003) | 0.752 (+0.008) | 0.753 (+0.009) | 0.425 |

## Table 4 — Real Per-Token Latency Profile

- **Device:** `cpu` (`gpt2`)
- **Vanilla KV-cached decode:** `159.88 ms/tok`
- **TRUEGUARD online decode:** `143.37 ms/tok` (sensor + probe math: `19.14 ms/tok`)
- **TRUEGUARD post-pass decode:** `390.73 ms/tok`
- **5-sample consistency baseline:** `1361.49 ms/tok` (**9.5x speedup** for TRUEGUARD online)
