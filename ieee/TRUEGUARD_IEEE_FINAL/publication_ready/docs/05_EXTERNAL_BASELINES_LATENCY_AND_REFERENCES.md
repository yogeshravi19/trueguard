# External Baseline Verification, Fair Cost Comparison, and References

## 1. External Baseline Implementation Fidelity
- **SelfCheckGPT-NLI** (Manakul et al., EMNLP 2023): Uses official `potsawee/deberta-v3-large-mnli` (`{0: entailment, 1: contradiction}`), `M = 10` stochastic samples (`T=0.7, top_p=0.9`), exact `(sentence, sample)` input ordering. *Documented deviations:* TriviaQA short-phrase answers (mean 13.98 words, 0 empty) are scored as a single sentence; NLI ran in `float16`.
- **Semantic Entropy** (Kuhn et al., ICLR 2023; Farquhar et al., Nature 2024): Uses official `microsoft/deberta-large-mnli` (`{0: contradiction, 1: neutral, 2: entailment}`), `M = 10` samples, exact case-insensitive duplicate fast-path, length-normalized sequence log-probabilities from unwarped logits (plus discrete SE, matching within `0.0003` AUROC). *Documented deviation:* Uses Farquhar et al.'s relaxed bidirectional entailment rule (neither direction contradicts and at least one entails) rather than Kuhn et al.'s stricter both-directions-entail rule.
- **Zero Test Leakage:** Calibration thresholds (Youden's J) were fit strictly on the 250-question calibration split.
- **Supervision Fairness Disclosure (Critical):** On TriviaQA (`n_cal=250, n_test=250`), `TRUEGUARD_4sensor` (`0.7876` AUROC) and `TRUEGUARD_ISP_only` (`0.7706` AUROC) were **trained from scratch on the `250` labeled TriviaQA calibration questions** (`det_tqa.fit(F_cal, H_cal, y_cal)`), whereas `SelfCheckGPT-NLI` (`0.7477`), `Semantic Entropy` (`0.6859`), `Predictive Entropy` (`0.6583`), and `NLL` (`0.4678`) are **completely label-free for ranking** (using the 250 calibration labels only for the binary F1 threshold). Without target labels, zero-shot `TRUEGUARD_Pooled_ZeroShot` achieves only `0.5504` AUROC / `0.6342` AURC. The comparison therefore evaluates a **few-shot target-refitted (`K=250`) single-pass white-box detector** against **label-free multi-sample external baselines**.

## 2. Fair Computational Cost Accounting (Non-Equivalence Disclosure)
- **Non-Equivalent Timing Protocols:** The original `real_latency.json` measured TRUEGUARD (`0.8285 s/q` post-pass, `0.9082 s/q` online) vs. sequential 5-sample decoding (`3.8106 s/q`) under controlled identical conditions (`attn_implementation='eager'`, `batch_size=1`, `min_new_tokens=24`). By contrast, the external baseline Colab run batched all `M = 10` samples in parallel (`batch_size=10`) with PyTorch's fast `sdpa` kernel and early EOS stopping (`0.6545 s/q` sampling + `0.0523 s/q` SelfCheckGPT NLI, omitting the initial greedy generation; `1.0078 s/q` Semantic Entropy bidirectional NLI).
- **Therefore, direct wall-clock speedup over SelfCheckGPT-NLI is NOT claimed.**
- **Supported Cost Claims:**
  1. Under identical sequential single-query serving (`real_latency.json`), TRUEGUARD is **4.20x–4.60x faster** than 5x multi-sampling (`+15.9%` post-pass / `+27.1%` online monitoring overhead).
  2. Architecturally, TRUEGUARD requires **1 LLM generation and 0 external NLI models**, whereas SelfCheckGPT-NLI and Semantic Entropy require **10–11 LLM generations** plus an external **435M-parameter DeBERTa-large model** (`+1.00–2.47 GB` VRAM).
  3. Monitoring-only latency excludes Tier 1 resampling and Tier 2 Wikipedia retrieval mitigation overhead on flagged queries.

## 3. Core References for External Baselines
- P. Manakul, A. Liusie, and M. J. F. Gales, "SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models," in *Proc. EMNLP*, 2023, pp. 9004–9017.
- L. Kuhn, Y. Gal, and S. Farquhar, "Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation," in *Proc. ICLR*, 2023.
- S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal, "Detecting hallucinations in large language models using semantic entropy," *Nature*, vol. 630, pp. 625–630, 2024.
