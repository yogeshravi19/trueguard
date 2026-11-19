# Clean Two-Column Academic Review Manuscript Report

**Date:** 2026-11-20  
**Review PDF:** [TRUEGUARD_REVIEW_MANUSCRIPT_10P.pdf](file:///E:/trueguard/ieee/overleaf/TRUEGUARD_REVIEW_MANUSCRIPT_10P.pdf) (`10` pages, `1.22 MB`, clean standard 10pt two-column academic layout, black body text, subtle blue `#164A75` title/section headings, zero journal logos or publisher headers)  
**Editable Review LaTeX Source:** [review_main.tex](file:///E:/trueguard/ieee/overleaf/review_main.tex) (full build folder: [review_manuscript](file:///E:/trueguard/ieee/overleaf/review_manuscript))  
**Preserved Official IEEE Access Project (Untouched):** [TRUEGUARD_IEEE_ACCESS_FINAL.pdf](file:///E:/trueguard/ieee/overleaf/TRUEGUARD_IEEE_ACCESS_FINAL.pdf) (`15` pages), [main.tex](file:///E:/trueguard/ieee/overleaf/main.tex), [TRUEGUARD_IEEE_ACCESS_OVERLEAF.zip](file:///E:/trueguard/ieee/overleaf/TRUEGUARD_IEEE_ACCESS_OVERLEAF.zip), and `ieee_access_build/`.

---

## 1. Final Compiled Page Count & Verification
- **Actual Page Count:** **`10` pages** (including all references; within the 10-page target at normal 10pt font and standard `0.72in` margins without shrinking text or distorting figures).
- **Abstract Length:** **~186 words** (within the requested 150–200 word range; avoids listing dense numerical tables while stating all three core empirical conclusions).
- **Equations Preserved:** All **`10`** numbered equations (`(1)`–`(10)`) intact with symbol definitions.
- **Clickable Hyperlinks Verified (PyMuPDF):** **`89` clickable internal links** (`70` IEEE numerical citations `[1]`–`[43]`, `6` figure links, `7` table links, `6` section links), **`0` broken links**, **`0` undefined citations**, **`0` undefined references**.

---

## 2. Retained Visuals in the 10-Page Review Manuscript (`5` Figures, `6` Tables)

### Retained Figures (`5`)
1. **Fig. 1** (`Fig1_TRUEGUARD_Architecture.pdf`): TRUEGUARD single-pass white-box architecture and three-tier selective controller (`Sec. III-A`).
2. **Fig. 2** (`Fig2_TargetDomain_FewShot_Refitting_vs_Baselines.png`): Target-domain few-shot refitting (`K = 50, 100, 250`) vs. Source Risk Recalibration, 1D EEM, 1D LEN, and Answer TF-IDF (`Sec. V-B`).
3. **Fig. 3** (`Fig8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.png`): Two-panel domain-shift diagnostic — (a) within-domain vs. cross-domain ISP probe cosine alignment; (b) raw vs. length-controlled EEM AUROC (`Sec. V-C`).
4. **Fig. 4** (`Fig7_External_Baselines_RiskCurve.png`): TriviaQA risk–coverage selective prediction curves vs. `SelfCheckGPT-NLI`, `Semantic Entropy`, `Predictive Entropy`, and `NLL` (`Sec. V-D`).
5. **Fig. 5** (`Fig3_TriviaQA_Matched_Coverage_RiskCurve.png`): TriviaQA matched-coverage selective prediction curves showing the `3-Tier Controller` (`54.8%`) point visibly below `Pure Abstain-Only` (`55.6%`) (`Sec. V-D`).

### Retained Tables (`6`)
1. **TABLE I** (`tab:datasets`): 10-Dataset Benchmark Suite, Protocol Roles, Splits, and Exclusions (`Sec. IV-A`).
2. **TABLE II** (`tab:indomain`): In-Domain 5-Fold Group CV With Dataset-Artifact Controls (`LEN`, `TF-IDF`, Shuffled, Length-Matched `|ΔL| ≤ 2` + paired `p_boot`) (`Sec. V-A`).
3. **TABLE III** (`tab:fewshot`): Target-Domain Few-Shot Refitting (`K = 50, 100, 250`) vs. Source Recalibration & Simple Baselines (`Sec. V-B`).
4. **TABLE IV** (`tab:diag`): Empirical Domain-Shift Diagnostics — Full & Equal-`N=900` Probe Alignment and Length-Controlled EEM (`Sec. V-C`).
5. **TABLE V** (`tab:external`): Head-to-Head External Baselines on TriviaQA (Supervision-Distinguished, including `TRUEGUARD_Pooled_ZS`) (`Sec. V-D`).
6. **TABLE VI** (`tab:mitigation`): TriviaQA Selective Abstention (`64/115 = 55.65%`) vs. Full 3-Tier Controller Ablation (`63/115 = 54.78%`, `4` fixed / `3` broken) (`Sec. V-D`).

---

## 3. Optional Visuals Excluded From Main Review Manuscript (Preserved Untouched on Disk)

| Excluded Visual | Preserved File Location | Reason Excluded From 10-Page Review Paper | Where Essential Findings Remain Reported |
| :--- | :--- | :--- | :--- |
| **In-Domain 3-Panel ROC Curves** *(official Fig. 2)* | `overleaf/figures/Fig5a_ROC_HaluEval_QA.png`, `Fig5b_ROC_TruthfulQA.png`, `Fig5c_ROC_HaluEval_General.png` | Duplicates discrimination values already reported with 95% CIs and artifact controls in Table II | **TABLE II** & **Sec. V-A** |
| **HaluEval-General Ablation Bar Chart** *(official Fig. 3)* | `overleaf/figures/Fig6_Ablation_HaluEval_General.png` | Single-dataset AUROC bar chart; full 5-dataset leave-one-sensor-out ablation summary is more informative in prose | **Sec. V-A** (`-ISP` drop `-0.0584` to `-0.2709`, `-AAS/-EEM/-DST <= 0.0018`, `ISP_logit = +2.9353`) |
| **In-Domain 5×5 Transfer Matrix** *(official Fig. 4)* | `overleaf/figures/Fig4_InDomain_5x5_Transfer_Matrix_v2.pdf` | Secondary to the 4 unseen cross-domain benchmarks (`Table III`, `Table IV`, `Fig. 3`) | **Sec. V-B & V-C** (unseen zero-shot `0.4597–0.5205`, equal-`N` cosine diagnostics) |
| **9-Dataset Raw Sensor Heatmap** *(official Fig. 7)* | `overleaf/figures/Fig1_Sensor_Sign_Inversion_9Datasets.png` | Superseded by the more informative raw-vs.-length-controlled EEM diagnostic in Fig. 3(b) and Table IV | **Fig. 3(b)** & **TABLE IV** |
| **Leave-One-Sensor-Out Ablation Table** *(official Table III)* | `publication_ready/tables/Table4_FourSensor_Ablation_and_Complementarity.md` | All key ranges (`-ISP`, `-AAS/-EEM/-DST`, `ISP_logit >96%`, HaluEval-General union recall `0.348 -> 0.529`) are reported cleanly in one paragraph | **Sec. V-A** |
| **Controlled Sequential Latency Table** *(official Table VIII)* | `publication_ready/tables/Table6_Inference_Latency_Profiling.md` | Compact 4-row table; all four timings (`29.78`, `34.52`, `37.84`, `158.77 ms/tok`), speedups (`4.60x`/`4.20x`), and batching non-equivalence are stated verbatim in prose | **Sec. V-D** |
