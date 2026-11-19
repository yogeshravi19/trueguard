# Baseline Comparison Matrix (Reproduced vs. Literature Reference — Post-Review Reconciled)

## A. Experimentally Reproduced Baselines (Identical Frozen TinyLlama-1.1B, Data, and Splits)

| Baseline | Category | Scope & Fidelity | Key Finding vs. TRUEGUARD |
| :--- | :--- | :--- | :--- |
| **SelfCheckGPT-NLI** (Manakul et al., EMNLP 2023) | Black-box multi-sample (`M=10` + `potsawee/deberta-v3-large-mnli`) | TriviaQA (`n_cal=250, n_test=250`) | `0.7477` AUROC / `0.4659` AURC / `0.8537` AUPRC / `50.4%` Acc@46%. TRUEGUARD (`0.7876` / `0.4360` / `0.8460` / `55.6%`) is competitive (`p_Holm = 0.478 / 0.362`, n.s.) with `1` generation and `0` external NLI models. |
| **Semantic Entropy (LN & Discrete)** (Kuhn et al., ICLR 2023; Farquhar et al., Nature 2024) | Black-box/white-box multi-sample (`M=10` + `microsoft/deberta-large-mnli`) | TriviaQA (`n_cal=250, n_test=250`) | `0.6859` LN (`0.6856` Disc) AUROC / `0.5411` AURC / `49.6%` Acc@46%. TRUEGUARD significantly outperforms both (`p_Holm = 0.012` AUROC, `0.006` AURC). |
| **ISP-Only (SAPLMA-style multi-layer probe)** (Azaria & Mitchell, 2023) | White-box linear probe | All 10 datasets, identical hidden states & splits | Matches 4-sensor fusion in-domain (`±0.002`) and on TriviaQA (`0.7706` vs. `0.7876`, `p_Holm = 0.478`, n.s.); collapses zero-shot (`0.46–0.52`). |
| **Predictive Entropy (`ENT_mean`)** | Single-pass token uncertainty | All 10 datasets, identical logits | Strong zero-shot on FaithDial (`0.745`) & XSum (`0.667`); significantly worse than TRUEGUARD on TriviaQA (`0.6583` AUROC, `0.5309` AURC, `p_Holm = 0.006`). |
| **Length-Normalized NLL (`NLL_mean`)** | Single-pass token likelihood | All 10 datasets, identical logits | Inverted on HaluEval (`0.095–0.296`); weak on TriviaQA (`0.4678` AUROC, `0.6843` AURC, `p_Holm = 0.006`). |
| **1D EEM (Shannon + Rényi-2)** | Single-pass unsupervised/1D-calibrated | All 9 teacher-forced datasets | Beats TRUEGUARD at `K=50` on FaithDial (`0.7473` vs. `0.6987`) and XSum (`0.6082` vs. `0.5401`); length-free on FaithDial (`0.7662` quartile-mean) & XSum (`0.6648`). |
| **Answer-Text TF-IDF (Word 1-2 + Char 3-5)** | Surface-text artifact control (Zero LLM) | 5 in-domain + 4 target-refit datasets | Exposes strong HaluEval style artifacts (`0.9661` QA, `0.9539` Summ); beats TRUEGUARD at `K=50` on WikiBio & FEVER; surpassed by TRUEGUARD in-domain (`+0.022` to `+0.071`) and at `K=250` on FaithDial/FEVER/WikiBio. |
| **1D Answer Length (`LEN`)** | Length-artifact control | 5 in-domain + 4 target-refit datasets | Exposes severe HaluEval-QA length confound (`0.9572` CV); matches `K=250` TRUEGUARD on XSum (`0.6445` vs. `0.6456`). |
| **Source Risk Recalibration (`SrcRecal`)** | 1D Platt/sign recalibration of source risk | 4 unseen target datasets (`K=50, 100, 250`) | Remains at chance (`0.4957–0.5242`), confirming zero recoverable source-probe transfer. |
| **Pure Abstain-Only vs. Full 3-Tier Controller** | Selective abstention vs. active repair ablation | TriviaQA (`n_test=250`, matched `46.0%` coverage) | Abstain-only achieves `55.65%` (`64/115`) vs. Full 3-Tier Controller `54.78%` (`63/115`; `4` repaired, `3` broken) — no demonstrated net benefit from Tier 1/2 repair. |
| **5x Sequential Multi-Sample Decoding Cost** | Controlled latency baseline | CUDA T4, `eager`, `bs=1`, `25×24` tokens | `158.77 ms/tok` vs. TRUEGUARD `34.52 ms` post-pass (`4.60x`) / `37.84 ms` online (`4.20x`). *Not directly comparable to GPU-batched (`bs=10, sdpa`) Colab timings.* |

## B. Published Literature Methods (Contextual Reference Only — Not Reproduced on TinyLlama-1.1B)
- **CCS** (Burns et al., ICLR 2023), **ITI** (Li et al., NeurIPS 2023), **EigenScore / INSIDE** (Chen et al., ICLR 2024), **Lookback Lens** (Chuang et al., ACL 2024): Discussed in Related Work and Limitations; no direct numerical superiority is claimed against these un-reproduced white-box methods.
