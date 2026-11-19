# TRUEGUARD — IEEE Access Publication Evidence Package

**Status:** **READY TO WRITE IEEE ACCESS MANUSCRIPT**  
**Directory:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\publication_ready`

## Contents
### 1. Verified Publication Tables (`tables/` — both `.md` and `.csv`)
- `Table1_Dataset_Methodology_and_Splits` — All 10 datasets, raw/usable rows, groups, labels, exclusions.
- `Table2_InDomain_5Fold_GroupCV` — 5-fold GroupKFold CV across 5 in-domain datasets (AUROC + 95% CI, AUPRC, F1, Prec, Rec, ECE, Brier, single sensors, raw baselines).
- `Table3_Original_vs_FewShot_Adapted` — Identical 40% held-out test set comparison of Zero-Shot Unadapted vs. Raw EEM/ENT/NLL vs. `K=50, 100, 250` Few-Shot Adaptation (10 seeds + Holm-Bonferroni `p`).
- `Table4_FourSensor_Ablation_and_Complementarity` — Leave-one-sensor-out ablations & low-FPR unique failure catches.
- `Table5_TriviaQA_MatchedCoverage_Mitigation` — Matched 46% coverage & full risk-coverage AURC comparisons vs. ISP-only, Scalars, Entropy, and NLL.
- `Table6_Inference_Latency_Profiling` — Genuine CUDA T4 per-token timings and speedup vs. 5x multi-sampling.

### 2. Publication-Quality Figures (`figures/` — 300 DPI PNGs)
- `Fig1_Sensor_Sign_Inversion_9Datasets.png`
- `Fig2_FewShot_Target_Adaptation_Curves.png`
- `Fig3_TriviaQA_Matched_Coverage_RiskCurve.png`
- `Fig4_InDomain_5x5_Transfer_Matrix.png`
- `Fig5a_ROC_HaluEval_QA.png`
- `Fig5b_ROC_TruthfulQA.png`
- `Fig5c_ROC_HaluEval_General.png`
- `Fig6_Ablation_HaluEval_General.png`

### 3. Methodology, Baselines, Statistics & Disclosures (`docs/`)
- `01_SUPPORTED_CONTRIBUTIONS_AND_LIMITATIONS.md`
- `02_STATISTICAL_VALIDATION_AND_FLAGS.md`
- `03_BASELINE_COMPARISON_MATRIX.md`
- `04_REPRODUCIBILITY_MANIFEST.json`
