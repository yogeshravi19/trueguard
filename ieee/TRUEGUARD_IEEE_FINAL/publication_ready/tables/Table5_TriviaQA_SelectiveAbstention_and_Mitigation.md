# Table V — TriviaQA Closed-Book Selective Abstention vs. Full Three-Tier Controller Intervention Ablation (n_test = 250)

| System / Method (TriviaQA n_test=250) | Role | AUROC | AURC [95% CI] | Coverage (Answered) | Correct / Answered | Selective Accuracy | System Halluc. Rate | Active Repairs / Broken | dAURC vs TG (p_Holm*) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Greedy Baseline (No Mitigation) | Unfiltered baseline | — | — | 100.0% (250/250) | 85 / 250 | 34.00% | 66.00% | 0 / 0 | — |
| TRUEGUARD 4-Sensor — Pure Abstain-Only | Primary selective abstention | 0.7876 | 0.4360 [0.360, 0.524] | 46.0% (115/250) | 64 / 115 | 55.65% | 20.40% | 0 / 0 | — |
| TRUEGUARD Full 3-Tier Controller (Ablation) | Intervention ablation (T1+T2+T3) | 0.7876 | — (fixed operating pt) | 46.0% (115/250) | 63 / 115 | 54.78% (-0.87%) | 20.80% | 4 fixed / 3 broken | No net gain over abstain-only |
| TRUEGUARD ISP-Only — Abstain-Only | Single-sensor ablation | 0.7706 | 0.4473 [0.369, 0.532] | 46.0% (115/250) | 62 / 115 | 53.91% | 21.20% | 0 / 0 | -0.0113 (pH=0.451, n.s.) |
| Scalars-Only (AAS+EEM+DST) — Abstain-Only | No-ISP ablation | 0.7130 | 0.4891 [0.404, 0.577] | 46.0% (115/250) | 57 / 115 | 49.57% | 23.20% | 0 / 0 | -0.0531 (p_boot<=0.001) |
| Predictive Entropy — Abstain-Only | Token uncertainty baseline | 0.6583 | 0.5309 [0.448, 0.617] | 46.0% (115/250) | 52 / 115 | 45.22% | 25.20% | 0 / 0 | -0.0949 (pH=0.006) |
| Length-Norm. NLL — Abstain-Only | Token likelihood baseline | 0.4678 | 0.6843 [0.603, 0.760] | 46.0% (115/250) | 36 / 115 | 31.30% | 31.60% | 0 / 0 | -0.2483 (pH=0.006) |

*Sources: `results/mitigation_report.json`, `research_improvements/phase5_mitigation_deep_analysis.json`, `external_validation/external_validation/external_baselines_report.json`, and `reviewer_response/reviewer_controls_results.json`. Mitigation Reframing: Risk-based selective abstention is the primary demonstrated mitigation outcome (reducing system-wide incorrect outputs from 66.0% to 20.4% and raising selective accuracy from 34.00% to 55.65% at 46.0% coverage). The full 3-tier controller (81 Safe, 23 Tier-1 Resample, 11 Tier-2 TF-IDF Retrieval, 135 Tier-3 Abstain) achieved 54.78% (63/115) — repairing 4 hallucinations while breaking 3 originally correct answers — and therefore did NOT provide a net benefit over pure abstain-only on TinyLlama-1.1B. *Finite-sample bootstrap p-values use B=1000 (`p >= 1/(B+1)`).*
