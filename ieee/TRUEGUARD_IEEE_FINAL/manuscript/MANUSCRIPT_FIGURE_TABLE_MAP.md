# Manuscript Figure and Table Traceability Map (IEEE Access Ready — All 9 Figures & 8 Tables Retained)

**Manuscript:** `E:\trueguard\ieee\overleaf\TRUEGUARD_Manuscript_Refined.md` *(synced copy at `E:\trueguard\ieee\TRUEGUARD_IEEE_FINAL\manuscript\TRUEGUARD_Manuscript_Refined.md`)*  
**Figures Directory:** `E:\trueguard\ieee\overleaf\figures\` *(synced with `manuscript/figures/` and `publication_ready/figures/`)*  
**Audit Record Preserved Unchanged:** `MANUSCRIPT_FIGURE_TABLE_FINAL_VERIFICATION.md`  
**Policy:** All **9 figures** (`FIGURE 1`–`FIGURE 9`) and all **8 tables** (`TABLE I`–`TABLE VIII`) are retained intact for complete two-column IEEE Access LaTeX compilation.

---

## 1. Figures Map (All 9 Figures Ready as Actual Files)

| Fig # | Sec. | Final Filename(s) (`figures/`) | Type & Source Evidence | Intended LaTeX Placement | Status |
| :---: | :---: | :--- | :--- | :---: | :---: |
| **FIGURE 1** | III-A | `Fig1_TRUEGUARD_Architecture.pdf`, `.svg`, `.png` *(NEW — created in this task; did not exist prior)* | **Conceptual** — Matches `tg_pipeline.py` & `tg_controller.py` (frozen TinyLlama-1.1B, 4 parallel sensors, 7-dim fusion, 3-tier controller) | `figure*` (full 2-col width, vector PDF) | **READY (CONCEPTUAL, VISUALLY VERIFIED)** |
| **FIGURE 2** | V-A | `Fig5a_ROC_HaluEval_QA.png`, `Fig5b_ROC_TruthfulQA.png`, `Fig5c_ROC_HaluEval_General.png` | **Experimental** — `predictions/in_domain_oof_*.npz`, `results/final_experiment_report.json` | `figure*` (3-panel horizontal subfigures) | **VERIFIED (300 DPI)** |
| **FIGURE 3** | V-C | `Fig6_Ablation_HaluEval_General.png` *(caption corrected in manuscript; original plot preserved)* | **Experimental** — `results/final_experiment_report.json` (AUROC bars only; low-FPR recall in Table III) | `figure` (single-column) | **VERIFIED (CAPTION FIXED)** |
| **FIGURE 4** | V-D | `Fig4_InDomain_5x5_Transfer_Matrix_v2.pdf`, `.png` *(NEW unclipped v2; original `.png` preserved as backup)* | **Experimental** — `results/final_experiment_report.json` (`in_domain_transfer_5x5` + 5-fold CV diagonal) | `figure` (single-column, vector PDF) | **VERIFIED (TITLE FIXED)** |
| **FIGURE 5** | V-E | `Fig2_TargetDomain_FewShot_Refitting_vs_Baselines.png` | **Experimental** — `unseen_zeroshot_*.npz`, `phase3_fewshot_adaptation_results.json`, `reviewer_controls_results.json` | `figure*` (full 2-col width) | **VERIFIED (300 DPI)** |
| **FIGURE 6** | V-F, V-G | `Fig8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.png` | **Experimental** — `phase2_cross_domain_diagnostics.json`, `cosine_and_eem_controls.json` | `figure*` (full 2-col width, 2 panels) | **VERIFIED (300 DPI)** |
| **FIGURE 7** | V-G | `Fig1_Sensor_Sign_Inversion_9Datasets.png` | **Experimental** — `phase2_cross_domain_diagnostics.json` | `figure` or `figure*` (readable at 0.48–0.75 textwidth) | **VERIFIED (300 DPI)** |
| **FIGURE 8** | V-H | `Fig7_External_Baselines_RiskCurve.png` | **Experimental** — `external_validation/external_validation/external_baselines_report.json` | `figure` (single-column) | **VERIFIED (300 DPI)** |
| **FIGURE 9** | V-I | `Fig3_TriviaQA_Matched_Coverage_RiskCurve.png` | **Experimental** — `phase5_mitigation_deep_analysis.json`, `mitigation_report.json` | `figure` (single-column) | **VERIFIED (300 DPI)** |

---

## 2. Tables Map (All 8 Tables Verified — `216/216` Cells Exact, Zero Deletions)

| Table # | Sec. | Frozen Source File (`publication_ready/tables/`) | Intended LaTeX Placement & Formatting | Status |
| :---: | :---: | :--- | :--- | :---: |
| **TABLE I** | IV-B | `Table1_Dataset_Methodology_and_Splits.md` | `table*` (full 2-col width, `booktabs`, standard IEEE `\footnotesize`) | **VERIFIED** |
| **TABLE II** | V-A, V-B | `Table2_InDomain_5Fold_GroupCV.md` + `final_pre_manuscript_checks.json` | `table*` (full 2-col width, `booktabs` + `\setlength{\tabcolsep}{3.5pt}`) | **VERIFIED** |
| **TABLE III** | V-C | `Table4_FourSensor_Ablation_and_Complementarity.md` | `table*` (full 2-col width, `booktabs`) | **VERIFIED** |
| **TABLE IV** | V-E | `Table3_TargetDomain_FewShot_Refitting.md` | `table*` (full 2-col width, `booktabs`) | **VERIFIED** |
| **TABLE V** | V-F, V-G | `Table8_CrossDomain_Diagnostics_Cosine_and_LengthControlled_EEM.md` + `final_pre_manuscript_checks.json` | `table*` (full 2-col width, `booktabs`) | **VERIFIED** |
| **TABLE VI** | V-H | `Table7_External_Baselines_TriviaQA.md` | `table*` (full 2-col width, `booktabs`, explicit `Supervision` column) | **VERIFIED** |
| **TABLE VII** | V-I | `Table5_TriviaQA_SelectiveAbstention_and_Mitigation.md` | `table*` (full 2-col width, `booktabs`) | **VERIFIED** |
| **TABLE VIII** | V-J | `Table6_Inference_Latency_Profiling.md` | `table` (single-column, compact 4 rows) | **VERIFIED** |
