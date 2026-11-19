# TRUEGUARD — IEEE Access Publication Evidence Package (v3.0 Post-Review Reconciled)

**Status:** **READY TO DRAFT IEEE ACCESS MANUSCRIPT**  
**Directory:** `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\publication_ready`  
**Prior Pre-Review Version Backup:** [publication_ready_v1_pre_review_backup](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready_v1_pre_review_backup)  
**Primary Readiness Report:** [FINAL_RESEARCH_READINESS_AFTER_REVIEW.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/FINAL_RESEARCH_READINESS_AFTER_REVIEW.md)  
**Final Pre-Manuscript Verification:** [FINAL_PRE_MANUSCRIPT_VERIFICATION.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/FINAL_PRE_MANUSCRIPT_VERIFICATION.md)  
**Reviewer Validation Audit:** [CLAUDE_REVIEW_VALIDATION_REPORT.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/reviewer_response/CLAUDE_REVIEW_VALIDATION_REPORT.md)

---

## 1. Verified Publication Tables (`tables/` — both `.md` and `.csv`)
- **Table I:** [Table1_Dataset_Methodology_and_Splits.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table1_Dataset_Methodology_and_Splits.md) — 10-dataset suite, protocol roles, splits, exclusions.
- **Table II:** [Table2_InDomain_5Fold_GroupCV.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table2_InDomain_5Fold_GroupCV.md) — In-domain 5-fold GroupKFold CV **with dataset-artifact controls** (`LEN`, answer-text `TF-IDF`, shuffled-label check, length-matched `|ΔL| ≤ 2` subset).
- **Table III:** [Table3_TargetDomain_FewShot_Refitting.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table3_TargetDomain_FewShot_Refitting.md) — **Target-domain few-shot refitting (target-only probe training)** across `K ∈ {50, 100, 250}` vs. exact Colab `.npz` zero-shot, source risk recalibration, `1D EEM`, `1D LEN`, and answer-text `TF-IDF`.
- **Table IV:** [Table4_FourSensor_Ablation_and_Complementarity.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table4_FourSensor_Ablation_and_Complementarity.md) — Leave-one-sensor-out ablations (showing ISP dominance) & low-FPR complementarity.
- **Table V:** [Table5_TriviaQA_SelectiveAbstention_and_Mitigation.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table5_TriviaQA_SelectiveAbstention_and_Mitigation.md) — TriviaQA closed-book **selective abstention** (`55.65%`, `64/115`) vs. **full 3-tier controller ablation** (`54.78%`, `63/115`, `4` fixed / `3` broken) and internal/uncertainty baselines.
- **Table VI:** [Table6_Inference_Latency_Profiling.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table6_Inference_Latency_Profiling.md) — Controlled sequential CUDA T4 latency (`eager`, `bs=1`) with non-equivalence disclosure vs. GPU-batched `M=10` baselines.
- **Table VII:** [Table7_External_Baselines_TriviaQA.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table7_External_Baselines_TriviaQA.md) — Head-to-head comparison against `SelfCheckGPT-NLI` (`M=10`) and `Semantic Entropy` (`M=10`) on identical `250` TriviaQA test questions with finite-sample Holm-Bonferroni bootstrap `p`-values.
- **Table VIII:** [Table8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/tables/Table8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.md) — Within-domain split-half vs. cross-domain ISP probe cosine alignment and length-controlled EEM audit across all 9 datasets.

## 2. Publication-Quality Figures (`figures/` — 300 DPI PNGs)
- `Fig1_Sensor_Sign_Inversion_9Datasets.png` — Raw sensor AUROCs across 9 teacher-forced datasets.
- `Fig2_TargetDomain_FewShot_Refitting_vs_Baselines.png` — Target-only few-shot refitting (`K=50, 100, 250`) vs. source recalibration, `1D EEM`, `1D LEN`, and `TF-IDF`.
- `Fig3_TriviaQA_Matched_Coverage_RiskCurve.png` — TriviaQA risk-coverage selective prediction curves (internal sensors & uncertainty baselines).
- `Fig4_InDomain_5x5_Transfer_Matrix.png` — In-domain 5×5 cross-dataset transfer matrix.
- `Fig5a_ROC_HaluEval_QA.png`, `Fig5b_ROC_TruthfulQA.png`, `Fig5c_ROC_HaluEval_General.png` — Representative in-domain ROC curves.
- `Fig6_Ablation_HaluEval_General.png` — Leave-one-sensor-out ablation on imbalanced HaluEval-General.
- `Fig7_External_Baselines_RiskCurve.png` — TriviaQA risk-coverage curves vs. `SelfCheckGPT-NLI` and `Semantic Entropy`.
- `Fig8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.png` — Within-domain vs. cross-domain ISP probe cosine alignment and length-controlled EEM behavior.

## 3. Reconciled Documentation & Reproducibility Manifest (`docs/`)
- [01_SUPPORTED_CONTRIBUTIONS_AND_LIMITATIONS.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/01_SUPPORTED_CONTRIBUTIONS_AND_LIMITATIONS.md)
- [02_STATISTICAL_VALIDATION_AND_FLAGS.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/02_STATISTICAL_VALIDATION_AND_FLAGS.md)
- [03_BASELINE_COMPARISON_MATRIX.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/03_BASELINE_COMPARISON_MATRIX.md)
- [05_EXTERNAL_BASELINES_LATENCY_AND_REFERENCES.md](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/05_EXTERNAL_BASELINES_LATENCY_AND_REFERENCES.md)
- [06_REPRODUCIBILITY_MANIFEST_FINAL.json](file:///E:/trueguard/ieee/TRUEGUARD_IEEE_FINAL/publication_ready/docs/06_REPRODUCIBILITY_MANIFEST_FINAL.json) (v3.0, linking every table to immutable source artifacts)
