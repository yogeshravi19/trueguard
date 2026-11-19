# Statistical Reporting & Verification Flags

## 1. Verified Statistical Methods
- **In-Domain 5-Fold Group CV:** `GroupKFold(n_splits=5)` preserving prompt/document/question groups; 95% CIs computed via **500 group-level bootstrap resamples** (resampling whole groups, never splitting pairs). Paired sensor comparisons (`Full` vs. `Best Single` / `ISP-only` / `LOSO`) use paired group bootstrap.
- **TriviaQA Matched-Coverage Mitigation:** 95% CIs and paired `p`-values on `AURC` and `Acc@46%` computed via **1,000 paired bootstrap resamples** on the exact same 250 test questions.
- **Few-Shot Adaptation (10 Seeds):** Mean +/- SD and 95% `t`-intervals across 10 fixed seeds (`0..9`) on identical, group-disjoint 40% held-out test sets (`group_overlap = 0`), with Holm-Bonferroni correction across all 36 tests.

## 2. Explicit Statistical Flag (Repeated Seeds + Shared Test Set)
- **Flagged Nuance:** In the 10-seed few-shot table (`Table III`), the 1-sample / paired `t`-tests across the 10 seeds quantify **adaptation-sample draw variance** while holding the 40% test set fixed (Nadeau & Bengio, 2003). They do *not* fold test-set finite-sample variance into the same `t`-statistic.
- **Impact Assessment:**
  - **Robust Large Effects (`K=250` vs. Unadapted Fusion & vs. Raw EEM on FaithDial/WikiBio/FEVER):** Effect sizes are massive (`+0.178` to `+0.335` AUROC; non-overlapping 95% group-bootstrap test CIs vs. zero-shot CIs; Cohen's `d = 4.3` to `27.7`). These improvements remain unambiguously significant even after accounting for test-set variance.
  - **Marginal Small Effects (`Full` vs. `ISP_only` at `K=250`):** Differences are small (`-0.009` to `-0.014` AUROC). Even though FEVER `K=250` yielded `p_Holm = 0.045` under fixed-test seed pairing, this difference is **within the test-set bootstrap uncertainty** and must be reported as practically comparable / non-robust rather than a definitive superiority of ISP-only.
